// Brückner 1870 – digital edition: shared behaviour (no framework, no build step)
(function () {
  'use strict';
  var doc = document.documentElement;
  var ROOT = document.body.getAttribute('data-root') || '';
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function $(s, el) { return (el || document).querySelector(s); }
  function $$(s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); }
  function ui() { return doc.getAttribute('data-ui') || 'de'; }
  function escapeHtml(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function fmt(n) { return Number(n).toLocaleString(ui() === 'en' ? 'en-GB' : 'de-DE'); }
  window.RJ = { root: ROOT, ui: ui, store: store, esc: escapeHtml, fmt: fmt };

  // Data files are scripts calling RJ.put(key, data): browsers block fetch() on pages opened from disk (file://).
  var dataStore = {}, dataWait = {};
  RJ.put = function (key, data) { dataStore[key] = data; if (dataWait[key]) dataWait[key].resolve(data); };
  RJ.load = function (key) {
    if (key in dataStore) return Promise.resolve(dataStore[key]);
    if (dataWait[key]) return dataWait[key].promise;
    var wait = dataWait[key] = {};
    wait.promise = new Promise(function (resolve, reject) {
      wait.resolve = resolve;
      var s = document.createElement('script');
      s.src = ROOT + key.split('/').map(encodeURIComponent).join('/') + '.js';
      s.onload = function () { if (!(key in dataStore)) { delete dataWait[key]; reject(new Error('no data: ' + key)); } };
      s.onerror = function () { delete dataWait[key]; s.remove(); reject(new Error('missing: ' + key)); };
      document.head.appendChild(s);
    });
    return wait.promise;
  };

  // ------------------------------------------------------------ language / theme / menu
  var ATTRS = ['placeholder', 'aria-label', 'title', 'alt'];
  function applyLang(lang) {
    doc.setAttribute('data-ui', lang);
    doc.lang = lang;
    $$('[data-en-placeholder], [data-en-aria-label], [data-en-title], [data-en-alt]').forEach(function (el) {
      ATTRS.forEach(function (a) { var v = el.getAttribute('data-' + lang + '-' + a); if (v !== null) el.setAttribute(a, v); });
    });
    $$('[data-en-text]').forEach(function (el) { el.textContent = el.getAttribute('data-' + lang + '-text'); });
  }
  applyLang(ui());
  var lt = $('[data-lang-toggle]');
  if (lt) lt.addEventListener('click', function () {
    var next = ui() === 'de' ? 'en' : 'de';
    applyLang(next); store('rj.ui', next);
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

  // ------------------------------------------------------------ citations
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    var ta = document.createElement('textarea');
    ta.value = text; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select();
    try { document.execCommand('copy'); } finally { ta.remove(); }
    return Promise.resolve();
  }
  $$('[data-copy]').forEach(function (b) {
    var label = b.innerHTML;
    b.addEventListener('click', function () {
      var src = $(b.getAttribute('data-copy')); if (!src) return;
      copyText(src.innerText.replace(/\s+/g, ' ').trim()).then(function () {
        b.textContent = b.getAttribute('data-done-' + ui()) || 'OK';
        setTimeout(function () { b.innerHTML = label; }, 1600);
      });
    });
  });
  // without a configured base URL, cite the address the edition is actually opened from
  $$('[data-url]').forEach(function (s) {
    if (/^https?:/.test(s.textContent.trim())) return;
    var path = s.getAttribute('data-path');
    s.textContent = path ? new URL(ROOT + path, location.href).href : location.href.split(/[?#]/)[0];
  });

  // ------------------------------------------------------------ quick search
  var KIND = {
    place: ['Ort', 'Place'], nature: ['Natur', 'Nature'], person: ['Person', 'Person'], organisation: ['Institution', 'Institution'],
    organism: ['Tier oder Pflanze', 'Animal or plant'], concept: ['Sache', 'Thing'], section: ['Kapitel', 'Chapter'],
    analysis: ['Auswertung', 'Analysis'], glossary: ['Glossar', 'Glossary'], page: ['Seite', 'Page']
  };
  RJ.kindLabel = function (k) { var l = KIND[k] || [k, k]; return ui() === 'en' ? l[1] : l[0]; };
  RJ.passages = function (n) { return fmt(n) + (ui() === 'en' ? (n === 1 ? ' passage' : ' passages') : (n === 1 ? ' Stelle' : ' Stellen')); };
  var qsForm = $('[data-quicksearch]');
  if (qsForm) {
    var input = $('input', qsForm), box = $('.qs-results', qsForm), quick = null, sel = -1;
    var load = function () {
      if (quick) return Promise.resolve(quick);
      return RJ.load('suche/quick').then(function (d) {
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
        sel = -1;
        var html = '', last = null;
        out.forEach(function (it, i) {
          if (it.kind !== last) { html += '<div class="grp">' + RJ.kindLabel(it.kind) + '</div>'; last = it.kind; }
          html += '<a role="option" href="' + ROOT + it.href + '" data-i="' + i + '"><span>' + escapeHtml(it.label) + '</span><span class="meta">' + (it.n ? RJ.passages(it.n) : '') + '</span></a>';
        });
        html += '<div class="grp">' + (ui() === 'en' ? 'Full text' : 'Volltext') + '</div><a role="option" href="' + ROOT + 'suche.html?q=' + encodeURIComponent(q) + '"><span>' +
          (ui() === 'en' ? 'Search the whole book for “' : 'Im ganzen Buch nach „') + escapeHtml(q) + (ui() === 'en' ? '”' : '“ suchen') + '</span></a>';
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

  // ------------------------------------------------------------ page view
  if (!document.body.classList.contains('page-view')) return;
  var body = document.body;
  function toggle(btn, onChange) {
    if (!btn) return function () {};
    var set = function (on) { btn.setAttribute('aria-pressed', on ? 'true' : 'false'); onChange(on); };
    btn.addEventListener('click', function () { var on = btn.getAttribute('aria-pressed') !== 'true'; set(on); btn.dispatchEvent(new CustomEvent('rj:toggle', { detail: on })); });
    return set;
  }
  var setEnts = toggle($('[data-toggle-ents]'), function (on) { body.classList.toggle('no-ents', !on); store('rj.ents', on ? 'on' : 'off'); });
  var setLinesView = toggle($('[data-toggle-lines]'), function (on) { body.classList.toggle('show-lines', on); store('rj.lines', on ? 'on' : 'off'); });
  var setFacs = toggle($('[data-toggle-facs]'), function (on) { body.classList.toggle('no-facs', !on); store('rj.facs', on ? 'on' : 'off'); if (on) initViewer(); });
  setEnts(store('rj.ents') !== 'off');
  setLinesView(store('rj.lines') === 'on');
  // narrow screens: text first, facsimile on demand (unless the reader chose otherwise)
  var facsPref = store('rj.facs');
  body.classList.toggle('no-facs', !(facsPref ? facsPref !== 'off' : window.innerWidth > 1100));
  $('[data-toggle-facs]').setAttribute('aria-pressed', body.classList.contains('no-facs') ? 'false' : 'true');

  var citeBtn = $('[data-cite-toggle]'), citePanel = $('#cite');
  if (citeBtn && citePanel) {
    citeBtn.addEventListener('click', function () {
      var open = citePanel.hidden;
      citePanel.hidden = !open; citeBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !citePanel.hidden) { citePanel.hidden = true; citeBtn.setAttribute('aria-expanded', 'false'); citeBtn.focus(); }
    });
  }

  document.addEventListener('keydown', function (e) {
    if (e.target.closest('input, textarea, select') || e.altKey || e.ctrlKey || e.metaKey) return;
    var a = e.key === 'ArrowLeft' ? $('[data-prev]') : e.key === 'ArrowRight' ? $('[data-next]') : null;
    if (a) location.href = a.href;
  });
  var gf = $('[data-goto]');
  if (gf) gf.addEventListener('submit', function (e) {
    e.preventDefault();
    var v = $('input', gf).value.trim().replace(/^s\.?\s*/i, '');
    if (v) location.href = /^[IVX]+$/i.test(v) ? v.toUpperCase() + '.html' : v + '.html';
  });

  // entity tooltips + highlighting of all mentions of an entity
  var ents = {};
  try { ents = JSON.parse($('#page-entities').textContent); } catch (e) {}
  var tip = document.createElement('div'); tip.className = 'ent-tip'; tip.hidden = true; document.body.appendChild(tip);
  function showTip(el) {
    var e = ents[el.getAttribute('data-e')]; if (!e) return;
    tip.innerHTML = '<span class="k"><span class="swatch" style="--ec:var(--e-' + e.c + ')"></span>' + RJ.kindLabel(e.c) + (e.k ? ', ' + escapeHtml(e.k) : '') + '</span><b>' + escapeHtml(e.l) + '</b>' +
      (e.m ? '<span class="muted">' + escapeHtml(e.m) + '</span><br>' : '') +
      (e.d ? escapeHtml(ui() === 'en' && e.de ? e.de : e.d) + '<br>' : '') +
      '<span class="muted">' + RJ.passages(e.n) + (ui() === 'en' ? ' in the book' : ' im Buch') + '</span>';
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
  $$('.names a[data-e]').forEach(function (c) {
    var targets = $$('.ent[data-e="' + CSS.escape(c.getAttribute('data-e')) + '"]');
    c.addEventListener('mouseenter', function () { targets.forEach(function (t) { t.classList.add('hl'); }); });
    c.addEventListener('mouseleave', function () { targets.forEach(function (t) { t.classList.remove('hl'); }); });
  });

  // highlight search terms (?hl=…)
  var marks = [];
  var hl = new URLSearchParams(location.search).get('hl');
  if (hl && window.RJNorm) {
    var want = {};
    RJNorm.tokens(hl).forEach(function (w) { want[RJNorm.norm(w)] = true; });
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
            marks.push(mk); last = m.index + m[0].length;
          }
        }
        if (frag) { frag.appendChild(document.createTextNode(txt.slice(last))); n.parentNode.replaceChild(frag, n); }
      });
    });
    if (marks.length && !location.hash) marks[0].scrollIntoView({ block: 'center' });
  }

  // ------------------------------------------------------------ printed lines: text <-> facsimile
  var LINES = null;
  try { LINES = JSON.parse($('#page-lines').textContent); } catch (e) {}
  var lineById = {}, lbs = $$('.lb'), BLOCK = 'p, li, h2, h3, h4, h5, h6, .footnotes p';
  if (LINES) LINES.l.forEach(function (l) { lineById[l[0]] = l; });
  var viewer = null, hoverZone = document.createElement('div'), blockZone = document.createElement('div');
  hoverZone.className = 'zone'; blockZone.className = 'zone block';

  function rect(box) { return viewer.viewport.imageToViewportRectangle(box[0], box[1], box[2], box[3]); }
  function showZone(el, box) {
    if (!viewer || !box) return hideZone(el);
    if (el.parentNode && el._overlay) viewer.updateOverlay(el, rect(box));
    else { viewer.addOverlay({ element: el, location: rect(box) }); el._overlay = true; }
  }
  function hideZone(el) { if (viewer && el._overlay) { viewer.removeOverlay(el); el._overlay = false; } }
  function boxOf(line) { return line ? line.slice(3, 7) : null; }

  // the last line start (.lb) before a DOM position, if it belongs to the same block
  function lineStartBefore(node) {
    var lo = 0, hi = lbs.length - 1, found = -1;
    while (lo <= hi) {
      var mid = (lo + hi) >> 1;
      if (lbs[mid] === node || (lbs[mid].compareDocumentPosition(node) & Node.DOCUMENT_POSITION_FOLLOWING)) { found = mid; lo = mid + 1; } else hi = mid - 1;
    }
    if (found < 0) return -1;
    var blk = node.nodeType === 1 ? node.closest(BLOCK) : node.parentNode && node.parentNode.closest(BLOCK);
    return blk && lbs[found].closest(BLOCK) === blk ? found : -1;
  }
  function caretNode(x, y) {
    if (document.caretPositionFromPoint) { var p = document.caretPositionFromPoint(x, y); return p && (p.offsetNode.childNodes[p.offset] || p.offsetNode); }
    if (document.caretRangeFromPoint) { var r = document.caretRangeFromPoint(x, y); return r && (r.startContainer.childNodes[r.startOffset] || r.startContainer); }
    return null;
  }
  function textRange(i) {
    var r = document.createRange(), blk = lbs[i].closest(BLOCK), next = lbs[i + 1];
    r.setStartAfter(lbs[i]);
    if (next && next.closest(BLOCK) === blk) r.setEndBefore(next); else r.setEnd(blk, blk.childNodes.length);
    return r;
  }
  function markText(i) {
    if (!window.CSS || !CSS.highlights || typeof Highlight === 'undefined') return;
    if (i < 0) CSS.highlights.delete('line'); else CSS.highlights.set('line', new Highlight(textRange(i)));
  }
  function clearSync() { hideZone(hoverZone); hideZone(blockZone); markText(-1); }

  if (LINES) {
    var pending = null;
    $$('.transcription, .footnotes').forEach(function (root) {
      root.addEventListener('mousemove', function (e) {
        if (pending || !viewer) return;
        pending = requestAnimationFrame(function () {
          pending = null;
          var node = caretNode(e.clientX, e.clientY), i = node ? lineStartBefore(node) : -1;
          if (i >= 0) {
            showZone(hoverZone, boxOf(lineById[lbs[i].getAttribute('data-line')])); hideZone(blockZone); markText(i);
            return;
          }
          var blk = e.target.closest('.tbl, ' + BLOCK), id = blk && (blk.id || (blk.closest('[id]') || {}).id);
          markText(-1); hideZone(hoverZone);
          if (id && LINES.r[id]) showZone(blockZone, LINES.r[id]); else hideZone(blockZone);
        });
      });
      root.addEventListener('mouseleave', clearSync);
    });
  }
  function lineAt(x, y) {
    if (!LINES) return null;
    for (var k = 0; k < LINES.l.length; k++) {
      var l = LINES.l[k];
      if (x >= l[3] && x <= l[3] + l[5] && y >= l[4] && y <= l[4] + l[6]) return l;
    }
    return null;
  }
  function lbIndex(id) { for (var k = 0; k < lbs.length; k++) if (lbs[k].getAttribute('data-line') === id) return k; return -1; }
  function attachViewerSync() {
    if (!LINES) return;
    new OpenSeadragon.MouseTracker({
      element: viewer.canvas,
      moveHandler: function (ev) {
        var p = viewer.viewport.viewportToImageCoordinates(viewer.viewport.pointFromPixel(ev.position));
        var l = lineAt(p.x, p.y);
        if (!l) { clearSync(); return; }
        showZone(hoverZone, boxOf(l));
        var i = lbIndex(l[0]); markText(i);
      },
      leaveHandler: clearSync
    });
    viewer.addHandler('canvas-click', function (ev) {
      if (!ev.quick) return;
      var p = viewer.viewport.viewportToImageCoordinates(viewer.viewport.pointFromPixel(ev.position));
      var l = lineAt(p.x, p.y), i = l ? lbIndex(l[0]) : -1;
      if (i >= 0) { var r = textRange(i).getBoundingClientRect(); window.scrollBy({ top: r.top - window.innerHeight / 2, behavior: 'smooth' }); }
    });
    // search hits on the facsimile
    var seen = {};
    marks.forEach(function (mk) {
      var i = lineStartBefore(mk); if (i < 0) return;
      var id = lbs[i].getAttribute('data-line'); if (seen[id]) return; seen[id] = true;
      var z = document.createElement('div'); z.className = 'zone hit';
      viewer.addOverlay({ element: z, location: rect(boxOf(lineById[id])) });
    });
  }

  // IIIF deep zoom (OpenSeadragon, BSB image service); static image as fallback
  var viewerStarted = false;
  function initViewer() {
    if (viewerStarted) return;
    var box = $('#facs'); if (!box) return;
    var start = function () {
      if (!window.OpenSeadragon || viewerStarted) return;
      viewerStarted = true;
      var v = OpenSeadragon({
        element: box, tileSources: box.getAttribute('data-iiif'), showNavigationControl: false, showNavigator: false,
        visibilityRatio: 0.6, minZoomImageRatio: 0.6, maxZoomPixelRatio: 2.5, gestureSettingsMouse: { clickToZoom: false, dblClickToZoom: true },
        crossOriginPolicy: 'Anonymous', preserveImageSizeOnResize: true, animationTime: 0.4
      });
      v.addHandler('open', function () { var s = $('img.static', box); if (s) s.remove(); viewer = v; attachViewerSync(); });
      var de = ui() !== 'en';
      var ctl = document.createElement('div'); ctl.className = 'facs-controls';
      ctl.innerHTML = '<button type="button" data-z="in" aria-label="' + (de ? 'Vergrößern' : 'Zoom in') + '">+</button>' +
        '<button type="button" data-z="out" aria-label="' + (de ? 'Verkleinern' : 'Zoom out') + '">−</button>' +
        '<button type="button" data-z="home" aria-label="' + (de ? 'Ganze Seite' : 'Whole page') + '">⤢</button>' +
        '<button type="button" data-z="full" aria-label="' + (de ? 'Vollbild' : 'Full screen') + '">⛶</button>';
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
