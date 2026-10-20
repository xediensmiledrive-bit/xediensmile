# Gói web Phố Xe Điện (nhánh tạm, xoá sau khi triển khai)

- `build/`: mã dựng (Python 3, không cần thư viện ngoài).
- `dist/`: bản đã dựng sẵn, giá đang ghi "Liên hệ".

Gắn giá thật: chép `gia-smile-2026-10-20.json` vào `build/gia-smile.json` (dạng `{"models":[...],"stores":[...]}`), rồi chạy
`python build/build.py dist` (dựng lại cả 2 web vào `dist/`).

Đưa lên VPS: nội dung `dist/phoxedien.vn/` → `/home/smilemot/phoxedien.vn/`, `dist/phoxedien.com.vn/` → `/home/smilemot/phoxedien.com.vn/` (chủ smilemot:smilemot).

Bài Muse đã đạt soát: đặt biến `PXD_KHO` trỏ tới thư mục SEO-web (vd `set PXD_KHO=Y:\CLAUDE\SEO-web`) rồi chạy build như trên. Build đọc `phoxedien-vn\_kho\dat\*\` và `phoxedien-com-vn\_kho\dat\*\` (bai.html + meta.json + <slug>.webp nếu có), tự đặt URL theo chuyên mục (meta.json có `url` hoặc `chuyen_muc` thì theo đó), gắn og:image + ảnh đầu bài khi có ảnh, thêm vào trang chủ, chuyên mục, trang tác giả và sitemap. Không có PXD_KHO thì bỏ qua bài Muse.

Ảnh xe thật: đặt `PXD_ANH` trỏ tới thư mục ảnh hãng (có `nguon.csv`: hang, mau_trong_gia_smile, tep, ...). Build ghép `mau_trong_gia_smile` với `name` trong gia-smile.json, chép tối đa 3 ảnh/mẫu vào `/anh-xe/<hang>/` (đổi WebP 900px nếu có Pillow), gắn ảnh nhỏ vào bảng giá, lưới "Ảnh xe thật" ở trang chủ, bảng giá, trang loại xe, trang hãng, và "Mẫu xe nhắc trong bài" cuối bài có nhắc tên mẫu/hãng.
