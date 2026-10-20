# -*- coding: utf-8 -*-
"""Chính sách và thông tin công ty trên chân trang hai web (anh góp ý 20/10 23:32): đổi trả, bảo hành, bảo hành giá,
bảo mật thông tin, cùng thông tin Công ty TNHH Xe Điện Smile. Nội dung máy nhà lấy từ xediensmile.com (web của Smile):
PXD_KHO/chinh-sach/<slug>.md (dòng đầu "# Tiêu đề", sau đó đoạn văn, "## mục", "- ý") và PXD_KHO/chinh-sach/cong-ty.json
{"ten", "dia_chi", "dien_thoai", "email", "giay_phep", "nguoi_dai_dien"}. Thiếu tệp nào thì phần đó không hiện."""
import html
import json
import os
import re

GOC = os.path.join(os.environ.get("PXD_KHO", "").strip(), "chinh-sach") if os.environ.get("PXD_KHO", "").strip() else ""
# thứ tự hiện ở chân trang; tệp .md khác trong thư mục xếp sau
THU_TU = ["doi-tra", "bao-hanh", "bao-hanh-gia", "bao-mat", "tra-gop", "van-chuyen"]


def _doc_md(f):
    dong = open(f, encoding="utf-8-sig").read().strip().splitlines()
    if not dong or not dong[0].startswith("# "):
        return None
    tieu_de, o, ds = dong[0][2:].strip(), [], []

    def chu(t):
        t = html.escape(t.strip())
        return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)

    def dong_ds():
        if ds:
            o.append("<ul>%s</ul>" % "".join("<li>%s</li>" % x for x in ds))
            ds.clear()
    for d in dong[1:]:
        d = d.rstrip()
        if d.startswith("- ") or d.startswith("* "):
            ds.append(chu(d[2:]))
            continue
        dong_ds()
        if d.startswith("### "):
            o.append("<h3>%s</h3>" % chu(d[4:]))
        elif d.startswith("## "):
            o.append("<h2>%s</h2>" % chu(d[3:]))
        elif d.strip():
            o.append("<p>%s</p>" % chu(d))
    dong_ds()
    return tieu_de, "\n".join(o)


def ds_chinh_sach():
    if not (GOC and os.path.isdir(GOC)):
        return []
    tep = [f[:-3] for f in os.listdir(GOC) if f.endswith(".md")]
    tep.sort(key=lambda s: (THU_TU.index(s) if s in THU_TU else 99, s))
    ra = []
    for s in tep:
        r = _doc_md(os.path.join(GOC, s + ".md"))
        if r:
            ra.append((s, r[0], r[1]))
    return ra


def cong_ty():
    f = os.path.join(GOC, "cong-ty.json") if GOC else ""
    if not (f and os.path.isfile(f)):
        return {}
    try:
        return json.load(open(f, encoding="utf-8-sig"))
    except ValueError:
        return {}


def cong_ty_html():
    c = cong_ty()
    if not c.get("ten"):
        return ""
    o = ['<b class="ct-ten">%s</b>' % html.escape(c["ten"])]
    for k, nhan in (("dia_chi", "Địa chỉ"), ("giay_phep", "Giấy phép"), ("nguoi_dai_dien", "Người đại diện"), ("dien_thoai", "Điện thoại"), ("email", "Email")):
        if c.get(k):
            v = html.escape(c[k])
            if k == "email":
                v = '<a href="mailto:%s">%s</a>' % (v, v)
            o.append("<span>%s: %s</span>" % (nhan, v))
    return '<div class="cong-ty">%s</div>' % "".join(o)


def link_chan():
    return [(t, "/chinh-sach/%s/" % s) for s, t, _ in ds_chinh_sach()]


def gan(vn, comvn):
    cs = ds_chinh_sach()
    for site in (vn, comvn):
        for s, t, noi in cs:
            url = "/chinh-sach/%s/" % s

            def body(_s, t=t, noi=noi, site=site):
                return ('<div class="wrap doc"><div class="duong"><a href="/">Trang chủ</a> › <b>%s</b></div>'
                        '<div class="dau-trang"><h1>%s</h1></div><div class="noi-dung chinh-sach">%s</div>%s</div>'
                        % (html.escape(t), html.escape(t), noi, cong_ty_html()))
            site["pages"].insert(-1, {"url": url, "title": "%s | %s" % (t, "Xe Điện Smile"),
                                      "desc": ("%s của Xe Điện Smile áp dụng khi mua xe tại các cửa hàng Smile Motor: điều kiện, thời hạn và cách liên hệ." % t)[:160],
                                      "body": body, "crumbs": [("Trang chủ", "/"), (t, url)]})
