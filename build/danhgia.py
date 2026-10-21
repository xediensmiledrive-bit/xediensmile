# -*- coding: utf-8 -*-
"""Mục "Khách hàng nói gì" trên trang chủ .vn, ngay trên bảng giá (anh chốt 20/10 20:37).
Chỉ dùng đánh giá thật máy nhà tải từ Google Maps các chi nhánh Xe Điện Smile, không tự viết:
PXD_KHO/review-smile.json {"cap_nhat", "chi_nhanh": [{ten, dia_chi, map, sao_tb, so_danh_gia}],
                           "reviews": [{chi_nhanh, ten, sao, ngay, noi_dung, link_map}]}
Ảnh khách thật (Y:\\CLAUDE\\KHACH DV MOTOR) máy nhà đã chèn khung có logo từng web, để ở
PXD_KHO/anh-khach/<domain>/*.webp. Luật cứng: không dùng ảnh chưa có khung, nên chỉ đọc đúng thư mục đó.
Thiếu tệp thì mục không hiện."""
import html
import re
import json
import os
import shutil

GOC = os.environ.get("PXD_KHO", "").strip()
WEB = ["phoxedien.vn", "phoxedien.com.vn"]
HIEN = 12
ANH_TOI_DA = 16


def _doc():
    f = os.path.join(GOC, "review-smile.json") if GOC else ""
    if not (f and os.path.isfile(f)):
        return None
    try:
        d = json.load(open(f, encoding="utf-8-sig"))
    except ValueError:
        return None
    ds = [r for r in d.get("reviews", []) if (r.get("noi_dung") or "").strip() and int(r.get("sao") or 0) >= 4]
    cn = [c for c in d.get("chi_nhanh", []) if c.get("so_danh_gia")]
    tong = {}
    if cn:
        so = sum(int(c["so_danh_gia"]) for c in cn)
        tong = {"so": so, "diem": sum(float(c.get("sao_tb") or 0) * int(c["so_danh_gia"]) for c in cn) / so,
                "link": max(cn, key=lambda c: int(c["so_danh_gia"])).get("map"), "cn": len(cn)}
    return {"tong": tong, "ds": ds[:HIEN]} if ds else None


def _anh_khach(d):
    tm = os.path.join(GOC, "anh-khach", d) if GOC else ""
    if not (tm and os.path.isdir(tm)):
        return []
    return sorted(f for f in os.listdir(tm) if f.lower().endswith(".webp"))[:ANH_TOI_DA]


def _link(u):
    u = (u or "").strip()
    return u if u.startswith("https://") and ("google." in u or "goo.gl" in u) else ""


def _sao(n):
    n = max(0, min(5, int(round(float(n or 0)))))
    return '<span class="dg-sao" aria-label="%d trên 5 sao">%s<i class="tat">%s</i></span>' % (n, "★" * n, "★" * (5 - n))


G = ('<svg class="dg-g" viewBox="0 0 48 48" aria-hidden="true"><path fill="#4285F4" d="M45 24.5c0-1.6-.1-3.1-.4-4.5H24v8.5h11.8c-.5 2.7-2.1 5-4.4 6.6v5.5h7.1c4.2-3.9 6.5-9.6 6.5-16.1z"/>'
     '<path fill="#34A853" d="M24 46c5.9 0 10.9-2 14.5-5.4l-7.1-5.5c-2 1.3-4.5 2.1-7.4 2.1-5.7 0-10.5-3.8-12.2-9H4.5v5.7C8.1 41.1 15.5 46 24 46z"/>'
     '<path fill="#FBBC05" d="M11.8 28.2c-.4-1.3-.7-2.7-.7-4.2s.3-2.9.7-4.2v-5.7H4.5C3 17.1 2 20.4 2 24s1 6.9 2.5 9.9l7.3-5.7z"/>'
     '<path fill="#EA4335" d="M24 10.8c3.2 0 6.1 1.1 8.4 3.3l6.3-6.3C34.9 4.2 29.9 2 24 2 15.5 2 8.1 6.9 4.5 14.1l7.3 5.7c1.7-5.2 6.5-9 12.2-9z"/></svg>')


def _tieu_de(r):
    """Chủ đề ngắn của đánh giá: máy nhà ghi sẵn "tieu_de" thì dùng, không thì lấy câu đầu của chính khách (không tự viết lời khách)."""
    t = (r.get("tieu_de") or "").strip()
    if t:
        return t
    c = re.split(r"(?<=[.!?…])\s", r["noi_dung"].strip())[0].strip(" .")
    if len(c) > 60:
        c = c[:58].rsplit(" ", 1)[0] + "…"
    return c


def _the(r):
    ten = (r.get("ten") or "Khách hàng").strip()
    lk = _link(r.get("link_map"))
    noi = '<a class="dg-nguon" href="%s" target="_blank" rel="noopener nofollow" aria-label="Xem đánh giá trên Google Maps">%s</a>' % (html.escape(lk, quote=True), G) if lk else '<span class="dg-nguon">%s</span>' % G
    anh = ('<img class="dg-anh" src="/anh-khach/%s" alt="%s nhận xe tại Xe Điện Smile" width="400" height="400" loading="lazy">' % (html.escape(r["anh"], quote=True), html.escape(ten, quote=True))
           if r.get("anh") else "")
    return ('<figure class="dg-the">%s<figcaption class="dg-dau"><span class="dg-av">%s</span><span><b>%s</b><small>%s</small></span>%s</figcaption>%s'
            '<b class="dg-chu-de">“%s”</b><blockquote>%s</blockquote>%s</figure>'
            % (anh, html.escape(ten[:1].upper()), html.escape(ten), html.escape(str(r.get("ngay") or "").strip()), noi, _sao(r.get("sao")),
               html.escape(_tieu_de(r)), html.escape(r["noi_dung"].strip()),
               '<p class="dg-ch">%s</p>' % html.escape(r["chi_nhanh"].strip()) if (r.get("chi_nhanh") or "").strip() else ""))


def html_muc(site):
    """Bằng chứng khách hàng ngay dưới banner trang chủ (anh chốt 20/10 23:59): ảnh khách thật chạy vòng, review Google thật chạy ngược chiều."""
    if site["domain"] not in WEB:
        return ""
    d = _doc() or {"tong": {}, "ds": []}
    anh = _anh_khach(site["domain"])
    if not d["ds"] and not anh:
        return ""
    t = d["tong"]
    tong = ""
    if t:
        lk = _link(t.get("link"))
        tong = ('<div class="dg-tong">%s<b>%s</b>%s<span class="dg-so">%s đánh giá trên Google Maps%s</span>%s</div>'
                % (G, ("%.1f" % t["diem"]).replace(".", ","), _sao(t["diem"]), "{:,}".format(t["so"]).replace(",", "."),
                   " · %d chi nhánh" % t["cn"] if t["cn"] > 1 else "",
                   '<a href="%s" target="_blank" rel="noopener nofollow">Xem trên Google Maps ›</a>' % html.escape(lk, quote=True) if lk else ""))
    # dải chạy vòng: nhân đôi nội dung để chạy liền không giật; bản thứ hai ẩn với trình đọc màn hình
    def dai(lop, o):
        if not o:
            return ""
        return '<div class="dg-dai %s"><div class="dg-chay">%s<div class="dg-lap" aria-hidden="true">%s</div></div></div>' % (lop, "".join(o), "".join(o))
    kh = dai("dg-khach", ['<img src="/anh-khach/%s" alt="Khách nhận xe tại Xe Điện Smile" width="400" height="400" loading="lazy">' % f for f in anh])
    rv = dai("dg-ray", [_the(r) for r in d["ds"]])
    return ('<section class="danh-gia bang-chung"><div class="tieude"><h2>Khách hàng nói gì về Smile</h2></div>'
            '<p class="dg-mo">Ảnh thật khách nhận xe tại cửa hàng và đánh giá thật trên Google Maps.</p>%s%s%s</section>'
            % (tong, kh, rv))


def chep(site, base):
    """Chép ảnh khách đã có khung của web này sang bản dựng."""
    anh = _anh_khach(site["domain"]) if site["domain"] in WEB else []
    anh += [r["anh"] for r in ((_doc() or {}).get("ds") or []) if r.get("anh") and r["anh"] not in anh
            and os.path.isfile(os.path.join(GOC, "anh-khach", site["domain"], r["anh"]))]
    if anh:
        os.makedirs(os.path.join(base, "anh-khach"), exist_ok=True)
        for f in anh:
            shutil.copy(os.path.join(GOC, "anh-khach", site["domain"], f), os.path.join(base, "anh-khach"))
