"""Parsing of the industry tables pp. 252-255 (shared by the industry analyses)."""
import re
import sys
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\A10")
from common import *

DISTRICTS = ["Gera", "Schleiz", "Lobenstein-Ebersdorf"]
DIST_EN = {"Gera": "Gera", "Schleiz": "Schleiz", "Lobenstein-Ebersdorf": "Lobenstein-Ebersdorf"}
BRANCHES = ["Nahrung", "Kleidung", "Bauhandwerker", "Hausausstattung", "Sonstige"]
BRANCH_EN = {"Nahrung": "Food", "Kleidung": "Clothing", "Bauhandwerker": "Building trades",
             "Hausausstattung": "Household and farm equipment", "Sonstige": "Other industry"}

# cleaned German name -> (printed name expanded, English)
TR = {
    "Müller": ("Müller", "Miller"),
    "Bäcker u. Conditor": ("Bäcker und Conditor", "Baker and confectioner"),
    "Fleischer": ("Fleischer", "Butcher"),
    "Fischer": ("Fischer", "Fisherman"),
    "Brauer": ("Brauer", "Brewer"),
    "Branntweinbrenner": ("Branntweinbrenner", "Distiller"),
    "Weber": ("Weber", "Weaver"),
    "Spinnereibesitzer": ("Spinnereibesitzer", "Spinning-mill owner"),
    "Tuchmacher": ("Tuchmacher", "Cloth maker"),
    "Wollen- und Tuchwaarenfabriker": ("Wollen- und Tuchwaarenfabriker", "Woollen and cloth manufacturer"),
    "Färber": ("Färber", "Dyer"),
    "Gerber": ("Gerber", "Tanner"),
    "Posamentirer": ("Posamentirer", "Trimmings maker"),
    "Schneider": ("Schneider", "Tailor"),
    "Schuhmacher": ("Schuhmacher", "Shoemaker"),
    "Strick-, Sticker- u. Spinner": ("Strick-, Sticker- und Spinner", "Knitter, embroiderer and spinner"),
    "Putzmacher": ("Putzmacher", "Milliner"),
    "Strumpfwirker": ("Strumpfwirker", "Stocking weaver"),
    "Strumpfwaarenfabrikanten": ("Strumpfwaarenfabrikanten", "Hosiery manufacturer"),
    "Beutler, Kürschner, Handschuh- und Mützenmacher": ("Beutler, Kürschner, Handschuh- und Mützenmacher", "Pouch, fur, glove and cap makers"),
    "Hutmacher": ("Hutmacher", "Hatter"),
    "Glaser": ("Glaser", "Glazier"),
    "Maurer, Steinhauer": ("Maurer, Steinhauer", "Mason, stonecutter"),
    "Lackirer, Tüncher, Stubenmaler": ("Lackirer, Tüncher, Stubenmaler", "Varnisher, whitewasher, house painter"),
    "Schornsteinfeger": ("Schornsteinfeger", "Chimney sweep"),
    "Dachdecker": ("Dachdecker", "Roofer"),
    "Ziegelbrenner": ("Ziegelbrenner", "Brickmaker"),
    "Zimmerleute": ("Zimmerleute", "Carpenter"),
    "Gürtler, Rothgießer": ("Gürtler, Rothgießer", "Brazier, brass founder"),
    "Klempner": ("Klempner", "Tinsmith"),
    "Kupferschmiede": ("Kupferschmiede", "Coppersmith"),
    "Schlosser, Feilenhauer": ("Schlosser, Feilenhauer", "Locksmith, file cutter"),
    "Schmiede": ("Schmiede", "Blacksmith"),
    "Zinngießer": ("Zinngießer", "Pewterer"),
    "Nadler": ("Nadler", "Needle maker"),
    "Drahtbinder": ("Drahtbinder", "Wire binder"),
    "Böttcher": ("Böttcher", "Cooper"),
    "Bürstenmacher": ("Bürstenmacher", "Brush maker"),
    "Drechsler": ("Drechsler", "Turner"),
    "Korb- u. Siebmacher": ("Korb- und Siebmacher", "Basket and sieve maker"),
    "Tischler": ("Tischler", "Joiner"),
    "Wagner": ("Wagner", "Wheelwright"),
    "Holzschuhmacher, Muldenhauer": ("Holzschuhmacher, Muldenhauer", "Clog and trough maker"),
    "Kammmacher": ("Kammmacher", "Comb maker"),
    "Riemer, Sattler, Tapezirer": ("Riemer, Sattler, Tapezirer", "Harness maker, saddler, upholsterer"),
    "Seiler": ("Seiler", "Rope maker"),
    "Töpfer": ("Töpfer", "Potter"),
    "Porzellanmaler": ("Porzellanmaler", "Porcelain painter"),
    "Porzellanwaaren= fabrikanten": ("Porzellanwaarenfabrikanten", "Porcelain manufacturer"),
    "Maschinenbauer": ("Maschinenbauer", "Machine builder"),
    "Mühlenbauer": ("Mühlenbauer", "Millwright"),
    "Apotheker": ("Apotheker", "Pharmacist"),
    "Hebammen": ("Hebammen", "Midwife"),
    "Barbierer": ("Barbierer", "Barber"),
    "Seifensieder": ("Seifensieder", "Soap boiler"),
    "Hadersammler": ("Hadersammler", "Rag collector"),
    "Papiermüller": ("Papiermüller", "Paper miller"),
    "Buchdrucker": ("Buchdrucker", "Printer"),
    "Buchbinder": ("Buchbinder", "Bookbinder"),
    "Abschreiber": ("Abschreiber", "Copyist"),
    "Mechaniker": ("Mechaniker", "Mechanic"),
    "Uhrmacher": ("Uhrmacher", "Watchmaker"),
    "Kupferstecher, Lithographen": ("Kupferstecher, Lithographen", "Engraver, lithographer"),
    "Photographen": ("Photographen", "Photographer"),
    "Instrumentenmach": ("Instrumentenmacher", "Instrument maker"),
    "Gold- u. Silberarb": ("Gold- und Silberarbeiter", "Gold and silver worker"),
    "Büchsenmacher": ("Büchsenmacher", "Gunsmith"),
    "Tabaksfabrikanten": ("Tabaksfabrikanten", "Tobacco manufacturer"),
    "Saline": ("Saline", "Saltworks"),
    "Chem. Fabrik": ("Chemische Fabrik", "Chemical factory"),
    "Wasenmeister": ("Wasenmeister", "Knacker"),
    "Fabrikarbeiter ohne angegeb. Fabrikzweig": ("Fabrikarbeiter ohne angegebenen Fabrikzweig", "Factory workers, branch not stated"),
    "Nichtbenannte Nahrungszweige": ("Nichtbenannte Nahrungszweige", "Unnamed food trades"),
}


def clean(name):
    n = re.sub(r"\*+\)", "", name)
    n = n.replace("= ", "=").replace("Feilen=hauer", "Feilenhauer")
    n = re.sub(r"\s*(\.\s?)+$", "", n.strip())
    n = re.sub(r"\s+", " ", n).strip()
    n = n.replace("Barbierer.", "Barbierer")
    n = n.replace("Feilen=hauer", "Feilenhauer").replace("Mechaniker ", "Mechaniker").strip()
    n = n.replace("Mechaniker .", "Mechaniker")
    n = re.sub(r"\s*\.\s*\.$", "", n)
    if n == "Porzellanwaaren=fabrikanten":
        n = "Porzellanwaaren= fabrikanten"
    n = n.rstrip(" .")
    return n


def parse_trades():
    """returns list of dict(branch, trade_key, row_ref, vals(16 ints/None))"""
    out = []
    branch = None
    spec = [("252", "b4"), ("253", "b1"), ("254", "b1")]
    for label, bid in spec:
        for i, r in enumerate(grid(label, bid), start=1):
            if len(r) != 17:
                continue
            name = r[0].strip()
            if re.match(r"^1\)", name):
                branch = "Nahrung"; continue
            if re.match(r"^2\)", name):
                branch = "Kleidung"; continue
            if re.match(r"^3\)", name):
                branch = "Bauhandwerker"; continue
            if re.match(r"^4\)", name):
                branch = "Hausausstattung"; continue
            if re.match(r"^5\)", name):
                branch = "Sonstige"; continue
            if name in ("Industrie.", "", "Summe", "Latus", "Transport"):
                continue
            vals = [num(x) for x in r[1:]]
            out.append({"branch": branch, "key": clean(name), "ref": f"S. {label} {bid} r{i}", "vals": vals, "raw": name,
                        "page": label, "block": bid, "row": i})
    return out


def sums_rows():
    """printed Summe rows: dict (page,row) -> vals"""
    res = {}
    for label, bid in [("252", "b4"), ("253", "b1"), ("254", "b1")]:
        for i, r in enumerate(grid(label, bid), start=1):
            if len(r) == 17 and r[0].strip() in ("Summe",):
                res[(label, i)] = [num(x) or 0 for x in r[1:]]
    return res


if __name__ == "__main__":
    T = parse_trades()
    print(len(T))
    for t in T:
        if t["key"] not in TR:
            print("NO MAPPING", repr(t["key"]), repr(t["raw"]))
    zero = [t["key"] for t in T if all(v is None for v in t["vals"])]
    print("all-dash rows", zero)
