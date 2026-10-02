"""Extract the lists of mountain names (pp. 10-11, 17-20) with their region labels."""
import re
from common import *

# (page, block, landesteil, grossraum, [(gebiet, start_anchor), ...])  -- every segment runs to the next anchor / end of block
SEGS = [
    ("10", "b5", "Unterland", "Elster rechts", [
        ("Elster rechts, Uferberge Lichtenau–Langenberg", "1) von der Lichtenau bis Langenberg:"),
        ("Elster rechts, Uferberge Langenberg–Gera", "2) von Langenberg bis Gera:"),
        ("Elster rechts, Uferberge Gera–Zoitsberg", "3) von Gera bis zum Zoitsberg:")]),
    ("10", "b6", "Unterland", "Elster rechts", [("Elster rechts, Wipse–faltischer Grund", "faltischen Grunde:")]),
    ("11", "b1", "Unterland", "Elster rechts", [("Elster rechts, Wipse–faltischer Grund", "")]),
    ("11", "b2", "Unterland", "Elster rechts", [("Elster rechts, Bramthal", "im Bramthalgebiete:")]),
    ("11", "b3", "Unterland", "Elster rechts", [("Elster rechts, kleine Schnauder", "Schnauder:")]),
    ("11", "b4", "Unterland", "Elster rechts", [("Elster rechts, Agagebiet", "im Agagebiete:")]),
    ("11", "b6", "Unterland", "Elster links", [("Elster links, Nordgrenze–Goldthal", "Eleonorenthal:")]),
    ("11", "b7", "Unterland", "Elster links", [("Elster links, Goldthal–Schafgrund", "Schafgrund:")]),
    ("11", "b8", "Unterland", "Elster links", [("Elster links, Schafgrund–Erlbach", "Erlbach:")]),
    ("11", "b9", "Unterland", "Elster links", [("Elster links, Erlbach–Frankenthal", "Langengrobsdorf:")]),
    ("11", "b10", "Unterland", "Elster links", [("Elster links, Elster–Erl-/Saarbach", "Saarbach:")]),
    ("17", "b1", "Oberland", "Frankenwald", [
        ("Frankenwald, Ostseite", "auf der Ostseite"),
        ("Frankenwald, Südseite", "auf der Südseite"),
        ("Frankenwald, Nordseite", "auf der Nordseite"),
        ("Frankenwald, Westseite", "auf der Westseite")]),
    ("17+18", "b2+b1", "Oberland", "Eliasbrunner Hochbuckel", [
        ("Eliasbrunner Hochbuckel, Ottergebiet", "im Ottergebiet"),
        ("Eliasbrunner Hochbuckel, Ilmquellen", "an den Ilmquellen"),
        ("Eliasbrunner Hochbuckel, Törpig", "an der Törpig"),
        ("Eliasbrunner Hochbuckel, Lemnitz", "an der Lemnitz"),
        ("Eliasbrunner Hochbuckel, Friesa–Saale", "zwischen der Friesa und der Saale")]),
    ("18", "b3", "Oberland", "Hirschberger Saalwand", [
        ("Hirschberger Saalwand, Hochrücken", "als Berghäupter des Hochrückens"),
        ("Hirschberger Saalwand, Tannenbach", "auf dem Gelände am Tannenbach"),
        ("Hirschberger Saalwand, Aubach", "am Aubach"),
        ("Hirschberger Saalwand, Göritz-/Frössner Tal", "zwischen dem Göritz- und frössner Thale"),
        ("Hirschberger Saalwand, westlich von Frössen", "westlich von Frössen")]),
    ("19", "b1", "Oberland", "Wiesenthal-Wetteraplateau", [
        ("Wiesenthal-Wetteraplateau, südlich Pösnigsbach", "auf der Südseite des Pösnigsbachs"),
        ("Wiesenthal-Wetteraplateau, Pösnigsbach–Wettera", "zwischen dem Pösnigsbach und der Wettera"),
        ("Wiesenthal-Wetteraplateau, Wettera–Wiesenthal", "zwischen der Wettera und Wiesenthal")]),
    ("19", "b2", "Oberland", "Modelitzmulde", [
        ("Modelitzmulde, Norden", "im Norden"),
        ("Modelitzmulde, Osten", "im Osten"),
        ("Modelitzmulde, Süden", "am Südrande"),
        ("Modelitzmulde, Westen", "am Westrande")]),
    ("20", "b1", "Oberland", "Ziegenrücker/Hohenleubener Plateau", [
        ("Ziegenrücker Plateau", "auf dem ziegenrücker Plateau"),
        ("Hohenleubener Plateau, Hohenleuben", "auf dem hohenleubener Plateau um Hohenleuben"),
        ("Hohenleubener Plateau, Triebes", "bei Triebes"),
        ("Hohenleubener Plateau, Niederböhmsdorf", "bei Niederböhmsdorf"),
        ("Hohenleubener Plateau, Pöllwitzwald", "im Pöllwitzwalde"),
        ("Langenwetzendorf", "Jenseits der Leuba")]),
]

SPECIAL = [
    (" oder auf Seiten der Triebes das hintere Tännig bei Schilbach", " hintere Tännig"),
    ("in der Richtung von Leitlitz nach Triebes der Brand", "der Brand"),
    ("liegen bei Langenwetzendorf die Hart", "Hart"),
    ("; dann ", ", "),
    ("der große und kleine Silberberg", "großer Silberberg, kleiner Silberberg"),
    ("die obere und untere Hart", "obere Hart, untere Hart"),
    ("obere und untere Trog", "obere Trog, untere Trog"),
    ("großer und kleiner Brand", "großer Brand, kleiner Brand"),
    ("der Mühlberg, Honigberg", "der Mühlberg, Honigberg"),
]
ARTICLES = {"der", "die", "das", "den", "dem", "des"}


def segment_text(page, bid, anchors):
    if page == "17+18":
        t = text("17", "b2") + text("18", "b1")
        t = re.sub(r"-\s*(?=hügel)", "", t)      # 'Geiers-' + 'hügel'
    else:
        t = text(page, bid)
    t = re.sub(r"\s+", " ", t)
    out = []
    pos = []
    for gebiet, a in anchors:
        i = t.find(a) if a else 0
        assert i >= 0, (page, bid, a)
        pos.append((i + len(a), gebiet))
    for k, (start, gebiet) in enumerate(pos):
        end = pos[k + 1][0] - len(anchors[k + 1][1]) if k + 1 < len(pos) else len(t)
        # cut the tail of the previous segment before the next anchor phrase; drop leading words of the following anchor
        seg = t[start:end]
        out.append((gebiet, seg))
    return out


def split_names(seg):
    s = seg
    s = re.sub(r"\*+\)?", "", s)
    s = re.sub(r"\([^)]*\)", "", s)               # alternative names / qualifiers
    s = s.replace("-hügel", "hügel") if False else s
    for a, b in SPECIAL:
        s = s.replace(a, b)
    s = s.replace("Geiers- hügel", "Geiershügel").replace("Geiers-hügel", "Geiershügel")
    s = re.sub(r"[;:]", ",", s)
    s = s.strip().rstrip(".")
    s = re.sub(r"\s+und\s*$", "", s)
    parts = re.split(r",\s*|\s+und\s+", s)
    names = []
    for p in parts:
        p = p.strip().strip(".").strip()
        if not p:
            continue
        p = re.sub(r"^und\s+", "", p)
        p = re.sub(r"\s+bei [A-ZÄÖÜ]\w+$", "", p)
        p = re.sub(r"\s+mit dem Osterstein$", "", p)
        p = re.sub(r"^sog\.\s*", "", p)
        w = p.split(" ")
        while w and w[0] in ARTICLES:
            w = w[1:]
        if w:
            names.append(" ".join(w))
    return names


def all_names():
    res = []
    for page, bid, lt, gr, anchors in SEGS:
        # blocks with a single (empty-anchor) continuation segment
        segs = segment_text(page, bid, anchors)
        for gebiet, seg in segs:
            for n in split_names(seg):
                res.append(dict(page=page, block=bid, landesteil=lt, grossraum=gr, gebiet=gebiet, name=n))
    return res


if __name__ == "__main__":
    import collections
    R = all_names()
    print(len(R), collections.Counter(r["landesteil"] for r in R), collections.Counter(r["grossraum"] for r in R))
    for g in dict.fromkeys(r["gebiet"] for r in R):
        print(g, [r["name"] for r in R if r["gebiet"] == g][:60])
