(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Scroll reveal
  if (!reduce && 'IntersectionObserver' in window) {
    document.documentElement.classList.add('js-motion');
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('.rv').forEach(function (el) { io.observe(el); });
  }

  // Back to top: appears after one screen of scrolling
  var top = document.getElementById('totop');
  if (top) {
    var tick = false;
    function onScroll() {
      if (tick) return; tick = true;
      requestAnimationFrame(function () {
        var show = window.scrollY > window.innerHeight * 0.8;
        if (show) { top.hidden = false; requestAnimationFrame(function () { top.classList.add('show'); }); }
        else { top.classList.remove('show'); setTimeout(function () { if (!top.classList.contains('show')) top.hidden = true; }, 250); }
        tick = false;
      });
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
    top.addEventListener('click', function (e) {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
      if (history.replaceState) history.replaceState(null, '', location.pathname);
    });
  }

  // Hero: a perfused vascular network. Branching tree grown once, then particles (medium) flow through it.
  var cv = document.getElementById('vasc');
  if (!cv) return;
  var ctx = cv.getContext('2d');
  var dpr = Math.min(window.devicePixelRatio || 1, 2);
  var W, H, segs = [], parts = [];
  var css = getComputedStyle(document.documentElement);
  function tok(n) { return css.getPropertyValue(n).trim(); }

  function rnd(a, b) { return a + Math.random() * (b - a); }

  function grow(x, y, ang, len, w, depth) {
    if (depth > 9 || w < 0.5) return;
    var nx = x + Math.cos(ang) * len, ny = y + Math.sin(ang) * len;
    segs.push({ x1: x, y1: y, x2: nx, y2: ny, w: w, d: depth });
    var n = depth < 2 ? 2 : (Math.random() < 0.72 ? 2 : 1);
    for (var i = 0; i < n; i++) {
      var spread = n === 1 ? rnd(-0.25, 0.25) : (i === 0 ? rnd(0.25, 0.75) : rnd(-0.75, -0.25));
      grow(nx, ny, ang + spread, len * rnd(0.72, 0.9), w * rnd(0.6, 0.78), depth + 1);
    }
  }

  function build() {
    W = cv.clientWidth; H = cv.clientHeight;
    cv.width = W * dpr; cv.height = H * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    segs = []; parts = [];
    // Two inlets from the right edge feeding leftward, like perfusion channels into a chamber.
    grow(W + 10, H * 0.22, Math.PI + rnd(-0.1, 0.1), Math.min(W, 900) * 0.17, 5, 0);
    grow(W + 10, H * 0.55, Math.PI + rnd(-0.1, 0.1), Math.min(W, 900) * 0.16, 4.4, 0);
    grow(W + 10, H * 0.85, Math.PI + rnd(-0.1, 0.1), Math.min(W, 900) * 0.15, 3.8, 0);
    var count = Math.round(Math.min(320, segs.length * 1.3));
    for (var i = 0; i < count; i++) parts.push(newPart(true));
  }

  function newPart(anywhere) {
    var s = segs[Math.floor(Math.random() * segs.length)];
    return { s: s, t: anywhere ? Math.random() : 0, v: rnd(0.004, 0.011) * (1 + (6 - s.d) * 0.08) };
  }

  var accent, line, fg;
  function colors() { accent = tok('--accent'); line = tok('--fg-2'); fg = tok('--fg-2'); }

  function drawNet() {
    ctx.lineCap = 'round';
    for (var i = 0; i < segs.length; i++) {
      var s = segs[i];
      ctx.strokeStyle = line; ctx.lineWidth = s.w;
      ctx.globalAlpha = 0.55;
      ctx.beginPath(); ctx.moveTo(s.x1, s.y1); ctx.lineTo(s.x2, s.y2); ctx.stroke();
    }
    ctx.globalAlpha = 1;
  }

  function frame() {
    ctx.clearRect(0, 0, W, H);
    drawNet();
    ctx.fillStyle = accent;
    for (var i = 0; i < parts.length; i++) {
      var p = parts[i], s = p.s;
      p.t += p.v;
      if (p.t >= 1) { parts[i] = newPart(false); continue; }
      var x = s.x1 + (s.x2 - s.x1) * p.t, y = s.y1 + (s.y2 - s.y1) * p.t;
      var r = Math.max(1.4, s.w * 0.6);
      ctx.globalAlpha = 0.6 + 0.4 * (1 - s.d / 10);
      ctx.beginPath(); ctx.arc(x, y, r, 0, 6.283); ctx.fill();
    }
    ctx.globalAlpha = 1;
    // Soft fade toward the left where the text sits
    var g = ctx.createLinearGradient(0, 0, W, 0);
    var bg = tok('--bg');
    g.addColorStop(0, bg); g.addColorStop(0.45, bg); g.addColorStop(0.75, 'rgba(0,0,0,0)');
    ctx.globalCompositeOperation = 'destination-out';
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
    ctx.globalCompositeOperation = 'source-over';
  }

  var raf;
  function loop() { frame(); raf = requestAnimationFrame(loop); }

  colors(); build();
  if (reduce) { frame(); }
  else {
    loop();
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) cancelAnimationFrame(raf); else loop();
    });
  }
  var rt;
  window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { build(); if (reduce) frame(); }, 150); });
  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', function () { setTimeout(colors, 50); });
  }
})();
