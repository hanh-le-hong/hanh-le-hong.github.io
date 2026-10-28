---
status: verified
---

# Intent & Plan: AiPRIL Lightweight CMS & Writing System (v1)

## Problem
Bạn muốn bắt đầu viết từng bài (cho các mảng `The Craft`, `The Lab`, `The Human`) trực tiếp trên website cá nhân mà không phải đụng vào code HTML phức tạp mỗi lần viết bài mới, đồng thời vẫn giữ kiến trúc nhẹ, miễn phí, an toàn (không cần thuê database hay lo lộ mật khẩu admin).

## Solution (Git-backed Markdown CMS + Visual Studio)
Xây dựng hệ thống **Hybrid Markdown CMS** gồm 3 mảnh ghép hoạt động trơn tru:
1. **Kho bài viết (`posts/*.md` + `posts/index.json`):**
   - Mỗi bài viết là một file Markdown thuần túy (`.md`) nằm trong thư mục `posts/`, dễ đọc, dễ sao lưu trên GitHub.
2. **Giao diện đọc bài viết (`post.html?slug=<ten-bai>`):**
   - Trang đọc bài viết tối giản kiểu Chip Huyen, đồng bộ chế độ `Winter / Spring`, tự động tính thời gian đọc.
3. **Giao diện soạn thảo trực quan (`studio.html` + `cms-server.py`):**
   - Mở `http://localhost:4174/studio.html` trên máy của bạn để gõ bài viết mới, xem bản nháp trực tiếp (Live Preview), chọn chuyên mục (`The Craft`, `The Lab`, `The Human`) và bấm **Publish** — hệ thống tự động lưu file `.md` và cập nhật lên trang chủ ngay lập tức.
