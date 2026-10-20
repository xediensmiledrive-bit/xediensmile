# -*- coding: utf-8 -*-
"""Trang theo hãng cho phoxedien.vn (anh chốt 20/10: tối ưu theo cách phoxedien.com chia danh mục hãng × loại xe).
Chỉ dựng trang cho hãng có từ 2 mẫu trong gia-smile.json, mọi con số lấy từ file giá, không bịa."""
import re
import unicodedata

from noidung import (MODELS, NHOM, THANG, NGAY_VN, VN, vnd, models_of, faq_html_local, faq_ld_local,
                     keu, xe_svg, dap_svg)

# Loại xe làm trang hãng trên .vn: khoá NHOM -> (đường dẫn trang loại, tên ngắn trong tiêu đề)
LOAI = {"may": ("/xe-may-dien/", "Xe máy điện"), "dap": ("/xe-dap-dien/", "Xe đạp điện")}
TOI_THIEU = 2


def slug(s):
    s = unicodedata.normalize("NFD", s.replace("đ", "d").replace("Đ", "D"))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def hang_cua(k):
    """{tên hãng: [mẫu]} cho một loại xe, chỉ hãng đủ số mẫu."""
    g = {}
    for m in models_of(k):
        b = (m.get("brand") or "").strip()
        if b:
            g.setdefault(b, []).append(m)
    return {b: ms for b, ms in sorted(g.items(), key=lambda x: (-len(x[1]), x[0])) if len(ms) >= TOI_THIEU}


def dong(m, k):
    spec = " · ".join(x for x in [m.get("range"), m.get("speed")] if x)
    g = '<span class="gia">%s</span>' % vnd(m["price"]) if m.get("price") else '<span class="gia lh">Liên hệ</span>'
    return '<div class="dong" data-n="%s"><div class="ten">%s<small>%s</small></div>%s</div>' % (k, m["name"], spec or NHOM[k][0], g)


def itemlist_ld(url, ms):
    items = []
    for i, m in enumerate(ms):
        p = {"@type": "Product", "name": m["name"]}
        if m.get("brand"):
            p["brand"] = {"@type": "Brand", "name": m["brand"]}
        if m.get("price"):
            p["offers"] = {"@type": "Offer", "price": int(m["price"]), "priceCurrency": "VND",
                           "availability": "https://schema.org/InStock", "seller": {"@type": "Organization", "name": "Smile Motor"}}
        items.append({"@type": "ListItem", "position": i + 1, "item": p})
    return {"@context": "https://schema.org", "@type": "ItemList", "url": "https://phoxedien.vn" + url, "itemListElement": items}


def trang_hang(k, b, ms):
    goc, ten_loai = LOAI[k]
    url = "%s%s/" % (goc, slug(b))
    ms = sorted(ms, key=lambda m: (m.get("price") is None, m.get("price") or 0))
    co_gia = [m for m in ms if m.get("price")]
    re_nhat = co_gia[0] if co_gia else None
    dat_nhat = co_gia[-1] if co_gia else None
    khoang = ("từ %s đến %s" % (vnd(re_nhat["price"]), vnd(dat_nhat["price"]))) if co_gia and re_nhat is not dat_nhat else (
        vnd(re_nhat["price"]) if re_nhat else "Liên hệ")
    h1 = "%s %s: bảng giá tháng %s" % (ten_loai, b, THANG)
    svg = dap_svg() if k == "dap" else xe_svg()
    tom = ['%d mẫu %s %s đang có giá tham khảo tại Smile Motor.' % (len(ms), ten_loai.lower(), b),
           "Khoảng giá: %s." % khoang]
    if re_nhat:
        tom.append("Mẫu giá thấp nhất: %s (%s)." % (re_nhat["name"], vnd(re_nhat["price"])))
    faqs = [
        ("%s %s giá bao nhiêu?" % (ten_loai, b),
         "Theo bảng giá tham khảo cập nhật %s, %s %s có giá %s. Giá chưa gồm lệ phí trước bạ, biển số và bảo hiểm; giá trong tháng có thể đổi theo khuyến mãi." % (
             NGAY_VN, ten_loai.lower(), b, khoang)),
        ("Mẫu %s %s nào rẻ nhất?" % (ten_loai.lower(), b),
         ("%s, giá tham khảo %s." % (re_nhat["name"], vnd(re_nhat["price"]))) if re_nhat else "Các mẫu đang cập nhật giá, bạn chat hoặc gọi để có giá hôm nay."),
        ("Mua %s %s ở đâu?" % (ten_loai.lower(), b),
         "Smile Motor có 6 cửa hàng (TP.HCM, Đồng Tháp, Phan Thiết), mở cửa 8h–21h. Bạn chat trên trang hoặc gọi, nhắn Zalo 0888.266.233 để hỏi mẫu còn hàng và quà tặng."),
    ]
    khac = [x for x in hang_cua(k) if x != b][:8]
    lien = "".join('<a class="chip" href="%s%s/">%s %s</a>' % (goc, slug(x), ten_loai, x) for x in khac)

    def body(s):
        return f'''<div class="wrap"><div class="duong"><a href="/">Trang chủ</a> › <a href="{goc}">{ten_loai}</a> › <b>{b}</b></div>
<div class="dau-trang"><h1>{h1}</h1><div class="tac"><span class="av">K</span><span><a href="/tac-gia/kha-uyen/">Khả Uyên</a> · cập nhật {NGAY_VN}</span></div></div>
<div class="nhanh hd-in"><b>Tóm tắt nhanh</b><ul>{"".join("<li>%s</li>" % t for t in tom)}</ul></div>
<section style="margin-top:20px"><div class="the bang hd-in"><div class="dong dau"><span>Mẫu {ten_loai.lower()} {b}</span><span>Giá tham khảo</span></div>{"".join(dong(m, k) for m in ms)}
<div class="chu-thich">Giá tham khảo cập nhật {NGAY_VN}, giá bán tại Smile Motor, chưa gồm lệ phí trước bạ, biển số và bảo hiểm.</div></div></section>
<section class="noi-dung hd-in"><h2>Chọn {ten_loai.lower()} {b} sao cho đúng</h2>
<p>Các mẫu {b} trong bảng xếp từ giá thấp đến cao. Khi so hai mẫu gần giá nhau, nhìn quãng đường mỗi lần sạc và tốc độ tối đa ở dòng chữ nhỏ dưới tên xe, rồi xem loại pin: bản pin lithium thường đắt hơn bản ắc quy chì nhưng nhẹ và bền hơn (<a href="/so-sanh/pin-lithium-hay-ac-quy-chi/">so sánh hai loại pin</a>).</p>
<p>Muốn biết tổng tiền phải trả, cộng thêm lệ phí trước bạ, biển số và bảo hiểm theo bài <a href="/bang-gia/gia-lan-banh-xe-may-dien-xe-50cc/">cách tính giá lăn bánh</a>. Xem tất cả hãng ở trang <a href="{goc}">{ten_loai.lower()}</a> hoặc <a href="/bang-gia-xe-dien/">bảng giá xe điện tháng {THANG}</a>.</p></section>
{('<section><div class="tieude"><h2>Hãng khác</h2></div><nav class="chips" style="padding:0;flex-wrap:wrap">%s</nav></section>' % lien) if lien else ""}
<section class="hd-in"><div class="tieude"><h2>Hỏi đáp {ten_loai.lower()} {b}</h2></div>{faq_html_local(faqs)}</section>
{keu(VN["cta_title"], VN["cta_text"])}</div>'''

    return {"url": url, "title": "%s %s: giá tham khảo tháng %s (%d mẫu)" % (ten_loai, b, THANG, len(ms)),
            "desc": "Bảng giá %s %s tháng %s: %d mẫu, %s. Có so sánh pin, quãng đường và hỏi đáp." % (ten_loai.lower(), b, THANG, len(ms), khoang),
            "body": body, "schemas": [faq_ld_local(faqs), itemlist_ld(url, ms)],
            "crumbs": [("Trang chủ", "/"), (ten_loai, goc), (b, url)]}


def chip_hang(k):
    goc, ten_loai = LOAI[k]
    hs = hang_cua(k)
    if not hs:
        return ""
    return '<section><div class="tieude"><h2>Xem theo hãng</h2></div><nav class="chips" style="padding:0;flex-wrap:wrap">%s</nav></section>' % "".join(
        '<a class="chip" href="%s%s/">%s <small style="opacity:.7">(%d)</small></a>' % (goc, slug(b), b, len(ms)) for b, ms in hs.items())


def them_trang_hang(site):
    """Gắn trang hãng vào site, thêm khối 'Xem theo hãng' vào trang loại xe, thêm schema FAQ và ItemList cho trang loại."""
    moi = []
    for k in LOAI:
        for b, ms in hang_cua(k).items():
            moi.append(trang_hang(k, b, ms))
    return moi


def schema_trang_loai(k):
    ms = sorted(models_of(k), key=lambda m: (m.get("price") is None, m.get("price") or 0))
    return [itemlist_ld(LOAI.get(k, ("/bang-gia-xe-dien/",))[0], ms[:50])] if ms else []
