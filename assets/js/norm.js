// Search normalisation - must stay identical to pipeline/site/norm.py
(function (g) {
  'use strict';
  var TOKEN = /[0-9]+|[A-Za-zÀ-ÖØ-öø-ÿſ]+/g;
  function fold(w) {
    w = w.toLowerCase().replace(/ſ/g, 's');
    w = w.replace(/ß/g, 'ss').replace(/ä/g, 'a').replace(/ö/g, 'o').replace(/ü/g, 'u');
    w = w.replace(/ae/g, 'a').replace(/oe/g, 'o').replace(/ue/g, 'u');
    w = w.replace(/é/g, 'e').replace(/è/g, 'e').replace(/à/g, 'a');
    w = w.replace(/th/g, 't').replace(/ph/g, 'f').replace(/y/g, 'i');
    w = w.replace(/c(?=[aouklrt])/g, 'k').replace(/c(?=[eiäöü])/g, 'z');
    w = w.replace(/ck/g, 'k').replace(/dt/g, 't');
    return w;
  }
  function stem(w) {
    if (w.length < 4 || /^[0-9]+$/.test(w)) return w;
    if (w.indexOf('ge') === 0 && w.length >= 6) w = w.slice(2);
    w = w.replace(/sch/g, '$').replace(/ei/g, '%').replace(/ie/g, '&');
    w = w.replace(/(.)\1/g, '$1*');
    while (w.length > 4) { // never stem below four letters
      var n;
      if (w.length > 5) {
        n = w.replace(/e[mr]$/, '');
        if (n !== w) { w = n; continue; }
        n = w.replace(/nd$/, '');
        if (n !== w) { w = n; continue; }
      }
      n = w.replace(/t$/, '');
      if (n !== w) { w = n; continue; }
      n = w.replace(/[esn]$/, '');
      if (n !== w) { w = n; continue; }
      break;
    }
    if (w.length === 4 && w.charAt(3) === 'e') w = w.slice(0, 3);
    w = w.replace(/(.)\*/g, '$1$1');
    return w.replace(/\$/g, 'sch').replace(/%/g, 'ei').replace(/&/g, 'ie');
  }
  function norm(word) { return stem(fold(word)); }
  function tokens(text) { return (text.match(TOKEN) || []); }
  g.RJNorm = { fold: fold, stem: stem, norm: norm, tokens: tokens };
  if (typeof module !== 'undefined') module.exports = g.RJNorm;
})(typeof window !== 'undefined' ? window : globalThis);
