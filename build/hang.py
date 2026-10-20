# -*- coding: utf-8 -*-
"""Trang loại xe và trang theo hãng cho 2 web (anh chốt 20/10):
- cả 2 web đánh cả xe xăng 50cc lẫn xe điện;
- phoxedien.vn bám sát cây danh mục của phoxedien.com (loại xe × hãng), giọng bảng giá;
- phoxedien.com.vn làm trang loại xe theo góc "cho học sinh", giọng cẩm nang, không làm trang hãng để không trùng .vn.
Chỉ dựng trang hãng khi hãng có từ 2 mẫu trong gia-smile.json; mọi con số lấy từ file giá, không bịa."""
import re
import unicodedata

import anhxe

from noidung import (o_gia, THI_TRUONG, NGUNG_BAN, NHOM, THANG, NGAY_VN, VN, COMVN, vnd, models_of, bang, faq_html_local, faq_ld_local,
                     keu, xe_svg, dap_svg)

TOI_THIEU = 2
# Thứ tự ưu tiên từ khoá chung (anh chốt 20/10): xediensmile/smilemotor > dvmotor.vn/dvmotors > 2 web phoxedien.
# Anh chốt 10:09: trùng từ khoá thì viết khác góc, mỗi web số điện thoại riêng, không ẩn trang nào. Để trống.
NHUONG_HANG = set()
LUAT = "Luật Trật tự, an toàn giao thông đường bộ 2024 (hiệu lực 01/01/2025)"

# Loại xe trên phoxedien.vn: khoá -> (đường dẫn, tên)
LOAI_VN = {"may": ("/xe-may-dien/", "Xe máy điện"), "dap": ("/xe-dap-dien/", "Xe đạp điện"),
           "ga": ("/xe-ga-50cc/", "Xe ga 50cc"), "so": ("/xe-so-50cc/", "Xe số 50cc"), "wave": ("/xe-wave-50cc/", "Xe wave 50cc")}
# Trang loại xe mới cần dựng thêm trên .vn (máy điện, đạp điện, 3 bánh đã có sẵn trong noidung.py)
MOI_VN = ["ga", "so", "wave"]
# Trang loại xe trên phoxedien.com.vn, góc học sinh
LOAI_COMVN = {"ga": ("/xe-ga-50cc-cho-hoc-sinh/", "Xe ga 50cc cho học sinh"), "so": ("/xe-so-50cc-cho-hoc-sinh/", "Xe số 50cc cho học sinh"),
              "may": ("/xe-may-dien-cho-hoc-sinh/", "Xe máy điện cho học sinh"), "dap": ("/xe-dap-dien-cho-hoc-sinh/", "Xe đạp điện cho học sinh")}


def slug(s):
    s = unicodedata.normalize("NFD", s.replace("đ", "d").replace("Đ", "D"))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def sap(ms):
    return sorted(ms, key=lambda m: (m.get("price") is None, m.get("price") or 0))


def hang_cua(k):
    g = {}
    for m in models_of(k):
        if k == "so" and (m.get("type") or "").lower() == "wave":
            continue  # wave đã có trang hãng riêng ở /xe-wave-50cc/, tránh 2 trang trùng mẫu
        b = (m.get("brand") or "").strip()
        if b:
            g.setdefault(b, []).append(m)
    return {b: ms for b, ms in sorted(g.items(), key=lambda x: (-len(x[1]), x[0])) if len(ms) >= TOI_THIEU}


def khoang(ms):
    ps = [m["price"] for m in ms if m.get("price")]
    if not ps:
        return "Liên hệ"
    return vnd(min(ps)) if min(ps) == max(ps) else "từ %s đến %s" % (vnd(min(ps)), vnd(max(ps)))


def dong(m, k):
    spec = " · ".join(x for x in [m.get("brand"), m.get("range"), m.get("speed")] if x)
    g = o_gia(m)
    return '<div class="dong" data-n="%s">%s<div class="ten">%s<small>%s</small></div>%s</div>' % (k, anhxe.tn(m), m["name"], spec or NHOM[k][0], g)


def itemlist_ld(domain, url, ms):
    items = []
    for i, m in enumerate(ms):
        p = {"@type": "Product", "name": m["name"]}
        if anhxe.anh(m["name"]):
            p["image"] = "https://%s%s" % (domain, anhxe.anh(m["name"]))
        if m.get("brand"):
            p["brand"] = {"@type": "Brand", "name": m["brand"]}
        if m.get("price"):
            p["offers"] = {"@type": "Offer", "price": int(m["price"]), "priceCurrency": "VND",
                           "availability": "https://schema.org/InStock", "seller": {"@type": "Organization", "name": "Smile Motor"}}
        items.append({"@type": "ListItem", "position": i + 1, "item": p})
    return {"@context": "https://schema.org", "@type": "ItemList", "url": "https://%s%s" % (domain, url), "itemListElement": items}


def ngan_sach(k):
    """Bảng đếm số mẫu theo khoảng giá, tính từ file giá."""
    ps = [m["price"] for m in models_of(k) if m.get("price")]
    if len(ps) < 4:
        return ""
    moc = [(0, 10e6, "Dưới 10 triệu"), (10e6, 15e6, "10–15 triệu"), (15e6, 20e6, "15–20 triệu"), (20e6, 30e6, "20–30 triệu"), (30e6, 1e12, "Trên 30 triệu")]
    hang = "".join('<tr><td>%s</td><td>%d mẫu</td></tr>' % (t, sum(1 for p in ps if a <= p < b)) for a, b, t in moc if any(a <= p < b for p in ps))
    return '<h2>Có bao nhiêu mẫu ở mỗi tầm giá</h2><div class="cuon-bang"><table><tr><th>Tầm giá</th><th>Số mẫu</th></tr>%s</table></div><p>Theo bảng giá cập nhật %s.</p>' % (hang, NGAY_VN)


def chip_hang(k, goc):
    hs = hang_cua(k)
    if not hs:
        return ""
    return '<section><div class="tieude"><h2>Xem theo hãng</h2></div><nav class="chips" style="padding:0;flex-wrap:wrap">%s</nav></section>' % "".join(
        '<a class="chip" href="%s%s/">%s <small style="opacity:.7">(%d)</small></a>' % (goc, slug(b), b, len(ms)) for b, ms in hs.items())


# ---------------- Nội dung riêng từng loại ----------------
GIOI_THIEU_VN = {
    "ga": f'''<p>Xe ga 50cc là xe gắn máy có hộp số tự động, dung tích xi lanh dưới 50 cm³ và tốc độ thiết kế đến 50 km/h. Theo {LUAT}, người từ đủ 16 tuổi được điều khiển xe gắn máy và không cần giấy phép lái xe; xe vẫn phải đăng ký, gắn biển số.</p>
<h2>Ba thứ làm giá xe ga 50cc chênh nhau</h2><ul><li><b>Thân vỏ và cốp:</b> mẫu cốp rộng, yên dài, đèn LED thường đắt hơn.</li><li><b>Phanh:</b> phanh đĩa trước an toàn hơn phanh cơ khi chở người hoặc đi mưa.</li><li><b>Hãng và bảo hành:</b> hãng có xưởng, phụ tùng gần nhà thì nuôi xe rẻ hơn về lâu dài.</li></ul>''',
    "so": f'''<p>Xe số 50cc (gồm dáng wave và cub) là xe gắn máy dưới 50 cm³, số tròn, không có côn tay. Xe nhẹ, rẻ, dễ sửa và tiết kiệm xăng, nên hợp học sinh từ đủ 16 tuổi và người đi làm gần. Theo {LUAT}, xe gắn máy không cần bằng lái nhưng phải đăng ký biển số.</p>
<h2>Xe số hay xe ga</h2><p>Xe số rẻ hơn xe ga cùng hãng, nhẹ hơn và phụ tùng dễ tìm. Xe ga có cốp, không phải sang số, dễ đi trong phố đông. So sánh đủ ưu nhược ở bài <a href="/so-sanh/xe-ga-50cc-hay-xe-so-50cc/">xe ga 50cc hay xe số 50cc</a>.</p>''',
    "wave": f'''<p>Wave 50cc là dáng xe số quen thuộc nhất: yên dài, gầm cao vừa, số tròn 4 cấp, không côn. Nhiều hãng làm dáng này ở bản dưới 50 cm³ để học sinh từ đủ 16 tuổi đi được mà không cần bằng lái ({LUAT}).</p>
<h2>Khi chọn wave 50cc</h2><ul><li>Ngồi thử: hai chân chạm đất là vừa.</li><li>Xem phanh trước (đĩa hay cơ) và vành (đúc hay nan).</li><li>Hỏi hãng có bảo hành, có phụ tùng thay thế ở gần nhà không.</li></ul>''',
}
FAQ_VN = {
    "ga": [("Xe ga 50cc bao nhiêu tuổi được đi?", f"Từ đủ 16 tuổi, theo {LUAT}."),
           ("Xe ga 50cc có cần bằng lái không?", "Không. Xe gắn máy dưới 50 cm³ không thuộc hạng giấy phép lái xe nào. Xe vẫn phải đăng ký, gắn biển số và có bảo hiểm bắt buộc."),
           ("Xe ga 50cc tốn xăng không?", "Mỗi mẫu có mức tiêu hao nhiên liệu riêng do hãng công bố. Bạn chat hoặc gọi để được báo số liệu của mẫu cụ thể.")],
    "so": [("Xe số 50cc có cần bằng lái không?", "Không, với xe dưới 50 cm³ và tốc độ thiết kế đến 50 km/h. Người đi phải từ đủ 16 tuổi."),
           ("Xe số 50cc có côn không?", "Xe số 50cc phổ thông dùng số tròn, không có côn tay, chỉ cần sang số bằng chân."),
           ("Giá xe số 50cc đã gồm biển số chưa?", "Chưa. Giá trong bảng là giá xe; lệ phí trước bạ, biển số và bảo hiểm tính riêng.")],
    "wave": [("Wave 50cc có cần bằng lái không?", "Không, nếu dung tích dưới 50 cm³. Người đi phải từ đủ 16 tuổi."),
             ("Wave 50cc và wave 110 khác gì?", "Wave 110 có dung tích trên 50 cm³ nên là mô tô, người đi phải có bằng lái hạng A1. Wave 50cc là xe gắn máy, không cần bằng."),
             ("Mua wave 50cc ở đâu?", "Smile Motor có 6 cửa hàng, mở cửa 8h–21h. Bạn chat trên trang hoặc gọi, nhắn Zalo 0888.266.233.")],
}
GIOI_THIEU_COMVN = {
    "ga": '''<p>Con đủ 16 tuổi, đi học dưới 10 km, nhà không có chỗ sạc: xe ga 50cc là lựa chọn nhiều phụ huynh nghiêng về. Xe tự động nên con không phải sang số, có cốp để áo mưa và cặp.</p>
<h2>Mẹ nên thử 3 việc ở cửa hàng</h2><ul><li>Cho con ngồi lên: hai chân chạm đất khi dừng đèn đỏ.</li><li>Cho con tự dắt xe vài mét và dựng chân chống giữa.</li><li>Bóp thử phanh trước, hỏi phanh đĩa hay phanh cơ.</li></ul>''',
    "so": '''<p>Xe số 50cc rẻ hơn xe ga, nhẹ hơn và ít hỏng vặt, nên hợp với con đi học đường bằng, gần nhà. Con cần tập sang số vài buổi, nhưng không có côn tay nên quen rất nhanh.</p>
<h2>Khi nào nên chọn xe số cho con</h2><ul><li>Ngân sách chặt, muốn chi phí sửa chữa thấp.</li><li>Con đã quen đi xe đạp, phản xạ tốt.</li><li>Đường đi học ít kẹt xe (kẹt xe nhiều thì xe ga đỡ mỏi tay hơn).</li></ul>''',
    "may": '''<p>Con đủ 16 tuổi được đi xe máy điện loại xe gắn máy (công suất đến 4 kW, tốc độ thiết kế đến 50 km/h) mà không cần bằng lái. Xe êm, không tốn xăng, hợp đường đi học dưới 30 km mỗi ngày và nhà có chỗ sạc.</p>
<h2>Câu hỏi nên đặt cho người bán</h2><ul><li>Mẫu này là xe gắn máy điện hay mô tô điện (mô tô điện cần bằng A1)?</li><li>Pin lithium hay ắc quy chì, bảo hành pin bao lâu?</li><li>Sạc đầy mất mấy tiếng, có sạc được ở ổ điện thường không?</li></ul>''',
    "dap": '''<p>Con dưới 16 tuổi chưa được đi xe gắn máy, nên xe đạp điện là lựa chọn hợp luật và nhẹ ví. Xe có bàn đạp, tốc độ thấp và không phải đăng ký biển số.</p>
<h2>Chọn xe đạp điện vừa với con</h2><ul><li>Chiều cao yên: ngồi lên, hai mũi chân chạm đất.</li><li>Cân nặng xe: con tự dắt, tự dựng chân chống được.</li><li>Phanh hai bánh còn ăn, đèn và còi đủ sáng, đủ to.</li></ul>''',
}
FAQ_COMVN = {
    "ga": [("Con 16 tuổi đi xe ga 50cc cần giấy tờ gì?", 'Căn cước hoặc giấy tờ tuỳ thân, giấy đăng ký xe và bảo hiểm bắt buộc. Xem đủ ở <a href="/giay-to/16-tuoi-di-xe-50cc-can-giay-to-gi/">bài giấy tờ khi đi xe 50cc</a>.'),
           ("Xe ga 50cc hay xe máy điện cho con?", "Nhà có chỗ sạc, đường đi học dưới 30 km mỗi ngày thì xe máy điện rẻ hơn khi đi. Không có chỗ sạc hoặc đi xa thì xe ga 50cc tiện hơn.")],
    "so": [("Con gái đi xe số 50cc được không?", "Được. Xe số 50cc nhẹ, yên thấp vừa, chỉ cần con tập sang số vài buổi."),
           ("Xe số 50cc có bền không?", "Xe số cấu tạo đơn giản nên ít hỏng vặt, phụ tùng rẻ, dễ thay ở các tiệm sửa xe.")],
    "may": [("Học sinh đi xe máy điện có cần bằng lái không?", "Không, nếu là xe gắn máy điện (đến 4 kW, tốc độ thiết kế đến 50 km/h) và con đủ 16 tuổi. Xe mạnh hơn là mô tô điện, cần bằng A1."),
            ("Xe máy điện có phải đăng ký biển số không?", "Có. Xe máy điện phải đăng ký và gắn biển số như xe xăng.")],
    "dap": [("Xe đạp điện có cần biển số không?", "Không. Người đi vẫn phải đội mũ bảo hiểm và đi đúng làn."),
            ("Con lớp 7 đi xe đạp điện được không?", "Luật không đặt tuổi tối thiểu riêng cho xe đạp điện. Phụ huynh nên cho con đi khi con đã đi xe đạp vững và quen đường.")],
}


def _trang_loai(site, k, url, ten, gioi, faqs, tac, av, khung_tim):
    ms = sap(models_of(k))
    tt = sap(THI_TRUONG.get(k, [])) if (k in NGUNG_BAN and not ms) else []
    dong_gia = ("Giá thị trường tham khảo (theo giá hãng và đại lý), có thể khác tuỳ nơi bán." if tt
                else "Giá chưa gồm lệ phí trước bạ, biển số và bảo hiểm.")
    svg = dap_svg() if k == "dap" else xe_svg()
    h1 = "%s: bảng giá tháng %s và cách chọn" % (ten, THANG) if site is VN else "%s: chọn sao cho đúng, giá tháng %s" % (ten, THANG)

    def body(s):
        return f'''<div class="wrap"><div class="duong"><a href="/">Trang chủ</a> › <b>{ten}</b></div>
<div class="dau-trang"><h1>{h1}</h1><div class="tac"><span class="av">{av}</span><span><a href="/tac-gia/{tac[0]}/">{tac[1]}</a> · cập nhật {NGAY_VN}</span></div></div>
<div class="nhanh hd-in"><b>Tóm tắt nhanh</b><ul><li>{len(ms or tt) or "Các"} mẫu {NHOM[k][0].lower()} có giá tham khảo, {khoang(ms or tt)}.</li><li>{dong_gia}</li></ul></div>
<div class="hinh-hero hd-in" style="background:var(--hero);height:170px;border-radius:20px;margin:16px 0">{svg}</div>
<div class="noi-dung">{gioi}</div>
<section>{bang([k], "bg-" + slug(ten))}</section>
{khung_tim}
<section class="noi-dung hd-in">{ngan_sach(k)}</section>
<section class="hd-in"><div class="tieude"><h2>Hỏi đáp</h2></div>{faq_html_local(faqs)}</section>
{keu(site["cta_title"], site["cta_text"])}</div>'''

    sch = [faq_ld_local(faqs)] + ([itemlist_ld(site["domain"], url, ms[:50])] if ms else [])
    title = ("%s: giá tham khảo tháng %s, so sánh các hãng" if site is VN else "%s: chọn xe và giá tháng %s") % (ten, THANG)
    desc = "%s tháng %s: %s. Cách chọn, hỏi đáp về tuổi, bằng lái, biển số." % (ten, THANG, khoang(ms or tt))
    p = {"url": url, "title": title, "desc": desc, "body": body, "schemas": sch, "crumbs": [("Trang chủ", "/"), (ten, url)]}
    if not ms and not tt:
        p["robots"] = "noindex,follow"  # chưa có mẫu nào trong bảng giá: ẩn khỏi Google tới khi có giá
    return p


def trang_hang(k, b, ms):
    goc, ten_loai = LOAI_VN[k]
    url = "%s%s/" % (goc, slug(b))
    ms = sap(ms)
    co_gia = [m for m in ms if m.get("price")]
    re_nhat = co_gia[0] if co_gia else None
    kg = khoang(ms)
    h1 = "%s %s: bảng giá tháng %s" % (ten_loai, b, THANG)
    tom = ['%d mẫu %s %s đang có giá tham khảo tại Smile Motor.' % (len(ms), ten_loai.lower(), b), "Khoảng giá: %s." % kg]
    if re_nhat:
        tom.append("Mẫu giá thấp nhất: %s (%s)." % (re_nhat["name"], vnd(re_nhat["price"])))
    dien = k in ("may", "dap")
    faqs = [
        ("%s %s giá bao nhiêu?" % (ten_loai, b),
         "Theo bảng giá tham khảo cập nhật %s, %s %s có giá %s. Giá chưa gồm lệ phí trước bạ, biển số và bảo hiểm; giá trong tháng có thể đổi theo khuyến mãi." % (NGAY_VN, ten_loai.lower(), b, kg)),
        ("Mẫu %s %s nào rẻ nhất?" % (ten_loai.lower(), b),
         ("%s, giá tham khảo %s." % (re_nhat["name"], vnd(re_nhat["price"]))) if re_nhat else "Các mẫu đang cập nhật giá, bạn chat hoặc gọi để có giá hôm nay."),
        ("Mua %s %s ở đâu?" % (ten_loai.lower(), b),
         "Smile Motor có 6 cửa hàng (TP.HCM, Đồng Tháp, Phan Thiết), mở cửa 8h–21h. Bạn chat trên trang hoặc gọi, nhắn Zalo 0888.266.233 để hỏi mẫu còn hàng và quà tặng."),
    ]
    khac = [x for x in hang_cua(k) if x != b][:8]
    lien = "".join('<a class="chip" href="%s%s/">%s %s</a>' % (goc, slug(x), ten_loai, x) for x in khac)
    so_sanh = ('Khi so hai mẫu gần giá nhau, nhìn quãng đường mỗi lần sạc và tốc độ tối đa ở dòng chữ nhỏ dưới tên xe, rồi xem loại pin: bản pin lithium thường đắt hơn bản ắc quy chì nhưng nhẹ và bền hơn (<a href="/so-sanh/pin-lithium-hay-ac-quy-chi/">so sánh hai loại pin</a>).'
               if dien else 'Khi so hai mẫu gần giá nhau, xem phanh trước (đĩa hay cơ), vành đúc hay nan và chiều cao yên so với người đi. Phân vân giữa xe ga và xe số thì đọc <a href="/so-sanh/xe-ga-50cc-hay-xe-so-50cc/">so sánh xe ga và xe số 50cc</a>.')
    bg = "/bang-gia-xe-dien/" if dien else "/bang-gia-xe-50cc/"

    def body(s):
        return f'''<div class="wrap"><div class="duong"><a href="/">Trang chủ</a> › <a href="{goc}">{ten_loai}</a> › <b>{b}</b></div>
<div class="dau-trang"><h1>{h1}</h1><div class="tac"><span class="av">K</span><span><a href="/tac-gia/kha-uyen/">Khả Uyên</a> · cập nhật {NGAY_VN}</span></div></div>
<div class="nhanh hd-in"><b>Tóm tắt nhanh</b><ul>{"".join("<li>%s</li>" % t for t in tom)}</ul></div>
<section style="margin-top:20px"><div class="the bang hd-in"><div class="dong dau"><span>Mẫu {ten_loai.lower()} {b}</span><span>Giá tham khảo</span></div>{"".join(dong(m, k) for m in ms)}
<div class="chu-thich">Giá tham khảo cập nhật {NGAY_VN}, giá bán tại Smile Motor, chưa gồm lệ phí trước bạ, biển số và bảo hiểm.</div></div></section>
{anhxe.luoi(ms, "Ảnh %s %s" % (ten_loai.lower(), b), 12, vnd)}
<section class="noi-dung hd-in"><h2>Chọn {ten_loai.lower()} {b} sao cho đúng</h2>
<p>Các mẫu {b} trong bảng xếp từ giá thấp đến cao. {so_sanh}</p>
<p>Muốn biết tổng tiền phải trả, cộng thêm lệ phí trước bạ, biển số và bảo hiểm theo bài <a href="/bang-gia/gia-lan-banh-xe-may-dien-xe-50cc/">cách tính giá lăn bánh</a>. Xem tất cả hãng ở trang <a href="{goc}">{ten_loai.lower()}</a> hoặc <a href="{bg}">bảng giá tháng {THANG}</a>.</p></section>
{('<section><div class="tieude"><h2>Hãng khác</h2></div><nav class="chips" style="padding:0;flex-wrap:wrap">%s</nav></section>' % lien) if lien else ""}
<section class="hd-in"><div class="tieude"><h2>Hỏi đáp {ten_loai.lower()} {b}</h2></div>{faq_html_local(faqs)}</section>
{keu(VN["cta_title"], VN["cta_text"])}</div>'''

    return {"url": url, "title": "%s %s: giá tham khảo tháng %s (%d mẫu)" % (ten_loai, b, THANG, len(ms)),
            "desc": "Bảng giá %s %s tháng %s: %d mẫu, %s. Có cách chọn và hỏi đáp." % (ten_loai.lower(), b, THANG, len(ms), kg),
            "body": body, "schemas": [faq_ld_local(faqs), itemlist_ld("phoxedien.vn", url, ms)],
            "crumbs": [("Trang chủ", "/"), (ten_loai, goc), (b, url)],
            **({"robots": "noindex,follow"} if slug(b) in NHUONG_HANG else {})}


def trang_vn():
    """Trang loại mới (ga, số, wave) + trang hãng của mọi loại cho phoxedien.vn."""
    out = []
    for k in MOI_VN:
        goc, ten = LOAI_VN[k]
        out.append(_trang_loai(VN, k, goc, ten, GIOI_THIEU_VN[k], FAQ_VN[k], ("minh-trang", "Minh Trang"), "M", chip_hang(k, goc)))
    for k in LOAI_VN:
        if k == "wave":
            continue  # mẫu dáng wave đã nằm trong trang hãng xe số 50cc, không dựng trang hãng trùng
        for b, ms in hang_cua(k).items():
            out.append(trang_hang(k, b, ms))
    return out


def trang_comvn():
    tac = {"ga": ("thu-ha", "Thu Hà", "H"), "so": ("thu-ha", "Thu Hà", "H"), "may": ("quoc-bao", "Quốc Bảo", "B"), "dap": ("thu-ha", "Thu Hà", "H")}
    out = []
    for k, (url, ten) in LOAI_COMVN.items():
        t = tac[k]
        out.append(_trang_loai(COMVN, k, url, ten, GIOI_THIEU_COMVN[k], FAQ_COMVN[k], (t[0], t[1]), t[2], ""))
    return out


def schema_trang_loai(k):
    ms = sap(models_of(k))
    return [itemlist_ld("phoxedien.vn", LOAI_VN[k][0], ms[:50])] if ms and k in LOAI_VN else []
