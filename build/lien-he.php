<?php
// Nhận thông tin khách để lại (khung chat, form trả góp), ghi vào file ngoài thư mục web,
// rồi chuyển tiếp cho chatbot2 để chia cho sale (anh chốt 21/10 9:35).
// Gửi kiểu cửa /api/lead.php của app social: ký HMAC-SHA256 (X-Thoi-Gian, X-Nonce, X-Chu-Ky) bằng SOCIAL_KHOA_WEB
// trong /home/smilemot/social-noi-web.php (ngoài thư mục web). Chưa đọc được khoá thì chỉ ghi lại, khách vẫn được báo đã nhận.
header('Content-Type: application/json; charset=utf-8');
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); echo '{"ok":false}'; exit; }
$d = json_decode(file_get_contents('php://input'), true) ?: [];
$sdt = preg_replace('/\D/', '', $d['sdt'] ?? '');
if (!preg_match('/^0[35789]\d{8}$/', $sdt)) { http_response_code(400); echo '{"ok":false}'; exit; }
$chu = function ($k, $n) use ($d) {
    $v = trim(preg_replace('/[\x00-\x1F\x7F]+/u', ' ', (string)($d[$k] ?? '')));
    return mb_substr($v, 0, $n, 'UTF-8');
};
$web = preg_replace('/[^a-z0-9.\-]/i', '', $d['web'] ?? '');
$trang = substr(preg_replace('/[^\w\/\-.?=&%]/u', '', $d['trang'] ?? ''), 0, 200);
$loai = preg_replace('/[^a-z\-]/', '', $d['loai'] ?? 'chat') ?: 'chat';
$k = [
    'luc' => date('c'), 'nguon' => $web, 'loai' => $loai, 'trang' => $trang, 'sdt' => $sdt,
    'ten' => $chu('ten', 60), 'xe' => $chu('xe', 120), 'gia' => $chu('gia', 30),
    'tra_truoc' => $chu('tra_truoc', 4), 'ky_han' => $chu('ky_han', 4), 'ghi_chu' => $chu('ghi_chu', 300),
];
$dir = '/home/smilemot/phoxedien-khach';
if (!is_dir($dir)) { @mkdir($dir, 0750, true); }
$f = fopen("$dir/khach-de-lai-so.csv", 'a');
if (!$f) { http_response_code(500); echo '{"ok":false}'; exit; }
flock($f, LOCK_EX);
fputcsv($f, [date('Y-m-d H:i:s'), $sdt, $web, $trang, $_SERVER['REMOTE_ADDR'] ?? '', $loai, $k['ten'], $k['xe'], $k['gia'], $k['tra_truoc'], $k['ky_han'], $k['ghi_chu']]);
flock($f, LOCK_UN); fclose($f);

// Trả lời khách trước, rồi mới chuyển cho chatbot2 (app social.xediensmile.com) để khách không phải chờ
echo '{"ok":true}';
if (function_exists('fastcgi_finish_request')) { fastcgi_finish_request(); }
$khoa = '/home/smilemot/social-noi-web.php';  // định nghĩa SOCIAL_KHOA_WEB, ngoài thư mục web, không đưa lên git
if (is_readable($khoa)) { require_once $khoa; }
if (defined('SOCIAL_KHOA_WEB') && SOCIAL_KHOA_WEB !== '' && function_exists('curl_init')) {
    $ten_web = ['phoxedien.vn' => 'Phố Xe Điện (phoxedien.vn)', 'phoxedien.com.vn' => 'Phố Xe Điện (phoxedien.com.vn)'][$web] ?? ($web ?: 'web');
    $ghi = ['Khách để lại số trên ' . $ten_web . ($loai === 'tra-gop' ? ', form trả góp' : ($loai === 'tu-van' ? ', form nhờ gọi tư vấn' : ', khung chat'))];
    if ($k['xe'] !== '') { $ghi[] = 'Xe: ' . $k['xe'] . ($k['gia'] !== '' ? ' · ' . $k['gia'] : ''); }
    if ($k['tra_truoc'] !== '' || $k['ky_han'] !== '') { $ghi[] = 'Trả trước ' . $k['tra_truoc'] . '% · góp ' . $k['ky_han'] . ' tháng'; }
    if ($k['ghi_chu'] !== '') { $ghi[] = 'Khách ghi: ' . $k['ghi_chu']; }
    if ($trang !== '') { $ghi[] = 'Trang: https://' . $web . $trang; }
    // "nguon": app chưa có nguồn riêng cho phoxedien nên gửi chatbot_web, ghi rõ web trong ghi_chu
    $gui = ['sdt' => $sdt, 'ten' => $k['ten'], 'thuong_hieu' => 'smile', 'nguon' => 'chatbot_web', 'nhu_cau' => $k['xe'], 'ghi_chu' => implode("\n", $ghi)];
    $body = json_encode($gui, JSON_UNESCAPED_UNICODE);
    $tg = (string) time();
    $nonce = bin2hex(random_bytes(12));
    $ky = hash_hmac('sha256', $tg . '.' . $nonce . '.' . $body, SOCIAL_KHOA_WEB);
    $ch = curl_init('https://social.xediensmile.com/api/lead.php');
    curl_setopt_array($ch, [CURLOPT_POST => true, CURLOPT_POSTFIELDS => $body, CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 5, CURLOPT_CONNECTTIMEOUT => 3,
        CURLOPT_HTTPHEADER => ['Content-Type: application/json', 'X-Thoi-Gian: ' . $tg, 'X-Nonce: ' . $nonce, 'X-Chu-Ky: ' . $ky]]);
    $kq = curl_exec($ch);
    $ma = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    if ($ma !== 200) {  // ghi lại để gửi bù, không làm hỏng form
        @file_put_contents("$dir/chatbot2-gui-bu.jsonl", json_encode($gui + ['luc' => $k['luc'], 'ma_loi' => $ma, 'tra_ve' => mb_substr((string)$kq, 0, 200, 'UTF-8')], JSON_UNESCAPED_UNICODE) . "\n", FILE_APPEND | LOCK_EX);
    }
}

