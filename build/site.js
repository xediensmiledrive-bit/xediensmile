(function(){
  var d=document,top=d.querySelector('.top');
  // Đầu trang có viền khi cuộn
  addEventListener('scroll',function(){top.classList.toggle('cuon',scrollY>8)},{passive:true});
  // Menu
  var nut=d.querySelector('.nut-menu');
  if(nut)nut.addEventListener('click',function(){var m=d.body.classList.toggle('mo');nut.setAttribute('aria-expanded',m)});
  // Hiện dần khi cuộn tới
  var els=d.querySelectorAll('.hd-in');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('vao');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
    els.forEach(function(el){io.observe(el)});
  }else els.forEach(function(el){el.classList.add('vao')});
  // Lọc bảng giá theo nhóm
  d.querySelectorAll('[data-loc]').forEach(function(nhom){
    var bang=d.getElementById(nhom.getAttribute('data-loc'));
    nhom.addEventListener('click',function(e){
      var c=e.target.closest('.chip');if(!c)return;
      nhom.querySelectorAll('.chip').forEach(function(x){x.classList.toggle('on',x===c)});
      var k=c.getAttribute('data-k');
      bang.querySelectorAll('[data-n]').forEach(function(r){r.classList.toggle('an',k!=='all'&&r.getAttribute('data-n')!==k)});
    });
  });
  // Chọn xe giúp tôi
  d.querySelectorAll('.chon').forEach(function(k){
    var gy=k.querySelector('.goi-y');
    k.addEventListener('click',function(e){
      var b=e.target.closest('button[data-g]');if(!b)return;
      k.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===b)});
      gy.innerHTML=b.getAttribute('data-g');gy.classList.remove('hien');void gy.offsetWidth;gy.classList.add('hien');
    });
  });
})();
(function(){
  /* Chatbot kiểu chatbot2: có tên người tư vấn, cây ý định, nút gợi ý, xin số rồi chuyển nhân viên */
  var d=document,P=window.PXD||{},k=d.querySelector('.chat');if(!k)return;
  var than=k.querySelector('.chat-than'),goi=k.querySelector('.chat-goi'),f=k.querySelector('.chat-o'),inp=f.querySelector('input');
  var TEN=P.bot||'bạn tư vấn',HOT=P.hot,opened=false,gotPhone=false,askIdx=0;
  var DC=(P.stores&&P.stores.length)?P.stores:null;
  var A={
    hello:{t:['Chào bạn, em là '+TEN+', tư vấn của Xe điện Smile. Bạn đang tìm xe cho mình hay cho con đi học ạ?'],c:[['Cho con đi học','hoc_sinh'],['Cho mình đi làm','di_lam'],['Hỏi giá','gia'],['Hỏi giấy tờ','bang_lai']]},
    hoc_sinh:{t:['Dạ, bé nhà mình năm nay bao nhiêu tuổi rồi ạ? Tuổi quyết định đi được loại xe nào nên em hỏi trước.'],c:[['Chưa đủ 16 tuổi','duoi16'],['Đủ 16 tuổi trở lên','du16']]},
    duoi16:{t:['Dưới 16 tuổi thì luật chưa cho đi xe 50cc hay xe máy điện ạ. Bé đi xe đạp điện là đúng luật: không cần bằng, không cần biển số.','Bé cao khoảng bao nhiêu, nhà cách trường xa không ạ? Em gợi ý mẫu vừa người bé.'],c:[['Xem giá xe đạp điện','gia'],['Nhà gần, dưới 5 km','gan'],['Nhà xa trên 5 km','xa']]},
    du16:{t:['Đủ 16 tuổi là đi được xe gắn máy rồi ạ: xe dưới 50cc hoặc xe máy điện đến 4 kW, tốc độ đến 50 km/h, không cần bằng lái.','Nhà mình có chỗ sạc điện cho xe không ạ? Có thì xe điện tiết kiệm hơn, không thì xe 50cc đỡ lo.'],c:[['Có chỗ sạc','co_sac'],['Không có chỗ sạc','khong_sac'],['Cần giấy tờ gì?','bang_lai']]},
    gan:{t:['Nhà gần thì xe đạp điện là đủ, nhẹ, bé tự dắt được. Bạn để số, bên em báo giá các mẫu đang có màu bé thích nha.'],ask:1},
    xa:{t:['Đi xa thì nên chọn xe đạp điện pin lithium, nhẹ mà đi được xa hơn bản ắc quy. Em nhờ bạn bên em gọi tư vấn mẫu cụ thể nha.'],ask:1},
    co_sac:{t:['Vậy xe máy điện hợp lắm ạ: êm, không xăng, sạc qua đêm ở nhà. Bạn cho em biết tầm tiền dự định để em lọc mẫu?'],c:[['Dưới 15 triệu','tam_tien'],['15 đến 25 triệu','tam_tien'],['Trên 25 triệu','tam_tien']]},
    khong_sac:{t:['Không có chỗ sạc thì xe 50cc tiện hơn ạ, đổ xăng vài phút là đi. Bé thích xe ga hay xe số?'],c:[['Xe ga','tam_tien'],['Xe số, wave, cub','tam_tien'],['Chưa biết, so giúp em','so_sanh']]},
    di_lam:{t:['Dạ, mỗi ngày mình đi khoảng bao nhiêu km, và có chỗ sạc ở nhà hoặc chỗ làm không ạ?'],c:[['Dưới 30 km, có chỗ sạc','co_sac'],['Đi xa hoặc không có chỗ sạc','khong_sac']]},
    tam_tien:{t:['Em ghi nhận rồi ạ. Giá từng mẫu có trong bảng giá trên trang, còn giá hôm nay kèm quà tặng và màu còn hàng thì bạn bên em báo chính xác hơn.'],ask:1},
    gia:{t:['Giá trên trang là giá tham khảo tháng này ạ, chưa gồm trước bạ, biển số và bảo hiểm. Bạn đang xem mẫu nào, hoặc tầm tiền bao nhiêu để em báo giá lăn bánh?'],c:[['Dưới 15 triệu','tam_tien'],['15 đến 25 triệu','tam_tien'],['Trên 25 triệu','tam_tien'],['Có trả góp không?','gop']]},
    gop:{t:['Nhiều mẫu mua trả góp được ạ. Số trả trước và giấy tờ tuỳ chương trình từng tháng, thường chỉ cần căn cước. Bạn để số, bên em tính đúng số tiền mỗi tháng theo mẫu bạn chọn nha.'],ask:1},
    bang_lai:{t:['Xe gắn máy (dưới 50cc hoặc xe điện đến 4 kW, tốc độ đến 50 km/h): đủ 16 tuổi là đi được, không cần bằng lái.','Khi đi đường mang đăng ký xe, bảo hiểm bắt buộc và căn cước; đã tích hợp VNeID thì xuất trình trên điện thoại được.'],c:[['Đăng ký biển số thế nào?','bien_so'],['Hỏi giá','gia']]},
    bien_so:{t:['Xe máy điện và xe 50cc đều phải đăng ký biển số ạ, làm ở công an xã, phường nơi mình cư trú. Mua ở Smile thì bên em hỗ trợ hướng dẫn hồ sơ. Xe đạp điện thì không cần biển số.'],c:[['Hỏi giá lăn bánh','gia']]},
    so_sanh:{t:['Xe ga: không sang số, có cốp, hợp bạn nữ, nặng hơn chút. Xe số, wave, cub: rẻ, nhẹ, bền, sửa đâu cũng được.','Bé nhỏ người thì nên ngồi thử xem chống chân được không trước khi chọn ạ.'],c:[['Hỏi giá xe ga','gia'],['Hỏi giá xe số','gia']]},
    pin:{t:['Pin lithium nhẹ, bền hơn nhưng đắt hơn ắc quy chì. Xe đang không lên nguồn thì bạn thử kiểm khoá chống trộm, cầu chì, giắc pin và tay phanh trước nha.','Vẫn không được thì gọi '+HOT+', thợ bên em hướng dẫn tiếp.']},
    dc:{t:DC?['Smile Motor có các cửa hàng:'].concat(DC):['Smile Motor có nhiều cửa hàng ạ. Bạn ở quận, huyện nào để em chỉ cửa hàng gần nhất?'],ask:1},
    nguoi:{t:['Em là trợ lý tự động của Xe điện Smile ạ, trả lời nhanh các câu hay gặp. Cần nói chuyện với nhân viên thật thì bạn gọi hoặc Zalo '+HOT+' nha.']},
    fallback:{t:['Câu này em chưa chắc, để nhân viên bên em trả lời cho chính xác ạ.'],ask:1}
  };
  var ASKS=['Bạn cho em xin số điện thoại, bạn bên em gọi tư vấn kỹ nha?','Mình để lại số, bên em gọi báo giá đúng mẫu cho bạn liền.','Bạn nhắn em số điện thoại, hoặc gọi thẳng '+HOT+' cho nhanh ạ.'];
  function add(t,who){var e=d.createElement('div');e.className='tn '+(who||'bot');e.textContent=t;than.appendChild(e);than.scrollTop=than.scrollHeight;return e}
  function chips(list){goi.innerHTML='';(list||[]).forEach(function(c){var b=d.createElement('button');b.type='button';b.textContent=c[0];b.onclick=function(){add(c[0],'toi');run(c[1])};goi.appendChild(b)});
    var a=d.createElement('a');a.href='tel:'+P.tel;a.textContent='Gọi '+HOT;goi.appendChild(a);
    var z=d.createElement('a');z.href='https://zalo.me/'+P.tel;z.target='_blank';z.rel='noopener nofollow';z.textContent='Zalo';goi.appendChild(z)}
  function say(lines,done){var i=0;goi.innerHTML='';(function next(){if(i>=lines.length){done&&done();return}
    var t=add('','bot');t.innerHTML='<span class="dang-go"><i></i><i></i><i></i></span>';
    setTimeout(function(){t.textContent=lines[i++];than.scrollTop=than.scrollHeight;next()},Math.min(1300,450+String(lines[i]).length*10))})()}
  function run(key){var a=A[key]||A.fallback,l=a.t.slice();if(a.ask&&!gotPhone){l.push(ASKS[askIdx++%ASKS.length])}say(l,function(){chips(a.c||[['Hỏi giá','gia'],['Giấy tờ, bằng lái','bang_lai'],['Cửa hàng ở đâu?','dc']])})}
  function classify(s){s=s.toLowerCase();
    var r=[['nguoi','người thật|người hay máy|bot|robot|máy trả lời'],['gop','góp|trả trước|lãi'],['gia','giá|bao nhiêu|bn|tiền|triệu|rẻ|đắt|mắc'],['bien_so','biển|đăng ký|đăng kí'],['bang_lai','bằng|giấy tờ|tuổi|luật|phạt'],['dc','địa chỉ|cửa hàng|ở đâu|chi nhánh|showroom'],['pin','pin|sạc|ắc quy|hỏng|lỗi|không lên|không chạy'],['so_sanh','so sánh|hay là|xe ga|xe số|wave|cub'],['hoc_sinh','con|học sinh|đi học|lớp'],['di_lam','đi làm']];
    for(var i=0;i<r.length;i++)if(new RegExp(r[i][1]).test(s))return r[i][0];return 'fallback'}
  function phone(s){var x=s.replace(/\D/g,'');if(x.length<8)return null;if(x.length===10&&/^0[35789]/.test(x))return{ok:1,n:x};return{ok:0}}
  function guiSo(n){/* Gửi số về máy chủ nếu có điểm nhận; không có thì mời khách gọi, Zalo */
    var ok=function(){say(['Em cảm ơn, em đã chuyển số '+n.replace(/(\d{4})(\d{3})(\d{3})/,'$1.$2.$3')+' cho nhân viên, bên em gọi lại trong giờ làm việc nha. Cần gấp thì bạn gọi '+HOT+'.'],function(){chips()})};
    var fail=function(){say(['Em chưa gửi được số tự động. Bạn bấm Gọi hoặc Zalo '+HOT+' bên dưới, nhân viên nghe máy ngay ạ.'],function(){chips()})};
    try{fetch('/api/lien-he.php',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({sdt:n,web:P.web,trang:location.pathname,luc:new Date().toISOString()})}).then(function(r){r.ok?ok():fail()}).catch(fail)}catch(e){fail()}}
  function mo(intent){k.classList.add('mo');k.setAttribute('aria-hidden','false');
    if(!opened){opened=true;run(intent||'hello')}else if(intent){run(intent)}}
  d.addEventListener('click',function(e){var b=e.target.closest('[data-chat]');if(b){e.preventDefault();mo(b.getAttribute('data-chat')||'')}});
  k.querySelector('.chat-dong').addEventListener('click',function(){k.classList.remove('mo');k.setAttribute('aria-hidden','true')});
  f.addEventListener('submit',function(e){e.preventDefault();var v=inp.value.trim();if(!v)return;inp.value='';add(v,'toi');
    var p=phone(v);if(p){if(p.ok){gotPhone=true;guiSo(p.n)}else say(['Số này chưa đúng 10 số di động, bạn gõ lại giúp em nha.']);return}
    run(classify(v))});
})();
(function(){
  /* Hero chạy cuộn: vuốt tay, chấm chọn, tự chuyển 5 giây; dừng khi chạm, rê chuột, tab ẩn hoặc bật giảm chuyển động */
  var t=document.querySelector('.truot');if(!t)return;
  // Banner theo mùa (data-mua="MM-DD,MM-DD"): ngoài dịp thì gỡ banner và chấm tương ứng
  var dd=new Date(),md=('0'+(dd.getMonth()+1)).slice(-2)+'-'+('0'+dd.getDate()).slice(-2),cs=t.querySelectorAll('.tr-cham button');
  [].slice.call(t.querySelectorAll('.tr-o')).forEach(function(o,k){var m=o.getAttribute('data-mua');if(!m)return;m=m.split(',');
    if(!(m[0]<=m[1]?(md>=m[0]&&md<=m[1]):(md>=m[0]||md<=m[1]))){o.remove();if(cs[k])cs[k].remove()}});
  // slide hãng: ảnh điện thoại có thể là hãng khác ảnh máy tính, link theo ảnh đang hiện
  if(matchMedia('(max-width:767px)').matches)t.querySelectorAll('.tr-lk[data-href-dt]').forEach(function(a){a.href=a.getAttribute('data-href-dt')});
  var ray=t.querySelector('.tr-ray'),o=ray.children,ch=t.querySelectorAll('.tr-cham button'),n=o.length,i=0,hen=null,
      im=matchMedia('(prefers-reduced-motion:reduce)').matches;
  function toi(k){i=(k+n)%n;ray.scrollTo({left:o[i].offsetLeft-ray.offsetLeft,behavior:im?'auto':'smooth'})}
  function danh(){ch.forEach(function(c,k){if(k===i)c.setAttribute('aria-current','true');else c.removeAttribute('aria-current')})}
  function chay(){dung();if(!im&&!document.hidden)hen=setInterval(function(){toi(i+1)},5000)}
  function dung(){clearInterval(hen);hen=null}
  ch.forEach(function(c,k){c.addEventListener('click',function(){toi(k);chay()})});
  var lui=t.querySelector('.tr-lui'),tien=t.querySelector('.tr-toi');
  if(lui)lui.addEventListener('click',function(){toi(i-1);chay()});
  if(tien)tien.addEventListener('click',function(){toi(i+1);chay()});
  var cho;ray.addEventListener('scroll',function(){clearTimeout(cho);cho=setTimeout(function(){i=Math.round(ray.scrollLeft/ray.clientWidth);danh()},60)},{passive:true});
  ray.addEventListener('touchstart',dung,{passive:true});ray.addEventListener('touchend',chay,{passive:true});
  t.addEventListener('mouseenter',dung);t.addEventListener('mouseleave',chay);
  document.addEventListener('visibilitychange',chay);
  // điểm sáng trên banner: bấm ra ô thông tin xe; mở thì dừng tự chuyển
  var pop=t.querySelector('.tr-pop'),than=pop&&pop.querySelector('.tp-than'),mo=false;
  function dong(){if(!pop)return;pop.hidden=true;mo=false;chay()}
  t.querySelectorAll('.tr-diem').forEach(function(b){b.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();
    var tp=b.parentNode.querySelector('.tr-tpl');if(!tp||!pop)return;than.innerHTML='';than.appendChild(tp.content.cloneNode(true));
    pop.hidden=false;mo=true;dung()})});
  if(pop){pop.querySelector('.tp-dong').addEventListener('click',dong);
    document.addEventListener('click',function(e){if(mo&&!pop.contains(e.target)&&!e.target.closest('.tr-diem'))dong()});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&mo)dong()});
    t.addEventListener('mouseleave',function(){if(mo)dung()})}
  chay();
})();
(function(){
  /* Hiệu ứng rơi theo ngày trong năm (kiểu các site Smile). Mỗi dòng: từ ngày, đến ngày (MM-DD hoặc YYYY-MM-DD), hình rơi.
     Tết và Trung thu theo âm lịch nên ghi rõ năm. Thử ngày khác: thêm ?roi=MM-DD vào địa chỉ. */
  var L=[
    ['12-30','01-02',['🎉','✨','🎊']],
    ['2027-01-30','2027-02-14',['🌸','🌼','🧧']],
    ['02-13','02-14',['❤️','💕','🌹']],
    ['03-06','03-08',['🌷','🌸','💐']],
    ['04-29','05-01',['⭐','🎉']],
    ['05-31','06-01',['🎈','⭐','🍭']],
    ['09-01','09-02',['⭐','🎉']],
    ['2027-09-13','2027-09-15',['🏮','🌕','⭐']],
    ['10-18','10-20',['🌸','🌷','💐','💖']],
    ['11-18','11-20',['🌷','💐','📚']],
    ['12-22','12-25',['❄️','⛄','🎄']]
  ];
  if(matchMedia('(prefers-reduced-motion:reduce)').matches)return;
  try{if(localStorage.getItem('tatRoi')===new Date().toDateString())return}catch(e){}
  var q=(location.search.match(/[?&]roi=([\d-]+)/)||[])[1],d=new Date(),
      p=function(x){return x<10?'0'+x:''+x},md=q||p(d.getMonth()+1)+'-'+p(d.getDate()),ymd=d.getFullYear()+'-'+md;
  function trong(a,b){var x=a.length>5?ymd:md;return a<=b?(x>=a&&x<=b):(x>=a||x<=b)}
  var h=null;L.forEach(function(r){if(!h&&trong(r[0],r[1]))h=r[2]});if(!h)return;
  var k=document.createElement('div');k.className='roi';k.setAttribute('aria-hidden','true');
  var so=innerWidth<768?5:10;
  for(var j=0;j<so;j++){var e=document.createElement('i'),z=(innerWidth<768?12:14)+Math.random()*12;
    e.textContent=h[j%h.length];
    e.style.cssText='left:'+(Math.random()*100)+'%;font-size:'+z+'px;opacity:'+(.4+Math.random()*.35)+';animation-duration:'+(7+Math.random()*7)+'s;animation-delay:-'+(Math.random()*12)+'s;--x:'+(Math.random()*120-60)+'px;--r:'+(Math.random()*540-270)+'deg';
    k.appendChild(e)}
  var b=document.createElement('button');b.type='button';b.className='tat-roi';b.textContent='Tắt hiệu ứng';b.setAttribute('aria-label','Tắt hiệu ứng');b.title='Tắt hiệu ứng';
  b.onclick=function(){k.remove();b.remove();try{localStorage.setItem('tatRoi',new Date().toDateString())}catch(e){}};
  document.body.appendChild(k);document.body.appendChild(b);
})();
(function(){
  /* Trang chủ bán xe: lọc thẻ xe theo loại và hãng ngay trên trang, hiện 12 thẻ rồi Xem thêm */
  var g=document.querySelector('.ban-xe');if(!g)return;
  var the=[].slice.call(g.children),buoc=+g.getAttribute('data-hien')||12,hien=buoc,loai='',hang='',
      them=document.querySelector('.xem-them');
  function ve(){var n=0;the.forEach(function(o){var hop=(!loai||o.getAttribute('data-loai')===loai)&&(!hang||o.getAttribute('data-hang')===hang);
      o.classList.toggle('an',!hop);o.classList.toggle('gioi',hop&&++n>hien)});
    if(them)them.style.display=n>hien?'':'none'}
  function nhom(sel,attr,cb){document.querySelectorAll(sel).forEach(function(b){b.addEventListener('click',function(){
      document.querySelectorAll(sel).forEach(function(x){x.classList.toggle('on',x===b)});cb(b.getAttribute(attr)||'');hien=buoc;ve()})})}
  nhom('.tab-xe [data-tab]','data-tab',function(v){loai=v});
  nhom('.hang-xe [data-hang]','data-hang',function(v){hang=v});
  if(them)them.addEventListener('click',function(){hien+=buoc;ve()});
  ve();
})();
(function(){
  /* ?hang=<slug>: trang loại xe chỉ hiện xe của hãng đó (menu .com.vn bấm vào hãng) */
  var h=(location.search.match(/[?&]hang=([a-z0-9-]+)/)||[])[1];if(!h)return;
  var rs=document.querySelectorAll('.dong[data-hang],.o-xe[data-hang]'),co=0,ten='';
  rs.forEach(function(r){var ok=r.getAttribute('data-hang')===h;r.style.display=ok?'':'none';if(ok){co++;if(!ten){var s=r.querySelector('small');ten=s?s.textContent.split(' · ')[0]:''}}});
  if(!co){rs.forEach(function(r){r.style.display=''});return}
  var b=document.querySelector('.the.bang'),n=document.createElement('div');n.className='dang-loc';
  n.innerHTML='Đang xem xe <b></b> · <a href="'+location.pathname+'">Xem tất cả hãng</a>';n.querySelector('b').textContent=ten||h;
  if(b)b.parentNode.insertBefore(n,b);
  var bh=document.querySelector('.banner-hang[data-hang="'+h+'"]');if(bh){bh.hidden=false;bh.querySelectorAll('img').forEach(function(i){i.loading='eager'})}
})();
(function(){
  /* Banner hãng: mũi tên, số trang, tự chuyển 5 giây, dừng khi rê chuột */
  document.querySelectorAll('.banner-hang').forEach(function(w){
    var r=w.querySelector('.bh-ray'),n=r.children.length,so=w.querySelector('.bh-so');if(n<2)return;
    function i(){return Math.round(r.scrollLeft/r.clientWidth)}
    function toi(k){r.scrollTo({left:((k+n)%n)*r.clientWidth,behavior:'smooth'})}
    w.querySelector('.bh-lui').onclick=function(){toi(i()-1)};w.querySelector('.bh-toi').onclick=function(){toi(i()+1)};
    r.addEventListener('scroll',function(){if(so)so.textContent=(i()+1)+'/'+n},{passive:true});
    var dung=false;w.onmouseenter=function(){dung=true};w.onmouseleave=function(){dung=false};
    setInterval(function(){if(!dung&&!w.hidden&&!document.hidden)toi(i()+1)},5000);
  });
})();
(function(){
  /* Video: bấm vào ảnh mới tải YouTube (nhẹ trang) */
  document.addEventListener('click',function(e){var b=e.target.closest('.vd[data-yt]');if(!b)return;
    var f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+b.getAttribute('data-yt')+'?autoplay=1&rel=0';
    f.allow='accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture';f.allowFullscreen=true;f.title=b.getAttribute('aria-label')||'Video';
    b.replaceWith(f)});
})();
(function(){
  /* Tải trước trang khi rê chuột hoặc chạm vào link nội bộ: bấm là mở gần như tức thì */
  var da={};
  function tai(e){var a=e.target.closest&&e.target.closest('a[href]');if(!a||a.target||a.hasAttribute('download'))return;
    var u=new URL(a.href,location.href);if(u.origin!==location.origin||u.pathname===location.pathname||da[u.pathname])return;
    if(navigator.connection&&(navigator.connection.saveData||/2g/.test(navigator.connection.effectiveType||'')))return;
    da[u.pathname]=1;var l=document.createElement('link');l.rel='prefetch';l.href=u.pathname;document.head.appendChild(l)}
  document.addEventListener('mouseover',function(e){clearTimeout(tai.t);tai.t=setTimeout(function(){tai(e)},65)},{passive:true});
  document.addEventListener('touchstart',tai,{passive:true});
})();
(function(){
  /* Chân trang: bấm cửa hàng nào thì bản đồ chuyển sang cửa hàng đó */
  var m=document.querySelector('.ch-map iframe');if(!m)return;
  document.querySelectorAll('.ch-o').forEach(function(b){b.onclick=function(){
    document.querySelectorAll('.ch-o.on').forEach(function(x){x.classList.remove('on')});b.classList.add('on');m.src=b.getAttribute('data-map')}});
})();
/* Clip TikTok: clip nào nằm trọn trong màn hình thì gắn trình phát tự chạy không tiếng, ra khỏi màn hình thì gỡ cho nhẹ máy */
(function(){
  var ds=document.querySelectorAll('.tt-o[data-tt]');
  if(!ds.length||!('IntersectionObserver' in window))return;
  var io=new IntersectionObserver(function(es){es.forEach(function(e){
    var a=e.target,f=a.querySelector('iframe');
    if(e.isIntersecting&&e.intersectionRatio>.6){
      if(!f&&document.querySelectorAll('.tt-o iframe').length<4){
        f=document.createElement('iframe');
        f.src='https://www.tiktok.com/player/v1/'+a.getAttribute('data-tt')+'?autoplay=1&muted=1&loop=1&controls=0&progress_bar=0&play_button=0&volume_control=0&fullscreen_button=0&timestamp=0&music_info=0&description=0&rel=0&native_context_menu=0&closed_caption=0';
        f.allow='autoplay; encrypted-media; fullscreen';f.loading='lazy';f.title='Clip TikTok Smile Motor';
        a.appendChild(f);
      }
    }else if(f){f.remove();}
  });},{threshold:[0,.6,1]});
  ds.forEach(function(a){io.observe(a);});
})();
/* Bảng, danh sách dài: chỉ hiện phần đầu, nút "Xem thêm" mở tiếp (anh góp ý 21/10 0:08). Nội dung vẫn nằm sẵn trong trang cho Google đọc. */
(function(){
  var NHOM=[['.the.bang','.dong:not(.dau)',10,'mẫu'],['.luoi-xe:not(.ban-xe):not(.dau)','.o-xe',8,'mẫu'],['.luoi-tin','.tin-the',6,'bài'],['section','.bai-nho',6,'bài',true],['.ch-luoi ul','li',3,'cửa hàng',true]];
  var ds=[];
  NHOM.forEach(function(n){document.querySelectorAll(n[0]).forEach(function(c){
    var con=n[4]?Array.prototype.filter.call(c.children,function(x){return x.matches(n[1])}):c.querySelectorAll(n[1]);
    if(con.length>n[2]+2)ds.push({c:c,sel:n[1],n:n[2],dv:n[3],truc:n[4]});
  });});
  function lam(o){
    var con=o.truc?Array.prototype.filter.call(o.c.children,function(x){return x.matches(o.sel)}):Array.prototype.slice.call(o.c.querySelectorAll(o.sel));
    var hien=0,an=0;
    con.forEach(function(x){x.classList.remove('gon');if(x.classList.contains('an'))return;hien++;if(!o.mo&&hien>o.n){x.classList.add('gon');an++;}});
    if(!o.nut){o.nut=document.createElement('button');o.nut.type='button';o.nut.className='btn xem-them xem-gon';
      o.nut.onclick=function(){o.mo=1;lam(o);};o.c.parentNode.insertBefore(o.nut,o.c.nextSibling);}
    o.nut.textContent='Xem thêm '+an+' '+o.dv;o.nut.hidden=!an;
  }
  ds.forEach(lam);
  document.addEventListener('click',function(e){if(e.target.closest('.chip,.hx'))setTimeout(function(){ds.forEach(function(o){o.mo=0;lam(o);});},30);});
})();
document.addEventListener('click',function(e){var b=e.target.closest('.doc-tiep');if(b)b.closest('.chot').classList.add('mo');});

/* Trang từng xe: ô "Trả góp từ ... /tháng" (anh chốt 21/10 9:35), cùng công thức trang Trả góp; tính không ra thì giữ chữ mời bấm */
(function(){var o=document.querySelector('[data-sp-tg]');if(!o)return;
  function chay(dt){var T=window.PXDTraGop;if(!T)return;var gia=+o.dataset.gia,l=o.dataset.loai;
    var thu=[[30,12],[30,9],[40,12],[50,12]];
    for(var i=0;i<thu.length;i++){var tot=null;dt.forEach(function(x){var k=T.tinh(x,gia,l,thu[i][0],thu[i][1]);if(k.ok&&(!tot||k.thang<tot.thang))tot=k;});
      if(tot){o.querySelector('[data-sp-tg-chu]').innerHTML='Trả góp từ <b>'+T.tien(tot.thang)+'</b>/tháng<small>Trả trước '+thu[i][0]+'%, góp '+thu[i][1]+' tháng, số tham khảo</small>';o.classList.add('co-so');return;}}}
  function cho(dt){if(window.PXDTraGop)chay(dt);else setTimeout(function(){cho(dt)},150);}
  fetch('/tra-gop-dt.json').then(function(r){return r.ok?r.json():null}).then(function(dt){if(dt)cho(dt)}).catch(function(){});
})();

/* Hỏi đáp kiểu chat trên trang chủ (Kiểu A, 21/10 10:36): hiện cặp đầu, câu khác thành nút; bấm thì câu hỏi bay lên, trả lời hiện như đang gõ */
(function(){var k=document.querySelector('[data-hc]');if(!k)return;var nut=document.querySelector('[data-hc-nut]'),cap=[].slice.call(k.querySelectorAll('.hc-cap'));
  if(cap.length<2)return;k.classList.add('hc-js');
  function hien(c,go){c.classList.add('hien');if(!go)return;var d=c.querySelector('.hc-dap');d.classList.add('dang-go');setTimeout(function(){d.classList.remove('dang-go')},900)}
  hien(cap[0]);
  cap.slice(1).forEach(function(c){var b=document.createElement('button');b.type='button';b.textContent=c.querySelector('.hc-hoi').textContent;
    b.onclick=function(){b.remove();k.appendChild(c);hien(c,true);setTimeout(function(){c.scrollIntoView({behavior:'smooth',block:'nearest'})},50)};nut.appendChild(b)});
})();
