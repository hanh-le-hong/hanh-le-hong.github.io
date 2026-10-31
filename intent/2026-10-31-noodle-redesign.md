---
status: shipped
---
# Redesign AiPRIL Personal Website in Noodle Terminal-Editorial Style

**Problem** -- Giao diện cũ dùng tranh chân dung Phục Hưng và nhiều font pha trộn chưa tạo cảm giác gọn, sắc nét và đậm chất builder/systems như thiết kế của `https://poteto.github.io/noodle/`.

**Outcome** -- Toàn bộ website `https://hanh-le-hong.github.io/` (gồm trang chủ `index.html`, trang đọc bài `post.html`, và `studio.html`) được redesign đồng bộ theo ngôn ngữ thị giác của Noodle:
1. Typography 100% `JetBrains Mono`, góc vuông sắc nét, khung lưới `1px` matrix, nền lưới chấm `20px` (dot-grid).
2. Giữ bộ chuyển chế độ `Winter / Spring` theo phong cách Noodle (`Winter` mặc định: nền đen `#080808` + vàng `#facc15`; `Spring`: giấy sáng `#fafafa` + lưới chấm kỹ thuật + điểm nhấn vàng/hổ phách độ tương phản cao), loại bỏ hoàn toàn tranh Phục Hưng.
3. Hero thoáng chuẩn Noodle (`AiPRIL` + `Born in Spring. / Chasing Winter_` có con trỏ `_` nhấp nháy + 1 dòng tóm tắt + CTA + thanh copy email nhanh), đưa 5 đoạn giới thiệu chân thực xuống khung `00 // README.md` ngay bên dưới.
4. Bật mục `Writing` lên trang chủ cùng bộ lọc chuyên mục và 2 bài viết đầu tiên (đã rà sạch dấu em-dash), tự động ẩn các nút quản trị `Studio` đối với khách truy cập public.

**Constraints** -- Zero external JS framework/build step (thuần HTML/CSS/JS tĩnh chạy trực tiếp trên GitHub Pages), 100% không có dấu em-dash trong nội dung hiển thị, không lưu bất kỳ secret hay đường dẫn máy cá nhân nào.

**Out of scope** -- Không thay đổi cấu trúc lưu trữ bài viết Markdown (`posts/*.md` + `posts/index.json`).

**Open questions** -- (Đã chốt toàn bộ 4 quyết định thiết kế với April).
