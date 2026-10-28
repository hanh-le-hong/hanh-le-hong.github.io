#!/usr/bin/env python3
"""
AiPRIL Local CMS & Static Server
Serves the website and allows 1-click saving of Markdown posts from /studio.html
into posts/<slug>.md and posts/index.json.
"""

import http.server
import json
import os
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
POSTS_DIR = ROOT_DIR / "posts"
INDEX_FILE = POSTS_DIR / "index.json"


class CMSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT_DIR), **kwargs)

    def do_POST(self):
        if self.path != "/api/posts":
            self.send_error(404, "Endpoint not found")
            return

        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length)
        try:
            data = json.loads(raw_body.decode("utf-8"))
        except Exception:
            self.send_error(400, "Invalid JSON")
            return

        slug = re.sub(r"[^a-z0-9-]+", "-", data.get("slug", "").lower()).strip("-")
        title = data.get("title", "").strip()
        category = data.get("category", "The Craft").strip()
        date = data.get("date", "").strip()
        summary = data.get("summary", "").strip()
        read_time = data.get("readTime", "3 min read").strip()
        content = data.get("content", "")

        if not slug or not title:
            self.send_error(400, "Missing slug or title")
            return

        POSTS_DIR.mkdir(parents=True, exist_ok=True)

        # 1. Write the Markdown file: posts/<slug>.md
        md_path = POSTS_DIR / f"{slug}.md"
        md_path.write_text(content, encoding="utf-8")

        # 2. Update posts/index.json
        posts = []
        if INDEX_FILE.exists():
            try:
                posts = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
            except Exception:
                posts = []

        entry = {
            "slug": slug,
            "title": title,
            "date": date,
            "category": category,
            "summary": summary,
            "readTime": read_time,
        }

        updated = False
        for i, p in enumerate(posts):
            if p.get("slug") == slug:
                posts[i] = entry
                updated = True
                break
        if not updated:
            posts.insert(0, entry)

        # Sort newest first
        posts.sort(key=lambda x: x.get("date", ""), reverse=True)
        INDEX_FILE.write_text(
            json.dumps(posts, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        response = json.dumps({"ok": True, "slug": slug}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "4174"))
    server = http.server.ThreadingHTTPServer(("", port), CMSRequestHandler)
    print(f"AiPRIL CMS Server running at http://localhost:{port}")
    server.serve_forever()
