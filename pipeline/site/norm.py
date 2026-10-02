"""Search normalisation shared by the index (Python) and the client (assets/js/norm.js).

1. fold: lower case, 1870 -> modern spelling equivalence classes
   (th -> t, c+a/o/u -> k, c+e/i -> z, ph -> f, y -> i, umlauts and their
   transcriptions ae/oe/ue -> a/o/u, ß -> ss)
2. stem: CISTEM (Weissweiler & Fraser 2017), case-insensitive variant.

Both sides apply the same function, so the classes only have to be
consistent, not linguistically perfect. Keep in sync with norm.js
(tests/test_norm_parity.py checks a word list).
"""
from __future__ import annotations

import re

TOKEN = re.compile(r"[0-9]+|[A-Za-zÀ-ÖØ-öø-ÿſ]+")


def fold(w: str) -> str:
    w = w.lower().replace("ſ", "s")
    w = w.replace("ß", "ss")
    w = w.replace("ä", "a").replace("ö", "o").replace("ü", "u")
    w = w.replace("ae", "a").replace("oe", "o").replace("ue", "u")
    w = w.replace("é", "e").replace("è", "e").replace("à", "a")
    w = w.replace("th", "t").replace("ph", "f").replace("y", "i")
    w = re.sub(r"c(?=[aouklrt])", "k", w)
    w = re.sub(r"c(?=[eiäöü])", "z", w)
    w = w.replace("ck", "k").replace("dt", "t")
    return w


def stem(w: str) -> str:
    if len(w) < 4 or w.isdigit():
        return w
    if w.startswith("ge") and len(w) >= 6:
        w = w[2:]
    w = w.replace("sch", "$").replace("ei", "%").replace("ie", "&")
    w = re.sub(r"(.)\1", r"\1*", w)
    while len(w) > 4:  # never stem below four letters (Frost/Fronen, Kloster/clothes stay apart)
        if len(w) > 5:
            n = re.sub(r"e[mr]$", "", w)
            if n != w:
                w = n
                continue
            n = re.sub(r"nd$", "", w)
            if n != w:
                w = n
                continue
        n = re.sub(r"t$", "", w)
        if n != w:
            w = n
            continue
        n = re.sub(r"[esn]$", "", w)
        if n != w:
            w = n
            continue
        break
    if len(w) == 4 and w.endswith("e"):  # Thale -> Thal, Teile -> Teil
        w = w[:-1]
    w = re.sub(r"(.)\*", r"\1\1", w)
    return w.replace("$", "sch").replace("%", "ei").replace("&", "ie")


def norm(word: str) -> str:
    return stem(fold(word))


def tokens(text: str) -> list[str]:
    return TOKEN.findall(text)


if __name__ == "__main__":
    for w in ["Thal", "Tal", "Thälern", "Theil", "Teile", "Cöstritz", "Köstritz", "Centner", "Zentner", "Mühlen",
              "Muehle", "Fürstenthums", "Gera's", "Schleizer", "geboren", "Geburten", "Kirchen", "Kirche", "Procent"]:
        print(w, "->", norm(w))
