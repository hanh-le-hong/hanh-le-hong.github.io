---
intent: intent/2026-10-29-personal-website-v1.md
status: verified
---

# Plan: Personal Website v1 — April Hanh (Human × Robotic)

## Architecture & Design Decisions
1. **Zero-Overhead Stack (Lean & Fast):**
   - Sử dụng **HTML5 + Modern CSS (Custom Properties & CSS Grid) + Vanilla JavaScript** chuẩn chỉnh, tích hợp sẵn **SEO Meta Tags + Schema.org (`Person` JSON-LD)** cho tên **`April Hanh`** (`Hanh Le Hong`).
2. **Visual & Typography System ("Simple, Logical, Bold, Art-Focused"):**
   - **Wordmark `APRIL HANH`:** Tối giản, sắc nét, kết hợp font Serif cổ điển (`Instrument Serif`) và Monospace kỹ thuật (`JetBrains Mono`) để thể hiện trực diện tinh thần **Renaissance × Robotic**.
   - **Dual Mode (`[RENAISSANCE]` ↔ `[ROBOTIC]`):**
     - `Renaissance Mode` (Default Light): Nền giấy mỹ thuật ấm (`#F5F2EB`), chữ mực đen (`#141413`), điểm nhấn đỏ son/vàng đồng cổ điển (`#8C3A2B`), đường lưới mảnh (`1px solid rgba(20,20,19,0.12)`).
     - `Robotic Mode` (Dark): Nền đá đen (`#0B0C0E`), chữ trắng ngà (`#EAE6DF`), điểm nhấn xanh terminal/bạc (`#64D2FF` / `#C8B89A`), đường lưới kỹ thuật (`1px solid rgba(234,230,223,0.12)`).
   - **Điểm nhấn Art (Hero Centerpiece):** Một tác phẩm nghệ thuật cổ điển kết hợp hình học kỹ thuật đặt trong khung tỷ lệ vàng ở Hero, không rải hình ảnh lộn xộn khắp trang.

## Files (Theo thứ tự thực hiện)
1. `.gitignore` — Chặn `.env`, `.DS_Store`, thư mục tạm theo chuẩn `/bto-secrets`.
2. `index.html` — Cấu trúc ngữ nghĩa (Semantic HTML + Schema `Person` JSON-LD cho `April Hanh`) chia đúng 4 Chương:
   - **Header & Mode Switcher:** Logo `APRIL HANH`, điều hướng 4 chương (`I. Craft`, `II. Lab 04`, `III. Human`, `IV. Connect`), nút gạt `RENAISSANCE / ROBOTIC`.
   - **Hero Section:** Dòng định vị Bold Serif lớn + Khung tác phẩm Art cổ điển làm tâm điểm + 2 nút điều hướng rõ ràng.
   - **Chapter I — `01 / THE CRAFT`:** Lưới 4 trụ cột chuyên môn (`Marketing Management`, `Product & Growth`, `Technology & AI`, `Business Strategy`) + 3 thẻ Selected Impact.
   - **Chapter II — `02 / LAB 04`:** Khu vực dự án thực nghiệm & nghiên cứu (lấy cảm hứng từ tháng 4 & phòng thí nghiệm của Haibara Ai).
   - **Chapter III — `03 / THE HUMAN`:** Bố cục tạp chí tối giản cho 4 mảng ngoài công việc (`Soundwaves / Music`, `Motion / Sports`, `Coordinates / Travel`, `Field Notes / Curiosity`).
   - **Chapter IV — `04 / CONNECT`:** 3 cánh cửa hợp tác (`Hiring & Leadership`, `Advisory & Growth`, `Builders & Community`).
3. `styles.css` — Hệ thống biến màu 2 chế độ, lưới Blueprint `1px`, typography lớn táo bạo, responsive cho cả Desktop và Mobile.
4. `main.js` — Logic chuyển đổi mượt mà giữa `Renaissance Mode` và `Robotic Mode` (lưu trạng thái vào `localStorage`), bộ lọc nhanh ở phần Craft/Human, và tương tác cuộn mượt tới từng chương.
5. `assets/renaissance-hero.svg` (hoặc tranh cổ điển public domain chất lượng cao kết hợp đường nét hình học) — Tác phẩm Art điểm nhấn trung tâm.

## Risks & Mitigations
- **Rủi ro 1 (Giao diện bị rối / Overwhelmed):** Nhiều trang học theo Shopify Editions nhồi quá nhiều chữ nhỏ và hiệu ứng.
  - *Cách chặn:* Giới hạn tối đa 3 cấp độ chữ trên mỗi màn hình; giữ ít nhất 35% diện tích là khoảng trắng (whitespace); không dùng animation tự chạy gây mỏi mắt.
- **Rủi ro 2 (Chuyển đổi 2 chế độ bị chói hoặc mất tương phản):**
  - *Cách chặn:* Toàn bộ màu sắc đi qua biến CSS (`--bg`, `--fg`, `--muted`, `--line`, `--accent`), kiểm tra độ tương phản chữ ở cả 2 chế độ.

## Proof (Bằng chứng hoàn thành ở Phase 4)
1. Quét bảo mật theo `/bto-secrets` trước khi commit (không có key/secret nào).
2. Khởi chạy local server, kiểm tra trang trả về `HTTP 200`, không có lỗi Console hay link gãy.
3. Kiểm tra nút chuyển đổi `[RENAISSANCE]` ↔ `[ROBOTIC]` đổi toàn bộ bảng màu và trạng thái ngay lập tức.
4. Kiểm tra hiển thị thực tế trên cả màn hình lớn (Desktop) và điện thoại (Mobile).
