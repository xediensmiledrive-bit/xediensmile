# -*- coding: utf-8 -*-
"""Trang Trả góp /tra-gop/ cho phoxedien.vn (giao 21/10/2026 sáng): chọn dòng xe, mẫu xe đang bán (giá Smile trong gia-smile.json)
rồi tính góp mỗi tháng theo 6 công ty tài chính.
Công thức, % trả trước, kỳ hạn, lãi, bảo hiểm LẤY NGUYÊN từ máy tính trả góp xediensmile.com (js/tra-gop.js ?ver=1.0.24.tg5,
bảng đối tác in trong form trang chủ, đo 21/10/2026): bảng số ở tra-gop-doi-tac.json, hàm tính ở tra-gop.js (chép nguyên phần tính).
Đổi số thì chép lại bảng từ xediensmile.com, không sửa tay ở đây."""
import html
import json
import os

import anhxe
import mxh
from noidung import vnd

HERE = os.path.dirname(os.path.abspath(__file__))
URL = "/tra-gop/"
DONG = [("may", "Xe máy điện"), ("ga", "Xe ga 50cc"), ("so", "Xe số 50cc")]
MAC_DINH = "chocolate v8"
_XE = {}


def _doi_tac():
    ds = json.load(open(os.path.join(HERE, "tra-gop-doi-tac.json"), encoding="utf-8"))
    co_logo = {t for _, t in mxh.doi_tac()}
    for dt in ds:
        tep = "%s.png" % dt["ma"]
        dt["logo"] = "/doi-tac/%s" % tep if tep in co_logo else ""
    return ds


def _loai(m):
    # như xds_loai_tra_gop() bên xediensmile.com: có chữ "đạp" là xe đạp điện, còn lại xe máy điện
    t = ((m.get("name") or "") + " " + (m.get("type") or "")).lower()
    return "dap" if "đạp" in t else "may"


def gan(vn):
    """Gọi sau sanpham.gan (cần anhxe.SP đã có danh sách trang xe)."""
    import sanpham
    anhxe.WEB = vn["domain"]
    xe = []
    for k, m in sanpham.ds_xe():
        if not m.get("price"):
            continue  # chỉ mẫu có giá Smile trên web; mẫu "Liên hệ" không tính được
        xe.append({"n": m["name"].strip(), "g": int(m["price"]), "l": _loai(m), "d": k, "b": (m.get("brand") or "").strip(),
                   "u": anhxe.url_xe(m["name"]) or "", "a": anhxe.anh(m["name"]) or ""})
    anhxe.WEB = ""
    xe.sort(key=lambda x: (x["b"], x["g"]))
    _XE[vn["domain"]] = xe
    vn["pages"].insert(-1, {"url": URL, "title": "Tính trả góp xe máy điện, xe 50cc: góp mỗi tháng bao nhiêu | Phố Xe Điện",
                            "desc": "Chọn mẫu xe đang bán, mức trả trước và kỳ hạn để xem số góp mỗi tháng theo FE Credit, HD Saison, Home Credit, Mirae Asset, AEON, Shinhan.",
                            "body": body, "crumbs": [("Trang chủ", "/"), ("Trả góp", URL)]})


def _chips(nhom, ds, chon, duoi):
    return '<div class="tgp-chips" role="group" data-nhom="%s">%s</div>' % (nhom, "".join(
        '<button type="button" class="tgp-chip" data-v="%s" aria-pressed="%s">%s%s</button>' % (v, "true" if v == chon else "false", v, duoi) for v in ds))


def body(site):
    xe = _XE.get(site["domain"], [])
    dem = {k: sum(1 for x in xe if x["d"] == k) for k, _ in DONG}
    md = next((x for x in xe if MAC_DINH in x["n"].lower()), xe[0] if xe else None)
    dong_md = md["d"] if md else "may"
    so = site["hot"].replace(".", "")
    data = json.dumps({"xe": xe, "dt": _doi_tac(), "md": md["n"] if md else ""}, ensure_ascii=False).replace("</", "<\\/")
    js = open(os.path.join(HERE, "tra-gop.js"), encoding="utf-8").read()
    import chinhsach
    cs = (' <a href="/chinh-sach/tra-gop/">Xem chính sách trả góp ›</a>'
          if any(u == "/chinh-sach/tra-gop/" for _, u in chinhsach.link_chan()) else "")
    return f'''<div class="wrap rong tgp"><div class="duong"><a href="/">Trang chủ</a> › <b>Trả góp</b></div>
<div class="mo-dau"><h1>Tính trả góp xe điện, xe 50cc</h1><p>Chọn mẫu xe, mức trả trước và số tháng góp: bảng dưới hiện số góp mỗi tháng của từng công ty tài chính. Giá xe là giá tham khảo tại Smile Motor, chưa gồm lệ phí trước bạ, biển số.</p></div>
<form class="tgp-form" data-tgp onsubmit="return false">
<div class="tgp-o"><span class="tgp-nhan">1. Dòng xe</span><div class="tgp-chips" role="group" data-nhom="dong">{"".join('<button type="button" class="tgp-chip" data-v="%s" aria-pressed="%s">%s <small>%d</small></button>' % (k, "true" if k == dong_md else "false", t, dem[k]) for k, t in DONG if dem[k])}</div></div>
<div class="tgp-o"><label class="tgp-nhan" for="tgp-xe">2. Mẫu xe</label><select id="tgp-xe" data-tgp-xe></select>
<div class="tgp-xe" data-tgp-the><span class="tgp-anh" data-tgp-anh></span><span class="tgp-xe-nd"><b data-tgp-ten></b><span class="tgp-gia" data-tgp-gia></span><a data-tgp-link href="#" hidden>Xem xe ›</a></span></div></div>
<div class="tgp-o"><span class="tgp-nhan">3. Trả trước</span>{_chips("tra-truoc", [10, 20, 30, 40, 50], 30, "%")}<p class="tgp-tt" data-tgp-tt></p></div>
<div class="tgp-o"><span class="tgp-nhan">4. Góp trong</span>{_chips("ky-han", [6, 9, 12, 18, 24], 12, " tháng")}</div>
<div class="tgp-bang" data-tgp-bang aria-live="polite"></div>
<p class="tgp-chan">Số tham khảo, số thật theo hồ sơ được duyệt của từng công ty tài chính. Mức lãi %/tháng hoặc %/năm ghi trên thẻ được tính trên số tiền vay ban đầu (lãi phẳng), nên lãi thực mỗi năm cao hơn con số ghi. Riêng Shinhan tính trên dư nợ giảm dần.</p>
<script type="application/json" data-tgp-dl>{data}</script>
</form>
<div class="tgp-keu"><b>Muốn làm hồ sơ hoặc hỏi số chính xác?</b><p>Gọi hoặc nhắn Zalo {site["hot"]}, nhân viên Smile Motor tính đúng theo giấy tờ của bạn và báo xe còn màu nào.</p>
<a class="btn btn-chinh" href="tel:{so}">Gọi {site["hot"]}</a> <a class="btn tgp-zalo" href="https://zalo.me/{so}" target="_blank" rel="noopener nofollow">Nhắn Zalo</a>
<p class="tgp-giay">Mang giấy tờ ra cửa hàng, nhân viên làm hồ sơ ngay tại chỗ; hồ sơ duyệt xong là nhận xe.{cs}</p></div>
</div>
<script>{js}</script>'''
