// Register pages: live filter, kind filter, citations (KWIC) on demand
(function () {
  'use strict';
  var me = document.currentScript, file = me && me.getAttribute('data-file');
  var input = document.querySelector('[data-reg-filter]'), kindSel = document.querySelector('[data-reg-kind]');
  var count = document.querySelector('[data-reg-count]');
  var items = Array.prototype.slice.call(document.querySelectorAll('.reg-item'));
  var fold = function (s) { return window.RJNorm ? RJNorm.fold(s) : s.toLowerCase(); };
  var keys = items.map(function (li) { return fold(li.getAttribute('data-k') || li.textContent); });
  function apply() {
    var q = fold((input && input.value || '').trim()), k = kindSel ? kindSel.value : '', shown = 0;
    items.forEach(function (li, i) {
      var ok = (!q || keys[i].indexOf(q) >= 0) && (!k || li.getAttribute('data-kind') === k);
      li.hidden = !ok; if (ok) shown++;
    });
    Array.prototype.forEach.call(document.querySelectorAll('[data-letter]'), function (sec) {
      sec.hidden = !sec.querySelector('.reg-item:not([hidden])');
    });
    if (count) count.textContent = shown + ' / ' + items.length;
  }
  if (input) input.addEventListener('input', apply);
  if (kindSel) kindSel.addEventListener('change', apply);
  if (input && location.hash.length < 2) { var q = new URLSearchParams(location.search).get('q'); if (q) { input.value = q; } }
  apply();

  var kwic = null;
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-kwic]'); if (!b || !file) return;
    var id = b.getAttribute('data-kwic'), li = b.closest('.reg-item');
    var open = li.querySelector('.kwic');
    if (open) { open.remove(); return; }
    (kwic ? Promise.resolve(kwic) : RJ.load('register/belege/' + file).then(function (d) { kwic = d; return d; }))
      .then(function (d) {
        var list = d[id] || [], box = document.createElement('div'); box.className = 'kwic';
        box.innerHTML = list.map(function (m) {
          var txt = RJ.esc(m[2]).replace('⟦', '<b>').replace('⟧', '</b>');
          return '<a href="../seite/' + m[0] + '.html#' + m[1] + '"><span class="p">' + m[0] + '</span><span>…' + txt + '…</span></a>';
        }).join('') || '<span class="muted">–</span>';
        li.appendChild(box);
      });
  });
  if (location.hash) { var t = document.getElementById(decodeURIComponent(location.hash.slice(1))); if (t) { t.hidden = false; t.scrollIntoView({ block: 'center' }); } }
})();
