# -*- coding: utf-8 -*-
"""Trang chủ kiểu web bán xe (anh góp ý 20/10 18:58): hãng xe và thẻ xe có ảnh, giá ngay trên trang chủ;
cẩm nang, giấy tờ, sửa xe, hỏi đáp gom vào mục Tin tức thay vì dẫn đi vòng vòng."""
import html
import os

import anhxe
import danhgia
import tiktok
import noidung
HERE = os.path.dirname(os.path.abspath(__file__))
from noidung import NHOM, THANG, vnd, models_of, tom_gia, keu, faq_html_local, xe_svg, dap_svg

LOAI = {"phoxedien.vn": [("may", "/xe-may-dien/"), ("ga", "/xe-ga-50cc/"), ("so", "/xe-so-50cc/"), ("wave", "/xe-wave-50cc/"), ("dap", "/xe-dap-dien/"), ("ba", "/xe-dien-3-banh/")],
        "phoxedien.com.vn": [("may", "/xe-may-dien-cho-hoc-sinh/"), ("ga", "/xe-ga-50cc-cho-hoc-sinh/"), ("so", "/xe-so-50cc-cho-hoc-sinh/"), ("dap", "/xe-dap-dien-cho-hoc-sinh/")]}
BAN = ["may", "ga", "so"]  # loại có thẻ xe trên trang chủ
HIEN = 10                  # số thẻ hiện trước, bấm "Xem thêm" để mở tiếp


def _gia(m):
    if m.get("price"):
        return vnd(m["price"]), ""
    tt = noidung.GIA_TT.get((m.get("name") or "").strip().lower())
    return (vnd(tt) + " <small>giá thị trường</small>", "") if tt else ("Liên hệ", " lh")


def _xe():
    ra, thay = [], set()
    for k in BAN:
        for m in models_of(k):
            if m["name"] not in thay:
                thay.add(m["name"])
                ra.append((k, m))
    co = [x for x in ra if anhxe.anh(x[1]["name"])]
    if co:  # có ảnh thật thì chỉ hiện xe có ảnh (anh không muốn hình vẽ thay ảnh)
        ra = co
    # có ảnh lên trước, rồi xen kẽ hãng để trang không chỉ toàn một hãng
    theo = {}
    for k, m in sorted(ra, key=lambda x: anhxe.anh(x[1]["name"]) is None):
        theo.setdefault(m.get("brand") or "", []).append((k, m))
    xen = []
    while any(theo.values()):
        for v in theo.values():
            if v:
                xen.append(v.pop(0))
    return xen


def _the(k, m, svg):
    a = anhxe.anh(m["name"])
    g, lop = _gia(m)
    hinh = ('<img src="%s" alt="%s" width="300" height="225" loading="lazy">' % (a, html.escape(m["name"]))) if a else '<div class="khong-anh">%s</div>' % svg
    ten = '<b>%s</b>' % html.escape(m["name"])
    u = anhxe.url_xe(m["name"])
    if u:
        hinh, ten = '<a href="%s">%s</a>' % (u, hinh), '<a class="ten-xe" href="%s">%s</a>' % (u, ten)
    return ('<div class="o-xe" data-loai="%s" data-hang="%s">%s<div class="nd"><span class="hang-xe-nho">%s</span>%s'
            '<span class="gia%s">%s</span>%s</div></div>'
            % (k, html.escape(m.get("brand") or ""), hinh, html.escape(m.get("brand") or ""), ten, lop, g, anhxe.nut(m, not lop)))


def anh_loai(k):
    """Ảnh ô loại xe: build/loai/<k>.webp, hoặc PXD_ANH/danh-muc/<k>.webp do luồng ảnh dựng trên máy nhà."""
    for tm in (os.path.join(HERE, "loai"), os.path.join(anhxe.GOC, "danh-muc") if anhxe.GOC else ""):
        if tm and os.path.isfile(os.path.join(tm, k + ".webp")):
            return os.path.join(tm, k + ".webp")
    return None


def _loai_xe(site):
    """Hàng loại xe: mỗi ô một ảnh xe thật đã tách nền (build/loai/<khoá>.webp), cùng cỡ, cùng nền.
    Loại nào chưa có ảnh tách nền thì chưa hiện ô (anh không muốn hình vẽ hay hình lỗi, 20/10 19:27)."""
    o = []
    for k, url in LOAI[site["domain"]]:
        if not anh_loai(k):
            continue
        o.append('<a class="lx" href="%s"><span class="lx-anh"><img src="/loai/%s.webp" alt="%s" width="360" height="270" loading="lazy"></span><b>%s</b><small>%s</small></a>'
                 % (url, k, NHOM[k][0], NHOM[k][0], noidung.gia_tu(k)))
    return '<nav class="loai-xe" aria-label="Loại xe">%s</nav>' % "".join(o) if o else ""


def _hang(xe):
    """Lọc theo hãng: nút chữ gọn, cùng cỡ (ảnh khung thu nhỏ ở đây khó đọc, anh chê 20/10 19:27)."""
    dem = {}
    for k, m in xe:
        b = m.get("brand") or ""
        if b:
            dem[b] = dem.get(b, 0) + 1
    if len(dem) < 2:
        return ""
    o = ['<button type="button" class="hx on" data-hang=""><b>Tất cả</b><small>%d</small></button>' % len(xe)]
    for b, n in sorted(dem.items(), key=lambda x: -x[1])[:12]:
        o.append('<button type="button" class="hx" data-hang="%s"><b>%s</b><small>%d</small></button>' % (html.escape(b), html.escape(b), n))
    return '<div class="hang-xe">%s</div>' % "".join(o)


def _tin(site, arts, chips):
    o = []
    for a in arts[:6]:
        # chưa có ảnh bìa: ô chữ theo chuyên mục, không dùng emoji
        bia = ('<img src="/anh/%s.webp" alt="%s" width="400" height="225" loading="lazy">' % (a["slug"], html.escape(a.get("anh_alt") or a["h1"])) if a.get("anh")
               else '<span class="tin-o">%s</span>' % html.escape(a["cat_name"]))
        o.append('<a class="tin-the hd-in" href="%s"><span class="tin-bia">%s</span><span class="nd"><small>%s</small><b>%s</b></span></a>' % (a["url"], bia, a["cat_name"], html.escape(a["h1"])))
    c = "".join('<a class="chip" href="%s">%s</a>' % (u, n) for n, u in chips)
    return ('<section class="tin"><div class="tieude"><h2>Tin tức</h2><a href="%s">Tất cả ›</a></div><nav class="chips" style="padding:0 0 12px">%s</nav>'
            '<div class="luoi-tin">%s</div></section>' % (chips[0][1], c, "".join(o)))


# Điểm mạnh Smile (anh nêu 20/10 23:33): hiện ngay dưới banner trang chủ và trên trang xe
DIEM_MANH = [
    ("cua-hang", "6 cửa hàng", "TP.HCM, Đồng Tháp, Phan Thiết"),
    ("kinh-nghiem", "10 năm kinh nghiệm", "Bán và sửa xe điện, xe 50cc"),
    ("bao-hanh", "Bảo hành phụ tùng 7 năm", "Theo chính sách Xe Điện Smile"),
    ("gia", "Giá cập nhật hằng tháng", "Có ảnh thật từng mẫu xe"),
]
_ICON = {
    "cua-hang": '<path d="M3 9l1.5-5h15L21 9M3 9h18M3 9a3 3 0 0 0 6 0 3 3 0 0 0 6 0 3 3 0 0 0 6 0M5 12v8h14v-8M10 20v-5h4v5"/>',
    "kinh-nghiem": '<circle cx="12" cy="9" r="6"/><path d="M8.5 14L7 22l5-3 5 3-1.5-8"/>',
    "bao-hanh": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "gia": '<path d="M20.6 13.4L13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
}


def diem_manh():
    return '<div class="diem-manh">%s</div>' % "".join(
        '<div class="dm"><svg viewBox="0 0 24 24" aria-hidden="true">%s</svg><span><b>%s</b><small>%s</small></span></div>' % (_ICON[k], t, p)
        for k, t, p in DIEM_MANH)


def trang_chu(site, h1, mo_ta, bang_gia, tom, chips, faqs):
    xe = _xe()
    svg = xe_svg("#3aa52a", "#f26b1d")
    the = "".join(_the(k, m, svg) for k, m in xe)
    tab = "".join('<button type="button" class="chip" data-tab="%s">%s</button>' % (k, NHOM[k][0]) for k in BAN if any(x[0] == k for x in xe))
    ban = ""
    if xe:
        ban = ('<section id="xe-ban"><div class="tieude"><h2>Xe đang bán</h2><a href="%s">Bảng giá đủ ›</a></div>%s'
               '<nav class="chips tab-xe" style="padding:0 0 12px"><button type="button" class="chip on" data-tab="">Tất cả</button>%s</nav>'
               '<div class="luoi-xe ban-xe" data-hien="%d">%s</div>'
               '<button type="button" class="btn xem-them">Xem thêm xe</button>'
               '<p class="chu-anh">Giá tham khảo cập nhật %s. Màu xe thực tế có thể khác ảnh.</p></section>'
               % (bang_gia, _hang(xe), tab, HIEN, the, noidung.NGAY_VN))
    # 20/10 23:59: ngay dưới banner là bằng chứng khách hàng thay cho hàng ô loại xe (loại xe đã có trên menu)
    return f'''<div class="wrap rong">
{danhgia.html_muc(site) or _loai_xe(site)}
{diem_manh()}
<div class="mo-dau"><h1>{h1}</h1><p>{mo_ta}</p></div>
{ban}
{tiktok.html_muc(site)}
<section><div class="tieude"><h2>Giá tham khảo tháng {THANG}</h2><a href="{bang_gia}">Xem đủ ›</a></div>
<div class="the bang hd-in"><div class="dong dau"><span>Nhóm xe</span><span>Giá tham khảo</span></div>{tom_gia(tom)}</div></section>
{_tin(site, site["articles"], chips)}
{keu(site["cta_title"], site["cta_text"])}
<section class="hd-in"><div class="tieude"><h2>Hỏi nhanh đáp gọn</h2></div>{faq_html_local(faqs)}</section>
</div>'''


def gan(vn, comvn):
    """Thay thân trang chủ hai web bằng bố cục bán xe."""
    from noidung import FAQ_VN_HOME, FAQ_COMVN
    cau_hinh = {
        "phoxedien.vn": dict(h1="Bảng giá xe điện, xe 50cc tháng " + THANG,
                             mo_ta="Đủ hãng, ảnh thật, giá tham khảo cập nhật hằng tháng. Đặt xe nhanh qua điện thoại hoặc Zalo.",
                             bang_gia="/bang-gia-xe-dien/", tom=["may", "ga", "so", "dap", "ba"],
                             chips=[("So sánh và đánh giá", "/so-sanh/"), ("Bảng giá xe điện", "/bang-gia-xe-dien/"), ("Bảng giá xe 50cc", "/bang-gia-xe-50cc/")],
                             faqs=FAQ_VN_HOME),
        "phoxedien.com.vn": dict(h1="Xe ga, xe số 50cc và xe máy điện",
                                 mo_ta="Xe hợp tuổi từ 16, không cần bằng lái. Ảnh thật, giá tham khảo cập nhật hằng tháng.",
                                 bang_gia="/gia-xe-50cc/", tom=["ga", "so", "may", "dap"],
                                 chips=[("Cẩm nang", "/cam-nang/"), ("Xe cho học sinh", "/cam-nang/?muc=hoc-sinh"), ("Tuổi và bằng lái", "/cam-nang/?muc=giay-to"),
                                        ("Pin, sạc, sửa xe", "/cam-nang/?muc=sua-xe"), ("Hỏi đáp", "/hoi-dap/")],
                                 faqs=FAQ_COMVN[:3]),
    }
    for site in (vn, comvn):
        ch = cau_hinh[site["domain"]]
        for p in site["pages"]:
            if p["url"] == "/":
                p["body"] = lambda s, site=site, ch=ch: trang_chu(site, **ch)
