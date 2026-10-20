<?php
// Nhận số điện thoại khách để lại trong khung chat, ghi vào file ngoài thư mục web.
header('Content-Type: application/json; charset=utf-8');
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); echo '{"ok":false}'; exit; }
$d = json_decode(file_get_contents('php://input'), true) ?: [];
$sdt = preg_replace('/\D/', '', $d['sdt'] ?? '');
if (!preg_match('/^0[35789]\d{8}$/', $sdt)) { http_response_code(400); echo '{"ok":false}'; exit; }
$web = preg_replace('/[^a-z0-9.\-]/i', '', $d['web'] ?? '');
$trang = substr(preg_replace('/[^\w\/\-.?=&]/u', '', $d['trang'] ?? ''), 0, 200);
$dir = '/home/smilemot/phoxedien-khach';
if (!is_dir($dir)) { @mkdir($dir, 0750, true); }
$f = fopen("$dir/khach-de-lai-so.csv", 'a');
if (!$f) { http_response_code(500); echo '{"ok":false}'; exit; }
flock($f, LOCK_EX);
fputcsv($f, [date('Y-m-d H:i:s'), $sdt, $web, $trang, $_SERVER['REMOTE_ADDR'] ?? '']);
flock($f, LOCK_UN); fclose($f);
echo '{"ok":true}';
