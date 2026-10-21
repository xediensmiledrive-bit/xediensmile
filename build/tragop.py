# -*- coding: utf-8 -*-
"""Trang Trả góp /tra-gop/ cho phoxedien.vn (giao 21/10/2026 sáng): chọn dòng xe, mẫu xe đang bán (giá Smile trong gia-smile.json)
rồi tính góp mỗi tháng theo 6 công ty tài chính.
Công thức, % trả trước, kỳ hạn, lãi, bảo hiểm LẤY NGUYÊN từ máy tính trả góp xediensmile.com (js/tra-gop.js ?ver=1.0.24.tg5,
bảng đối tác in trong form trang chủ, đo 21/10/2026): bảng số ở tra-gop-doi-tac.json, hàm tính ở tra-gop.js (chép nguyên phần tính).
Đổi số thì chép lại bảng từ xediensmile.com, không sửa tay ở đây."""
import html
import json
import os
import shutil

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


# Form để lại thông tin sau bảng tính (anh chốt 21/10 9:35): gửi về /api/lien-he.php kèm xe, trả trước, kỳ hạn;
# máy chủ ghi lại và chuyển tiếp cho chatbot2 để chia cho sale.
LEAD_JS = r"""(function(){var f=document.querySelector('[data-tgp-lead]');if(!f)return;
var $=function(s){return document.querySelector(s)},chon=function(n){var c=document.querySelector('[data-nhom="'+n+'"] .tgp-chip[aria-pressed="true"]');return c?c.dataset.v:''};
function tom(){var t=($('[data-tgp-ten]')||{}).textContent||'',g=($('[data-tgp-gia]')||{}).textContent||'';
 return {xe:t,gia:g,tra_truoc:chon('tra-truoc'),ky_han:chon('ky-han')}}
function ve(){var x=tom();$('[data-tgp-tom]').textContent=x.xe?('Bạn đang xem: '+x.xe+' · '+x.gia+' · trả trước '+x.tra_truoc+'% · góp '+x.ky_han+' tháng'):''}
document.addEventListener('click',function(e){if(e.target.closest('.tgp-chip'))setTimeout(ve,0)});
var sel=$('[data-tgp-xe]');if(sel)sel.addEventListener('change',ve);setTimeout(ve,0);
f.addEventListener('submit',function(e){e.preventDefault();var kq=$('[data-tgp-kq]'),b=f.querySelector('button');
 var sdt=f.sdt.value.replace(/\D/g,'');if(!/^0[35789]\d{8}$/.test(sdt)){kq.className='tgp-lead-kq loi';kq.textContent='Bạn kiểm tra lại số điện thoại (10 số, bắt đầu bằng 0).';f.sdt.focus();return}
 var x=tom();x.loai='tra-gop';x.ten=f.ten.value.trim();x.sdt=sdt;x.ghi_chu=f.ghi_chu.value.trim();x.web=(window.PXD||{}).web||location.hostname;x.trang=location.pathname+location.search;x.luc=new Date().toISOString();
 b.disabled=true;kq.className='tgp-lead-kq';kq.textContent='Đang gửi...';
 var hong=function(){b.disabled=false;kq.className='tgp-lead-kq loi';kq.textContent='Chưa gửi được. Bạn gọi hoặc nhắn Zalo __HOT__, nhân viên nghe máy ngay ạ.'};
 fetch('/api/lien-he.php',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(x)}).then(function(r){if(!r.ok)return hong();
  f.classList.add('xong');kq.className='tgp-lead-kq ok';kq.textContent='Đã nhận thông tin. Nhân viên Smile sẽ gọi '+sdt.replace(/(\d{4})(\d{3})(\d{3})/,'$1.$2.$3')+' trong giờ làm việc 8h–21h.'}).catch(hong)});
})();"""


def du_lieu_dt():
    """Bảng đối tác cho ô "Trả góp từ" trên trang từng xe (tải /tra-gop-dt.json)."""
    return json.dumps(_doi_tac(), ensure_ascii=False)


def chep(base):
    shutil.copy(os.path.join(HERE, "tra-gop.js"), base)
    open(os.path.join(base, "tra-gop-dt.json"), "w", encoding="utf-8").write(du_lieu_dt())


def gan(vn):
    """Gọi sau sanpham.gan (cần anhxe.SP đã có danh sách trang xe)."""
    import sanpham
    anhxe.WEB = vn["domain"]
    xe = []
    for k, m in sanpham.ds_xe():
        if not m.get("price"):
            continue  # chỉ mẫu có giá Smile trên web; mẫu "Liên hệ" không tính được
        if vn["domain"] == "phoxedien.com.vn" and "dv motor" in (m.get("brand") or "").lower():
            continue  # luật cứng: không thêm nội dung DV Motor trên .com.vn
        xe.append({"n": m["name"].strip(), "g": int(m["price"]), "l": _loai(m), "d": k, "b": (m.get("brand") or "").strip(),
                   "u": anhxe.url_xe(m["name"]) or "", "a": anhxe.anh(m["name"]) or ""})
    anhxe.WEB = ""
    xe.sort(key=lambda x: (x["b"], x["g"]))
    _XE[vn["domain"]] = xe
    vn["pages"].insert(-1, {"url": URL, "title": "Trả góp xe máy điện, xe 50cc: góp mỗi tháng bao nhiêu",
                            "desc": "Chọn mẫu xe đang bán, mức trả trước và kỳ hạn để xem số góp mỗi tháng theo FE Credit, HD Saison, Home Credit, Mirae Asset, AEON, Shinhan.",
                            "body": body, "crumbs": [("Trang chủ", "/"), ("Trả góp", URL)]})


def _chips(nhom, ds, chon, duoi):
    return '<div class="tgp-chips" role="group" data-nhom="%s">%s</div>' % (nhom, "".join(
        '<button type="button" class="tgp-chip" data-v="%s" aria-pressed="%s">%s%s</button>' % (v, "true" if v == chon else "false", v, duoi) for v in ds))


def _bai_doc(site):
    """Bài về trả góp (url /tra-gop/<slug>/): lãi suất, giấy tờ, từng công ty tài chính."""
    ds = [a for a in site["articles"] if a.get("url", "").startswith(URL) and a["url"] != URL]
    if not ds:
        return ""
    return ('<section class="tgp-doc"><h2>Đọc trước khi góp</h2><ul>%s</ul></section>'
            % "".join('<li><a href="%s">%s</a></li>' % (a["url"], html.escape(a.get("h1") or a.get("title", ""))) for a in ds[:12]))


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
<div class="mo-dau"><h1>Tính trả góp xe điện, xe 50cc</h1><p>Chọn mẫu xe, mức trả trước và số tháng góp: bảng dưới hiện số góp mỗi tháng của từng công ty tài chính. Giá xe là giá tại Smile, chưa gồm lệ phí trước bạ, biển số.</p></div>
<form class="tgp-form" data-tgp onsubmit="return false">
<div class="tgp-o"><span class="tgp-nhan">1. Dòng xe</span><div class="tgp-chips" role="group" data-nhom="dong">{"".join('<button type="button" class="tgp-chip" data-v="%s" aria-pressed="%s">%s <small>%d</small></button>' % (k, "true" if k == dong_md else "false", t, dem[k]) for k, t in DONG if dem[k])}</div></div>
<div class="tgp-o"><label class="tgp-nhan" for="tgp-xe">2. Mẫu xe</label><select id="tgp-xe" data-tgp-xe></select>
<div class="tgp-xe" data-tgp-the><span class="tgp-anh" data-tgp-anh></span><span class="tgp-xe-nd"><b data-tgp-ten></b><span class="tgp-gia" data-tgp-gia></span><a data-tgp-link href="#" hidden>Xem xe ›</a></span></div></div>
<div class="tgp-o"><span class="tgp-nhan">3. Trả trước</span>{_chips("tra-truoc", [10, 20, 30, 40, 50], 30, "%")}<p class="tgp-tt" data-tgp-tt></p></div>
<div class="tgp-o"><span class="tgp-nhan">4. Góp trong</span>{_chips("ky-han", [6, 9, 12, 18, 24], 12, " tháng")}</div>
<div class="tgp-bang" data-tgp-bang aria-live="polite"></div>
<p class="tgp-chan">Số góp dự kiến, số chính xác theo hồ sơ được duyệt của từng công ty tài chính. Mức lãi %/tháng hoặc %/năm ghi trên thẻ được tính trên số tiền vay ban đầu (lãi phẳng), nên lãi thực mỗi năm cao hơn con số ghi. Riêng Shinhan tính trên dư nợ giảm dần.</p>
<script type="application/json" data-tgp-dl>{data}</script>
</form>
<form class="tgp-lead" data-tgp-lead novalidate>
<b class="tgp-lead-dau">Để lại số, Smile gọi tư vấn hồ sơ trả góp</b>
<p class="tgp-lead-tom" data-tgp-tom></p>
<label>Họ tên<input name="ten" autocomplete="name" maxlength="60" placeholder="Ví dụ: Nguyễn Văn An"></label>
<label>Số điện thoại<input name="sdt" type="tel" inputmode="numeric" autocomplete="tel" maxlength="14" required placeholder="09xx xxx xxx"></label>
<label>Cần hỏi thêm <small>(không bắt buộc)</small><textarea name="ghi_chu" maxlength="300" rows="2" placeholder="Màu xe, giấy tờ đang có, giờ tiện nghe máy..."></textarea></label>
<button type="submit" class="btn btn-chinh">Gửi thông tin</button>
<p class="tgp-lead-kq" data-tgp-kq aria-live="polite"></p>
<p class="tgp-lead-rieng">Thông tin chỉ dùng để nhân viên Smile gọi tư vấn trả góp cho bạn, không chia sẻ cho bên khác.</p>
</form>
{_bai_doc(site)}<div class="tgp-keu"><b>Muốn làm hồ sơ hoặc hỏi số chính xác?</b><p>Gọi hoặc nhắn Zalo {site["hot"]}, nhân viên Smile tính đúng theo giấy tờ của bạn và báo xe còn màu nào.</p>
<a class="btn btn-chinh" href="tel:{so}">Gọi {site["hot"]}</a> <a class="btn tgp-zalo" href="https://zalo.me/{so}" target="_blank" rel="noopener nofollow">Nhắn Zalo</a>
<p class="tgp-giay">Mang giấy tờ ra cửa hàng, nhân viên làm hồ sơ ngay tại chỗ; hồ sơ duyệt xong là nhận xe.{cs}</p></div>
</div>
<script>{js}</script>
<script>{LEAD_JS.replace("__HOT__", site["hot"])}</script>'''
