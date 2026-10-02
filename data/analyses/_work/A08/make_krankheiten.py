"""Analysis: Krankheitsstatistik (pp. 169-172): Hauptkrankheiten nach Orten, Hohenleuben nach Monaten, Gera Hautkrankheiten."""
import re
from _common import *

PLACES = ["Lobenstein", "Tanna", "Gera", "Hohenleuben"]
EN = {
    "Catarrhe:": "Catarrhs",
    "a) der Luftwege": "Catarrhs of the airways",
    "b) des Darmcanals": "Catarrhs of the intestinal tract",
    "Rheumatische Fieber": "Rheumatic fevers",
    "Nervenfieber": "Nervous fever",
    "Gastrische Fieber": "Gastric fevers",
    "Lungenentzündung": "Pneumonia",
    "Lungenschwindsucht": "Pulmonary consumption",
    "Unterleibsentzündung": "Abdominal inflammation",
    "Kolik": "Colic",
    "Magenkrampf": "Stomach cramps",
    "Mandelbräune": "Quinsy (tonsillitis)",
    "Friesel": "Friesel (rash fevers)",
    "Blattern (Varicellen)": "Pox (varicella)",
    "Bleichsucht": "Chlorosis (anaemia)",
    "Krätze und ähnliche Hautkrankheiten": "Scabies and similar skin diseases",
    "Flechten": "Lichens (skin eruptions)",
    "Venerie": "Venereal diseases",
    "Masern": "Measles",
    "Scharlach": "Scarlet fever",
    "Kropf": "Goitre",
    "Gebärmutterkrankheiten": "Diseases of the womb",
}
DE_SHORT = {"Catarrhe:": "Katarrhe", "Krätze und ähnliche Hautkrankheiten": "Krätze u. ähnl. Hautkrankheiten",
            "Blattern (Varicellen)": "Blattern (Varicellen)"}
EN_SHORT = {"Scabies and similar skin diseases": "Scabies, similar skin diseases"}
FRAC = {"1/2": 0.5, "1/4": 0.25, "1/8": 0.125}


def val(s):
    return FRAC[s] if s in FRAC else num(s)


g = block("172", "b2")["grid"]
rows = []
for r in g[1:]:
    name = r[0]
    level = 1 if name[:2] in ("a)", "b)") else 0
    de = DE_SHORT.get(name, name)
    en_ = EN[name]
    en_ = EN_SHORT.get(en_, en_)
    for place, cell in zip(PLACES, r[1:5]):
        if cell == "—":
            continue
        rows.append([de, en_, level, place, cell, val(cell), "172"])
# scrofula (text p. 170 b2)
t = text("170", "b2")
scr = re.search(r"dort (\d,\d+), hier (\d,\d+) Procente", t)
assert scr
rows.append(["Skrofeln", "Scrofula", 0, "Gera", scr.group(1), num(scr.group(1)), "170"])
rows.append(["Skrofeln", "Scrofula", 0, "Hohenleuben", scr.group(2), num(scr.group(2)), "170"])
# number of places per disease (level 0)
from collections import defaultdict
nplaces = defaultdict(set)
for r in rows:
    if r[2] == 0:
        nplaces[r[0]].add(r[3])
for r in rows:
    r.append(1 if (r[2] == 0 and len(nplaces[r[0]]) >= 2) else 0)
rows_dis = [[r[0], r[1], r[2], r[3], r[4], r[5], r[7]] for r in rows]
print(len(rows_dis), "disease cells;", sum(r[6] for r in rows_dis), "in shared comparison")
lob = sorted([r for r in rows_dis if r[3] == "Lobenstein" and r[2] == 0], key=lambda r: -r[5])
print([(r[0], r[5]) for r in lob][:6])

# ---- Hohenleuben monthly
gm = block("169", "b3")["grid"]
MONTH_DE = ["Jan.", "Febr.", "März", "Apr.", "Mai", "Juni", "Juli", "Aug.", "Sept.", "Okt.", "Nov.", "Dez."]
MONTH_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
printed = {}
for r in gm:
    for i in range(0, 8, 2):
        printed[r[i]] = r[i + 1]
ORDER = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "October", "November", "December"]
rows_m = []
for k, name in enumerate(ORDER, start=1):
    v = num(printed[name])
    rows_m.append([k, name, MONTH_DE[k - 1], MONTH_EN[k - 1], (k - 1) // 3 + 1, v])
tot = round(sum(r[5] for r in rows_m), 2)
print("sum of months", tot)
h1 = round(sum(r[5] for r in rows_m[:6]), 2)
h2 = round(sum(r[5] for r in rows_m[6:]), 2)
print("halves", h1, h2)
gq = block("169", "b5")["grid"]
qprinted = [num(gq[1][1]), num(gq[1][3]), num(gq[1][5]), num(gq[1][7].replace("Proc.,", ""))]
rows_q = []
for q in range(1, 5):
    s = round(sum(r[5] for r in rows_m if r[4] == q), 2)
    rows_q.append([q, qprinted[q - 1], s, round(qprinted[q - 1] - s, 2)])
print(rows_q)
mx = max(rows_m, key=lambda r: r[5]); mn = min(rows_m, key=lambda r: r[5])
low3 = sorted(rows_m, key=lambda r: r[5])[:3]
print(mx, mn, [r[1] for r in low3])

# ---- Gera skin diseases
t = text("171", "b2")
m1 = re.search(r"1856—1860 gab es daselbst unter (\d+) Krankheitsfällen (\d+) und von 1861—1864 unter (\d+) Krankheitsfällen (\d+)", t)
m2 = re.search(r"1865—1867 unter (\d+) inneren Krankheitsfällen (\d+) Erkrankte", t)
m3 = re.search(r"in jener Periode (\d,\d+), in dieser (\d,\d+), und in der von 1865—1867: (\d+,\d+) Procent", t)
assert m1 and m2 and m3, (m1, m2, m3)
periods = [
    ("1856–1860", int(m1.group(1)), int(m1.group(2)), num(m3.group(1))),
    ("1861–1864", int(m1.group(3)), int(m1.group(4)), num(m3.group(2))),
    ("1865–1867", int(m2.group(1)), int(m2.group(2)), num(m3.group(3))),
]
rows_g = []
for k, (lab, pat, cases, pct) in enumerate(periods, start=1):
    rows_g.append([k, lab, pat, cases, pct, round(100 * cases / pat, 1)])
print(rows_g)
ratio = round(periods[2][3] / periods[0][3], 2)
print("printed pct 1865-67 / 1856-60 =", ratio)

# derived figures for text
gera_h = {r[0]: r[5] for r in rows_dis if r[3] == "Gera"}
hoh = {r[0]: r[5] for r in rows_dis if r[3] == "Hohenleuben"}
lobd = {r[0]: r[5] for r in rows_dis if r[3] == "Lobenstein" and r[2] == 0}

YEARS = bi("Jahre", "Years")
ana = {
    "id": "gesundheit-krankheitsstatistik-lobenstein-gera-hohenleuben",
    "title": bi("Hauptkrankheiten in Lobenstein, Gera und Hohenleuben", "Main diseases at Lobenstein, Gera and Hohenleuben"),
    "category": "health",
    "section": "t1-2-6",
    "sources": [
        {"page": "172", "block": "b2", "rows": "r2-r23"},
        {"page": "172", "block": "fn1"},
        {"page": "169", "block": "b2"},
        {"page": "169", "block": "b3"},
        {"page": "169", "block": "b5"},
        {"page": "170", "block": "b2"},
        {"page": "170", "block": "b3"},
        {"page": "171", "block": "b2"},
    ],
    "summary": bi(
        "Brückner stützt sein Bild der Volkskrankheiten auf die Aufzeichnungen weniger Ärzte und Stationen: Dr. Aschenbach (Lobenstein, zehnjährige Erfahrung), die Krankenhausstation Gera, Hohenleuben und Tanna. Die »Uebersicht der Hauptkrankheiten in Procenten der Erkrankten« (S. 172) stellt 20 Krankheitsgruppen nebeneinander; dazu kommen die Monatsverteilung der Erkrankungen in Hohenleuben 1850–1860 (S. 169) und die Zunahme der Krätze in der Station Gera (S. 171). Die Grafiken zeigen, welche Krankheiten die Orte unterscheiden, wann im Jahr am häufigsten erkrankt wurde und wie stark die Hautleiden in Gera zunahmen.",
        "Brückner bases his picture of the diseases of the people on the records of a few physicians and stations: Dr Aschenbach (Lobenstein, ten years’ experience), the hospital station at Gera, Hohenleuben and Tanna. The “overview of the main diseases in percentages of those taken ill” (p. 172) sets 20 disease groups side by side; added to this are the monthly distribution of illness at Hohenleuben 1850–1860 (p. 169) and the rise of scabies at the Gera station (p. 171). The charts show which diseases distinguish the places, when in the year people fell ill most often, and how strongly skin complaints increased at Gera.",
    ),
    "method": bi(
        "Die Prozentwerte der Tabelle S. 172 (Block b2, r2–r23) wurden Zelle für Zelle übernommen; Striche (—) bedeuten »nicht angegeben« und wurden weggelassen, Brüche (1/2, 1/4, 1/8) in Dezimalzahlen überführt (Spalte »printed« = Druckform). Skrofeln (Gera 0,09 %, Hohenleuben 1,30 %) stehen nur im Text S. 170. Die Monatswerte (S. 169, b3) und Quartalswerte (b5) wurden übernommen; die Quartalssummen wurden aus den Monaten nachgerechnet. Die Zahlen zur Krätze in Gera stammen aus dem Text S. 171 (Fallzahlen und gedruckte Prozente). Die Orte sind nicht unmittelbar vergleichbar: Lobenstein = Praxis von Dr. Aschenbach, Gera = innere Station des Krankenhauses, Hohenleuben = ganzer Ort (S. 169).",
        "The percentages of the table on p. 172 (block b2, r2–r23) were taken cell by cell; dashes (—) mean “not given” and were omitted, fractions (1/2, 1/4, 1/8) were converted into decimals (column “printed” = printed form). Scrofula (Gera 0.09 %, Hohenleuben 1.30 %) appears only in the text on p. 170. The monthly values (p. 169, b3) and quarterly values (b5) were taken over; the quarterly sums were recomputed from the months. The figures on scabies at Gera come from the text on p. 171 (case numbers and printed percentages). The places are not directly comparable: Lobenstein = the practice of Dr Aschenbach, Gera = the internal ward of the hospital, Hohenleuben = the whole town (p. 169).",
    ),
    "findings": [
        bi(
            f"Krätze und ähnliche Hautkrankheiten sind in der Station Gera mit {dz(gera_h['Krätze u. ähnl. Hautkrankheiten'], 2)} % mehr als doppelt so häufig wie in Hohenleuben ({dz(hoh['Krätze u. ähnl. Hautkrankheiten'], 2)} %) und Lobenstein ({dz(lobd['Krätze u. ähnl. Hautkrankheiten'], 0)} %); Brückner führt dies auf die Fabrikarbeiter zurück.",
            f"Scabies and similar skin diseases account for {ez(gera_h['Krätze u. ähnl. Hautkrankheiten'], 2)} % at the Gera station, more than twice the share at Hohenleuben ({ez(hoh['Krätze u. ähnl. Hautkrankheiten'], 2)} %) and Lobenstein ({ez(lobd['Krätze u. ähnl. Hautkrankheiten'], 0)} %); Brückner attributes this to the factory workers.",
        ),
        bi(
            f"In Gera stieg der gedruckte Prozentsatz der Hautkranken von {dz(periods[0][3], 2)} % (1856–1860) über {dz(periods[1][3], 2)} % (1861–1864) auf {dz(periods[2][3], 2)} % (1865–1867), also auf das {dz(ratio, 1)}fache.",
            f"At Gera the printed percentage of skin patients rose from {ez(periods[0][3], 2)} % (1856–1860) through {ez(periods[1][3], 2)} % (1861–1864) to {ez(periods[2][3], 2)} % (1865–1867), i.e. to {ez(ratio, 1)} times.",
        ),
        bi(
            f"Katarrhe sind die häufigste Krankheitsgruppe in Lobenstein ({lobd['Katarrhe']:.0f} %: Atemwege 3, Darm 6), Hohenleuben (7 %) und Gera ({dz(gera_h['Katarrhe'], 0)} %); in Lobenstein folgen Krätze (6 %), Gastrische Fieber und Lungenentzündung (je 4 %).",
            f"Catarrhs are the most frequent group at Lobenstein ({lobd['Katarrhe']:.0f} %: airways 3, intestines 6), Hohenleuben (7 %) and Gera ({ez(gera_h['Katarrhe'], 0)} %); at Lobenstein they are followed by scabies (6 %), gastric fevers and pneumonia (4 % each).",
        ),
        bi(
            f"In Hohenleuben (Durchschnitt 1850–1860) entfallen die meisten Erkrankungen auf Mai ({dz(mx[5], 2)} %) und April ({dz(rows_m[3][5], 2)} %), die wenigsten auf November ({dz(rows_m[10][5], 2)} %), August ({dz(rows_m[7][5], 2)} %) und Oktober ({dz(rows_m[9][5], 2)} %). Auf das erste Halbjahr kommen {dz(h1, 2)} %, auf das zweite {dz(h2, 2)} % der Fälle.",
            f"At Hohenleuben (average 1850–1860) most cases fall in May ({ez(mx[5], 2)} %) and April ({ez(rows_m[3][5], 2)} %), the fewest in November ({ez(rows_m[10][5], 2)} %), August ({ez(rows_m[7][5], 2)} %) and October ({ez(rows_m[9][5], 2)} %). The first half-year accounts for {ez(h1, 2)} % of the cases, the second for {ez(h2, 2)} %.",
        ),
    ],
    "caveats": [
        bi(
            "Die Spalten messen Verschiedenes: Lobenstein beruht auf der zehnjährigen Erfahrung eines Arztes, Gera auf der Krankenhausstation (vor allem Fabrikarbeiter und Arme), Hohenleuben auf dem ganzen Ort. Tanna liefert nur einen Wert (Nervenfieber 0,36 %). Fehlende Werte (Striche) bedeuten »nicht angegeben«, nicht »0«.",
            "The columns measure different things: Lobenstein rests on one physician’s ten years of experience, Gera on the hospital station (mainly factory workers and the poor), Hohenleuben on the whole town. Tanna supplies only one value (nervous fever 0.36 %). Missing values (dashes) mean “not given”, not “0”.",
        ),
        bi(
            "Der Druck ist an mehreren Stellen in sich widersprüchlich (am Faksimile geprüft, die Transkription stimmt mit dem Druck überein): Gastrische Fieber in Hohenleuben 4,26 % in der Tabelle (S. 172), 4,91 % im Text (S. 170); das dritte Vierteljahr 23,28 % (S. 169), die gedruckten Monate ergeben 23,38 %. Außerdem lassen sich die gedruckten Prozentwerte der Krätze nicht aus den gedruckten Fallzahlen ableiten (413 von 1010 = 40,9 %, gedruckt 13,60 %; 377 von 1191 = 31,7 %, gedruckt 6,50 %); vermutlich liegt eine andere Bezugsgröße zugrunde, die Brückner nicht nennt. Die Grafik zeigt deshalb die gedruckten Prozentwerte.",
            "The print is internally inconsistent in several places (checked against the facsimile; the transcription agrees with the print): gastric fevers at Hohenleuben 4.26 % in the table (p. 172), 4.91 % in the text (p. 170); the third quarter 23.28 % (p. 169), whereas the printed months add up to 23.38 %. Moreover, the printed percentages for scabies cannot be derived from the printed case numbers (413 of 1010 = 40.9 %, printed 13.60 %; 377 of 1191 = 31.7 %, printed 6.50 %); presumably a different base is meant, which Brückner does not state. The chart therefore shows the printed percentages.",
        ),
        bi(
            "Mit 20 Krankheitsgruppen aus vier Quellen und zum Teil wenigen hundert Fällen sind die Werte grobe Anhaltspunkte; zeitgenössische Krankheitsbezeichnungen (Friesel, Flechten, Bleichsucht, Venerie) sind nicht mit modernen Diagnosen gleichzusetzen.",
            "With 20 disease groups from four sources and in part a few hundred cases, the values are rough indications only; contemporary disease names (Friesel, Flechten, Bleichsucht, Venerie) cannot be equated with modern diagnoses.",
        ),
    ],
    "conversions": [
        {"from": "Bruchwerte 1/2, 1/4, 1/8 (Prozent)", "to": "Dezimalzahl", "factor_or_formula": "0.5, 0.25, 0.125"},
    ],
    "datasets": [
        {
            "name": "diseases",
            "title": bi("Krankheiten in Prozent der Erkrankten nach Ort", "Diseases in per cent of those taken ill, by place"),
            "columns": [
                {"name": "disease_de", "label": bi("Krankheit (de)", "Disease (de)"), "type": "string", "unit": None},
                {"name": "disease_en", "label": bi("Krankheit (en)", "Disease (en)"), "type": "string", "unit": None},
                {"name": "level", "label": bi("Ebene (0 = Gruppe, 1 = Untergruppe)", "Level (0 = group, 1 = subgroup)"), "type": "integer", "unit": None, "derived": True},
                {"name": "place", "label": bi("Ort", "Place"), "type": "string", "unit": None},
                {"name": "printed", "label": bi("Druckform", "Printed form"), "type": "string", "unit": None},
                {"name": "percent", "label": bi("Prozent der Erkrankten", "Per cent of those taken ill"), "type": "number", "unit": "%", "derived": True, "note": "Brüche und Dezimalkommata in Dezimalzahlen überführt"},
                {"name": "shared", "label": bi("In mindestens zwei Orten angegeben", "Given for at least two places"), "type": "integer", "unit": None, "derived": True},
            ],
            "rows": rows_dis,
            "source_refs": [{"page": "172", "block": "b2", "rows": "r2-r23"}, {"page": "170", "block": "b2"}],
        },
        {
            "name": "hohenleuben_months",
            "title": bi("Erkrankungen in Hohenleuben nach Monaten, Durchschnitt 1850–1860", "Cases of illness at Hohenleuben by month, average 1850–1860"),
            "columns": [
                {"name": "month", "label": bi("Monat (Nummer)", "Month (number)"), "type": "integer", "unit": None, "derived": True, "note": "Monatsnummer 1–12, editorisch"},
                {"name": "month_printed", "label": bi("Monat (Original)", "Month (original)"), "type": "string", "unit": None},
                {"name": "month_de", "label": bi("Monat (kurz, de)", "Month (short, de)"), "type": "string", "unit": None, "derived": True},
                {"name": "month_en", "label": bi("Monat (kurz, en)", "Month (short, en)"), "type": "string", "unit": None, "derived": True},
                {"name": "quarter", "label": bi("Vierteljahr", "Quarter"), "type": "integer", "unit": None, "derived": True},
                {"name": "percent", "label": bi("Anteil an den Erkrankungsfällen", "Share of the cases of illness"), "type": "number", "unit": "%"},
            ],
            "rows": rows_m,
            "source_refs": [{"page": "169", "block": "b3"}],
        },
        {
            "name": "hohenleuben_quarters",
            "title": bi("Vierteljahre in Hohenleuben (gedruckt und nachgerechnet)", "Quarters at Hohenleuben (printed and recomputed)"),
            "columns": [
                {"name": "quarter", "label": bi("Vierteljahr", "Quarter"), "type": "integer", "unit": None, "derived": True},
                {"name": "printed", "label": bi("Gedruckter Wert", "Printed value"), "type": "number", "unit": "%"},
                {"name": "sum_months", "label": bi("Summe der Monate", "Sum of the months"), "type": "number", "unit": "%", "derived": True},
                {"name": "difference", "label": bi("Differenz", "Difference"), "type": "number", "unit": "%", "derived": True},
            ],
            "rows": rows_q,
            "source_refs": [{"page": "169", "block": "b5"}],
        },
        {
            "name": "gera_skin",
            "title": bi("Krätze und ähnliche Hautausschläge in der inneren Station Gera", "Scabies and similar skin eruptions at the internal station Gera"),
            "columns": [
                {"name": "period_no", "label": bi("Zeitraum (Nr.)", "Period (no.)"), "type": "integer", "unit": None, "derived": True},
                {"name": "period", "label": bi("Zeitraum", "Period"), "type": "string", "unit": None},
                {"name": "patients", "label": bi("Krankheitsfälle", "Cases of illness"), "type": "integer", "unit": "Fälle"},
                {"name": "skin_cases", "label": bi("davon Krätze und ähnliche Hautausschläge", "of which scabies and similar skin eruptions"), "type": "integer", "unit": "Fälle"},
                {"name": "percent_printed", "label": bi("Prozent (gedruckt)", "Per cent (printed)"), "type": "number", "unit": "%"},
                {"name": "percent_ratio", "label": bi("Quotient der gedruckten Fallzahlen", "Quotient of the printed case numbers"), "type": "number", "unit": "%", "derived": True},
            ],
            "rows": rows_g,
            "source_refs": [{"page": "171", "block": "b2"}],
        },
    ],
    "charts": [
        {
            "id": "c1",
            "dataset": "diseases",
            "title": bi("Krankheiten im Vergleich der Orte", "Diseases compared between places"),
            "caption": bi(
                "Neun Krankheitsgruppen, für die mindestens zwei Orte Werte nennen (Prozent der Erkrankten). In Gera dominieren die Hautleiden; Rheumatische Fieber sind in Hohenleuben am häufigsten.",
                "Nine disease groups for which at least two places give values (per cent of those taken ill). Skin complaints dominate at Gera; rheumatic fevers are most frequent at Hohenleuben.",
            ),
            "vegalite": {
                "height": 380,
                "transform": [{"filter": "datum.shared == 1"}],
                "mark": "bar",
                "encoding": {
                    "y": {"field": {"de": "disease_de", "en": "disease_en"}, "type": "nominal", "title": None, "sort": {"field": "percent", "op": "max", "order": "descending"}, "axis": {"labelLimit": 400}},
                    "yOffset": {"field": "place", "sort": ["Lobenstein", "Tanna", "Gera", "Hohenleuben"]},
                    "x": {"field": "percent", "type": "quantitative", "title": bi("Prozent der Erkrankten", "Per cent of those taken ill")},
                    "color": {"field": "place", "type": "nominal", "title": None, "scale": {"domain": PLACES}},
                    "tooltip": [
                        {"field": {"de": "disease_de", "en": "disease_en"}, "title": bi("Krankheit", "Disease")},
                        {"field": "place", "title": bi("Ort", "Place")},
                        {"field": "printed", "title": bi("Gedruckt", "Printed")},
                        {"field": "percent", "title": bi("Prozent", "Per cent")},
                    ],
                },
            },
        },
        {
            "id": "c2",
            "dataset": "diseases",
            "title": bi("Krankheitsbild in Lobenstein", "Disease profile at Lobenstein"),
            "caption": bi(
                "Nach der zehnjährigen Erfahrung von Dr. Aschenbach. Die Katarrhe (9 %) setzen sich aus Atemwegen (3) und Darm (6) zusammen.",
                "According to Dr Aschenbach’s ten years of experience. The catarrhs (9 %) consist of airways (3) and intestinal tract (6).",
            ),
            "vegalite": {
                "height": 400,
                "transform": [{"filter": "datum.place == 'Lobenstein' && datum.level == 0"}],
                "mark": "bar",
                "encoding": {
                    "y": {"field": {"de": "disease_de", "en": "disease_en"}, "type": "nominal", "title": None, "sort": {"field": "percent", "order": "descending"}, "axis": {"labelLimit": 400}},
                    "x": {"field": "percent", "type": "quantitative", "title": bi("Prozent der Erkrankten", "Per cent of those taken ill")},
                    "tooltip": [
                        {"field": {"de": "disease_de", "en": "disease_en"}, "title": bi("Krankheit", "Disease")},
                        {"field": "printed", "title": bi("Gedruckt", "Printed")},
                        {"field": "percent", "title": bi("Prozent", "Per cent")},
                    ],
                },
            },
        },
        {
            "id": "c3",
            "dataset": "hohenleuben_months",
            "title": bi("Erkrankungen im Jahresverlauf (Hohenleuben)", "Illness over the year (Hohenleuben)"),
            "caption": bi(
                "Anteil der Erkrankungsfälle je Monat, Durchschnitt 1850–1860. Die gestrichelte Linie markiert die Gleichverteilung (100 ÷ 12 = 8,33 %).",
                "Share of cases of illness per month, average 1850–1860. The dashed line marks an even distribution (100 ÷ 12 = 8.33 %).",
            ),
            "vegalite": {
                "height": 260,
                "layer": [
                    {
                        "mark": "bar",
                        "encoding": {
                            "x": {"field": {"de": "month_de", "en": "month_en"}, "type": "ordinal", "sort": {"field": "month", "op": "min"}, "title": None, "axis": {"labelAngle": 0}},
                            "y": {"field": "percent", "type": "quantitative", "title": "%"},
                            "tooltip": [
                                {"field": "month_printed", "title": bi("Monat", "Month")},
                                {"field": "percent", "title": bi("Prozent der Fälle", "Per cent of cases")},
                            ],
                        },
                    },
                    {"mark": {"type": "rule", "strokeDash": [4, 3]}, "encoding": {"y": {"datum": 8.33}}},
                ],
            },
        },
        {
            "id": "c4",
            "dataset": "gera_skin",
            "title": bi("Krätze und ähnliche Hautausschläge in Gera", "Scabies and similar skin eruptions at Gera"),
            "caption": bi(
                "Gedruckter Prozentsatz der Hautkranken unter den inneren Krankheitsfällen der Krankenhausstation, drei Zeiträume. Brückner führt die Zunahme auf die Fabrikarbeiter zurück.",
                "Printed percentage of skin patients among the internal cases of the hospital station, three periods. Brückner attributes the increase to factory workers.",
            ),
            "vegalite": {
                "height": 220,
                "mark": "bar",
                "encoding": {
                    "x": {"field": "period", "type": "ordinal", "sort": {"field": "period_no", "op": "min"}, "title": None, "axis": {"labelAngle": 0}},
                    "y": {"field": "percent_printed", "type": "quantitative", "title": "%"},
                    "tooltip": [
                        {"field": "period", "title": bi("Zeitraum", "Period")},
                        {"field": "patients", "title": bi("Krankheitsfälle", "Cases of illness")},
                        {"field": "skin_cases", "title": bi("Hautkranke (gedruckt)", "Skin cases (printed)")},
                        {"field": "percent_printed", "title": bi("Prozent (gedruckt)", "Per cent (printed)")},
                    ],
                },
            },
        },
    ],
    "transcription_issues": [],
    "keywords": {
        "de": ["Krankheiten", "Volkskrankheit", "Krätze", "Katarrh", "Fieber", "Jahreszeit", "Lobenstein", "Gera", "Hohenleuben", "Tanna"],
        "en": ["diseases", "scabies", "catarrh", "fever", "seasonality", "morbidity", "hospital statistics"],
    },
    "related": ["gesundheit-militaer-tauglichkeit-1864-1866"],
    "generated_by": GEN,
    "date": DATE,
}
write(ana)
