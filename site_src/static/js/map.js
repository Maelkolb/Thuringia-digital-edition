// Map of all georeferenced places (Leaflet + OSM tiles)
(function () {
  'use strict';
  var ROOT = document.body.getAttribute('data-root') || '';
  var en = function () { return document.documentElement.getAttribute('data-ui') === 'en'; };
  var esc = function (s) { return RJ.esc(s == null ? '' : s); };
  window.addEventListener('load', function () {
    var map = L.map('map', { zoomSnap: 0.25, preferCanvas: true }).setView([50.62, 11.82], 10);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
    var css = getComputedStyle(document.documentElement);
    var cPlace = css.getPropertyValue('--e-place').trim() || '#2a78d6';
    var cNature = css.getPropertyValue('--e-nature').trim() || '#008300';
    fetch(ROOT + 'karte/orte.json').then(function (r) { return r.json(); }).then(function (feats) {
      var layer = L.layerGroup().addTo(map), markers = {};
      var list = document.getElementById('map-list'), detail = document.getElementById('map-detail');
      var filter = document.querySelector('[data-map-filter]'), sel = document.querySelector('[data-map-layer]');
      function radius(f) { return Math.max(4, Math.min(22, 3 + Math.sqrt(f.n) * 1.4)); }
      function show(f) {
        var g = f.g, h = '<div class="card app-block" style="margin-bottom:14px"><h2>' + (f.c === 'nature' ? (en() ? 'Natural feature' : 'Natur') : (en() ? 'Place' : 'Ort')) + (f.k ? ' · ' + esc(f.k) : '') + '</h2>' +
          '<h3 style="margin:0 0 6px;font:600 1.15rem var(--serif)">' + esc(f.l) + '</h3>';
        if (g) {
          var facts = [esc(g.type)];
          if (g.inh) facts.push(g.inh + (en() ? ' inhabitants' : ' Einwohner'));
          if (g.houses) facts.push(g.houses + (en() ? ' houses' : ' Häuser'));
          if (g.first) facts.push((en() ? 'first record ' : 'urkundl. ') + g.first);
          h += '<p style="font-size:.9rem">' + facts.join(' · ') + '</p><p style="font:400 .95rem/1.5 var(--serif)">' + esc(en() ? g.en : g.de) + '</p>' +
            '<p><a class="small-btn" href="' + ROOT + 'seite/' + g.page + '.html#' + g.block + '">' + (en() ? 'Place article p. ' : 'Ortsartikel S. ') + g.page + '</a> ';
        } else h += '<p>';
        h += '<a class="small-btn" href="' + ROOT + f.href + '">' + (en() ? 'Index entry' : 'Registereintrag') + '</a></p>';
        h += '<p class="muted" style="font-size:.85rem">' + f.n + (en() ? ' mentions; pp. ' : ' Erwähnungen; S. ') + f.p.map(function (p) { return '<a href="' + ROOT + 'seite/' + p + '.html?hl=' + encodeURIComponent(f.l) + '">' + p + '</a>'; }).join(', ') + (f.n > f.p.length ? ' …' : '') + '</p></div>';
        detail.innerHTML = h;
      }
      function draw() {
        layer.clearLayers(); list.innerHTML = '';
        var q = RJNorm.fold((filter.value || '').trim()), mode = sel.value, shown = [];
        feats.forEach(function (f) {
          if (mode === 'gaz' && !f.g) return;
          if (mode === 'nature' ? f.c !== 'nature' : (mode !== 'all' && f.c === 'nature')) return;
          if (mode === 'all' && f.c === 'nature') return;
          if (q && RJNorm.fold(f.l).indexOf(q) < 0) return;
          var col = f.c === 'nature' ? cNature : cPlace;
          var m = L.circleMarker([f.lat, f.lon], { radius: radius(f), color: col, weight: 1.5, fillColor: col, fillOpacity: f.g ? 0.55 : 0.12 });
          m.bindTooltip(esc(f.l) + ' (' + f.n + ')');
          m.on('click', function () { show(f); history.replaceState(null, '', '#' + f.id); });
          m.addTo(layer); markers[f.id] = m; shown.push(f);
        });
        shown.sort(function (a, b) { return b.n - a.n; });
        list.innerHTML = shown.slice(0, 200).map(function (f) {
          return '<li class="reg-item" style="padding:6px 0"><div><a href="#' + f.id + '" data-f="' + f.id + '">' + esc(f.l) + '</a> <span class="kind">' + esc(f.k) + '</span></div><div class="auth"><span class="n">' + f.n + '×</span></div></li>';
        }).join('');
      }
      list.addEventListener('click', function (e) {
        var a = e.target.closest('[data-f]'); if (!a) return; e.preventDefault();
        var f = feats.find(function (x) { return x.id === a.getAttribute('data-f'); });
        map.setView([f.lat, f.lon], Math.max(map.getZoom(), 12)); show(f); history.replaceState(null, '', '#' + f.id);
      });
      filter.addEventListener('input', draw); sel.addEventListener('change', draw);
      draw();
      var inside = feats.filter(function (f) { return f.in && f.c === 'place'; });
      if (inside.length) map.fitBounds(L.latLngBounds(inside.map(function (f) { return [f.lat, f.lon]; })).pad(0.08));
      if (location.hash) {
        var f = feats.find(function (x) { return x.id === decodeURIComponent(location.hash.slice(1)); });
        if (f) { map.setView([f.lat, f.lon], 13); show(f); }
      }
      document.addEventListener('rj:lang', function () { draw(); });
    });
  });
})();
