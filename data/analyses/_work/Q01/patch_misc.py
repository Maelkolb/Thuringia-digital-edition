"""Q01: idempotent patches that are not plain text normalisation (run after fix_text.py).

 1. id renames of the three analyses with an English id prefix (housing-/dialect-/places-)
 2. `related` links: dangling ids fixed, curated pairs added, every link made symmetric
 3. small content patches (decimal commas in English text, cross-notes between overlapping analyses)
G7's orte-*/ortskunde-* files are never written; links to them are kept symmetric only on the other side.
"""
import glob
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
AN = ROOT / "data" / "analyses"
PREV = AN / "_preview"


def load(i):
    return json.load(open(AN / f"{i}.json", encoding="utf-8"))


def save(d):
    (AN / f"{d['id']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def is_g7(i):
    return False  # G7 has finished (orte-* files are processed like all others)


# ------------------------------------------------------------------ 1. renames
RENAMES = {
    "housing-kirchenneubauten-1611-1842": "wohnen-kirchenneubauten-1611-1842",
    "dialect-sprachproben-orte-und-textsorten": "mundart-sprachproben-orte-und-textsorten",
    "places-ortsnamen-sorbische-wurzeln": "ortsnamen-sorbische-wurzeln",
}
for old, new in RENAMES.items():
    po, pn = AN / f"{old}.json", AN / f"{new}.json"
    if po.exists():
        d = json.load(open(po, encoding="utf-8"))
        d["id"] = new
        pn.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        po.unlink()
    for f in PREV.glob(f"{old}__*"):
        f.unlink()
# references in other analyses
for f in glob.glob(str(AN / "*.json")):
    t = Path(f).read_text(encoding="utf-8")
    t2 = t
    for old, new in RENAMES.items():
        t2 = t2.replace(f'"{old}"', f'"{new}"')
    if t2 != t and not is_g7(Path(f).stem):
        Path(f).write_text(t2, encoding="utf-8")

# ------------------------------------------------------------------ 2. related
FIX_ID = {"geschichte-landerwerb-landverlust-1248-1572": "geschichte-landerwerb-landverlust-1248-1690"}
CURATED = [
    # gewaesser / relief
    ("gewaesser-quellen-muendungen-hoehen", "gewaesser-hauptfluesse-lauf-gefaelle"),
    ("gewaesser-quellen-muendungen-hoehen", "gewaesser-nebenfluesse-verzeichnis"),
    ("gewaesser-hauptfluesse-lauf-gefaelle", "gewaesser-nebenfluesse-verzeichnis"),
    ("gewaesser-quellen-muendungen-hoehen", "relief-hoehenstufen-oberland-unterland"),
    ("gewaesser-quellen-muendungen-hoehen", "relief-erhebungen-hoechste-punkte"),
    ("gewaesser-hauptfluesse-lauf-gefaelle", "relief-hoehenstufen-oberland-unterland"),
    ("gewaesser-heilquellen-lobenstein-analyse", "klima-quellentemperatur-brunnen"),
    ("gewaesser-heilquellen-lobenstein-analyse", "gewaesser-nebenfluesse-verzeichnis"),
    ("klima-quellentemperatur-brunnen", "klima-stationen-temperatur-vergleich"),
    # geologie
    ("geologie-formationen-bodenguete", "geologie-formationen-rohstoffe"),
    ("geologie-formationen-bodenguete", "geologie-fossilfunde-zechstein-clymenienkalk"),
    ("geologie-formationen-rohstoffe", "geologie-fossilfunde-zechstein-clymenienkalk"),
    ("geologie-formationen-bodenguete", "landwirtschaft-bodennutzung-1854"),
    ("geologie-formationen-rohstoffe", "bergbau-erzbergbau-zeitleiste-ober-unterland"),
    ("geologie-formationen-rohstoffe", "bergbau-schieferbrueche-lobenstein-1868"),
    ("geologie-formationen-rohstoffe", "bergbau-bestand-oberland-vor-1648"),
    ("flora-exklusivarten-unterland-oberland", "geologie-formationen-bodenguete"),
    # klima
    ("klima-gera-luftdruck-1856-1867", "klima-gera-temperatur-1856-1867"),
    ("klima-gera-luftdruck-1856-1867", "klima-hoehenlage-temperatur-luftdruck"),
    ("klima-gera-luftdruck-1856-1867", "klima-witterungserscheinungen-gera-1856-1867"),
    ("klima-gera-luftdruck-1856-1867", "klima-stationen-temperatur-vergleich"),
    ("klima-gera-temperatur-1856-1867", "phaenologie-bluetezeiten-gera-hohenleuben-1851-1861"),
    ("klima-stationen-temperatur-vergleich", "phaenologie-bluetezeiten-gera-hohenleuben-1851-1861"),
    ("klima-niederschlagstage-stationen", "klima-bewoelkung-stationen"),
    ("klima-wind-gera-1856-1865", "klima-witterungserscheinungen-gera-1856-1867"),
    ("klima-hoehenlage-temperatur-luftdruck", "relief-wohnorte-hoehenlage"),
    ("phaenologie-zugvoegel-gera-1859-1864", "fauna-voegel-zugzeiten-und-seltene-gaeste"),
    # bevoelkerung / gesundheit
    ("bevoelkerung-geburtensaldo-wanderung-1859-1867", "bevoelkerung-natuerlicher-zuwachs-1858-1867"),
    ("bevoelkerung-geburtensaldo-wanderung-1859-1867", "bevoelkerung-wanderung-1864-1867"),
    ("bevoelkerung-natuerlicher-zuwachs-1858-1867", "bevoelkerung-todtgeborene-1858-1867"),
    ("bevoelkerung-natuerlicher-zuwachs-1858-1867", "bevoelkerung-sterblichkeit-1858-1867"),
    ("bevoelkerung-natuerlicher-zuwachs-1858-1867", "bevoelkerung-geburten-1858-1867"),
    ("bevoelkerung-entwicklung-1647-1867", "bevoelkerung-dichte-1834-1867"),
    ("bevoelkerung-entwicklung-1647-1867", "bevoelkerung-stadt-land-1833-1867"),
    ("bevoelkerung-entwicklung-1647-1867", "bevoelkerung-geschlecht-alter-1834-1867"),
    ("bevoelkerung-entwicklung-1647-1867", "bevoelkerung-geburtensaldo-wanderung-1859-1867"),
    ("bevoelkerung-sterblichkeit-lobenstein-1794-1804", "bevoelkerung-sterblichkeit-1858-1867"),
    ("gesundheit-militaer-tauglichkeit-1864-1866", "bevoelkerung-altersaufbau-1864"),
    ("gesundheit-militaer-tauglichkeit-1864-1866", "militaer-kontingent-reichsmatrikel-bis-1867"),
    ("gesundheit-medizinalwesen-und-seuchen-zeitleiste", "gesundheit-krankheitsstatistik-lobenstein-gera-hohenleuben"),
    ("gesundheit-volksmedizin-hausmittel-nach-leiden", "gesundheit-krankheitsstatistik-lobenstein-gera-hohenleuben"),
    ("gesundheit-selbstmord-unglueck-1858-1867", "gesundheit-taubstumme-blinde-1864-1867"),
    ("wohnen-wohnhaeuser-wohndichte-1867", "versicherung-feuerversicherung-1867-orte"),
    # wirtschaft
    ("wirtschaft-berufsklassen-1864", "industrie-hauptzweige-staedte-plattland-1864"),
    ("wirtschaft-berufsklassen-1864", "industrie-gewerbe-1864-einzelne-gewerbe"),
    ("wirtschaft-berufsklassen-1864", "handel-gewerbe-nach-landesteilen-1864"),
    ("wirtschaft-berufsklassen-1864", "landwirtschaft-grundbesitz-1854"),
    ("industrie-hauptzweige-staedte-plattland-1864", "handel-gewerbe-nach-landesteilen-1864"),
    ("forstwirtschaft-waldflaeche-besitz", "wald-baumarten-flurnamen"),
    ("landwirtschaft-agrarreformen-1836-1868", "landwirtschaft-kammer-rittergueter-1854"),
    ("handel-jahrmaerkte-marktorte-landesteile", "handel-verkehr-begleitscheine-1858-1867"),
    ("bergbau-schieferbrueche-lobenstein-1868", "bergbau-erzbergbau-zeitleiste-ober-unterland"),
    ("bergbau-saline-heinrichshall-absatz-1857-1863", "gewaesser-heilquellen-lobenstein-analyse"),
    # staat / justiz / schule / kirche / armenwesen
    ("staat-haushalt-einnahmen-ausgaben-1866-1868", "staat-schulden-kassenscheine-1857-1866"),
    ("staat-haushalt-einnahmen-ausgaben-1866-1868", "staat-chausseen-laenge-kosten-1868"),
    ("staat-haushalt-einnahmen-ausgaben-1866-1868", "militaer-kontingent-reichsmatrikel-bis-1867"),
    ("verfassung-landtag-gemeinderaete-vertretung", "verwaltung-aerzte-gendarmen-justizaemter-landestheile"),
    ("verwaltung-aerzte-gendarmen-justizaemter-landestheile", "justiz-zivilrechtspflege-einzelgerichte-1864-1867"),
    ("schule-volksschulen-schueler-lehrer-1863-1868", "schule-hoehere-anstalten-schueler-lehrer-1868"),
    ("schule-volksschulen-schueler-lehrer-1863-1868", "schule-stipendien-stiftungen-betraege-gruendung"),
    ("schule-stipendien-stiftungen-betraege-gruendung", "armenwesen-stiftungen-kapital-1828-1866"),
    ("armenwesen-stiftungen-kapital-1828-1866", "armenwesen-selbsthilfe-kassen-gruendungsjahre-1777-1869"),
    ("kirche-ephorien-pfarreien-besoldung-1868", "schule-volksschulen-schueler-lehrer-1863-1868"),
    ("kirche-ephorien-pfarreien-besoldung-1868", "wohnen-kirchenneubauten-1611-1842"),
    # geschichte / genealogie
    ("geschichte-landesteilungen-linien-1240-1870", "geschichte-landerwerb-landverlust-1248-1690"),
    ("geschichte-landesteilungen-linien-1240-1870", "genealogie-voigte-heinriche-1143-1572"),
    ("geschichte-landesteilungen-linien-1240-1870", "genealogie-reuss-lebensdauer-kindersterblichkeit-1550-1850"),
    ("geschichte-chronik-ereignisse-530-1867", "geschichte-landerwerb-landverlust-1248-1690"),
    ("geschichte-chronik-ereignisse-530-1867", "bergbau-bestand-oberland-vor-1648"),
    ("genealogie-voigte-heinriche-1143-1572", "genealogie-reuss-lebensdauer-kindersterblichkeit-1550-1850"),
    ("geschichte-chronik-ereignisse-530-1867", "gesundheit-medizinalwesen-und-seuchen-zeitleiste"),
    # kultur / namen
    ("mundart-sprachproben-orte-und-textsorten", "ortsnamen-sorbische-wurzeln"),
    ("kultur-ortssiegel-motive", "ortsnamen-sorbische-wurzeln"),
    ("kultur-sagenorte-nach-typ-und-landestheil", "ortsnamen-sorbische-wurzeln"),
    ("relief-bergnamen", "ortsnamen-sorbische-wurzeln"),
    ("relief-bergnamen", "fauna-tiernamen-in-flurnamen"),
    # maße / berichtigungen
    ("masse-gewichte-umrechnung-1869", "flaeche-fuerstenthum-vermessung-nachbarn"),
    ("masse-gewichte-umrechnung-1869", "staat-chausseen-laenge-kosten-1868"),
    ("masse-gewichte-umrechnung-1869", "forstwirtschaft-holzpreise-zuwachs"),
    ("masse-gewichte-umrechnung-1869", "relief-wohnorte-hoehenlage"),
    ("masse-gewichte-umrechnung-1869", "klima-gera-luftdruck-1856-1867"),
    ("zusaetze-berichtigungen-1870", "klima-niederschlagstage-stationen"),
    ("zusaetze-berichtigungen-1870", "klima-gewitter-gera-stationen"),
    ("zusaetze-berichtigungen-1870", "klima-regenmenge-gera-1860-1867"),
]
# the six justice analyses belong together
JUSTIZ = ["justiz-zivilrechtspflege-einzelgerichte-1864-1867", "justiz-kreisgerichte-berufungen-konkurse-1864-1867",
          "justiz-strafsachen-einzelrichter-uebertretungen-1864-1867", "justiz-strafsachen-kreisgerichte-staatsanwaltschaft-1864-1867",
          "justiz-gefangene-hafttage-1864-1867", "justiz-freiwillige-gerichtsbarkeit-1864-1867"]
for i, a in enumerate(JUSTIZ):
    for b in JUSTIZ[i + 1:]:
        CURATED.append((a, b))

docs = {Path(f).stem: json.load(open(f, encoding="utf-8")) for f in glob.glob(str(AN / "*.json"))}
rel = {i: list(dict.fromkeys(FIX_ID.get(r, r) for r in (d.get("related") or []))) for i, d in docs.items()}
for a, b in CURATED:
    assert a in docs and b in docs, (a, b)
    rel[a].append(b)
    rel[b].append(a)
# symmetry (also towards G7 files: only the non-G7 side is written)
for i in list(rel):
    for r in list(rel[i]):
        if r in rel and i not in rel[r]:
            rel[r].append(i)
changed = []
for i, d in docs.items():
    if is_g7(i):
        continue
    new = [r for r in dict.fromkeys(rel[i]) if r != i and r in docs]
    if new != (d.get("related") or []):
        d["related"] = new
        changed.append(i)
        save(d)
print("related updated in", len(changed), "files")

# ------------------------------------------------------------------ 3. content patches
def sub_en(d, fn):
    """apply fn to every English string of bilingual nodes (not code)"""
    def walk(n):
        if isinstance(n, list):
            return [walk(x) for x in n]
        if isinstance(n, dict):
            if set(n) == {"de", "en"} and isinstance(n["de"], str):
                return {"de": n["de"], "en": fn(n["en"]) if "datum." not in n["en"] else n["en"]}
            return {k: (v if k == "rows" else walk(v)) for k, v in n.items()}
        return n
    return walk(d)


def sub_both(d, fn_de, fn_en):
    def walk(n):
        if isinstance(n, list):
            return [walk(x) for x in n]
        if isinstance(n, dict):
            if set(n) == {"de", "en"} and isinstance(n["de"], str):
                if "datum." in n["en"]:
                    return n
                return {"de": fn_de(n["de"]), "en": fn_en(n["en"])}
            return {k: (v if k == "rows" else walk(v)) for k, v in n.items()}
        return n
    return walk(d)


def patch(i, fn):
    d = load(i)
    d2 = fn(d)
    if d2 != load(i):
        save(d2)
        print("patched", i)


ident = lambda s: s

# 3a English decimal commas
patch("relief-hoehe-und-lage-neigung", lambda d: sub_en(d, lambda s: s.replace("−0,90", "−0.90").replace("R² = 0,60", "R² = 0.60").replace("R² = 0,06", "R² = 0.06")))
patch("lage-vermessene-punkte-laenge-breite", lambda d: sub_en(d, lambda s: s.replace("59,84″", "59.84″")))
patch("staat-haushalt-einnahmen-ausgaben-1866-1868", lambda d: sub_en(d, lambda s: s.replace("60-thalers difference", "60-thaler difference")))


# 3b cross-notes between overlapping analyses
def add_caveat(d, de, en, marker):
    cv = d.get("caveats", [])
    if any(marker in c["de"] for c in cv):
        return d
    cv = cv + [{"de": de, "en": en}]
    d["caveats"] = cv[:6]
    return d


patch("bevoelkerung-geburtensaldo-wanderung-1859-1867", lambda d: add_caveat(
    d,
    "Für Lobenstein-Ebersdorf 1866 nennt S. 98 922 Geborene (Fürstentum 3620), die Jahrestabelle S. 107 dagegen 925 (3623); die Auswertung »Geborene und Gestorbene 1858–1867: Geburtenüberschuss« verwendet die Zahlen von S. 107, diese Auswertung die von S. 98. Die Dreijahressalden (S. 98–99) sind davon nicht berührt.",
    "For Lobenstein-Ebersdorf in 1866 p. 98 gives 922 births (principality 3,620), whereas the annual table on p. 107 gives 925 (3,623); the analysis “Births and deaths 1858–1867: natural increase” uses the figures of p. 107, this analysis those of p. 98. The three-year balances (pp. 98–99) are not affected.",
    "Für Lobenstein-Ebersdorf 1866 nennt S. 98"))


def ernte_note(d):
    m = d["method"]
    de_add = " In den Bergbau-Auswertungen ist der Zollcentner mit 100 Zollpfund = 50 kg angesetzt; ob Brückners »Centner Roggenwerth« so zu verstehen ist, sagt er nicht, deshalb bleibt die Einheit hier unverändert."
    en_add = " In the mining analyses the Zollcentner is taken as 100 Zollpfund = 50 kg; whether Brückner's “Centner Roggenwerth” is to be read that way he does not say, so the unit is left unchanged here."
    de_add = de_add.replace("Zollcentner", "Zollzentner").replace("»Centner Roggenwerth«", "»Centner Roggenwerth«")
    if "Zollzentner mit 100 Zollpfund" not in m["de"]:
        m["de"] += de_add
        m["en"] += en_add
    return d


patch("landwirtschaft-ernte-versorgung", ernte_note)


# 3c title consistency (DE: no comma before a trailing period; EN: "topic, 1858–1867"; no page numbers or full sentences in titles)
TITLE_EDITS = {
    "bevoelkerung-eheschliessungen-1858-1867": (None, "Marriages, 1858–1867"),
    "bevoelkerung-entwicklung-1647-1867": (None, "Population development by district, 1647–1867"),
    "bevoelkerung-geburten-1858-1867": (None, "Births, 1858–1867: districts, town and country, sex"),
    "bevoelkerung-natuerlicher-zuwachs-1858-1867": (None, "Births and deaths, 1858–1867: natural increase"),
    "bevoelkerung-sterblichkeit-1858-1867": (None, "Deaths and mortality, 1858–1867"),
    "bevoelkerung-todtgeborene-1858-1867": (None, "Stillbirths, 1858–1867"),
    "bevoelkerung-uneheliche-geburten-1858-1867": (None, "Illegitimate births, 1858–1867"),
    "forstwirtschaft-holzpreise-zuwachs": (None, "Timber prices (1800–1868) and growth of the forests"),
    "justiz-kreisgerichte-berufungen-konkurse-1864-1867": (None, "Kreisgerichte, 1864–1867: lawsuits, appeals, bankruptcies and divorces"),
    "schule-volksschulen-schueler-lehrer-1863-1868": (None, "Elementary schools, 1863–1868: pupils and teachers by district, town and country"),
    "staat-haushalt-einnahmen-ausgaben-1866-1868": (None, "State budget, 1866/68: revenue, taxes and itemized expenditure"),
    "staat-schulden-kassenscheine-1857-1866": (None, "State debt and treasury notes compared, 1857–1866"),
    "mundart-sprachproben-orte-und-textsorten": ("Mundartproben nach Orten und Textsorten", "Dialect samples by place and text type"),
    "militaer-kontingent-reichsmatrikel-bis-1867": ("Militärische Gestellungspflicht von Reuß: vom Reichskontingent bis 1867", "Military obligation of Reuss: from the imperial contingent to 1867"),
    "bergbau-schieferbrueche-lobenstein-1868": ("Dachschieferbrüche im Lobenstein-Ebersdorfer Revier 1868", None),
    "verwaltung-aerzte-gendarmen-justizaemter-landestheile": (None, "Physicians, gendarmes and Justizämter in the three districts"),
}
for i, (de, en) in TITLE_EDITS.items():
    d = load(i)
    t = dict(d["title"])
    if de:
        t["de"] = de
    if en:
        t["en"] = en
    if t != d["title"]:
        d["title"] = t
        save(d)
        print("title", i)


# 3d wording: no hype
WORDING = [
    ("industrie-gewerbe-1864-einzelne-gewerbe", "Die Weberei überragt alles: sie ernährt", "Die Weberei ist mit Abstand das größte Gewerbe: sie ernährt",
     "Weaving towers above everything: it supports", "Weaving is by far the largest trade: it supports"),
    ("armenwesen-stiftungen-kapital-1828-1866", "überragt alle anderen", "ist mit Abstand die größte",
     "dwarfs all others", "is by far the largest"),
    ("bergbau-erzbergbau-zeitleiste-ober-unterland", "Zwei Konjunkturen (", "Zwei Phasen mit vielen Belegen (",
     "Two boom periods (", "Two periods with many records ("),
]
for i, dold, dnew, eold, enew in WORDING:
    patch(i, lambda d, dold=dold, dnew=dnew, eold=eold, enew=enew: sub_both(d, lambda s: s.replace(dold, dnew), lambda s: s.replace(eold, enew)))
