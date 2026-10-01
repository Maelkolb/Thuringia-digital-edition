// Full-text search over the static, sharded index (BM25), see pipeline/site/search_index.py
(function () {
  'use strict';
  var ROOT = document.body.getAttribute('data-root') || '';
  var BASE = ROOT + 'suche/';
  var K1 = 1.2, B = 0.75, PAGE = 25;
  var D = null, V = null, SYN = null, SECTIONS = null, QUICK = null, SECIDX = null;
  var shardCache = {}, textCache = {};
  var form = document.querySelector('[data-search-form]'), input = form.querySelector('input');
  var out = document.querySelector('[data-results]'), status = document.querySelector('[data-search-status]');
  var dym = document.querySelector('[data-dym]'), entHits = document.querySelector('[data-entity-hits]');
  var moreBtn = document.querySelector('[data-more]');
  var state = { all: null, list: [], shown: 0, terms: [], facets: { part: null, chapter: null, kind: null } };
  var en = function () { return document.documentElement.getAttribute('data-ui') === 'en'; };
  var KINDS = { p: ['Fließtext', 'Text'], h: ['Überschrift', 'Heading'], t: ['Tabelle', 'Table'], l: ['Liste', 'List'], f: ['Fußnote', 'Footnote'],
    m: ['Seitenübersicht', 'Page summary'], e: ['Register', 'Index entry'], g: ['Ortsartikel', 'Place article'], a: ['Auswertung', 'Analysis'], w: ['Glossar', 'Glossary'] };
  var REGFILE = { place: 'orte', nature: 'natur', person: 'personen', organisation: 'institutionen', organism: 'organismen', concept: 'sachen' };
  // question words and function words are ignored when other words remain ("wie viele Einwohner hatte Gera")
  var STOP = ('der die das den dem des ein eine einer eines einem einen und oder aber in im am an auf aus bei mit nach von vom zu zum zur ' +
    'für über unter vor wie was wer wo wann warum welche welcher welches viele viel hatte hat haben ist sind war waren wurde wurden ' +
    'es sich nicht auch als noch so man da gab gibt the a an of and or in on at to for with from by is was were are what which who how ' +
    'many much did do does when where why about').split(' ');
  var STOPSET = {}; STOP.forEach(function (w) { STOPSET[w] = true; });
  var PAGEKINDS = 'phtlfm';
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
        SECIDX = {}; SECTIONS.forEach(function (s, i) { SECIDX[s[0]] = i; });
      });
  }
  function postings(term) {
    var s = shardName(term);
    var p = shardCache[s] ? Promise.resolve(shardCache[s]) : json(BASE + 'i/' + s + '.json').catch(function () { return {}; }).then(function (d) { shardCache[s] = d; return d; });
    return p.then(function (d) { return d[term] || []; });
  }
  function df(n) { return V.index[n] !== undefined ? V.df[V.index[n]] : 0; }
  // --- query parsing --------------------------------------------------------
  function parse(q) {
    var phrases = [], excl = [], words = [];
    q = q.replace(/[„“"”]([^„“"”]+)[„“"”]/g, function (_, ph) { phrases.push(ph); return ' ' + ph + ' '; });
    q.split(/\s+/).forEach(function (w) {
      if (!w) return;
      if (w[0] === '-' && w.length > 1) { RJNorm.tokens(w.slice(1)).forEach(function (t) { excl.push(RJNorm.norm(t)); }); return; }
      RJNorm.tokens(w).forEach(function (t) { words.push(t); });
    });
    // drop function words and over-frequent tokens when other words remain (not inside phrases)
    var content = words.filter(function (w) {
      if (STOPSET[w.toLowerCase()]) return false;
      return df(RJNorm.norm(w)) < D.docs.length * 0.2 || /^[0-9]+$/.test(w);
    });
    if (content.length && !phrases.length) words = content;
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
  // expansions for one query word: exact, synonyms (EN->DE, modern->1870), prefix (last word), fuzzy fallback
  function expand(word, isLast) {
    var n = RJNorm.norm(word), out = [];
    if (V.index[n] !== undefined) out.push({ t: n, w: 1 });
    (SYN[n] || []).forEach(function (s) { if (V.index[s] !== undefined && s !== n) out.push({ t: s, w: 0.75, syn: true }); });
    if (/^[0-9]+$/.test(n)) return out;
    var f = RJNorm.fold(word);
    // prefix completion only helps unfinished words: skip it when the word itself is frequent
    if (isLast && f.length >= 3 && df(n) < 5) {
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
      cands.slice(0, 3).forEach(function (c, i) { out.push({ t: c.t, w: (i === 0 ? 0.7 : 0.35) / (1 + c.d), fuzzy: true }); });
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
      var fixed = [], fuzzyUsed = false;
      groups.forEach(function (g, i) {
        if (g.length && g.every(function (x) { return x.fuzzy; })) { fuzzyUsed = true; fixed.push(V.d[V.index[g[0].t]]); } else fixed.push(P.words[i]);
      });
      var all = []; groups.forEach(function (g) { g.forEach(function (x) { all.push(x.t); }); });
      P.excl.forEach(function (t) { all.push(t); });
      return Promise.all(all.map(postings)).then(function (lists) {
        var post = {}; all.forEach(function (t, i) { post[t] = lists[i]; });
        var N = D.docs.length, scores = {}, matched = {};
        var qfold = RJNorm.fold(P.words.join(' '));
        var qwords = {}; P.words.forEach(function (w) { qwords[RJNorm.fold(w)] = true; });
        groups.forEach(function (g, gi) {
          g.forEach(function (x) {
            var p = post[x.t] || [], dfx = p.length / 2, idf = Math.log(1 + (N - dfx + 0.5) / (dfx + 0.5));
            for (var i = 0; i < p.length; i += 2) {
              var di = p[i], tf = p[i + 1], doc = D.docs[di];
              // short index stubs get no length bonus over real passages
              var dl = 'egaw'.indexOf(doc[0]) >= 0 ? Math.max(doc[4], D.avgLen * 0.75) : doc[4];
              var s = idf * (tf * (K1 + 1)) / (tf + K1 * (1 - B + B * dl / D.avgLen)) * x.w * (D.weights[doc[0]] || 1);
              scores[di] = (scores[di] || 0) + s;
              (matched[di] = matched[di] || {})[gi] = true;
            }
          });
        });
        var numericQuery = P.words.every(function (w) { return /^[0-9]+$/.test(w); });
        Object.keys(scores).forEach(function (k) {
          var doc = D.docs[k];
          if (numericQuery && PAGEKINDS.indexOf(doc[0]) < 0) scores[k] *= 0.3;  // years: prefer the pages about the events
          if (doc[5]) {
            var tf = RJNorm.fold(doc[5]);
            if (tf === qfold) scores[k] *= 4;              // exact title / label
            else if (qwords[tf]) scores[k] *= 2.5;         // one query word is the title ("Schule Hirschberg")
          }
          if (doc[3] >= 0 && SECTIONS[doc[3]][0] === 'inhalt') scores[k] *= 0.3; // table-of-contents pages
        });
        var excluded = {};
        P.excl.forEach(function (t) { var p = post[t] || []; for (var i = 0; i < p.length; i += 2) excluded[p[i]] = true; });
        var need = groups.filter(function (g) { return g.length; }).length;
        var ids = Object.keys(scores).map(Number).filter(function (d) { return !excluded[d]; });
        var andIds = ids.filter(function (d) { return Object.keys(matched[d]).length >= need; });
        var mode = 'and';
        if (!andIds.length && need > 1) {
          // fall back to documents matching most of the words
          mode = 'or';
          ids = ids.filter(function (d) { return Object.keys(matched[d]).length >= Math.ceil(need / 2); });
        } else ids = andIds;
        state.terms = [];
        groups.forEach(function (g) { g.forEach(function (x) { state.terms.push(x.t); }); });
        state.phrases = P.phrases.map(function (ph) { return RJNorm.tokens(ph).map(RJNorm.norm).join(' '); });
        state.all = ids.map(function (d) { return { d: d, s: scores[d] }; }).sort(function (a, b) { return b.s - a.s; });
        state.mode = mode; state.query = q;
        if (fuzzyUsed) {
          var sug = fixed.join(' ');
          dym.innerHTML = (en() ? 'No exact match – showing results for ' : 'Kein genauer Treffer – Ergebnisse für ') +
            '<a href="?q=' + encodeURIComponent(sug) + '"><b>' + RJ.esc(sug) + '</b></a>';
        }
        entityHits(P.words.join(' '));
        return applyPhrases().then(function () { facets(); render(true); });
      });
    }).catch(function (e) { status.textContent = (en() ? 'Search index could not be loaded. ' : 'Der Suchindex konnte nicht geladen werden. ') + (location.protocol === 'file:' ? (en() ? 'Please open the edition via a web server (e.g. python -m http.server).' : 'Bitte die Edition über einen Webserver öffnen (z. B. python -m http.server).') : ''); console.error(e); });
  }
  // phrase queries: verify the phrase in the text before counting/rendering (top 200 candidates)
  function applyPhrases() {
    if (!state.phrases.length) return Promise.resolve();
    var cand = state.all.slice(0, 200), pages = {};
    cand.forEach(function (r) { var doc = D.docs[r.d]; if (PAGEKINDS.indexOf(doc[0]) >= 0) pages[doc[1]] = true; });
    return Promise.all(Object.keys(pages).map(pageTexts)).then(function () {
      state.all = cand.filter(function (r) {
        var doc = D.docs[r.d];
        if (PAGEKINDS.indexOf(doc[0]) < 0) return phraseOk(doc[5] || '');
        var tx = textCache[doc[1]] || {};
        return phraseOk(doc[0] === 'm' ? (tx._summary_de || '') + ' ' + (tx._summary_en || '') : tx[doc[2]] || '');
      });
    });
  }
  function entityHits(q) {
    var f = RJNorm.fold(q);
    var hits = QUICK.filter(function (x) {
      if (['place', 'nature', 'person', 'organisation', 'organism', 'concept'].indexOf(x[1]) < 0) return false;
      var l = RJNorm.fold(x[0]);
      return l === f || l.indexOf(f + ' ') === 0 || l.indexOf(f + ',') === 0 || RJNorm.norm(x[0]) === RJNorm.norm(q);
    }).sort(function (a, b) { return (RJNorm.fold(b[0]) === f) - (RJNorm.fold(a[0]) === f) || b[3] - a[3]; }).slice(0, 8);
    entHits.innerHTML = hits.map(function (x) {
      return '<a class="chip k-' + x[1] + '" style="--ec:var(--e-' + x[1] + ')" href="' + ROOT + x[2] + '"><span class="swatch"></span>' + RJ.esc(x[0]) + ' <span class="n">' + RJ.kindLabel(x[1]) + (x[3] ? ' · ' + x[3] + '×' : '') + '</span></a>';
    }).join('');
  }
  function chain(doc) {
    if (doc[3] < 0) return [];
    var s = SECTIONS[doc[3]], c = [s], guard = 0;
    while (s && s[4] && guard++ < 6) { s = SECTIONS[SECIDX[s[4]]]; if (s) c.unshift(s); }
    return c;
  }
  function partOf(doc) { var c = chain(doc); return c.length ? c[0][0] : null; }
  function chapterOf(doc) { var c = chain(doc); return c.length > 1 ? c[1][0] : (c.length ? c[0][0] : null); }
  function secLabel(id) { var s = SECTIONS[SECIDX[id]]; return s ? (s[1] ? s[1] + ' ' : '') + (en() && s[3] ? s[3] : s[2]) : id; }
  function filtered() {
    return state.all.filter(function (r) {
      var doc = D.docs[r.d];
      if (state.facets.kind && doc[0] !== state.facets.kind) return false;
      if (state.facets.part && partOf(doc) !== state.facets.part) return false;
      if (state.facets.chapter && chapterOf(doc) !== state.facets.chapter) return false;
      return true;
    });
  }
  // one result per page (best passage first, further passages counted), index entries as they are
  function grouped(list) {
    var seen = {}, outl = [];
    list.forEach(function (r) {
      var doc = D.docs[r.d];
      if (PAGEKINDS.indexOf(doc[0]) >= 0) {
        if (seen[doc[1]] !== undefined) { outl[seen[doc[1]]].more.push(r); return; }
        seen[doc[1]] = outl.length;
      }
      outl.push({ r: r, more: [] });
    });
    return outl;
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
      if (!keys.length) return;
      var all = document.createElement('label');
      all.innerHTML = '<input type="radio" name="f-' + f + '" value=""' + (!state.facets[f] ? ' checked' : '') + '> ' + (en() ? 'all' : 'alle');
      box.appendChild(all);
      keys.forEach(function (k) {
        var l = document.createElement('label');
        l.innerHTML = '<input type="radio" name="f-' + f + '" value="' + k + '"' + (state.facets[f] === k ? ' checked' : '') + '> ' + RJ.esc(f === 'kind' ? kl(k) : secLabel(k)) + '<span class="c">' + counts[f][k] + '</span>';
        box.appendChild(l);
      });
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
    var o = '', pos = start;
    hits.forEach(function (h) { if (h[0] >= start && h[1] <= end) { o += RJ.esc(text.slice(pos, h[0])) + '<mark class="hit">' + RJ.esc(text.slice(h[0], h[1])) + '</mark>'; pos = h[1]; } });
    o += RJ.esc(text.slice(pos, end));
    return (start > 0 ? '… ' : '') + o.replace(/\s*\|\s*/g, ' · ').replace(/\n/g, ' ') + (end < text.length ? ' …' : '');
  }
  function phraseOk(text) {
    if (!state.phrases.length) return true;
    var norm = RJNorm.tokens(text).map(RJNorm.norm).join(' ');
    return state.phrases.every(function (ph) { return norm.indexOf(ph) >= 0; });
  }
  function render(reset) {
    if (reset) { out.innerHTML = ''; state.shown = 0; state.list = grouped(filtered()); }
    var n = state.list.length, pages = state.list.filter(function (g) { return PAGEKINDS.indexOf(D.docs[g.r.d][0]) >= 0; }).length;
    status.innerHTML = n ? (n + (en() ? ' results' : ' Treffer') + (pages ? (en() ? ' (' + pages + ' pages)' : ' (' + pages + ' Seiten)') : '') +
      (state.mode === 'or' ? (en() ? ' – not all words found together' : ' – nicht alle Wörter gemeinsam gefunden') : '')) : (en() ? 'No hits.' : 'Keine Treffer.');
    var slice = state.list.slice(state.shown, state.shown + PAGE);
    state.shown += slice.length;
    var hl = encodeURIComponent(state.query.replace(/[„“"”-]/g, ' '));
    slice.forEach(function (g) {
      var r = g.r, doc = D.docs[r.d], div = document.createElement('div');
      div.className = 'result';
      var kind = doc[0], href, title, where = '';
      if (PAGEKINDS.indexOf(kind) >= 0) {
        href = ROOT + 'seite/' + doc[1] + '.html?hl=' + hl + (doc[2] ? '#' + doc[2] : '');
        title = (en() ? 'Page ' : 'Seite ') + doc[1];
        where = doc[3] >= 0 ? secLabel(SECTIONS[doc[3]][0]) : '';
      } else if (kind === 'e') {
        var cls = doc[1].split(':')[0];
        href = ROOT + 'register/' + (REGFILE[cls] || 'index') + '.html#' + doc[1].split(':').slice(1).join(':');
        title = doc[5]; where = RJ.kindLabel(cls);
      } else if (kind === 'g') {
        href = ROOT + 'seite/' + doc[2] + '.html?hl=' + hl; title = doc[5]; where = (en() ? 'p. ' : 'S. ') + doc[2];
      } else if (kind === 'a') {
        href = ROOT + 'auswertungen/' + doc[1] + '.html'; title = doc[5]; where = '';
      } else if (kind === 'w') {
        href = ROOT + 'register/glossar.html#' + doc[1]; title = doc[5]; where = '';
      }
      var more = g.more.length ? '<span class="where">+' + g.more.length + (en() ? ' more on this page' : ' weitere auf dieser Seite') + '</span>' : '';
      div.innerHTML = '<div class="rt"><a href="' + href + '">' + RJ.esc(title) + '</a><span class="pill">' + kl(kind) + '</span><span class="where">' + RJ.esc(where) + '</span>' + more + '</div><div class="snip"></div>';
      out.appendChild(div);
      if (PAGEKINDS.indexOf(kind) >= 0) {
        pageTexts(doc[1]).then(function (tx) {
          var text = kind === 'm' ? (en() ? tx._summary_en : tx._summary_de) || '' : tx[doc[2]] || '';
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
