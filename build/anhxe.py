# -*- coding: utf-8 -*-
"""Ảnh xe thật lấy từ web/fanpage chính hãng (luồng ảnh xe, 20/10).

Thư mục lấy từ biến môi trường PXD_ANH (vd Y:\\CLAUDE\\Claude outputs\\anh-xe-hang-2026-10-20),
có nguon.csv: hang, mau_trong_gia_smile, tep, url_bai_hoac_trang, url_anh, ngay_tai.
"tep" là đường dẫn tương đối trong thư mục (hoặc chỉ tên tệp, nằm trong thư mục <hang>).
Không có PXD_ANH thì mọi hàm trả rỗng, web dựng như cũ.
"""
import csv, html, os, re, shutil, unicodedata

MOI_MAU = 3  # số ảnh tối đa chép cho mỗi mẫu
GOC = os.environ.get("PXD_ANH", "").strip()
ANH = {}      # tên mẫu (chữ thường) -> [(đường dẫn web, tệp nguồn, hãng)]
_CHEP = []    # (tệp nguồn, đường dẫn web)
WEB = ""      # domain đang dựng (build.py đặt), để chọn ảnh đã đóng khung theo từng web
# Ảnh đóng khung anh chọn 20/10 (.vn SA11 "Sân khấu", .com.vn SB1 "Nền sạch"), vuông 1000x1000, đặt ở
# PXD_ANH/khung/<domain>/<slug tên mẫu>.webp. Có thì dùng thay ảnh gốc cho web đó.


def _slug(s):
    s = unicodedata.normalize("NFD", s.replace("đ", "d").replace("Đ", "D"))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def _nap():
    if not GOC or not os.path.isfile(os.path.join(GOC, "nguon.csv")):
        return
    with open(os.path.join(GOC, "nguon.csv"), encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            mau, hang, tep = (r.get("mau_trong_gia_smile") or "").strip(), (r.get("hang") or "").strip(), (r.get("tep") or "").strip()
            if not (mau and tep):
                continue
            nguon = next((p for p in (os.path.join(GOC, tep), os.path.join(GOC, hang, tep)) if os.path.isfile(p)), None)
            if not nguon or not re.search(r"\.(jpe?g|png|webp)$", nguon, re.I):
                continue
            ds = ANH.setdefault(mau.lower(), [])
            if len(ds) >= MOI_MAU:
                continue
            web = "/anh-xe/%s/%s-%d.webp" % (_slug(hang) or "khac", _slug(mau), len(ds) + 1)
            ds.append((web, nguon, hang))
            _CHEP.append((nguon, web))


_nap()


def _khung(ten):
    if not (GOC and WEB and ten):
        return None
    f = os.path.join(GOC, "khung", WEB, _slug(ten) + ".webp")
    return f if os.path.isfile(f) else None


_CO_KHUNG = {}
SP = {}  # domain -> tên mẫu (chữ thường) có trang riêng /xe/<slug>/ trên web đó (sanpham.py điền)


def co_khung():
    """Web đang dựng đã có thư mục ảnh đóng khung chưa. Có thì chỉ dùng ảnh khung (anh chốt 20/10 19:00: đổi hết sang khung)."""
    if WEB not in _CO_KHUNG:
        tm = os.path.join(GOC, "khung", WEB) if GOC and WEB else ""
        _CO_KHUNG[WEB] = bool(tm and os.path.isdir(tm) and any(f.endswith(".webp") for f in os.listdir(tm)))
    return _CO_KHUNG[WEB]


def anh(ten):
    if _khung(ten):
        return "/anh-xe/khung/%s.webp" % _slug(ten)
    if co_khung():
        return None
    ds = ANH.get((ten or "").strip().lower())
    return ds[0][0] if ds else None


def url_xe(ten):
    return "/xe/%s/" % _slug(ten) if (ten or "").strip().lower() in SP.get(WEB, ()) else None


def nut(m, co_gia):
    """Có giá thì Đặt xe, chưa có giá mới Hỏi giá (anh góp ý 20/10 19:00)."""
    t = html.escape(m["name"], quote=True)
    if co_gia:
        return '<button class="hoi-gia dat-xe" data-chat="Mình muốn đặt xe %s">Đặt xe</button>' % t
    return '<button class="hoi-gia" data-chat="Cho mình hỏi giá %s">Hỏi giá</button>' % t


def chep(base):
    """Chép ảnh vào web: đổi sang WebP rộng tối đa 900px nếu có Pillow, không thì chép nguyên (vẫn phục vụ được)."""
    n = 0
    tm = os.path.join(GOC, "khung", WEB) if GOC and WEB else ""
    if tm and os.path.isdir(tm):
        os.makedirs(os.path.join(base, "anh-xe", "khung"), exist_ok=True)
        for fn in os.listdir(tm):
            if fn.lower().endswith(".webp"):
                shutil.copy(os.path.join(tm, fn), os.path.join(base, "anh-xe", "khung", fn))
                n += 1
    if not _CHEP:
        return n
    try:
        from PIL import Image
    except Exception:
        Image = None
    for nguon, web in _CHEP:
        dich = os.path.join(base, web.lstrip("/"))
        os.makedirs(os.path.dirname(dich), exist_ok=True)
        try:
            if Image:
                im = Image.open(nguon)
                im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
                if im.width > 900:
                    im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
                im.save(dich, "WEBP", quality=78, method=4)
            else:
                shutil.copy(nguon, dich)
            n += 1
        except Exception as e:
            print("  ảnh lỗi", nguon, e)
    return n


def tn(m):
    """Ảnh nhỏ đặt đầu dòng trong bảng giá."""
    a = anh(m.get("name"))
    return '<img class="tn-xe" src="%s" alt="%s" width="56" height="42" loading="lazy">' % (a, html.escape(m["name"])) if a else ""


def luoi(ms, tieu_de="Ảnh xe thật", toi_da=8, gia=None):
    """Lưới thẻ xe có ảnh thật. gia: hàm định dạng giá (truyền vnd từ noidung)."""
    co = [m for m in ms if anh(m.get("name"))][:toi_da]
    if not co:
        return ""
    o = []
    for m in co:
        import noidung
        tt = None if m.get("price") else noidung.GIA_TT.get((m.get("name") or "").strip().lower())
        g = (gia(m["price"]) if gia and m.get("price") else (gia(tt) + " (giá thị trường)") if gia and tt else "Liên hệ")
        u = url_xe(m["name"])
        img = '<img src="%s" alt="%s" width="300" height="225" loading="lazy">' % (anh(m["name"]), html.escape(m["name"]))
        ten = '<b>%s</b>' % html.escape(m["name"])
        if u:
            img, ten = '<a href="%s">%s</a>' % (u, img), '<a class="ten-xe" href="%s">%s</a>' % (u, ten)
        o.append('<div class="o-xe hd-in">%s<div class="nd">%s<span class="gia%s">%s</span>%s</div></div>'
                 % (img, ten, "" if (m.get("price") or tt) else " lh", g, nut(m, bool(m.get("price") or tt))))
    return '<section><div class="tieude"><h2>%s</h2></div><div class="luoi-xe">%s</div><p class="chu-anh">Màu xe thực tế có thể khác ảnh.</p></section>' % (tieu_de, "".join(o))


def lien_quan(text, models, toi_da=4):
    """Chọn mẫu có ảnh mà tên hoặc hãng xuất hiện trong bài."""
    t = (text or "").lower()
    co = [m for m in models if anh(m.get("name"))]
    theo_ten = [m for m in co if m["name"].lower() in t]
    theo_hang = [m for m in co if m not in theo_ten and (m.get("brand") or "").lower() and re.search(r"\b%s\b" % re.escape(m["brand"].lower()), t)]
    return (theo_ten + theo_hang)[:toi_da]
