<?php
// Nhận thông tin khách để lại (khung chat, form trả góp), ghi vào file ngoài thư mục web,
// rồi chuyển tiếp cho chatbot2 để chia cho sale (anh chốt 21/10 9:35).
// Địa chỉ nhận của chatbot2 đặt ở /home/smilemot/phoxedien-khach/chatbot2.json: {"url": "https://...", "token": "..."}
// (ngoài thư mục web, không đưa lên git). Chưa có tệp đó thì chỉ ghi lại, khách vẫn được báo đã nhận.
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

// chuyển tiếp chatbot2; lỗi thì ghi lại để gửi bù, không làm khách phải chờ
$cfg = @json_decode(@file_get_contents("$dir/chatbot2.json"), true);
if (!empty($cfg['url']) && strpos($cfg['url'], 'https://') === 0 && function_exists('curl_init')) {
    $ch = curl_init($cfg['url']);
    $h = ['Content-Type: application/json'];
    if (!empty($cfg['token'])) { $h[] = 'Authorization: Bearer ' . $cfg['token']; }
    curl_setopt_array($ch, [CURLOPT_POST => true, CURLOPT_POSTFIELDS => json_encode($k, JSON_UNESCAPED_UNICODE),
        CURLOPT_HTTPHEADER => $h, CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 4, CURLOPT_CONNECTTIMEOUT => 3]);
    curl_exec($ch);
    $ma = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    if ($ma < 200 || $ma >= 300) {
        @file_put_contents("$dir/chatbot2-gui-bu.jsonl", json_encode($k + ['ma_loi' => $ma], JSON_UNESCAPED_UNICODE) . "\n", FILE_APPEND | LOCK_EX);
    }
}
echo '{"ok":true}';
