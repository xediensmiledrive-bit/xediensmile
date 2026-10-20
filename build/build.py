#!/usr/bin/env python3
"""Dựng 2 web tĩnh Phố Xe Điện: phoxedien.vn và phoxedien.com.vn."""
import json, os, shutil, sys, html

OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
NGAY = "2026-10-20"
NGAY_VN = "20/10/2026"
THANG = "10/2026"
HOTLINE = "0888.266.233"
TEL = "0888266233"

sys.path.insert(0, HERE)
from noidung import SITES, keu  # noqa: E402
import noidung  # noqa: E402
import hang  # noqa: E402

# phoxedien.vn: trang theo hãng + schema cho trang loại (tối ưu SEO 20/10)
_vn = noidung.VN
for _k in hang.LOAI:
    noidung.CHIP_HANG[_k] = hang.chip_hang(_k)
for _p in _vn["pages"]:
    _f = _p.get("body")
    if getattr(_f, "faqs", None):
        _k = {"/xe-may-dien/": "may", "/xe-dap-dien/": "dap", "/xe-dien-3-banh/": "ba"}.get(_p["url"])
        _p["schemas"] = [noidung.faq_ld_local(_f.faqs)] + (hang.schema_trang_loai(_k) if _k else [])
        _p.setdefault("crumbs", [("Trang chủ", "/"), (_p["title"].split(":")[0], _p["url"])])
_vn["pages"][-1:-1] = hang.them_trang_hang(_vn)

FONT = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@700;800&family=Be+Vietnam+Pro:wght@400;600;700&display=swap" rel="stylesheet">')


HTACCESS = """ErrorDocument 404 /404.html
Options -Indexes
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]
RewriteRule ^ https://%1%{REQUEST_URI} [R=301,L]
</IfModule>
<IfModule mod_deflate.c>
AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml application/xml text/plain
</IfModule>
<IfModule mod_headers.c>
<FilesMatch "\\.(css|js|svg)$">
Header set Cache-Control "public, max-age=604800"
</FilesMatch>
Header always set X-Content-Type-Options "nosniff"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>
"""


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>'


def crumbs_ld(site, crumbs):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n,
                                 "item": "https://%s%s" % (site["domain"], u)} for i, (n, u) in enumerate(crumbs)]}


def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faqs]}


def strip(s):
    import re
    return re.sub(r"<[^>]+>", "", s)


def faq_html(faqs):
    return '<div class="hd">' + "".join(
        '<details><summary>%s</summary><p>%s</p></details>' % (q, a) for q, a in faqs) + '</div>'


def stores_html(site):
    st = site.get("stores") or []
    if not st:
        return ""
    li = "".join('<li><b>%s</b>%s%s</li>' % (html.escape(x.get("name", "")), html.escape(x.get("address", "")),
                 (' · <a href="%s" target="_blank" rel="noopener nofollow">Chỉ đường</a>' % x["map"]) if x.get("map") else "") for x in st)
    return '<div class="cua-hang"><b>Cửa hàng Smile Motor · mở cửa 8h–21h</b><ul>%s</ul></div>' % li


def page(site, path, title, desc, body, schemas=(), crumbs=None, robots="index,follow"):
    d = site["domain"]
    css_vars = ";".join("--%s:%s" % kv for kv in site["vars"].items())
    menu = "".join('<a href="%s">%s</a>' % (u, n) for n, u in site["menu"])
    sch = "".join(ld(s) for s in schemas)
    if crumbs:
        sch += ld(crumbs_ld(site, crumbs))
    org = {"@context": "https://schema.org", "@type": "Organization", "name": "Phố Xe Điện (%s)" % d,
           "url": "https://%s/" % d, "logo": "https://%s/logo.svg" % d}
    if path == "/":
        sch += ld(org) + ld({"@context": "https://schema.org", "@type": "WebSite", "name": site["sitename"],
                             "url": "https://%s/" % d, "inLanguage": "vi"})
    skin = site.get("skin")
    skin_head = ('<link href="https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">'
                 '<link rel="stylesheet" href="/skin-%s.css?v=1">' % skin) if skin else ""
    ten = site.get("logo_ten", "PHỐ <i>XE ĐIỆN</i>")
    goi_dau = ('<a class="nut-goi" href="tel:%s" aria-label="Gọi %s"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg></a>' % (TEL, HOTLINE)) if skin else ""
    if skin:
        day = f'''<div class="day dock">
<button class="hoi" data-chat><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>Hỏi</button>
<a class="zalo" href="https://zalo.me/{TEL}" target="_blank" rel="noopener nofollow"><span class="zl">Z</span>Zalo</a>
<a class="goi" href="tel:{TEL}">Gọi tư vấn<small>{HOTLINE} · 8h–21h</small></a>
</div>'''
    else:
        day = f'''<div class="day">
<a class="goi" href="tel:{TEL}"><i></i>Gọi tư vấn</a>
<a class="zalo" href="https://zalo.me/{TEL}" target="_blank" rel="noopener nofollow">Zalo</a>
<button class="xem" data-chat>Chat tư vấn</button>
</div>'''
    return f'''<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="https://{d}{path}">
<meta name="theme-color" content="{site['theme']}">
<meta property="og:type" content="{'website' if path == '/' else 'article'}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="https://{d}{path}">
<meta property="og:locale" content="vi_VN">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{FONT}
<link rel="stylesheet" href="/site.css?v=1">
{skin_head}
<style>:root{{{css_vars}}}</style>
{sch}
</head>
<body{' class="skin-%s"' % skin if skin else ""}>
<header class="top"><div class="wrap wide">
<a class="logo" href="/" aria-label="{site['sitename']} - trang chủ">{site['icon']}<span><b>{ten}</b><small>{site['tagline']}</small></span></a>
<span class="dau-phai">{goi_dau}<button class="nut-menu" aria-label="Mở menu" aria-expanded="false"><span></span></button></span>
</div></header>
<nav class="ngan-menu" aria-label="Menu">{menu}<div class="nho">Gọi tư vấn: <a href="tel:{TEL}" style="display:inline;padding:0;border:0;color:inherit">{HOTLINE}</a></div></nav>
<main>
{body}
</main>
<footer><div class="wrap wide">
<a class="logo" href="/">{site['icon']}<span><b>{ten}</b><small>{site['tagline']}</small></span></a>
<p>{site['footer']}</p>
<p>Trang cẩm nang do Smile Motor biên soạn. Giá trên trang là giá tham khảo, có ghi ngày cập nhật. Khi mua xe, người bán là Smile Motor. Hotline {HOTLINE}.</p>
{stores_html(site)}
<nav>{"".join('<a href="%s">%s</a>' % (u, n) for n, u in site['foot'])}</nav>
</div></footer>
{day}
<div class="chat" role="dialog" aria-label="Chat tư vấn" aria-hidden="true">
<div class="chat-dau"><span class="chat-av">{site['bot'][0]}</span><div><b>{site['bot']}</b><small><i></i>Tư vấn Xe điện Smile · {site['hot']}</small></div><button class="chat-dong" aria-label="Đóng">×</button></div>
<div class="chat-than" aria-live="polite"></div>
<div class="chat-goi"></div>
<form class="chat-o"><input type="text" placeholder="Nhắn câu hỏi hoặc số điện thoại..." aria-label="Câu hỏi" maxlength="300"><button aria-label="Gửi">➤</button></form>
</div>
<script>window.PXD={{stores:{json.dumps([x.get('name','')+': '+x.get('address','') for x in site.get('stores') or []], ensure_ascii=False)},tel:"{TEL}",hot:"{HOTLINE}",web:"{site['chat']}",bot:"{site['bot']}"}}</script>
<script src="/site.js?v=1" defer></script>
</body>
</html>
'''


def write(site, path, content):
    # Mỗi web một hotline riêng (anh chốt 20/10): thay số mặc định trong mẫu bằng số của web
    content = content.replace("0888.266.233", site["hot"]).replace("0888266233", site["hot"].replace(".", ""))
    if site.get("brand"):  # phoxedien.vn đổi tên thành "Phố Xe Điện Smile" (anh chốt 20/10)
        content = content.replace("Phố Xe Điện", site["brand"])
    base = os.path.join(OUT, site["domain"])
    f = os.path.join(base, path.strip("/"), "index.html") if path.endswith("/") else os.path.join(base, path.lstrip("/"))
    os.makedirs(os.path.dirname(f), exist_ok=True)
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(content)


def article_page(site, a):
    au = site["authors"][a["author"]]
    toc = "".join('<a href="#m%d">%d. %s</a>' % (i + 1, i + 1, h) for i, h in enumerate(a["toc"]))
    crumbs = [("Trang chủ", "/"), (a["cat_name"], a["cat_url"]), (a["h1"], a["url"])]
    sch = [{"@context": "https://schema.org", "@type": "Article", "headline": a["h1"], "description": a["desc"],
            "datePublished": NGAY, "dateModified": NGAY, "inLanguage": "vi",
            "author": {"@type": "Person", "name": au["name"], "url": "https://%s/tac-gia/%s/" % (site["domain"], a["author"])},
            "publisher": {"@type": "Organization", "name": "Phố Xe Điện", "logo": {"@type": "ImageObject", "url": "https://%s/logo.svg" % site["domain"]}},
            "mainEntityOfPage": "https://%s%s" % (site["domain"], a["url"])},
           faq_ld(a["faq"])]
    rel = "".join(f'<a class="bai-nho" href="{r["url"]}"><div class="o">{r["emoji"]}</div><div><div class="muc">{r["cat_name"]}</div><h3>{r["h1"]}</h3><div class="meta">{r["read"]} phút đọc</div></div></a>'
                  for r in site["articles"] if r["url"] != a["url"])[:4000]
    body = f'''<div class="wrap">
<div class="duong"><a href="/">Trang chủ</a> › <a href="{a['cat_url']}">{a['cat_name']}</a> › <b>{a['crumb']}</b></div>
<article>
<div class="dau-trang"><h1>{a['h1']}</h1>
<div class="tac"><span class="av">{au['name'][0]}</span><span><a href="/tac-gia/{a['author']}/">{au['name']}</a> · cập nhật {NGAY_VN} · {a['read']} phút đọc</span></div></div>
<div class="nhanh hd-in"><b>{a.get('quick_title', 'Trả lời nhanh')}</b><ul>{''.join('<li>%s</li>' % x for x in a['quick'])}</ul></div>
<div class="muc-luc"><b>Trong bài</b>{toc}<a href="#hoi-dap">{len(a['toc']) + 1}. Hỏi đáp nhanh</a></div>
<div class="noi-dung">{a['body']}</div>
<section id="hoi-dap" class="hd-in"><div class="tieude"><h2>Hỏi đáp nhanh</h2></div>{faq_html(a['faq'])}</section>
<p class="ky">Bài viết được viết bởi <a href="/tac-gia/{a['author']}/">{au['name']}</a>, Phố Xe Điện.</p>
</article>
{keu(site['cta_title'], site['cta_text'])}
<section class="hd-in"><div class="tieude"><h2>Bài liên quan</h2></div>{rel}</section>
</div>'''
    return page(site, a["url"], a["title"], a["desc"], body, sch, crumbs)


def author_page(site, slug):
    au = site["authors"][slug]
    lst = "".join(f'<a class="bai-nho" href="{r["url"]}"><div class="o">{r["emoji"]}</div><div><div class="muc">{r["cat_name"]}</div><h3>{r["h1"]}</h3><div class="meta">{r["read"]} phút đọc</div></div></a>'
                  for r in site["articles"] if r["author"] == slug) or '<p class="meta">Bài đầu tiên của %s đang được biên soạn.</p>' % au["name"]
    url = "/tac-gia/%s/" % slug
    body = f'''<div class="wrap"><div class="duong"><a href="/">Trang chủ</a> › <b>Tác giả</b></div>
<div class="dau-trang"><h1>{au['name']}</h1></div>
<div class="noi-dung"><p>{au['name']} là bút danh của ban biên tập Phố Xe Điện ({site['domain']}). {au['bio']}</p>
<p class="luu-y">Phố Xe Điện là trang cẩm nang do Smile Motor biên soạn. Giá trong bài là giá tham khảo, có ghi ngày cập nhật.</p></div>
<section><div class="tieude"><h2>Bài của {au['name']}</h2></div>{lst}</section></div>'''
    sch = [{"@context": "https://schema.org", "@type": "ProfilePage", "mainEntity": {"@type": "Person", "name": au["name"], "description": au["bio"]}}]
    return page(site, url, "%s, tác giả Phố Xe Điện" % au["name"], "%s: bút danh của ban biên tập Phố Xe Điện. %s" % (au["name"], au["bio"]), body, sch,
                [("Trang chủ", "/"), (au["name"], url)])


def build(site):
    d = site["domain"]
    base = os.path.join(OUT, d)
    if os.path.exists(base):
        shutil.rmtree(base)
    os.makedirs(base)
    shutil.copy(os.path.join(HERE, "site.css"), base)
    shutil.copy(os.path.join(HERE, "site.js"), base)
    if site.get("skin"):
        shutil.copy(os.path.join(HERE, "skin-%s.css" % site["skin"]), base)
    os.makedirs(os.path.join(base, "api"))
    shutil.copy(os.path.join(HERE, "lien-he.php"), os.path.join(base, "api"))
    open(os.path.join(base, ".htaccess"), "w").write(HTACCESS)
    for fn, svg in (("logo.svg", site["logo_svg"]), ("favicon.svg", site["favicon"])):
        open(os.path.join(base, fn), "w").write(svg)
    urls = []
    for p in site["pages"]:
        write(site, p["url"], page(site, p["url"], p["title"], p["desc"], p["body"](site), p.get("schemas", []), p.get("crumbs"), p.get("robots", "index,follow")))
        if p.get("robots", "index,follow").startswith("index"):
            urls.append(p["url"])
    for a in site["articles"]:
        write(site, a["url"], article_page(site, a))
        urls.append(a["url"])
    for slug in site["authors"]:
        write(site, "/tac-gia/%s/" % slug, author_page(site, slug))
        urls.append("/tac-gia/%s/" % slug)
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        "<url><loc>https://%s%s</loc><lastmod>%s</lastmod></url>\n" % (d, u, NGAY) for u in urls) + "</urlset>\n"
    open(os.path.join(base, "sitemap.xml"), "w").write(sm)
    open(os.path.join(base, "robots.txt"), "w").write("User-agent: *\nAllow: /\n\nSitemap: https://%s/sitemap.xml\n" % d)
    print(d, len(urls), "trang")


for s in SITES:
    build(s)
