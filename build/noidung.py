# -*- coding: utf-8 -*-
# LUẬT CỨNG anh chốt 20/10 11:19: nút bấm .vn đa phần màu cam (#f26b1d), .com.vn xanh lá non sáng (#6fd92e). Không đổi lẫn.
"""Nội dung 2 web Phố Xe Điện. Giá đọc từ gia-smile.json nếu có; chưa có thì ghi "Liên hệ"."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
NGAY_VN = "20/10/2026"
THANG = "10/2026"

import anhxe  # noqa: E402  ảnh xe thật (PXD_ANH)

# ---------- Giá ----------
GIA_FILE = os.path.join(HERE, "gia-smile.json")
MODELS, STORES = [], []
if os.path.exists(GIA_FILE):
    raw = json.load(open(GIA_FILE, encoding="utf-8"))
    MODELS = raw["models"] if isinstance(raw, dict) else raw
    STORES = raw.get("stores", []) if isinstance(raw, dict) else []

# Nhóm xe dùng chung cho bảng giá: khoá -> (tên hiển thị, các "type" trong file giá)
NHOM = {
    "dap": ("Xe đạp điện", ["xe đạp điện"]),
    "may": ("Xe máy điện", ["xe máy điện"]),
    "ba": ("Xe điện 3 bánh", ["3 bánh"]),
    "ga": ("Xe ga 50cc", ["xe ga 50cc"]),
    "so": ("Xe số 50cc", ["xe số 50cc", "wave", "cub"]),
    "wave": ("Xe wave 50cc", ["wave"]),
}
# Hàng mẫu khi chưa có file giá: hãng đang được tìm nhiều (khung từ khoá 20/10)
CHO = {
    "dap": ["Osakar", "Detech", "Pega HKbike", "DK Bike", "Yadea", "Asama"],
    "may": ["VinFast", "Yadea", "DK Bike", "Osakar", "Kazuki", "Detech"],
    "ba": ["Xe ba bánh điện", "Xe lăn điện"],
    "ga": ["Victoria", "Detech", "DK Bike", "Osakar", "Nioshima"],
    "so": ["Wave 50cc Detech", "Wave 50cc Victoria", "Cub 50cc", "Kaiser W2 50cc", "Daelim"],
    "wave": ["Wave 50cc Detech", "Wave 50cc Victoria", "Wave 50cc Daelim"],
}


def vnd(n):
    return "{:,}".format(int(n)).replace(",", ".") + "đ"


# Smile bán xe số 50cc dáng wave nhưng file giá ghi "Xe Số 50cc" (luồng giá trang trống, 20/10): ghép theo tên mẫu
WAVE_TEN = ["espero classic vvip ii", "espero 50c2a-2", "espero plus 2", "espero 50c3he",
            "kaiser w2", "kaiser m2", "kaiser d2", "daelim si7"]


def models_of(k):
    types = NHOM[k][1]
    if k == "wave":
        return [m for m in MODELS if (m.get("type") or "").lower() == "wave"
                or ((m.get("type") or "").lower() in NHOM["so"][1] and any(t in (m.get("name") or "").lower() for t in WAVE_TEN))]
    return [m for m in MODELS if (m.get("type") or "").lower() in types]


NGUNG_BAN = {"dap", "ba"}
# Smile không bán xe đạp điện, 3 bánh; anh cho dùng giá tham khảo thị trường để kéo traffic (20/10). Không ghi là giá Smile.
THI_TRUONG = {}
_ftt = os.path.join(HERE, "gia-thi-truong.csv")
if os.path.exists(_ftt):
    import csv
    for _r in csv.DictReader(open(_ftt, encoding="utf-8-sig")):
        _k = {"xe-dap-dien": "dap", "xe-ba-banh": "ba"}.get(_r.get("loai"))
        if _k and (_r.get("gia_tham_khao_vnd") or "").strip().isdigit():
            THI_TRUONG.setdefault(_k, []).append({"name": _r["mau"], "brand": _r["hang"], "price": int(_r["gia_tham_khao_vnd"]), "thi_truong": True})
CHU_TT = "Giá tham khảo thị trường cập nhật %s, tổng hợp từ giá hãng công bố và giá đại lý, có thể khác theo nơi bán. Đây không phải giá bán của Smile Motor." % THANG


def rows(k, limit=None):
    ms = models_of(k)
    out = []
    if ms:
        ms = sorted(ms, key=lambda m: (m.get("price") is None, m.get("price") or 0))
        for m in ms[:limit]:
            spec = " · ".join(x for x in [m.get("brand"), m.get("range"), m.get("speed")] if x)
            g = '<span class="gia">%s</span>' % vnd(m["price"]) if m.get("price") else '<span class="gia lh">Liên hệ</span>'
            out.append('<div class="dong" data-n="%s">%s<div class="ten">%s<small>%s</small></div>%s</div>' % (k, anhxe.tn(m), m["name"], spec or NHOM[k][0], g))
    elif k in NGUNG_BAN:
        # Smile ngừng bán từ 25/9/2026: chỉ hiện giá thị trường (nếu có), không liệt kê hàng chờ giá
        for m in sorted(THI_TRUONG.get(k, []), key=lambda m: m["price"])[:limit]:
            out.append('<div class="dong" data-n="%s">%s<div class="ten">%s<small>%s · giá thị trường</small></div><span class="gia">%s</span></div>' % (
                k, anhxe.tn(m), m["name"], m["brand"], vnd(m["price"])))
    else:
        for b in CHO[k][:limit]:
            ten = b if k in ("ba", "so", "wave") else "%s %s" % (NHOM[k][0], b)
            out.append('<div class="dong" data-n="%s"><div class="ten">%s<small>Đang cập nhật giá tháng %s</small></div><span class="gia lh">Liên hệ</span></div>' % (k, ten, THANG))
    return "".join(out)


def gia_tu(k):
    ps = [m["price"] for m in models_of(k) if m.get("price")]
    return ("từ " + vnd(min(ps))) if ps else "Liên hệ"


def bang(keys, bid, limit=None, loc=True):
    keys = [k for k in keys if rows(k, 1)] or keys[:0]
    if not keys:
        return ""
    chips = ""
    if loc and len(keys) > 1:
        chips = '<div class="chips" style="padding:0 0 12px" data-loc="%s"><span class="chip on" data-k="all">Tất cả</span>%s</div>' % (
            bid, "".join('<span class="chip" data-k="%s">%s</span>' % (k, NHOM[k][0]) for k in keys))
    body = "".join('<div class="dong dau" data-n="%s"><span>%s</span><span>Giá tham khảo</span></div>%s' % (k, NHOM[k][0], rows(k, limit)) for k in keys)
    tt = any(k in NGUNG_BAN and not models_of(k) and THI_TRUONG.get(k) for k in keys)
    them = (' <b>Xe đạp điện, xe 3 bánh:</b> ' + CHU_TT) if tt else ""
    if tt and all(k in NGUNG_BAN and not models_of(k) for k in keys):
        return chips + '<div class="the bang hd-in" id="%s">%s<div class="chu-thich">%s</div></div>' % (bid, body, CHU_TT)
    return chips + '<div class="the bang hd-in" id="%s">%s<div class="chu-thich">Giá tham khảo cập nhật %s, giá bán tại Smile Motor, chưa gồm lệ phí trước bạ, biển số và bảo hiểm. Bấm Chat hoặc Gọi để có giá chính xác hôm nay.%s</div></div>' % (bid, body, NGAY_VN, them)


def tom_gia(keys):
    return "".join('<div class="dong"><div class="ten">%s<small>cập nhật %s</small></div><span class="gia%s">%s</span></div>' % (
        NHOM[k][0], NGAY_VN, "" if models_of(k) else " lh", gia_tu(k)) for k in keys)


# ---------- Hình minh hoạ (vẽ tay, không phải ảnh xe thật) ----------
def xe_svg(c1="#fff", c2="#ffb27d", nen="none"):
    return f'''<svg viewBox="0 0 320 180" aria-hidden="true"><ellipse cx="160" cy="166" rx="130" ry="7" fill="#000" opacity=".12"/>
<circle cx="72" cy="136" r="30" fill="none" stroke="{c1}" stroke-width="10"/><circle cx="72" cy="136" r="8" fill="{c1}"/>
<circle cx="250" cy="136" r="30" fill="none" stroke="{c1}" stroke-width="10"/><circle cx="250" cy="136" r="8" fill="{c1}"/>
<path d="M72 136 L120 136 Q140 100 190 100 L232 100 L250 136" fill="none" stroke="{c1}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M104 104 Q110 76 150 76 L196 76 Q214 76 214 92 L214 100 L120 104 Z" fill="{c2}"/>
<path d="M232 100 L218 40 M206 40 L236 40" stroke="{c1}" stroke-width="9" stroke-linecap="round"/>
<rect x="128" y="66" width="62" height="12" rx="6" fill="{c1}"/><circle cx="240" cy="62" r="7" fill="#ffd84d"/></svg>'''


def dap_svg(c1="#fff", c2="#ffb27d"):
    return f'''<svg viewBox="0 0 320 180" aria-hidden="true"><ellipse cx="160" cy="166" rx="130" ry="7" fill="#000" opacity=".12"/>
<circle cx="78" cy="128" r="36" fill="none" stroke="{c1}" stroke-width="8"/><circle cx="244" cy="128" r="36" fill="none" stroke="{c1}" stroke-width="8"/>
<path d="M78 128 L130 70 L206 70 L244 128 M130 70 L160 128 L206 70 M160 128 L78 128" fill="none" stroke="{c1}" stroke-width="8" stroke-linejoin="round"/>
<path d="M120 58 L148 58" stroke="{c1}" stroke-width="9" stroke-linecap="round"/><path d="M206 70 L196 36 L222 36" fill="none" stroke="{c1}" stroke-width="8" stroke-linecap="round"/>
<rect x="138" y="82" width="52" height="22" rx="7" fill="{c2}"/></svg>'''


# ---------- Logo ----------
ICON_VN = '''<svg viewBox="0 0 64 56" aria-hidden="true"><path d="M8 4h48l6 18H2z" fill="#f26b1d"/><path d="M20 4l-4 18M32 4v18M44 4l4 18" stroke="#fff" stroke-width="4"/>
<path d="M2 22q7.5 8 15 0q7.5 8 15 0q7.5 8 15 0q7.5 8 15 0" fill="#f26b1d"/><rect x="7" y="30" width="50" height="26" fill="#3aa52a"/><rect x="25" y="36" width="14" height="20" rx="1.5" fill="#fff"/></svg>'''
ICON_COMVN = '''<svg viewBox="0 0 64 56" aria-hidden="true"><rect x="29" y="2" width="6" height="54" rx="3" fill="#4a5258"/><path d="M8 8h40l10 9-10 9H8z" fill="#3aa52a"/>
<path d="M56 30H16L6 39l10 9h40z" fill="#9aa5ad"/></svg>'''


def logo_svg(icon, tag, c1, c2):
    inner = icon.replace('<svg viewBox="0 0 64 56" aria-hidden="true">', '<g>').replace('</svg>', '</g>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 80"><g transform="translate(4 12)">{inner}</g>
<text x="80" y="46" font-family="Baloo 2,Be Vietnam Pro,Arial,sans-serif" font-weight="800" font-size="40"><tspan fill="{c1}">PHỐ </tspan><tspan fill="{c2}">XE ĐIỆN</tspan></text>
<text x="82" y="70" font-family="Be Vietnam Pro,Arial,sans-serif" font-weight="700" font-size="14" letter-spacing="3" fill="#6b757c">{tag}</text></svg>'''


def fav(icon):
    return icon.replace('<svg viewBox="0 0 64 56" aria-hidden="true">', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2 -6 68 68">')


# ---------- Mảnh dùng chung ----------
def keu(title, text):
    return f'''<section class="hd-in"><div class="keu"><h2>{title}</h2><p>{text}</p>
<div class="hang-nut"><button class="btn btn-trang" data-chat>Chat tư vấn</button><a class="btn btn-phu" href="tel:0888266233">Gọi 0888.266.233</a></div></div></section>'''


def list_bai(arts, big_first=True, ico=None):
    out = []
    for i, a in enumerate(arts):
        if i == 0 and big_first:
            out.append(f'<a class="the bai-to hd-in" href="{a["url"]}" style="display:block;margin-bottom:6px"><div class="anh">{ico or ""}</div><div class="nd"><div class="muc">{a["cat_name"]}</div><h3>{a["h1"]}</h3><div class="meta">{a["read"]} phút đọc · cập nhật {NGAY_VN}</div></div></a>')
        else:
            out.append(f'<a class="bai-nho hd-in" href="{a["url"]}"><div class="o">{a["emoji"]}</div><div><div class="muc">{a["cat_name"]}</div><h3>{a["h1"]}</h3><div class="meta">{a["read"]} phút đọc</div></div></a>')
    return "".join(out)


def the_xe(items):
    return '<div class="luot">' + "".join(
        f'<a class="the the-xe hd-in" href="{u}"><div class="anh">{svg}</div><div class="nd"><h3>{t}</h3><p>{s}</p><div class="gia">{g}</div></div></a>'
        for t, s, g, u, svg in items) + '</div>'


def chon(opts):
    return '<div class="chon hd-in"><h2>Chọn xe giúp tôi</h2><p>Bạn dùng xe vào việc gì? Chạm một ô để xem gợi ý.</p><div class="lua">' + "".join(
        '<button data-g="%s">%s</button>' % (g.replace('"', '&quot;'), t) for t, g in opts) + '</div><div class="goi-y" aria-live="polite"></div></div>'


from baiviet import BAI_VN, BAI_COMVN  # noqa: E402

# =====================================================================
# phoxedien.vn: Bảng giá và so sánh
# =====================================================================
VN = {
    "domain": "phoxedien.vn", "sitename": "Phố Xe Điện: bảng giá và so sánh xe điện, xe 50cc",
    "brand": "Phố Xe Điện Smile", "logo_ten": "PHỐ <i>XE ĐIỆN</i> SMILE",
    "tagline": "Cẩm nang xe điện", "theme": "#3aa52a",
    "icon": ICON_VN, "logo_svg": logo_svg(ICON_VN, "CẨM NANG XE ĐIỆN", "#3aa52a", "#f26b1d"), "favicon": fav(ICON_VN),
    "vars": {"c1": "#3aa52a", "c2": "#f26b1d", "c2d": "#c24d0a", "chu": "#1f2a30", "phu": "#5f6b73", "vien": "#e4ebe6",
             "nen": "#f5fdee", "nen2": "#fff6ef", "hero": "linear-gradient(140deg,#3aa52a 0%,#2b8f1e 55%,#2f3a40 100%)",
             "nhan-hero": "#ffb27d", "btn": "#f26b1d", "bong": "rgba(242,107,29,.35)",
             "keu": "linear-gradient(135deg,#f26b1d,#c94d0b)", "chan": "#2f3a40", "gia": "#d4401a"},
    "menu": [("Bảng giá xe điện", "/bang-gia-xe-dien/"), ("Bảng giá xe 50cc", "/bang-gia-xe-50cc/"), ("Xe máy điện", "/xe-may-dien/"),
             ("Xe đạp điện", "/xe-dap-dien/"), ("Xe ga 50cc", "/xe-ga-50cc/"), ("Xe số 50cc", "/xe-so-50cc/"), ("Xe wave 50cc", "/xe-wave-50cc/"),
             ("Xe điện 3 bánh", "/xe-dien-3-banh/"), ("So sánh và đánh giá", "/so-sanh/"), ("Giới thiệu", "/gioi-thieu/")],
    "foot": [("Bảng giá xe điện", "/bang-gia-xe-dien/"), ("Bảng giá xe 50cc", "/bang-gia-xe-50cc/"), ("So sánh", "/so-sanh/"), ("Giới thiệu", "/gioi-thieu/")],
    "footer": "Phố Xe Điện (phoxedien.vn) gom bảng giá tham khảo theo tháng và so sánh xe điện, xe 50cc để bạn chọn nhanh, đúng túi tiền.",
    "authors": {
        "kha-uyen": {"name": "Khả Uyên", "bio": "Uyên phụ trách bảng giá theo tháng, top xe theo ngân sách, giá lăn bánh và trả góp."},
        "minh-trang": {"name": "Minh Trang", "bio": "Trang phụ trách so sánh và đánh giá xe: đặt các mẫu cạnh nhau theo thông số, nói rõ cả điểm mạnh lẫn điểm yếu."},
        "anh-ngoc": {"name": "Ánh Ngọc", "bio": "Ngọc viết về xe cho nữ, mẫu mới, màu sắc và các dòng xe điện mini."},
    },
    "articles": BAI_VN,
    "chat": "phoxedien.vn", "hot": "0889.277.112", "bot": "Hoàng Vy",
}
VN["cta_title"] = "Cần giá chính xác hôm nay?"
VN["cta_text"] = "Chat hoặc gọi hotline Xe điện Smile 0888.266.233 để biết giá, quà tặng và mẫu còn hàng. Người bán là Smile Motor."
ART_VN = {a["url"]: a for a in BAI_VN}


def vn_home(s):
    so_sanh = BAI_VN[:8]
    return f'''<div class="hero"><span class="cau a"></span><span class="cau b"></span>
<div><span class="nhan">Cập nhật tháng {THANG}</span><h1>Bảng giá xe điện <em>tháng {THANG}</em></h1>
<p>Giá tham khảo mới nhất của xe máy điện, xe đạp điện và xe 50cc, kèm so sánh để chọn đúng xe cho đi học, đi làm.</p></div>
<div class="hinh-hero">{xe_svg()}<span class="sticker">Nói thật!</span></div>
<div class="hang-nut"><a class="btn btn-chinh nhip" href="/bang-gia-xe-dien/">Xem bảng giá</a><button class="btn btn-phu" data-chat>Chọn xe giúp tôi</button></div></div>
<nav class="chips" aria-label="Danh mục"><a class="chip on" href="/bang-gia-xe-dien/">Bảng giá</a><a class="chip" href="/xe-may-dien/">Xe máy điện</a><a class="chip" href="/xe-dap-dien/">Xe đạp điện</a><a class="chip" href="/bang-gia-xe-50cc/">Xe 50cc</a><a class="chip" href="/xe-dien-3-banh/">Xe 3 bánh</a><a class="chip" href="/so-sanh/">So sánh</a></nav>
<div class="wrap">
<section><div class="tieude"><h2>Bảng giá tham khảo</h2><a href="/bang-gia-xe-dien/">Xem đủ ›</a></div>
<div class="the bang hd-in"><div class="dong dau"><span>Nhóm xe</span><span>Giá tham khảo</span></div>{tom_gia(["may", "dap", "ba", "ga", "so"])}</div></section>
<section><div class="tieude"><h2>Xem theo loại xe</h2></div>{the_xe([
        ("Xe máy điện", "Đi học, đi làm trong phố", gia_tu("may"), "/xe-may-dien/", xe_svg("#3aa52a", "#f26b1d")),
        ("Xe đạp điện", "Nhẹ, rẻ, hợp học sinh", gia_tu("dap"), "/xe-dap-dien/", dap_svg("#3aa52a", "#f26b1d")),
        ("Xe ga 50cc", "Tự động, có cốp, từ 16 tuổi", gia_tu("ga"), "/xe-ga-50cc/", xe_svg("#2f3a40", "#f26b1d")),
        ("Xe số 50cc", "Wave, cub, rẻ và bền", gia_tu("so"), "/xe-so-50cc/", xe_svg("#2f3a40", "#ffb27d")),
        ("Xe điện 3 bánh", "Cho người lớn tuổi", gia_tu("ba"), "/xe-dien-3-banh/", xe_svg("#3aa52a", "#ffb27d"))])}</section>
<section>{chon([
        ("Đi học", 'Học sinh từ đủ 16 tuổi đi được xe gắn máy (xe điện đến 4 kW hoặc xe dưới 50cc). Xem <a href="/xe-may-dien/">xe máy điện</a> hoặc <a href="/bang-gia-xe-50cc/">xe 50cc</a>; dưới 16 tuổi chọn <a href="/xe-dap-dien/">xe đạp điện</a>.'),
        ("Đi làm", 'Đi dưới 30 km mỗi ngày: <a href="/xe-may-dien/">xe máy điện</a> tiết kiệm nhất. Đi xa hoặc không có chỗ sạc: cân nhắc <a href="/bang-gia-xe-50cc/">xe 50cc</a>.'),
        ("Chở người lớn tuổi", 'Ông bà khó giữ thăng bằng thì <a href="/xe-dien-3-banh/">xe điện 3 bánh</a> an toàn hơn xe 2 bánh.')])}</section>
<section><div class="tieude"><h2>So sánh và đánh giá</h2><a href="/so-sanh/">Tất cả ›</a></div>{list_bai(so_sanh, ico=xe_svg())}</section>
{keu(VN["cta_title"], VN["cta_text"])}
<section class="hd-in"><div class="tieude"><h2>Hỏi nhanh đáp gọn</h2></div>{faq_vn_home_html}</section>
</div>'''


FAQ_VN_HOME = [
    ("Giá trên Phố Xe Điện có phải giá bán thật không?", "Đây là giá tham khảo lấy từ bảng giá của Smile Motor, có ghi ngày cập nhật. Giá có thể đổi theo chương trình khuyến mãi, nên trước khi mua bạn bấm Chat hoặc gọi 0888.266.233 để biết giá hôm nay."),
    ("Giá lăn bánh khác giá niêm yết thế nào?", 'Giá lăn bánh là giá xe cộng lệ phí trước bạ, lệ phí đăng ký biển số và bảo hiểm trách nhiệm dân sự bắt buộc. Xem cách tính trong bài <a href="/bang-gia/gia-lan-banh-xe-may-dien-xe-50cc/">giá lăn bánh</a>.'),
    ("Mua xe ở đâu sau khi xem giá?", "Phố Xe Điện là trang cẩm nang do Smile Motor biên soạn. Khi bạn muốn mua, Smile Motor là người bán: chat trên trang hoặc gọi, nhắn Zalo 0888.266.233."),
]
faq_vn_home_html = ""


def vn_bang_gia_dien(s):
    return f'''<div class="wrap"><div class="duong"><a href="/">Trang chủ</a> › <b>Bảng giá xe điện</b></div>
<div class="dau-trang"><h1>Bảng giá xe điện tháng {THANG}</h1><div class="tac"><span class="av">K</span><span><a href="/tac-gia/kha-uyen/">Khả Uyên</a> · cập nhật {NGAY_VN}</span></div></div>
<div class="nhanh hd-in"><b>Tóm tắt nhanh</b><ul><li>Xe máy điện: {gia_tu("may")}</li><li>Xe đạp điện: {gia_tu("dap")}</li><li>Xe điện 3 bánh: {gia_tu("ba")}</li><li>Giá tham khảo tại Smile Motor, chưa gồm lệ phí. Hỏi giá hôm nay qua Chat hoặc 0888.266.233.</li></ul></div>
<section style="margin-top:20px">{bang(["may", "dap", "ba"], "bg-dien")}</section>
<section class="noi-dung hd-in"><h2>Đọc bảng giá sao cho đúng</h2>
<p>Giá trong bảng là giá xe, chưa gồm lệ phí trước bạ, lệ phí cấp biển số và bảo hiểm. Xe đạp điện không phải đăng ký biển số; xe máy điện thì phải. Vì vậy hai chiếc cùng giá niêm yết có thể chênh nhau khi lăn bánh. Cách tính chi tiết ở bài <a href="/bang-gia/gia-lan-banh-xe-may-dien-xe-50cc/">giá lăn bánh</a>.</p>
<p>Với xe máy điện, khoản chênh lớn nhất thường nằm ở pin: cùng một dáng xe, bản pin lithium thường đắt hơn bản ắc quy chì nhưng nhẹ hơn và bền hơn. Bài <a href="/so-sanh/pin-lithium-hay-ac-quy-chi/">pin lithium hay ắc quy chì</a> giúp bạn quyết có đáng bỏ thêm tiền không.</p>
<h2>Chọn theo ngân sách</h2>
<ul><li><b>Ngân sách thấp, người đi dưới 16 tuổi:</b> xem <a href="/xe-dap-dien/">xe đạp điện</a>, không cần bằng lái, không cần biển số.</li>
<li><b>Học sinh từ 16 tuổi, người đi làm trong phố:</b> <a href="/xe-may-dien/">xe máy điện</a> loại xe gắn máy (công suất đến 4 kW, tốc độ đến 50 km/h), không cần bằng lái.</li>
<li><b>Người lớn tuổi:</b> <a href="/xe-dien-3-banh/">xe điện 3 bánh</a> vững hơn khi dừng, đỗ.</li></ul></section>
<section class="hd-in"><div class="tieude"><h2>Hỏi về giá</h2></div>{faq_html_local(FAQ_BG_DIEN)}</section>
{keu(VN["cta_title"], VN["cta_text"])}</div>'''


FAQ_BG_DIEN = [
    ("Bảng giá xe điện cập nhật khi nào?", "Phố Xe Điện cập nhật bảng giá mỗi tháng và ghi ngày ở đầu trang. Giá giữa tháng có thể đổi theo khuyến mãi, nên bạn nên hỏi lại qua Chat hoặc hotline 0888.266.233 trước khi mua."),
    ("Xe máy điện có phải đăng ký biển số không?", "Có. Xe máy điện thuộc loại xe gắn máy hoặc xe mô tô điện, đều phải đăng ký và gắn biển số. Xe đạp điện thì không phải đăng ký."),
    ("Mua trả góp xe điện được không?", "Được với nhiều mẫu. Điều kiện và số tiền trả trước tuỳ chương trình của Smile Motor từng tháng; bạn chat hoặc gọi để được tính cụ thể theo mẫu xe."),
]


def faq_html_local(faqs):
    return '<div class="hd">' + "".join('<details><summary>%s</summary><p>%s</p></details>' % (q, a) for q, a in faqs) + '</div>'


def vn_bang_gia_50(s):
    return f'''<div class="wrap"><div class="duong"><a href="/">Trang chủ</a> › <b>Bảng giá xe 50cc</b></div>
<div class="dau-trang"><h1>Bảng giá xe 50cc tháng {THANG}</h1><div class="tac"><span class="av">K</span><span><a href="/tac-gia/kha-uyen/">Khả Uyên</a> · cập nhật {NGAY_VN}</span></div></div>
<div class="nhanh hd-in"><b>Tóm tắt nhanh</b><ul><li>Xe ga 50cc: {gia_tu("ga")}</li><li>Xe số, wave, cub 50cc: {gia_tu("so")}</li><li>Người đủ 16 tuổi đi được xe dưới 50cc, không cần bằng lái.</li></ul></div>
<section style="margin-top:20px">{bang(["ga", "so"], "bg-50")}</section>
<section class="noi-dung hd-in"><h2>Xe ga hay xe số: tiền chênh nằm ở đâu</h2>
<p>Xe ga 50cc thường đắt hơn xe số cùng hãng vì có hộp số tự động, cốp và thân vỏ lớn hơn. Xe số, wave, cub rẻ hơn, nhẹ hơn, phụ tùng dễ tìm. So sánh đủ ưu, nhược ở bài <a href="/so-sanh/xe-ga-50cc-hay-xe-so-50cc/">xe ga 50cc hay xe số 50cc</a>.</p>
<p>Xem riêng từng loại: <a href="/xe-ga-50cc/">xe ga 50cc</a>, <a href="/xe-so-50cc/">xe số 50cc</a>, <a href="/xe-wave-50cc/">xe wave 50cc</a>.</p>
<p>Khi so giá, nhìn thêm 3 thứ: phanh (phanh đĩa trước hay phanh cơ), chiều cao yên so với người đi, và hãng có bảo hành, có phụ tùng gần nhà không.</p></section>
<section class="hd-in"><div class="tieude"><h2>Hỏi về giá xe 50cc</h2></div>{faq_html_local(FAQ_BG_50)}</section>
{keu(VN["cta_title"], VN["cta_text"])}</div>'''


FAQ_BG_50 = [
    ("Xe 50cc bao nhiêu tuổi được đi?", "Theo Luật Trật tự, an toàn giao thông đường bộ 2024 (hiệu lực từ 01/01/2025), người đủ 16 tuổi được điều khiển xe gắn máy, gồm xe dưới 50cc có vận tốc thiết kế đến 50 km/h."),
    ("Xe 50cc có cần bằng lái không?", "Xe gắn máy (dưới 50cc, tốc độ thiết kế đến 50 km/h) không thuộc hạng giấy phép lái xe nào, nên không cần bằng lái. Xe vẫn phải đăng ký, gắn biển số và có bảo hiểm bắt buộc."),
    ("Giá xe 50cc đã gồm biển số chưa?", "Chưa. Giá trong bảng là giá xe. Lệ phí trước bạ, lệ phí biển số và bảo hiểm tính riêng, tuỳ nơi bạn đăng ký."),
]


def vn_cat(slug, h1, desc_p, keys, svg, faqs, extra=""):
    def f(s):
        return f'''<div class="wrap"><div class="duong"><a href="/">Trang chủ</a> › <b>{h1.split(":")[0]}</b></div>
<div class="dau-trang"><h1>{h1}</h1><div class="tac"><span class="av">M</span><span><a href="/tac-gia/minh-trang/">Minh Trang</a> · cập nhật {NGAY_VN}</span></div></div>
<div class="hinh-hero hd-in" style="background:var(--hero);height:170px;border-radius:20px;margin:16px 0">{svg}</div>
<div class="noi-dung">{desc_p}</div>
<section>{bang(keys, "bg-" + slug)}</section>
{CHIP_HANG.get(slug, "")}
{extra}
<section class="hd-in"><div class="tieude"><h2>Hỏi đáp</h2></div>{faq_html_local(faqs)}</section>
{keu(VN["cta_title"], VN["cta_text"])}</div>'''
    f.faqs = faqs
    return f


CHIP_HANG = {}  # khoá loại xe -> khối "Xem theo hãng", build.py điền sau khi dựng trang hãng
VN_MAY = vn_cat("may", "Xe máy điện: giá tham khảo và cách chọn tháng " + THANG,
                '''<p>Xe máy điện chia làm hai nhóm theo luật: <b>xe gắn máy điện</b> (công suất đến 4 kW, tốc độ thiết kế đến 50 km/h) cho người từ đủ 16 tuổi, không cần bằng lái; và <b>xe mô tô điện</b> mạnh hơn, cần bằng A1 và người lái từ đủ 18 tuổi. Trước khi so giá, hãy chắc mẫu bạn chọn thuộc nhóm nào.</p>
<h2>Ba thứ quyết định giá</h2><ul><li><b>Pin:</b> lithium nhẹ, bền hơn nhưng đắt hơn ắc quy chì. Xem <a href="/so-sanh/pin-lithium-hay-ac-quy-chi/">so sánh hai loại pin</a>.</li>
<li><b>Quãng đường mỗi lần sạc:</b> con số hãng công bố đo ở điều kiện chuẩn; đi thực tế với người nặng, đường đông thường thấp hơn.</li>
<li><b>Động cơ và phanh:</b> động cơ khoẻ hơn leo dốc tốt hơn; phanh đĩa trước an toàn hơn khi chở người.</li></ul>''',
                ["may"], xe_svg(), [
                    ("Xe máy điện nào không cần bằng lái?", "Xe gắn máy điện, tức công suất động cơ đến 4 kW và tốc độ thiết kế đến 50 km/h. Mẫu mạnh hơn được xếp là xe mô tô và cần bằng A1."),
                    ("Xe máy điện đi được bao nhiêu km một lần sạc?", "Tuỳ dung lượng pin và cách đi. Hãng thường công bố quãng đường ở điều kiện thử nghiệm; khi đi thực tế, chở nặng, chạy nhanh hoặc trời lạnh thì quãng đường giảm. Hỏi Smile để biết số đo thực tế của từng mẫu."),
                    ("VinFast, Yadea có bán ở Smile không?", "Phố Xe Điện có thông tin giá tham khảo cả các hãng Smile không bán. Nếu hãng bạn hỏi không có tại Smile, nhân viên sẽ gợi ý mẫu tương đương về giá và thông số."),
                ])
VN_DAP = vn_cat("dap", "Xe đạp điện: giá tham khảo và cách chọn tháng " + THANG,
                '''<p>Xe đạp điện có bàn đạp, tốc độ thấp và không phải đăng ký biển số, nên là lựa chọn quen thuộc cho học sinh dưới 16 tuổi. Theo Luật Trật tự, an toàn giao thông đường bộ 2024, xe đạp điện vẫn là xe thô sơ có động cơ điện trợ lực, người đi phải đội mũ bảo hiểm.</p>
<h2>Chọn xe đạp điện cho học sinh</h2><ul><li>Chiều cao yên: ngồi lên, hai mũi chân chạm đất là vừa.</li><li>Cân nặng xe: con tự dắt, tự dựng chân chống được.</li><li>Phanh: bóp thử, xe phải dừng chắc, không kêu rít.</li><li>Pin: hỏi rõ pin lithium hay ắc quy chì, bảo hành bao lâu.</li></ul>''',
                ["dap"], dap_svg(), [
                    ("Xe đạp điện có cần biển số không?", "Không. Xe đạp điện không phải đăng ký, gắn biển số. Người đi vẫn phải đội mũ bảo hiểm và đi đúng làn."),
                    ("Học sinh lớp mấy đi được xe đạp điện?", "Luật không đặt tuổi tối thiểu riêng cho xe đạp điện như xe gắn máy. Phụ huynh nên cho con đi khi con đã đi xe đạp vững và hiểu luật đường phố."),
                    ("Xe đạp điện hay xe máy điện cho con lớp 9?", "Con dưới 16 tuổi thì chọn xe đạp điện, vì xe máy điện loại xe gắn máy chỉ dành cho người từ đủ 16 tuổi."),
                ])
VN_BA = vn_cat("ba", "Xe điện 3 bánh: giá tham khảo tháng " + THANG + " cho người lớn tuổi",
               '''<p>Xe điện 3 bánh đứng vững khi dừng, không cần chống chân, nên hợp với ông bà, người đi chợ gần nhà hoặc người khó giữ thăng bằng. Có hai nhóm chính: xe ba bánh điện (ngồi như xe máy, có giỏ, có cốp) và xe lăn điện.</p>
<h2>Khi chọn xe 3 bánh</h2><ul><li>Cua chậm: xe 3 bánh dễ lật hơn khi cua gấp ở tốc độ cao.</li><li>Có số lùi và phanh tay giữ xe thì dễ dắt, đỗ hơn.</li><li>Đo bề ngang xe so với cửa nhà, hẻm.</li></ul>''',
               ["ba"], xe_svg(), [
                   ("Người lớn tuổi đi xe 3 bánh điện có cần bằng lái không?", "Tuỳ loại xe. Xe lăn điện dành cho người khuyết tật không cần bằng. Xe ba bánh điện có công suất, tốc độ như xe gắn máy thì không cần bằng nhưng phải đăng ký biển số; mẫu mạnh hơn có thể cần bằng. Hỏi Smile loại xe cụ thể trước khi mua."),
                   ("Xe 3 bánh có an toàn hơn xe 2 bánh không?", "Khi dừng và đi chậm thì có, vì xe không đổ. Khi cua nhanh thì xe 3 bánh lại dễ mất lái hơn, nên người lớn tuổi nên đi chậm."),
                   ("Xe 3 bánh có chở được hàng không?", "Nhiều mẫu có giỏ trước và cốp sau, đủ cho đi chợ. Xe chở hàng nặng là dòng riêng, cần hỏi tải trọng khi mua."),
               ])


def vn_so_sanh(s):
    return f'''<div class="wrap"><div class="duong"><a href="/">Trang chủ</a> › <b>So sánh và đánh giá</b></div>
<div class="dau-trang"><h1>So sánh và đánh giá xe điện, xe 50cc</h1></div>
<div class="noi-dung"><p>Đặt các mẫu, các loại xe cạnh nhau theo thông số, chi phí và điểm yếu để bạn biết tiền chênh nằm ở đâu.</p></div>
<section>{list_bai(BAI_VN, ico=xe_svg())}</section>{keu(VN["cta_title"], VN["cta_text"])}</div>'''


def gioi_thieu(site, extra):
    def f(s):
        return f'''<div class="wrap"><div class="duong"><a href="/">Trang chủ</a> › <b>Giới thiệu</b></div>
<div class="dau-trang"><h1>Giới thiệu Phố Xe Điện</h1></div><div class="noi-dung">
<p>{extra}</p>
<p>Trang do Smile Motor biên soạn. Giá trên trang là giá tham khảo theo bảng giá Smile Motor, có ghi ngày cập nhật. Khi bạn mua xe, người bán là Smile Motor; hotline và Zalo: 0888.266.233.</p>
<h2>Cách chúng tôi viết</h2><ul><li>Bài viết mới hoàn toàn, có tên người viết (bút danh của ban biên tập) ở cuối bài.</li><li>Luật và quy định trích từ văn bản đang có hiệu lực, có ghi số hiệu.</li><li>Không bịa con số: giá chưa có thì ghi "liên hệ".</li></ul>
<h2>Người viết</h2><ul>{"".join('<li><a href="/tac-gia/%s/">%s</a>: %s</li>' % (k, v["name"], v["bio"]) for k, v in site["authors"].items())}</ul>
<p class="luu-y">Phố Xe Điện (trang này) không liên quan tới chuỗi cửa hàng hay website nào khác có tên tương tự.</p></div></div>'''
    return f


def notfound(s):
    return '''<div class="wrap" style="text-align:center;padding-top:40px"><div class="dau-trang"><h1>Không tìm thấy trang</h1></div>
<p>Trang bạn tìm không có hoặc đã đổi địa chỉ.</p><p style="margin-top:16px"><a class="btn btn-chinh" href="/">Về trang chủ</a></p></div>'''


VN["pages"] = [
    {"url": "/", "title": "Phố Xe Điện: bảng giá xe điện, xe 50cc tháng %s" % THANG, "desc": "Bảng giá tham khảo xe máy điện, xe đạp điện, xe 50cc cập nhật tháng %s, kèm so sánh để chọn đúng xe. Hỏi giá qua chat hoặc 0888.266.233." % THANG, "body": vn_home},
    {"url": "/bang-gia-xe-dien/", "title": "Bảng giá xe điện tháng %s: xe máy điện, xe đạp điện" % THANG, "desc": "Giá tham khảo xe máy điện, xe đạp điện, xe điện 3 bánh tháng %s, lọc theo loại xe, cập nhật ngày %s." % (THANG, NGAY_VN), "body": vn_bang_gia_dien, "crumbs": [("Trang chủ", "/"), ("Bảng giá xe điện", "/bang-gia-xe-dien/")]},
    {"url": "/bang-gia-xe-50cc/", "title": "Bảng giá xe 50cc tháng %s: xe ga, xe số, wave, cub" % THANG, "desc": "Giá tham khảo xe ga 50cc, xe số 50cc, wave và cub 50cc tháng %s, kèm tuổi được đi và giấy tờ cần có." % THANG, "body": vn_bang_gia_50, "crumbs": [("Trang chủ", "/"), ("Bảng giá xe 50cc", "/bang-gia-xe-50cc/")]},
    {"url": "/xe-may-dien/", "title": "Xe máy điện: giá tham khảo tháng %s và cách chọn" % THANG, "desc": "Giá xe máy điện các hãng tháng %s, cách phân biệt xe gắn máy điện và mô tô điện, chọn pin và quãng đường." % THANG, "body": VN_MAY, "crumbs": [("Trang chủ", "/"), ("Xe máy điện", "/xe-may-dien/")]},
    {"url": "/xe-dap-dien/", "title": "Xe đạp điện: giá tham khảo tháng %s và cách chọn cho học sinh" % THANG, "desc": "Giá xe đạp điện các hãng tháng %s, cách chọn xe cho học sinh dưới 16 tuổi." % THANG, "body": VN_DAP, "crumbs": [("Trang chủ", "/"), ("Xe đạp điện", "/xe-dap-dien/")]},
    {"url": "/xe-dien-3-banh/", "title": "Xe điện 3 bánh cho người lớn tuổi: giá tháng %s và cách chọn" % THANG, "desc": "Giá tham khảo xe ba bánh điện, xe lăn điện và những điều cần xem khi mua cho ông bà.", "body": VN_BA, "crumbs": [("Trang chủ", "/"), ("Xe điện 3 bánh", "/xe-dien-3-banh/")]},
    {"url": "/so-sanh/", "title": "So sánh và đánh giá xe điện, xe 50cc | Phố Xe Điện", "desc": "So sánh pin, loại xe, chi phí và giá lăn bánh xe điện, xe 50cc.", "body": vn_so_sanh, "crumbs": [("Trang chủ", "/"), ("So sánh", "/so-sanh/")]},
    {"url": "/gioi-thieu/", "title": "Giới thiệu Phố Xe Điện (phoxedien.vn)", "desc": "Phố Xe Điện là trang bảng giá và so sánh xe điện, xe 50cc do Smile Motor biên soạn.", "body": None},
    {"url": "/404.html", "title": "Không tìm thấy trang | Phố Xe Điện", "desc": "Trang không tồn tại.", "body": notfound, "robots": "noindex,follow"},
]
VN["pages"][7]["body"] = gioi_thieu(VN, "Phố Xe Điện (phoxedien.vn) là trang bảng giá và so sánh xe điện, xe 50cc. Mỗi tháng chúng tôi cập nhật giá tham khảo, đặt các mẫu xe cạnh nhau theo thông số và chi phí, để bạn chọn nhanh và đúng túi tiền.")
faq_vn_home_html = faq_html_local(FAQ_VN_HOME)
VN["pages"][0]["schemas"] = []

# =====================================================================
# phoxedien.com.vn: Cẩm nang và hỏi đáp
# =====================================================================
COMVN = {
    "domain": "phoxedien.com.vn", "sitename": "Phố Xe Điện: cẩm nang và hỏi đáp xe 50cc, xe điện",
    "tagline": "Cẩm nang xe 50cc và xe điện", "theme": "#0f1112", "skin": "sup", "logo_ten": "Phố Xe Điện",
    "icon": ICON_COMVN, "logo_svg": logo_svg(ICON_COMVN, "CẨM NANG XE 50CC", "#14280f", "#3aa52a"), "favicon": fav(ICON_COMVN),
    # Bảng màu M5 anh chọn 20/10 (thay mint): đầu trang và thanh đáy #0F1112, nền #F3F4F4, nút xanh chanh, giá xanh #2B8F1E
    "vars": {"c1": "#1c2124", "c2": "#3aa52a", "c2d": "#2b8f1e", "chu": "#1c2124", "phu": "#5d666c", "vien": "#dce0e2",
             "nen": "#f3f4f4", "nen2": "#ffffff", "hero": "radial-gradient(120% 90% at 85% 10%,#2c3a2a,#15181a 70%)",
             "nhan-hero": "#a6f07a", "btn": "#6fd92e", "bong": "rgba(15,17,18,.35)",
             "keu": "#15181a", "chan": "#0f1112", "gia": "#2b8f1e"},
    "menu": [("Xe cho học sinh", "/cam-nang/?muc=hoc-sinh"), ("Tuổi, bằng lái, biển số", "/cam-nang/?muc=giay-to"), ("Pin, sạc, sửa xe", "/cam-nang/?muc=sua-xe"),
             ("Xe ga 50cc cho học sinh", "/xe-ga-50cc-cho-hoc-sinh/"), ("Xe số 50cc cho học sinh", "/xe-so-50cc-cho-hoc-sinh/"),
             ("Xe máy điện cho học sinh", "/xe-may-dien-cho-hoc-sinh/"), ("Xe đạp điện cho học sinh", "/xe-dap-dien-cho-hoc-sinh/"),
             ("Tất cả cẩm nang", "/cam-nang/"), ("Hỏi đáp", "/hoi-dap/"), ("Giá xe 50cc", "/gia-xe-50cc/"), ("Giới thiệu", "/gioi-thieu/")],
    "foot": [("Cẩm nang", "/cam-nang/"), ("Hỏi đáp", "/hoi-dap/"), ("Giá xe 50cc", "/gia-xe-50cc/"), ("Giới thiệu", "/gioi-thieu/")],
    "footer": "Phố Xe Điện (phoxedien.com.vn) là cẩm nang và hỏi đáp về xe 50cc, xe điện: chọn xe cho học sinh, tuổi, bằng lái, biển số, pin sạc và bảo dưỡng.",
    "authors": {
        "thu-ha": {"name": "Thu Hà", "bio": "Hà viết cho phụ huynh: chọn xe cho học sinh, an toàn khi đi xe và chi phí nuôi xe."},
        "quoc-bao": {"name": "Quốc Bảo", "bio": "Bảo viết về pin, sạc, ắc quy, bảo dưỡng và cách tự kiểm lỗi thường gặp trước khi mang xe ra tiệm."},
        "bao-chau": {"name": "Bảo Châu", "bio": "Châu viết về luật và thủ tục: tuổi được đi xe, bằng lái, đăng ký biển số, mức phạt và hồ sơ trả góp."},
    },
    "articles": BAI_COMVN,
    "chat": "phoxedien.com.vn", "hot": "0833.666.916", "bot": "Ngọc Anh",
}
COMVN["cta_title"] = "Còn băn khoăn? Hỏi người bán xe"
COMVN["cta_text"] = "Chat hoặc gọi hotline Xe điện Smile 0888.266.233, nhân viên trả lời về giá, giấy tờ và mẫu hợp với con. Người bán là Smile Motor."

FAQ_COMVN = [
    ("Học sinh bao nhiêu tuổi được đi xe 50cc?", "Từ đủ 16 tuổi, theo Luật Trật tự, an toàn giao thông đường bộ 2024 (hiệu lực 01/01/2025). Xe gắn máy gồm xe dưới 50cc và xe điện đến 4 kW, tốc độ thiết kế đến 50 km/h."),
    ("Đi xe 50cc có cần bằng lái không?", "Không. Xe gắn máy không thuộc hạng giấy phép lái xe nào. Người đi vẫn phải mang đăng ký xe, bảo hiểm bắt buộc và giấy tờ tuỳ thân."),
    ("Xe điện hay xe 50cc rẻ hơn khi đi hằng ngày?", "Tiền sạc điện mỗi km thường thấp hơn tiền xăng. Bù lại xe điện có chi phí thay pin sau vài năm. Xem bài chọn xe cho con để tính đủ hai khoản."),
    ("Xe điện không lên nguồn có phải hỏng pin không?", 'Chưa chắc. Nhiều lần chỉ do khoá, cầu chì, giắc nối hoặc công tắc phanh. Xem <a href="/sua-xe/xe-dien-khong-len-nguon/">4 chỗ tự kiểm</a> trước khi gọi thợ.'),
    ("Muốn mua xe thì liên hệ ai?", "Phố Xe Điện là trang cẩm nang do Smile Motor biên soạn. Bấm Chat trên trang hoặc gọi, nhắn Zalo 0888.266.233, người bán là Smile Motor."),
]


def comvn_home(s):
    return f'''<div class="hero"><span class="cau a"></span><span class="cau b"></span>
<div><span class="nhan">Cập nhật tháng {THANG}</span><h1>Xe 50cc cho học sinh: <em>hỏi gì cũng có</em></h1>
<p>Bao nhiêu tuổi được đi, cần giấy tờ gì, xe ga hay xe số, xe điện có hợp không, nuôi xe hết bao nhiêu. Trả lời ngắn, đúng luật đang có hiệu lực.</p></div>
<div class="hinh-hero">{xe_svg("#fff", "#6fd92e")}<span class="sticker">Nói thật!</span></div>
<div class="hang-nut"><a class="btn btn-chinh nhip" href="/cam-nang/">Đọc cẩm nang</a><button class="btn btn-phu" data-chat>Hỏi nhanh</button></div></div>
<nav class="chips" aria-label="Danh mục"><a class="chip on" href="/cam-nang/?muc=hoc-sinh">Xe cho học sinh</a><a class="chip" href="/cam-nang/?muc=giay-to">Tuổi và bằng lái</a><a class="chip" href="/cam-nang/?muc=sua-xe">Pin, sạc, sửa xe</a><a class="chip" href="/gia-xe-50cc/">Giá xe 50cc</a><a class="chip" href="/hoi-dap/">Hỏi đáp</a></nav>
<div class="wrap">
<section><div class="tieude"><h2>Giá tham khảo</h2><a href="/gia-xe-50cc/">Xem đủ ›</a></div>
<div class="the bang hd-in"><div class="dong dau"><span>Nhóm xe</span><span>Giá tham khảo</span></div>{tom_gia(["ga", "so", "may", "dap"])}</div></section>
<section>{chon([
        ("Con 14–15 tuổi", 'Chưa đủ 16 tuổi thì chỉ nên đi xe đạp hoặc <b>xe đạp điện</b>. Đọc <a href="/hoc-sinh/chon-xe-cho-con-hoc-cap-3/">cách chọn xe cho con</a>.'),
        ("Con đủ 16", 'Đi được xe gắn máy: xe dưới 50cc hoặc xe máy điện đến 4 kW, không cần bằng lái. Xem <a href="/giay-to/16-tuoi-di-xe-50cc-can-giay-to-gi/">giấy tờ cần có</a>.'),
        ("Xe đang hỏng", 'Xe điện không lên nguồn? Thử <a href="/sua-xe/xe-dien-khong-len-nguon/">4 bước tự kiểm</a> trước khi gọi thợ.')])}</section>
<section><div class="tieude"><h2>Cẩm nang</h2><a href="/cam-nang/">Tất cả ›</a></div>{list_bai(BAI_COMVN[:8], ico=xe_svg("#fff", "#6fd92e"))}</section>
{keu(COMVN["cta_title"], COMVN["cta_text"])}
<section class="hd-in"><div class="tieude"><h2>Hỏi nhanh đáp gọn</h2><a href="/hoi-dap/">Thêm ›</a></div>{faq_html_local(FAQ_COMVN[:3])}</section>
</div>'''


def comvn_camnang(s):
    cats = [("hoc-sinh", "Xe cho học sinh"), ("giay-to", "Tuổi, bằng lái, biển số"), ("sua-xe", "Pin, sạc, sửa xe")]
    items = "".join(f'<a class="bai-nho hd-in" data-n="{a["muc"]}" href="{a["url"]}"><div class="o">{a["emoji"]}</div><div><div class="muc">{a["cat_name"]}</div><h3>{a["h1"]}</h3><div class="meta">{a["read"]} phút đọc · {a["funnel"]}</div></div></a>' for a in BAI_COMVN)
    return f'''<div class="wrap"><div class="duong"><a href="/">Trang chủ</a> › <b>Cẩm nang</b></div>
<div class="dau-trang"><h1>Cẩm nang xe 50cc, xe điện</h1></div>
<div class="chips" style="padding:6px 0 12px" data-loc="ds-cn"><span class="chip on" data-k="all">Tất cả</span>{"".join('<span class="chip" data-k="%s">%s</span>' % c for c in cats)}</div>
<div id="ds-cn">{items}</div>{keu(COMVN["cta_title"], COMVN["cta_text"])}</div>
<script>(function(){{var m=new URLSearchParams(location.search).get("muc");if(!m)return;addEventListener("DOMContentLoaded",function(){{var c=document.querySelector('[data-loc="ds-cn"] [data-k="'+m+'"]');if(c)c.click()}})}})()</script>'''


def comvn_hoidap(s):
    return f'''<div class="wrap"><div class="duong"><a href="/">Trang chủ</a> › <b>Hỏi đáp</b></div>
<div class="dau-trang"><h1>Hỏi đáp về xe 50cc và xe điện</h1></div>
<div class="noi-dung"><p>Những câu phụ huynh và học sinh hỏi nhiều nhất. Câu nào chưa có, bấm Chat để hỏi trực tiếp.</p></div>
<section class="hd-in">{faq_html_local(FAQ_COMVN)}</section>{keu(COMVN["cta_title"], COMVN["cta_text"])}</div>'''


def comvn_gia(s):
    return f'''<div class="wrap"><div class="duong"><a href="/">Trang chủ</a> › <b>Giá xe 50cc</b></div>
<div class="dau-trang"><h1>Giá xe 50cc và xe điện cho học sinh tháng {THANG}</h1><div class="tac"><span class="av">H</span><span><a href="/tac-gia/thu-ha/">Thu Hà</a> · cập nhật {NGAY_VN}</span></div></div>
<div class="nhanh hd-in"><b>Trước khi xem giá</b><ul><li>Con đủ 16 tuổi: chọn trong xe ga 50cc, xe số 50cc hoặc xe máy điện đến 4 kW.</li><li>Con dưới 16 tuổi: xe đạp điện.</li><li>Ngoài giá xe, tính thêm lệ phí trước bạ, biển số và bảo hiểm.</li></ul></div>
<section style="margin-top:20px">{bang(["ga", "so", "may", "dap"], "bg-hs")}</section>
<section class="noi-dung hd-in"><h2>Mẹ nên nhìn gì ngoài giá</h2><ul><li><b>Chân con chạm đất:</b> con ngồi lên, hai chân chống được là an toàn khi dừng đèn đỏ.</li><li><b>Con dắt được xe:</b> xe nặng quá, con không tự dựng chân chống thì dễ ngã khi dắt.</li><li><b>Chi phí nuôi xe:</b> xăng, dầu nhớt với xe 50cc; tiền điện và thay pin với xe điện.</li></ul>
<p>Xem riêng từng loại: <a href="/xe-ga-50cc-cho-hoc-sinh/">xe ga 50cc</a>, <a href="/xe-so-50cc-cho-hoc-sinh/">xe số 50cc</a>, <a href="/xe-may-dien-cho-hoc-sinh/">xe máy điện</a>, <a href="/xe-dap-dien-cho-hoc-sinh/">xe đạp điện</a> cho học sinh.</p>
<p>Đọc thêm: <a href="/hoc-sinh/chon-xe-cho-con-hoc-cap-3/">chọn xe cho con học cấp 3</a> và <a href="/giay-to/16-tuoi-di-xe-50cc-can-giay-to-gi/">giấy tờ khi con đi xe 50cc</a>.</p></section>
{keu(COMVN["cta_title"], COMVN["cta_text"])}</div>'''


COMVN["pages"] = [
    {"url": "/", "title": "Phố Xe Điện: cẩm nang xe 50cc, xe điện cho học sinh", "desc": "Hỏi đáp xe 50cc và xe điện: tuổi được đi, bằng lái, biển số, chọn xe cho học sinh, pin sạc, bảo dưỡng. Giá tham khảo cập nhật tháng %s." % THANG, "body": comvn_home},
    {"url": "/cam-nang/", "title": "Cẩm nang xe 50cc, xe điện | Phố Xe Điện", "desc": "Cẩm nang chọn xe cho học sinh, luật và giấy tờ, pin sạc và sửa xe.", "body": comvn_camnang, "crumbs": [("Trang chủ", "/"), ("Cẩm nang", "/cam-nang/")]},
    {"url": "/hoi-dap/", "title": "Hỏi đáp xe 50cc và xe điện cho học sinh | Phố Xe Điện", "desc": "Trả lời ngắn các câu hỏi về tuổi đi xe 50cc, bằng lái, biển số, xe điện không lên nguồn.", "body": comvn_hoidap, "schemas": [faq_ld_local(FAQ_COMVN)] if False else [], "crumbs": [("Trang chủ", "/"), ("Hỏi đáp", "/hoi-dap/")]},
    {"url": "/gia-xe-50cc/", "title": "Giá xe 50cc cho học sinh tháng %s: xe ga, xe số, xe điện" % THANG, "desc": "Giá tham khảo xe 50cc và xe điện cho học sinh tháng %s, kèm những điều mẹ nên xem ngoài giá." % THANG, "body": comvn_gia, "crumbs": [("Trang chủ", "/"), ("Giá xe 50cc", "/gia-xe-50cc/")]},
    {"url": "/gioi-thieu/", "title": "Giới thiệu Phố Xe Điện (phoxedien.com.vn)", "desc": "Phố Xe Điện là trang cẩm nang và hỏi đáp xe 50cc, xe điện do Smile Motor biên soạn.", "body": gioi_thieu(COMVN, "Phố Xe Điện (phoxedien.com.vn) là cẩm nang và hỏi đáp về xe 50cc, xe điện cho học sinh và gia đình: tuổi được đi, giấy tờ, chọn xe an toàn, pin sạc và bảo dưỡng."), "crumbs": [("Trang chủ", "/"), ("Giới thiệu", "/gioi-thieu/")]},
    {"url": "/404.html", "title": "Không tìm thấy trang | Phố Xe Điện", "desc": "Trang không tồn tại.", "body": notfound, "robots": "noindex,follow"},
]


def faq_ld_local(faqs):
    import re
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faqs]}


COMVN["pages"][2]["schemas"] = [faq_ld_local(FAQ_COMVN)]
VN["pages"][0]["schemas"] = [faq_ld_local(FAQ_VN_HOME)]
VN["pages"][1]["schemas"] = [faq_ld_local(FAQ_BG_DIEN)]
VN["pages"][2]["schemas"] = [faq_ld_local(FAQ_BG_50)]

# 6 chi nhánh như xediensmile.com (anh chốt 08:53 ngày 20/10), mở cửa 8h–21h
CUA_HANG = [
    {"name": "Smile Hậu Giang", "address": "285 - 285A Hậu Giang, Phường Bình Tây, TP. Hồ Chí Minh"},
    {"name": "Smile Bình Thới 188", "address": "188 Lạc Long Quân, Phường Bình Thới, TP. Hồ Chí Minh"},
    {"name": "Smile Bình Thới 190", "address": "190 Lạc Long Quân, Phường Bình Thới, TP. Hồ Chí Minh"},
    {"name": "Smile Bình Phú", "address": "112 Trần Văn Kiểu, Phường Bình Phú, TP. Hồ Chí Minh"},
    {"name": "Smile Đồng Tháp", "address": "594 Quốc Lộ 50, Bình Đông Trung, Đồng Sơn, Đồng Tháp"},
    {"name": "Smile Phan Thiết", "address": "05 Võ Thị Sáu, Phường Bình Hưng, TP. Phan Thiết"},
]
VN["stores"] = COMVN["stores"] = STORES or CUA_HANG
SITES = [VN, COMVN]
