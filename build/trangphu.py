# -*- coding: utf-8 -*-
"""Trang Tin tức và Liên hệ trên thanh menu (anh chốt 20/10 23:33), dùng chung cho hai web."""
import html

import chinhsach
import mxh


def _the_bai(a):
    bia = ('<img src="/anh/%s.webp" alt="%s" width="400" height="225" loading="lazy">' % (a["slug"], html.escape(a.get("anh_alt") or a["h1"], quote=True))
           if a.get("anh") else '<span class="tin-o">%s</span>' % html.escape(a["cat_name"]))
    return ('<a class="tin-the" href="%s"><span class="tin-bia">%s</span><span class="nd"><small>%s</small><b>%s</b></span></a>'
            % (a["url"], bia, html.escape(a["cat_name"]), html.escape(a["h1"])))


def tin_tuc(site):
    def body(s):
        arts = site["articles"]
        muc = []
        for a in arts:
            if (a["cat_name"], a["cat_url"]) not in muc:
                muc.append((a["cat_name"], a["cat_url"]))
        chips = "".join('<a class="chip" href="%s">%s</a>' % (u, html.escape(n)) for n, u in muc)
        return ('<div class="wrap rong"><div class="duong"><a href="/">Trang chủ</a> › <b>Tin tức</b></div>'
                '<div class="mo-dau"><h1>Tin tức xe điện, xe 50cc</h1><p>%d bài: bảng giá, so sánh, kinh nghiệm chọn xe và chăm xe, cập nhật thường xuyên.</p></div>'
                '%s<section class="tin"><div class="luoi-tin">%s</div></section></div>'
                % (len(arts), ('<nav class="chips" style="padding:0 0 14px">%s</nav>' % chips) if chips else "", "".join(_the_bai(a) for a in arts)))
    return {"url": "/tin-tuc/", "title": "Tin tức xe điện, xe 50cc",
            "desc": "Tin tức, bảng giá, so sánh và kinh nghiệm chọn xe điện, xe 50cc từ %s, cập nhật thường xuyên." % site["sitename"],
            "body": body, "crumbs": [("Trang chủ", "/"), ("Tin tức", "/tin-tuc/")]}


def lien_he(site, stores_html, tel, hotline):
    so = hotline.replace(".", "")

    def body(s):
        cs = chinhsach.link_chan()
        return f'''<div class="wrap rong"><div class="duong"><a href="/">Trang chủ</a> › <b>Liên hệ</b></div>
<div class="mo-dau"><h1>Liên hệ Xe Điện Smile</h1><p>Hỏi giá, màu còn hàng, trả góp hay đặt xe: gọi, nhắn Zalo hoặc chat ngay trên trang. Cửa hàng mở cửa 8h–21h mỗi ngày.</p></div>
<div class="lh-nut">
<a class="lh-o" href="tel:{tel}"><b>Gọi hotline</b><span>{hotline}</span></a>
<a class="lh-o" href="https://zalo.me/{so}" target="_blank" rel="noopener nofollow">{mxh.icon("zalo")}<b>Nhắn Zalo</b><span>{hotline}</span></a>
<button type="button" class="lh-o" data-chat><b>Chat tư vấn</b><span>Trả lời ngay trên trang</span></button>
</div>
<section><div class="tieude"><h2>Theo dõi Xe Điện Smile</h2></div>{mxh.hang(hotline, "mxh-to")}</section>
{mxh.tra_gop("tg-to")}
<section class="lh-trang">{stores_html(site)}</section>
{('<section class="lh-ct">%s</section>' % chinhsach.cong_ty_html()) if chinhsach.cong_ty_html() else ""}
{('<section><div class="tieude"><h2>Chính sách</h2></div><nav class="chips" style="padding:0;flex-wrap:wrap">%s</nav></section>' % "".join('<a class="chip" href="%s">%s</a>' % (u, n) for n, u in cs)) if cs else ""}
</div>'''
    return {"url": "/lien-he/", "title": "Liên hệ: hotline %s, 6 cửa hàng Smile" % hotline,
            "desc": "Gọi hoặc Zalo %s để hỏi giá, màu còn hàng và đặt xe. Địa chỉ và bản đồ 6 cửa hàng Smile Motor, mở cửa 8h–21h." % hotline,
            "body": body, "crumbs": [("Trang chủ", "/"), ("Liên hệ", "/lien-he/")]}


def gan(vn, comvn, stores_html, tel_cua):
    for site in (vn, comvn):
        tel, hot = tel_cua(site)
        site["pages"].insert(-1, tin_tuc(site))
        site["pages"].insert(-1, lien_he(site, stores_html, tel, hot))
