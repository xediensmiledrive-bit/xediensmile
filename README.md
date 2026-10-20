# Gói web Phố Xe Điện (nhánh tạm, xoá sau khi triển khai)

- `build/`: mã dựng (Python 3, không cần thư viện ngoài).
- `dist/`: bản đã dựng sẵn, giá đang ghi "Liên hệ".

Gắn giá thật: chép `gia-smile-2026-10-20.json` vào `build/gia-smile.json` (dạng `{"models":[...],"stores":[...]}`), rồi chạy
`python build/build.py dist` (dựng lại cả 2 web vào `dist/`).

Đưa lên VPS: nội dung `dist/phoxedien.vn/` → `/home/smilemot/phoxedien.vn/`, `dist/phoxedien.com.vn/` → `/home/smilemot/phoxedien.com.vn/` (chủ smilemot:smilemot).
