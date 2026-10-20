# -*- coding: utf-8 -*-
"""Clip review thật từ kênh TikTok @xediensmiledrama (anh chốt 21/10 1:17: clip dọc có khung, trôi từ trái qua phải, đặt ngay trên mục tin tức);
trước đó là clip TikTok Smile Motor chạy vòng trên trang chủ phoxedien.vn, tự phát không tiếng (anh chốt 21/10 0:01), kèm link web Smile Motor.
Máy nhà lấy clip mới nhất của kênh mỗi ngày, ghi PXD_KHO/tiktok-smile.json:
{"cap_nhat", "tai_khoan": "@...", "link": "https://www.tiktok.com/@...", "web": "https://...", "web_ten": "Smile Motor",
 "video": [{"id": "7xxxxxxxxxxxxxxxxxx", "mo_ta": "...", "anh": "<id>.webp"}]}
Ảnh bìa (nếu có) để ở PXD_KHO/tiktok/<anh>. Thiếu tệp thì mục không hiện."""
import html
import json
import os
import re
import shutil

GOC = os.environ.get("PXD_KHO", "").strip()
WEB = ["phoxedien.vn"]
TOI_DA = 16


def _doc():
    f = os.path.join(GOC, "tiktok-smile.json") if GOC else ""
    if not (f and os.path.isfile(f)):
        return None
    try:
        d = json.load(open(f, encoding="utf-8-sig"))
    except ValueError:
        return None
    d["video"] = [v for v in d.get("video", []) if re.fullmatch(r"\d{15,22}", str(v.get("id", "")))][:TOI_DA]
    return d if d["video"] else None


def _https(u):
    u = (u or "").strip()
    return u if u.startswith("https://") else ""


def _anh(v):
    a = os.path.basename(v.get("anh") or "")
    return a if a and GOC and os.path.isfile(os.path.join(GOC, "tiktok", a)) else ""


LOGO = ('<svg class="tt-logo" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M16.6 5.8A4.3 4.3 0 0 1 15.5 3h-3.1v12.4a2.6 2.6 0 1 1-2.6-2.6c.3 0 .5 0 .8.1V9.7a5.7 5.7 0 1 0 4.9 5.7V9.1a7.4 7.4 0 0 0 4.3 1.4V7.4a4.3 4.3 0 0 1-3.2-1.6z"/></svg>')


def html_muc(site):
    if site["domain"] not in WEB:
        return ""
    d = _doc()
    if not d:
        return ""
    o = []
    for v in d["video"]:
        mo = html.escape((v.get("mo_ta") or "").strip()[:90], quote=True)
        a = _anh(v)
        bia = ('<img src="/tiktok/%s" alt="%s" width="270" height="480" loading="lazy">' % (a, mo or "Clip review xe trên TikTok")) if a else LOGO
        o.append('<a class="tt-o" href="https://www.tiktok.com/%s/video/%s" target="_blank" rel="noopener nofollow" data-tt="%s" aria-label="Xem clip trên TikTok">%s'
                 '<span class="tt-chu">%s</span></a>' % (html.escape(d.get("tai_khoan") or "@", quote=True), v["id"], v["id"], bia, mo))
    kenh = _https(d.get("link"))
    web = _https(d.get("web"))
    nut = "".join([
        ('<a class="tt-nut" href="%s" target="_blank" rel="noopener nofollow">%s Kênh TikTok %s</a>' % (html.escape(kenh, quote=True), LOGO, html.escape(d.get("tai_khoan") or ""))) if kenh else "",
        ('<a class="tt-nut tt-web" href="%s" target="_blank" rel="noopener">Web %s ›</a>' % (html.escape(web, quote=True), html.escape(d.get("web_ten") or "Smile Motor"))) if web else ""])
    return ('<section class="tiktok"><div class="tieude"><h2>Clip review thật trên TikTok</h2></div>'
            '<div class="tt-dai"><div class="tt-chay">%s<div class="tt-lap" aria-hidden="true">%s</div></div></div><div class="tt-nuts">%s</div></section>'
            % ("".join(o), "".join(o).replace('data-tt=', 'tabindex="-1" data-tt='), nut))


def chep(site, base):
    d = _doc() if site["domain"] in WEB else None
    if not d:
        return
    for v in d["video"]:
        a = _anh(v)
        if a:
            os.makedirs(os.path.join(base, "tiktok"), exist_ok=True)
            shutil.copy(os.path.join(GOC, "tiktok", a), os.path.join(base, "tiktok"))
