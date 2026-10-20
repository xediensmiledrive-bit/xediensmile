# -*- coding: utf-8 -*-
"""Banner chính hãng trên trang hãng (luồng banner gửi 20/10, anh duyệt): giữ logo hãng, không gắn logo mình,
giữ đúng tỉ lệ gốc, không cắt. Tệp ở build/banner-hang/<domain>/banner-<hang>-<so>.webp.
.vn: trang hãng /<loai>/<hang>/. .com.vn: không có trang hãng, banner hiện khi lọc ?hang= trên trang loại.
.com.vn không dùng banner DV Motor (luật cứng: không thêm nội dung DV Motor trên .com.vn)."""
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))


def _kich_thuoc(f):
    """Rộng, cao của ảnh webp đọc từ đầu tệp (máy nhà có thể không có PIL)."""
    b = open(f, "rb").read(30)
    if b[12:16] == b"VP8X":
        return 1 + int.from_bytes(b[24:27], "little"), 1 + int.from_bytes(b[27:30], "little")
    if b[12:16] == b"VP8 ":
        w, h = struct.unpack("<HH", b[26:30])
        return w & 0x3FFF, h & 0x3FFF
    if b[12:16] == b"VP8L":
        v = int.from_bytes(b[21:25], "little")
        return (v & 0x3FFF) + 1, ((v >> 14) & 0x3FFF) + 1
    return 1600, 900


def khoa(ten_hang):
    import hang
    return hang.slug(ten_hang).replace("-", "")


def tep(domain, ten_hang):
    tm = os.path.join(HERE, "banner-hang", domain)
    if not os.path.isdir(tm):
        return []
    k = khoa(ten_hang)
    if domain == "phoxedien.com.vn" and k == "dvmotor":
        return []
    return sorted(f for f in os.listdir(tm) if f.startswith("banner-%s-" % k) and f.endswith(".webp"))


def html(domain, ten_hang, an=False):
    ds = tep(domain, ten_hang)
    if not ds:
        return ""
    tm = os.path.join(HERE, "banner-hang", domain)
    o = []
    for i, f in enumerate(ds):
        w, h = _kich_thuoc(os.path.join(tm, f))
        o.append('<div class="bh"><img src="/banner-hang/%s" alt="Banner %s chính hãng" width="%d" height="%d"%s></div>'
                 % (f, ten_hang, w, h, "" if i == 0 and not an else ' loading="lazy"'))
    mui = ('<button type="button" class="bh-mui bh-lui" aria-label="Ảnh trước"><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg></button>'
           '<button type="button" class="bh-mui bh-toi" aria-label="Ảnh sau"><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></button>'
           '<span class="bh-so">1/%d</span>' % len(ds)) if len(ds) > 1 else ""
    import hang
    return '<div class="banner-hang" data-hang="%s"%s><div class="bh-ray">%s</div>%s</div>' % (hang.slug(ten_hang), " hidden" if an else "", "".join(o), mui)


def chep(domain, base):
    tm = os.path.join(HERE, "banner-hang", domain)
    if os.path.isdir(tm):
        os.makedirs(os.path.join(base, "banner-hang"), exist_ok=True)
        for f in os.listdir(tm):
            if f.endswith(".webp"):
                import shutil
                shutil.copy(os.path.join(tm, f), os.path.join(base, "banner-hang"))
