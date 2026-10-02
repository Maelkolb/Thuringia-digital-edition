"""Shared extraction of Brückner's height lists (pp. 10-15, 20-24) for the relief analyses (A01).

Provides
  PLACES   - 'Wohnpunkte' (heads of the settlement lists) with min/max height in preuss. Decimalfuss
  SUMMITS  - 'Höhenpunkte / Berghöhen' with one height value
  DFUSS_M  - metres per preuss. Decimalfuss (= 1/10 preuss. Ruthe = 0.3766242 m; Brückner p. 11 fn., p. 831)
"""
import re
from parse_heights import *   # noqa: F401,F403
from common import *          # noqa: F401,F403

# ---------------------------------------------------------------------------------------------------------
# name cleaning
# ---------------------------------------------------------------------------------------------------------
NAME_FIX = {
    "Törbizmühle a. d. Weida": "Sörbitzmühle a. d. Weida",           # facsimile p. 20: "Sörbitzmühle"
    "Nordosthöhe von Dettersdorf (bei den Eisengruben": "Nordosthöhe von Dettersdorf (bei den Eisengruben)",
    "Tummelplatz bei Kießling": "Tummelsplatz bei Kießling",                              # facsimile p. 24: "Tummelsplatz"
    "Südwesthöhe von Rusitz nach Frankenthal": "Südwesthöhe von Rubitz nach Frankenthal",   # facsimile p. 14: "Rubitz"
}


def clean_name(n):
    n = n.strip()
    n = re.sub(r"^\(", "", n)
    n = re.sub(r"(\w)- (\w)", r"\1\2", n)           # line-break hyphen artefacts: 'Süd- west'
    n = n.replace("=", "-")
    n = NAME_FIX.get(n, n)
    return n.strip()


# ---------------------------------------------------------------------------------------------------------
# settlements
# ---------------------------------------------------------------------------------------------------------
SUB_U = re.compile(r"^(Markt|Kirche|Ziegelei|Pfarrhaus|Gutsgebäude|Windmühle|Dorfmitte|Teich|Rittergutsboden|Kammergut|Gottesacker|Fuß der Kirche|oberer Hof|das Westhaus|oberer Rand)")
SUB_O = re.compile(r"^(Kirche|Dorfteich|Dorfsmitte|Dorfmitte|Chausseebrücke|Hungriger Wolf|obere Häuser|unterste Häuser|oberste Häuser|Haupttheil der Stadt|Wiesenthalbrücke|Schloß,|Schloßberg|Thurmruine|Teich|Herrenhaus|am reußischen Hofe|Friedhofsmitte|Bodenhöhe|Wetterfahne|Einzelhaus|Ausgang der Chaussee)")

EINZEL = re.compile(r"(mühle|Mühle|hammer|Hammer|Hochofen|Forsthaus|Chausseehaus|Rettungshaus|Saalhäuser|Waldhäuser|Schäferei|Schmidtsgut|Grüngut|Kolonie|Weidmannsheil|Grauer Affe|Bahnhof|Tinzer Park|Küchengarten|Wirthshaus|Pulverthurm|Bergschlösschen|Bergkirche|Rothenacker Kirche|Arlas, Kirchenruine|Mündung des|goldne Hahn|Wachholderbaum, Chaussee|Göttengrün, Chaussee|^Bellevue|Gottliebsthal)")

LISTS = [
    # (page, block, landesteil, gruppe, subregex)
    ("11", "b13", "Unterland", "Unterland, rechtes Elsterufer", SUB_U),
    ("12", "b1", "Unterland", "Unterland, rechtes Elsterufer", SUB_U),
    ("12", "b3", "Unterland", "Unterland, linkes Elsterufer", SUB_U),
    ("13", "b1", "Unterland", "Unterland, linkes Elsterufer", SUB_U),
    ("20", "b3", "Oberland", "Oberland", SUB_O),
    ("21", "b1", "Oberland", "Oberland", SUB_O),
    ("22", "b1", "Oberland", "Oberland", SUB_O),
]

PLACES = []      # heads
DETAILS = []     # sub entries (church, village centre ...)
_last = None
for page, bid, lt, grp, SUB in LISTS:
    for e in table_entries(page, bid):
        if e.get("lo") is None:
            DETAILS.append(dict(e, landesteil=lt, parent=_last, page=page, block=bid))
            continue
        raw_name = e["name"]
        name = clean_name(raw_name)
        if SUB.match(name):
            DETAILS.append(dict(e, name=name, landesteil=lt, parent=_last, page=page, block=bid))
            continue
        d = dict(page=page, block=bid, ref=e["ref"], name=name, bracket=1 if raw_name.startswith("(") else 0,
                 landesteil=lt, gruppe=grp, lo=e["lo"], hi=e["hi"], rng=1 if e.get("range") else 0,
                 kind="einzelstelle" if EINZEL.search(name) else "ort")
        PLACES.append(d)
        _last = d

# the single 'Lobenstein, unterstes Haus ...' entry: head for the town Lobenstein (lowest house 1250', highest 1300')
for p in PLACES:
    if p["name"].startswith("Lobenstein, unterstes Haus"):
        p["name"] = "Lobenstein"
        p["hi"] = 1300.0
        p["rng"] = 1
        p["note"] = "unterstes Haus im Lemnitzgrunde 1250', oberste Häuser im Koselgrunde 1300'"
    p.setdefault("note", "")

# cell reference for the dataset: e.g. 'r12c1' (merged continuation lines: first row)
for p in PLACES:
    m = re.search(r"/(r\d+c\d)", p["ref"])
    p["cell"] = m.group(1) if m else ""

# ---------------------------------------------------------------------------------------------------------
# summit lists
# ---------------------------------------------------------------------------------------------------------

def _text_entries(page, bid):
    t = text(page, bid)
    lines = [clean(l) for l in t.split("\n")]
    cells = [(f"{page}/{bid}/l{i+1}", l) for i, l in enumerate(lines)]
    return [parse_entry(r, c) for r, c in column_stream(cells)]


_SUM_SRC = [
    ("13", "b3", "Unterland", "t"), ("14", "b1", "Unterland", "x"), ("14", "b2", "Unterland", "x"),
    ("22", "b4", "Oberland", "t"), ("23", "b1", "Oberland", "t"), ("24", "b1", "Oberland", "t"),
]
SUMMITS = []
for page, bid, lt, mode in _SUM_SRC:
    es = table_entries(page, bid) if mode == "t" else _text_entries(page, bid)
    for e in es:
        SUMMITS.append(dict(page=page, block=bid, ref=e["ref"], name_raw=e["name"], landesteil=lt, h=e["lo"], error=e.get("error", False)))
# p. 15 b1: messy 2x4 table, entries read by hand from table + facsimile
SUMMITS += [
    dict(page="15", block="b1", ref="15/b1/r1c1+r2c1", name_raw="Westhöhe (Mühlberg) von Kraftsdorf", landesteil="Unterland", h=955.0),
    dict(page="15", block="b1", ref="15/b1/r3c1", name_raw="Käseberg", landesteil="Unterland", h=958.0),
    dict(page="15", block="b1", ref="15/b1/r4c1", name_raw="Westhöhe von Hundhaupten", landesteil="Unterland", h=975.0),
    dict(page="15", block="b1", ref="15/b1/r1c2", name_raw="Steinbusch (Südwest) b. Kraftsdorf", landesteil="Unterland", h=975.0),
    dict(page="15", block="b1", ref="15/b1/r2c2", name_raw="Südhöhe von Kraftsdorf", landesteil="Unterland", h=975.0),
    dict(page="15", block="b1", ref="15/b1/r3c2+r4c2", name_raw="Scheidberg bei Hundhaupten (Signal)", landesteil="Unterland", h=989.0),
]

DIR_RE = re.compile(r"^(?:Nord|Süd|Ost|West)[a-zäöüß]*höhe\b|^Höhe zwischen|^Berghöhe zwischen|^Chausseehöhe|^Straßenhöhe|^Waldhöhe|^Höchster Punkt|^Höhe\b|^Nordost von|^Buckel zwischen")
BAU_RE = re.compile(r"(Windmühle|Ziegelei|Chaussee|Alter Markt|Rindenhütte|Gypsbrüche|Bahnhof|Chausseerundtheil|Quelle der Rodach|Tummels?platz|Wetterfahne)")


def summit_kind(name):
    if re.match(r"^Signal", name):
        return "detail"
    if BAU_RE.search(name) and not re.search(r"höhe", name.split(" ")[0]):
        return "bauwerk"
    if DIR_RE.search(name):
        return "richtungshoehe"
    return "berg"


for s in SUMMITS:
    s["bracket"] = 1 if s["name_raw"].startswith("(") else 0
    s["name"] = clean_name(s["name_raw"])
    s["kind"] = summit_kind(s["name"])
    m = re.search(r"/(r\d+c\d)", s["ref"])
    s["cell"] = m.group(1) if m else ""
    if not m:
        m2 = re.search(r"/(l\d+)", s["ref"])
        s["cell"] = m2.group(1) if m2 else ""

if __name__ == "__main__":
    import collections
    print(len(PLACES), "places;", len(DETAILS), "details;", len(SUMMITS), "summits")
    print(collections.Counter((p["gruppe"], p["kind"]) for p in PLACES))
    print(collections.Counter((s["landesteil"], s["kind"]) for s in SUMMITS))
    print([s["name"] for s in SUMMITS if s["kind"] == "bauwerk"])
    print([s["name"] for s in SUMMITS if s["kind"] == "detail"])
    print([s["name"] for s in SUMMITS if s["kind"] == "berg"][:200])
    print("errors", [s for s in SUMMITS if s.get("error")])
