// Brückner 1870 – digital edition: shared behaviour (no framework, no build step)
(function () {
  'use strict';
  var doc = document.documentElement;
  var ROOT = document.body.getAttribute('data-root') || '';
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function $(s, el) { return (el || document).querySelector(s); }
  function $$(s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); }
  function ui() { return doc.getAttribute('data-ui') || 'de'; }
  window.RJ = { root: ROOT, ui: ui, store: store };

  // ------------------------------------------------------------ language / theme / menu
  var lt = $('[data-lang-toggle]');
  if (lt) lt.addEventListener('click', function () {
    var next = ui() === 'de' ? 'en' : 'de';
    doc.setAttribute('data-ui', next); store('rj.ui', next);
    document.dispatchEvent(new CustomEvent('rj:lang', { detail: next }));
  });
  var tt = $('[data-theme-toggle]');
  if (tt) tt.addEventListener('click', function () {
    var cur = doc.getAttribute('data-theme');
    if (!cur) cur = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    var next = cur === 'dark' ? 'light' : 'dark';
    doc.setAttribute('data-theme', next); store('rj.theme', next);
    document.dispatchEvent(new CustomEvent('rj:theme', { detail: next }));
  });
  var mt = $('[data-menu]'), nav = $('[data-nav]');
  if (mt && nav) mt.addEventListener('click', function () {
    var open = nav.classList.toggle('open'); mt.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  $$('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var src = $(b.getAttribute('data-copy'));
      if (!src || !navigator.clipboard) return;
      navigator.clipboard.writeText(src.innerText.trim()).then(function () {
        var old = b.innerHTML; b.textContent = '✓'; setTimeout(function () { b.innerHTML = old; }, 1400);
      });
    });
  });

  // citation URLs: fill in the real address when no base URL is configured
  $$('[data-url]').forEach(function (s) {
    var v = s.textContent.trim();
    if (!/^https?:/.test(v)) s.textContent = location.origin + location.pathname;
  });
  $$('[data-url-root]').forEach(function (s) {
    if (!/^https?:/.test(s.textContent.trim())) s.textContent = location.origin + location.pathname.replace(/edition\/[^/]*$/, '');
  });

  // ------------------------------------------------------------ quick search
  var KIND = {
    place: ['Ort', 'Place'], nature: ['Natur', 'Nature'], person: ['Person', 'Person'], organisation: ['Institution', 'Institution'],
    organism: ['Tier/Pflanze', 'Organism'], concept: ['Sache', 'Thing'], section: ['Kapitel', 'Chapter'],
    analysis: ['Auswertung', 'Analysis'], glossary: ['Glossar', 'Glossary'], page: ['Seite', 'Page']
  };
  window.RJ.kindLabel = function (k) { var l = KIND[k] || [k, k]; return ui() === 'en' ? l[1] : l[0]; };
  var qsForm = $('[data-quicksearch]');
  if (qsForm) {
    var input = $('input', qsForm), box = $('.qs-results', qsForm), quick = null, sel = -1, items = [];
    var load = function () {
      if (quick) return Promise.resolve(quick);
      return fetch(ROOT + 'suche/quick.json').then(function (r) { return r.json(); }).then(function (d) {
        quick = d.map(function (x) { return { label: x[0], kind: x[1], href: x[2], n: x[3], key: RJNorm.fold(x[0]) }; });
        return quick;
      });
    };
    var render = function () {
      var q = input.value.trim();
      if (!q) { box.classList.remove('open'); return; }
      load().then(function (list) {
        var fq = RJNorm.fold(q), out = [];
        if (/^(s\.?\s*)?[0-9]{1,3}$|^[IVX]+$/i.test(q)) {
          var p = q.replace(/^s\.?\s*/i, '');
          out.push({ label: (ui() === 'en' ? 'Page ' : 'Seite ') + p, kind: 'page', href: 'seite/' + p + '.html', n: 0 });
        }
        var starts = [], contains = [];
        for (var i = 0; i < list.length; i++) {
          var it = list[i], pos = it.key.indexOf(fq);
          if (pos === 0) starts.push(it); else if (pos > 0) contains.push(it);
        }
        var byN = function (a, b) { return (b.n - a.n) || a.label.localeCompare(b.label, 'de'); };
        out = out.concat(starts.sort(byN), contains.sort(byN)).slice(0, 12);
        items = out; sel = -1;
        var html = '', last = null;
        out.forEach(function (it, i) {
          if (it.kind !== last) { html += '<div class="grp">' + RJ.kindLabel(it.kind) + '</div>'; last = it.kind; }
          html += '<a role="option" href="' + ROOT + it.href + '" data-i="' + i + '"><span>' + escapeHtml(it.label) + '</span><span class="meta">' + (it.n ? it.n + '×' : '') + '</span></a>';
        });
        html += '<div class="grp">' + (ui() === 'en' ? 'Full text' : 'Volltext') + '</div><a role="option" href="' + ROOT + 'suche.html?q=' + encodeURIComponent(q) + '"><span>„' + escapeHtml(q) + '“ ' + (ui() === 'en' ? 'in the whole book' : 'im ganzen Buch') + '</span><span class="meta">↵</span></a>';
        box.innerHTML = html; box.classList.add('open');
      });
    };
    input.addEventListener('input', render);
    input.addEventListener('focus', function () { load(); if (input.value) render(); });
    input.addEventListener('keydown', function (e) {
      var links = $$('a', box);
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        sel = Math.max(-1, Math.min(links.length - 1, sel + (e.key === 'ArrowDown' ? 1 : -1)));
        links.forEach(function (a, i) { a.setAttribute('aria-selected', i === sel ? 'true' : 'false'); });
      } else if (e.key === 'Enter' && sel >= 0 && links[sel]) { e.preventDefault(); location.href = links[sel].href; }
      else if (e.key === 'Escape') { box.classList.remove('open'); }
    });
    document.addEventListener('click', function (e) { if (!qsForm.contains(e.target)) box.classList.remove('open'); });
  }
  function escapeHtml(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  window.RJ.esc = escapeHtml;

  // ------------------------------------------------------------ page view
  if (!document.body.classList.contains('page-view')) return;
  var body = document.body;
  var entsBtn = $('[data-toggle-ents]'), facsBtn = $('[data-toggle-facs]');
  function setEnts(on) { body.classList.toggle('no-ents', !on); entsBtn.setAttribute('aria-pressed', on ? 'true' : 'false'); }
  function setFacs(on) { body.classList.toggle('no-facs', !on); facsBtn.setAttribute('aria-pressed', on ? 'true' : 'false'); if (on) initViewer(); }
  setEnts(store('rj.ents') !== 'off');
  // narrow screens: text first, facsimile on demand (unless the reader chose otherwise)
  var facsPref = store('rj.facs');
  setFacs(facsPref ? facsPref !== 'off' : window.innerWidth > 1100);
  entsBtn.addEventListener('click', function () { var on = body.classList.contains('no-ents'); setEnts(on); store('rj.ents', on ? 'on' : 'off'); });
  facsBtn.addEventListener('click', function () { var on = body.classList.contains('no-facs'); setFacs(on); store('rj.facs', on ? 'on' : 'off'); });

  document.addEventListener('keydown', function (e) {
    if (e.target.closest('input, textarea, select') || e.altKey || e.ctrlKey || e.metaKey) return;
    var a = e.key === 'ArrowLeft' ? $('[data-prev]') : e.key === 'ArrowRight' ? $('[data-next]') : null;
    if (a) location.href = a.href;
  });
  var gf = $('[data-goto]');
  if (gf) gf.addEventListener('submit', function (e) {
    e.preventDefault();
    var v = $('input', gf).value.trim().replace(/^s\.?\s*/i, '');
    if (v) location.href = v.toUpperCase() === v && /^[IVX]+$/i.test(v) ? v.toUpperCase() + '.html' : v + '.html';
  });

  // entity tooltips + highlighting of all mentions of an entity
  var ents = {};
  try { ents = JSON.parse($('#page-entities').textContent); } catch (e) {}
  var tip = document.createElement('div'); tip.className = 'ent-tip'; tip.hidden = true; document.body.appendChild(tip);
  function showTip(el) {
    var e = ents[el.getAttribute('data-e')]; if (!e) return;
    var k = RJ.kindLabel(e.c);
    tip.innerHTML = '<span class="k" style="color:var(--e-' + e.c + ')">' + k + (e.k ? ' · ' + escapeHtml(e.k) : '') + '</span><b>' + escapeHtml(e.l) + '</b>' +
      (e.m ? '<span class="muted">' + escapeHtml(e.m) + '</span><br>' : '') +
      (e.d ? escapeHtml(ui() === 'en' && e.de ? e.de : e.d) + '<br>' : '') +
      '<span class="muted">' + e.n + (ui() === 'en' ? ' mentions in the book' : ' Erwähnungen im Buch') + '</span>';
    var r = el.getBoundingClientRect();
    tip.hidden = false;
    var left = Math.min(window.scrollX + r.left, window.scrollX + document.documentElement.clientWidth - tip.offsetWidth - 12);
    tip.style.left = Math.max(8, left) + 'px';
    tip.style.top = (window.scrollY + r.bottom + 6) + 'px';
  }
  $$('.transcription .ent, .footnotes .ent').forEach(function (el) {
    el.addEventListener('mouseenter', function () { if (!body.classList.contains('no-ents')) showTip(el); });
    el.addEventListener('mouseleave', function () { tip.hidden = true; });
    el.addEventListener('focus', function () { showTip(el); });
    el.addEventListener('blur', function () { tip.hidden = true; });
  });
  $$('.chip[data-e]').forEach(function (c) {
    var id = c.getAttribute('data-e');
    var targets = $$('.ent[data-e="' + CSS.escape(id) + '"]');
    c.addEventListener('mouseenter', function () { targets.forEach(function (t) { t.classList.add('hl'); }); });
    c.addEventListener('mouseleave', function () { targets.forEach(function (t) { t.classList.remove('hl'); }); });
  });

  // highlight search terms (?hl=…)
  var hl = new URLSearchParams(location.search).get('hl');
  if (hl && window.RJNorm) {
    var want = {};
    RJNorm.tokens(hl).forEach(function (w) { want[RJNorm.norm(w)] = true; });
    var first = null;
    $$('.transcription, .footnotes').forEach(function (root) {
      var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null), nodes = [];
      while (walker.nextNode()) nodes.push(walker.currentNode);
      nodes.forEach(function (n) {
        var txt = n.nodeValue, re = /[0-9]+|[A-Za-zÀ-ÖØ-öø-ÿſ]+/g, m, last = 0, frag = null;
        while ((m = re.exec(txt))) {
          if (want[RJNorm.norm(m[0])]) {
            frag = frag || document.createDocumentFragment();
            frag.appendChild(document.createTextNode(txt.slice(last, m.index)));
            var mk = document.createElement('mark'); mk.className = 'hit'; mk.textContent = m[0]; frag.appendChild(mk);
            first = first || mk; last = m.index + m[0].length;
          }
        }
        if (frag) { frag.appendChild(document.createTextNode(txt.slice(last))); n.parentNode.replaceChild(frag, n); }
      });
    });
    if (first && !location.hash) first.scrollIntoView({ block: 'center' });
  }

  // IIIF deep zoom (OpenSeadragon, BSB image service); static image as fallback
  var viewerStarted = false;
  function initViewer() {
    if (viewerStarted) return;
    var box = $('#facs'); if (!box) return;
    var start = function () {
      if (!window.OpenSeadragon) return;
      viewerStarted = true;
      var v = OpenSeadragon({
        element: box, tileSources: box.getAttribute('data-iiif'), showNavigationControl: false, showNavigator: false,
        visibilityRatio: 0.6, minZoomImageRatio: 0.6, maxZoomPixelRatio: 2.5, gestureSettingsMouse: { clickToZoom: false, dblClickToZoom: true },
        crossOriginPolicy: 'Anonymous', preserveImageSizeOnResize: true, animationTime: 0.4
      });
      v.addHandler('open', function () { var s = $('img.static', box); if (s) s.remove(); });
      var ctl = document.createElement('div'); ctl.className = 'facs-controls';
      ctl.innerHTML = '<button type="button" data-z="in" aria-label="Zoom in">+</button><button type="button" data-z="out" aria-label="Zoom out">−</button><button type="button" data-z="home" aria-label="Fit">⤢</button><button type="button" data-z="full" aria-label="Fullscreen">⛶</button>';
      box.appendChild(ctl);
      ctl.addEventListener('click', function (e) {
        var z = e.target.getAttribute('data-z');
        if (z === 'in') v.viewport.zoomBy(1.4); else if (z === 'out') v.viewport.zoomBy(1 / 1.4);
        else if (z === 'home') v.viewport.goHome(); else if (z === 'full') v.setFullScreen(!v.isFullPage());
      });
    };
    if (window.OpenSeadragon) start(); else window.addEventListener('load', start);
  }
  if (!body.classList.contains('no-facs')) initViewer();
})();
