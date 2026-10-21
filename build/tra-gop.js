/* Trả góp phoxedien.vn (21/10/2026). Phần tính chép NGUYÊN từ xediensmile.com js/tra-gop.js ?ver=1.0.24.tg5 (dòng 6–61), không sửa số hay công thức.
   Chạy thử bằng node: require('./tra-gop.js').tinh(...) */
(function (goc) {
  'use strict';
  var tien = function (n) { return Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.') + 'đ'; };
  var pc = function (x) { return String(x).replace('.', ','); };
  var lamTron = function (n) { return Math.round(n / 1000) * 1000; };
  var EPS = 1e-9;

  function trongKhoang(g, tu, den) { return g >= tu - EPS && (!den || g < den - EPS); }
  function co(arr, v) { return arr && arr.indexOf(v) !== -1; }
  function dsKy(a) { return a.join('·'); }

  /* Tính 1 đối tác: dt = đối tác, gia = giá xe (đ), loai = 'dap' | 'may', tt = % trả trước, n = kỳ hạn (tháng).
     Trả {ok:false, ly_do} (làm mờ) hoặc {ok:true, thang, bh, bh_chu, lai_chu, tt_min, vay, ...}. */
  function tinh(dt, gia, loai, tt, n) {
    var luat = null, i, vay = gia * (1 - tt / 100);
    for (i = 0; i < dt.luat.length; i++) {
      var l = dt.luat[i];
      if ((!l.loai || !l.loai.length || co(l.loai, loai)) && trongKhoang(gia, l.gia_tu || 0, l.gia_den || 0) && trongKhoang(vay, l.vay_tu || 0, l.vay_den || 0)) { luat = l; break; }
    }
    if (!luat) return { ok: false, ly_do: dt.ly_do_loai || 'Chưa có số cho loại xe này' };

    var ttMin = luat.tra_truoc_min || 0;
    var r = { tt_min: ttMin, tt_min_tien: gia * ttMin / 100 };
    if (tt < ttMin - EPS) return { ok: false, ly_do: 'Cần trả trước từ ' + pc(ttMin) + '%', tt_min: ttMin, tt_min_tien: r.tt_min_tien };
    if (luat.tra_truoc_max && tt > luat.tra_truoc_max + EPS) return { ok: false, ly_do: 'Trả trước tối đa ' + pc(luat.tra_truoc_max) + '%', tt_min: ttMin, tt_min_tien: r.tt_min_tien };
    if (luat.vay_min && vay < luat.vay_min - EPS) return { ok: false, ly_do: 'Khoản vay từ ' + pc(luat.vay_min / 1000000) + ' triệu', tt_min: ttMin, tt_min_tien: r.tt_min_tien };
    if (co(dt.ky_han_chua_co, n)) return { ok: false, ly_do: 'Chưa có mức lãi kỳ ' + n + ' tháng, chờ xác nhận', tt_min: ttMin, tt_min_tien: r.tt_min_tien };
    if (!co(luat.ky_han, n)) return { ok: false, ly_do: 'Chưa có kỳ ' + n + ' tháng (có ' + dsKy(luat.ky_han) + ')', tt_min: ttMin, tt_min_tien: r.tt_min_tien };

    var lai = null;
    for (i = 0; i < luat.lai.length; i++) {
      var e = luat.lai[i];
      if (n >= e.ky_tu && n <= e.ky_den && tt >= e.tt_tu - EPS && tt < e.tt_den - EPS) { lai = e; break; }
    }
    if (!lai) return { ok: false, ly_do: 'Chưa có mức lãi cho lựa chọn này', tt_min: ttMin, tt_min_tien: r.tt_min_tien };

    var bhc = luat.bao_hiem || { kieu: 'khong' };
    var bh = bhc.kieu === 'phan_tram' ? vay * bhc.muc / 100 : bhc.kieu === 'tien' ? bhc.muc : 0;
    var goc = vay + (bhc.tinh_lai ? bh : 0); // phần chịu lãi
    var thang, giamDan = false, cuoi = 0, tongLai = 0;
    if (dt.kieu_tinh === 'giam_dan_goc_deu') {
      /* Dư nợ giảm dần, gốc chia đều (đúng cách ví dụ bài 5970): tháng đầu = gốc/n + gốc x lãi; tháng cuối = gốc/n x (1 + lãi);
         tổng lãi = gốc x lãi x (n + 1) / 2. Bảo hiểm thu riêng (không tính lãi) KHÔNG nằm trong số góp. */
      var rg = lai.don_vi === 'nam' ? lai.lai / 1200 : lai.lai / 100;
      thang = goc / n + goc * rg; cuoi = goc / n * (1 + rg); tongLai = goc * rg * (n + 1) / 2; giamDan = true;
    } else if (dt.kieu_tinh === 'giam_dan') {
      var rt = lai.don_vi === 'nam' ? lai.lai / 1200 : lai.lai / 100;
      var niemKim = function (p) { return rt > 0 ? p * rt / (1 - Math.pow(1 + rt, -n)) : p / n; };
      thang = niemKim(goc) + (bhc.tinh_lai ? 0 : bh / n);
    } else {
      var tong = lai.don_vi === 'thang' ? lai.lai / 100 * n : lai.don_vi === 'nam' ? lai.lai / 100 * n / 12 : lai.lai / 100;
      thang = goc * (1 + tong) / n; /* bảo hiểm thu riêng (không tính lãi) KHÔNG nằm trong số góp, khớp bài 5970 */
    }
    r.ok = true; r.giam_dan = giamDan; r.cuoi = lamTron(cuoi); r.tong_lai = lamTron(tongLai); r.thang = lamTron(thang); r.vay = vay; r.bh = bh; r.lai_chu = lai.chu || ''; r.bh_loai = bhc.kieu;
    r.bh_chu = bhc.kieu === 'khong' ? 'Không có'
      : (bhc.kieu === 'phan_tram' ? pc(bhc.muc) + '% khoản vay (≈ ' + tien(lamTron(bh)) + ')' : '≈ ' + tien(bhc.muc)) + (bhc.chu ? ', ' + bhc.chu : '');
    return r;
  }

  var API = { tinh: tinh, tien: tien };
  if (typeof module !== 'undefined' && module.exports) { module.exports = API; }
  goc.PXDTraGop = API;
  if (typeof document === 'undefined') return;

  /* ---------- Phần giao diện (riêng phoxedien.vn, cùng cách vẽ thẻ như xediensmile.com) ---------- */
  var $ = function (s, g) { return (g || document).querySelector(s); };
  var $$ = function (s, g) { return Array.prototype.slice.call((g || document).querySelectorAll(s)); };
  function e(ten, lop, chu) { var x = document.createElement(ten); if (lop) x.className = lop; if (chu != null) x.textContent = chu; return x; }
  function giaTri(g) { var c = g && $('.tgp-chip[aria-pressed="true"]', g); return c ? c.dataset.v : null; }

  function theDoiTac(dt, kq) {
    var li = e('li', 'tgp-dong' + (kq.ok ? '' : ' mo'));
    var dau = e('div', 'tgp-dau');
    var lg = e('span', 'tgp-logo');
    if (dt.logo) { var im = e('img'); im.src = dt.logo; im.alt = dt.ten; im.loading = 'lazy'; im.onerror = function () { lg.textContent = dt.ten; lg.classList.add('chu'); }; lg.appendChild(im); }
    else { lg.textContent = dt.ten; lg.className += ' chu'; }
    dau.appendChild(lg);
    var gop = e('span', 'tgp-gop');
    if (kq.ok) { gop.appendChild(e('b', null, tien(kq.thang))); gop.appendChild(e('small', null, kq.giam_dan ? 'tháng đầu' : '/ tháng')); }
    else { gop.appendChild(e('span', 'tgp-ly-do', 'Chưa hỗ trợ')); }
    dau.appendChild(gop);
    li.appendChild(dau);
    var ct = e('div', 'tgp-ct');
    if (kq.tt_min != null) ct.appendChild(e('span', null, kq.tt_min > 0 ? 'Trả trước tối thiểu ' + pc(kq.tt_min) + '% (' + tien(lamTron(kq.tt_min_tien)) + ')' : 'Không bắt buộc trả trước, tuỳ hồ sơ'));
    if (kq.ok) {
      ct.appendChild(e('span', null, kq.lai_chu));
      if (kq.giam_dan) ct.appendChild(e('span', null, 'Giảm dần mỗi tháng, tháng cuối ≈ ' + tien(kq.cuoi) + ', tổng lãi ≈ ' + tien(kq.tong_lai)));
      ct.appendChild(e('span', null, 'Bảo hiểm: ' + kq.bh_chu));
    }
    if (!kq.ok && kq.ly_do) ct.appendChild(e('span', 'tgp-ghi', kq.ly_do));
    if (dt.ghi_chu && (kq.ok || !kq.ly_do)) ct.appendChild(e('span', 'tgp-ghi', dt.ghi_chu));
    if (dt.cho_anh_chot) ct.appendChild(e('span', 'tgp-cho', 'Số tham khảo, chờ xác nhận'));
    li.appendChild(ct);
    return li;
  }

  $$('[data-tgp]').forEach(function (f) {
    var dl; try { dl = JSON.parse($('[data-tgp-dl]', f).textContent); } catch (x) { return; }
    var gDong = $('[data-nhom="dong"]', f), gTt = $('[data-nhom="tra-truoc"]', f), gKh = $('[data-nhom="ky-han"]', f);
    var sel = $('[data-tgp-xe]', f), bang = $('[data-tgp-bang]', f), ttChu = $('[data-tgp-tt]', f);
    var ten = $('[data-tgp-ten]', f), gia = $('[data-tgp-gia]', f), link = $('[data-tgp-link]', f), anh = $('[data-tgp-anh]', f);
    var q = (location.search.match(/[?&]xe=([^&]+)/) || [])[1];
    if (q) { q = decodeURIComponent(q); var t = dl.xe.filter(function (x) { return x.u === '/xe/' + q + '/'; })[0]; if (t) dl.md = t.n; }

    function napMau(giu) {
      var d = giaTri(gDong), hang = {}, thu = [];
      sel.innerHTML = '';
      dl.xe.forEach(function (x, i) { if (x.d !== d) return; var b = x.b || 'Hãng khác'; if (!hang[b]) { hang[b] = []; thu.push(b); } hang[b].push(i); });
      thu.forEach(function (b) {
        var og = document.createElement('optgroup'); og.label = b + ' · ' + hang[b].length + ' xe';
        hang[b].forEach(function (i) { var x = dl.xe[i], o = document.createElement('option'); o.value = i; o.textContent = x.n + ' · ' + tien(x.g); if (x.n === giu) o.selected = true; og.appendChild(o); });
        sel.appendChild(og);
      });
    }
    function ve() {
      var x = dl.xe[parseInt(sel.value, 10)];
      bang.innerHTML = '';
      if (!x) return;
      ten.textContent = x.n; gia.textContent = tien(x.g);
      if (x.u) { link.href = x.u; link.hidden = false; } else { link.hidden = true; }
      anh.innerHTML = ''; if (x.a) { var im = e('img'); im.src = x.a; im.alt = x.n; im.width = 96; im.height = 96; im.loading = 'lazy'; anh.appendChild(im); }
      var pt = parseFloat(giaTri(gTt)) || 30, n = parseInt(giaTri(gKh), 10) || 12;
      ttChu.textContent = 'Trả trước ' + pt + '% ≈ ' + tien(lamTron(x.g * pt / 100)) + ', số vay ≈ ' + tien(lamTron(x.g * (1 - pt / 100)));
      var ul = e('ul', 'tgp-ds'), mo = [];
      dl.dt.forEach(function (dt) { var kq = tinh(dt, x.g, x.l, pt, n); if (kq.ok) ul.appendChild(theDoiTac(dt, kq)); else mo.push(theDoiTac(dt, kq)); });
      mo.forEach(function (li) { ul.appendChild(li); });
      bang.appendChild(ul);
    }
    function chon(g, sau) {
      $$('.tgp-chip', g).forEach(function (c) {
        c.addEventListener('click', function () { $$('.tgp-chip', g).forEach(function (o) { o.setAttribute('aria-pressed', o === c ? 'true' : 'false'); }); sau(); });
      });
    }
    if (dl.md) { var m0 = dl.xe.filter(function (x) { return x.n === dl.md; })[0]; if (m0) $$('.tgp-chip', gDong).forEach(function (c) { c.setAttribute('aria-pressed', c.dataset.v === m0.d ? 'true' : 'false'); }); }
    chon(gDong, function () { napMau(null); ve(); }); chon(gTt, ve); chon(gKh, ve);
    sel.addEventListener('change', ve);
    napMau(dl.md); ve();
  });
})(typeof window !== 'undefined' ? window : this);
