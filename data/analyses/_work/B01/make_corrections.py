"""B01 analysis 3: Zusätze und Berichtigungen (pp. 830-834) as a dataset of the author's corrections.

Each printed correction (one "lies ... statt ..." clause, one addition, one update) becomes one row. The printed text is
taken from the canonical page JSON by anchoring on the first words of each clause; target page and line are parsed from
the printed text. Kind/detail/gloss are editorial.
"""
import re
import sys
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
from common import ROOT, block, load_page, write_analysis

# kind: correction | deletion | addition | update ;  detail: spelling | word | number | name | statement | omission | supplement | event
# (page, block, item|None, anchor|None, kind, detail, gloss_en[, page_override])
R = [
    ("830", "b2", None, "S. 61.", "addition", "omission", "Word missing after 'zeigte sich': 1864 (climate, p. 61)."),
    ("830", "b3", None, "S. 66.", "correction", "number", "Column 3 of the Gera table: seven figures and 'Mai Max.' replaced by 'Juli Max.'."),
    ("830", "b4", "i1", None, "correction", "number", "128.6 for 148.4 and 22.5 for 22.3."),
    ("830", "b4", "i2", None, "correction", "word", "'der Regentage' for 'des Regens'."),
    ("830", "b4", "i3", None, "correction", "word", "'Juli' for 'Mai'."),
    ("830", "b4", "i4", None, "correction", "number", "Column 11, two lines from the bottom: 1 for 2 and 5 for 6."),
    ("830", "b5", "i1", None, "correction", "name", "Observer is Dr. Rob. Schmidt in Gera, not Rob. Schmidt in Hohenleuben."),
    ("830", "b5", "i2", None, "correction", "name", "'Dr. Rob. Schmidt' for 'Rud. Schmidt'."),
    ("830", "b6", None, "S. 69.", "correction", "number", "Column 5 of the table: 319.25 for 319.28."),
    ("830", "b6", None, "in der 6. Spalte", "correction", "number", "Column 6 of the table: 534.50 for 554.50."),
    ("830", "b6", None, "in der 9. Spalte", "correction", "number", "Column 9 of the table: six figures corrected."),
    ("830", "b7", "i1", None, "deletion", "statement", "Delete Laserpitium pruthenicum from the plant list."),
    ("830", "b7", "i2", None, "correction", "spelling", "Plant name spelled Pulicaria."),
    ("830", "b7", "i3", None, "correction", "spelling", "Botanist's name spelled Schlechtendal."),
    ("830", "b8", None, "S. 73.", "deletion", "statement", "Delete Neottia nidus-avis and Gentiana ciliata from the plants peculiar to the lowland: they also occur in the upland."),
    ("830", "b8", None, "dagegen ist", "addition", "supplement", "Add Salvia verticillata as peculiar to the lowland."),
    ("830", "b9", None, "Z. 6 v. u.", "deletion", "statement", "Remove the asterisk at Nuphar luteum: it is often found in the upland."),
    ("830", "b9", None, "Dem Oberlande", "addition", "supplement", "Libanotis montana and Phyteum orbiculare also belong to the upland."),
    ("830", "b10", None, None, "correction", "spelling", "'villosum' for 'vilosum'."),
    ("830", "b11", None, None, "addition", "supplement", "The Apocynum of the Küchengarten at Untermhaus is Apocynum venetum, per court gardener Papst."),
    ("830", "b12", None, None, "update", "event", "The tall solitary spruce was broken by a storm on 7 Dec. 1868."),
    ("830", "b13", None, "S. 79.", "correction", "spelling", "'Cladonienflechten' for 'Clidoniensflechten'."),
    ("830", "b13", None, "Der Straußenfarn", "deletion", "statement", "Delete ostrich fern and Laserpitium pruthenicum from the characteristic plants of the upland."),
    ("830", "b14", "i1", "S. 80.", "correction", "word", "'allenthalben' for 'nur stellenweise'."),
    ("830", "b14", "i1", "Nach Calla", "addition", "supplement", "Add 'very rare' (Plothen pond district) after Calla palustris."),
    ("830", "b14", "i2", None, "correction", "spelling", "'canopsea' for 'canopea'."),
    ("830", "b14", "i3", None, "addition", "supplement", "The vegetable called Otterzunge is Rumex in several species."),
    ("830", "b14", "i4", None, "addition", "supplement", "The worst field weed of the upland is the bramble (Ackerbrombeere)."),
    ("830", "b14", "i5", None, "addition", "supplement", "Sedum villosum grows only on wet, slightly acid meadows."),
    ("831", "b1", None, "S. 84.", "correction", "word", "'Buntspechte' (spotted woodpeckers) for 'Grünspechte'."),
    ("831", "b1", None, '" 19 u. 21', "correction", "spelling", "'Steinschmätzer' for 'Steinschmetter'."),
    ("831", "b1", None, '" 23 v. o.', "update", "event", "The great grey shrike, once thought extinct, was proved native again in summer 1869."),
    ("831", "b2", None, "S. 85.", "addition", "supplement", "Main reason for the nightingale's absence in the lowland: loss of brushwood in the side valleys of the Elster."),
    ("831", "b2", None, "Z. 14 v. o.", "update", "event", "Magpies have increased strongly again in the last two years."),
    ("831", "b2", None, "Der mit Z. 7 v. u.", "addition", "supplement", "Comment on the reliability of the bird list taken from the society's third annual report."),
    ("831", "b3", None, "S. 86.", "correction", "spelling", "'Schellente' for 'Schallente'."),
    ("831", "b3", None, "S. 87.", "correction", "spelling", "'Bandschmerle' for 'Brandschmerle'."),
    ("831", "b4", None, None, "addition", "supplement", "Cockchafer flight years: four-year cycle; orchard damage from 1828; 1829 bounty on butterflies."),
    ("831", "b5", None, "S. 168.", "correction", "word", "'eine' for 'zwei'."),
    ("831", "b5", None, "S. 192.", "addition", "supplement", "The Twelve Nights began originally on 21 December, later (documented 1321) on 25 December."),
    ("831", "b5", None, "S. 219.", "correction", "word", "Table heading: 'Steuerwerth in Steuereinheiten à 10 Thlr.' for 'Steuerwerth — Thaler' (pp. 219, 221, 223)."),
    ("831", "b5", None, "S. 230.", "correction", "number", "26 for 29."),
    ("831", "b5", None, "S. 251.", "update", "event", "Salt retail outlets abolished from 1868 after the federal law of 12 Oct. 1867."),
    ("831", "b5", None, "S. 272.", "addition", "omission", "Insert 'und die Mannschaft' after 'Officiere'."),
    ("831", "b5", None, "S. 277. Z. 14", "update", "event", "The tax receiving office (Steuerreceptur) has been abolished."),
    ("831", "b5", None, '" Z. 13 v. u.', "correction", "spelling", "'zuverzinsenden' for 'zu verzinsenden'."),
    ("831", "b6", None, None, "update", "event", "Conversion of the former weights and measures: ministerial notice of 20 March 1869 (the table on pp. 831-832)."),
    ("833", "b1", None, None, "update", "event", "The princely house's common vote in the Oberappellationsgericht Jena; joint military affairs ended in 1868."),
    ("833", "b2", None, None, "update", "event", "Church-council ordinance of 1866 widens the powers of the local church councils."),
    ("833", "b3", None, None, "correction", "spelling", "'Pöritzsch' for 'Pöritsch'."),
    ("833", "b5", "i1", None, "update", "event", "Foundation of the merchant Hermann Ferber for Gera (1869, 10,000 Thlr.).", "309"),
    ("833", "b5", "i2", None, "addition", "supplement", "Foundation of the merchant Heinrich Bruhm for Gera (1000 + 500 + 500 Thlr.).", "309"),
    ("833", "b6", None, None, "correction", "statement", "Seventh point: 'a son and two grandsons'; Heinrich of Weida already called himself 'by the grace of God'."),
    ("833", "b7", None, None, "correction", "number", "c. 1279 for c. 1274."),
    ("833", "b8", None, None, "correction", "number", "1420 for 1520."),
    ("833", "b9", None, None, "addition", "supplement", "Since 1276 part of the upland was called Ruthenenland: support for the explanation of the name Reuß."),
    ("833", "b10", None, None, "correction", "number", "Heinrich 'LXII.' for 'XLII.'."),
    ("833", "b11", None, None, "correction", "statement", "Death of the prince: Prussian captain à la suite, died 15 Aug. 1866 at Bad Liebenstein, instead of a Prussian major's death in battle."),
    ("833", "b12", None, None, "correction", "number", "Death year 1748 for 1686."),
    ("833", "b13", None, None, "correction", "number", "Death year 1857 for '18..'."),
    ("833", "b14", None, None, "update", "event", "Boundary treaty with Saxe-Altenburg of 30 May / 5 Aug. 1868 settles disputed border plots."),
    ("833", "b15", None, None, "correction", "statement", "The Marstall on the Osterstein is not the work of Prince Heinrich LXXII."),
    ("833", "b16", None, None, "update", "event", "The two hospitals have been united since 1868."),
    ("833", "b17", None, None, "addition", "supplement", "Two further scholars born in Gera: H. B. Roth and H. J. C. Weißenborn."),
    ("833", "b18", None, None, "update", "event", "The new stone bridge over the Elster was built by the municipalities with district aid."),
    ("833", "b19", None, None, "correction", "spelling", "'ganz' for the misprint 'gauz'."),
    ("833", "b20", None, None, "correction", "spelling", "'besondere' for the misprint 'besondeer'."),
    ("833", "b21", None, "S. 503.", "addition", "supplement", "The family v. Haugk was among the last owners of the manor."),
    ("833", "b21", None, '" Z. 5', "correction", "statement", "Bells: largest and middle cast 1617, smallest 1455 (inscription), instead of three bells cast in 1617."),
    ("834", "b1", "i1", None, "correction", "word", "'noch' for 'nach'."),
    ("834", "b1", "i2", None, "correction", "word", "'An das vormalige Dorf' for 'An das Dorf'."),
    ("834", "b1", "i3", None, "correction", "number", "40 for 400."),
    ("834", "b1", "i4", None, "correction", "spelling", "'mehrerer' for 'mehrere'."),
    ("834", "b1", "i5", None, "correction", "word", "'geschlagen' for 'zerschlagen'."),
    ("834", "b1", "i6", None, "addition", "supplement", "A writer from Schleiz: Adam Heinr. Meisner (1711-1782)."),
    ("834", "b1", "i7", None, "correction", "word", "'13 Einw.' for '13'."),
    ("834", "b1", "i8", None, "addition", "supplement", "The spinning mill at Blankenstein is called Rosenthal."),
    ("834", "b1", "i9", None, "addition", "supplement", "Juchhöh is often also called Dornbusch; one of the Dornhäuser is the Quarkschenke."),
]
# facsimile-confirmed corrections of the transcription (page, block, item) -> (wrong, right)
TEXT_FIXES = {
    ("831", "b5", None): [("zuversindenden statt zu verzindenden", "zuverzinsenden statt zu verzinsenden")],
    ("833", "b19", None): [("ganz statt ganz", "ganz statt gauz")],
    ("833", "b20", None): [("besondere statt besonderer", "besondere statt besondeer")],
}
OLDNEW = {  # (page, block, anchor) -> (new, old) where the clause is not of the plain 'lies X statt Y' form
    ("830", "b6", "in der 6. Spalte"): ("534,50", "554,50"),
    ("831", "b5", "S. 219."): ("Steuerwerth in Steuereinheiten à 10 Thlr.", "Steuerwerth — Thaler"),
}
CHAPTERS = {
    "t1-1": ("Natur des Landes", "Nature of the land"), "t1-2": ("Das Volk", "The people"),
    "t1-3": ("Volksbetriebsamkeit", "Economic activity"), "t1-4": ("Der Staat", "The state"), "t1-5": ("Geschichte", "History"),
    "t2": ("Ortskunde: Einleitung", "Topography: introduction"), "t2-1": ("Ortskunde Gera", "Topography: Gera"),
    "t2-2": ("Ortskunde Schleiz", "Topography: Schleiz"), "t2-3": ("Ortskunde Lobenstein-Ebersdorf", "Topography: Lobenstein-Ebersdorf"),
}
CHAPTER_ORDER = list(CHAPTERS)
KINDS = {"correction": ("Berichtigung", "Correction"), "deletion": ("Streichung", "Deletion"),
         "addition": ("Zusatz", "Addition"), "update": ("Aktualisierung", "Update")}
KIND_ORDER = list(KINDS)


def raw_text(page, bid, item):
    b = block(page, bid)
    if item:
        for i, it in enumerate(b["items"], start=1):
            if f"i{i}" == item:
                return it["text"]
        raise KeyError((page, bid, item))
    return b["text"]


def slice_for(idx):
    page, bid, item, anchor = R[idx][:4]
    txt = raw_text(page, bid, item)
    # clauses of the same block/item: bounded by the next anchored record of the same source
    same = [j for j, r in enumerate(R) if r[:3] == (page, bid, item)]
    pos = same.index(idx)
    start = txt.index(anchor) if anchor else 0
    if pos + 1 < len(same):
        nxt = R[same[pos + 1]][3]
        end = txt.index(nxt, start + 1)
    else:
        end = len(txt)
    s = txt[start:end].replace("\n", " ").strip()
    if anchor is None and pos == 0:
        s = txt.replace("\n", " ").strip()
    return s


def target_pages(s, prev_page):
    m = re.match(r'^S\. (\d+)(?:\.\s*(\d+)\.\s*(\d+)\.|\s+und\s+(\d+))?', s)
    if m:
        pages = [m.group(1)] + [g for g in m.groups()[1:] if g]
        return pages
    return [prev_page]


def line_ref(s, prev_dir):
    """Return (numbers, direction) from the clause; dittos inherit the direction of the previous clause."""
    t = re.sub(r"^S\. \d+(?:\.\s*\d+\.\s*\d+\.|\s+und\s+\d+)?\.?\s*", "", s)
    t = re.sub(r'^"\s*', "", t)
    m = re.match(r"^(?:Z\.\s*)?(\d+)(?:\s+(?:und|u\.)\s+(\d+))?\s+(?:v\. ([ou])\.|\" \")", t)
    if m:
        d = {"o": "top", "u": "bottom", None: prev_dir}[m.group(3)]
        return [m.group(1)] + ([m.group(2)] if m.group(2) else []), d
    m = re.search(r"Z\.\s*(\d+)(?:\s+(?:und|u\.)\s+(\d+))?\s+v\. ([ou])\.", t)
    if m:
        return [m.group(1)] + ([m.group(2)] if m.group(2) else []), {"o": "top", "u": "bottom"}[m.group(3)]
    m = re.search(r"Zur Z\. (\d+)", t)
    if m:
        return [m.group(1)], "top"
    return None, prev_dir


def build():
    rows = []
    prev_page, prev_dir = None, None
    for idx, rec in enumerate(R):
        page, bid, item, anchor, kind, detail, gloss = rec[:7]
        override = rec[7] if len(rec) > 7 else None
        s = slice_for(idx)
        for wrong, right in TEXT_FIXES.get((page, bid, item), []):
            s = s.replace(wrong, right)
        pages = [override] if override else target_pages(s, prev_page)
        # the very first clause of an item written with the S. anchor may include the page
        nums, direction = line_ref(s, prev_dir)
        if not nums and item and rows and (rows[-1]["cpage"], rows[-1]["block"], rows[-1]["item"]) == (page, bid, item):
            nums, direction = rows[-1]["line_nums"], rows[-1]["direction"]
        if re.match(r"^S\. \d+", s) or override:
            prev_dir = None
        if direction:
            prev_dir = direction
        prev_page = pages[0]
        # old/new text
        old = new = ""
        pairs = len(re.findall(r"\bstatt\b", s))
        m = re.search(r"\blies:?\s*(.+?)\s+statt:?\s*(.+)$", s)
        if m and kind in ("correction", "update") and pairs == 1:
            new, old = m.group(1).strip(), m.group(2).strip().rstrip(";").strip()
        if (page, bid, anchor) in OLDNEW:
            new, old = OLDNEW[(page, bid, anchor)]
        new = new.rstrip(" —").strip()
        if old.endswith(".") and not old.endswith("..") and not re.search(r"\b(Max|Einw|Dr|Rob|Rud|Thlr)\.$", old):
            old = old[:-1]
        n_changes = pairs if pairs else 1
        if page == "830" and bid == "b3":
            n_changes = 1
        rows.append(dict(i=idx + 1, cpage=page, block=bid, item=item or "", pages=pages, line_nums=nums, direction=direction or "", kind=kind, detail=detail, gloss=gloss,
                         text=s, old=old, new=new, n_changes=n_changes))
    # sections of the target pages
    for r in rows:
        p = load_page(r["pages"][0])
        path = p["section_path"]
        r["section"] = path[-1]
        r["chapter"] = path[1] if len(path) > 1 and path[1] in CHAPTERS else path[-1] if path[-1] in CHAPTERS else path[0]
        if r["chapter"] not in CHAPTERS:
            raise KeyError((r["pages"], path))
        # does the replaced text occur on the target page(s)?
        r["old_found"] = ""
        if r["old"] and (len(r["old"]) >= 5 or (r["old"].isdigit() and len(r["old"]) == 4)):
            hay = " ".join(load_page(pp) and (ROOT / "data/text/pages" / f"{pp}.txt").read_text(encoding="utf-8") for pp in r["pages"])
            hay = re.sub(r"\s+", " ", hay)
            r["old_found"] = "yes" if r["old"].rstrip(".") in hay else "no"
    return rows


def line_label(r):
    if not r["line_nums"]:
        return ""
    d = {"top": "v. o.", "bottom": "v. u.", "": ""}[r["direction"]]
    return ("Z. " + " u. ".join(r["line_nums"]) + (" " + d if d else "")).strip()


rows = build()
N = len(rows)
by_kind = Counter(r["kind"] for r in rows)
by_chapter = Counter(r["chapter"] for r in rows)
by_detail = Counter((r["kind"], r["detail"]) for r in rows)
tp = [int(r["pages"][0]) for r in rows]
nature = [r for r in rows if r["chapter"] == "t1-1"]
nat_pages = (min(int(r["pages"][0]) for r in nature), max(int(r["pages"][0]) for r in nature))
upd = [r for r in rows if r["kind"] == "update"]
years = sorted({int(y) for r in upd for y in re.findall(r"\b(18[4-7]\d)\b", r["text"])})
num_fix = [r for r in rows if r["kind"] == "correction" and r["detail"] == "number"]
spell = [r for r in rows if r["detail"] == "spelling"]
found = Counter(r["old_found"] for r in rows if r["old_found"])
print(N, by_kind, by_chapter, "nature", nat_pages, "years", years, "found", found)
for r in rows:
    if r["old"] and r["old_found"] == "no":
        print("  not found on page:", r["pages"], "|", r["old"], "|", r["text"][:80])
print([(r["cpage"], r["block"], r["item"], r["pages"], line_label(r), r["kind"]) for r in rows][:12])

pct = lambda a, b: 100 * a / b
dec = lambda x: f"{x:.1f}".replace(".", ",")
fmt1 = lambda x: f"{x:.1f}"
part1 = sum(v for k, v in by_chapter.items() if k.startswith("t1"))
part2 = N - part1
n_pages = len({p for r in rows for p in r["pages"]})
n_multi_page = sum(1 for r in rows if len(r["pages"]) > 1)
nat_share = pct(len(nature), N)
nat_span = nat_pages[1] - nat_pages[0] + 1
best_chapter = max(by_chapter, key=by_chapter.get)

# ------------------------------------------------------------------ dataset
cols = [
    ("corr_id", "Nr.", "No.", "string", None, True, "laufende Nummer der Berichtigung in Brückners Reihenfolge (editorisch)"),
    ("correction_page", "Seite der Berichtigung", "Page of the correction", "string", None, False, None),
    ("block", "Block", "Block", "string", None, False, None),
    ("item", "Listenpunkt", "List item", "string", None, False, "nur bei Listenblöcken"),
    ("target_page", "Bezugsseite", "Target page", "integer", None, False, "gedruckte Seite des Buchs, auf die sich die Berichtigung bezieht (erste, wenn mehrere)"),
    ("target_pages", "Bezugsseiten", "Target pages", "string", None, True, "alle genannten Seiten, durch Semikolon getrennt"),
    ("line_ref", "Zeile", "Line", "string", None, True, "Zeilenangabe, Wiederholungszeichen aufgelöst; v. o. = von oben, v. u. = von unten"),
    ("line_first", "Zeile (erste Zahl)", "Line (first number)", "integer", None, False, "gedruckte Zeilennummer"),
    ("line_from", "Zählung ab", "Counted from", "string", None, True, "top | bottom"),
    ("kind", "Art", "Kind", "string", None, True, "correction (lies … statt …) | deletion (zu streichen) | addition (Zusatz, Einfügung) | update (Ereignis nach Abfassung)"),
    ("detail", "Näheres", "Detail", "string", None, True, "spelling | word | number | name | statement | omission | supplement | event"),
    ("section", "Abschnitt", "Section", "string", None, True, "innerster Abschnitt der Bezugsseite"),
    ("chapter", "Kapitel", "Chapter", "string", None, True, "Kapitel der Bezugsseite (t1-1 … t2-3, t2 = Einleitung Teil II)"),
    ("text_printed", "Wortlaut (gedruckt)", "Wording (as printed)", "string", None, False, "Text der Berichtigung, wörtlich; drei Lesefehler des Transkripts nach dem Faksimile korrigiert"),
    ("corrected_text", "Zu setzen", "To read", "string", None, False, "Text nach »lies«, nur bei einfachen Berichtigungen"),
    ("replaced_text", "Statt", "Instead of", "string", None, False, "Text nach »statt«"),
    ("replaced_found_on_page", "Ersetzter Text auf der Bezugsseite", "Replaced text found on target page", "string", None, True, "yes/no: Suche im Text der Bezugsseite (nur wo »statt« einen einfachen Text von mindestens fünf Zeichen oder eine vierstellige Zahl nennt)"),
    ("n_changes", "Anzahl Änderungen", "Number of changes", "integer", None, True, "Anzahl der »statt«-Paare im Wortlaut (1 bei Zusätzen und Streichungen)"),
    ("gloss_en", "Kurzbeschreibung (en)", "Short description (en)", "string", None, True, "englische Kurzfassung (editorisch)"),
]
D = lambda r: ";".join(r["pages"])
data_rows = []
for r in rows:
    data_rows.append([f"K{r['i']:03d}", r["cpage"], r["block"], r["item"], int(r["pages"][0]), D(r), line_label(r),
                      int(r["line_nums"][0]) if r["line_nums"] else None, r["direction"], r["kind"], r["detail"], r["section"], r["chapter"],
                      r["text"], r["new"], r["old"], r["old_found"], r["n_changes"], r["gloss"]])
columns = []
for n, lde, len_, t, u, der, note in cols:
    c = {"name": n, "label": {"de": lde, "en": len_}, "type": t, "unit": u}
    if der:
        c["derived"] = True
    if note:
        c["note"] = note
    columns.append(c)

# chart helper strings
def lookup(mapping, idx):
    return "{" + ", ".join(f"'{k}': '{v[idx]}'" for k, v in mapping.items()) + "}"

CH_CALC = {"de": lookup(CHAPTERS, 0) + "[datum.chapter]", "en": lookup(CHAPTERS, 1) + "[datum.chapter]"}
KIND_CALC = {"de": lookup(KINDS, 0) + "[datum.kind]", "en": lookup(KINDS, 1) + "[datum.kind]"}
KIND_DOMAIN = [{"de": KINDS[k][0], "en": KINDS[k][1]} for k in KIND_ORDER]
CH_DOMAIN = [{"de": CHAPTERS[k][0], "en": CHAPTERS[k][1]} for k in CHAPTER_ORDER]
T_KIND = {"de": "Art", "en": "Kind"}
T_CH = {"de": "Kapitel", "en": "Chapter"}
tip = [{"field": "corr_id", "title": {"de": "Nr.", "en": "No."}}, {"field": "target_page", "title": {"de": "Bezugsseite", "en": "Target page"}},
       {"field": "line_ref", "title": {"de": "Zeile", "en": "Line"}}, {"field": "kind_label", "title": T_KIND},
       {"field": "text_printed", "title": {"de": "Wortlaut", "en": "Wording"}}]

c1 = {
    "height": 300,
    "transform": [{"calculate": CH_CALC, "as": "chapter_label"}, {"calculate": KIND_CALC, "as": "kind_label"},
                  {"calculate": "indexof(" + str(CHAPTER_ORDER) + ", datum.chapter)", "as": "chapter_no"}],
    "mark": "bar",
    "encoding": {
        "y": {"field": "chapter_label", "type": "nominal", "sort": {"field": "chapter_no", "op": "min"}, "title": None, "axis": {"labelLimit": 300}},
        "x": {"aggregate": "count", "type": "quantitative", "title": {"de": "Berichtigungen", "en": "Corrections"}},
        "color": {"field": "kind_label", "type": "nominal", "scale": {"domain": KIND_DOMAIN}, "title": T_KIND, "legend": {"columns": 2}},
        "tooltip": [{"field": "chapter_label", "title": T_CH}, {"field": "kind_label", "title": T_KIND}, {"aggregate": "count", "title": {"de": "Anzahl", "en": "Number"}}],
    },
}
c2 = {
    "height": 240,
    "transform": [{"calculate": KIND_CALC, "as": "kind_label"}],
    "mark": "bar",
    "encoding": {
        "x": {"field": "target_page", "type": "quantitative", "bin": {"step": 25, "extent": [0, 850]}, "title": {"de": "Seite des Buchs (Klassen zu 25 Seiten)", "en": "Page of the book (bins of 25 pages)"},
              "axis": {"format": "d", "tickMinStep": 25}},
        "y": {"aggregate": "count", "type": "quantitative", "title": {"de": "Berichtigungen", "en": "Corrections"}},
        "color": {"field": "kind_label", "type": "nominal", "scale": {"domain": KIND_DOMAIN}, "title": T_KIND},
        "tooltip": [{"field": "target_page", "bin": {"step": 25, "extent": [0, 850]}, "title": {"de": "Seiten", "en": "Pages"}},
                    {"field": "kind_label", "title": T_KIND}, {"aggregate": "count", "title": {"de": "Anzahl", "en": "Number"}}],
    },
}
DETAIL_LABEL = {"spelling": ("Schreibung", "spelling"), "word": ("Wort", "word"), "number": ("Zahl, Datum", "number, date"), "name": ("Name", "name"),
                "statement": ("Aussage", "statement"), "omission": ("Auslassung", "omission"), "supplement": ("Ergänzung", "supplement"), "event": ("neues Ereignis", "new event")}
DETAIL_ORDER = ["spelling", "word", "number", "name", "statement", "omission", "supplement", "event"]
c3 = {
    "height": 260,
    "transform": [{"calculate": lookup(DETAIL_LABEL, 0) + "[datum.detail]", "as": "detail_de"}, {"calculate": lookup(DETAIL_LABEL, 1) + "[datum.detail]", "as": "detail_en"},
                  {"calculate": KIND_CALC, "as": "kind_label"},
                  {"calculate": "indexof(" + str(DETAIL_ORDER) + ", datum.detail)", "as": "detail_no"}],
    "mark": "bar",
    "encoding": {
        "y": {"field": "detail", "type": "nominal", "sort": DETAIL_ORDER, "title": None,
              "axis": {"labelExpr": {"de": "{" + ", ".join(f"'{k}': '{v[0]}'" for k, v in DETAIL_LABEL.items()) + "}[datum.label]",
                                     "en": "{" + ", ".join(f"'{k}': '{v[1]}'" for k, v in DETAIL_LABEL.items()) + "}[datum.label]"}}},
        "x": {"aggregate": "count", "type": "quantitative", "title": {"de": "Berichtigungen", "en": "Corrections"}},
        "color": {"field": "kind_label", "type": "nominal", "scale": {"domain": KIND_DOMAIN}, "title": T_KIND},
        "tooltip": [{"field": "detail", "title": {"de": "Näheres", "en": "Detail"}}, {"field": "kind_label", "title": T_KIND}, {"aggregate": "count", "title": {"de": "Anzahl", "en": "Number"}}],
    },
}

blocks = [("830", "b2"), ("830", "b3"), ("830", "b4"), ("830", "b5"), ("830", "b6"), ("830", "b7"), ("830", "b8"), ("830", "b9"), ("830", "b10"), ("830", "b11"),
          ("830", "b12"), ("830", "b13"), ("830", "b14"), ("831", "b1"), ("831", "b2"), ("831", "b3"), ("831", "b4"), ("831", "b5"), ("831", "b6")] + \
         [("833", f"b{i}") for i in range(1, 22)] + [("834", "b1")]
refs = [{"page": p, "block": b} for p, b in blocks]

title = {"de": "Zusätze und Berichtigungen des Verfassers (1870)", "en": "The author's addenda and corrigenda (1870)"}
summary = {
    "de": (f"Auf S. 830–834 stellt Brückner {N} Zusätze und Berichtigungen zum Buch zusammen, jeweils mit Seite und Zeile des Haupttextes. Der Datensatz ordnet sie nach Art "
           f"(Berichtigung, Streichung, Zusatz, Aktualisierung), Kapitel und Bezugsseite; die Edition kann damit jede Berichtigung mit ihrer Seite verknüpfen. Die Diagramme zeigen die Verteilung auf Kapitel, "
           f"Seitenbereiche und Arten."),
    "en": (f"On pp. 830–834 Brückner collects {N} addenda and corrigenda to the book, each with page and line of the main text. The dataset classifies them by kind "
           f"(correction, deletion, addition, update), chapter and target page, so that the edition can link every correction to its page. The charts show the distribution across chapters, "
           f"page ranges and kinds."),
}
method = {
    "de": (f"Quelle sind die Blöcke auf S. 830–834 (Überschrift »Zusätze und Berichtigungen«). Jede gedruckte Anweisung (»lies … statt …«, »zu streichen«, Zusatz, neue Tatsache) ist eine Zeile; "
           f"enthält ein Absatz mehrere Anweisungen, wurde er an den Satzgrenzen geteilt (z. B. S. 73: Streichung zweier Pflanzen und Ergänzung einer dritten). Bezugsseite und Zeilenangabe stammen aus dem gedruckten Text "
           f"(»Z. 20 v. o.« = Zeile 20 von oben; das Wiederholungszeichen „ steht für die vorher genannte Zählung). Art, Näheres und Kurzbeschreibung sind redaktionell: correction = Austausch von Text, deletion = Streichung, "
           f"addition = Ergänzung oder Einfügung, update = Mitteilung eines nach der Abfassung eingetretenen Ereignisses (1866–1869). Das Kapitel folgt aus der Gliederung des Buchs (Seite → Abschnitt). "
           f"Bei einfachen »lies … statt …«-Berichtigungen wurde geprüft, ob der ersetzte Text auf der Bezugsseite steht ({found.get('yes', 0)} von {sum(found.values())} gefunden). "
           f"Alle Seiten wurden am Faksimile gelesen; drei Lesefehler des Transkripts (S. 277, 489, 496) sind korrigiert."),
    "en": (f"The source is the blocks on pp. 830–834 (heading “Zusätze und Berichtigungen”). Each printed instruction (“lies … statt …”, “zu streichen”, addition, new fact) is one row; "
           f"where a paragraph contains several instructions it was split at the sentence boundaries (e.g. p. 73: deletion of two plants and addition of a third). Target page and line come from the printed text "
           f"(“Z. 20 v. o.” = line 20 from the top; the ditto mark „ stands for the counting direction named before). Kind, detail and short description are editorial: correction = replacement of text, deletion = removal, "
           f"addition = supplement or insertion, update = report of an event that occurred after the text was written (1866–1869). The chapter follows from the structure of the book (page → section). "
           f"For simple “lies … statt …” corrections it was checked whether the replaced text occurs on the target page ({found.get('yes', 0)} of {sum(found.values())} found). "
           f"All pages were read against the facsimile; three misreadings of the transcript (pp. 277, 489, 496) are corrected."),
}
findings = [
    {"de": (f"Brückner verzeichnet {N} Änderungen: {by_kind['correction']} Berichtigungen, {by_kind['deletion']} Streichungen, {by_kind['addition']} Zusätze und {by_kind['update']} Aktualisierungen. "
            f"{len(spell)} davon betreffen die Schreibung, {len(num_fix)} Zahlen oder Daten."),
     "en": (f"Brückner lists {N} changes: {by_kind['correction']} corrections, {by_kind['deletion']} deletions, {by_kind['addition']} additions and {by_kind['update']} updates. "
            f"{len(spell)} of them concern spelling, {len(num_fix)} numbers or dates.")},
    {"de": (f"Teil I (Allgemeines, S. 1–404) hat {part1} Einträge, Teil II (Ortskunde, S. 405–825) {part2}. Das Kapitel »Natur des Landes« allein vereint {len(nature)} ({dec(nat_share)} %), "
            f"auf den Seiten {nat_pages[0]}–{nat_pages[1]} ({nat_span} Seiten): Klima-Tabellen, Pflanzen- und Tiernamen."),
     "en": (f"Part I (general, pp. 1–404) has {part1} entries, Part II (topography, pp. 405–825) {part2}. The chapter “The nature of the land” alone accounts for {len(nature)} ({fmt1(nat_share)} %), "
            f"on pages {nat_pages[0]}–{nat_pages[1]} ({nat_span} pages): climate tables, plant and animal names.")},
    {"de": (f"{len(upd)} Einträge sind Aktualisierungen: sie berichten Ereignisse bis {max(years)} (u. a. Bundesgesetz über den Salzhandel 1867/68, Vereinigung der Hospitäler 1868, Grenzvertrag mit Sachsen-Altenburg 1868, "
            f"Umrechnung der Maße und Gewichte 1869) und stützen die Datierung des Drucks auf 1869/70."),
     "en": (f"{len(upd)} entries are updates: they report events up to {max(years)} (among others the federal law on salt trade 1867/68, the union of the hospitals 1868, the boundary treaty with Saxe-Altenburg 1868, "
            f"the conversion of weights and measures 1869) and support dating the print to 1869/70.")},
    {"de": (f"Die {n_pages} verschiedenen Bezugsseiten sind über das ganze Buch verteilt; {n_multi_page} Einträge nennen mehrere Seiten (S. 89/90, 219/221/223, 446/447). "
            f"Die Berichtigung zu S. 279 ist die Umrechnungstabelle der Maße und Gewichte (S. 831–832), die eigens ausgewertet ist."),
     "en": (f"The {n_pages} different target pages are spread across the whole book; {n_multi_page} entries name several pages (pp. 89/90, 219/221/223, 446/447). "
            f"The entry for p. 279 is the conversion table of weights and measures (pp. 831–832), which is analysed separately.")},
]
caveats = [
    {"de": "Die Zeilenangaben beziehen sich auf den Satzspiegel des gedruckten Buchs (»v. o.« von oben, »v. u.« von unten, Überschriften und Fußnoten eingerechnet oder nicht, ist offen). Sie wurden nicht an den Seiten nachgezählt; für die Verknüpfung in der Edition ist die Bezugsseite maßgeblich.",
     "en": "The line numbers refer to the type area of the printed book (“v. o.” from the top, “v. u.” from the bottom; whether headings and footnotes were counted is unclear). They were not recounted on the pages; for linking in the edition the target page is what matters."},
    {"de": "Art und Näheres sind redaktionelle Zuordnungen; die Grenze zwischen Zusatz und Aktualisierung ist unscharf (unbelegt datierte Neuerungen wie die Stiftung Bruhm gelten als Zusatz). Ein gedruckter Absatz kann mehrere Zeilen des Datensatzes ergeben.",
     "en": "Kind and detail are editorial assignments; the line between addition and update is blurred (undated novelties such as the Bruhm foundation count as additions). One printed paragraph can yield several rows of the dataset."},
    {"de": "Das Transkript hat drei Berichtigungen verfälscht, indem es die korrigierten Druckfehler stillschweigend glättete oder verlas (S. 489 »gauz«, S. 496 »besondeer«, S. 277 »zuverzinsenden«); der Datensatz gibt den gedruckten Wortlaut wieder.",
     "en": "The transcript distorted three corrections by silently smoothing or misreading the misprints being corrected (p. 489 “gauz”, p. 496 “besondeer”, p. 277 “zuverzinsenden”); the dataset gives the printed wording."},
    {"de": (f"Der Haupttext wurde nicht verändert; die Edition soll die Berichtigung neben der Stelle anzeigen. Bei {found.get('no', 0)} von {sum(found.values())} einfachen Berichtigungen steht der »statt«-Text nicht auf der Bezugsseite der Transkription: "
            f"teils ist die Stelle umformuliert zitiert, teils hat die Transkription den Druckfehler schon stillschweigend gebessert (geprüft am Faksimile für S. 489: gedruckt »gauz«, Transkription »ganz«). »no« in dieser Spalte heißt daher nicht, dass die Berichtigung falsch verortet ist."),
     "en": (f"The main text was not altered; the edition is meant to display the correction next to the passage. For {found.get('no', 0)} of {sum(found.values())} simple corrections the “statt” text is not on the target page of the transcription: "
            f"in some cases the passage is quoted in different words, in others the transcription has already silently improved the misprint (checked on the facsimile for p. 489: printed “gauz”, transcription “ganz”). “no” in this column therefore does not mean the correction is misplaced.")},
]
charts = [
    {"id": "c1", "dataset": "corrections", "title": {"de": "Berichtigungen je Kapitel", "en": "Corrections per chapter"},
     "caption": {"de": f"Anzahl der Einträge nach Kapitel der Bezugsseite, nach Art gefärbt. Die Natur des Landes (S. {nat_pages[0]}–{nat_pages[1]}) ist am dichtesten berichtigt.",
                 "en": f"Number of entries by chapter of the target page, coloured by kind. The nature of the land (pp. {nat_pages[0]}–{nat_pages[1]}) is the most densely corrected."},
     "vegalite": c1},
    {"id": "c2", "dataset": "corrections", "title": {"de": "Wo im Buch berichtigt wird", "en": "Where in the book corrections fall"},
     "caption": {"de": "Einträge je 25 Seiten des Buchs (Bezugsseite). Die erste Spitze liegt bei den naturkundlichen Kapiteln S. 61–90, danach bei Staat, Geschichte und Ortskunde.",
                 "en": "Entries per 25 pages of the book (target page). The first peak lies in the natural-history chapters pp. 61–90, afterwards in state, history and topography."},
     "vegalite": c2},
    {"id": "c3", "dataset": "corrections", "title": {"de": "Was berichtigt wird", "en": "What is corrected"},
     "caption": {"de": "Einträge nach Näherem (Schreibung, Wort, Zahl/Datum, Name, Aussage, Auslassung, Ergänzung, neues Ereignis), nach Art gefärbt.",
                 "en": "Entries by detail (spelling, word, number/date, name, statement, omission, supplement, new event), coloured by kind."},
     "vegalite": c3},
]
ana = {
    "id": "zusaetze-berichtigungen-1870",
    "title": title, "category": "reception", "section": "berichtigungen",
    "sources": refs, "summary": summary, "method": method, "findings": findings, "caveats": caveats,
    "datasets": [{"name": "corrections", "title": {"de": "Zusätze und Berichtigungen (ein Eintrag je Anweisung)", "en": "Addenda and corrigenda (one entry per instruction)"},
                  "columns": columns, "rows": data_rows, "source_refs": refs}],
    "charts": charts,
    "transcription_issues": [
        {"page": "831", "block": "b5", "transcribed": "lies: zuversindenden statt zu verzindenden", "facsimile": "lies: zuverzinsenden statt zu verzinsenden", "checked_facsimile": True,
         "note": "S. 277, Z. 13 v. u.; Fraktur-s als d gelesen"},
        {"page": "833", "block": "b19", "transcribed": "lies: ganz statt ganz", "facsimile": "lies: ganz statt gauz", "checked_facsimile": True,
         "note": "S. 489; der korrigierte Druckfehler »gauz« wurde im Transkript geglättet"},
        {"page": "833", "block": "b20", "transcribed": "lies: besondere statt besonderer", "facsimile": "lies: besondere statt besondeer", "checked_facsimile": True,
         "note": "S. 496; der korrigierte Druckfehler »besondeer« wurde im Transkript verlesen"},
    ],
    "related": ["masse-gewichte-umrechnung-1869"],
    "keywords": {"de": ["Berichtigungen", "Zusätze", "Corrigenda", "Druckfehler", "Nachträge", "Aktualisierung", "Brückner"],
                 "en": ["corrigenda", "addenda", "errata", "misprints", "updates", "Brückner"]},
    "generated_by": "Claude Sonnet 5.5 (subagent B01)", "date": "2026-10-01",
}
print(write_analysis(ana))
