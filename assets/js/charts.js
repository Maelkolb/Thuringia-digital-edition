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
  // narrow screens: wrap horizontal legends into two columns so no entry is cut off
  function adaptLegends(spec, narrow) {
    if (!narrow) return spec;
    spec = JSON.parse(JSON.stringify(spec));
    (function walk(n) {
      if (Array.isArray(n)) return n.forEach(walk);
      if (n && typeof n === 'object') {
        if (Array.isArray(n.legends)) n.legends.forEach(function (l) { if (l.direction !== 'vertical' && !l.columns) { l.columns = 2; l.labelLimit = 150; } });
        Object.keys(n).forEach(function (k) { walk(n[k]); });
      }
    })(spec);
    return spec;
  }
  function draw() {
    if (!specs || !window.vega) return;
    views.forEach(function (v) { v.finalize(); }); views = [];
    var lang = document.documentElement.getAttribute('data-ui') === 'en' ? 'en' : 'de';
    vega.formatLocale(lang === 'de' ? { decimal: ',', thousands: '.', grouping: [3], currency: ['', ' Taler'] } : { decimal: '.', thousands: ',', grouping: [3], currency: ['', ' thalers'] });
    document.querySelectorAll('[data-chart]').forEach(function (el) {
      var s = specs[el.getAttribute('data-chart')]; if (!s) return;
      el.innerHTML = '';
      var spec = adaptLegends(s[lang + '_' + mode()], el.clientWidth < 600);
      var view = new vega.View(vega.parse(spec), { renderer: 'svg', container: el, hover: true });
      view.tooltip(tooltip);
      // the container carries the chart title as its accessible name; the data are in the tables below
      view.runAsync().then(function () { el.querySelectorAll('svg').forEach(function (svg) { svg.setAttribute('aria-hidden', 'true'); }); });
      views.push(view);
    });
  }
  window.addEventListener('load', function () {
    RJ.load(url).then(function (d) { specs = d; draw(); });
  });
  document.addEventListener('rj:lang', draw);
  document.addEventListener('rj:theme', draw);
  if (window.matchMedia) matchMedia('(prefers-color-scheme: dark)').addEventListener('change', draw);
  document.addEventListener('scroll', function () { tip.hidden = true; }, { passive: true });
})();
