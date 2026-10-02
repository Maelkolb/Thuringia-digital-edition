"""Parse Brückner's conversion table (pp. 831 b7/b8 and 832 b1-b12) into one record per unit definition.

Everything is read from the canonical page JSON; nothing is typed by hand except the editorial
normalisations (short unit name, district label, quantity code) that are rule based and listed below.
"""
import re
from fractions import Fraction
from common import block

def num(s: str) -> float:
    return float(s.replace(",", "."))

SECTIONS = {  # printed heading -> (roman number, quantity code)
    "I": "length", "II": "area", "III": "capacity", "IV": "weight", "V": "firewood", "VI": "stone", "VII": "distance",
}
DISTRICT_NORM = [  # (regex on printed heading, normalised district)
    (r"im ganzen F", "ganzes Fürstenthum"),
    (r"in Gera|Landestheil Gera", "Gera"),
    (r"Schleiz", "Schleiz"),
    (r"Saalburg", "Saalburg"),
    (r"Lobenstein", "Lobenstein"),
    (r"Hirschberg", "Hirschberg"),
]
BASE = {  # printed unit -> (factor, base unit)
    "Meter": (1, "m"), "Quadratmeter": (1, "m²"), "Hectaren": (10000, "m²"),
    "Liter": (1, "L"), "Hectoliter": (100, "L"), "Kilogramm": (1, "kg"),
    "Kubikmeter": (1, "m³"), "künftige Meile": (7500, "m"),
}


def norm_district(printed: str) -> str:
    for rx, d in DISTRICT_NORM:
        if re.search(rx, printed):
            return d
    return "ohne Angabe"


def short_unit(defn: str) -> str:
    s = re.sub(r"^1\s+", "", defn)
    return re.split(r"\s*\(|,", s)[0].strip()


def parse():
    recs = []
    sec = None            # roman numeral
    district_printed = "" # heading text as printed ("in Gera")
    foot = None           # foot length noted in a wood-measure heading (par. Linien)
    last_unit = None

    def add(page, blk, ref, defn, val, unit_printed, extra=None):
        nonlocal last_unit
        r = dict(page=page, block=blk, ref=ref, section=sec, quantity=SECTIONS[sec], district_printed=district_printed or "",
                 district=norm_district(district_printed) if district_printed else "ohne Angabe", definition=defn.strip(),
                 unit=short_unit(defn), value=num(val) if val else None, unit_printed=unit_printed)
        m = re.search(r"\((\d+) Kannen\)|(\d+) K\.\)", defn)
        r["n_kannen"] = int(m.group(1) or m.group(2)) if m else None
        m = re.search(r"(\d+,\d+) (?:pariser Linien|par\. Lin\.|par\. L\.)", defn)
        r["ref_par_lin"] = num(m.group(1)) if m else None
        if extra:
            r.update(extra)
        recs.append(r)

    # --- p. 831 b7 heading + b8 grid -----------------------------------------------------------
    sec = "I"
    grid = block("831", "b8")["grid"]
    for i, row in enumerate(grid, start=1):
        if row[1] == "" and row[2] == "":          # header/group row: "a) im ganzen Fürstenthume:"
            district_printed = re.sub(r"^[a-f]\)\s*", "", row[0]).rstrip(":").strip()
            continue
        m = re.match(r"^([0-9]+,[0-9]+)\s*(.*)$", row[2])
        val, unit = m.group(1), m.group(2).strip().rstrip(".")
        unit = last_unit if unit in ('"', "") else unit
        last_unit = unit
        add("831", "b8", f"r{i}", row[0], val, unit)

    # --- p. 832 ---------------------------------------------------------------------------------
    def lines(bid):
        return [l.strip() for l in block("832", bid)["text"].split("\n") if l.strip()]

    def run(bid, section):
        nonlocal sec, district_printed, foot, last_unit
        sec = section
        district_printed = ""
        foot = None
        last_unit = None
        for li, l in enumerate(lines(bid), start=1):
            if re.match(r"^[a-d]\)\s", l) and l.endswith(":"):
                district_printed = re.sub(r"^[a-d]\)\s*", "", l).rstrip(":").strip()
                m = re.search(r"den Fuß zu (\d+,\d+) par", l)
                foot = num(m.group(1)) if m else None
                continue
            if l.startswith("("):                   # note line, e.g. (Leipz. Maß, den Fuß = 125,3 par. Linien.)
                m = re.search(r"Fuß = (\d+,\d+) par", l)
                foot = num(m.group(1)) if m else foot
                continue
            if "gilt beim Chausseebau" in l:
                add("832", bid, f"l{li}", "die geraische Ruthe gilt beim Chausseebau, die schleizer Schachtruthe auch im Privatverkehr", None, "",
                    {"unit": "Ruthe/Schachtruthe", "foot": None})
                continue
            if l.startswith("die schleizer Schachtruthe"):
                continue
            m = re.match(r"^(1 .*?)\s*=\s*([0-9]+,[0-9]+)\s+(.+?)\.?$", l)
            if not m:
                raise ValueError((bid, l))
            defn, val, unit = m.groups()
            unit = unit.strip()
            if unit.startswith("künftige Meile"):
                unit = "künftige Meile"
            if unit in ('"', "„"):
                unit = last_unit
            last_unit = unit
            add("832", bid, f"l{li}", defn, val, unit, {"foot": foot})

    run("b2", "II")
    run("b4", "III")
    run("b6", "IV")
    run("b8", "V")
    run("b10", "VI")
    run("b12", "VII")
    return recs


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    for r in parse():
        print(r["section"], r["quantity"], "|", r["district"], "|", r["unit"], "|", r["definition"], "|", r["value"], r["unit_printed"], "|", r["n_kannen"], r["ref_par_lin"], r.get("foot"))
