"""Analysis: Volksmedizin - Hausmittel und Heilmittel nach Leiden (pp. 174-175)."""
import re
from collections import Counter, OrderedDict, defaultdict
from _common import *

a = text("174", "b3")
b = text("175", "b1")
gen = text("174", "b2")
t = a[a.index("Bei innerlichen Krankheiten"):] + " " + b
t = t.replace("Ofenblasen= wasser", "Ofenblasenwasser").replace("Ofenblasen=\nwasser", "Ofenblasenwasser")

USES = OrderedDict([
    ("abfuehr", ("So zur Abführung:", bi("Abführung", "Laxatives"), "innerlich")),
    ("harn", ("als Harn treibend:", bi("Harn treibend", "Diuretics"), "innerlich")),
    ("brust", ("als Brustmittel:", bi("Brustmittel", "Chest remedies"), "innerlich")),
    ("lunge", ("bei Lungensucht:", bi("Lungensucht", "Consumption"), "innerlich")),
    ("leber", ("bei Leberleiden:", bi("Leberleiden", "Liver complaints"), "innerlich")),
    ("magen", ("gegen Magenleiden:", bi("Magenleiden", "Stomach complaints"), "innerlich")),
    ("krampf", ("als krampfstillend:", bi("Krampfstillend", "Antispasmodics"), "innerlich")),
    ("blut", ("zur Blutreinigung:", bi("Blutreinigung", "Blood purification"), "innerlich")),
    ("wurm", ("gegen Würmer:", bi("Würmer", "Worms"), "innerlich")),
    ("blaeh", ("gegen Blähung:", bi("Blähung", "Flatulence"), "innerlich")),
    ("durchfall", ("gegen Durchfall:", bi("Durchfall", "Diarrhoea"), "innerlich")),
    ("ruhr", ("bei Dysenterie und Kolik:", bi("Ruhr und Kolik", "Dysentery and colic"), "innerlich")),
    ("schweiss", ("gegen Nachtschweiße:", bi("Nachtschweiß", "Night sweats"), "innerlich")),
    ("epilepsie", ("gegen Epilepsie:", bi("Epilepsie", "Epilepsy"), "innerlich")),
    ("abort", ("als Abortivmittel:", bi("Abtreibung", "Abortifacients"), "innerlich")),
    ("aussen", ("darunter hauptsächlich:", bi("Äußere Übel", "External ailments"), "äußerlich")),
])
SCOPE_EN = {"innerlich": "internal", "äußerlich": "external", "allgemein": "general"}
pos = []
for k, (marker, lab, scope) in USES.items():
    i = t.index(marker)
    pos.append((i, k, marker))
pos.sort()
segments = {}
for n, (i, k, marker) in enumerate(pos):
    j = pos[n + 1][0] if n + 1 < len(pos) else len(t)
    seg = t[i + len(marker):j]
    # cut at the sentence that introduces the external remedies
    if k == "abort":
        seg = seg.split(". Zur Heilung")[0]
    segments[k] = seg.strip().rstrip(".;").strip()


def items_of(seg):
    out = []
    # drop generic or trailing phrases
    seg = re.sub(r",? außerdem verschiedene Pillen und Tincturen", "", seg)
    seg = re.sub(r" und verschiedene Kräutersäfte", "", seg)
    seg = re.sub(r"und bei Thieren ", "und bei Thieren: ", seg)
    seg = seg.replace(", verschiedene Kräutersäfte", "").rstrip(";, ")
    parts = []
    # protect parentheses
    buf, depth = "", 0
    for ch in seg:
        if ch == "(":
            depth += 1
        if ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(buf)
            buf = ""
        else:
            buf += ch
    parts.append(buf)
    for p in parts:
        p = p.strip().rstrip(";").strip()
        if not p:
            continue
        if " und bei Thieren: " in p:
            first, second = p.split(" und bei Thieren: ")
            out.append((first.strip(), ""))
            out.append((second.strip(), "bei Tieren"))
            continue
        # split a trailing " und X" (last element) but keep multiword remedies
        m = re.match(r"^(.*?) und (bei Thieren: )?(.+)$", p)
        if m and not p.startswith("Bier mit") and "(" not in m.group(1):
            for q, note in ((m.group(1), ""), (m.group(3), "bei Tieren" if m.group(2) else "")):
                out.append((q.strip(), note))
        else:
            out.append((p, ""))
    res = []
    for r, note in out:
        mm = re.match(r"^(.*?)\s*\(([^)]*)\)$", r)
        if mm:
            r, note2 = mm.group(1).strip(), mm.group(2)
            note = (note + "; " + note2).strip("; ")
        res.append((r, note))
    return res


NORM = {"Chamillen": "Chamille", "Pfeffermünz": "Pfeffermünze", "Arnicamontana": "Arnica", "Arnica montana": "Arnica"}


def keyof(s):
    return NORM.get(s, s).lower()


rows = []
for k, (marker, lab, scope) in USES.items():
    for r, note in items_of(segments[k]):
        rows.append([k, lab["de"], lab["en"], scope, SCOPE_EN[scope], r, note, "175" if (k not in ("abfuehr", "harn", "brust") ) else "174", "b1" if (k not in ("abfuehr", "harn", "brust")) else "b3"])
# general household remedies (p. 174 b2)
gseg = gen[gen.index("vornämlich:") + len("vornämlich:"):]
gseg = gseg[:gseg.index(". Unter diesen Mitteln")]
gitems = items_of(gseg)
for r, note in gitems:
    rows.append(["haus", "Hausapotheke (allgemeine Hausmittel)", "Household remedies (general)", "allgemein", "general", r, note, "174", "b2"])
cnt = Counter(r[0] for r in rows)
print(cnt)
for k in USES:
    print(k, cnt[k], [r[5] for r in rows if r[0] == k][:6])
print("general", cnt["haus"])
# fix page/block for 'brust' tail on p.175 (items before 'Ofenblasenwasser' on p.174, rest p.175)
brust_tail = False
for r in rows:
    if r[0] == "brust":
        if r[5].startswith("Ofenblasenwasser") or brust_tail:
            brust_tail = True
        r[7], r[8] = ("175", "b1") if brust_tail else ("174", "b3")
        if r[5] == "Ofenblasenwasser":
            r[7], r[8] = "174", "b3"
            brust_tail = True
# all remaining brust items after Ofenblasenwasser are on p.175 b1
seen = False
for r in rows:
    if r[0] == "brust":
        if seen:
            r[7], r[8] = "175", "b1"
        if r[5] == "Ofenblasenwasser":
            r[7], r[8] = "174", "b3"
            seen = True

# verify every item occurs in the text
alltext = (a + " " + b + " " + gen).replace("Ofenblasen= wasser", "Ofenblasenwasser")
for r in rows:
    key = r[5].split()[0]
    assert key in alltext.replace("=\n", ""), r

spec = [r for r in rows if r[0] != "haus"]
distinct_spec = {keyof(r[5]) for r in spec}
distinct_gen = {keyof(r[5]) for r in rows if r[0] == "haus"}
overlap = distinct_spec & distinct_gen
print(len(spec), "specific entries;", len(distinct_spec), "distinct;", len(distinct_gen), "general;", len(overlap), "overlap")
uses_per = defaultdict(set)
for r in spec:
    uses_per[keyof(r[5])].add(r[0])
multi = sorted(((k, len(v)) for k, v in uses_per.items() if len(v) >= 2), key=lambda x: (-x[1], x[0]))
print(multi)
disp = {}
for r in rows:
    disp.setdefault(keyof(r[5]), NORM.get(r[5], r[5]))
HH = {1: bi("auch in der Hausapotheke", "also in the household pharmacy"), 0: bi("nur in den Einzellisten", "only in the individual lists")}
rows_multi = []
for k, n in multi:
    for u in USES:
        if u in uses_per[k]:
            rows_multi.append([disp[k], n, 1 if k in distinct_gen else 0, HH[1 if k in distinct_gen else 0]["de"], HH[1 if k in distinct_gen else 0]["en"], USES[u][1]["de"], USES[u][1]["en"]])
print(rows_multi[:6])
n_multi = len(multi)
magen_pairs = [k for k, n in multi if "magen" in uses_per[k]]
print("with Magenleiden:", magen_pairs)
max_uses = max(n for k, n in multi)
use_counts = [[USES[k][1]["de"], USES[k][1]["en"], USES[k][2], SCOPE_EN[USES[k][2]], cnt[k]] for k in USES]
use_counts.append(["Hausapotheke (allgemeine Hausmittel)", "Household remedies (general)", "allgemein", "general", cnt["haus"]])
print(use_counts)
top_uses = sorted(use_counts, key=lambda x: -x[4])
print(top_uses[:5])
n_int = sum(cnt[k] for k in USES if USES[k][2] == "innerlich")
assert "Johannisblume die größte Verehrung" in gen

USE_ORDER = None
SCOPE_DOMAIN = [bi("innerlich", "internal"), bi("äußerlich", "external"), bi("allgemein", "general")]
src = [{"page": "174", "block": "b2"}, {"page": "174", "block": "b3"}, {"page": "175", "block": "b1"}]

mt = rows_multi[:3]
ana = {
    "id": "gesundheit-volksmedizin-hausmittel-nach-leiden",
    "title": bi("Volksmedizin: Hausmittel und Heilmittel nach Leiden", "Folk medicine: household remedies by ailment"),
    "category": "health",
    "section": "t1-2-6",
    "sources": src,
    "summary": bi(
        f"Brückner zählt die Mittel der Volksmedizin in Listen auf: {cnt['haus']} allgemeine Hausmittel (S. 174) und {len(spec)} Nennungen von Kräutern, Salben und anderen Mitteln für 15 innere Leiden und äußere Übel (S. 174 f.). Die Auszählung zeigt, bei welchen Leiden das Volk die meisten Mittel kennt und welche Mittel vielseitig verwendet werden.",
        f"Brückner lists the means of folk medicine: {cnt['haus']} general household remedies (p. 174) and {len(spec)} mentions of herbs, ointments and other remedies for 15 internal ailments and external ills (pp. 174 f.). The count shows for which ailments the people know the most remedies and which remedies are used for several purposes.",
    ),
    "method": bi(
        "Die Aufzählungen im Text (S. 174 b2, b3, S. 175 b1) wurden per Skript an den Stichwörtern der Leiden (»gegen Würmer:« usw.) gegliedert und an Kommas und »und« in einzelne Mittel zerlegt; Angaben in Klammern (»gepulvert«, »neuntägige«) sind als Zusatz geführt, allgemeine Angaben (»verschiedene Pillen und Tincturen«, »Kräutersäfte«) nicht mitgezählt. Die Schreibweise der Mittel ist die gedruckte (z. B. »Wachholder«, »Chamille«); dasselbe Mittel wird über die Schreibung gleichgesetzt, Spielarten (Chamille/Chamillen) nicht. Zur Heilung äußerer Übel nennt Brückner nur eine einzige Liste.",
        "The enumerations in the text (p. 174 b2, b3, p. 175 b1) were divided by script at the key words of the ailments (“gegen Würmer:” etc.) and split into single remedies at commas and “und”; details in parentheses (“gepulvert”, “neuntägige”) are kept as notes, general statements (“verschiedene Pillen und Tincturen”, “Kräutersäfte”) are not counted. The spelling of the remedies is the printed one (e.g. “Wachholder”, “Chamille”); the same remedy is identified by its spelling, variant forms (Chamille/Chamillen) are not. For the cure of external ills Brückner gives only one single list.",
    ),
    "findings": [
        bi(
            f"Für äußere Übel nennt Brückner {cnt['aussen']} Mittel (Salben, Pflaster, Geister, Öle), für Brustleiden {cnt['brust']} und für Magenleiden {cnt['magen']}; die allgemeine Hausapotheke umfasst {cnt['haus']} Mittel. Für Epilepsie nennt er nur {cnt['epilepsie']}, für Lungensucht, Leberleiden, Nachtschweiß und Abtreibung je {cnt['lunge']}.",
            f"For external ills Brückner names {cnt['aussen']} remedies (ointments, plasters, spirits, oils), for chest complaints {cnt['brust']} and for stomach complaints {cnt['magen']}; the general household pharmacy comprises {cnt['haus']} remedies. For epilepsy he names only {cnt['epilepsie']}, for consumption, liver complaints, night sweats and abortion {cnt['lunge']} each.",
        ),
        bi(
            f"Nur {n_multi} von {len(distinct_spec)} verschiedenen Mitteln der Einzellisten stehen bei mehr als einem Leiden, und keines bei mehr als {max_uses}; bei {len(magen_pairs)} dieser {n_multi} Mittel gehört Magenleiden zu den beiden Anwendungen (z. B. Anis, Knoblauch, Pfeffer, Schafgarbe).",
            f"Only {n_multi} of {len(distinct_spec)} distinct remedies of the individual lists appear for more than one ailment, and none for more than {max_uses}; for {len(magen_pairs)} of these {n_multi} remedies stomach complaints are one of the two uses (e.g. anise, garlic, pepper, yarrow).",
        ),
        bi(
            f"{len(overlap)} der {len(distinct_spec)} Mittel der Einzellisten stehen auch in der allgemeinen Hausapotheke; als meistverehrtes Hausmittel nennt Brückner die Johannisblume (Arnika), die im Oberland korbweise gesammelt wird.",
            f"{len(overlap)} of the {len(distinct_spec)} remedies of the individual lists also appear in the general household pharmacy; as the most revered household remedy Brückner names the Johannisblume (arnica), which is gathered by the basket in the Oberland.",
        ),
    ],
    "caveats": [
        bi(
            "Gezählt wird, was Brückner aufzählt; er gibt weder Häufigkeit des Gebrauchs noch Wirksamkeit an, und die Listen sind Auswahlen (»nur Einiges kann angemerkt werden«). Die Zerlegung des Fließtextes in Einzelmittel ist redaktionell und kann bei zusammengesetzten Bezeichnungen (z. B. »Bier mit Gänsefett«) abweichen.",
            "What is counted is what Brückner enumerates; he gives neither frequency of use nor efficacy, and the lists are selections (“only some can be noted”). The splitting of the running text into single remedies is editorial and can differ for compound names (e.g. “Bier mit Gänsefett”).",
        ),
        bi(
            "Die Mittelnamen sind historisch (Allermannsharnisch, Sannickel, Elendsklaue, Attigbeeren); eine botanische oder pharmazeutische Identifizierung ist hier nicht versucht. Neben den Kräutermitteln stellt Brückner Amulette, Zauberformeln und die Wunderkur (S. 175 f.), die hier nicht erfasst sind.",
            "The names of the remedies are historical (Allermannsharnisch, Sannickel, Elendsklaue, Attigbeeren); no botanical or pharmaceutical identification is attempted here. Besides the herbal remedies Brückner treats amulets, magic formulas and the miracle cure (pp. 175 f.), which are not covered here.",
        ),
    ],
    "datasets": [
        {
            "name": "remedies",
            "title": bi("Mittel der Volksmedizin nach Leiden", "Remedies of folk medicine by ailment"),
            "columns": [
                {"name": "use_key", "label": bi("Leiden (Schlüssel)", "Ailment (key)"), "type": "string", "unit": None, "derived": True},
                {"name": "use_de", "label": bi("Leiden / Anwendung (de)", "Ailment / use (de)"), "type": "string", "unit": None},
                {"name": "use_en", "label": bi("Leiden / Anwendung (en)", "Ailment / use (en)"), "type": "string", "unit": None, "derived": True},
                {"name": "scope_de", "label": bi("Anwendung (de)", "Application (de)"), "type": "string", "unit": None, "derived": True},
                {"name": "scope_en", "label": bi("Anwendung (en)", "Application (en)"), "type": "string", "unit": None, "derived": True},
                {"name": "remedy", "label": bi("Mittel (gedruckt)", "Remedy (as printed)"), "type": "string", "unit": None},
                {"name": "note", "label": bi("Zusatz", "Note"), "type": "string", "unit": None},
                {"name": "page", "label": bi("Seite", "Page"), "type": "string", "unit": None},
                {"name": "block", "label": bi("Block", "Block"), "type": "string", "unit": None},
            ],
            "rows": rows,
            "source_refs": src,
        },
        {
            "name": "use_counts",
            "title": bi("Zahl der Mittel je Leiden", "Number of remedies per ailment"),
            "columns": [
                {"name": "use_de", "label": bi("Leiden / Anwendung (de)", "Ailment / use (de)"), "type": "string", "unit": None, "derived": True},
                {"name": "use_en", "label": bi("Leiden / Anwendung (en)", "Ailment / use (en)"), "type": "string", "unit": None, "derived": True},
                {"name": "scope_de", "label": bi("Anwendung (de)", "Application (de)"), "type": "string", "unit": None, "derived": True},
                {"name": "scope_en", "label": bi("Anwendung (en)", "Application (en)"), "type": "string", "unit": None, "derived": True},
                {"name": "remedies", "label": bi("Zahl der Mittel", "Number of remedies"), "type": "integer", "unit": "Mittel", "derived": True},
            ],
            "rows": use_counts,
            "source_refs": src,
        },
        {
            "name": "multi",
            "title": bi("Mittel für mehrere Leiden", "Remedies used for several ailments"),
            "columns": [
                {"name": "remedy", "label": bi("Mittel", "Remedy"), "type": "string", "unit": None, "derived": True},
                {"name": "ailments", "label": bi("Zahl der Leiden des Mittels", "Number of ailments of the remedy"), "type": "integer", "unit": "Leiden", "derived": True},
                {"name": "in_household", "label": bi("Auch in der Hausapotheke (1 = ja)", "Also in the household pharmacy (1 = yes)"), "type": "integer", "unit": None, "derived": True},
                {"name": "household_de", "label": bi("Hausapotheke (de)", "Household pharmacy (de)"), "type": "string", "unit": None, "derived": True},
                {"name": "household_en", "label": bi("Hausapotheke (en)", "Household pharmacy (en)"), "type": "string", "unit": None, "derived": True},
                {"name": "use_de", "label": bi("Leiden / Anwendung (de)", "Ailment / use (de)"), "type": "string", "unit": None, "derived": True},
                {"name": "use_en", "label": bi("Leiden / Anwendung (en)", "Ailment / use (en)"), "type": "string", "unit": None, "derived": True},
            ],
            "rows": rows_multi,
            "source_refs": src,
        },
    ],
    "charts": [
        {
            "id": "c1",
            "dataset": "use_counts",
            "title": bi("Wie viele Mittel für welches Leiden", "How many remedies for which ailment"),
            "caption": bi(
                "Zahl der von Brückner genannten Mittel je Leiden (S. 174 f.). Für äußere Übel und die allgemeine Hausapotheke werden die meisten Mittel aufgezählt, unter den inneren Leiden für Brust- und Magenleiden.",
                "Number of remedies named by Brückner per ailment (pp. 174 f.). The most remedies are listed for external ills and the general household pharmacy, among internal ailments for chest and stomach complaints.",
            ),
            "vegalite": {
                "height": 420,
                "mark": "bar",
                "encoding": {
                    "y": {"field": {"de": "use_de", "en": "use_en"}, "type": "nominal", "sort": {"field": "remedies", "order": "descending"}, "title": None, "axis": {"labelLimit": 420}},
                    "x": {"field": "remedies", "type": "quantitative", "title": bi("Mittel", "Remedies"), "axis": {"tickMinStep": 1}},
                    "color": {"field": {"de": "scope_de", "en": "scope_en"}, "type": "nominal", "title": None, "scale": {"domain": SCOPE_DOMAIN}, "legend": {"labelLimit": 400}},
                    "tooltip": [
                        {"field": {"de": "use_de", "en": "use_en"}, "title": bi("Leiden", "Ailment")},
                        {"field": "remedies", "title": bi("Mittel", "Remedies")},
                    ],
                },
            },
        },
        {
            "id": "c2",
            "dataset": "multi",
            "title": bi("Mittel für zwei Leiden", "Remedies used for two ailments"),
            "caption": bi(
                "Mittel, die in Brückners Einzellisten bei zwei Leiden stehen (Punkte = Anwendungen). Magenleiden teilen die meisten Mittel mit anderen Leiden (Abführung, Blähung, Ruhr, Würmer, Krampf, äußere Übel).",
                "Remedies that appear in Brückner’s individual lists for two ailments (dots = uses). Stomach complaints share the most remedies with other ailments (laxatives, flatulence, dysentery, worms, spasms, external ills).",
            ),
            "vegalite": {
                "height": 320,
                "mark": {"type": "point", "filled": True, "size": 110},
                "encoding": {
                    "y": {"field": "remedy", "type": "nominal", "sort": "ascending", "title": None},
                    "x": {"field": {"de": "use_de", "en": "use_en"}, "type": "nominal", "title": None, "axis": {"labelAngle": -45, "labelLimit": 300}},
                    "color": {"field": {"de": "household_de", "en": "household_en"}, "type": "nominal", "title": None, "scale": {"domain": [HH[1], HH[0]]}, "legend": {"labelLimit": 400}},
                    "tooltip": [
                        {"field": "remedy", "title": bi("Mittel", "Remedy")},
                        {"field": {"de": "use_de", "en": "use_en"}, "title": bi("Leiden", "Ailment")},
                    ],
                },
            },
        },
    ],
    "transcription_issues": [],
    "keywords": {
        "de": ["Volksmedizin", "Hausmittel", "Kräuter", "Heilmittel", "Arnika", "Johannisblume", "Aberglaube", "Apotheke", "Hausapotheke"],
        "en": ["folk medicine", "household remedies", "herbs", "remedies", "arnica", "superstition", "pharmacy"],
    },
    "related": ["gesundheit-krankheitsstatistik-lobenstein-gera-hohenleuben", "gesundheit-medizinalwesen-und-seuchen-zeitleiste"],
    "generated_by": GEN,
    "date": DATE,
}
write(ana)
