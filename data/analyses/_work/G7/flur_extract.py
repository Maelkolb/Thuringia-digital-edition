"""Extraction of rent per Morgen ("Pacht") and soil shares from the article texts (analysis 8)."""
import re
from fractions import Fraction

NUMW = {"ein": 1, "eins": 1, "zwei": 2, "drei": 3, "vier": 4, "fünf": 5, "sechs": 6, "sieben": 7, "acht": 8, "neun": 9, "zehn": 10}
NUM = r"(?:\d+(?:\s\d{1,2}/\d{1,2})?|\d+[,.]\d+|" + "|".join(NUMW) + r")"
RANGE = rf"({NUM})(?:\s*(?:[—–-]|bis|und)\s*({NUM}))?"


def tonum(s):
    s = s.strip()
    if s in NUMW:
        return float(NUMW[s])
    m = re.fullmatch(r"(\d+)\s(\d{1,2})/(\d{1,2})", s)
    if m:
        return int(m.group(1)) + int(m.group(2)) / int(m.group(3))
    return float(s.replace(",", "."))


PAT_A = re.compile(r"(?:Pacht|verpachtet|gepachtet|Feldpachtung)(?!er)(?!erlös)[^.\d]{0,70}?" + RANGE + r"\s*Thlr")
PAT_B = re.compile(RANGE + r"\s*Thlr\.?\s*(?:Pacht|verpachtet|gepachtet)")
PAT_C = re.compile(r"(?:Morgen|Acker|Feld)[^.\d]{0,40}?(?:giebt|gibt|trägt|bringt|steht zu|zu)\s+" + RANGE + r"\s*Thlr\.?\s*Pacht")


def rent(text):
    """-> (lo, hi, snippet) of the first rent-per-Morgen statement or None."""
    t = text.replace("\n", " ")
    cands = []
    for pat in (PAT_B, PAT_A, PAT_C):
        for m in pat.finditer(t):
            ctx = t[max(0, m.start() - 90): m.end() + 40]
            if re.search(r"Morgen|Acker|Feld|Boden", ctx) and not re.search(r"Pachter|Hofpacht|Reihebierschank|Kleinhäusern|Pachterlös|Gutspachter|Achtel", ctx):
                lo = tonum(m.group(1))
                hi = tonum(m.group(2)) if m.group(2) else lo
                if hi > 40 or lo > hi:
                    continue
                pre = t[max(0, m.start() - 100): m.start()]
                starts = [x.start() for x in re.finditer(r"(?<=\. )[A-ZÄÖÜ]", pre)]
                if starts:
                    pre = pre[starts[-1]:]
                else:
                    k = pre.find(" ")
                    pre = pre[k + 1:] if k >= 0 else pre
                post = t[m.end(): m.end() + 14]
                k = post.rfind(" ")
                post = post[:k] if k > 0 else post
                snippet = (pre + t[m.start(): m.end()] + post).strip()
                cands.append((m.start(), lo, hi, snippet))
    if not cands:
        return None
    cands.sort()
    return cands[0][1], cands[0][2], cands[0][3]


QUAL = {"gut": "good", "guten": "good", "guter": "good", "gutes": "good", "gutem": "good", "ergiebig": "good", "ergiebigen": "good",
        "mittelgut": "med", "mittelguten": "med", "mittelguter": "med", "mittelgutes": "med", "mittelgutem": "med", "mittel": "med", "mittleren": "med",
        "mittlerer": "med", "mittleres": "med", "mittelmäßig": "med", "mittelmäßigen": "med",
        "gering": "poor", "geringen": "poor", "geringer": "poor", "geringem": "poor", "mager": "poor", "mageren": "poor", "schlecht": "poor"}
FR = re.compile(r"(\d+)\s*/\s*(\d+)\s+(?:Boden\s+)?([A-Za-zäöüß]+)")


def soil(txt):
    """-> dict good/med/poor shares from fractions, or None."""
    if not txt:
        return None
    out = {"good": 0.0, "med": 0.0, "poor": 0.0}
    tot = 0.0
    for m in FR.finditer(txt):
        w = m.group(3).lower()
        if w in QUAL:
            f = int(m.group(1)) / int(m.group(2))
            out[QUAL[w]] += f
            tot += f
    if 0.95 <= tot <= 1.05:
        return {k: round(v / tot, 3) for k, v in out.items()}
    return None
