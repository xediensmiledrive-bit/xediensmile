# Gửi khách về app social (chatbot2) — mô tả cửa nhận

Rút từ mã đang có trên máy nhà ngày 21/10/2026. Bản này không chứa khoá hay bí mật nào.

## Cửa nhận
- `POST https://social.xediensmile.com/api/lead.php`. Phương thức khác trả 405.
- Body là JSON thô (UTF-8), `Content-Type: application/json`, tối đa 20.000 byte.

## Chữ ký (HMAC-SHA256, chữ ký dạng hex chữ thường)
- `X-Thoi-Gian`: unix giây (chuỗi). Lệch quá 300 giây so với máy chủ thì trả 401.
- `X-Nonce`: 12–64 ký tự `[A-Za-z0-9_-]`, mỗi lần gửi một mã mới. Dùng lại trong 10 phút thì trả 409.
- `X-Chu-Ky` = `hash_hmac('sha256', X-Thoi-Gian . "." . X-Nonce . "." . body, SOCIAL_KHOA_WEB)`.
  - `body` phải đúng từng byte đã gửi đi.
- Khoá web là hằng `SOCIAL_KHOA_WEB`, đặt trong tệp ngoài thư mục web: `/home/smilemot/social-noi-web.php` (`<?php define('SOCIAL_KHOA_WEB', '...');`).
  - Không ghi khoá vào mã hay repo.
  - Cùng VPS nên có thể `require_once` đúng tệp đó.
- Thiếu khoá phía app thì trả 503 `chua_co_khoa`. Sai chữ ký thì trả 401 `chu_ky`.

## Trường JSON
| trường | bắt buộc | ghi chú |
|---|---|---|
| `sdt` | có | 10 số di động VN. Sai thì trả 422. |
| `ten` | không | |
| `thuong_hieu` | không | `smile` (mặc định) hoặc `kh` (Khoa Smile) |
| `nguon` | không | giá trị lạ tự thành `chatbot_web` |
| `chi_nhanh` | không | `cn1` Hậu Giang · `cn2` 188 LLQ · `cn3` 190 LLQ · `cn4` Trần Văn Kiểu/Bình Phú · `cn5` Đồng Tháp · `cn6` Phan Thiết |
| `nhu_cau` | không | tên xe / sản phẩm |
| `ghi_chu` | không | nên ghi rõ nguồn web + số liệu trả góp (giá, trả trước, kỳ hạn) |

Khoá web không nhận `giao_sale`, `so_zalo`, `so_ten` (chỉ khoá bot Zalo mới dùng được 3 trường này).

## Giá trị `nguon` app đang chấp nhận (inc/core.php, hằng NGUON)
`goi_toi`, `chatbot_web`, `bot_zalo`, `offline`, `cua_hang`, `fanpage`, `gioi_thieu`, `khac`.
- Chưa có nguồn riêng cho phoxedien. Muốn sale thấy "Phố Xe Điện" thì phải thêm khoá vào NGUON ở app social.
- Trước khi thêm, gửi `chatbot_web` và ghi rõ trong `ghi_chu`.

## Trả về
- 200 `{"id", "ket_qua", "thong_diep"}`. Số trùng (cùng thương hiệu) cũng trả 200: app gộp vào khách cũ và báo sale đang giữ (`ket_qua` khác tạo mới).
- 422 khi `lead_tao` báo lỗi (thường do SĐT sai). 400 `json` khi body không phải JSON.

## Mẫu PHP (giống bộ gửi của xediensmile.com, mu-plugin social-noi-lead.php)
```php
$body  = json_encode($d, JSON_UNESCAPED_UNICODE);
$tg    = (string) time();
$nonce = bin2hex(random_bytes(12));
$ky    = hash_hmac('sha256', $tg . '.' . $nonce . '.' . $body, SOCIAL_KHOA_WEB);
$ch = curl_init('https://social.xediensmile.com/api/lead.php');
curl_setopt_array($ch, [CURLOPT_POST => true, CURLOPT_POSTFIELDS => $body, CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 5,
  CURLOPT_HTTPHEADER => ['Content-Type: application/json', 'X-Thoi-Gian: ' . $tg, 'X-Nonce: ' . $nonce, 'X-Chu-Ky: ' . $ky]]);
$kq = curl_exec($ch); $ma = curl_getinfo($ch, CURLINFO_HTTP_CODE);
```
- Nên gửi sau khi đã trả trang cho khách (`fastcgi_finish_request()`).
- Lỗi thì ghi lại để gửi bù, không làm hỏng form.
