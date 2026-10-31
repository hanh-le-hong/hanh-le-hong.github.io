#!/usr/bin/env python3
"""
AiPRIL Static SEO & Agentic Publisher (zero external dependencies).

Reads `posts/index.json` + `posts/<slug>.md` and pre-renders:
  1. `writing/<slug>/index.html` (static HTML, OpenGraph, BlogPosting + BreadcrumbList Schema)
  2. `index.html` (syncs pre-rendered `#posts-feed` links between markers)
  3. `sitemap.xml` (clean canonical URLs + accurate `<lastmod>`, no deprecated tags)
  4. `rss.xml` (RSS 2.0 feed)
  5. `llms.txt` (curated site & Markdown index for AI agents)
"""

from __future__ import annotations

import datetime as dt
import html
import json
import re
from email.utils import format_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://iced-latte.com"


def slugify_heading(text: str) -> str:
    clean = re.sub(r"<[^>]+>", "", text).lower()
    clean = re.sub(r"[^a-z0-9]+", "-", clean).strip("-")
    return clean or "section"


def format_inline(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)

    def replace_link(match: re.Match[str]) -> str:
        label, url = match.group(1), match.group(2)
        if url.startswith(("http://", "https://")) and not url.startswith(SITE_URL):
            return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{label}</a>'
        return f'<a href="{url}">{label}</a>'

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace_link, text)


def render_table(table_lines: list[str]) -> str:
    rows = []
    for raw in table_lines:
        cells = [c.strip() for c in raw.strip().strip("|").split("|")]
        rows.append(cells)
    if len(rows) < 2:
        return ""
    header = rows[0]
    body = [r for r in rows[1:] if not all(re.match(r"^:?-{2,}:?$", c) for c in r)]
    thead = "<thead><tr>" + "".join(f"<th>{format_inline(c)}</th>" for c in header) + "</tr></thead>"
    tbody_rows = []
    for r in body:
        tbody_rows.append("<tr>" + "".join(f"<td>{format_inline(c)}</td>" for c in r) + "</tr>")
    tbody = "<tbody>" + "".join(tbody_rows) + "</tbody>"
    return f'<div class="table-wrap"><table class="prose-table">{thead}{tbody}</table></div>'


def render_markdown(md: str) -> str:
    code_blocks: list[str] = []
    safe = html.escape(md, quote=False)

    def stash_code(match: re.Match[str]) -> str:
        code = match.group(2).strip()
        token = f"@@CODEBLOCK_{len(code_blocks)}@@"
        code_blocks.append(f'<pre class="prose-code"><code>{code}</code></pre>')
        return f"\n{token}\n"

    safe = re.sub(r"```(\w*)\n([\s\S]*?)```", stash_code, safe)

    lines = safe.split("\n")
    out: list[str] = []
    in_list = False
    list_type = "ul"
    table_buf: list[str] = []

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            out.append(f"</{list_type}>")
            in_list = False

    def flush_table() -> None:
        nonlocal table_buf
        if table_buf:
            rendered = render_table(table_buf)
            if rendered:
                out.append(rendered)
            table_buf = []

    for raw in lines:
        line = raw.strip()
        if not line:
            close_list()
            flush_table()
            continue

        if line.startswith("|") and line.endswith("|"):
            close_list()
            table_buf.append(line)
            continue
        else:
            flush_table()

        code_match = re.match(r"^@@CODEBLOCK_(\d+)@@$", line)
        if code_match:
            close_list()
            out.append(code_blocks[int(code_match.group(1))])
            continue

        if line.startswith("### "):
            close_list()
            inner = format_inline(line[4:])
            hid = slugify_heading(inner)
            out.append(f'<h3 id="{hid}">{inner}</h3>')
        elif line.startswith("## "):
            close_list()
            inner = format_inline(line[3:])
            hid = slugify_heading(inner)
            out.append(f'<h2 id="{hid}">{inner}</h2>')
        elif line.startswith("- "):
            if not in_list or list_type != "ul":
                close_list()
                out.append("<ul>")
                in_list = True
                list_type = "ul"
            out.append(f"<li>{format_inline(line[2:])}</li>")
        elif re.match(r"^\d+\.\s+", line):
            if not in_list or list_type != "ol":
                close_list()
                out.append("<ol>")
                in_list = True
                list_type = "ol"
            cleaned = re.sub(r"^\d+\.\s+", "", line)
            out.append(f"<li>{format_inline(cleaned)}</li>")
        elif line.startswith("&gt; "):
            close_list()
            out.append(f"<blockquote>{format_inline(line[5:])}</blockquote>")
        else:
            close_list()
            out.append(f"<p>{format_inline(line)}</p>")

    close_list()
    flush_table()
    return "\n".join(out)


def build_article_page(post: dict, body_html: str) -> str:
    slug = post["slug"]
    title = post["title"]
    summary = post.get("summary", "")
    date_pub = post["date"]
    date_mod = post.get("updated", date_pub)
    category = post.get("category", "Writing")
    read_time = post.get("readTime", "3 min read")
    canonical = f"{SITE_URL}/writing/{slug}/"
    raw_md_url = f"{SITE_URL}/posts/{slug}.md"

    esc_title = html.escape(title, quote=True)
    esc_summary = html.escape(summary, quote=True)
    esc_cat = html.escape(category, quote=True)
    esc_cat_upper = html.escape(category.upper(), quote=True)

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BlogPosting",
                "@id": f"{canonical}#article",
                "headline": title,
                "description": summary,
                "datePublished": date_pub,
                "dateModified": date_mod,
                "articleSection": category,
                "inLanguage": "en",
                "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
                "author": {
                    "@type": "Person",
                    "name": "April",
                    "alternateName": ["AiPRIL", "Hanh Le", "Le Hong Hanh"],
                    "url": f"{SITE_URL}/",
                    "email": "drink@iced-latte.com",
                    "sameAs": [
                        "https://www.upwork.com/freelancers/lehonghanh",
                        "https://www.linkedin.com/in/hanhlehong/",
                        "https://github.com/hanh-le-hong",
                    ],
                },
                "publisher": {
                    "@type": "Person",
                    "name": "April (AiPRIL)",
                    "url": f"{SITE_URL}/",
                },
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
                    {"@type": "ListItem", "position": 2, "name": "Writing", "item": f"{SITE_URL}/#writing"},
                    {"@type": "ListItem", "position": 3, "name": title, "item": canonical},
                ],
            },
        ],
    }
    schema_json = json.dumps(schema, ensure_ascii=False, indent=2)

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="winter">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc_title} | AiPRIL</title>
  <meta name="description" content="{esc_summary}" />
  <meta name="author" content="April (Hanh Le)" />
  <link rel="canonical" href="{canonical}" />
  <link rel="alternate" type="application/rss+xml" title="AiPRIL RSS Feed" href="{SITE_URL}/rss.xml" />
  <link rel="alternate" type="text/markdown" href="{raw_md_url}" />

  <meta property="og:type" content="article" />
  <meta property="og:title" content="{esc_title}" />
  <meta property="og:description" content="{esc_summary}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:site_name" content="AiPRIL" />
  <meta property="article:published_time" content="{date_pub}" />
  <meta property="article:modified_time" content="{date_mod}" />
  <meta property="article:author" content="April (Hanh Le)" />
  <meta property="article:section" content="{esc_cat}" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="{esc_title}" />
  <meta name="twitter:description" content="{esc_summary}" />

  <link rel="icon" type="image/svg+xml" href="../../favicon.svg" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../../styles.css" />

  <script type="application/ld+json">
{schema_json}
  </script>
</head>
<body data-article-slug="{html.escape(slug, quote=True)}" data-article-category="{esc_cat}">
  <div class="site-shell" id="top">
    <header class="header">
      <div class="header-inner">
        <div class="header-left">
          <a href="../../" class="brand" aria-label="AiPRIL Home">AiPRIL</a>
          <nav class="header-nav" aria-label="Main Navigation">
            <a href="../../#writing" class="nav-link">&lt;- All Writing</a>
            <a href="../../#about" class="nav-link">About</a>
            <a href="../../#craft" class="nav-link">Craft</a>
            <a href="../../#lab" class="nav-link">Lab</a>
            <a href="../../#human" class="nav-link">Human</a>
            <a href="../../#connect" class="nav-link">Connect</a>
          </nav>
        </div>

        <div class="header-right">
          <button id="theme-toggle" class="season-switch" type="button" aria-label="Switch between Winter and Spring mode">
            <span class="season-opt" data-season="winter">WINTER</span>
            <span class="season-sep">/</span>
            <span class="season-opt" data-season="spring">SPRING</span>
          </button>
          <div class="divider-v" aria-hidden="true"></div>
          <a
            href="https://github.com/hanh-le-hong"
            class="external-top-link"
            target="_blank"
            rel="noopener noreferrer"
          >
            GitHub
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
              <path d="M7 7h10v10" />
              <path d="M7 17 17 7" />
            </svg>
          </a>
        </div>
      </div>

      <nav class="mobile-nav" aria-label="Mobile Navigation">
        <a href="../../#writing" class="nav-link">&lt;- All Writing</a>
        <a href="../../#about" class="nav-link">About</a>
        <a href="../../#craft" class="nav-link">Craft</a>
        <a href="../../#lab" class="nav-link">Lab</a>
        <a href="../../#connect" class="nav-link">Connect</a>
      </nav>
    </header>

    <main class="article-main">
      <article class="article-container">
        <div class="article-meta-bar">
          <span class="tag">{esc_cat_upper}</span>
          <span class="meta-dot">·</span>
          <time datetime="{date_pub}" class="mono-date">{date_pub}</time>
          <span class="meta-dot">·</span>
          <span class="mono-date">{html.escape(read_time)}</span>
        </div>

        <h1 class="article-title">{esc_title}</h1>
        <p class="article-lead">{esc_summary}</p>

        <div id="post-body" class="article-prose">
{body_html}
        </div>

        <aside class="article-author-box" aria-label="About the Author">
          <p class="article-author-label">WRITTEN BY APRIL (HANH LE) // MARKETER &amp; BUILDER</p>
          <p class="article-author-bio">
            9-to-5 marketer and operator solving business problems through marketing, product, and analysis. Born in Spring (craft), chasing Winter (systems).
          </p>
          <div class="article-author-links">
            <a href="https://www.upwork.com/freelancers/lehonghanh" target="_blank" rel="noopener noreferrer" class="btn-primary btn-sm">Upwork Profile -&gt;</a>
            <a href="https://www.linkedin.com/in/hanhlehong/" target="_blank" rel="noopener noreferrer" class="btn-secondary btn-sm">LinkedIn</a>
            <a href="mailto:drink@iced-latte.com" class="btn-secondary btn-sm">drink@iced-latte.com</a>
          </div>
        </aside>

        <div class="article-footer-nav">
          <a href="../../#writing" class="btn-secondary">&lt;- Back to Writing</a>
          <a href="../../posts/{html.escape(slug, quote=True)}.md" class="article-raw-link">View Raw .md</a>
          <a href="../../studio.html?edit={html.escape(slug, quote=True)}" class="btn-secondary local-only" hidden>Edit in Studio</a>
        </div>
      </article>
    </main>

    <footer class="footer">
      <div class="footer-inner">
        <span class="footer-text">AiPRIL · ICED-LATTE.COM © 2026</span>
        <a href="../../" class="footer-text footer-top-link">HOME ↑</a>
      </div>
    </footer>
  </div>

  <script src="../../analytics-config.js"></script>
  <script src="../../analytics.js"></script>
  <script src="../../main.js"></script>
</body>
</html>
"""


def build_feed_rows(posts: list[dict]) -> str:
    rows = []
    for p in posts:
        slug = html.escape(p["slug"], quote=True)
        cat = html.escape(p.get("category", "Writing"))
        date = html.escape(p["date"])
        title = html.escape(p["title"])
        summary = html.escape(p.get("summary", ""))
        read_time = html.escape(p.get("readTime", "3 min read"))
        rows.append(
            f'            <a href="writing/{slug}/" class="post-row">\n'
            f'              <div class="post-row-meta">\n'
            f'                <span class="tag">{cat}</span>\n'
            f'                <span class="post-row-date">{date}</span>\n'
            f'              </div>\n'
            f'              <div class="post-row-main">\n'
            f'                <h3>{title}</h3>\n'
            f'                <p>{summary}</p>\n'
            f'              </div>\n'
            f'              <div class="post-row-right">\n'
            f'                <span>{read_time} -&gt;</span>\n'
            f'              </div>\n'
            f'            </a>'
        )
    return "\n".join(rows)


def build_sitemap(posts: list[dict]) -> str:
    latest_date = max((p.get("updated", p["date"]) for p in posts), default="2026-10-31")
    entries = [
        f"  <url>\n    <loc>{SITE_URL}/</loc>\n    <lastmod>{latest_date}</lastmod>\n  </url>"
    ]
    for p in posts:
        lastmod = p.get("updated", p["date"])
        loc = f"{SITE_URL}/writing/{p['slug']}/"
        entries.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod}</lastmod>\n  </url>")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )


def build_rss(posts: list[dict]) -> str:
    items = []
    for p in posts:
        link = f"{SITE_URL}/writing/{p['slug']}/"
        d = dt.date.fromisoformat(p["date"])
        pub_rfc = format_datetime(dt.datetime(d.year, d.month, d.day, tzinfo=dt.timezone.utc))
        items.append(
            "    <item>\n"
            f"      <title>{html.escape(p['title'])}</title>\n"
            f"      <link>{link}</link>\n"
            f"      <guid isPermaLink=\"true\">{link}</guid>\n"
            f"      <pubDate>{pub_rfc}</pubDate>\n"
            f"      <category>{html.escape(p.get('category', 'Writing'))}</category>\n"
            f"      <description>{html.escape(p.get('summary', ''))}</description>\n"
            "    </item>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        "  <channel>\n"
        "    <title>AiPRIL | April (Hanh Le)</title>\n"
        f"    <link>{SITE_URL}/</link>\n"
        "    <description>Notes on marketing craft, marketing systems, product growth, and building tiny projects with AI.</description>\n"
        "    <language>en</language>\n"
        f'    <atom:link href="{SITE_URL}/rss.xml" rel="self" type="application/rss+xml" />\n'
        + "\n".join(items)
        + "\n  </channel>\n</rss>\n"
    )


def build_llms_txt(posts: list[dict]) -> str:
    post_lines = []
    for p in posts:
        slug = p["slug"]
        title = p["title"]
        summary = p.get("summary", "")
        post_lines.append(
            f"- [{title}]({SITE_URL}/writing/{slug}/): {summary} (Markdown: {SITE_URL}/posts/{slug}.md)"
        )
    posts_section = "\n".join(post_lines) if post_lines else "- New essays coming soon."
    return f"""# AiPRIL (iced-latte.com)

> Personal website and working notebook of April (Hanh Le), a marketer and operator moving deeper into marketing systems, product growth, measurement, and AI workflows.

## Core Pages
- [Homepage & Profile]({SITE_URL}/): Overview of April's background, marketing craft, tiny AI builds, and contact details.
- [RSS Feed]({SITE_URL}/rss.xml): XML feed of published essays and working notes.
- [Sitemap]({SITE_URL}/sitemap.xml): Canonical URL index.

## Writing & Working Notes
{posts_section}

## Lab Projects
- [Marketing Systems Lab](https://github.com/hanh-le-hong/marketing-systems-lab): Public repository practising measurement, KPI trees, AI fluency, and marketing automation.
- [Snapcard](https://snapcard-dc0ca.web.app/): Lightweight web app for creating and sending digital postcards with a single link.

## Author & Contact
- Name: April (Hanh Le / Le Hong Hanh)
- Role: Marketer & Operator (M.S. in Marketing Management)
- Email: drink@iced-latte.com
- Upwork: https://www.upwork.com/freelancers/lehonghanh
- LinkedIn: https://www.linkedin.com/in/hanhlehong/
- GitHub: https://github.com/hanh-le-hong
"""


def main() -> None:
    posts_index_path = ROOT / "posts" / "index.json"
    posts: list[dict] = json.loads(posts_index_path.read_text(encoding="utf-8"))

    for post in posts:
        slug = post["slug"]
        md_path = ROOT / "posts" / f"{slug}.md"
        if not md_path.exists():
            continue
        md_text = md_path.read_text(encoding="utf-8")
        body_html = render_markdown(md_text)
        out_dir = ROOT / "writing" / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(build_article_page(post, body_html), encoding="utf-8")

    # Sync pre-rendered #posts-feed in index.html
    index_html_path = ROOT / "index.html"
    if index_html_path.exists():
        raw_index = index_html_path.read_text(encoding="utf-8")
        marker_pattern = re.compile(
            r"(<!-- POSTS_FEED_START -->)[\s\S]*?(<!-- POSTS_FEED_END -->)"
        )
        rows_html = build_feed_rows(posts)
        updated_index = marker_pattern.sub(
            rf"\1\n{rows_html}\n            \2", raw_index
        )
        index_html_path.write_text(updated_index, encoding="utf-8")

    (ROOT / "sitemap.xml").write_text(build_sitemap(posts), encoding="utf-8")
    (ROOT / "rss.xml").write_text(build_rss(posts), encoding="utf-8")
    (ROOT / "llms.txt").write_text(build_llms_txt(posts), encoding="utf-8")


if __name__ == "__main__":
    main()
