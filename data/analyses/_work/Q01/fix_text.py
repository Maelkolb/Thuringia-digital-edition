"""Q01: idempotent text normaliser for all analyses (including G7's orte-* files once G7 had finished).

Applies to every bilingual node {"de": ..., "en": ...} (title, summary, method, findings, caveats, chart
titles/captions, dataset/column labels, vega-lite titles and tooltip titles) and to `keywords`:

  English: American spelling (metre->meter, colour->color, per cent->percent, ...), "Thaler" -> "thalers",
           "Lower/Upper Land" -> Unterland/Oberland, "Dr X" -> "Dr. X", typographic apostrophe.
  German:  modern orthography in the edition's own words (Landestheil->Landesteil, Fuerstenthum->Fürstentum,
           Procent->Prozent, Thaler->Taler, Cubikfuß->Kubikfuß, Centner->Zentner, ...) -- but never inside
           quotations from the source (»...«, „...“) and never inside JavaScript expression strings
           (anything containing "datum.").
  Units:   `unit` strings (Thaler->Taler, Cubikfuß->Kubikfuß, Centner->Zentner), one square-mile glyph (□).

Usage: python fix_text.py [id-glob ...]   (default: all non-G7 analyses)
"""
import glob
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
AN = ROOT / "data" / "analyses"

# ---------------------------------------------------------------- English
BRIT = [
    (r"\bkilometres\b", "kilometers"), (r"\bkilometre\b", "kilometer"),
    (r"\bcentimetres\b", "centimeters"), (r"\bcentimetre\b", "centimeter"),
    (r"\bmillimetres\b", "millimeters"), (r"\bmillimetre\b", "millimeter"),
    (r"\bhectolitres\b", "hectoliters"), (r"\bhectolitre\b", "hectoliter"),
    (r"\bmetres\b", "meters"), (r"\bmetre\b", "meter"),
    (r"\blitres\b", "liters"), (r"\blitre\b", "liter"),
    (r"\bcolours\b", "colors"), (r"\bcolour\b", "color"), (r"\bcoloured\b", "colored"), (r"\bColour\b", "Color"),
    (r"\bcentres\b", "centers"), (r"\bcentre\b", "center"), (r"\bcentred\b", "centered"),
    (r"\bneighbouring\b", "neighboring"), (r"\bneighbours\b", "neighbors"), (r"\bneighbour\b", "neighbor"),
    (r"\bNeighbouring\b", "Neighboring"),
    (r"\blabourers\b", "laborers"), (r"\blabourer\b", "laborer"), (r"\blabour\b", "labor"),
    (r"\bfavourable\b", "favorable"), (r"\bhonour\b", "honor"),
    (r"\banalysed\b", "analyzed"), (r"\banalysing\b", "analyzing"),
    (r"\b(Brückner|he|it|she|[Tt]he analysis|which|who) analyses\b", r"\1 analyzes"),
    (r"\bstandardised\b", "standardized"), (r"\bstandardising\b", "standardizing"),
    (r"\bnormalised\b", "normalized"), (r"\bnormalising\b", "normalizing"),
    (r"\bdigitised\b", "digitized"), (r"\bsummarised\b", "summarized"),
    (r"\borganisation\b", "organization"), (r"\burbanisation\b", "urbanization"),
    (r"\bmineralised\b", "mineralized"), (r"\bmineralisation\b", "mineralization"),
    (r"\bgrey\b", "gray"), (r"\blicence\b", "license"), (r"\bjudgement\b", "judgment"),
    (r"\blabelled\b", "labeled"), (r"\btonnes\b", "metric tons"), (r"\btonne\b", "metric ton"),
    (r"\bsulphate\b", "sulfate"), (r"\bper cent\b", "percent"), (r"\bPer cent\b", "Percent"),
    (r"\bLower Land\b", "Unterland"), (r"\bUpper Land\b", "Oberland"),
    (r"\bLandrath\b", "Landrat"),
    (r"\bDr (?=[A-ZÄÖÜ])", "Dr. "),
    (r"\bstoreys\b", "stories"), (r"\bstorey\b", "story"),
    (r"\bmodernised\b", "modernized"), (r"\bitemised\b", "itemized"), (r"\bitemises\b", "itemizes"),
    (r"\bamortisation\b", "amortization"), (r"\blevelling\b", "leveling"), (r"\bmeagre\b", "meager"),
    (r"\bpractise\b", "practice"), (r"\bpractises\b", "practices"),
    (r"\b(north|south)-(east|west)\b", r"\1\2"), (r"\b(North|South)-(east|west)\b", r"\1\2"),
    (r"\btowards\b", "toward"), (r"\bTowards\b", "Toward"),
    (r"(?<=\d) %", "%"),
]
BRIT = [(re.compile(a), b) for a, b in BRIT]


def fix_thaler(s):
    # "1 Thaler" -> "1 thaler"; other "Thaler" (German plural-less) -> "thalers"
    s = re.sub(r"\bThalers\b", "thalers", s)
    s = re.sub(r"(?<=\b1 )Thaler\b", "thaler", s)
    s = re.sub(r"\bThaler\b", "thalers", s)
    # sentence/segment start or whole string: capitalise again
    s = re.sub(r"^thalers\b", "Thalers", s)
    s = re.sub(r"(?<=[.;:] )thalers\b", "Thalers", s)
    return s


def fix_en(s):
    if "datum." in s or "==" in s:
        return s
    parts = re.split(r"(“[^”]*”)", s)  # keep quotations from the source untouched (only spelling words below)
    out = []
    for p in parts:
        if p.startswith("“"):
            out.append(p)
            continue
        for rx, rep in BRIT:
            p = rx.sub(rep, p)
        p = fix_thaler(p)
        out.append(p)
    s = "".join(out)
    # british spelling inside quotations is rare; still unify the few unit words there
    s = re.sub(r"\bmetres\b", "meters", s)
    s = re.sub(r"(?<=\w)'(?=\w)", "’", s)
    s = re.sub(r"(?<=s)'(?=\s)", "’", s)
    return s


# ---------------------------------------------------------------- German
DE = [
    ("Landestheil", "Landesteil"), ("Landtheil", "Landteil"),
    ("Fürstenthum", "Fürstentum"),
    ("Procent", "Prozent"), ("procent", "prozent"),
    ("Dezimal-Thaler", "Dezimal-Taler"), ("Dezimal-Thalern", "Dezimal-Talern"),
    ("Todtgeb", "Totgeb"), ("todtgeb", "totgeb"),
    ("Cubikfuß", "Kubikfuß"), ("Cubikfuss", "Kubikfuß"),
    ("Zollcentner", "Zollzentner"), ("Centner", "Zentner"), ("centner", "zentner"),
    ("Landwirthschaft", "Landwirtschaft"), ("landwirthschaft", "landwirtschaft"),
    ("Forstwirthschaft", "Forstwirtschaft"), ("forstwirthschaft", "forstwirtschaft"),
    ("Fruchtvertheilung", "Fruchtverteilung"), ("Vertheilung", "Verteilung"), ("vertheilung", "verteilung"),
    ("Arbeitsthiere", "Arbeitstiere"), ("Arbeitsthieren", "Arbeitstieren"), ("Maulthiere", "Maultiere"),
    ("Verheirathete", "Verheiratete"), ("verheirathete", "verheiratete"),
    ("Landrathsbezirk", "Landratsbezirk"), ("Landrathsamt", "Landratsamt"), ("Landraths ", "Landrats "),
    ("theilweise", "teilweise"),
    ("Steuerwerth", "Steuerwert"), ("Roggenwerth", "Roggenwert"),
    ("Hauptcontingent", "Hauptkontingent"), ("Reichscontingent", "Reichskontingent"),
    ("Reservecontingent", "Reservekontingent"), ("Gesamtcontingent", "Gesamtkontingent"),
    ("Diaconaten", "Diakonate"), ("Diaconen", "Diakonen"),
    ("Colonial-", "Kolonial-"), ("Victualien", "Viktualien"),
    ("Leichencommun", "Leichenkommun"), ("Sterbefiscus", "Sterbefiskus"),
]
DE_RX = [
    (re.compile(r"\bThalern\b"), "Talern"), (re.compile(r"\bThaler\b"), "Taler"), (re.compile(r"\bThalers\b"), "Talers"),
    (re.compile(r"(?<![A-Za-zäöüß])Producirende"), "Produzierende"),
    (re.compile(r"\btodt\b"), "tot"),
]
PROTECT_DE = re.compile(r"(»[^«]*«|„[^“]*“)")


def fix_de(s):
    if "datum." in s or "==" in s:
        return s
    parts = PROTECT_DE.split(s)
    out = []
    for p in parts:
        if PROTECT_DE.fullmatch(p):
            out.append(p)
            continue
        for a, b in DE:
            p = p.replace(a, b)
        for rx, b in DE_RX:
            p = rx.sub(b, p)
        out.append(p)
    return "".join(out)


UNIT_MAP = {
    "Thaler": "Taler", "Thaler/ha": "Taler/ha", "Thaler je Normalklafter": "Taler je Normalklafter",
    "Sgr. je Cubikfuß": "Sgr. je Kubikfuß", "Cubikfuß je Jahr": "Kubikfuß je Jahr",
    "Centner": "Zentner", "Centner/□Meile": "Zentner/□Meile", "Zollcentner": "Zollzentner",
}


PROTECT_KEYS = {"domain", "sort", "range", "values"}  # strings here must equal the data values / expression literals


def walk(node, protected=False):
    """Return the transformed node."""
    if isinstance(node, list):
        return [walk(x, protected) for x in node]
    if isinstance(node, dict):
        keys = set(node)
        if keys == {"de", "en"} and isinstance(node["de"], str) and isinstance(node["en"], str):
            if protected:
                return node
            return {"de": fix_de(node["de"]), "en": fix_en(node["en"])}
        out = {}
        for k, v in node.items():
            if k == "rows":
                out[k] = v
            elif k == "unit" and isinstance(v, str):
                out[k] = UNIT_MAP.get(v, v)
            elif k == "keywords" and isinstance(v, dict) and set(v) == {"de", "en"}:
                out[k] = {"de": [fix_de(x) for x in v["de"]], "en": [fix_en(x) for x in v["en"]]}
            else:
                out[k] = walk(v, protected or k in PROTECT_KEYS)
        return out
    return node


LABEL_RX = re.compile(r"^Fürstenthum(?=$|[ ,(\-])")


def fix_labels(d):
    """Region label "Fürstenthum" (whole principality) -> "Fürstentum" in short data cells and, consistently,
    in every string of the chart specs (also inside JavaScript expressions that compare against it)."""
    for ds in d.get("datasets", []):
        for r in ds["rows"]:
            for j, v in enumerate(r):
                if isinstance(v, str) and len(v) <= 45 and LABEL_RX.match(v):
                    r[j] = v.replace("Fürstenthum", "Fürstentum", 1)

    def walk(n):
        if isinstance(n, list):
            return [walk(x) for x in n]
        if isinstance(n, dict):
            return {k: walk(v) for k, v in n.items()}
        if isinstance(n, str) and "Fürstenthum" in n and (len(n) <= 45 or "datum." in n or "==" in n):
            return n.replace("Fürstenthum", "Fürstentum")
        return n
    def walk2(n):
        if isinstance(n, list):
            return [walk2(x) for x in n]
        if isinstance(n, dict):
            return {k: ("Taler" if k == "title" and v == "Thaler" else walk2(v)) for k, v in n.items()}
        if isinstance(n, str) and "Fürstenthum" in n and (len(n) <= 45 or "datum." in n or "==" in n):
            return n.replace("Fürstenthum", "Fürstentum")
        return n
    for ch in d.get("charts", []):
        ch["vegalite"] = walk2(ch["vegalite"])
    return d


def process(path):
    d = json.load(open(path, encoding="utf-8"))
    d2 = fix_labels(walk(d))
    txt = json.dumps(d2, ensure_ascii=False, indent=1).replace("☐", "□")
    old = Path(path).read_text(encoding="utf-8")
    if txt != old:
        Path(path).write_text(txt, encoding="utf-8")
        return True
    return False


if __name__ == "__main__":
    pats = sys.argv[1:] or ["*"]
    changed = []
    for pat in pats:
        for f in sorted(glob.glob(str(AN / f"{pat}.json"))):
            name = Path(f).stem
            if process(f):
                changed.append(name)
    print(len(changed), "files changed")
    for c in changed:
        print("  ", c)
