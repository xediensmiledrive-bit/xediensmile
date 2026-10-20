# -*- coding: utf-8 -*-
"""Trang chủ kiểu web bán xe (anh góp ý 20/10 18:58): hãng xe và thẻ xe có ảnh, giá ngay trên trang chủ;
cẩm nang, giấy tờ, sửa xe, hỏi đáp gom vào mục Tin tức thay vì dẫn đi vòng vòng."""
import html

import anhxe
import noidung
from noidung import NHOM, THANG, vnd, models_of, tom_gia, keu, faq_html_local, xe_svg, dap_svg

LOAI = {"phoxedien.vn": [("may", "/xe-may-dien/"), ("ga", "/xe-ga-50cc/"), ("so", "/xe-so-50cc/"), ("dap", "/xe-dap-dien/"), ("ba", "/xe-dien-3-banh/")],
        "phoxedien.com.vn": [("may", "/xe-may-dien-cho-hoc-sinh/"), ("ga", "/xe-ga-50cc-cho-hoc-sinh/"), ("so", "/xe-so-50cc-cho-hoc-sinh/"), ("dap", "/xe-dap-dien-cho-hoc-sinh/")]}
BAN = ["may", "ga", "so"]  # loại có thẻ xe trên trang chủ
HIEN = 12                  # số thẻ hiện trước, bấm "Xem thêm" để mở tiếp


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


def _loai_xe(site):
    o = []
    for k, url in LOAI[site["domain"]]:
        ms = models_of(k) if k not in noidung.NGUNG_BAN else []
        a = next((anhxe.anh(m["name"]) for m in ms if anhxe.anh(m["name"])), None)
        hinh = '<img src="%s" alt="" width="96" height="72" loading="lazy">' % a if a else (dap_svg("#3aa52a", "#f26b1d") if k == "dap" else xe_svg("#3aa52a", "#f26b1d"))
        o.append('<a class="lx" href="%s"><span class="lx-anh">%s</span><b>%s</b><small>%s</small></a>' % (url, hinh, NHOM[k][0], noidung.gia_tu(k)))
    return '<nav class="loai-xe" aria-label="Loại xe">%s</nav>' % "".join(o)


def _hang(xe):
    dem = {}
    for k, m in xe:
        b = m.get("brand") or ""
        if b:
            d = dem.setdefault(b, [0, None])
            d[0] += 1
            d[1] = d[1] or anhxe.anh(m["name"])
    if len(dem) < 2:
        return ""
    o = ['<button type="button" class="hx on" data-hang=""><span class="hx-anh tat-ca">Tất cả</span><b>Tất cả hãng</b><small>%d mẫu</small></button>' % len(xe)]
    for b, (n, a) in sorted(dem.items(), key=lambda x: -x[1][0])[:11]:
        o.append('<button type="button" class="hx" data-hang="%s"><span class="hx-anh">%s</span><b>%s</b><small>%d mẫu</small></button>'
                 % (html.escape(b), '<img src="%s" alt="" width="96" height="72" loading="lazy">' % a if a else html.escape(b[:2].upper()), html.escape(b), n))
    return '<div class="hang-xe">%s</div>' % "".join(o)


def _tin(site, arts, chips):
    o = []
    for a in arts[:6]:
        bia = '<img src="/anh/%s.webp" alt="%s" width="400" height="225" loading="lazy">' % (a["slug"], html.escape(a.get("anh_alt") or a["h1"])) if a.get("anh") else '<span class="tin-o">%s</span>' % a["emoji"]
        o.append('<a class="tin-the hd-in" href="%s"><span class="tin-bia">%s</span><span class="nd"><small>%s</small><b>%s</b></span></a>' % (a["url"], bia, a["cat_name"], html.escape(a["h1"])))
    c = "".join('<a class="chip" href="%s">%s</a>' % x for x in chips)
    return ('<section class="tin"><div class="tieude"><h2>Tin tức</h2><a href="%s">Tất cả ›</a></div><nav class="chips" style="padding:0 0 12px">%s</nav>'
            '<div class="luoi-tin">%s</div></section>' % (chips[0][1], c, "".join(o)))


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
    return f'''<div class="wrap">
<div class="mo-dau"><h1>{h1}</h1><p>{mo_ta}</p></div>
{_loai_xe(site)}
{ban}
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
        "phoxedien.com.vn": dict(h1="Xe 50cc và xe điện cho học sinh",
                                 mo_ta="Xe ga, xe số 50cc và xe máy điện hợp tuổi học sinh, có ảnh thật và giá tham khảo.",
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
