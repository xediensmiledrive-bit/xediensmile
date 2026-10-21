# -*- coding: utf-8 -*-
"""Nội dung chốt đơn cho các trang banner dẫn tới trên phoxedien.vn (anh chốt 21/10 0:07: "bài dynamic content, dynamic keyword,
nhồi từ khoá, văn hoa mỹ, chạm người đọc, đây là đoạn chuyển đổi").
Luật: không bịa số liệu, giá và thông số luôn đọc từ bảng giá; chỉ dùng điều Smile công bố (6 cửa hàng, 10 năm, bảo hành phụ tùng 7 năm, 8h–21h).
Phần dài nằm trong khối .chot-dai, mặc định thu gọn, có nút "Đọc tiếp" (anh không muốn trang dài, 21/10 0:08)."""
import html

import mxh

HOT = "0889.277.112"


def _nut(ten_xe=None, hot=HOT):
    so = hot.replace(".", "")
    hoi = html.escape("Mình muốn hỏi giá và màu còn hàng của %s" % ten_xe if ten_xe else "Mình muốn được tư vấn chọn xe", quote=True)
    return ('<div class="chot-nut"><button type="button" class="btn btn-chinh" data-chat="%s">Nhận tư vấn ngay</button>'
            '<a class="btn btn-phu" href="tel:%s">Gọi %s</a><a class="btn btn-phu btn-zalo" href="https://zalo.me/%s" target="_blank" rel="noopener nofollow">%sZalo</a></div>%s'
            % (hoi, so, hot, so, mxh.icon("zalo"), mxh.tra_gop()))


def _tin():
    return ('<ul class="chot-tin"><li><b>6 cửa hàng Smile</b> TP.HCM, Đồng Tháp, Phan Thiết</li>'
            '<li><b>10 năm</b> bán và sửa xe điện</li><li><b>Bảo hành phụ tùng 7 năm</b></li>'
            '<li><b>Xe chính hãng</b>, ảnh thật</li></ul>')


def khoi(tieu, mo, dai, ten_xe=None):
    """Khối chốt đơn: đoạn mở chạm cảm xúc + lý do tin Smile + nút; phần dài thu gọn có nút Đọc tiếp."""
    return ('<section class="chot hd-in"><h2>%s</h2>%s%s%s%s</section>'
            % (tieu, "".join("<p>%s</p>" % p for p in mo), _tin(), _nut(ten_xe),
               ('<div class="chot-dai">%s</div><button type="button" class="doc-tiep">Đọc tiếp</button>' % dai) if dai else ""))


# ---------- Trang loại xe ----------
LOAI = {
    "may": ("Xe máy điện: êm như một hơi thở, nhẹ như một lời hứa",
            ["Có những buổi sáng, chỉ cần vặn tay ga là chiếc <b>xe máy điện</b> lướt đi không một tiếng nổ, không mùi xăng, không khói bụi. Con đến trường đúng giờ, mẹ đi chợ thong thả, bố đi làm mà ví vẫn dày. Đó là lý do mỗi tháng có thêm nhiều gia đình tìm đến <b>Xe Điện Smile</b> để chọn chiếc <b>xe máy điện chính hãng</b> đầu tiên của mình.",
             "Bảng <b>giá xe máy điện</b> bên dưới là giá tháng này tại <b>Smile</b>, có ảnh thật từng mẫu. Bạn chỉ cần lướt, chọn chiếc vừa mắt, phần còn lại để Smile lo."],
            '''<h3>Chọn xe máy điện theo người cầm lái</h3>
<p><b>Xe máy điện cho học sinh:</b> con từ đủ 16 tuổi đi được <b>xe máy điện không cần bằng lái</b> (loại xe gắn máy, công suất đến 4 kW, tốc độ thiết kế đến 50 km/h). Chọn xe nhẹ, yên vừa tầm, phanh đĩa trước để bố mẹ yên lòng mỗi sáng con dắt xe ra cổng.</p>
<p><b>Xe máy điện cho nữ:</b> dáng thon, màu pastel, sàn để chân rộng, cốp đủ chỗ cho áo mưa và túi xách. Một chiếc xe đẹp không chỉ để đi, mà để mỗi lần dừng đèn đỏ là một lần thấy mình xinh hơn.</p>
<p><b>Xe máy điện đi làm:</b> ưu tiên pin lithium, quãng đường mỗi lần sạc đủ cho cả đi và về, đèn LED sáng cho những tối tan ca muộn.</p>
<p><b>Xe máy điện cho người lớn tuổi:</b> xe thấp, nhẹ, có số lùi, phanh êm. Ông bà đi chợ, đi chùa nhẹ nhàng như đi bộ.</p>
<h3>Từ lúc bước vào Smile đến lúc lăn bánh</h3>
<p>Bạn được ngồi thử, chạy thử, hỏi tới khi thật hiểu chiếc xe. Nhân viên Smile kiểm tra xe, sạc pin, hướng dẫn cách sạc đúng để pin bền, rồi bàn giao kèm sổ bảo hành. Sau này xe cần chăm sóc, bạn ghé bất kỳ cửa hàng nào trong 6 cửa hàng Smile.</p>
<p>Chưa chắc chọn mẫu nào? Nhắn Smile một dòng: bạn cao bao nhiêu, đi bao xa mỗi ngày, ngân sách tầm nào. Bạn sẽ nhận lại 2–3 mẫu vừa vặn nhất, không vòng vo.</p>'''),
    "dap": ("Xe đạp điện: đôi cánh nhỏ cho những ngày đến trường",
            ["Tuổi học trò chỉ đến một lần. Một chiếc <b>xe đạp điện</b> nhẹ nhàng, an toàn, không cần biển số sẽ cùng con qua những con đường đến lớp, những buổi học thêm tối muộn, những lần ghé nhà bạn làm bài nhóm.",
             "<b>Giá xe đạp điện</b> tháng này tại <b>Xe Điện Smile</b> nằm ngay bên dưới, mỗi mẫu đều có ảnh thật để bố mẹ và con cùng chọn."],
            '''<h3>Bố mẹ nên nhìn gì trước khi mua xe đạp điện cho con</h3>
<p>Cho con ngồi thử: hai mũi chân chạm đất là vừa. Con tự dắt, tự dựng chân chống được là xe không quá nặng. Bóp phanh thử: xe dừng chắc, không rít. Hỏi rõ pin lithium hay ắc quy chì và thời gian bảo hành.</p>
<p>Ở Smile, con được chạy thử trong sân cửa hàng, bố mẹ được hướng dẫn cách sạc để pin bền, và mỗi lần xe cần chăm sóc đã có 6 cửa hàng Smile ở gần.</p>'''),
    "ga": ("Xe ga 50cc: tự do tuổi 16, không cần bằng lái",
           ["Ngày con tròn 16 tuổi cũng là ngày con muốn tự đi. Một chiếc <b>xe ga 50cc</b> nhỏ gọn, tự động, không cần sang số, không cần bằng lái là món quà vừa đủ lớn để con trưởng thành, vừa đủ an toàn để bố mẹ yên tâm.",
            "<b>Giá xe ga 50cc</b> tháng này tại <b>Smile</b> có ngay bên dưới, kèm ảnh thật từng mẫu."],
           '''<h3>Chọn xe ga 50cc cho con</h3>
<p>Ưu tiên phanh đĩa trước, yên vừa tầm chân, cốp đủ cho áo mưa và cặp. Màu xe để con chọn, vì chiếc xe con yêu là chiếc xe con giữ gìn.</p>
<p>Xe ga 50cc vẫn phải đăng ký biển số, con đi đường mang theo đăng ký xe, bảo hiểm và căn cước. Smile hướng dẫn đủ giấy tờ ngay khi bàn giao.</p>'''),
    "so": ("Xe số 50cc: bền bỉ, tiết kiệm, đi đâu cũng tới",
           ["Có những chiếc xe không cần ồn ào để được yêu. <b>Xe số 50cc</b> nhẹ, rẻ, ít hỏng vặt, đổ xăng một lần đi cả tuần, là người bạn đồng hành quen thuộc của học sinh từ đủ 16 tuổi và người đi làm gần.",
            "<b>Giá xe số 50cc</b> tháng này tại <b>Smile</b> có ngay bên dưới, mỗi mẫu đều có ảnh thật."],
           '''<h3>Vì sao nhiều gia đình chọn xe số 50cc</h3>
<p>Số tròn, không côn tay, con tập vài buổi là quen. Phụ tùng dễ tìm, sửa nhanh. Không cần bằng lái theo luật hiện hành, chỉ cần đăng ký biển số.</p>
<p>Đến Smile, con được ngồi thử, nhân viên chỉnh tay phanh, gương cho vừa tầm, hướng dẫn chăm xe để xe chạy êm nhiều năm.</p>'''),
}


def loai(k):
    if k not in LOAI:
        return ""
    t, mo, dai = LOAI[k]
    return khoi(t, mo, dai)


# ---------- Trang hãng ----------
HANG = {
    "dv-motor": "Dòng <b>DV Motor Takashi</b> mang dáng xe ga hiện đại, nhiều phiên bản pin và màu sắc, là cái tên được hỏi nhiều tại Smile.",
    "detech": "<b>Detech Espero</b> là dòng xe quen mặt trên phố, nhiều kiểu dáng từ thanh lịch đến cá tính, giá dễ tiếp cận.",
}


def hang(b, ten_loai, slug_hang):
    ten = html.escape(b)
    them = HANG.get(slug_hang, "")
    mo = ["Mỗi chiếc <b>%s %s</b> trong bảng dưới đây đều là xe chính hãng, có ảnh thật và giá tháng này tại <b>Xe Điện Smile</b>. %s" % (ten_loai.lower(), ten, them),
          "Bạn thích mẫu nào, nhắn Smile để biết màu còn hàng, quà tặng trong tháng và cửa hàng gần nhất. Một tin nhắn, một chiếc xe đúng ý."]
    dai = ('<h3>Mua %s %s ở đâu yên tâm?</h3><p>Smile có 6 cửa hàng ở TP.HCM, Đồng Tháp và Phan Thiết. Bạn được xem xe tận tay, chạy thử, '
           'được hướng dẫn sạc pin hoặc chăm máy đúng cách, và có chỗ quen để quay lại mỗi lần xe cần bảo dưỡng.</p>'
           '<p>Giá trên trang là giá xe, chưa gồm lệ phí trước bạ, biển số và bảo hiểm. Nhân viên Smile tính sẵn tổng tiền lăn bánh để bạn không bất ngờ.</p>') % (ten_loai.lower(), ten)
    return khoi("Chọn %s %s tại Smile" % (ten_loai.lower(), ten), mo, dai)


# ---------- Trang xe trên banner trang chủ ----------
# khớp theo chữ trong tên mẫu (chữ thường); câu chữ không nêu thông số, thông số nằm ở bảng bên cạnh
XE = [
    (("velia", "e"), "Espero Velia E: thanh lịch từ cái nhìn đầu tiên",
     ["Có những chiếc xe chỉ cần dựng trước cửa là đủ khiến người đi ngang ngoái nhìn. <b>Espero Velia E</b> mang dáng xe ga thanh thoát, đường nét mềm mại, hợp với người thích sự chỉn chu mỗi ngày đi làm, đi học.",
      "Đến <b>Xe Điện Smile</b> để ngồi lên Velia E, cảm nhận tay lái, yên xe và chọn màu bạn thích nhất."]),
    (("takashi", "vibera"), "DVMotor Takashi Vibera: món quà cho người phụ nữ bạn thương",
     ["Có món quà nào dịu dàng hơn một chiếc xe để người ấy tự do đi đến nơi mình muốn? <b>Takashi Vibera</b> của <b>DV Motor</b> là mẫu xe ga điện dáng đẹp, êm ái, dễ điều khiển, hợp để tặng mẹ, tặng vợ, tặng người yêu.",
      "Ghé <b>Smile</b> để xem Vibera tận tay, chọn màu và nhận tư vấn quà tặng trong tháng."]),
    (("takashi", "pro"), "DVMotor Takashi Pro: mạnh mẽ cho những hành trình dài",
     ["Người đi làm xa cần một chiếc xe khoẻ, bền, sẵn sàng mỗi sáng. <b>Takashi Pro</b> của <b>DV Motor</b> là phiên bản dành cho người cần nhiều hơn từ chiếc xe điện của mình.",
      "Xem Takashi Pro tại <b>Xe Điện Smile</b>, chạy thử và hỏi nhân viên về quãng đường thực tế khi đi hằng ngày."]),
    (("type", "3"), "Espero Type 3: gọn gàng, cá tính, đi đâu cũng hợp",
     ["<b>Espero Type 3</b> có dáng gọn, dễ dắt, dễ đỗ, hợp với phố đông và những con hẻm nhỏ. Một chiếc xe để mỗi ngày đi học, đi làm đều nhẹ nhõm.",
      "Đến <b>Smile</b> để ngồi thử Type 3 và chọn phiên bản vừa nhu cầu."]),
    (("billy",), "Detech Billy: nhỏ xinh, đáng yêu, đi phố nhẹ tênh",
     ["<b>Detech Billy</b> là kiểu xe nhỏ nhắn khiến người ta mỉm cười khi nhìn thấy. Nhẹ, dễ điều khiển, hợp với bạn trẻ và người mới tập đi xe điện.",
      "Ghé <b>Xe Điện Smile</b> để xem Billy tận tay và chọn màu bạn yêu."]),
    (("type", "3", "pro"), "Espero Type 3 Pro: món quà tri ân thầy cô, món quà cho chính mình",
     ["<b>Espero Type 3 Pro</b> là phiên bản nâng cấp của Type 3, cho người muốn chiếc xe gọn gàng nhưng đầy đủ hơn. Một món quà ý nghĩa dịp 20/11, hoặc phần thưởng cho chính bạn sau một năm cố gắng.",
      "Đến <b>Smile</b> để chạy thử Type 3 Pro và nhận tư vấn ưu đãi trong tháng."]),
]


def xe(ten):
    # khớp cụm chữ liền nhau: "takashi pro" không khớp "takashi money pro"; "type 3 pro" thắng "type 3"
    t0 = " %s " % " ".join((ten or "").lower().replace("-", " ").split())
    hop = [x for x in XE if " %s " % " ".join(x[0]) in t0]
    if not hop:
        return ""
    k, t, mo = max(hop, key=lambda x: len(x[0]))
    return khoi(t, mo, "", ten)


# ---------- Trang so sánh ----------
SO_SANH = khoi("So sánh để chọn đúng, chọn một lần dùng thật lâu",
               ["Mua xe là chuyện của nhiều năm. Các bài so sánh dưới đây đặt từng mẫu <b>xe máy điện</b>, <b>xe 50cc</b> cạnh nhau theo giá, pin, quãng đường và điểm yếu, để bạn biết mỗi đồng chênh lệch đi đâu.",
                "Đọc xong vẫn phân vân? Nhắn <b>Xe Điện Smile</b>, nhân viên so giúp đúng hai mẫu bạn đang cân nhắc."], "")
