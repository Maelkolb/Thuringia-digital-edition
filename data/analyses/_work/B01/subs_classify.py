"""Classification layer for the subscriber list: name corrections, place normalisation, region, social group.

All rules are explicit and documented in the analysis text. Name corrections are only those confirmed on the facsimile
(they are also listed in the analysis' transcription_issues).
"""
import json
import re
from common import ROOT
from parse_subscribers import parse

# ---------------------------------------------------------------- confirmed corrections against the facsimile
# (page, row) -> (field, transcribed, printed)
FACSIMILE_FIXES = {
    ("838", "r5"): ("name", "Mauke, Rich.", "Maucke, Rich."),
    ("838", "r7"): ("name", "Meissner", "Meißner"),
    ("838", "r23"): ("place", "Weissendorf.", "Weißendorf."),
    ("839", "r10"): ("name", "Siekmann", "Sieckmann"),
    ("839", "r37"): ("name", "v. Boss", "v. Voß"),
    ("839", "r39"): ("name", "Weissker", "Weißker"),
    ("839", "r40"): ("name", "Weissker", "Weißker"),
    ("839", "r41"): ("name", "Weissker", "Weißker"),
}

# ---------------------------------------------------------------- regions
REG = json.loads((ROOT / "data/registers/ortsregister.json").read_text(encoding="utf-8"))
REG_BY_NAME = {}
for e in REG["entries"]:
    if e.get("pages"):
        REG_BY_NAME.setdefault(e["name"], []).append(e)


def region_of_page(p: int) -> str:
    if 407 <= p <= 569:
        return "gera"
    if 570 <= p <= 705:
        return "schleiz"
    if 706 <= p <= 825:
        return "lobenstein"
    raise ValueError(p)


# place as printed (without final period) -> (normalised place, qualifier, how the region is determined)
PLACE_MAP = {
    "Cuba bei Gera": ("Cuba", "bei Gera"),
    "Zechenhaus bei Lobenstein": ("Zechenhaus", "bei Lobenstein"),
    "Oertelsbruch b. Lobst": ("Oertelsbruch", "bei Lobenstein"),
    "Neuhammer b. Saalburg": ("Neuhammer", "bei Saalburg [sic]"),
    "Neuhammer b. Lobenstein": ("Neuhammer", "bei Lobenstein"),
    "Bellevue bei Ebersdorf": ("Bellevue", "bei Ebersdorf"),
    "Kammergut Harra": ("Harra", "Kammergut"),
    "Schloß Osterstein": ("Osterstein", "Schloß"),
    "Schloß Greiz": ("Greiz", "Schloß"),
    "Duttweiler bei Saarbrücken": ("Duttweiler", "bei Saarbrücken"),
    "Dettersdorf": ("Oettersdorf", "gedruckt Dettersdorf"),
    "Waidmannsheil": ("Weidmannsheil", "gedruckt Waidmannsheil"),
    "Mielsdorf": ("Mielesdorf", "gedruckt Mielsdorf"),
    "Saara": ("Saara", "Groß-/Kleinsaara"),
    "Wüstendittersdorf": ("Wüstendittersdorf", ""),
}
# places that are not in the Ortsregister but located by a qualifier of the list itself
REGION_BY_QUALIFIER = {"Zechenhaus": "lobenstein", "Oertelsbruch": "lobenstein", "Saara": "gera"}
SEE_ALSO_REGION = {"Wüstendittersdorf": "schleiz"}  # register: "Wüstendittersdorf s. Dittersdorf (Schleiz)" -> Dittersdorf W. (Schleiz) 593
OUTSIDE = {"Frankfurt a. M.", "Halle", "Eisenach", "Sondershausen", "Weimar", "Greifswald", "Greiz", "Dresden", "Karlsruhe", "Meiningen",
           "Altenhausen", "Potsdam", "München", "Wiesbaden", "Darmstadt", "Braunschweig", "Berlin", "Rudolstadt", "Leipzig", "Oldenburg",
           "Schwerin", "Duttweiler", "Rückersdorf"}


def place_info(printed: str):
    p = printed.strip().rstrip(".").strip()
    norm, qual = PLACE_MAP.get(p, (p, ""))
    if p in ("Frankfurt a. M",):
        norm = "Frankfurt a. M."
    if norm in OUTSIDE:
        return norm, qual, "outside", "außerhalb: nicht im Ortsregister" if norm == "Rückersdorf" else "außerhalb"
    if norm in REGION_BY_QUALIFIER:
        return norm, qual, REGION_BY_QUALIFIER[norm], "nach Zusatz der Liste"
    if norm in SEE_ALSO_REGION:
        return norm, qual, SEE_ALSO_REGION[norm], "Ortsregister (Verweis)"
    if norm == "Neuhammer":
        return norm, qual, region_of_page(int(REG_BY_NAME[norm][0]["pages"][0])), "Ortsregister (Neuhammer b. Saaldorf, S. 727)"
    ents = REG_BY_NAME.get(norm)
    if not ents:
        raise KeyError(f"place not found in Ortsregister: {printed!r} -> {norm!r}")
    regs = {region_of_page(int(pg)) for e in ents for pg in e["pages"]}
    assert len(regs) == 1, (norm, regs)
    return norm, qual, regs.pop(), "Ortsregister"


# ---------------------------------------------------------------- social groups
INSTITUTION_KINDS = [
    (r"Ministerium|Justizamt|Kreisgericht|Kammer, f|Landrathsamt|Hauptsteueramt|Rentamt|Stadtrath", "authority"),
    (r"(?i)bibliothek", "library"),
    (r"Verein|Gesellschaft", "society"),
    (r"Societät|Direction", "company"),
]
GROUPS = [  # (code, regex on occupation) - first match wins
    ("court", r"Fürst|Kammerherr|Hofbibliothekar|Hofgärtner|Hofcantor|Hofthierarzt|Kammerfourier"),
    ("booksellers", r"(?i)buchhandlung|buchhändler"),
    ("teachers", r"Lehrer|Oberlehrer|^Cantor|Collabor|Schuldirektor|Gymnasial-Director"),
    ("clergy", r"Pastor|Pfarrer|Oberpfarrer|Diaconus|Superintendent|Kirchenrath|Catechet"),
    ("forestry_mining", r"förster|Forst|Steiger|Bergverwalter|Bergmeister"),
    ("officials", r"Bürgermeister|Justiz|Geheimrath|Kreis-Gerichts-Rath|Advocat|Advokat|Rechts-Anwalt|Assessor|Aktuar|Kammerrath|Cabinetsrath|"
                  r"Steuer|Rendant|Rentmeister|Amtswachtmeister|Post|Telegraphist|Landrathsamts|Hypoth|Bauinspector|Geometer|Amtmännin"),
    ("trade", r"Kaufmann|Commerzienrath|Chem\. Fabrik|Mühlenbesitzer|schneidemühle|Brauereibesitzer|^Brauer|Buchdruckereibesitzer|Gerbereibesitzer|"
              r"Gastgeber|Gastwirth|Hotelier"),
    ("craftsmen", r"Buchbinder|Kupferstecher|Optikus|Werkführer|Platzmeister"),
    ("farmers", r"Gutsbesitzer|Oeconom|(?i:pachter)|Verwalter|Kunstgärtner"),
    ("others", r"Arzt|Dr\. med|Apotheker|Architect|Rentier|^Director|^Dr\."),
]
GROUP_LABELS = {
    "court": ("Adel und Hof", "Nobility and court"),
    "clergy": ("Geistliche, Kirchenbeamte", "Clergy and church officials"),
    "teachers": ("Lehrer und Kantoren", "Teachers and cantors"),
    "officials": ("Beamte und Juristen", "Officials and jurists"),
    "forestry_mining": ("Forst- und Bergbeamte", "Forestry and mining staff"),
    "trade": ("Kaufleute, Gewerbe, Gastwirte", "Merchants, industry, innkeepers"),
    "booksellers": ("Buchhandlungen", "Booksellers"),
    "craftsmen": ("Handwerker, Techniker", "Craftsmen and technicians"),
    "farmers": ("Landwirte, Gutsverwalter", "Farmers, estate managers"),
    "others": ("Ärzte, Apotheker u. a.", "Physicians, pharmacists, others"),
    "institutions": ("Behörden, Bibliotheken, Vereine", "Institutions"),
}
REGION_LABELS = {
    "gera": ("Gera", "Gera"),
    "schleiz": ("Schleiz", "Schleiz"),
    "lobenstein": ("Lobenstein-Ebersdorf", "Lobenstein-Ebersdorf"),
    "outside": ("außerhalb", "outside"),
}


def clean_occ(o: str) -> str:
    o = o.strip()
    if o.endswith(".") and not re.search(r"(Dr|em|phil|med|Hypoth|Ger|Chem|pract)\.$", o):
        o = o[:-1]
    return o


def build():
    recs = parse()
    out = []
    for r in recs:
        key = (r["page"], r["row"].split("+")[0])
        name, place_pr = r["name"], r["place"]
        if key in FACSIMILE_FIXES:
            field, was, now = FACSIMILE_FIXES[key]
            if field == "name":
                assert name == was, (key, name, was)
                name = now
            else:
                assert place_pr == was, (key, place_pr, was)
                place_pr = now
        occ = clean_occ(r["occupation"])
        title = {"": "", '"': "Herr", "Herr": "Herr", "Frau": "Frau"}[r["title"]]
        # --- the four princely entries: split address form / name / office
        if r["page"] == "835" and r["row"] in ("r2", "r3", "r4", "r5"):
            m = re.match(r"^(.*?(?:Herr|Frau))\s+(.*?),\s+(.*)$", name)
            title, name, occ = m.group(1), m.group(2), m.group(3)
        place_norm, qualifier, region, how = place_info(place_pr)
        entity = "person" if title else "institution"
        if re.search(r"(?i)buchhandlung", occ) and (not title or " & " in name):
            entity = "firm"
        grp = None
        if entity == "institution":
            grp = "institutions"
            kind = next(k for rx, k in INSTITUTION_KINDS if re.search(rx, name, re.I))
        else:
            kind = ""
            for g, rx in GROUPS:
                if re.search(rx, occ, re.I):
                    grp = g
                    break
            assert grp, (name, occ)
        # Catechet + Oberlehrer -> teachers is covered by rule order; bare Catechet -> clergy (documented)
        out.append(dict(r, key=key, title=title, name=name, occupation=occ, place_printed=place_pr.rstrip(".").strip(),
                        place=place_norm, qualifier=qualifier, region=region, region_how=how, entity=entity, group=grp, inst_kind=kind,
                        copies=int(r["copies"]), noble=int(bool(re.match(r"^v\. ", name)))))
    return out


if __name__ == "__main__":
    import sys
    from collections import Counter
    sys.stdout.reconfigure(encoding="utf-8")
    d = build()
    print(len(d), sum(x["copies"] for x in d))
    c = Counter(); cc = Counter()
    for x in d:
        c[x["group"]] += 1; cc[x["group"]] += x["copies"]
    for g, n in c.most_common():
        print(g, n, cc[g])
    print()
    for g in GROUP_LABELS:
        print(g, sorted({x["occupation"] for x in d if x["group"] == g}))
    print()
    pc = Counter(); pcc = Counter()
    for x in d:
        pc[(x["place"], x["region"])] += 1; pcc[(x["place"], x["region"])] += x["copies"]
    for (p, r), n in pc.most_common(30):
        print(p, r, n, pcc[(p, r)])
    rc = Counter(); rcc = Counter()
    for x in d:
        rc[x["region"]] += 1; rcc[x["region"]] += x["copies"]
    print(rc, rcc)
