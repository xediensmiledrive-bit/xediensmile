# -*- coding: utf-8 -*-
"""Bài mở màn cho 2 web. Mỗi bài theo đúng giọng người viết trong luật cứng."""


def h(i, t):
    return '<h2 id="m%d">%s</h2>' % (i, t)


# =====================================================================
# phoxedien.vn
# =====================================================================
BAI_VN = [
{
"url": "/so-sanh/pin-lithium-hay-ac-quy-chi/", "author": "minh-trang", "read": 6, "emoji": "🔋", "funnel": "Giữa phễu",
"cat_name": "So sánh", "cat_url": "/so-sanh/", "crumb": "Pin lithium hay ắc quy chì",
"title": "Pin lithium hay ắc quy chì: xe điện nên chọn loại nào? (2026)",
"desc": "So sánh pin lithium và ắc quy chì trên xe điện theo 6 tiêu chí: giá, cân nặng, độ bền, sạc, an toàn và chi phí thay. Khi nào đáng bỏ thêm tiền.",
"h1": "Pin lithium hay ắc quy chì: chọn loại nào cho xe điện?",
"quick": ["Lithium: nhẹ hơn, bền hơn, sạc nhanh hơn, nhưng giá xe cao hơn.",
          "Ắc quy chì: rẻ, dễ thay, nhưng nặng và xuống nhanh nếu sạc sai.",
          "Đi nhiều mỗi ngày, định giữ xe lâu: chọn lithium. Đi ít, ngân sách chặt: ắc quy chì vẫn ổn."],
"toc": ["Khác nhau ở đâu", "So theo 6 tiêu chí", "Tính tiền dài hạn", "Nên chọn loại nào"],
"body": h(1, "Khác nhau ở đâu") + """
<p>Cùng một dáng xe, hãng thường bán hai bản: bản <b>ắc quy chì</b> (thường là 4 đến 6 bình 12V mắc nối tiếp) và bản <b>pin lithium</b> (một khối pin gồm nhiều cell nhỏ, có mạch quản lý pin gọi là BMS). Hai loại cùng cấp điện cho động cơ, nhưng khác nhau về khối lượng, cách sạc và tuổi thọ, nên giá xe chênh nhau rõ.</p>
""" + h(2, "So theo 6 tiêu chí") + """
<div class="cuon-bang"><table><tr><th>Tiêu chí</th><th>Pin lithium</th><th>Ắc quy chì</th></tr>
<tr><td>Giá mua</td><td>Cao hơn</td><td>Thấp hơn</td></tr>
<tr><td>Cân nặng</td><td>Nhẹ hơn nhiều, xe dễ dắt</td><td>Nặng, mỗi bình vài ký</td></tr>
<tr><td>Số lần sạc trước khi chai</td><td>Thường cao hơn nhiều, tuỳ loại cell</td><td>Thường thấp hơn, xuống nhanh nếu để cạn</td></tr>
<tr><td>Sạc</td><td>Sạc nhanh hơn, sạc lúc còn nửa pin không sao</td><td>Nên sạc đầy, tránh để cạn lâu</td></tr>
<tr><td>An toàn</td><td>Cần sạc đúng bộ sạc, tránh va đập, ngâm nước</td><td>Ít rủi ro cháy, nhưng có axit</td></tr>
<tr><td>Thay thế</td><td>Thay cả khối, giá cao</td><td>Thay từng bình được, dễ tìm</td></tr></table></div>
<p class="luu-y">Số lần sạc cụ thể phụ thuộc loại cell và cách dùng. Hỏi rõ hãng công bố bao nhiêu và bảo hành pin bao lâu trước khi mua.</p>
<div class="hai-cot"><div class="cong"><b>Điểm cộng lithium</b>Nhẹ, bền, sạc linh hoạt, xe gọn hơn.</div><div class="tru"><b>Điểm trừ lithium</b>Giá cao; hỏng pin thì thay cả khối.</div></div>
""" + h(3, "Tính tiền dài hạn") + """
<p>Đừng chỉ so giá lúc mua. Hãy tính: <b>tiền chênh lúc mua</b> so với <b>số lần phải thay pin</b> trong thời gian bạn định giữ xe. Nếu bạn giữ xe 4 đến 5 năm và đi mỗi ngày, bản ắc quy chì có thể phải thay bình ít nhất một lần, trong khi bản lithium thường chưa phải thay. Nếu bạn chỉ đi vài km mỗi ngày, mức hao mòn thấp, khoản chênh này nhỏ đi.</p>
<p>Giá thay pin, thay bình của từng mẫu ở mỗi thời điểm khác nhau. Xem giá xe hiện tại trong <a href="/bang-gia-xe-dien/">bảng giá xe điện</a>.</p>
""" + h(4, "Nên chọn loại nào") + """
<ul><li><b>Chọn lithium</b> khi: đi trên 20 km mỗi ngày, ở chung cư phải dắt xe nhiều, định giữ xe lâu.</li>
<li><b>Chọn ắc quy chì</b> khi: ngân sách chặt, đi quãng ngắn, có chỗ để xe và sạc ngay tầng trệt.</li></ul>
""",
"faq": [("Pin lithium có dễ cháy không?", "Pin lithium có mạch BMS bảo vệ. Rủi ro tăng khi dùng sạc không đúng, pin bị va đập mạnh, phồng hoặc ngấm nước. Dùng đúng bộ sạc theo xe và không sạc qua đêm ở nơi kín là đủ an toàn cho đa số trường hợp."),
        ("Xe đang dùng ắc quy chì có nâng lên lithium được không?", "Nhiều xe làm được nhưng phải đổi cả bộ sạc và kiểm tra điện áp, chỗ đặt pin. Nên làm ở nơi có kỹ thuật và bảo hành, không tự lắp."),
        ("Ắc quy chì bao lâu phải thay?", "Tuỳ cách sạc và quãng đường mỗi ngày. Dấu hiệu cần thay là xe đi được quãng ngắn hơn hẳn lúc mới dù đã sạc đầy.")],
},
{
"url": "/so-sanh/xe-ga-50cc-hay-xe-so-50cc/", "author": "minh-trang", "read": 5, "emoji": "🛵", "funnel": "Giữa phễu",
"cat_name": "So sánh", "cat_url": "/so-sanh/", "crumb": "Xe ga 50cc hay xe số 50cc",
"title": "Xe ga 50cc hay xe số 50cc: so sánh để chọn đúng (2026)",
"desc": "So sánh xe ga 50cc và xe số 50cc: giá, cân nặng, tiện dụng, tiêu hao xăng, sửa chữa. Hợp với ai, tránh mua nhầm.",
"h1": "Xe ga 50cc hay xe số 50cc: chọn loại nào?",
"quick": ["Xe ga: không phải sang số, có cốp, hợp bạn nữ và người mới đi.",
          "Xe số (wave, cub): rẻ hơn, nhẹ hơn, bền, sửa rẻ.",
          "Cả hai đều là xe gắn máy, người đủ 16 tuổi đi được, không cần bằng lái."],
"toc": ["Đặt cạnh nhau", "Xe ga 50cc hợp ai", "Xe số 50cc hợp ai", "Câu hỏi trước khi chốt"],
"body": h(1, "Đặt cạnh nhau") + """
<div class="cuon-bang"><table><tr><th>Tiêu chí</th><th>Xe ga 50cc</th><th>Xe số 50cc</th></tr>
<tr><td>Giá</td><td>Thường cao hơn</td><td>Thường thấp hơn</td></tr>
<tr><td>Cách đi</td><td>Vặn ga là chạy, không sang số</td><td>Phải sang số bằng chân</td></tr>
<tr><td>Cốp, chỗ để đồ</td><td>Có cốp dưới yên, sàn để chân</td><td>Ít chỗ, thường chỉ có giỏ</td></tr>
<tr><td>Cân nặng</td><td>Nặng hơn</td><td>Nhẹ, dễ dắt</td></tr>
<tr><td>Xăng</td><td>Thường hao hơn chút</td><td>Thường tiết kiệm hơn</td></tr>
<tr><td>Sửa chữa</td><td>Bộ truyền động dây đai cần thay định kỳ</td><td>Đơn giản, thợ nào cũng sửa được</td></tr></table></div>
""" + h(2, "Xe ga 50cc hợp ai") + """
<p>Bạn nữ, học sinh mới tập đi, người đi phố đông phải dừng liên tục. Không sang số nên đỡ mỏi, cốp đựng được mũ bảo hiểm và áo mưa. Điểm yếu: nặng hơn, khi dắt lên dốc hay vào nhà sẽ vất vả hơn với người nhỏ con.</p>
""" + h(3, "Xe số 50cc hợp ai") + """
<p>Người cần xe rẻ, bền, đi đường xa hoặc đường xấu, muốn sửa ở đâu cũng được. Wave và cub 50cc nhẹ, dáng thấp, dễ chống chân. Điểm yếu: phải quen sang số, không có cốp.</p>
""" + h(4, "Câu hỏi trước khi chốt") + """
<ol><li>Người đi có chống được hai chân khi ngồi lên xe không?</li><li>Có tự dắt, tự dựng chân chống được không?</li><li>Phanh trước là phanh đĩa hay phanh cơ?</li><li>Bảo hành bao lâu, phụ tùng có sẵn gần nhà không?</li></ol>
<p>Xem giá từng nhóm trong <a href="/bang-gia-xe-50cc/">bảng giá xe 50cc tháng này</a>.</p>
""",
"faq": [("Xe ga 50cc có cần bằng lái không?", "Không. Xe ga hay xe số dưới 50cc, tốc độ thiết kế đến 50 km/h đều là xe gắn máy, không cần bằng lái. Người đi phải từ đủ 16 tuổi."),
        ("Xe số 50cc có chở được 2 người không?", "Được, nhưng xe 50cc yếu hơn xe 110cc nên chở 2 người lên dốc sẽ chậm. Nên đi chậm và giữ khoảng cách phanh xa hơn."),
        ("Học sinh nữ nên đi xe ga hay xe số?", "Phần lớn bạn nữ mới đi chọn xe ga vì dễ đi. Nếu bạn nhỏ người, chọn mẫu ga yên thấp hoặc cub 50cc để chống chân vững.")],
},
{
"url": "/bang-gia/gia-lan-banh-xe-may-dien-xe-50cc/", "author": "kha-uyen", "read": 5, "emoji": "🧾", "funnel": "Đáy phễu",
"cat_name": "Bảng giá", "cat_url": "/bang-gia-xe-dien/", "crumb": "Giá lăn bánh",
"title": "Giá lăn bánh xe máy điện, xe 50cc gồm những khoản nào? (2026)",
"desc": "Giá lăn bánh = giá xe + lệ phí trước bạ + lệ phí biển số + bảo hiểm bắt buộc. Cách tính từng khoản theo văn bản đang hiệu lực.",
"h1": "Giá lăn bánh xe máy điện, xe 50cc gồm những khoản nào?",
"quick": ["Giá lăn bánh = giá xe + lệ phí trước bạ + lệ phí đăng ký, biển số + bảo hiểm TNDS bắt buộc.",
          "Lệ phí trước bạ xe máy lần đầu: 2% giá tính lệ phí; 5% ở thành phố trực thuộc trung ương, thành phố thuộc tỉnh, thị xã nơi đặt trụ sở UBND tỉnh.",
          "Xe đạp điện không phải đăng ký, nên không có các khoản này."],
"toc": ["Bốn khoản cần cộng", "Lệ phí trước bạ", "Lệ phí đăng ký, biển số", "Bảo hiểm bắt buộc", "Mẹo để khỏi bị bất ngờ"],
"body": h(1, "Bốn khoản cần cộng") + """
<p>Uyên tóm lại một dòng: <b>giá lăn bánh = giá xe + lệ phí trước bạ + lệ phí đăng ký, cấp biển số + bảo hiểm trách nhiệm dân sự bắt buộc</b>. Giá xe bạn xem trong <a href="/bang-gia-xe-dien/">bảng giá xe điện</a> và <a href="/bang-gia-xe-50cc/">bảng giá xe 50cc</a>; ba khoản còn lại tính như bên dưới.</p>
""" + h(2, "Lệ phí trước bạ") + """
<p>Theo Nghị định 10/2022/NĐ-CP, xe máy (gồm xe máy điện, xe 50cc) nộp lệ phí trước bạ lần đầu <b>2%</b>. Nếu chủ xe đăng ký ở thành phố trực thuộc trung ương, thành phố thuộc tỉnh, hoặc thị xã nơi UBND tỉnh đặt trụ sở thì mức là <b>5%</b>. Số tiền tính trên giá tính lệ phí trước bạ do Bộ Tài chính ban hành cho từng mẫu xe, không hẳn bằng giá bạn mua.</p>
""" + h(3, "Lệ phí đăng ký, biển số") + """
<p>Lệ phí cấp đăng ký và biển số xe máy theo Thông tư 60/2023/TT-BTC, chia theo khu vực (khu vực I gồm Hà Nội, TP.HCM có mức cao nhất) và theo giá trị xe. Bạn hỏi Smile mức cụ thể theo nơi đăng ký khi chốt xe.</p>
""" + h(4, "Bảo hiểm bắt buộc") + """
<p>Mọi xe máy, xe gắn máy tham gia giao thông phải có bảo hiểm trách nhiệm dân sự của chủ xe cơ giới (Nghị định 67/2023/NĐ-CP). Đây là khoản nhỏ nhất trong bốn khoản, mua theo năm.</p>
""" + h(5, "Mẹo để khỏi bị bất ngờ") + """
<ul><li>Hỏi người bán báo <b>giá lăn bánh trọn gói</b> theo đúng nơi bạn đăng ký.</li><li>Hỏi khuyến mãi có hỗ trợ trước bạ hoặc biển số không.</li><li>Mua trả góp thì hỏi tổng số tiền phải trả, không chỉ tiền mỗi tháng.</li></ul>
""",
"faq": [("Xe đạp điện có phải đóng lệ phí trước bạ không?", "Không. Xe đạp điện không phải đăng ký, gắn biển số nên không có lệ phí trước bạ và lệ phí biển số."),
        ("Lệ phí trước bạ tính trên giá mua xe à?", "Tính trên giá tính lệ phí trước bạ theo bảng giá của Bộ Tài chính cho từng mẫu, có thể khác giá bạn mua thực tế."),
        ("Đăng ký xe ở quê có rẻ hơn ở thành phố không?", "Thường rẻ hơn: lệ phí trước bạ 2% thay vì 5%, và lệ phí biển số ở khu vực ngoài Hà Nội, TP.HCM thấp hơn. Xe phải đăng ký theo nơi cư trú của chủ xe.")],
},
{
"url": "/xe-cho-nu/chon-xe-dien-cho-nu/", "author": "anh-ngoc", "read": 4, "emoji": "🎀", "funnel": "Đầu phễu",
"cat_name": "Xe cho nữ", "cat_url": "/so-sanh/", "crumb": "Chọn xe điện cho nữ",
"title": "Chọn xe điện cho nữ: 5 thứ nhìn trước khi nhìn màu (2026)",
"desc": "Chọn xe máy điện, xe đạp điện cho bạn nữ: chiều cao yên, cân nặng, cốp, màu và giá. Mẹo thử xe trong 2 phút.",
"h1": "Chọn xe điện cho nữ: 5 thứ nhìn trước khi nhìn màu",
"quick": ["Ngồi lên chống được hai chân là điều đầu tiên.",
          "Xe nhẹ, có cốp vừa mũ bảo hiểm, sàn để chân phẳng.",
          "Màu đẹp thì chọn sau, sau khi xe vừa người."],
"toc": ["Chiều cao yên", "Cân nặng xe", "Cốp và sàn để chân", "Pin và chỗ sạc", "Màu và dáng"],
"body": h(1, "Chiều cao yên") + """
<p>Ngọc thử xe kiểu này: ngồi lên, hai bàn chân phải chạm đất, đầu gối hơi chùng. Nhón mũi chân mới chạm là xe hơi cao, dừng đèn đỏ sẽ dễ chao.</p>
""" + h(2, "Cân nặng xe") + """
<p>Bạn phải tự dắt xe ra vào nhà, lên dốc hầm gửi xe. Thử dắt một vòng và dựng chân chống giữa ngay tại cửa hàng. Thấy nặng là nên xem bản pin lithium, nhẹ hơn hẳn bản ắc quy (đọc <a href="/so-sanh/pin-lithium-hay-ac-quy-chi/">so sánh hai loại pin</a>).</p>
""" + h(3, "Cốp và sàn để chân") + """
<p>Cốp vừa một mũ bảo hiểm nửa đầu và áo mưa là đủ dùng hằng ngày. Sàn để chân phẳng giúp đi váy, để túi đồ thoải mái.</p>
""" + h(4, "Pin và chỗ sạc") + """
<p>Ở chung cư hay phòng trọ không sạc tại chỗ để xe được thì ưu tiên xe có pin rút ra mang lên nhà sạc.</p>
""" + h(5, "Màu và dáng") + """
<p>Giờ mới tới phần vui: các màu pastel, kem, xanh bạc hà và đen nhám đang được hỏi nhiều. Chọn màu bạn thích, nhưng nhớ màu sáng dễ thấy vết bẩn hơn. Xem giá các mẫu trong <a href="/bang-gia-xe-dien/">bảng giá xe điện</a>.</p>
""",
"faq": [("Bạn nữ cao 1m50 nên đi xe gì?", "Chọn xe có yên thấp, dáng nhỏ, hoặc xe đạp điện. Thử ngồi và chống chân trước khi mua."),
        ("Xe điện cho nữ có cần bằng lái không?", "Xe máy điện công suất đến 4 kW, tốc độ đến 50 km/h là xe gắn máy, không cần bằng lái. Mẫu mạnh hơn cần bằng A1."),
        ("Màu xe có ảnh hưởng giá không?", "Thường không. Một số bản màu đặc biệt có thể giá khác; hỏi khi đặt xe.")],
},
]

# =====================================================================
# phoxedien.com.vn
# =====================================================================
BAI_COMVN = [
{
"url": "/hoc-sinh/chon-xe-cho-con-hoc-cap-3/", "author": "thu-ha", "read": 7, "emoji": "🎒", "funnel": "Đầu phễu", "muc": "hoc-sinh",
"cat_name": "Xe cho học sinh", "cat_url": "/cam-nang/?muc=hoc-sinh", "crumb": "Chọn xe cho con học cấp 3",
"title": "Con vào lớp 10 nên đi xe gì? Cách chọn xe cho con tuổi cấp 3 (2026)",
"desc": "Mẹ nên mua xe gì cho con lớp 10: xe 50cc hay xe điện, tuổi được đi, giấy tờ, chọn xe an toàn và chi phí nuôi xe mỗi tháng.",
"h1": "Con vào lớp 10 nên đi xe gì? Cách chọn xe cho con tuổi cấp 3",
"quick": ["Con đủ 16 tuổi: đi được xe dưới 50cc hoặc xe máy điện đến 4 kW, không cần bằng lái.",
          "Con chưa đủ 16 tuổi: xe đạp hoặc xe đạp điện.",
          "Chọn xe con chống được hai chân, tự dắt được, có phanh tốt; mua mũ bảo hiểm đạt chuẩn."],
"toc": ["Hỏi luật trước, hỏi giá sau", "Xe 50cc hay xe điện", "Sáu điều mẹ nên thử", "Chi phí nuôi xe", "Dặn con trước khi đi"],
"body": h(1, "Hỏi luật trước, hỏi giá sau") + """
<p>Con mình vào lớp 10, câu đầu tiên mình hỏi không phải giá mà là: con đi xe này có đúng luật không. Theo Luật Trật tự, an toàn giao thông đường bộ 2024 (hiệu lực từ 01/01/2025), người <b>đủ 16 tuổi</b> được điều khiển <b>xe gắn máy</b>: xe có tốc độ thiết kế đến 50 km/h, dùng động cơ xăng dưới 50 cm³ hoặc động cơ điện đến 4 kW. Nhiều bạn lớp 10 chưa tròn 16 tuổi, mẹ nên xem kỹ ngày sinh của con. Giấy tờ cần có, Châu viết riêng ở bài <a href="/giay-to/16-tuoi-di-xe-50cc-can-giay-to-gi/">16 tuổi đi xe 50cc cần giấy tờ gì</a>.</p>
""" + h(2, "Xe 50cc hay xe điện") + """
<div class="cuon-bang"><table><tr><th></th><th>Xe 50cc (xăng)</th><th>Xe máy điện</th></tr>
<tr><td>Đi hằng ngày</td><td>Đổ xăng vài phút là xong</td><td>Sạc ở nhà, mất vài giờ</td></tr>
<tr><td>Quãng đường</td><td>Đi xa không lo</td><td>Đủ cho đi học trong phố, cần sạc đều</td></tr>
<tr><td>Tiếng ồn, mùi</td><td>Có</td><td>Êm, không khói</td></tr>
<tr><td>Bảo dưỡng</td><td>Thay nhớt, bugi định kỳ</td><td>Ít hạng mục, nhưng có chi phí thay pin sau vài năm</td></tr></table></div>
<p>Nhà gần trường, có chỗ sạc: xe điện tiện và êm. Nhà xa, hay đi học thêm nhiều nơi: xe 50cc đỡ lo hết pin giữa đường.</p>
<p class="luu-y">Lưu ý: xe máy điện công suất trên 4 kW hoặc chạy nhanh hơn 50 km/h là xe mô tô, cần bằng A1 và người lái đủ 18 tuổi. Hỏi rõ thông số khi mua.</p>
""" + h(3, "Sáu điều mẹ nên thử") + """
<ol><li><b>Con chống được hai chân</b> khi ngồi trên xe.</li><li><b>Con tự dắt và dựng chân chống</b> được.</li><li><b>Phanh:</b> bóp thử, xe dừng chắc; ưu tiên phanh đĩa trước.</li><li><b>Đèn, còi, xi nhan</b> sáng rõ.</li><li><b>Gương</b> đủ hai bên.</li><li><b>Mũ bảo hiểm</b> có tem hợp quy theo QCVN 2:2021/BKHCN, vừa đầu con, cài quai chắc.</li></ol>
""" + h(4, "Chi phí nuôi xe") + """
<p>Ngoài giá xe và lệ phí khi đăng ký, mẹ tính thêm: tiền xăng hoặc tiền điện mỗi tháng, gửi xe ở trường, bảo hiểm bắt buộc mỗi năm, bảo dưỡng định kỳ. Với xe điện, nhớ để dành một khoản cho lần thay pin. Giá xe tháng này ở trang <a href="/gia-xe-50cc/">giá xe 50cc và xe điện cho học sinh</a>.</p>
""" + h(5, "Dặn con trước khi đi") + """
<ul><li>Không chở quá một người, không đi hàng ba.</li><li>Không dùng điện thoại khi đang chạy.</li><li>Gửi xe đúng chỗ, khoá cổ và khoá đĩa.</li></ul>
""",
"faq": [("Con 15 tuổi đi xe máy điện được không?", "Không, nếu đó là xe gắn máy điện hay mô tô điện. Người dưới 16 tuổi chỉ nên đi xe đạp, xe đạp điện."),
        ("Mua xe cho con, bố mẹ đứng tên được không?", "Được. Nhiều gia đình để bố mẹ đứng tên đăng ký xe; con mang theo đăng ký xe (bản giấy hoặc bản điện tử) khi đi đường."),
        ("Xe điện hay xe 50cc an toàn hơn cho học sinh?", "Cả hai đều giới hạn tốc độ thiết kế 50 km/h. An toàn phụ thuộc phanh, mũ bảo hiểm và cách con đi nhiều hơn là loại động cơ.")],
},
{
"url": "/giay-to/16-tuoi-di-xe-50cc-can-giay-to-gi/", "author": "bao-chau", "read": 6, "emoji": "📄", "funnel": "Đáy phễu", "muc": "giay-to",
"cat_name": "Tuổi, bằng lái, biển số", "cat_url": "/cam-nang/?muc=giay-to", "crumb": "16 tuổi đi xe 50cc cần giấy tờ gì",
"title": "16 tuổi đi xe 50cc cần giấy tờ gì? Có cần bằng lái không? (2026)",
"desc": "Tuổi được đi xe 50cc, xe điện; có cần bằng lái không; giấy tờ phải mang theo và các bước đăng ký biển số, theo luật đang hiệu lực từ 2025.",
"h1": "16 tuổi đi xe 50cc cần giấy tờ gì?",
"quick_title": "Tóm lại",
"quick": ["Đủ 16 tuổi được đi xe gắn máy (dưới 50cc hoặc xe điện đến 4 kW, tốc độ đến 50 km/h).",
          "Không cần bằng lái.",
          "Phải mang: đăng ký xe, bảo hiểm TNDS bắt buộc, giấy tờ tuỳ thân (bản giấy hoặc tích hợp VNeID)."],
"toc": ["Tuổi được đi xe", "Có cần bằng lái không", "Giấy tờ phải mang theo", "Đăng ký biển số: 4 bước", "Giao xe cho người chưa đủ tuổi"],
"body": h(1, "Tuổi được đi xe") + """
<p>Căn cứ: <b>Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15</b>, hiệu lực từ 01/01/2025. Điều 59 quy định người <b>đủ 16 tuổi trở lên</b> được điều khiển xe gắn máy; đủ 18 tuổi trở lên mới được cấp giấy phép lái xe các hạng A1, A, B.</p>
<p>Xe gắn máy là xe có tốc độ thiết kế không quá 50 km/h; nếu dùng động cơ đốt trong thì dung tích xi lanh không quá 50 cm³, nếu dùng động cơ điện thì công suất không quá 4 kW.</p>
""" + h(2, "Có cần bằng lái không") + """
<p><b>Không.</b> Các hạng giấy phép lái xe trong luật mới bắt đầu từ hạng A1 cho xe mô tô (xăng trên 50 cm³ đến 125 cm³, điện trên 4 kW đến 11 kW). Xe gắn máy không thuộc hạng nào, nên người đủ 16 tuổi đi xe 50cc hay xe máy điện đến 4 kW không cần bằng lái.</p>
""" + h(3, "Giấy tờ phải mang theo") + """
<ul><li>Chứng nhận đăng ký xe.</li><li>Chứng nhận bảo hiểm bắt buộc trách nhiệm dân sự của chủ xe cơ giới.</li><li>Căn cước hoặc giấy tờ tuỳ thân.</li></ul>
<p>Các giấy tờ đã tích hợp trên ứng dụng VNeID có thể xuất trình bản điện tử thay cho bản giấy.</p>
""" + h(4, "Đăng ký biển số: 4 bước") + """
<p>Thủ tục theo Thông tư 79/2024/TT-BCA (hiệu lực 01/01/2025). Xe máy đăng ký tại công an cấp xã nơi chủ xe cư trú.</p>
<ol><li><b>Kê khai</b> giấy khai đăng ký xe trên Cổng dịch vụ công hoặc VNeID.</li><li><b>Nộp lệ phí trước bạ</b> (2% hoặc 5% tuỳ nơi, xem bài giá lăn bánh trên phoxedien.vn).</li><li><b>Mang xe và hồ sơ</b> (hoá đơn, phiếu kiểm tra chất lượng xuất xưởng, chứng từ lệ phí trước bạ, giấy tờ chủ xe) tới công an để kiểm tra xe.</li><li><b>Nhận biển số</b> và chứng nhận đăng ký xe.</li></ol>
<p class="luu-y">Thủ tục có thể được điều chỉnh theo văn bản mới. Trước khi đi, hỏi lại công an nơi đăng ký hoặc nhờ cửa hàng làm hộ.</p>
""" + h(5, "Giao xe cho người chưa đủ tuổi") + """
<p>Mức phạt theo Nghị định 168/2024/NĐ-CP. Người chưa đủ tuổi điều khiển xe gắn máy bị xử lý, và <b>người giao xe</b> cho người không đủ điều kiện điều khiển cũng có thể bị phạt. Bố mẹ đừng để con dưới 16 tuổi đi xe 50cc, xe máy điện.</p>
""",
"faq": [("Xe máy điện có phải đăng ký biển số không?", "Có. Xe máy điện là xe gắn máy hoặc xe mô tô, đều phải đăng ký và gắn biển số. Xe đạp điện thì không."),
        ("Học sinh có tự đứng tên đăng ký xe được không?", "Nhiều gia đình để bố mẹ đứng tên cho đơn giản. Nếu muốn con đứng tên, hỏi công an nơi đăng ký về điều kiện với người chưa đủ 18 tuổi."),
        ("Quên mang đăng ký xe có bị phạt không?", "Có thể bị xử phạt theo Nghị định 168/2024/NĐ-CP. Nếu đăng ký xe đã tích hợp trên VNeID, có thể xuất trình trên điện thoại.")],
},
{
"url": "/sua-xe/xe-dien-khong-len-nguon/", "author": "quoc-bao", "read": 5, "emoji": "🔧", "funnel": "Giữa phễu", "muc": "sua-xe",
"cat_name": "Pin, sạc, sửa xe", "cat_url": "/cam-nang/?muc=sua-xe", "crumb": "Xe điện không lên nguồn",
"title": "Xe điện không lên nguồn: tự kiểm 4 chỗ trước khi gọi thợ",
"desc": "Xe điện bật khoá không lên đèn, lên đèn mà không chạy: 4 chỗ tự kiểm trong 5 phút và khi nào phải mang ra tiệm.",
"h1": "Xe điện không lên nguồn: tự kiểm 4 chỗ trước khi gọi thợ",
"quick": ["Kiểm khoá và chế độ chống trộm, cầu chì, giắc nối pin, công tắc phanh.",
          "Lên đèn mà không chạy: hay do tay phanh bị kẹt hoặc chân chống.",
          "Pin phồng, có mùi khét, xe vừa ngập nước: ngừng dùng, mang ra tiệm."],
"toc": ["Khoá và chống trộm", "Cầu chì", "Giắc nối pin, ắc quy", "Công tắc phanh, chân chống", "Khi nào mang ra tiệm"],
"body": "<p>Xe tắt ngang chưa chắc đã hỏng pin. Bảo gặp nhiều nhất là bốn chỗ dưới đây, tự kiểm được trong 5 phút.</p>" + h(1, "Khoá và chống trộm") + """
<p>Nhiều xe có remote chống trộm: đang ở chế độ khoá thì bật chìa cũng không chạy. Bấm mở khoá trên remote, thử lại. Remote hết pin thì thay pin nút áo trong remote.</p>
""" + h(2, "Cầu chì") + """
<p>Cầu chì thường nằm gần bình hoặc dưới yên. Rút ra soi: dây bên trong đứt là phải thay đúng số ampe ghi trên cầu chì cũ. Thay xong lại đứt ngay là có chạm chập, đừng thay tiếp, mang ra tiệm.</p>
""" + h(3, "Giắc nối pin, ắc quy") + """
<p>Giắc lỏng hoặc bị ô xi hoá (có lớp xanh, trắng) làm mất điện chập chờn. Tắt khoá, rút giắc ra cắm lại cho chặt. Với pin rút được, lắp lại pin cho đúng khớp.</p>
""" + h(4, "Công tắc phanh, chân chống") + """
<p>Xe lên đèn mà vặn ga không chạy: nhiều xe ngắt động cơ khi tay phanh đang bóp hoặc chân chống đang hạ. Tay phanh bị kẹt, lò xo yếu là xe tưởng như hỏng. Bóp nhả phanh vài lần, gạt chân chống lên hẳn rồi thử lại.</p>
""" + h(5, "Khi nào mang ra tiệm") + """
<ul><li>Pin phồng, nóng bất thường, có mùi khét.</li><li>Xe vừa đi qua chỗ ngập sâu.</li><li>Đã kiểm 4 chỗ trên mà vẫn không lên.</li></ul>
<p><b>Không tự tháo khối pin lithium.</b> Pin hỏng cần nơi có thiết bị kiểm tra. Muốn biết pin còn tốt không, đọc thêm <a href="/hoc-sinh/chon-xe-cho-con-hoc-cap-3/">phần chi phí nuôi xe</a> và hỏi thợ đo dung lượng.</p>
""",
"faq": [("Xe điện sạc không vào là hỏng pin hay hỏng sạc?", "Thử sạc khác cùng loại hoặc ổ cắm khác trước. Đèn sạc không đổi màu, sạc không nóng thì nhiều khả năng do sạc; sạc tốt mà pin không lên thì mang pin đi kiểm."),
        ("Xe điện bị ngập nước có sạc ngay được không?", "Không. Tắt khoá, đẩy xe lên chỗ khô, không sạc, mang ra tiệm kiểm tra trước."),
        ("Cầu chì xe điện mua ở đâu?", "Cửa hàng phụ tùng xe điện có bán. Mang cầu chì cũ theo để mua đúng loại và đúng số ampe.")],
},
{
"url": "/hoc-sinh/xe-dien-hay-xe-xang-chi-phi/", "author": "thu-ha", "read": 5, "emoji": "💰", "funnel": "Giữa phễu", "muc": "hoc-sinh",
"cat_name": "Xe cho học sinh", "cat_url": "/cam-nang/?muc=hoc-sinh", "crumb": "Xe điện hay xe xăng: chi phí",
"title": "Xe điện hay xe xăng 50cc: chi phí nuôi xe mỗi tháng cho con",
"desc": "So chi phí xe điện và xe xăng 50cc cho học sinh: tiền mua, tiền xăng điện, bảo dưỡng, thay pin. Cách tự tính cho gia đình mình.",
"h1": "Xe điện hay xe xăng 50cc: bóc tách chi phí nuôi xe",
"quick": ["Tiền sạc điện mỗi km thường thấp hơn tiền xăng.",
          "Xe xăng tốn thêm nhớt, bugi; xe điện để dành tiền thay pin.",
          "Tự tính bằng 4 khoản: giá lăn bánh, năng lượng, bảo dưỡng, thay pin."],
"toc": ["Bốn khoản cần tính", "Tự tính tiền xăng, tiền điện", "Bảo dưỡng", "Kết luận cho phụ huynh"],
"body": h(1, "Bốn khoản cần tính") + """
<p>Mình hay thấy phụ huynh chỉ so giá xe. Nhưng con sẽ đi chiếc xe đó ba năm cấp 3, nên mình tính đủ bốn khoản: <b>giá lăn bánh</b>, <b>tiền xăng hoặc điện</b>, <b>bảo dưỡng</b>, và với xe điện là <b>thay pin</b>.</p>
""" + h(2, "Tự tính tiền xăng, tiền điện") + """
<ul><li><b>Xe xăng:</b> quãng đường mỗi tháng ÷ số km đi được mỗi lít (hỏi người bán mức tiêu hao của mẫu xe) × giá xăng hiện tại.</li>
<li><b>Xe điện:</b> số lần sạc mỗi tháng × số kWh mỗi lần sạc (dung lượng pin, hỏi người bán) × giá điện nhà bạn.</li></ul>
<p>Ví dụ cách làm: con đi 10 km mỗi ngày, 26 ngày mỗi tháng là khoảng 260 km. Thay số của mẫu xe bạn đang xem vào hai công thức trên là ra con số cho nhà mình, không phải đoán.</p>
""" + h(3, "Bảo dưỡng") + """
<p>Xe 50cc cần thay nhớt, kiểm tra bugi, lọc gió định kỳ. Xe điện ít hạng mục hơn (phanh, lốp, kiểm tra điện), nhưng pin sẽ chai dần; ắc quy chì thường phải thay sớm hơn pin lithium. Đọc thêm <a href="/sua-xe/xe-dien-khong-len-nguon/">các lỗi điện hay gặp</a>.</p>
""" + h(4, "Kết luận cho phụ huynh") + """
<p>Nhà gần trường, có chỗ sạc an toàn: xe điện thường rẻ hơn khi tính cả ba năm. Con đi xa, đi học thêm nhiều nơi, nhà không có chỗ sạc: xe 50cc đỡ phiền. Muốn có con số chính xác cho mẫu cụ thể, bấm Chat để nhân viên tính giúp.</p>
""",
"faq": [("Sạc xe điện ở nhà có tốn điện nhiều không?", "Tuỳ dung lượng pin và số lần sạc. Lấy dung lượng pin (kWh) nhân giá điện bậc nhà bạn đang dùng là ra tiền mỗi lần sạc đầy."),
        ("Thay pin xe điện có đắt không?", "Pin lithium đắt hơn ắc quy chì khi thay, nhưng thường bền hơn. Hỏi giá thay pin của đúng mẫu xe trước khi mua."),
        ("Xe 50cc có tốn xăng không?", "Xe 50cc nhỏ máy nên thường tiết kiệm xăng; mức cụ thể tuỳ mẫu, hỏi người bán số liệu của hãng.")],
},
]
