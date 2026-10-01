// Analysis charts: precompiled Vega specs (de/en x light/dark), shared theme
(function () {
  'use strict';
  var me = document.currentScript, url = me.getAttribute('data-spec');
  var specs = null, views = [];
  var tip = document.createElement('div'); tip.className = 'vg-tip'; tip.hidden = true; document.body.appendChild(tip);
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function fmt(v) {
    if (typeof v === 'number') return v.toLocaleString(document.documentElement.getAttribute('data-ui') === 'en' ? 'en-US' : 'de-DE', { maximumFractionDigits: 3 });
    return v;
  }
  function tooltip(handler, event, item, value) {
    if (value == null || value === '') { tip.hidden = true; return; }
    var html;
    if (typeof value === 'object') {
      html = '<table>' + Object.keys(value).map(function (k) { return '<tr><td class="k">' + esc(k) + '</td><td>' + esc(fmt(value[k])) + '</td></tr>'; }).join('') + '</table>';
    } else html = esc(fmt(value));
    tip.innerHTML = html; tip.hidden = false;
    var x = event.clientX + 14, y = event.clientY + 14;
    if (x + tip.offsetWidth > window.innerWidth - 8) x = event.clientX - tip.offsetWidth - 14;
    if (y + tip.offsetHeight > window.innerHeight - 8) y = event.clientY - tip.offsetHeight - 14;
    tip.style.left = x + 'px'; tip.style.top = y + 'px';
  }
  function mode() {
    var t = document.documentElement.getAttribute('data-theme');
    if (t) return t;
    return window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  function draw() {
    if (!specs || !window.vega) return;
    views.forEach(function (v) { v.finalize(); }); views = [];
    var lang = document.documentElement.getAttribute('data-ui') === 'en' ? 'en' : 'de';
    document.querySelectorAll('[data-chart]').forEach(function (el) {
      var s = specs[el.getAttribute('data-chart')]; if (!s) return;
      el.innerHTML = '';
      var view = new vega.View(vega.parse(s[lang + '_' + mode()]), { renderer: 'svg', container: el, hover: true });
      view.tooltip(tooltip);
      view.runAsync();
      views.push(view);
    });
  }
  window.addEventListener('load', function () {
    fetch(url).then(function (r) { return r.json(); }).then(function (d) { specs = d; draw(); });
  });
  document.addEventListener('rj:lang', draw);
  document.addEventListener('rj:theme', draw);
  if (window.matchMedia) matchMedia('(prefers-color-scheme: dark)').addEventListener('change', draw);
  document.addEventListener('scroll', function () { tip.hidden = true; }, { passive: true });
})();
