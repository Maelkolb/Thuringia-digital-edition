"""Parse the two exclusive-species lists of Brückner pp. 72-74 into tidy rows."""
import re
from common import *

# p.72 b5: two-column list set as running text (left column, then right column per line).
# Entered as (left, right) pairs exactly in the order of the printed lines; "-" = genus of
# the entry above in the same column.  Every string is asserted against the block text.
P72_LINES = [
    ("Acer Pseudoplatanus", "Rosa cinnamomea"),
    ("Clematis Vitalba", "- pumila"),
    ("Myosurus minimus", "- gallica"),
    ("Ranunculus Lingua", "Crataegus monogyna"),
    ("Corydalis solida", "Sempervivum soboliferum"),
    ("- pumila", "Silaus pratensis"),
    ("Conringia orientalis", "Seseli annuum"),
    ("Dianthus superbus", "Laserpitium pruthenicum"),
    ("Lepigonum rubrum", "Galium tricorne"),
    ("Geranium phaeum", "Scabiosa ochroleuca"),
    ("Coronilla varia", "Inula britannica"),
    ("Potentilla Fragariastrum", "Pulicaria dysenterica"),
    ("Rosa pimpinellifolia", "Helichrysum arenarium"),
]
P72_FLAGS = {"Ranunculus Lingua": "angeblich auch bei Plothen", "Corydalis pumila": "bei Köstritz, sonst nicht in Thüringen"}

FOOT = re.compile(r"\*\)|†+\)|\*")


def clean(cell):
    s = FOOT.sub("", cell)
    doubtful = "zweifelhaft" in s
    s = re.sub(r"\(zweifelhaft\)", "", s)
    s = s.split(",")[0].strip().rstrip(".").strip()
    return s, doubtful


def parse_grid(label, bid, doubtful_marked):
    rows = []
    last = [None, None]
    for r_i, row in enumerate(grid(label, bid), start=1):
        for c_i, cell in enumerate(row):
            if not cell.strip():
                continue
            name, doubt = clean(cell)
            star = "*)" in cell or "*" in cell
            if name.startswith("-"):
                name = last[c_i] + " " + name.lstrip("- ").strip()
            genus = name.split()[0]
            last[c_i] = genus
            rows.append({"page": label, "block": bid, "row": r_i, "col": c_i + 1, "name": name, "genus": genus,
                         "doubtful": doubt or star})
    return rows


def unterland():
    rows = []
    last = [None, None]
    for i, pair in enumerate(P72_LINES, start=1):
        for c, cell in enumerate(pair):
            need(cell.lstrip("- ").split()[-1], "72", "b5")
            name = cell
            if name.startswith("-"):
                name = last[c] + " " + name.lstrip("- ").strip()
            genus = name.split()[0]
            last[c] = genus
            rows.append({"page": "72", "block": "b5", "row": i, "col": c + 1, "name": name, "genus": genus,
                         "doubtful": False, "note": P72_FLAGS.get(name)})
    rows += parse_grid("73", "b1", True)
    for r in rows:
        r.setdefault("note", None)
        r["region"] = "UL"
    return rows


def oberland():
    rows = parse_grid("73", "b3", True) + parse_grid("74", "b1", True)
    for r in rows:
        r["region"] = "OL"
        r.setdefault("note", None)
    return rows


# genus -> (family [APG IV, modern], dicot/monocot class)  -- editorial, derived
FAMILY = {
    "Acer": "Sapindaceae", "Clematis": "Ranunculaceae", "Myosurus": "Ranunculaceae", "Ranunculus": "Ranunculaceae",
    "Corydalis": "Papaveraceae", "Conringia": "Brassicaceae", "Dianthus": "Caryophyllaceae",
    "Lepigonum": "Caryophyllaceae", "Geranium": "Geraniaceae", "Coronilla": "Fabaceae", "Potentilla": "Rosaceae",
    "Rosa": "Rosaceae", "Crataegus": "Rosaceae", "Sempervivum": "Crassulaceae", "Silaus": "Apiaceae",
    "Seseli": "Apiaceae", "Laserpitium": "Apiaceae", "Galium": "Rubiaceae", "Scabiosa": "Caprifoliaceae",
    "Inula": "Asteraceae", "Pulicaria": "Asteraceae", "Helichrysum": "Asteraceae", "Artemisia": "Asteraceae",
    "Doronicum": "Asteraceae", "Matricaria": "Asteraceae", "Rudbeckia": "Asteraceae", "Solidago": "Asteraceae",
    "Cineraria": "Asteraceae", "Senecio": "Asteraceae", "Echinops": "Asteraceae", "Centaurea": "Asteraceae",
    "Picris": "Asteraceae", "Podospermum": "Asteraceae", "Hypochoeris": "Asteraceae", "Crepis": "Asteraceae",
    "Aster": "Asteraceae", "Achillea": "Asteraceae", "Petasites": "Asteraceae", "Arnoseris": "Asteraceae",
    "Lactuca": "Asteraceae", "Echinospermum": "Boraginaceae", "Asperugo": "Boraginaceae",
    "Lithospermum": "Boraginaceae", "Cynoglossum": "Boraginaceae", "Myosotis": "Boraginaceae",
    "Campanula": "Campanulaceae", "Ledum": "Ericaceae", "Pyrola": "Ericaceae", "Apocynum": "Apocynaceae",
    "Gentiana": "Gentianaceae", "Verbascum": "Scrophulariaceae", "Scrophularia": "Scrophulariaceae",
    "Antirrhinum": "Plantaginaceae", "Linaria": "Plantaginaceae", "Gratiola": "Plantaginaceae",
    "Digitalis": "Plantaginaceae", "Veronica": "Plantaginaceae", "Orobanche": "Orobanchaceae",
    "Pulegium": "Lamiaceae", "Salvia": "Lamiaceae", "Hyssopus": "Lamiaceae", "Melittis": "Lamiaceae",
    "Ajuga": "Lamiaceae", "Teucrium": "Lamiaceae", "Lysimachia": "Primulaceae", "Hottonia": "Primulaceae",
    "Amaranthus": "Amaranthaceae", "Parietaria": "Urticaceae",
    "Orchis": "Orchidaceae", "Anacamptis": "Orchidaceae", "Ophrys": "Orchidaceae", "Cephalanthera": "Orchidaceae",
    "Neottia": "Orchidaceae", "Cypripedium": "Orchidaceae", "Herminium": "Orchidaceae", "Listera": "Orchidaceae",
    "Corallorhiza": "Orchidaceae", "Tulipa": "Liliaceae", "Fritillaria": "Liliaceae", "Gagea": "Liliaceae",
    "Anthericum": "Asparagaceae", "Ornithogalum": "Asparagaceae", "Muscari": "Asparagaceae",
    "Allium": "Amaryllidaceae", "Blysmus": "Cyperaceae", "Carex": "Cyperaceae", "Rhynchospora": "Cyperaceae",
    "Cladium": "Cyperaceae", "Schoenus": "Cyperaceae", "Scirpus": "Cyperaceae", "Cyperus": "Cyperaceae",
    "Andropogon": "Poaceae", "Panicum": "Poaceae", "Corynephorus": "Poaceae", "Triodia": "Poaceae",
    "Agrostis": "Poaceae", "Melica": "Poaceae", "Poa": "Poaceae", "Acorus": "Acoraceae", "Calla": "Araceae",
    "Pulsatilla": "Ranunculaceae", "Epimedium": "Berberidaceae", "Aconitum": "Ranunculaceae",
    "Nymphaea": "Nymphaeaceae", "Nuphar": "Nymphaeaceae", "Barbaraea": "Brassicaceae", "Arabis": "Brassicaceae",
    "Cardamine": "Brassicaceae", "Dentaria": "Brassicaceae", "Erysimum": "Brassicaceae", "Lunaria": "Brassicaceae",
    "Subularia": "Brassicaceae", "Thlaspi": "Brassicaceae", "Lepidium": "Brassicaceae",
    "Hutchinsia": "Brassicaceae", "Viola": "Violaceae", "Drosera": "Droseraceae", "Polygala": "Polygalaceae",
    "Silene": "Caryophyllaceae", "Radiola": "Linaceae", "Malva": "Malvaceae", "Hypericum": "Hypericaceae",
    "Erodium": "Geraniaceae", "Sarothamnus": "Fabaceae", "Cytisus": "Fabaceae", "Trifolium": "Fabaceae",
    "Spiraea": "Rosaceae", "Geum": "Rosaceae", "Comarum": "Rosaceae", "Cotoneaster": "Rosaceae",
    "Epilobium": "Onagraceae", "Circaea": "Onagraceae", "Trapa": "Lythraceae", "Montia": "Montiaceae",
    "Sedum": "Crassulaceae", "Saxifraga": "Saxifragaceae", "Pimpinella": "Apiaceae", "Bupleurum": "Apiaceae",
    "Oenanthe": "Apiaceae", "Archangelica": "Apiaceae", "Peucedanum": "Apiaceae", "Meum": "Apiaceae",
    "Imperatoria": "Apiaceae", "Orlaya": "Apiaceae", "Myrrhis": "Apiaceae", "Chaerophyllum": "Apiaceae",
    "Sambucus": "Adoxaceae", "Lonicera": "Caprifoliaceae", "Asperula": "Rubiaceae", "Polemonium": "Polemoniaceae",
    "Pinguicula": "Lentibulariaceae", "Utricularia": "Lentibulariaceae", "Rumex": "Polygonaceae",
    "Thesium": "Santalaceae", "Elatine": "Elatinaceae",
}
MONOCOT_FAMILIES = {"Orchidaceae", "Liliaceae", "Asparagaceae", "Amaryllidaceae", "Cyperaceae", "Poaceae",
                    "Acoraceae", "Araceae"}

# --- Brückner's own corrections, p. 830 (blocks b7-b9, b10) -------------------------------------
# S. 72 Z. 15 v.u.: Laserpitium pruthenicum zu streichen; S. 73: Neottia Nidus avis and Gentiana ciliata zu streichen
# (auch im Oberland), Salvia verticillata für das Unterland einzutragen; Libanotis montana and Phyteum orbiculare
# als nur im Oberland einzutragen; Stern bei Nuphar luteum fällt weg; S. 74: villosum statt vilosum.
DELETE_UL = {"Laserpitium pruthenicum": ("830", "b7"), "Neottia Nidus avis": ("830", "b8"), "Gentiana ciliata": ("830", "b8")}
ADD_UL = [("Salvia verticillata", "Salvia", "830", "b8")]
ADD_OL = [("Libanotis montana", "Libanotis", "830", "b9"), ("Phyteum orbiculare", "Phyteum", "830", "b9")]
FAMILY.update({"Phyteum": "Campanulaceae", "Libanotis": "Apiaceae"})
SPELLING = {"Sedum vilosum": "Sedum villosum"}


def corrected_sets():
    ul = {r["name"] for r in unterland() if r["name"] not in DELETE_UL} | {n for n, *_ in ADD_UL}
    ol = {r["name"] for r in oberland()} | {n for n, *_ in ADD_OL}
    return ul, ol


if __name__ == "__main__":
    from collections import Counter
    ul, ol = unterland(), oberland()
    print(len(ul), len(ol))
    for r in ul + ol:
        if r["genus"] not in FAMILY:
            print("NO FAMILY", r["genus"], r["name"])
    for nm, L in (("UL", ul), ("OL", ol)):
        mono = sum(FAMILY[r["genus"]] in MONOCOT_FAMILIES for r in L)
        print(nm, len(L), "monocots", mono, "dicots", len(L) - mono, "distinct", len({r['name'] for r in L}))
        c = Counter(r["name"] for r in L)
        print([k for k, v in c.items() if v > 1])
        print(Counter(FAMILY[r["genus"]] for r in L).most_common(30))
    both = {r["name"] for r in ul} & {r["name"] for r in ol}
    print("in both", both)
    print([r["name"] for r in ul + ol if r["doubtful"]])
