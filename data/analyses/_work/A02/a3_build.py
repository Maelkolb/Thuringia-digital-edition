"""Analysis gewaesser-nebenfluesse-verzeichnis: the numbered tributary lists of chapter 6 (pp. 45-53)."""
import re
from collections import Counter
from common import *
from tribs import parse

M = lambda de_, en_: {"de": de_, "en": en_}

REGION = {"Main": "Main (Rhein)", "Saale-Oberland": "Oberland", "Elster-Unterland": "Unterland"}
REGION_ORDER = {"Main (Rhein)": 1, "Oberland": 2, "Unterland": 3}

# principal name of each entry (text only; the numbers come from the printed list numbers)
NAMES = {
    ("Rodach", "links", 1): "Grunsenbach", ("Rodach", "links", 2): "Orlabach", ("Rodach", "links", 3): "Moschwitz (Muschwitz)",
    ("Rodach", "rechts", 1): "Thiersebach (Titschenbach)", ("Rodach", "rechts", 2): "Kettelbach (Kittel-, Ködelbach)",
    ("Saale", "rechts", 2): "Erlichsbach (Aubach)", ("Saale", "rechts", 10): "Waldbach (unbenannt, Harra gegenüber)",
    ("Saale", "rechts", 16): "Triebich (Triebes)", ("Saale", "links", 10): "Kieselbach (Sormitz im Burgwald)",
    ("Saale", "links", 2): "harraer Auwasser", ("Saale", "rechts", 6): "lerchenhügler Wässerlein",
    ("Weida", "links", 3): "Löhlabächlein", ("Weida", "rechts", 7): "Triebes",
    ("Elster", "links", 2): "Briete", ("Elster", "links", 9): "Goldthal- oder Eleonorenthalwasser",
    ("Elster", "rechts", 1): "Wasser von Pohlen", ("Elster", "rechts", 2): "kleinfalkischer Bach (pösnecker Bach)",
    ("Elster", "rechts", 3): "Thälchen von Kaimberg", ("Elster", "rechts", 4): "kleiner Schmerlbach",
    ("Elster", "rechts", 11): "Wässerlein zwischen Kienberg und Pönigsberg", ("Elster", "rechts", 13): "lichtenauer Wässerlein",
    ("Elster", "rechts", 16): "Pleiße", ("Elster", "links", 12): "seifarthsdorfer Bach", ("Elster", "links", 8): "Schafgrund (hartmannsdorfer Bach)",
}
# name types: bach (-bach/-bächlein), wasser (-wasser/-wässerlein), graben, grund, own (own name without generic word),
# desc (descriptive, no proper name)
TYPE_OVERRIDE = {
    ("Saale", "rechts", 10): "desc", ("Elster", "rechts", 1): "desc", ("Elster", "rechts", 3): "desc", ("Elster", "rechts", 11): "desc",
    ("Rodach", "links", 3): "own", ("Saale", "rechts", 16): "own", ("Weida", "rechts", 7): "own", ("Elster", "links", 2): "own",
    ("Elster", "rechts", 16): "own", ("Saale", "rechts", 2): "bach", ("Elster", "links", 8): "grund",
}
KEY_OVERRIDE = {("Saale", "rechts", 16): "Triebes", ("Saale", "rechts", 10): "Waldbach (unbenannt)", ("Saale", "rechts", 2): "Erlichsbach"}


def head(body):
    t = re.sub(r"^(links|rechts):\s*", "", body)
    t = re.sub(r"^(Der|Die|Das|der|die|das|Ein|Eine|Den)\s+", "", t)
    t = re.split(r"\s*\(|,|\s+oder\s+|\s+mit\s+|\s+entsteh|\s+entspring|\s+quillt|\s+mündet|\s+kommt|\s+läuft|\s+bei\s|\s+von\s|\s+im\s|\s+aus\s|\s+und\s|\s+am\s|\s+auf\s|\s+vom\s|\*\)|\s+tritt|\s+heißt|\s+nimmt|\s+erhält|\s+hat|\s+fließt|\s+rinnt|\s+gebildet|\s+östlich|\s+südöstlich|\s+dicht|\.", t)[0]
    return t.strip()


def ntype(name):
    n = name.lower()
    if re.search(r"(wässerlein|wasser)\b", n):
        return "wasser"
    if re.search(r"(bächlein|bach)\b", n):
        return "bach"
    if re.search(r"graben\b", n):
        return "graben"
    if re.search(r"grund\b", n):
        return "grund"
    return "own"


rows = []
src_refs = []
seen_rodach = Counter()
for r in parse():
    num = r["num"]
    if r["river"] == "Rodach":
        seen_rodach[r["bank"]] += 1
        num_local = seen_rodach[r["bank"]]
    else:
        num_local = num
    key = (r["river"], r["bank"], num_local)
    name = NAMES.get(key) or head(r["body"])
    typ = TYPE_OVERRIDE.get(key) or ntype(name)
    nkey = KEY_OVERRIDE.get(key) or re.sub(r"\s*\(.*$", "", name)
    reg = REGION[r["basin"]]
    rows.append([r["river"], reg, REGION_ORDER[reg], r["bank"], num, name, typ, nkey, r["page"], r["block"]])
    src_refs.append({"page": r["page"], "block": r["block"]})

# consistency checks: numbering runs 1..n without gaps per river and bank
for river in ("Saale", "Weida", "Elster"):
    for bank in ("links", "rechts"):
        nums = [x[4] for x in rows if x[0] == river and x[3] == bank]
        assert nums == list(range(1, len(nums) + 1)), (river, bank, nums)

cnt = Counter((x[0], x[3]) for x in rows)
print(cnt)
tot = len(rows)
right = sum(v for (rv, b), v in cnt.items() if b == "rechts")
left = tot - right
by_river = Counter(x[0] for x in rows)
print(tot, right, left, by_river)
tc = Counter((x[1], x[6]) for x in rows)
nreg = Counter(x[1] for x in rows)
for k in sorted(tc):
    print(k, tc[k])
ob = nreg["Oberland"]
un = nreg["Unterland"]
bach_o = tc[("Oberland", "bach")]
bach_u = tc[("Unterland", "bach")]
gg_u = tc[("Unterland", "graben")] + tc[("Unterland", "grund")]
gg_o = tc[("Oberland", "graben")] + tc[("Oberland", "grund")]
own_u = tc[("Unterland", "own")]
own_o = tc[("Oberland", "own")]
ws_o = tc[("Oberland", "wasser")]
ws_u = tc[("Unterland", "wasser")]
print(ob, un, bach_o, bach_u, gg_u, gg_o, own_u, own_o, ws_o, ws_u)
keycount = Counter(x[7] for x in rows)
dups = sorted(k for k, v in keycount.items() if v > 1)
print("repeated keys:", dups, [keycount[k] for k in dups])

pc = lambda a, b: a / b * 100
findings = [
    M(f"Brückner nennt {tot} Zuflüsse erster Ordnung in numerierten Listen: {by_river['Saale']} zur Saale, {by_river['Elster']} zur Elster (nur Unterland), {by_river['Weida']} zur Weida und {by_river['Rodach']} zur Rodach im Maingebiet.",
      f"Brückner lists {tot} first-order tributaries in numbered lists: {by_river['Saale']} to the Saale, {by_river['Elster']} to the Elster (Unterland only), {by_river['Weida']} to the Weida and {by_river['Rodach']} to the Rodach in the Main basin."),
    M(f"An jedem Fluss steht auf der rechten Seite mindestens so viele Zuflüsse wie auf der linken: Saale {cnt[('Saale','rechts')]} gegen {cnt[('Saale','links')]}, Elster {cnt[('Elster','rechts')]} gegen {cnt[('Elster','links')]}, Weida {cnt[('Weida','rechts')]} gegen {cnt[('Weida','links')]}; nur bei der Rodach überwiegt die linke Seite ({cnt[('Rodach','links')]} gegen {cnt[('Rodach','rechts')]}). Für die Saale bestätigt das Brückners Satz, sie habe »die größere Zahl auf der rechten Seite«.",
      f"On every river the right bank has at least as many tributaries as the left: Saale {cnt[('Saale','rechts')]} against {cnt[('Saale','links')]}, Elster {cnt[('Elster','rechts')]} against {cnt[('Elster','links')]}, Weida {cnt[('Weida','rechts')]} against {cnt[('Weida','links')]}; only on the Rodach does the left side prevail ({cnt[('Rodach','links')]} against {cnt[('Rodach','rechts')]}). For the Saale this confirms Brückner's statement that it has “the larger number on the right”."),
    M(f"Die Namen unterscheiden sich zwischen den Landesteilen: Im Oberland enden {bach_o} von {ob} Zuflussnamen ({pc(bach_o,ob):.0f} %) auf -bach/-bächlein, im Unterland nur {bach_u} von {un} ({pc(bach_u,un):.0f} %). Dort tragen {gg_u} von {un} ({pc(gg_u,un):.0f} %) einen Namen auf -graben oder -grund, im Oberland keiner; -wasser/-wässerlein kommt im Unterland etwas häufiger vor ({ws_u} von {un}, {pc(ws_u,un):.0f} %) als im Oberland ({ws_o} von {ob}, {pc(ws_o,ob):.0f} %).",
      f"The names differ between the two parts of the country: in the Oberland {bach_o} of {ob} tributary names ({pc(bach_o,ob):.0f} %) end in -bach/-bächlein, in the Unterland only {bach_u} of {un} ({pc(bach_u,un):.0f} %). There {gg_u} of {un} ({pc(gg_u,un):.0f} %) carry a name in -graben or -grund, in the Oberland none; -wasser/-wässerlein is slightly more frequent in the Unterland ({ws_u} of {un}, {pc(ws_u,un):.0f} %) than in the Oberland ({ws_o} of {ob}, {pc(ws_o,ob):.0f} %)."),
    M("Mehrfach vergebene Namen unter den Hauptzuflüssen sind " + ", ".join(f"{k} ({keycount[k]}×)" for k in dups) + "; Brückner nennt Aubach und Lohbach unter den häufigsten Bachnamen (S. 42).",
      "Names given more than once among the main tributaries are " + ", ".join(f"{k} ({keycount[k]}×)" for k in dups) + "; Brückner names Aubach and Lohbach among the most frequent stream names (p. 42)."),
]
for f in findings:
    print(f["de"])

COLS = [
    {"name": "river", "label": M("Fluss", "River"), "type": "string", "unit": None, "note": "Rodach (Main-Gebiet), Saale und Weida (Oberland), Elster (Unterland); Brückners Kapitelgliederung S. 45"},
    {"name": "region", "label": M("Gebiet", "Region"), "type": "string", "unit": None},
    {"name": "region_order", "label": M("Gebiet (Ordnung)", "Region (order)"), "type": "integer", "unit": None, "derived": True},
    {"name": "bank", "label": M("Uferseite", "Bank"), "type": "string", "unit": None, "note": "links/rechts in Fließrichtung, wie bei Brückner"},
    {"name": "number", "label": M("Nummer in Brückners Liste", "Number in Brückner's list"), "type": "integer", "unit": None, "note": "Bei der Rodach sind die Zuflüsse nicht numeriert (leer)."},
    {"name": "name", "label": M("Name", "Name"), "type": "string", "unit": None},
    {"name": "name_type", "label": M("Namenstyp", "Name type"), "type": "string", "unit": None, "derived": True, "note": "bach = -bach/-bächlein, wasser = -wasser/-wässerlein, graben, grund, own = Eigenname ohne Gattungswort (z. B. Selbitz, Lemnitz), desc = beschreibend, ohne eigenen Namen; Zuordnung editorisch nach dem Wortausgang"},
    {"name": "name_key", "label": M("Namensschlüssel", "Name key"), "type": "string", "unit": None, "derived": True, "note": "Hauptname ohne Klammerzusatz, zum Zählen von Namensdubletten"},
    {"name": "page", "label": M("Seite", "Page"), "type": "string", "unit": None},
    {"name": "block", "label": M("Block", "Block"), "type": "string", "unit": None},
]
# Rodach entries are unnumbered
for r in rows:
    if r[0] == "Rodach":
        r[4] = None

TT = lambda f, d, e: {"field": f, "title": M(d, e)}
BANK = {"calculate": {"de": "datum.bank == 'links' ? 'links' : 'rechts'", "en": "datum.bank == 'links' ? 'left' : 'right'"}, "as": "bank_l"}
c1 = {
    "height": 280,
    "transform": [BANK],
    "mark": "bar",
    "encoding": {
        "x": {"field": "river", "type": "nominal", "title": None, "sort": ["Saale", "Elster", "Weida", "Rodach"], "axis": {"labelAngle": 0}},
        "xOffset": {"field": "bank", "type": "nominal", "sort": ["links", "rechts"]},
        "y": {"aggregate": "count", "type": "quantitative", "title": M("Zahl der genannten Zuflüsse", "Number of tributaries listed")},
        "color": {"field": "bank_l", "type": "nominal", "title": M("Uferseite", "Bank"), "sort": {"field": "bank", "op": "min"}},
        "tooltip": [TT("river", "Fluss", "River"), TT("bank_l", "Uferseite", "Bank"), {"aggregate": "count", "type": "quantitative", "title": M("Zuflüsse", "Tributaries")}],
    },
}
TYPE_L = {"calculate": {"de": "datum.name_type == 'bach' ? '-bach' : datum.name_type == 'wasser' ? '-wasser' : datum.name_type == 'graben' ? '-graben' : datum.name_type == 'grund' ? '-grund' : datum.name_type == 'own' ? 'Eigenname' : 'beschreibend'",
                        "en": "datum.name_type == 'bach' ? '-bach' : datum.name_type == 'wasser' ? '-wasser' : datum.name_type == 'graben' ? '-graben' : datum.name_type == 'grund' ? '-grund' : datum.name_type == 'own' ? 'own name' : 'descriptive'"},
          "as": "type_l"}
TYPE_ORD = {"calculate": "indexof(['bach','wasser','graben','grund','own','desc'], datum.name_type)", "as": "type_order"}
c2 = {
    "height": 200,
    "transform": [TYPE_L, TYPE_ORD],
    "mark": "bar",
    "encoding": {
        "y": {"field": "region", "type": "nominal", "title": None, "sort": {"field": "region_order", "op": "min"}},
        "x": {"aggregate": "count", "type": "quantitative", "stack": "normalize", "title": M("Anteil der Zuflussnamen", "Share of tributary names"), "axis": {"format": "%"}},
        "color": {"field": "type_l", "type": "nominal", "title": M("Namenstyp", "Name type"), "sort": {"field": "type_order", "op": "min"}},
        "order": {"field": "type_order", "type": "quantitative"},
        "tooltip": [TT("region", "Gebiet", "Region"), TT("type_l", "Namenstyp", "Name type"), {"aggregate": "count", "type": "quantitative", "title": M("Anzahl", "Count")}],
    },
}

ana = {
    "id": "gewaesser-nebenfluesse-verzeichnis",
    "title": M("Zuflüsse der Rodach, Saale, Weida und Elster nach Uferseite und Namenstyp", "Tributaries of the Rodach, Saale, Weida and Elster by bank and name type"),
    "category": "hydrology",
    "section": "t1-1-6",
    "sources": src_refs,
    "summary": M(
        f"Brückner gliedert das Gewässernetz in vier Flusssysteme und zählt die Zuflüsse erster Ordnung nacheinander auf, bei Saale, Weida und Elster nach rechtem und linkem Ufer getrennt und durchnumeriert. Die Auswertung macht daraus {tot} Einträge und zählt sie nach Fluss und Uferseite; zusätzlich werden die Namen nach ihrem Ausgang (-bach, -graben, -grund …) in Oberland und Unterland verglichen.",
        f"Brückner divides the drainage network into four river systems and lists the first-order tributaries one after another; for the Saale, Weida and Elster they are separated by right and left bank and numbered. The analysis turns this into {tot} entries and counts them by river and bank; the names are also compared by their ending (-bach, -graben, -grund …) between Oberland and Unterland."),
    "method": M(
        "Aus den Listen S. 45–53 wurde jeder durchnumerierte Eintrag (bei der Rodach jeder unnumerierte Absatz) als ein Zufluss gezählt; Nebenbäche, die nur im Text der Einträge genannt werden (z. B. die Zuflüsse der Wettera), blieben unberücksichtigt. Die Numerierung läuft bei jedem Fluss und Ufer lückenlos von 1 bis n, was die Zählung bestätigt. Der Namenstyp ist nach dem Wortausgang des Hauptnamens editorisch zugeordnet (Beispiel: Kegelbach → -bach, Türkengraben → -graben); Namen wie »Selbitz« oder »Lemnitz« gelten als Eigennamen ohne Gattungswort, Einträge wie »Das Thälchen von Kaimberg« als beschreibend.",
        "Every numbered entry in the lists on pp. 45–53 (for the Rodach every unnumbered paragraph) was counted as one tributary; minor streams that are only named in the text of an entry (e.g. the tributaries of the Wettera) were not counted. The numbering runs without gaps from 1 to n on every river and bank, which confirms the count. The name type is assigned editorially from the ending of the main name (e.g. Kegelbach → -bach, Türkengraben → -graben); names such as “Selbitz” or “Lemnitz” count as own names without a generic word, entries such as “Das Thälchen von Kaimberg” as descriptive."),
    "findings": findings,
    "caveats": [
        M("Die Listen führen nur Zuflüsse erster Ordnung als eigene Einträge; Brückners Gesamtzahl von »300 Quellrieseln, Bächen und Flüssen« (S. 41) ist daher deutlich höher als die hier gezählten Einträge.",
          "The lists give only first-order tributaries as separate entries; Brückner's overall figure of “300 spring rills, brooks and rivers” (p. 41) is therefore well above the entries counted here."),
        M("Die Weida wird bei Brückner unter dem Oberland geführt, mündet aber in die Elster; die Pleiße und andere Elsterzuflüsse außerhalb des Landes erscheinen nur, soweit Brückner ihre Quellwasser im Unterland aufführt.",
          "Brückner lists the Weida under the Oberland although it joins the Elster; the Pleiße and other Elster tributaries outside the country appear only where Brückner lists their headwaters in the Unterland."),
        M("Die Aussage über die Namen beruht auf den Hauptnamen der Einträge; Alternativ- und frühere Namen in Klammern sind nicht mitgezählt. Die Typisierung ist eine grobe, editorische Einteilung.",
          "The statement about names rests on the main names of the entries; alternative and former names in brackets were not counted. The typing is a rough editorial classification."),
    ],
    "datasets": [
        {"name": "tributaries", "title": M("Zuflüsse erster Ordnung nach Brückners Verzeichnis", "First-order tributaries in Brückner's list"), "columns": COLS, "rows": rows,
         "source_refs": src_refs},
    ],
    "charts": [
        {"id": "c1", "dataset": "tributaries",
         "title": M("Zahl der aufgeführten Zuflüsse nach Fluss und Uferseite", "Number of tributaries listed by river and bank"),
         "caption": M("Zuflüsse erster Ordnung nach Brückners Verzeichnis (S. 45–53); links/rechts in Fließrichtung. Die Rodach-Zuflüsse sind unnumeriert.",
                      "First-order tributaries in Brückner's list (pp. 45–53); left/right in flow direction. The Rodach tributaries are unnumbered."),
         "vegalite": c1},
        {"id": "c2", "dataset": "tributaries",
         "title": M("Namenstypen der Zuflüsse in Oberland und Unterland", "Name types of the tributaries in the Oberland and Unterland"),
         "caption": M(f"Anteil der Namensausgänge an allen Zuflüssen des Gebiets (Main: {nreg['Main (Rhein)']}, Oberland: {ob}, Unterland: {un} Einträge). Im Oberland dominiert -bach, im Unterland sind -graben, -grund und -wasser häufiger.",
                      f"Share of name endings among all tributaries of the region (Main: {nreg['Main (Rhein)']}, Oberland: {ob}, Unterland: {un} entries). -bach dominates in the Oberland; -graben, -grund and -wasser are more frequent in the Unterland."),
         "vegalite": c2},
    ],
    "keywords": {"de": ["Zuflüsse", "Nebenflüsse", "Bachnamen", "Saale", "Weida", "Weiße Elster", "Rodach", "Gewässernamen", "Oberland", "Unterland"],
                 "en": ["tributaries", "streams", "stream names", "Saale", "Weida", "White Elster", "Rodach", "hydronyms", "Oberland", "Unterland"]},
    "generated_by": "Claude Sonnet 5.5 (subagent A02)",
    "date": "2026-10-01",
}
write_analysis(ana)
