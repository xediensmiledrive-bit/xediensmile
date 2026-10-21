#!/usr/bin/env python3
"""Dựng 2 web tĩnh Phố Xe Điện: phoxedien.vn và phoxedien.com.vn."""
import json, os, re, shutil, sys, html

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
import muse  # noqa: E402
import anhxe  # noqa: E402
import sanpham  # noqa: E402
import trangchu
import danhgia
import tiktok
import mxh
import chinhsach
import trangphu
import bannerhang  # noqa: E402

# Trang loại xe và trang hãng cho 2 web (tối ưu SEO 20/10: cả 2 web đánh xe xăng 50cc lẫn xe điện)
_vn, _comvn = noidung.VN, noidung.COMVN
for _k in ("may", "dap"):
    noidung.CHIP_HANG[_k] = hang.chip_hang(_k, hang.LOAI_VN[_k][0])
# Smile ngừng bán xe đạp điện từ 25/9/2026: trang giữ dạng thông tin + mẫu tương đương đang bán (luật: không bịa giá)
if not noidung.models_of("dap"):
    _tg = [m for m in hang.sap(noidung.models_of("may")) if m.get("price") and (m.get("brand") or "") in ("DV Motor", "Dibao", "Detech", "Yaka")][:6]
    if _tg:
        noidung.CHIP_HANG["dap"] = ('<section><div class="tieude"><h2>Đủ 16 tuổi? Xem xe máy điện giá mềm</h2></div>'
                                    '<p class="meta">Từ đủ 16 tuổi được đi xe máy điện loại xe gắn máy, không cần bằng lái. Các mẫu giá dễ chịu:</p>'
                                    '<div class="the bang hd-in">%s<div class="chu-thich">Giá tham khảo cập nhật %s.</div></div></section>'
                                    % ("".join(hang.dong(m, "may") for m in _tg), noidung.NGAY_VN)) + noidung.CHIP_HANG.get("dap", "")
for _p in _vn["pages"]:
    _f = _p.get("body")
    if getattr(_f, "faqs", None):
        _k = {"/xe-may-dien/": "may", "/xe-dap-dien/": "dap"}.get(_p["url"])
        _p["schemas"] = [noidung.faq_ld_local(_f.faqs)] + (hang.schema_trang_loai(_k) if _k else [])
for _p in _vn["pages"]:
    _k = {"/xe-may-dien/": "may", "/xe-dap-dien/": "dap", "/xe-dien-3-banh/": "ba"}.get(_p["url"])
    if _k and not noidung.models_of(_k) and not noidung.THI_TRUONG.get(_k):
        _p["robots"] = "noindex,follow"  # chưa có mẫu trong bảng giá
# Ảnh xe thật (PXD_ANH): lưới thẻ xe trên trang chủ, bảng giá, trang loại xe

def _ban(ten):
    """Số phiên bản theo nội dung tệp, đổi tệp là trình duyệt tải lại (tránh khách thấy CSS cũ như 20/10 19:24)."""
    import hashlib
    return hashlib.md5(open(os.path.join(HERE, ten), "rb").read()).hexdigest()[:8]

_LUOI = {"/bang-gia-xe-dien/": (["may", "dap", "ba"], "Ảnh xe điện thật"),
         "/bang-gia-xe-50cc/": (["ga", "so"], "Ảnh xe 50cc thật"), "/gia-xe-50cc/": (["ga", "so"], "Ảnh xe 50cc thật"),
         "/xe-may-dien/": (["may"], "Ảnh xe máy điện thật"), "/xe-ga-50cc/": (["ga"], "Ảnh xe ga 50cc thật"), "/xe-so-50cc/": (["so"], "Ảnh xe số 50cc thật"),
         "/xe-ga-50cc-cho-hoc-sinh/": (["ga"], "Mẫu xe ga 50cc, ảnh thật"), "/xe-so-50cc-cho-hoc-sinh/": (["so"], "Mẫu xe số 50cc, ảnh thật"),
         "/xe-may-dien-cho-hoc-sinh/": (["may"], "Mẫu xe máy điện, ảnh thật"),
         "/xe-dap-dien/": (["dap"], "Mẫu xe đạp điện, ảnh thật"), "/xe-wave-50cc/": (["wave"], "Mẫu xe wave 50cc, ảnh thật"),
         "/xe-dien-3-banh/": (["ba"], "Mẫu xe điện 3 bánh, ảnh thật"), "/xe-dap-dien-cho-hoc-sinh/": (["dap"], "Mẫu xe đạp điện, ảnh thật")}


def _hop_so(keys):
    """Ô để lại số ngay dưới lưới xe: mục tiêu trang là khách để lại tên, số cho sale gọi (anh nhắc 21/10 11:08)."""
    ten = noidung.NHOM[keys[0]][0].lower()
    return ('<form class="tgp-lead tv-lead" data-tv-lead data-xe="%s" novalidate>'
            '<b class="tgp-lead-dau">Chưa chọn được mẫu %s ưng ý? Để lại số, Smile gọi tư vấn</b>'
            '<p class="tgp-lead-tom">Nhân viên gợi ý 2, 3 mẫu hợp chiều cao, quãng đường và tầm tiền của nhà mình, báo giá hôm nay và cách trả góp.</p>'
            '<label>Họ tên<input name="ten" autocomplete="name" maxlength="60" placeholder="Ví dụ: Nguyễn Văn An"></label>'
            '<label>Số điện thoại<input name="sdt" type="tel" inputmode="numeric" autocomplete="tel" maxlength="14" required placeholder="09xx xxx xxx"></label>'
            '<button class="btn btn-chinh" type="submit">Nhờ Smile gọi tư vấn</button>'
            '<p class="tgp-lead-kq" data-tv-kq aria-live="polite"></p>'
            '<p class="tgp-lead-rieng">Thông tin chỉ dùng để nhân viên Smile Motor gọi tư vấn cho bạn, không chia sẻ cho bên khác.</p></form>') % (html.escape(noidung.NHOM[keys[0]][0], quote=True), ten)


def _co_luoi(f, keys, tde):
    def g(s):
        b = f(s)
        ms = []
        for k in keys:
            ms += [m for m in noidung.models_of(k) if m not in ms and anhxe.anh(m.get("name"))]
            if k in noidung.NGUNG_BAN and not noidung.models_of(k):
                # xe Smile không bán (xe đạp điện, 3 bánh): mẫu giá thị trường có ảnh, ghi rõ giá thị trường
                ms += [m for m in noidung.THI_TRUONG.get(k, []) if anhxe.anh(m.get("name"))]
        # xen kẽ hãng để lưới không chỉ toàn một hãng
        theo = {}
        for m in ms:
            theo.setdefault(m.get("brand") or "", []).append(m)
        xen = []
        while any(theo.values()):
            for v in list(theo.values()):
                if v:
                    xen.append(v.pop(0))
        # 2 hàng x 6 xe ngay dưới phần giới thiệu, khách nhìn mẫu trước khi đọc bảng giá dài (anh góp ý 21/10 11:00)
        # chưa có ảnh xe thì vẫn để ô để lại số dưới phần giới thiệu
        l = anhxe.luoi(xen, tde, 12, noidung.vnd, lop="dau") + _hop_so(keys)
        m_chot = re.search(r'<section class="chot hd-in">.*?</section>', b, re.S)
        if m_chot:
            return b[:m_chot.end()] + l + b[m_chot.end():]
        moc = '<section><div class="the bang'
        if moc not in b:
            moc = '<section class="hd-in"><div class="keu">'
        return b.replace(moc, l + moc, 1) if moc in b else b + l
    return g


def _gan_luoi(site, ds):
    for p in site["pages"]:
        if p["url"] in ds and callable(p.get("body")):
            p["body"] = _co_luoi(p["body"], *ds[p["url"]])


_vn["pages"][-1:-1] = hang.trang_vn()
_comvn["pages"][-1:-1] = hang.trang_comvn()
_gan_luoi(_vn, _LUOI)
_gan_luoi(_comvn, _LUOI)
sanpham.gan(_vn, _comvn)   # trang riêng từng xe /xe/<slug>/
trangchu.gan(_vn, _comvn)  # trang chủ kiểu web bán xe
chinhsach.gan(_vn, _comvn)  # trang chính sách lấy từ xediensmile.com (PXD_KHO/chinh-sach)
trangphu.gan(_vn, _comvn, lambda s: stores_html(s), lambda s: (s['hot'].replace('.', ''), s['hot']))  # Tin tức, Liên hệ
import tragop  # noqa: E402
tragop.gan(_vn)  # trang Trả góp /tra-gop/ (21/10), số như máy tính xediensmile.com
tragop.gan(_comvn)  # 21/10 10:24 anh chốt: .com.vn cũng đổi nút Trang chủ thành Trả góp

# Banner chốt kiểu A (luồng Banner Phố Xe Điện, 20/10): tệp ở build/banner/<domain>/, alt theo HUONG-DAN-GAN.md
BANNER = {
    "phoxedien.vn": {
        "hero": "Bảng giá xe máy điện tháng 10/2026, giá tham khảo từ 10,99 triệu, xe 50cc từ 14,79 triệu",
        "dai": "Hỏi giá hôm nay: gọi hoặc Zalo 0889.277.112",
        "hero2": "Xe điện và xe 50cc đủ giá, đủ hãng: 121 mẫu xe máy điện, 31 mẫu xe 50cc, gọi hoặc Zalo 0889.277.112",
        # link từng banner trong slider (HUONG-DAN-GAN.md); trang chưa có thì banner gọi tel:
        "mac_dinh": "/so-sanh/",
        "link": ["/bang-gia-xe-dien/", "/bang-gia-xe-50cc/", "/so-sanh/", "/xe-cho-nu/chon-xe-dien-cho-nu/", "/xe-may-dien/"],
        "loai": {"/xe-may-dien/": ("banner-xe-may-dien.webp", "Bảng giá xe máy điện: 121 mẫu, giá tham khảo từ 10.990.000đ"),
                 "/bang-gia-xe-dien/": ("banner-xe-may-dien.webp", "Bảng giá xe máy điện: 121 mẫu, giá tham khảo từ 10.990.000đ"),
                 "/xe-ga-50cc/": ("banner-xe-ga-50cc.webp", "Bảng giá xe ga 50cc: 16 mẫu, giá tham khảo từ 14.990.000đ"),
                 "/xe-so-50cc/": ("banner-xe-so-50cc.webp", "Bảng giá xe số 50cc: 10 mẫu, giá tham khảo từ 14.790.000đ"),
                 "/bang-gia-xe-50cc/": ("banner-xe-cub-50cc.webp", "Bảng giá xe cub 50cc: 5 mẫu, giá tham khảo từ 16.990.000đ")}},
    "phoxedien.com.vn": {
        "hero": "Con vào lớp 10 nên đi xe gì? Cẩm nang chọn xe 50cc và xe điện cho phụ huynh",
        "dai": "Chưa chắc chọn xe nào? Gọi hoặc Zalo 0833.666.916",
        "hero2": "Đủ 16 tuổi được đi xe 50cc: cần giấy tờ gì, xe nào hợp với con",
        "mac_dinh": "/cam-nang/",
        "link": ["/hoc-sinh/chon-xe-cho-con-hoc-cap-3/", "/giay-to/16-tuoi-di-xe-50cc-can-giay-to-gi/", "/cam-nang/?muc=hoc-sinh", "/cam-nang/", "/sua-xe/xe-dien-khong-len-nguon/"],
        "loai": {"/xe-ga-50cc-cho-hoc-sinh/": ("banner-xe-ga-50cc.webp", "Xe ga 50cc cho học sinh, giá tham khảo từ 14.990.000đ"),
                 "/xe-so-50cc-cho-hoc-sinh/": ("banner-xe-so-50cc.webp", "Xe số 50cc cho học sinh, giá tham khảo từ 14.790.000đ"),
                 "/xe-may-dien-cho-hoc-sinh/": ("banner-xe-may-dien.webp", "Xe máy điện cho học sinh, giá tham khảo từ 10.990.000đ")}},
}
_MOC_KEU = '<section class="hd-in"><div class="keu">'
# Hero trang chủ (luồng banner 20/10 21:55, anh chốt): mỗi web banner riêng, banner hãng tối đa 2 slide, còn lại là banner mùa.
# Tệp banner-hero-<ten>-{may-tinh,dien-thoai}.webp trong build/banner/<domain>/. "hang": (hãng ảnh máy tính, hãng ảnh điện thoại),
# link về trang hãng (.vn) hoặc trang loại lọc ?hang= (.com.vn). "mua": (từ MM-DD, đến MM-DD), ngoài khoảng site.js gỡ slide.
HERO = {
    "phoxedien.vn": [
        # luồng banner 20/10 23:56: mỗi slide một mẫu xe, bấm vào là trang xe đó, chưa có trang xe thì về trang hãng
        {"ten": "hang-1", "xe_chinh": ("Velia E", "Detech"), "alt": "Espero: Velia E giá tham khảo 23.500.000đ"},
        {"ten": "20-10", "mua": ("10-13", "10-21"), "xe_chinh": ("Takashi Vibera", "DV Motor"), "alt": "Ngày Phụ nữ Việt Nam 20/10: DVMotor Takashi Vibera"},
        {"ten": "halloween", "mua": ("10-13", "10-31"), "xe_chinh": ("Takashi Pro 2026 (Bản AQ)", "DV Motor"), "alt": "Halloween: DVMotor Takashi Pro"},
        {"ten": "hang-2", "xe_chinh": ("Type 3", "Detech"), "alt": "Espero: Type 3"},
        {"ten": "11-11", "mua": ("10-13", "11-11"), "xe_chinh": ("Billy", "Detech"), "alt": "11/11: Detech Billy giá tham khảo 19.000.000đ"},
        {"ten": "20-11", "mua": ("10-13", "11-20"), "xe_chinh": ("Type 3 Pro", "Detech"), "alt": "Ngày Nhà giáo 20/11: Espero Type 3 Pro giá tham khảo 16.590.000đ"},
    ],
    "phoxedien.com.vn": [
        # luồng banner 21/10 10:47 (anh duyệt "Anh duyệt 2 bộ hero mới"): 5 tấm, mỗi tấm một xe, bấm mở trang xe
        {"ten": "hang-1", "xe_chinh": ("Cup 83", "Detech"), "alt": "Espero Cup 83 Retro X, xe số 50cc, giá tham khảo 18.500.000đ"},
        {"ten": "halloween", "mua": ("10-13", "10-31"), "xe_chinh": ("50C3He", "Detech"), "alt": "Halloween: Espero 50C3He giá tham khảo 14.790.000đ"},
        {"ten": "hang-2", "xe_chinh": ("50VS Diamond Plus", "Detech"), "alt": "50VS Diamond Plus, xe ga 50cc, giá tham khảo 22.190.000đ"},
        {"ten": "11-11", "mua": ("10-13", "11-11"), "xe_chinh": ("Weezee Plus 3", "Detech"), "alt": "11/11: Espero Weezee Plus 3, xe máy điện"},
        {"ten": "20-11", "mua": ("10-13", "11-20"), "xe_chinh": ("50C2a-2", "Detech"), "alt": "Ngày Nhà giáo 20/11: Espero 50C2a-2 giá tham khảo 15.000.000đ"},
    ],
}


def _xe_slide(site, sl):
    """Xe hiện trong ô thông tin khi bấm điểm sáng trên banner: xe nêu tên trong slide, hoặc vài mẫu có ảnh của hãng."""
    ms = [m for m in noidung.MODELS if m.get("name")]
    if site["domain"] == "phoxedien.com.vn":
        ms = [m for m in ms if "dv motor" not in (m.get("brand") or "").lower()]
    ra = []
    for t in sl.get("xe", []) + ([sl["xe_chinh"][0]] if sl.get("xe_chinh") else []):
        t = t.lower()
        hop = [m for m in ms if all(w in m["name"].lower().split() for w in t.split()) and anhxe.anh(m["name"])]
        if hop:
            ra.append(min(hop, key=lambda m: len(m["name"])))
    if sl.get("hang"):
        for b in dict.fromkeys(sl["hang"]):
            k = hang.slug(b).replace("-", "")
            cua = [m for m in ms if hang.slug(m.get("brand") or "").replace("-", "") == k and anhxe.anh(m["name"])]
            cua.sort(key=lambda m: (m.get("price") is None, m.get("price") or 0))
            ra += cua[:2 if sl["hang"][0] != sl["hang"][1] else 3]
    return ra[:3]


def _the_slide(site, sl, ds):
    o = []
    for m in ds:
        u = anhxe.url_xe(m["name"])
        g = noidung.vnd(m["price"]) if m.get("price") else "Liên hệ"
        t = html.escape(m["name"], quote=True)
        o.append('<div class="tp-xe"><img src="%s" alt="%s" width="120" height="120" loading="lazy"><div><b>%s</b><span>%s</span>'
                 '<div class="tp-nut">%s<button type="button" class="hoi-gia dat-xe" data-chat="Mình muốn %s xe %s">%s</button></div></div></div>'
                 % (anhxe.anh(m["name"]), t, html.escape(m["name"]), g, ('<a href="%s">Xem xe</a>' % u) if u else "",
                    "đặt" if m.get("price") else "hỏi giá", t, "Đặt xe" if m.get("price") else "Hỏi giá"))
    tieu = "Xe %s" % " và ".join(dict.fromkeys(sl["hang"])) if sl.get("hang") else ("Xe trong banner")
    return '<template class="tr-tpl"><b class="tp-tieu">%s</b>%s</template>' % (html.escape(tieu), "".join(o))


def _link_xe(site, ten):
    """Trang /xe/<slug>/ của mẫu có tên chứa đủ các chữ trong ten; nhiều mẫu khớp thì lấy tên ngắn nhất (Type 3 chứ không phải Type 3 Pro)."""
    tu = ten.lower().split()
    hop = [n for n in anhxe.SP.get(site["domain"], ()) if all(t in n.split() for t in tu)]
    # "Type 3" không nhảy sang bản Pro/Plus/Max khi còn bản thường
    phu = {"pro", "plus", "max", "s"} - set(tu)
    hop.sort(key=lambda n: (bool(phu & set(n.split())), len(n)))
    return "/xe/%s/" % anhxe._slug(hop[0]) if hop else None


def _link_hang(site, ten):
    """Trang của hãng trên web: .vn /<loai>/<hang>/, .com.vn trang loại có hãng đó kèm ?hang=."""
    k = hang.slug(ten).replace("-", "")
    if site["domain"] == "phoxedien.vn":
        ds = [p["url"] for p in site["pages"] if p["url"].count("/") == 3 and p["url"].split("/")[2].replace("-", "") == k]
        ds.sort(key=lambda u: not u.startswith("/xe-may-dien/"))
        return ds[0] if ds else None
    for kk, (url, _) in hang.LOAI_COMVN.items():
        for b in hang.hang_cua(kk):
            if hang.slug(b).replace("-", "") == k and "dv motor" not in b.lower():
                return "%s?hang=%s" % (url, hang.slug(b))
    return None


def _so(site):
    return site["hot"].replace(".", "")


def _dai(site, bo2=False):
    # Bộ 2 chạy xen kẽ (anh chốt 10:59): trang chủ dùng bộ 1, cuối trang danh mục dùng bộ 2
    # dải gọi mở khung chat tư vấn ngay trên trang (anh không muốn bấm banner bị nhảy qua Zalo)
    return ('<a class="banner-dai" href="#chat" data-chat><img src="/banner/banner-dai-goi%s.webp" width="1080" height="360" alt="%s" loading="lazy"></a>'
            % ("-2" if bo2 else "", html.escape(BANNER[site["domain"]]["dai"])))


def _co_url(site):
    return {p["url"] for p in site["pages"]} | {a["url"] for a in site["articles"]} | {a.get("cat_url") for a in site["articles"]}


def _truot(site, bn):
    """Hero trang chủ chạy cuộn theo HERO[domain]; slide thiếu tệp thì bỏ qua."""
    tm = os.path.join(HERE, "banner", site["domain"])
    co = _co_url(site)
    o = []
    for sl in HERO.get(site["domain"], []):
        mt = sl.get("mt") or "banner-hero-%s-may-tinh.webp" % sl["ten"]
        dt = sl.get("dt") or "banner-hero-%s-dien-thoai.webp" % sl["ten"]
        if not os.path.isfile(os.path.join(tm, mt)):
            continue
        if not os.path.isfile(os.path.join(tm, dt)):
            dt = mt
        u, u_dt = sl.get("link"), None
        if sl.get("xe_chinh"):
            ten_xe, ten_hang = sl["xe_chinh"]
            u = _link_xe(site, ten_xe) or _link_hang(site, ten_hang)
            alt = sl["alt"]
        elif sl.get("hang"):
            h1, h2 = sl["hang"]
            u, u_dt = _link_hang(site, h1), _link_hang(site, h2)
            u = u or u_dt
            u_dt = u_dt if u_dt and u_dt != u else None
            alt = "Xe %s chính hãng tại Smile Motor" % (h1 if h1 == h2 else "%s và %s" % (h1, h2))
        else:
            alt = sl["alt"]
        # anh chốt 20/10 19:10: bấm banner là vào bài viết, không gọi điện, không Zalo; trang chưa có thì về trang danh mục chính
        if not u or u.split("?")[0] not in co:
            u = bn["mac_dinh"]
        mua = sl.get("mua")
        v = lambda t: _ban(os.path.join("banner", site["domain"], t))  # ảnh banner thay cùng tên thì khách vẫn thấy bản mới
        ds = _xe_slide(site, sl)
        # điểm sáng nhấp nháy trên xe: bấm ra ô thông tin xe, giá, nút đặt (anh muốn banner tương tác được, 20/10 23:33)
        diem = ('<button type="button" class="tr-diem" style="--x:%s;--y:%s;--xm:%s;--ym:%s" aria-label="Xem thông tin xe trong banner"><i></i></button>%s'
                % (sl.get("x", "70%"), sl.get("y", "56%"), sl.get("xm", "52%"), sl.get("ym", "64%"), _the_slide(site, sl, ds))) if ds else ""
        o.append('<div class="tr-o"%s><a class="tr-lk" href="%s"%s><picture><source media="(max-width:767px)" srcset="/banner/%s?v=%s" width="1080" height="1200">'
                 '<img src="/banner/%s?v=%s" width="1920" height="720" alt="%s"%s></picture></a>%s</div>'
                 % (' data-mua="%s,%s"' % mua if mua else "", u, ' data-href-dt="%s"' % u_dt if u_dt else "",
                    dt, v(dt), mt, v(mt), html.escape(alt), ' fetchpriority="high"' if not o else ' loading="lazy"', diem))
    if len(o) < 2:
        return '<div class="banner-dau">%s</div>' % "".join(o)
    cham = "".join('<button type="button" aria-label="Banner %d"%s></button>' % (i + 1, ' aria-current="true"' if not i else "") for i in range(len(o)))
    # mũi tên nhỏ hai bên để khách tự lướt, vẫn tự chuyển 5 giây (anh chốt 20/10 19:26)
    mui = ('<button type="button" class="tr-mui tr-lui" aria-label="Banner trước"><svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></button>'
           '<button type="button" class="tr-mui tr-toi" aria-label="Banner sau"><svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></button>')
    return ('<div class="banner-dau truot" aria-roledescription="carousel" aria-label="Banner"><div class="tr-khung"><div class="tr-ray">%s</div>%s'
            '<div class="tr-pop" hidden><button type="button" class="tp-dong" aria-label="Đóng">×</button><div class="tp-than"></div></div></div>'
            '<div class="tr-cham">%s</div></div>' % ("".join(o), mui, cham))


def _gan_banner(site):
    bn = BANNER.get(site["domain"])
    if not bn or not os.path.isdir(os.path.join(HERE, "banner", site["domain"])):
        return
    for p in site["pages"]:
        f = p.get("body")
        if not callable(f):
            continue
        if p["url"] == "/":
            def g(s, f=f, bn=bn):
                # dựng lúc render: lúc này mới có bài viết và ảnh khung theo từng web
                # trang chủ đã có khối tư vấn cuối trang, không thêm dải gọi để khỏi lặp 2 khối tối liền nhau
                return _truot(site, bn) + f(s)
            p["body"] = g
        elif p["url"] in bn["loai"]:
            tep, alt = bn["loai"][p["url"]]
            if list(bn["loai"]).index(p["url"]) % 2:  # xen kẽ theo trang: trang thứ chẵn dùng bộ 2
                tep = tep.replace(".webp", "-2.webp")
            anh = '<img class="banner-loai" src="/banner/%s" width="1080" height="540" alt="%s" loading="lazy">' % (tep, html.escape(alt))

            def g(s, f=f, anh=anh):
                b = f(s)
                moc = '<div class="dau-trang">'
                b = b.replace(moc, anh + moc, 1) if moc in b else anh + b
                return b.replace(_MOC_KEU, _dai(site, True) + _MOC_KEU, 1) if _MOC_KEU in b else b
            p["body"] = g



# Video YouTube của Smile (anh chốt 20/10 19:50: xe 3 bánh không bán vẫn đánh từ khoá, kéo traffic từ video Smile).
# Danh sách ở PXD_KHO/video.csv, cột: chu_de (vd 3-banh), youtube_id, tieu_de. Máy nhà điền, build tự gắn.
VIDEO = {}
_fv = os.path.join(os.environ.get("PXD_KHO", "").strip(), "video.csv") if os.environ.get("PXD_KHO", "").strip() else ""
if _fv and os.path.isfile(_fv):
    import csv as _csv
    for _r in _csv.DictReader(open(_fv, encoding="utf-8-sig", newline="")):
        _id = (_r.get("youtube_id") or "").strip()
        if _id and all(c.isalnum() or c in "-_" for c in _id):
            VIDEO.setdefault((_r.get("chu_de") or "").strip(), []).append((_id, (_r.get("tieu_de") or "").strip()))
# trang nào gắn video chủ đề nào; bài Muse có tiêu đề chứa từ khoá cũng được gắn
VIDEO_TRANG = {"/xe-dien-3-banh/": "3-banh"}
VIDEO_TU = {"3-banh": "3 bánh"}


def video_html(cd, toi_da=4):
    ds = VIDEO.get(cd, [])[:toi_da]
    if not ds:
        return ""
    o = "".join('<button type="button" class="vd" data-yt="%s" aria-label="Xem video %s"><img src="https://i.ytimg.com/vi/%s/hqdefault.jpg" alt="%s" width="480" height="360" loading="lazy"><span class="vd-nut"></span><b>%s</b></button>'
                % (i, html.escape(t, quote=True), i, html.escape(t, quote=True), html.escape(t)) for i, t in ds)
    return '<section class="hd-in"><div class="tieude"><h2>Video thực tế</h2></div><div class="luoi-vd">%s</div></section>' % o


def video_cho(url, tieu_de=""):
    cd = VIDEO_TRANG.get(url) or next((c for c, tu in VIDEO_TU.items() if tu in (tieu_de or "").lower()), None)
    return video_html(cd) if cd else ""


def _gan_video(site):
    for p in site["pages"]:
        if p["url"] in VIDEO_TRANG and callable(p.get("body")):
            def g(s, f=p["body"], u=p["url"]):
                b, v = f(s), video_cho(u)
                return b.replace(_MOC_KEU, v + _MOC_KEU, 1) if (v and _MOC_KEU in b) else b + v
            p["body"] = g


_gan_video(_vn)
_gan_video(_comvn)

_gan_banner(_vn)
_gan_banner(_comvn)

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


def _ban_do(x):
    from urllib.parse import quote
    return "https://maps.google.com/maps?q=%s&z=16&output=embed" % quote("%s, %s" % (x.get("name", ""), x.get("address", "")))


def stores_html(site):
    """Cửa hàng ở chân trang: danh sách bên trái, bản đồ Google bên phải; bấm cửa hàng nào bản đồ chuyển sang đó (anh góp ý 20/10 23:32)."""
    st = site.get("stores") or []
    if not st:
        return ""
    li = "".join('<li><button type="button" class="ch-o%s" data-map="%s"><b>%s</b><span>%s</span></button>%s</li>'
                 % (" on" if not i else "", html.escape(_ban_do(x), quote=True), html.escape(x.get("name", "")), html.escape(x.get("address", "")),
                    ('<a class="ch-di" href="%s" target="_blank" rel="noopener nofollow">Chỉ đường</a>' % html.escape(x["map"], quote=True)) if x.get("map") else "")
                 for i, x in enumerate(st))
    return ('<div class="cua-hang"><h3>Cửa hàng Smile Motor · mở cửa 8h–21h</h3><div class="ch-luoi"><ul>%s</ul>'
            '<div class="ch-map"><iframe src="%s" title="Bản đồ cửa hàng Smile Motor" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div></div></div>'
            % (li, html.escape(_ban_do(st[0]), quote=True)))


# Nền tia điện chạy mờ sau chân trang (anh góp ý 21/10 1:18): vẽ SVG nhẹ, chạy bằng CSS, tắt khi người dùng giảm chuyển động
_TIA = ["M40 0 L120 90 L80 110 L170 220 L130 240 L210 400", "M1180 0 L1090 80 L1130 105 L1030 210 L1075 235 L980 400",
        "M560 0 L610 70 L585 85 L650 170 L620 185 L690 290", "M300 400 L360 310 L330 295 L410 200 L380 185 L450 110",
        "M860 400 L900 320 L875 305 L940 230 L915 215 L990 130"]
TIA_DIEN = ('<div class="chan-dien" aria-hidden="true"><svg viewBox="0 0 1200 400" preserveAspectRatio="none">'
            + "".join('<g class="tia t%d"><path d="%s" class="quang"/><path d="%s" class="loi"/></g>' % (i, d, d) for i, d in enumerate(_TIA))
            + '</svg></div>')

LOGO_OG = "/logo-1200.png"


def co_logo(site):
    """Logo chốt 20/10 (A10 cho .vn, B7 cho .com.vn), tệp ở build/logo/<domain>/."""
    return os.path.isfile(os.path.join(HERE, "logo", site["domain"], "logo.svg"))


def icon_head(site):
    if not co_logo(site):
        return '<link rel="icon" href="/favicon.svg" type="image/svg+xml">'
    return ('<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" href="/favicon.svg" type="image/svg+xml">'
            '<link rel="icon" href="/icon-32.png" sizes="32x32" type="image/png"><link rel="icon" href="/icon-16.png" sizes="16x16" type="image/png">'
            '<link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/manifest.webmanifest">')


def logo_html(site, ten, dau):
    if not co_logo(site):
        return ('<a class="logo" href="/" aria-label="%s - trang chủ">%s<span><b>%s</b><small>%s</small></span></a>' % (site["sitename"], site["icon"], ten, site["tagline"])
                if dau else '<a class="logo" href="/">%s<span><b>%s</b><small>%s</small></span></a>' % (site["icon"], ten, site["tagline"]))
    if os.path.isfile(os.path.join(HERE, "logo", site["domain"], "logo-nen-toi.svg")):  # đầu trang, chân trang nền tối (M5 .com.vn)
        return '<a class="logo logo-anh toi" href="/"><img src="/logo-nen-toi.svg" alt="%s" height="52"></a>' % html.escape(site["sitename"])
    return '<a class="logo logo-anh%s" href="/"><img src="/logo.svg" alt="%s" height="52"></a>' % ("" if dau else " chan", html.escape(site["sitename"]))


def og_img_html(site, src):
    if not src:
        return ""
    return ('<meta property="og:image" content="https://%s%s">' % (site["domain"], src) +
            '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="675">')


def muse_page(site, a, src):
    """Bài Muse đã đạt soát: giữ nguyên đoạn <article> Khung A, thêm đường dẫn, ảnh bìa, bài liên quan."""
    au = site["authors"][a["author"]]
    d = site["domain"]
    ngay = a["ngay"] or NGAY
    crumbs = [("Trang chủ", "/"), (a["cat_name"], a["cat_url"]), (a["h1"], a["url"])]
    art = {"@context": "https://schema.org", "@type": "Article", "headline": a["h1"], "description": a["desc"],
           "datePublished": ngay, "dateModified": ngay, "inLanguage": "vi",
           "author": {"@type": "Person", "name": au["name"], "url": "https://%s/tac-gia/%s/" % (d, a["author"])},
           "publisher": {"@type": "Organization", "name": "Phố Xe Điện", "logo": {"@type": "ImageObject", "url": "https://%s/logo.svg" % d}},
           "mainEntityOfPage": "https://%s%s" % (d, a["url"])}
    if src:
        art["image"] = "https://%s%s" % (d, src)
    sch = [art] + ([faq_ld(a["faq"])] if a["faq"] else [])
    bai = a["html"]
    if src:
        img = '<img class="anh-bia" src="%s" width="1200" height="675" alt="%s" loading="eager" fetchpriority="high">' % (src, html.escape(a["anh_alt"]))
        bai = bai.replace("</h1>", "</h1>" + img, 1) if "</h1>" in bai else img + bai
    rel = "".join(f'<a class="bai-nho" href="{r["url"]}">{noidung.o_bai(r)}<div><div class="muc">{r["cat_name"]}</div><h3>{r["h1"]}</h3><div class="meta">{r["read"]} phút đọc</div></div></a>'
                  for r in ([x for x in site["articles"] if x["cat_url"] == a["cat_url"] and x["url"] != a["url"]] or [x for x in site["articles"] if x["url"] != a["url"]])[:6])
    body = f'''<div class="wrap doc">
<div class="duong"><a href="/">Trang chủ</a> › <a href="{a['cat_url']}">{a['cat_name']}</a> › <b>{html.escape(a['crumb'])}</b></div>
{bai}
{anhxe.luoi(anhxe.lien_quan(a['html'], noidung.MODELS), "Mẫu xe nhắc trong bài", 4, noidung.vnd)}
{video_cho(a["url"], a["h1"])}
{'<section class="hd-in"><div class="tieude"><h2>Bài liên quan</h2></div>%s</section>' % rel if rel else ''}
</div>'''
    return page(site, a["url"], a["title"], a["desc"], body, sch, crumbs, og_img=src)


def _hang_menu(site, u):
    """Các hãng của một loại xe cho menu: .vn mở trang hãng; .com.vn mở trang loại lọc sẵn theo hãng (không DV Motor)."""
    vn = site["domain"] == "phoxedien.vn"
    loai = {uu: k for k, (uu, _) in (hang.LOAI_VN if vn else hang.LOAI_COMVN).items()}
    k = loai.get(u)
    if not k:
        return []
    if vn:
        return [(b, "%s%s/" % (u, hang.slug(b))) for b in hang.hang_cua(k)] if k != "wave" else []
    dem = {}
    for m in noidung.models_of(k):
        b = (m.get("brand") or "").strip()
        if b and "dv motor" not in b.lower():
            dem[b] = dem.get(b, 0) + 1
    return [(b, "%s?hang=%s" % (u, hang.slug(b))) for b, _ in sorted(dem.items(), key=lambda x: -x[1])]


def _menu(site):
    """Menu điện thoại: bấm loại xe thì xổ ra các hãng (anh chốt 20/10 19:28)."""
    o = []
    for n, u in site["menu"]:
        hs = _hang_menu(site, u)
        if hs:
            o.append('<details class="mn"><summary>%s</summary><div class="mn-hang"><a href="%s">Tất cả %s</a>%s</div></details>'
                     % (n, u, n.lower(), "".join('<a href="%s">%s</a>' % (h, html.escape(b)) for b, h in hs)))
        else:
            o.append('<a href="%s">%s</a>' % (u, n))
    return "".join(o)


def _nav(site, path):
    """Thanh menu máy tính trong đầu trang; loại xe rê chuột ra danh sách hãng."""
    o = []
    for n, u in site.get("nav", []):
        on = ' aria-current="page"' if (path == u or (u != "/" and path.startswith(u))) else ""
        hs = _hang_menu(site, u)[:14]
        if hs:
            o.append('<div class="nv-o"><a href="%s"%s>%s<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></a><div class="nv-hang">%s</div></div>'
                     % (u, on, n, "".join('<a href="%s">%s</a>' % (h, html.escape(b)) for b, h in hs)))
        else:
            o.append('<div class="nv-o"><a href="%s"%s>%s</a></div>' % (u, on, n))
    return '<nav class="nav-dau" aria-label="Danh mục chính">%s</nav>' % "".join(o)


def _nav_nho(site, path):
    """Điện thoại: menu chính hiện thẳng thành dải lướt ngang dưới đầu trang, không giấu trong nút ba gạch (anh góp ý 20/10 23:57)."""
    o = []
    for n, u in site.get("nav", []):
        on = ' aria-current="page"' if (path == u or (u != "/" and path.startswith(u))) else ""
        o.append('<a href="%s"%s>%s</a>' % (u, on, n))
    return '<nav class="nav-nho" aria-label="Danh mục">%s</nav>' % "".join(o)


def page(site, path, title, desc, body, schemas=(), crumbs=None, robots="index,follow", og_img=None):
    d = site["domain"]
    css_vars = ";".join("--%s:%s" % kv for kv in site["vars"].items())
    menu = _menu(site)
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
                 '<link rel="stylesheet" href="/skin-%s.css?v=%s">' % (skin, _ban("skin-%s.css" % skin))) if skin else ""
    ten = site.get("logo_ten", "PHỐ <i>XE ĐIỆN</i>")
    goi_dau = ('<a class="nut-goi" href="tel:%s" aria-label="Gọi %s"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg></a>' % (TEL, HOTLINE)) if skin else ""
    if skin:
        day = f'''<div class="day dock">
<button class="hoi" data-chat><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>Hỏi</button>
<a class="zalo" href="https://zalo.me/{TEL}" target="_blank" rel="noopener nofollow"><span class="zl">{mxh.icon("zalo")}</span>Zalo</a>
<a class="goi" href="tel:{TEL}">Gọi tư vấn<small>{HOTLINE} · 8h–21h</small></a>
</div>'''
    else:
        day = f'''<div class="day">
<a class="goi" href="tel:{TEL}"><i></i>Gọi tư vấn</a>
<a class="zalo" href="https://zalo.me/{TEL}" target="_blank" rel="noopener nofollow"><span class="zl">{mxh.icon("zalo")}</span>Zalo</a>
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
{og_img_html(site, og_img or (LOGO_OG if co_logo(site) else None))}
{icon_head(site)}
{FONT}
<link rel="stylesheet" href="/site.css?v={_ban("site.css")}">
{skin_head}
<style>:root{{{css_vars}}}</style>
{sch}
</head>
<body{' class="skin-%s"' % skin if skin else ""}>
<header class="top"><div class="wrap wide">
{logo_html(site, ten, True)}
{_nav(site, path)}
<span class="dau-phai"><a class="goi-dai" href="tel:{site['hot'].replace('.', '')}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg><span><small>Hotline</small>{site['hot']}</span></a>{goi_dau}<button class="nut-menu" aria-label="Mở menu" aria-expanded="false"><span></span></button></span>
</div></header>
{_nav_nho(site, path)}
<nav class="ngan-menu" aria-label="Menu">{menu}<div class="nho">Gọi tư vấn: <a href="tel:{TEL}" style="display:inline;padding:0;border:0;color:inherit">{HOTLINE}</a></div></nav>
<main>
{body}
</main>
<footer>{TIA_DIEN}<div class="wrap wide">
<div class="chan-luoi">
<div class="chan-cot chan-gt">{logo_html(site, ten, False)}
<p>{site['footer']}</p>
<p>Mở cửa 8h–21h mỗi ngày. Gọi hoặc Zalo <a href="tel:{site['hot'].replace('.', '')}">{site['hot']}</a> để được tư vấn ngay.</p>
{chinhsach.cong_ty_html()}
{mxh.hang(site["hot"], "mxh-chan")}</div>
<div class="chan-cot"><h3>Danh mục</h3><nav>{"".join('<a href="%s">%s</a>' % (u, n) for n, u in site['foot'])}<a href="/tin-tuc/">Tin tức</a><a href="/lien-he/">Liên hệ</a></nav></div>
{('<div class="chan-cot"><h3>Chính sách</h3><nav>%s</nav></div>' % "".join('<a href="%s">%s</a>' % (u, n) for n, u in chinhsach.link_chan())) if chinhsach.link_chan() else ""}
{('<div class="chan-cot chan-tg">%s</div>' % mxh.tra_gop("tg-chan")) if mxh.tra_gop() else ""}
</div>
{stores_html(site)}
<div class="chan-cuoi">© 2026 {html.escape(chinhsach.cong_ty().get("ten") or "Xe Điện Smile")} · {site['domain']}</div>
</div></footer>
{day}
<div class="chat" role="dialog" aria-label="Chat tư vấn" aria-hidden="true">
<div class="chat-dau"><span class="chat-av">{site['bot'][0]}</span><div><b>{site['bot']}</b><small><i></i>Tư vấn Xe điện Smile · {site['hot']}</small></div><button class="chat-dong" aria-label="Đóng">×</button></div>
<div class="chat-than" aria-live="polite"></div>
<div class="chat-goi"></div>
<form class="chat-o"><input type="text" placeholder="Nhắn câu hỏi hoặc số điện thoại..." aria-label="Câu hỏi" maxlength="300"><button aria-label="Gửi">➤</button></form>
</div>
<script>window.PXD={{stores:{json.dumps([x.get('name','')+': '+x.get('address','') for x in site.get('stores') or []], ensure_ascii=False)},tel:"{TEL}",hot:"{HOTLINE}",web:"{site['chat']}",bot:"{site['bot']}"}}</script>
<script src="/site.js?v={_ban("site.js")}" defer></script>
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
    rel = "".join(f'<a class="bai-nho" href="{r["url"]}">{noidung.o_bai(r)}<div><div class="muc">{r["cat_name"]}</div><h3>{r["h1"]}</h3><div class="meta">{r["read"]} phút đọc</div></div></a>'
                  for r in site["articles"] if r["url"] != a["url"])[:4000]
    body = f'''<div class="wrap doc">
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
{anhxe.luoi(anhxe.lien_quan(a['body'] + a['h1'], noidung.MODELS), "Mẫu xe nhắc trong bài", 4, noidung.vnd)}
{keu(site['cta_title'], site['cta_text'])}
<section class="hd-in"><div class="tieude"><h2>Bài liên quan</h2></div>{rel}</section>
</div>'''
    return page(site, a["url"], a["title"], a["desc"], body, sch, crumbs)


def author_page(site, slug):
    au = site["authors"][slug]
    lst = "".join(f'<a class="bai-nho" href="{r["url"]}">{noidung.o_bai(r)}<div><div class="muc">{r["cat_name"]}</div><h3>{r["h1"]}</h3><div class="meta">{r["read"]} phút đọc</div></div></a>'
                  for r in site["articles"] if r["author"] == slug) or '<p class="meta">Bài của %s sẽ sớm có ở đây.</p>' % au["name"]
    url = "/tac-gia/%s/" % slug
    body = f'''<div class="wrap"><div class="duong"><a href="/">Trang chủ</a> › <b>Tác giả</b></div>
<div class="dau-trang"><h1>{au['name']}</h1></div>
<div class="noi-dung"><p>{au['bio']}</p></div>
<section><div class="tieude"><h2>Bài của {au['name']}</h2></div>{lst}</section></div>'''
    sch = [{"@context": "https://schema.org", "@type": "ProfilePage", "mainEntity": {"@type": "Person", "name": au["name"], "description": au["bio"]}}]
    return page(site, url, "%s, tác giả Phố Xe Điện" % au["name"], "%s, Phố Xe Điện. %s" % (au["name"], au["bio"]), body, sch,
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
    os.makedirs(os.path.join(base, "loai"), exist_ok=True)
    for k in noidung.NHOM:
        if trangchu.anh_loai(k):
            shutil.copy(trangchu.anh_loai(k), os.path.join(base, "loai", k + ".webp"))
    danhgia.chep(site, base)
    tiktok.chep(site, base)
    mxh.chep(base)
    bannerhang.chep(d, base)
    if os.path.isdir(os.path.join(HERE, "banner", d)):
        shutil.copytree(os.path.join(HERE, "banner", d), os.path.join(base, "banner"))
    import tragop
    tragop.chep(base)
    os.makedirs(os.path.join(base, "api"))
    shutil.copy(os.path.join(HERE, "lien-he.php"), os.path.join(base, "api"))
    open(os.path.join(base, ".htaccess"), "w").write(HTACCESS)
    for fn, svg in (("logo.svg", site["logo_svg"]), ("favicon.svg", site["favicon"])):
        open(os.path.join(base, fn), "w").write(svg)
    if co_logo(site):
        for fn in os.listdir(os.path.join(HERE, "logo", d)):
            shutil.copy(os.path.join(HERE, "logo", d, fn), base)
        open(os.path.join(base, "manifest.webmanifest"), "w", encoding="utf-8").write(json.dumps({
            "name": site["sitename"], "short_name": "Phố Xe Điện", "start_url": "/", "display": "browser", "theme_color": site["theme"],
            "background_color": "#ffffff", "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
                                                    {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False))
    anhxe.WEB = d
    anhxe.chep(base)
    urls, lastmod = [], {}
    bai_muse = muse.doc_bai(site)
    # bài Muse viết cho một mẫu xe (meta "san_pham") ghép vào trang /xe/<slug>/, không thành bài riêng
    for a in [a for a in bai_muse if a.get("san_pham")]:
        sanpham.MUSE[d][a["san_pham"].strip().lower()] = a
    bai_muse = [a for a in bai_muse if not a.get("san_pham")]
    site["articles"][:0] = bai_muse  # sửa tại chỗ để trang chủ, chuyên mục (đọc BAI_VN/BAI_COMVN) thấy bài mới
    for a in bai_muse:
        write(site, a["url"], muse_page(site, a, muse.chep_anh(a, base)))
        urls.append(a["url"])
        lastmod[a["url"]] = a["ngay"] or NGAY
    for p in site["pages"]:
        write(site, p["url"], page(site, p["url"], p["title"], p["desc"], p["body"](site), p.get("schemas", []), p.get("crumbs"), p.get("robots", "index,follow")))
        if p.get("robots", "index,follow").startswith("index"):
            urls.append(p["url"])
    for a in site["articles"]:
        if a.get("muse"):
            continue
        write(site, a["url"], article_page(site, a))
        urls.append(a["url"])
    for slug in site["authors"]:
        write(site, "/tac-gia/%s/" % slug, author_page(site, slug))
        urls.append("/tac-gia/%s/" % slug)
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        "<url><loc>https://%s%s</loc><lastmod>%s</lastmod></url>\n" % (d, u, lastmod.get(u, NGAY)) for u in urls) + "</urlset>\n"
    open(os.path.join(base, "sitemap.xml"), "w").write(sm)
    open(os.path.join(base, "robots.txt"), "w").write("User-agent: *\nAllow: /\n\nSitemap: https://%s/sitemap.xml\n" % d)
    print(d, len(urls), "trang,", len(bai_muse), "bài Muse")


for s in SITES:
    build(s)
