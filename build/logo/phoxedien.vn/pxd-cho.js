/* Phố Xe Điện: logo bật vào rồi viên pin nạp đầy 5 vạch. Màn hình chờ chỉ hiện lần đầu mỗi phiên, tắt khi khung trang sẵn sàng (chậm nhất 2,5 giây). Logo đầu trang nảy vào một lần. */
(function () {
  var css =
    '#pxd-cho{position:fixed;inset:0;z-index:99999;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:22px;background:radial-gradient(circle at 50% 45%,#FFF1E6 0%,#fff 60%);transition:opacity .5s ease,visibility .5s}' +
    '#pxd-cho.xong{opacity:0;visibility:hidden}' +
    '#pxd-cho .xc-lg{width:min(62vw,300px);height:auto;transform:scale(.3) rotate(-8deg);opacity:0;animation:pxdBat .62s cubic-bezier(.3,1.6,.5,1) .05s forwards}' +
    '#pxd-cho .xc-pin{display:flex;gap:5px;padding:5px;border:3px solid #F26B1D;border-radius:12px;position:relative;opacity:0;animation:pxdHien .25s ease .45s forwards}' +
    '#pxd-cho .xc-pin:after{content:"";position:absolute;right:-9px;top:50%;width:5px;height:12px;margin-top:-6px;border-radius:0 3px 3px 0;background:#F26B1D}' +
    '#pxd-cho .xc-pin i{width:16px;height:20px;border-radius:4px;background:#FDE3D3;animation:pxdNap .16s ease forwards}' +
    '#pxd-cho .xc-pin.xc-day{animation:pxdHien .25s ease .45s forwards,pxdDay .45s ease 1.3s}' +
    '@keyframes pxdBat{to{transform:none;opacity:1}}@keyframes pxdHien{to{opacity:1}}' +
    '@keyframes pxdNap{to{background:#F26B1D}}@keyframes pxdDay{50%{box-shadow:0 0 0 8px rgba(242,107,29,.18);transform:scale(1.08)}}' +
    'header .logo.nay-1{animation:pxdNay .6s cubic-bezier(.3,1.6,.5,1) both}' +
    '@keyframes pxdNay{from{transform:scale(.6);opacity:0}to{transform:none;opacity:1}}' +
    '@media (prefers-reduced-motion:reduce){#pxd-cho{display:none}header .logo.nay-1{animation:none}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  var giam = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var daXem = false; try { daXem = sessionStorage.getItem('pxdCho') === '1'; } catch (e) {}
  var hoan = -1;
  if (!giam && !daXem) {
    var cho = document.createElement('div'); cho.id = 'pxd-cho'; cho.setAttribute('aria-hidden', 'true');
    var vach = ''; for (var i = 0; i < 5; i++) vach += '<i style="animation-delay:' + (0.62 + i * 0.13).toFixed(2) + 's"></i>';
    cho.innerHTML = '<img class="xc-lg" src="/logo.svg" alt=""><span class="xc-pin xc-day">' + vach + '</span>';
    (document.body || document.documentElement).appendChild(cho);
    var t0 = Date.now(), daTat = false;
    var tat = function () {
      if (daTat) return; daTat = true;
      var cho2 = Math.max(0, 1750 - (Date.now() - t0)); hoan = cho2 + 150;
      setTimeout(function () { cho.classList.add('xong'); setTimeout(function () { cho.remove(); }, 600); }, cho2);
    };
    if (document.readyState !== 'loading') tat(); else document.addEventListener('DOMContentLoaded', tat);
    setTimeout(tat, 2500); // mạng chậm thì vẫn tắt
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
