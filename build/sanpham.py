# -*- coding: utf-8 -*-
"""Trang riêng cho từng mẫu xe /xe/<slug>/ (anh chốt 20/10 19:00): mỗi sản phẩm một trang SEO theo tên xe.
.vn nhắm giá và thông số, .com.vn nhắm góc học sinh, phụ huynh (2 web 2 góc, mỗi web số điện thoại riêng).
Chỉ dùng dữ liệu có trong gia-smile.json, không tự bịa thông số. Bài Muse có meta "san_pham" = đúng tên mẫu
sẽ được ghép vào trang (MUSE[domain][tên chữ thường])."""
import html

import anhxe
import trangchu
import chot
import mxh
import noidung
from noidung import NHOM, THANG, NGAY_VN, vnd, models_of, keu, faq_html_local, faq_ld_local

LOAI_SP = ["may", "ga", "so"]
MUSE = {"phoxedien.vn": {}, "phoxedien.com.vn": {}}
GOC_LOAI = {"phoxedien.vn": {"may": "/xe-may-dien/", "ga": "/xe-ga-50cc/", "so": "/xe-so-50cc/"},
            "phoxedien.com.vn": {"may": "/xe-may-dien-cho-hoc-sinh/", "ga": "/xe-ga-50cc-cho-hoc-sinh/", "so": "/xe-so-50cc-cho-hoc-sinh/"}}
THONG_SO = [("brand", "Hãng"), ("type", "Loại xe"), ("range", "Quãng đường mỗi lần sạc"), ("speed", "Tốc độ tối đa"),
            ("motor", "Động cơ"), ("battery", "Pin, ắc quy"), ("weight", "Trọng lượng"), ("colors", "Màu")]
# Thông số chính hãng máy nhà lấy từ web hãng (anh cho phép 20/10 23:35): PXD_KHO/thong-so-hang.json
# {"<tên mẫu chữ thường>": {"nguon": "https://web-hang/...", "thong_so": {"Động cơ": "1200W", ...}}}
import json as _json, os as _os
_f = _os.path.join(_os.environ.get("PXD_KHO", "").strip(), "thong-so-hang.json") if _os.environ.get("PXD_KHO", "").strip() else ""
try:
    TS_HANG = {k.strip().lower(): v for k, v in _json.load(open(_f, encoding="utf-8-sig")).items()} if _f and _os.path.isfile(_f) else {}
except ValueError:
    TS_HANG = {}
LUAT = ('Theo Luật Trật tự, an toàn giao thông đường bộ 2024 (hiệu lực 01/01/2025), xe gắn máy gồm xe dưới 50cc và xe điện '
        'công suất đến 4 kW, tốc độ thiết kế đến 50 km/h; người đủ 16 tuổi được đi và không cần giấy phép lái xe.')


def ds_xe():
    ra, thay = [], set()
    for k in LOAI_SP:
        for m in models_of(k):
            t = (m.get("name") or "").strip()
            if t and t.lower() not in thay:
                thay.add(t.lower())
                ra.append((k, m))
    return ra


def _gia(m):
    if m.get("price"):
        return vnd(m["price"]), "Giá tại Smile, cập nhật %s, chưa gồm lệ phí trước bạ, biển số và bảo hiểm." % NGAY_VN, True
    tt = noidung.GIA_TT.get(m["name"].strip().lower())
    if tt:
        return vnd(tt), "Giá thị trường tháng %s, có thể khác tuỳ nơi bán." % THANG, True
    return "Liên hệ", "Giá đang cập nhật. Gọi hoặc nhắn để có giá hôm nay.", False


def _lien_quan(k, m, n=4):
    cung = [x for kk, x in ds_xe() if x is not m and kk == k]
    p = m.get("price") or 0
    cung.sort(key=lambda x: (x.get("brand") != m.get("brand"), abs((x.get("price") or 10**9) - p)))
    return cung[:n]


def trang(site, k, m):
    d = site["domain"]
    ten, hang = m["name"], (m.get("brand") or "").strip()
    url = anhxe.url_xe(ten)
    loai = NHOM[k][0]
    gia, chu_gia, co_gia = _gia(m)
    vn = d == "phoxedien.vn"
    if vn:
        h1, phu = ten, "Giá tháng %s và thông số" % THANG
        title = "%s giá bao nhiêu? Giá tháng %s" % (ten, THANG)
        desc = ("%s giá %s (cập nhật %s). " % (ten, gia, NGAY_VN) if co_gia else "%s: hỏi giá hôm nay qua Chat hoặc hotline. " % ten) + "Xem ảnh thật, thông số, mẫu cùng tầm giá và đặt xe tại Smile."
    else:
        # .com.vn bỏ chữ "cho học sinh" ở tiêu đề; chưa có giá thì không ghi "giá Liên hệ" (anh chốt 21/10)
        h1, phu = ten, "Có hợp cho con đi học không? Giá và lưu ý"
        title = ("%s: giá %s, có cần bằng lái?" % (ten, gia)) if co_gia else "%s: tuổi nào đi được, có cần bằng lái?" % ten
        desc = "%s là %s của %s, giá %s. Học sinh bao nhiêu tuổi đi được, cần giấy tờ gì, nuôi xe tốn bao nhiêu." % (ten, loai.lower(), hang or "hãng", gia)
    ts = [(nhan, m.get(key)) for key, nhan in THONG_SO if m.get(key)]
    th = TS_HANG.get(ten.strip().lower()) or {}
    co = {n for n, _ in ts}
    ts += [(n, v) for n, v in (th.get("thong_so") or {}).items() if v and n not in co]
    bang_ts = "".join('<tr><th>%s</th><td>%s</td></tr>' % (html.escape(n), html.escape(str(v))) for n, v in ts)
    nguon = th.get("nguon") if str(th.get("nguon", "")).startswith("https://") else ""
    if nguon and bang_ts:
        bang_ts += '<tr><td colspan="2" class="ts-nguon">Thông số theo <a href="%s" target="_blank" rel="noopener nofollow">website chính hãng %s</a></td></tr>' % (html.escape(nguon, quote=True), html.escape(hang))
    dien = k == "may"
    if vn:
        gioi = ['%s là mẫu %s của %s.' % (ten, loai.lower(), hang or "hãng")]
        gioi.append('Giá trên trang là giá xe, chưa gồm lệ phí trước bạ, đăng ký biển số và bảo hiểm bắt buộc. Cách tính giá lăn bánh xem ở bài <a href="/bang-gia/gia-lan-banh-xe-may-dien-xe-50cc/">giá lăn bánh</a>.')
        gioi.append(('Khi so với các mẫu cùng tầm giá, nhìn quãng đường mỗi lần sạc, tốc độ tối đa và loại pin: pin lithium nhẹ, bền hơn nhưng đắt hơn ắc quy chì (<a href="/so-sanh/pin-lithium-hay-ac-quy-chi/">so sánh hai loại pin</a>).')
                    if dien else ('Khi so với các mẫu cùng tầm giá, xem phanh trước (đĩa hay cơ), vành đúc hay nan và chiều cao yên so với người đi. Phân vân giữa xe ga và xe số thì đọc <a href="/so-sanh/xe-ga-50cc-hay-xe-so-50cc/">so sánh xe ga và xe số 50cc</a>.'))
    else:
        gioi = ['%s là %s của %s. Dưới đây là những điều nên biết trước khi mua xe này cho con.' % (ten, loai.lower(), hang or "hãng")]
        gioi.append(LUAT + ' Khi chọn mẫu điện, xem thông số công suất và tốc độ để chắc xe thuộc nhóm xe gắn máy.' if dien else LUAT)
        gioi.append('Đi đường cần mang đăng ký xe, bảo hiểm bắt buộc và căn cước. Xem thêm <a href="/giay-to/16-tuoi-di-xe-50cc-can-giay-to-gi/">giấy tờ khi 16 tuổi đi xe 50cc</a>.')
        gioi.append('Trước khi mua, cho con ngồi thử xem chống chân chạm đất được không và tay với tới phanh thoải mái.')
    faqs = [("%s giá bao nhiêu?" % ten, "%s: %s. %s" % (ten, gia, chu_gia)),
            ("Đi %s có cần bằng lái không?" % ten, LUAT),
            ("Mua %s ở đâu?" % ten, "Smile có 6 cửa hàng (TP.HCM, Đồng Tháp, Phan Thiết), mở cửa 8h–21h. Gọi hoặc Zalo %s để hỏi màu còn hàng và quà tặng." % site["hot"])]
    so = site["hot"].replace(".", "")
    t = html.escape(ten, quote=True)
    nut = ('<button class="btn btn-chinh" data-chat="Mình muốn đặt xe %s">Đặt xe</button>' % t if co_gia
           else '<button class="btn btn-chinh" data-chat="Cho mình hỏi giá %s">Hỏi giá</button>' % t)
    goc = GOC_LOAI[d][k]
    mac_dinh = '<section class="noi-dung hd-in"><h2>%s</h2>%s</section>' % (
        "Thông tin %s" % ten if vn else "Học sinh đi %s được không?" % ten, "".join("<p>%s</p>" % p for p in gioi))
    lq = _lien_quan(k, m)
    sp = {"@context": "https://schema.org", "@type": "Product", "name": ten, "url": "https://%s%s" % (d, url)}
    if hang:
        sp["brand"] = {"@type": "Brand", "name": hang}
    if m.get("price"):
        sp["offers"] = {"@type": "Offer", "price": int(m["price"]), "priceCurrency": "VND", "availability": "https://schema.org/InStock",
                        "seller": {"@type": "Organization", "name": "Smile Motor"}}

    tg = ""
    if m.get("price") and url:  # 21/10 10:24: .com.vn cũng có trả góp
        import tragop
        tg = ('<div class="sp-tg" data-sp-tg data-gia="%d" data-loai="%s"><span class="sp-tg-chu" data-sp-tg-chu>Xem số góp mỗi tháng theo 6 công ty tài chính</span>'
              '<a class="btn btn-phu sp-tg-nut" href="/tra-gop/?xe=%s">Tính trả góp xe này ›</a></div>'
              '<script src="/tra-gop.js" defer></script>' % (int(m["price"]), tragop._loai(m), url.strip("/").split("/")[-1]))

    def body(s):
        # ảnh chọn lúc dựng vì anhxe.WEB (khung theo từng web) chỉ đặt trong build(); schemas đọc sau body nên ảnh vẫn vào được
        muse = MUSE[d].get(ten.lower())  # bài Muse đọc trong build(), sau lúc dựng danh sách trang
        noi_dung = muse["html"] if muse else mac_dinh
        a = anhxe.anh(ten)
        if a:
            sp["image"] = "https://%s%s" % (d, a)
        hinh = ('<img src="%s" alt="%s" width="900" height="900" fetchpriority="high">' % (a, html.escape(ten))) if a else '<div class="khong-anh sp-cho"><b>%s</b><span>Ảnh xe thật đang cập nhật</span></div>' % html.escape(hang or ten)
        return f'''<div class="wrap"><div class="duong"><a href="/">Trang chủ</a> › <a href="{goc}">{loai}</a> › <b>{html.escape(ten)}</b></div>
<div class="sp">
<div class="sp-anh">{hinh}</div>
<div class="sp-tt"><span class="hang-xe-nho">{html.escape(hang)}</span><h1>{html.escape(h1)}<span class="sp-phu">{phu}</span></h1>
<div class="sp-gia{"" if co_gia else " lh"}">{gia}</div><p class="sp-chu">{chu_gia}</p>
<div class="sp-nut">{nut}<a class="btn btn-phu" href="tel:{so}">Gọi {site["hot"]}</a><a class="btn btn-phu btn-zalo" href="https://zalo.me/{so}" target="_blank" rel="noopener nofollow">{mxh.icon("zalo")}Zalo</a></div>
{tg}
{mxh.tra_gop()}
{('<table class="sp-ts">%s</table>' % bang_ts) if bang_ts else ""}</div></div>
{chot.xe(ten) if vn else ""}
{trangchu.diem_manh()}
{noi_dung}
{anhxe.luoi(lq, "Mẫu cùng tầm giá", 4, vnd)}
<section class="hd-in"><div class="tieude"><h2>Hỏi đáp về {html.escape(ten)}</h2></div>{faq_html_local(faqs)}</section>
{keu(site["cta_title"], site["cta_text"])}</div>'''

    return {"url": url, "title": title, "desc": desc, "body": body, "schemas": [sp, faq_ld_local(faqs)],
            "crumbs": [("Trang chủ", "/"), (loai, goc), (ten, url)]}


def gan(vn, comvn):
    xe = ds_xe()
    for site in (vn, comvn):
        # luật cứng: không thêm trang DV Motor trên .com.vn
        co = [(k, m) for k, m in xe if not (site["domain"] == "phoxedien.com.vn" and "dv motor" in (m.get("brand") or "").lower())]
        anhxe.SP[site["domain"]] = {m["name"].strip().lower() for _, m in co}
        anhxe.WEB = site["domain"]  # url_xe đọc theo web
        site["pages"][-1:-1] = [trang(site, k, m) for k, m in co]
    anhxe.WEB = ""
