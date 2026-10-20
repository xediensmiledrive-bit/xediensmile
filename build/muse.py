# -*- coding: utf-8 -*-
"""Đọc bài Muse đã ĐẠT soát (_kho/dat/NNN-slug/) và ráp vào 2 web.

Gốc kho lấy từ biến môi trường PXD_KHO (vd Y:\\CLAUDE\\SEO-web). Không có thì bỏ qua.
Mỗi thư mục bài: bai.html (đoạn <article class="bai"> Khung A), meta.json, có thể có <slug>.webp.
"""
import json, os, re, shutil

THU_MUC = {"phoxedien.vn": "phoxedien-vn", "phoxedien.com.vn": "phoxedien-com-vn"}

# Chuyên mục khi meta.json không ghi sẵn "url"/"chuyen_muc"
MUC_VN = {"so-sanh": ("So sánh", "/so-sanh/"), "gia-dien": ("Bảng giá xe điện", "/bang-gia-xe-dien/"),
          "gia-50cc": ("Bảng giá xe 50cc", "/bang-gia-xe-50cc/")}
MUC_COMVN = {"cam-nang": ("Cẩm nang", "/cam-nang/"), "hoi-dap": ("Hỏi đáp", "/hoi-dap/")}
PHEU = {"TOFU": "Đầu phễu", "MOFU": "Giữa phễu", "BOFU": "Cuối phễu"}
EMOJI = {"TOFU": "📘", "MOFU": "⚖️", "BOFU": "🏷️"}


def goc():
    g = os.environ.get("PXD_KHO", "").strip()
    return g if g and os.path.isdir(g) else None


def _muc(site, m):
    kw = (m.get("tu_khoa_chinh", "") + " " + m.get("tieu_de", "")).lower()
    if site["domain"] == "phoxedien.vn":
        bang = MUC_VN
        if m.get("chuyen_muc") in bang:
            k = m["chuyen_muc"]
        elif re.search(r"so sánh| hay | vs |nên chọn|khác nhau", kw):
            k = "so-sanh"
        elif "giá" in kw and re.search(r"50cc|xe ga|xe số|cub|wave", kw):
            k = "gia-50cc"
        elif "giá" in kw:
            k = "gia-dien"
        else:
            k = "so-sanh"
    else:
        bang = MUC_COMVN
        if m.get("chuyen_muc") in bang:
            k = m["chuyen_muc"]
        elif re.search(r"có nên|có được|bao nhiêu tuổi|\?|hỏi", kw):
            k = "hoi-dap"
        else:
            k = "cam-nang"
    return bang[k]


def _sach(s, site):
    """Bỏ phần có thể chạy mã, ép số gọi/Zalo về số riêng của web, nút chat mở khung chat của trang."""
    s = re.sub(r"(?is)<(script|style|iframe|object|embed|form)\b.*?</\1\s*>", "", s)
    s = re.sub(r"(?is)<(script|iframe|object|embed|link|meta)\b[^>]*>", "", s)
    s = re.sub(r"(?i)\s+on[a-z]+\s*=\s*(\"[^\"]*\"|'[^']*'|[^\s>]+)", "", s)
    s = re.sub(r"(?i)javascript:", "", s)
    so = site["hot"].replace(".", "")
    s = re.sub(r"tel:\+?[\d.\s]+", "tel:" + so, s)
    s = re.sub(r"https?://zalo\.me/\+?\d+", "https://zalo.me/" + so, s)
    s = re.sub(r'href="#chatbot"', 'href="#chat" data-chat', s)
    s = re.sub(r'<article class="bai"', '<article class="bai bai-muse"', s, count=1)
    return s


def _slug_tac(site, ten):
    for k, v in site["authors"].items():
        if v["name"].strip().lower() == (ten or "").strip().lower():
            return k
    return next(iter(site["authors"]))


def doc_bai(site):
    """Trả về danh sách bài Muse ĐẠT của web, mới nhất trước."""
    g = goc()
    if not g:
        return []
    dat = os.path.join(g, THU_MUC[site["domain"]], "_kho", "dat")
    if not os.path.isdir(dat):
        return []
    ra, da_co = [], {a["url"] for a in site["articles"]}
    for ten in sorted(os.listdir(dat)):
        tm = os.path.join(dat, ten)
        fm, fb = os.path.join(tm, "meta.json"), os.path.join(tm, "bai.html")
        if not (os.path.isfile(fm) and os.path.isfile(fb)):
            continue
        try:
            m = json.load(open(fm, encoding="utf-8"))
            bai = open(fb, encoding="utf-8").read()
        except Exception as e:  # bài hỏng thì bỏ qua, không chặn cả web
            print("  bỏ qua", ten, e)
            continue
        slug = re.sub(r"[^a-z0-9-]", "", (m.get("slug") or ten.split("-", 1)[-1]).lower()) or ten
        cat_name, cat_url = _muc(site, m)
        url = m.get("url") or "%s%s/" % (cat_url, slug)
        if url in da_co:
            continue
        da_co.add(url)
        anh = None
        tep = (m.get("anh_bia") or {}).get("tep") or slug + ".webp"
        if os.path.isfile(os.path.join(tm, tep)) and tep.lower().endswith(".webp"):
            anh = os.path.join(tm, tep)
        h1 = m.get("tieu_de") or slug
        ra.append({
            "muse": True, "muc": "", "funnel": PHEU.get(m.get("tang"), "Đầu phễu"), "url": url, "slug": slug, "author": _slug_tac(site, m.get("tac_gia")),
            "read": m.get("phut_doc") or 5, "emoji": EMOJI.get(m.get("tang"), "📘"),
            "cat_name": cat_name, "cat_url": cat_url, "crumb": h1, "h1": h1,
            "title": m.get("tieu_de_seo") or h1, "desc": m.get("mo_ta_seo") or m.get("tra_loi_nhanh", "")[:155],
            "ngay": m.get("ngay"), "faq": [tuple(x[:2]) for x in m.get("faq") or [] if len(x) >= 2],
            "html": _sach(bai, site), "anh": anh, "anh_alt": (m.get("anh_bia") or {}).get("alt") or h1,
        })
    ra.sort(key=lambda a: a["ngay"] or "", reverse=True)
    return ra


def chep_anh(a, base):
    """Chép ảnh bìa lên /anh/<slug>.webp, trả về đường dẫn web hoặc None."""
    if not a.get("anh"):
        return None
    os.makedirs(os.path.join(base, "anh"), exist_ok=True)
    shutil.copy(a["anh"], os.path.join(base, "anh", a["slug"] + ".webp"))
    return "/anh/%s.webp" % a["slug"]
