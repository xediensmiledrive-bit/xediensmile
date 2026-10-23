/* Phố Xe Điện (bản dễ thương): logo nảy kiểu thạch, viên pin có mặt cười chớp mắt nạp đầy 5 vạch, pin nhảy mừng, rắc chấm màu. Màn hình chờ chỉ hiện lần đầu mỗi phiên, tắt khi khung trang sẵn sàng (chậm nhất 2,6 giây). Logo đầu trang nảy vào một lần. */
(function () {
  var O = '#F26B1D';
  var css =
    '#pxd-cho{position:fixed;inset:0;z-index:99999;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:26px;background:radial-gradient(circle at 50% 45%,#FFF1E6 0%,#fff 62%);transition:opacity .5s ease,visibility .5s;overflow:hidden}' +
    '#pxd-cho.xong{opacity:0;visibility:hidden}' +
    '#pxd-cho .xc-lg{width:min(62vw,300px);height:auto;opacity:0;transform:scale(.3);animation:pxdThach .9s ease-out .05s forwards}' +
    '#pxd-cho .xc-gr{position:relative;opacity:0;animation:pxdHien .25s ease .5s forwards,pxdMung .6s cubic-bezier(.3,1.6,.5,1) 1.45s}' +
    '#pxd-cho .xc-pin{display:flex;gap:5px;padding:6px;border:3.5px solid ' + O + ';border-radius:16px;background:#fff;position:relative}' +
    '#pxd-cho .xc-pin:after{content:"";position:absolute;right:-10px;top:50%;width:6px;height:14px;margin-top:-7px;border-radius:0 4px 4px 0;background:' + O + '}' +
    '#pxd-cho .xc-pin i{width:18px;height:26px;border-radius:6px;background:#FDE3D3;animation:pxdNap .16s ease forwards}' +
    '#pxd-cho .xc-mat{position:absolute;left:0;right:0;top:12px;display:flex;justify-content:center;gap:22px;pointer-events:none}' +
    '#pxd-cho .xc-mat b{width:7px;height:9px;border-radius:50%;background:#3B2314;animation:pxdChop 1.4s .75s infinite}' +
    '#pxd-cho .xc-mieng{position:absolute;left:50%;top:22px;width:14px;height:7px;margin-left:-7px;border:2.5px solid #3B2314;border-top:0;border-radius:0 0 10px 10px}' +
    '#pxd-cho .xc-ma{position:absolute;top:21px;width:9px;height:5px;border-radius:50%;background:#FF9FB0;opacity:.85}' +
    '#pxd-cho .xc-cham{position:absolute;left:50%;top:50%;width:8px;height:8px;border-radius:50%;opacity:0;animation:pxdBan .8s ease-out 1.5s forwards}' +
    '@keyframes pxdThach{0%{opacity:0;transform:scale(.3)}45%{opacity:1;transform:scale(1.12,.9)}62%{transform:scale(.94,1.06)}78%{transform:scale(1.03,.98)}to{opacity:1;transform:none}}' +
    '@keyframes pxdHien{to{opacity:1}}@keyframes pxdNap{to{background:' + O + '}}' +
    '@keyframes pxdChop{0%,86%,100%{transform:none}92%{transform:scaleY(.1)}}' +
    '@keyframes pxdMung{0%,100%{transform:none}40%{transform:translateY(-16px) scale(1.04,.96)}70%{transform:translateY(0) scale(1.06,.94)}}' +
    '@keyframes pxdBan{0%{opacity:1;transform:translate(-50%,-50%)}100%{opacity:0;transform:translate(var(--x),var(--y)) scale(.4)}}' +
    'header .logo.nay-1{animation:pxdNay .7s cubic-bezier(.3,1.6,.5,1) both}' +
    '@keyframes pxdNay{from{transform:scale(.6);opacity:0}to{transform:none;opacity:1}}' +
    '@media (prefers-reduced-motion:reduce){#pxd-cho{display:none}header .logo.nay-1{animation:none}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  var giam = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var daXem = false; try { daXem = sessionStorage.getItem('pxdCho') === '1'; } catch (e) {}
  var hoan = -1;
  if (!giam && !daXem) {
    var cho = document.createElement('div'); cho.id = 'pxd-cho'; cho.setAttribute('aria-hidden', 'true');
    var vach = ''; for (var i = 0; i < 5; i++) vach += '<i style="animation-delay:' + (0.62 + i * 0.13).toFixed(2) + 's"></i>';
    var mau = [O, '#FFC83D', '#FF9FB0', '#2BB673', O, '#FFC83D', '#FF9FB0', '#2BB673'], cham = '';
    for (var j = 0; j < 8; j++) { var g = j / 8 * 6.283; cham += '<span class="xc-cham" style="background:' + mau[j] + ';--x:' + Math.round(Math.cos(g) * 90) + 'px;--y:' + Math.round(Math.sin(g) * 70) + 'px"></span>'; }
    cho.innerHTML = '<img class="xc-lg" src="/logo.svg" alt="">' +
      '<span class="xc-gr">' +
      '<span class="xc-pin">' + vach + '</span>' +
      '<span class="xc-mat"><b></b><b></b></span><span class="xc-mieng"></span>' +
      '<span class="xc-ma" style="left:22px"></span><span class="xc-ma" style="right:28px"></span>' + cham + '</span>';
    (document.body || document.documentElement).appendChild(cho);
    var t0 = Date.now(), daTat = false;
    var tat = function () {
      if (daTat) return; daTat = true;
      var cho2 = Math.max(0, 2100 - (Date.now() - t0)); hoan = cho2 + 150;
      setTimeout(function () { cho.classList.add('xong'); setTimeout(function () { cho.remove(); }, 600); }, cho2);
    };
    if (document.readyState !== 'loading') tat(); else document.addEventListener('DOMContentLoaded', tat);
    setTimeout(tat, 2600); // mạng chậm thì vẫn tắt
    try { sessionStorage.setItem('pxdCho', '1'); } catch (e) {}
  }
  function nay() {
    if (hoan < 0) return; // chỉ nảy ngay sau màn hình chờ
    var l = document.querySelector('header .logo'); if (!l) return;
    l.style.opacity = '0';
    setTimeout(function () { l.style.opacity = ''; l.classList.add('nay-1'); }, hoan);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', nay); else nay();
})();
