# Plan: Noodle-Style Redesign for AiPRIL (`hanh-le-hong.github.io`)

## Files
1. `favicon.svg` -- Biểu tượng tab trình duyệt vuông góc `#080808` với ký hiệu `Ai_` màu vàng `#facc15`.
2. `styles.css` -- Hệ thống design tokens Noodle cho cả 2 chế độ `Winter` (`#080808` + `#facc15`) và `Spring` (`#fafafa` + `#facc15` / `#926000`), nền `dot-grid` `20px`, khung thẻ `1px` hairline matrix, animation `fadeUp` và con trỏ nhấp nháy `_`.
3. `index.html` -- Header `52px`, Hero chuẩn Noodle + thanh terminal copy email, khung `00 // README.md` (5 đoạn giới thiệu + bảng thông số nhanh), `01 // The Craft`, `02 // The Lab`, `03 // Writing` (đã mở `hidden`), `04 // The Human`, `05 // Connect`.
4. `main.js` -- Chuyển đổi `Winter / Spring`, copy email 1 chạm, tải danh sách bài viết từ `posts/index.json` có lọc chuyên mục, và chỉ hiện nút `Studio` khi chạy trên `localhost`.
5. `post.html` -- Giao diện đọc bài viết đồng bộ style Noodle docs (dot-grid, `h2` in hoa kẻ chân `1px`, code block vuông góc, ẩn nút `Edit in Studio` trên public domain).
6. `studio.html` -- Đồng bộ font `JetBrains Mono` và hệ màu Noodle mới cho trình soạn thảo local.
7. `posts/90-9-1-from-consuming-to-building.md` -- Thay dấu em-dash duy nhất còn sót bằng dấu phẩy để tuân thủ quy tắc zero-em-dash.

## Risks & Mitigations
- **Độ tương phản màu vàng trên nền sáng (`Spring`):** Màu `#facc15` rất sáng trên nền đen nhưng nếu làm màu chữ trên nền trắng sẽ khó đọc. Khắc phục: giữ `#facc15` kết hợp chữ đen `#0a0a0a` cho nút chính/vùng bôi đen (tương phản > 13:1), còn chữ nhấn/link/icon trên nền sáng dùng màu hổ phách đậm `#926000` (tương phản > 5.4:1, đạt chuẩn WCAG AA).
- **Lộ nút `Studio` cho khách từ Upwork:** Gắn thuộc tính `hidden` mặc định cho mọi link tới `studio.html` và chỉ mở bằng JS khi `hostname` là `localhost` hoặc `127.0.0.1`.

## Proof
- Toàn bộ file được đẩy atomic lên `main` của `hanh-le-hong/hanh-le-hong.github.io`.
- Kiểm tra không còn ký tự em-dash trong nội dung hiển thị và không có secret trong commit.
- Kiểm tra trạng thái deploy GitHub Pages hoàn tất trên `https://hanh-le-hong.github.io/`.
