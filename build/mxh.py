# -*- coding: utf-8 -*-
"""Logo mạng xã hội và logo công ty trả góp (anh chốt 21/10 0:36: hiện bằng logo của họ, không phải chữ, để tăng nhận diện).
Link mạng xã hội: PXD_KHO/mang-xa-hoi.json {"facebook","youtube","instagram","tiktok","zalo"}; thiếu mục nào thì bỏ mục đó
(Zalo luôn có, mặc định zalo.me/<hotline web>; TikTok lấy thêm từ tiktok-smile.json).
Logo trả góp: máy nhà tải logo chính thức về PXD_KHO/logo-doi-tac/, kèm doi-tac.json [{"ten","slug","tep"}]. Thiếu thì khối không hiện."""
import html
import json
import os
import re
import shutil

GOC = os.environ.get("PXD_KHO", "").strip()

# biểu tượng theo nhận diện của từng hãng, vẽ lại dạng SVG gọn để trang nhẹ
ICON = {
    "facebook": ('Facebook', '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="12" fill="#1877F2"/>'
                 '<path fill="#fff" d="M15.1 12.6l.4-2.7h-2.6V8.2c0-.8.4-1.5 1.6-1.5h1.2V4.4s-1.1-.2-2.2-.2c-2.2 0-3.6 1.3-3.6 3.7v2H7.6v2.7h2.3V20h3V12.6z"/></svg>'),
    "youtube": ('YouTube', '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="0" y="4" width="24" height="16" rx="5" fill="#FF0000"/>'
                '<path fill="#fff" d="M9.8 8.6v6.8l5.8-3.4z"/></svg>'),
    "instagram": ('Instagram', '<svg viewBox="0 0 24 24" aria-hidden="true"><defs><radialGradient id="igg" cx="30%" cy="107%" r="150%">'
                  '<stop offset="0" stop-color="#fdf497"/><stop offset=".05" stop-color="#fdf497"/><stop offset=".45" stop-color="#fd5949"/>'
                  '<stop offset=".6" stop-color="#d6249f"/><stop offset=".9" stop-color="#285AEB"/></radialGradient></defs>'
                  '<rect width="24" height="24" rx="6.5" fill="url(#igg)"/><rect x="5.2" y="5.2" width="13.6" height="13.6" rx="4" fill="none" stroke="#fff" stroke-width="1.8"/>'
                  '<circle cx="12" cy="12" r="3.3" fill="none" stroke="#fff" stroke-width="1.8"/><circle cx="16.3" cy="7.7" r="1.1" fill="#fff"/></svg>'),
    "tiktok": ('TikTok', '<svg viewBox="0 0 24 24" aria-hidden="true"><rect width="24" height="24" rx="6" fill="#000"/>'
               '<path fill="#25F4EE" d="M10.3 10.3v-.8a5.6 5.6 0 0 0-.8-.1 5.9 5.9 0 0 0-3.4 10.8 5.9 5.9 0 0 1 4.2-9.9z"/>'
               '<path fill="#25F4EE" d="M10.5 18.5a2.7 2.7 0 0 0 2.7-2.6V3.6h2.2a4 4 0 0 1-.1-.8h-3v12.4a2.7 2.7 0 0 1-4 2.3 2.7 2.7 0 0 0 2.2 1z"/>'
               '<path fill="#FE2C55" d="M17.4 7.9V7.1a4.1 4.1 0 0 1-2.2-.7 4.1 4.1 0 0 0 2.2 1.5z"/>'
               '<path fill="#FE2C55" d="M15.2 6.4a4.1 4.1 0 0 1-1-2.7h-.8a4.1 4.1 0 0 0 1.8 2.7zM8 12.6a2.7 2.7 0 0 0-1.2 5.1 2.7 2.7 0 0 1 3-4.3V10.3a5.6 5.6 0 0 0-.8-.1h-.1v2.4a2.7 2.7 0 0 0-.9 0z"/>'
               '<path fill="#fff" d="M17.4 7.9v2.4a7.7 7.7 0 0 1-4.5-1.4v6.4a5.9 5.9 0 0 1-9.3 4.8 5.9 5.9 0 0 0 10.1-4.1V9.6a7.7 7.7 0 0 0 4.5 1.4V8a4.1 4.1 0 0 1-.8-.1zM12.9 15.3V8.9a7.7 7.7 0 0 0 4.5 1.4V7.9a4.1 4.1 0 0 1-2.2-1.5 4.1 4.1 0 0 1-1.8-2.7h-2.2v12.3a2.7 2.7 0 0 1-4.9 1.6 2.7 2.7 0 0 1 3-4.4v-2.4a5.9 5.9 0 0 0-4.2 9.9 5.9 5.9 0 0 0 7.8-5.4z"/></svg>'),
    "zalo": ('Zalo', '<svg viewBox="0 0 24 24" aria-hidden="true"><rect width="24" height="24" rx="6" fill="#0068FF"/>'
             '<path fill="#fff" d="M12 4.6c-4.6 0-8.3 3-8.3 6.8 0 2.1 1.2 4 3 5.3l-.6 2.6 2.9-1.5c.9.3 2 .4 3 .4 4.6 0 8.3-3 8.3-6.8S16.6 4.6 12 4.6z"/>'
             '<text x="12" y="13.6" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="5.4" fill="#0068FF">Zalo</text></svg>'),
}
THU_TU = ["facebook", "zalo", "tiktok", "youtube", "instagram"]


def _json(ten):
    f = os.path.join(GOC, ten) if GOC else ""
    if not (f and os.path.isfile(f)):
        return None
    try:
        return json.load(open(f, encoding="utf-8-sig"))
    except ValueError:
        return None


def icon(k):
    return ICON[k][1]


def links(hot):
    d = _json("mang-xa-hoi.json") or {}
    tt = _json("tiktok-smile.json") or {}
    if not d.get("tiktok") and str(tt.get("link", "")).startswith("https://"):
        d["tiktok"] = tt["link"]
    if not str(d.get("zalo", "")).startswith("https://"):
        d["zalo"] = "https://zalo.me/%s" % hot.replace(".", "")
    return [(k, d[k]) for k in THU_TU if str(d.get(k, "")).startswith("https://")]


def hang(hot, lop=""):
    """Hàng logo mạng xã hội, bấm mở trang của Smile."""
    return '<div class="mxh %s">%s</div>' % (lop, "".join(
        '<a href="%s" target="_blank" rel="noopener nofollow" aria-label="%s Xe Điện Smile" title="%s">%s</a>'
        % (html.escape(u, quote=True), ICON[k][0], ICON[k][0], ICON[k][1]) for k, u in links(hot)))


# ---------- trả góp ----------
def doi_tac():
    ds = _json(os.path.join("logo-doi-tac", "doi-tac.json")) or []
    ra = []
    for x in ds if isinstance(ds, list) else []:
        tep = os.path.basename(str(x.get("tep") or ""))
        if x.get("ten") and tep and os.path.isfile(os.path.join(GOC, "logo-doi-tac", tep)):
            ra.append((x["ten"], tep))
    return ra


# Bài trả góp theo từng công ty tài chính ở /tra-gop/<slug công ty>/ (anh chốt 21/10 15:08: bấm logo là ra bài).
# build.py điền BAI bằng các url bài đang có của web; logo chưa có bài thì để ảnh như cũ.
BAI = set()


def _slug_dt(ten):
    for x in _json(os.path.join("logo-doi-tac", "doi-tac.json")) or []:
        if x.get("ten") == ten and x.get("slug"):
            return x["slug"]
    return re.sub(r"[^a-z0-9]+", "-", ten.lower()).strip("-")


def url_bai_dt(ten):
    return "/tra-gop/%s/" % _slug_dt(ten)


def tra_gop(lop=""):
    ds = doi_tac()
    if not ds:
        return ""
    o = []
    for n, t in ds:
        img = '<img src="/doi-tac/%s" alt="%s" title="Trả góp qua %s" height="32" loading="lazy">' % (html.escape(t, quote=True), html.escape(n, quote=True), html.escape(n, quote=True))
        u = url_bai_dt(n)
        o.append('<a href="%s" title="Trả góp qua %s: cần biết gì">%s</a>' % (u, html.escape(n, quote=True), img) if u in BAI else img)
    return '<div class="tra-gop %s"><b>Trả góp qua</b><div class="tg-logo">%s</div></div>' % (lop, "".join(o))


def chep(base):
    ds = doi_tac()
    if ds:
        os.makedirs(os.path.join(base, "doi-tac"), exist_ok=True)
        for _, t in ds:
            shutil.copy(os.path.join(GOC, "logo-doi-tac", t), os.path.join(base, "doi-tac"))
