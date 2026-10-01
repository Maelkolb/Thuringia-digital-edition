// Full-text search over the static, sharded index (BM25), see pipeline/site/search_index.py
(function () {
  'use strict';
  var ROOT = document.body.getAttribute('data-root') || '';
  var BASE = ROOT + 'suche/';
  var K1 = 1.2, B = 0.75, PAGE = 25;
  var D = null, V = null, SYN = null, SECTIONS = null, QUICK = null;
  var shardCache = {}, textCache = {};
  var form = document.querySelector('[data-search-form]'), input = form.querySelector('input');
  var out = document.querySelector('[data-results]'), status = document.querySelector('[data-search-status]');
  var dym = document.querySelector('[data-dym]'), entHits = document.querySelector('[data-entity-hits]');
  var moreBtn = document.querySelector('[data-more]');
  var state = { results: [], shown: 0, terms: [], facets: { part: null, chapter: null, kind: null } };
  var en = function () { return document.documentElement.getAttribute('data-ui') === 'en'; };
  var KINDS = { p: ['Fließtext', 'Text'], h: ['Überschrift', 'Heading'], t: ['Tabelle', 'Table'], l: ['Liste', 'List'], f: ['Fußnote', 'Footnote'],
    m: ['Seitenübersicht', 'Page summary'], e: ['Register', 'Index entry'], g: ['Ortsartikel', 'Place article'], a: ['Auswertung', 'Analysis'], w: ['Glossar', 'Glossary'] };
  function kl(k) { var l = KINDS[k] || [k, k]; return en() ? l[1] : l[0]; }
  function json(u) { return fetch(u).then(function (r) { if (!r.ok) throw new Error(u); return r.json(); }); }
  function shardName(term) {
    var t = RJNorm.fold(term), k = t.length >= 2 ? t.slice(0, 2) : t + '_';
    return k.replace(/[^a-z0-9]/g, '_');
  }
  function loadBase() {
    if (D) return Promise.resolve();
    status.textContent = en() ? 'Loading index …' : 'Suchindex wird geladen …';
    return Promise.all([json(BASE + 'docs.json'), json(BASE + 'vocab.json'), json(BASE + 'syn.json'), json(BASE + 'sections.json'), json(BASE + 'quick.json')])
      .then(function (r) {
        D = r[0]; V = r[1]; SYN = r[2]; SECTIONS = r[3]; QUICK = r[4];
        V.index = {}; V.t.forEach(function (t, i) { V.index[t] = i; });
      });
  }
  function postings(term) {
    var s = shardName(term);
    var p = shardCache[s] ? Promise.resolve(shardCache[s]) : json(BASE + 'i/' + s + '.json').catch(function () { return {}; }).then(function (d) { shardCache[s] = d; return d; });
    return p.then(function (d) { return d[term] || []; });
  }
  // --- query parsing --------------------------------------------------------
  function parse(q) {
    var phrases = [], excl = [], words = [];
    q = q.replace(/[„“"”]([^„“"”]+)[„“"”]/g, function (_, ph) { phrases.push(ph); return ' ' + ph + ' '; });
    q.split(/\s+/).forEach(function (w) {
      if (!w) return;
      if (w[0] === '-' && w.length > 1) { RJNorm.tokens(w.slice(1)).forEach(function (t) { excl.push(RJNorm.norm(t)); }); return; }
      RJNorm.tokens(w).forEach(function (t) { words.push(t); });
    });
    return { words: words, phrases: phrases, excl: excl };
  }
  function lev(a, b, max) {
    if (Math.abs(a.length - b.length) > max) return max + 1;
    var prev = [], cur, i, j;
    for (j = 0; j <= b.length; j++) prev[j] = j;
    for (i = 1; i <= a.length; i++) {
      cur = [i]; var best = i;
      for (j = 1; j <= b.length; j++) {
        cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
        if (cur[j] < best) best = cur[j];
      }
      if (best > max) return max + 1;
      prev = cur;
    }
    return prev[b.length];
  }
  // expansions for one query word: exact, synonyms (EN->DE), prefix (last word), fuzzy fallback
  function expand(word, isLast) {
    var n = RJNorm.norm(word), out = [];
    if (V.index[n] !== undefined) out.push({ t: n, w: 1 });
    (SYN[n] || []).forEach(function (s) { if (V.index[s] !== undefined) out.push({ t: s, w: 0.8, syn: true }); });
    if (/^[0-9]+$/.test(n)) return out;
    var f = RJNorm.fold(word);
    // prefix completion only helps unfinished words: skip it when the word itself is frequent
    var exactDf = V.index[n] !== undefined ? V.df[V.index[n]] : 0;
    if (isLast && f.length >= 3 && exactDf < 5) {
      var c = 0;
      for (var i = 0; i < V.t.length && c < 12; i++) {
        var t = V.t[i];
        if (t !== n && t.indexOf(f.length > 5 ? n : f) === 0) { out.push({ t: t, w: 0.35 }); c++; }
      }
    }
    if (!out.length && n.length >= 4) {
      var max = n.length >= 8 ? 2 : 1, cands = [];
      for (var k = 0; k < V.t.length; k++) {
        var tt = V.t[k];
        if (Math.abs(tt.length - n.length) > max || tt[0] !== n[0]) continue;
        var d = lev(n, tt, max);
        if (d <= max) cands.push({ t: tt, d: d, df: V.df[k] });
      }
      cands.sort(function (a, b) { return a.d - b.d || b.df - a.df; });
      cands.slice(0, 5).forEach(function (c) { out.push({ t: c.t, w: 0.5, fuzzy: true }); });
    }
    return out;
  }
  // --- search ---------------------------------------------------------------
  function run(q) {
    q = q.trim();
    out.innerHTML = ''; dym.innerHTML = ''; entHits.innerHTML = ''; moreBtn.hidden = true;
    if (!q) { status.textContent = ''; return; }
    loadBase().then(function () {
      var P = parse(q);
      if (!P.words.length) { status.textContent = ''; return; }
      var groups = P.words.map(function (w, i) { return expand(w, i === P.words.length - 1); });
      var fuzzyUsed = [];
      groups.forEach(function (g, i) { if (g.length && g.every(function (x) { return x.fuzzy; })) fuzzyUsed.push(V.d[V.index[g[0].t]]); });
      var all = []; groups.forEach(function (g) { g.forEach(function (x) { all.push(x.t); }); });
      P.excl.forEach(function (t) { all.push(t); });
      return Promise.all(all.map(postings)).then(function (lists) {
        var post = {}; all.forEach(function (t, i) { post[t] = lists[i]; });
        var N = D.docs.length, scores = {}, matched = {};
        groups.forEach(function (g, gi) {
          g.forEach(function (x) {
            var p = post[x.t] || [], df = p.length / 2, idf = Math.log(1 + (N - df + 0.5) / (df + 0.5));
            for (var i = 0; i < p.length; i += 2) {
              var di = p[i], tf = p[i + 1], doc = D.docs[di];
              var s = idf * (tf * (K1 + 1)) / (tf + K1 * (1 - B + B * doc[4] / D.avgLen)) * x.w * (D.weights[doc[0]] || 1);
              scores[di] = (scores[di] || 0) + s;
              (matched[di] = matched[di] || {})[gi] = true;
            }
          });
        });
        var excluded = {};
        P.excl.forEach(function (t) { var p = post[t] || []; for (var i = 0; i < p.length; i += 2) excluded[p[i]] = true; });
        var need = groups.filter(function (g) { return g.length; }).length;
        var ids = Object.keys(scores).map(Number).filter(function (d) { return !excluded[d]; });
        var andIds = ids.filter(function (d) { return Object.keys(matched[d]).length >= need; });
        var mode = 'and';
        if (!andIds.length && need > 1) { mode = 'or'; } else ids = andIds;
        state.terms = [];
        groups.forEach(function (g) { g.forEach(function (x) { state.terms.push(x.t); }); });
        // phrase filter (on snippet text, done later lazily) -> mark
        state.phrases = P.phrases.map(function (ph) { return RJNorm.tokens(ph).map(RJNorm.norm).join(' '); });
        var res = ids.map(function (d) { return { d: d, s: scores[d] }; }).sort(function (a, b) { return b.s - a.s; });
        state.all = res; state.mode = mode; state.query = q;
        if (fuzzyUsed.length) dym.innerHTML = (en() ? 'No exact match – showing similar words: ' : 'Kein genauer Treffer – ähnliche Wörter: ') + '<b>' + fuzzyUsed.map(RJ.esc).join(', ') + '</b>';
        entityHits(q);
        facets();
        render(true);
      });
    }).catch(function (e) { status.textContent = (en() ? 'Search index could not be loaded. ' : 'Der Suchindex konnte nicht geladen werden. ') + (location.protocol === 'file:' ? (en() ? 'Please open the edition via a web server (e.g. python -m http.server).' : 'Bitte die Edition über einen Webserver öffnen (z. B. python -m http.server).') : ''); console.error(e); });
  }
  function entityHits(q) {
    var f = RJNorm.fold(q), hits = QUICK.filter(function (x) { return ['place', 'nature', 'person', 'organisation', 'organism', 'concept'].indexOf(x[1]) >= 0 && RJNorm.fold(x[0]).indexOf(f) === 0; })
      .sort(function (a, b) { return b[3] - a[3]; }).slice(0, 8);
    entHits.innerHTML = hits.map(function (x) {
      return '<a class="chip k-' + x[1] + '" style="--ec:var(--e-' + x[1] + ')" href="' + ROOT + x[2] + '"><span class="swatch"></span>' + RJ.esc(x[0]) + ' <span class="n">' + RJ.kindLabel(x[1]) + (x[3] ? ' · ' + x[3] + '×' : '') + '</span></a>';
    }).join('');
  }
  function partOf(doc) {
    if (doc[3] < 0) return null;
    var s = SECTIONS[doc[3]], guard = 0;
    while (s && s[4] && guard++ < 6) { var p = SECTIONS.find(function (x) { return x[0] === s[4]; }); if (!p) break; s = p; }
    return s ? s[0] : null;
  }
  function chapterOf(doc) {
    if (doc[3] < 0) return null;
    var s = SECTIONS[doc[3]], chain = [s], guard = 0;
    while (s && s[4] && guard++ < 6) { s = SECTIONS.find(function (x) { return x[0] === s[4]; }); if (s) chain.unshift(s); }
    return chain.length > 1 ? chain[1][0] : chain[0][0];
  }
  function secLabel(id) { var s = SECTIONS.find(function (x) { return x[0] === id; }); return s ? (s[1] ? s[1] + ' ' : '') + (en() && s[3] ? s[3] : s[2]) : id; }
  function filtered() {
    return state.all.filter(function (r) {
      var doc = D.docs[r.d];
      if (state.facets.kind && doc[0] !== state.facets.kind) return false;
      if (state.facets.part && partOf(doc) !== state.facets.part) return false;
      if (state.facets.chapter && chapterOf(doc) !== state.facets.chapter) return false;
      return true;
    });
  }
  function facets() {
    var counts = { part: {}, chapter: {}, kind: {} };
    state.all.forEach(function (r) {
      var doc = D.docs[r.d], p = partOf(doc), c = chapterOf(doc);
      counts.kind[doc[0]] = (counts.kind[doc[0]] || 0) + 1;
      if (p) counts.part[p] = (counts.part[p] || 0) + 1;
      if (c && c !== p) counts.chapter[c] = (counts.chapter[c] || 0) + 1;
    });
    ['part', 'chapter', 'kind'].forEach(function (f) {
      var box = document.querySelector('[data-facet="' + f + '"]');
      var keys = Object.keys(counts[f]).sort(function (a, b) { return counts[f][b] - counts[f][a]; }).slice(0, 14);
      box.querySelectorAll('label').forEach(function (l) { l.remove(); });
      keys.forEach(function (k) {
        var l = document.createElement('label');
        l.innerHTML = '<input type="radio" name="f-' + f + '" value="' + k + '"' + (state.facets[f] === k ? ' checked' : '') + '> ' + RJ.esc(f === 'kind' ? kl(k) : secLabel(k)) + '<span class="c">' + counts[f][k] + '</span>';
        box.appendChild(l);
      });
      if (keys.length) {
        var all = document.createElement('label');
        all.innerHTML = '<input type="radio" name="f-' + f + '" value=""' + (!state.facets[f] ? ' checked' : '') + '> ' + (en() ? 'all' : 'alle');
        box.insertBefore(all, box.children[1]);
      }
    });
  }
  document.addEventListener('change', function (e) {
    var m = e.target.name && e.target.name.match(/^f-(\w+)$/); if (!m) return;
    state.facets[m[1]] = e.target.value || null; render(true);
  });
  function pageTexts(slug) {
    if (textCache[slug]) return Promise.resolve(textCache[slug]);
    return json(BASE + 't/' + encodeURIComponent(slug) + '.json').catch(function () { return {}; }).then(function (d) { textCache[slug] = d; return d; });
  }
  function snippet(text, terms) {
    var want = {}; terms.forEach(function (t) { want[t] = true; });
    var re = /[0-9]+|[A-Za-zÀ-ÖØ-öø-ÿſ]+/g, m, hits = [];
    while ((m = re.exec(text))) if (want[RJNorm.norm(m[0])]) hits.push([m.index, m.index + m[0].length]);
    var start = hits.length ? Math.max(0, hits[0][0] - 110) : 0, end = Math.min(text.length, start + 300);
    var out = '', pos = start;
    hits.forEach(function (h) { if (h[0] >= start && h[1] <= end) { out += RJ.esc(text.slice(pos, h[0])) + '<mark class="hit">' + RJ.esc(text.slice(h[0], h[1])) + '</mark>'; pos = h[1]; } });
    out += RJ.esc(text.slice(pos, end));
    return (start > 0 ? '… ' : '') + out.replace(/\n/g, ' ') + (end < text.length ? ' …' : '');
  }
  function phraseOk(text) {
    if (!state.phrases.length) return true;
    var norm = RJNorm.tokens(text).map(RJNorm.norm).join(' ');
    return state.phrases.every(function (ph) { return norm.indexOf(ph) >= 0; });
  }
  function render(reset) {
    var list = filtered();
    if (reset) { out.innerHTML = ''; state.shown = 0; state.list = list; }
    var n = state.list.length;
    status.innerHTML = n ? (n + (en() ? ' hits' : ' Treffer') + (state.mode === 'or' ? (en() ? ' (not all words found together – showing partial matches)' : ' (nicht alle Wörter gemeinsam gefunden – Teiltreffer)') : '')) : (en() ? 'No hits.' : 'Keine Treffer.');
    var slice = state.list.slice(state.shown, state.shown + PAGE);
    state.shown += slice.length;
    var hl = encodeURIComponent(state.query.replace(/[„“"”-]/g, ' '));
    slice.forEach(function (r) {
      var doc = D.docs[r.d], div = document.createElement('div');
      div.className = 'result';
      var kind = doc[0], href, title, where = '';
      if ('phtlfm'.indexOf(kind) >= 0) {
        href = ROOT + 'seite/' + doc[1] + '.html?hl=' + hl + (doc[2] ? '#' + doc[2] : '');
        title = (en() ? 'Page ' : 'Seite ') + doc[1];
        where = doc[3] >= 0 ? secLabel(SECTIONS[doc[3]][0]) : '';
      } else if (kind === 'e') {
        var q = QUICK.find(function (x) { return x[0] === doc[5]; });
        href = ROOT + (q ? q[2] : 'register/index.html'); title = doc[5]; where = q ? RJ.kindLabel(q[1]) : '';
      } else if (kind === 'g') {
        href = ROOT + 'seite/' + doc[2] + '.html?hl=' + hl; title = doc[5]; where = kl('g') + ', ' + (en() ? 'p. ' : 'S. ') + doc[2];
      } else if (kind === 'a') {
        href = ROOT + 'auswertungen/' + doc[1] + '.html'; title = doc[5]; where = kl('a');
      } else if (kind === 'w') {
        href = ROOT + 'register/glossar.html#' + doc[1]; title = doc[5]; where = kl('w');
      }
      div.innerHTML = '<div class="rt"><a href="' + href + '">' + RJ.esc(title) + '</a><span class="pill">' + kl(kind) + '</span><span class="where">' + RJ.esc(where) + '</span></div><div class="snip"></div>';
      out.appendChild(div);
      if ('phtlfm'.indexOf(kind) >= 0) {
        pageTexts(doc[1]).then(function (tx) {
          var text = kind === 'm' ? (en() ? tx._summary_en : tx._summary_de) || '' : tx[doc[2]] || '';
          if (!phraseOk(text)) { div.remove(); return; }
          div.querySelector('.snip').innerHTML = snippet(text, state.terms);
        });
      }
    });
    moreBtn.hidden = state.shown >= n;
  }
  moreBtn.addEventListener('click', function () { render(false); });
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var q = input.value;
    history.replaceState(null, '', '?q=' + encodeURIComponent(q));
    state.facets = { part: null, chapter: null, kind: null };
    run(q);
  });
  var q0 = new URLSearchParams(location.search).get('q');
  if (q0) { input.value = q0; run(q0); } else input.focus();
  document.addEventListener('rj:lang', function () { if (state.all) { facets(); render(true); } });
})();
