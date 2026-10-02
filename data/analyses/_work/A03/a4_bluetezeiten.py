"""Analysis 4: first flowering dates at Gera (1851-56) and Hohenleuben (1853-61) + tree stages at Gera (pp. 60-61),
related to the spring temperature at Hohenleuben (p. 56)."""
import re
import statistics as st
from common import *


def parse_date(s):
    s = s.strip()
    if s in ("—", ""):
        return None
    m = re.match(r"^(\d+)\.(?:-(\d+)\.)?/(\d+)\.?$", s)
    assert m, s
    assert m.group(2) is None, s
    return int(m.group(3)), int(m.group(1))  # month, day


KEYS = [  # (standard name, German, English)
    ("Viola odorata", "Märzveilchen", "Sweet violet"),
    ("Anemone nemorosa", "Buschwindröschen", "Wood anemone"),
    ("Ranunculus ficaria", "Scharbockskraut", "Lesser celandine"),
    ("Primula veris", "Echte Schlüsselblume", "Cowslip"),
    ("Ribes uva-crispa", "Stachelbeere", "Gooseberry"),
    ("Saxifraga granulata", "Körniger Steinbrech", "Meadow saxifrage"),
    ("Pyrus communis", "Birnbaum", "Pear"),
    ("Prunus domestica", "Pflaume", "Plum"),
    ("Prunus cerasus", "Sauerkirsche", "Sour cherry"),
    ("Malus domestica", "Apfelbaum", "Apple"),
    ("Crataegus", "Weißdorn", "Hawthorn"),
    ("Sambucus nigra", "Schwarzer Holunder", "Elder"),
    ("Vitis vinifera", "Weinrebe", "Grapevine"),
]
GERA_ORDER = list(range(12))              # same order as KEYS (no grapevine)
HOH_ORDER = list(range(13))

bloom = []        # long table
for station, bid, order in (("Gera", "b5", GERA_ORDER), ("Hohenleuben", "b7", HOH_ORDER)):
    g = grid("60", bid)
    years = [int(x.rstrip(".")) for x in g[0][1:-1]]
    rows = g[1:]
    assert len(rows) == len(order)
    for r, ki in zip(rows, order):
        key, de, en = KEYS[ki]
        for y, cell in zip(years, r[1:-1]):
            d = parse_date(cell)
            if d is None:
                continue
            mth, day = d
            bloom.append([station, key, r[0], de, en, y, f"{y}-{mth:02d}-{day:02d}", doy(mth, day), cell.strip()])

# ---- species summary --------------------------------------------------------------------
summary = []
for station, bid, order in (("Gera", "b5", GERA_ORDER), ("Hohenleuben", "b7", HOH_ORDER)):
    g = grid("60", bid)
    for r, ki in zip(g[1:], order):
        key, de, en = KEYS[ki]
        ds = [b[7] for b in bloom if b[0] == station and b[1] == key]
        summary.append([station, key, de, en, len(ds), min(ds), max(ds), round(st.mean(ds), 1), int(r[-1]), max(ds) - min(ds)])
mism = [(s[0], s[1], s[8], s[9]) for s in summary if s[8] != s[9]]
print("printed vs computed spread differs:", mism)

# ---- spring index -------------------------------------------------------------------------
def spring_index(station):
    sp = {}
    for b in bloom:
        if b[0] == station and b[1] != "Vitis vinifera":
            sp.setdefault(b[1], {})[b[5]] = b[7]
    mean = {k: st.mean(v.values()) for k, v in sp.items()}
    years = sorted({y for v in sp.values() for y in v})
    out = {}
    for y in years:
        dev = [v[y] - mean[k] for k, v in sp.items() if y in v]
        out[y] = (len(dev), st.mean(dev))
    return out

hm = {int(r[0]): [num(x) for x in r[1:13]] for r in grid("56", "b2")[1:9]}
spring_rows = []
for station in ("Gera", "Hohenleuben"):
    for y, (n, v) in spring_index(station).items():
        tmp = None
        if station == "Hohenleuben" and y in hm:
            tmp = round(st.mean(hm[y][2:5]) * R2C, 2)
        spring_rows.append([station, y, n, round(v, 2), tmp])
idx = {(r[0], r[1]): r[3] for r in spring_rows}
common = [y for y in range(1853, 1857) if ("Gera", y) in idx and ("Hohenleuben", y) in idx]
max_gap = max(abs(idx[("Gera", y)] - idx[("Hohenleuben", y)]) for y in common)
r_gh = st.correlation([idx[("Gera", y)] for y in common], [idx[("Hohenleuben", y)] for y in common])
print("common", common, max_gap, r_gh)

tmp_pts = [(r[4], r[3], r[1]) for r in spring_rows if r[0] == "Hohenleuben" and r[4] is not None]
xs, ys_ = [p[0] for p in tmp_pts], [p[1] for p in tmp_pts]
slope, icpt = st.linear_regression(xs, ys_)
r_t = st.correlation(xs, ys_)
print("temp relation", len(xs), slope, icpt, r_t)
x0, x1 = round(min(xs) - 0.3, 2), round(max(xs) + 0.3, 2)
trend_rows = [[x0, round(slope * x0 + icpt, 2), x1, round(slope * x1 + icpt, 2)]]

# Hohenleuben vs Gera for the same species and years 1853-56
pair = {}
for b in bloom:
    pair.setdefault((b[1], b[5]), {})[b[0]] = b[7]
dd = [v["Hohenleuben"] - v["Gera"] for (k, y), v in pair.items() if "Gera" in v and "Hohenleuben" in v and 1853 <= y <= 1856]
mean_diff = st.mean(dd)
n_pairs = len(dd)
elev_ft = (1012.5 - 552.5)  # midpoints of the height ranges (p. 12, 20), Prussian feet
schubler = 8 * elev_ft / 1000
print("diff", mean_diff, n_pairs, "schubler", schubler)

# index extremes
def ext(station):
    d = {y: v for (s, y), v in idx.items() if s == station}
    lo = min(d, key=d.get)
    hi = max(d, key=d.get)
    return lo, d[lo], hi, d[hi]
eg, eh = ext("Gera"), ext("Hohenleuben")
print(eg, eh)

# spread range
sp_calc = sorted(summary, key=lambda s: s[9])
lo_s, hi_s = sp_calc[0], sp_calc[-1]
print("spread min/max", lo_s, hi_s)

# ---- trees at Gera (p. 61 b2) ----------------------------------------------------------------
g61 = grid("61", "b2")
STAGES = [("leaf_bud", "Blattansatz", "Leaf bud"), ("flower_bud", "Blütenansatz", "Flower bud"), ("full_bloom", "Volle Blüte", "Full bloom"),
          ("first_fruit", "Erste Frucht", "First fruit"), ("leaf_fall", "Entblätterung", "Leaf fall")]
TREES = {"Roßkastanie": ("Rosskastanie", "Horse chestnut"), "Birnbaum": ("Birnbaum", "Pear tree")}
trees = []
for r in g61[1:]:
    de, en = TREES[r[0]]
    for i, (sk, sde, sen) in enumerate(STAGES):
        mth, day = parse_date(r[1 + i])
        trees.append([de, en, sk, sde, sen, i + 1, doy(mth, day), r[1 + i].strip()])
td = {(t[0], t[2]): t[6] for t in trees}
dur_k = td[("Rosskastanie", "leaf_fall")] - td[("Rosskastanie", "leaf_bud")]
dur_b = td[("Birnbaum", "leaf_fall")] - td[("Birnbaum", "leaf_bud")]
fruit_gap = td[("Rosskastanie", "first_fruit")] - td[("Birnbaum", "first_fruit")]
print(dur_k, dur_b, fruit_gap)

F, E = fde, fen
ana = {
    "id": "phaenologie-bluetezeiten-gera-hohenleuben-1851-1861",
    "title": bi("Blühtermine in Gera und Hohenleuben 1851–1861", "Flowering dates at Gera and Hohenleuben, 1851–1861"),
    "category": "phenology",
    "section": "t1-1-7",
    "sources": [
        {"page": "60", "block": "b3"},
        {"page": "60", "block": "b5", "rows": "r1-r13"},
        {"page": "60", "block": "b7", "rows": "r1-r14"},
        {"page": "61", "block": "b1"},
        {"page": "61", "block": "b2", "rows": "r1-r3"},
        {"page": "61", "block": "b3"},
        {"page": "56", "block": "b2", "rows": "r2-r9"},
        {"page": "12", "block": "b1", "rows": "r1", "note": "Höhe von Gera (505–600 Dezimalfuß)"},
        {"page": "20", "block": "b3", "rows": "r16", "note": "Höhe von Hohenleuben (975–1050 Dezimalfuß)"},
    ],
    "summary": bi(
        f"Auf S. 60 druckt Brückner die Tage des ersten Aufblühens von zwölf Pflanzen für Gera (1851–1856) und von zwölf bzw. dreizehn für Hohenleuben (1853–1861), jeweils mit der Spanne in Tagen; auf S. 61 folgen fünf Entwicklungsstufen von Rosskastanie und Birnbaum in Gera. Die Termine schwanken von Jahr zu Jahr um bis zu {F(eh[3]-eh[1],0)} Tage; Gera und Hohenleuben laufen im Gleichschritt, Hohenleuben im Mittel {F(mean_diff,1)} Tage später, und kalte Frühjahre bedeuten späte Blüte.",
        f"On p. 60 Brückner prints the days of first flowering of twelve plants for Gera (1851–1856) and of twelve or thirteen for Hohenleuben (1853–1861), each with the spread in days; p. 61 follows with five development stages of horse chestnut and pear at Gera. The dates vary from year to year by up to {E(eh[3]-eh[1],0)} days; Gera and Hohenleuben move in step, Hohenleuben on average {E(mean_diff,1)} days later, and cold springs mean late flowering."),
    "method": bi(
        "Die Brüche der Tabellen (»20./3.« = Tag/Monat, so erklärt auf S. 60) wurden in ISO-Daten umgesetzt; der Tag im Jahr wird in einem normierten Jahr ohne Schalttag gezählt (1. Januar = 1). Die lateinischen Namen sind im Druck teils abgekürzt (Hohenleuben) und werden hier vereinheitlicht und mit deutschen und englischen Namen versehen (editorische Deutung, z. B. Primula officinalis = Primula veris, Cerasus acida = Prunus cerasus, Ficaria verna = Ranunculus ficaria). Der Frühjahrsindex eines Jahres ist das Mittel der Abweichungen (in Tagen) der Blühtermine aller Arten außer der Weinrebe vom Mittel der jeweiligen Art an derselben Station; positive Werte bedeuten späte Blüte. Für den Vergleich mit der Temperatur wurde das Mittel von März bis Mai aus den Monatsmitteln von Hohenleuben (S. 56, °R × 1,25) gebildet, das Jahr 1853 entfällt (Temperaturreihe beginnt 1854). Die Trendgerade ist die lineare Regression des Index auf diese Frühjahrstemperatur. Die in der Tabelle gedruckten »Tage der Differenz« werden als eigene Spalte geführt und mit der Spanne der gedruckten Daten verglichen.",
        "The fractions of the tables (“20./3.” = day/month, as explained on p. 60) were converted to ISO dates; day of year is counted in a normalised year without a leap day (1 January = 1). The Latin names are partly abbreviated in the print (Hohenleuben) and are standardised here and given German and English names (editorial identification, e.g. Primula officinalis = Primula veris, Cerasus acida = Prunus cerasus, Ficaria verna = Ranunculus ficaria). A year’s spring index is the mean deviation (in days) of the flowering dates of all species except the grapevine from the mean of that species at the same station; positive values mean late flowering. For the comparison with temperature the March–May mean was formed from the monthly means of Hohenleuben (p. 56, °R × 1.25); 1853 is dropped (the temperature series begins in 1854). The trend line is the linear regression of the index on this spring temperature. The “days of difference” printed in the table are kept as a separate column and compared with the spread of the printed dates."),
    "findings": [
        bi(f"Der Frühjahrsindex schwankt von Jahr zu Jahr stark: in Gera von {F(eg[1],1)} Tagen ({eg[0]}) bis {F(eg[3],1)} Tage ({eg[2]}), in Hohenleuben von {F(eh[1],1)} Tagen ({eh[0]}) bis {F(eh[3],1)} Tage ({eh[2]}), also über rund drei Wochen.",
           f"The spring index varies strongly from year to year: at Gera from {E(eg[1],1)} days ({eg[0]}) to {E(eg[3],1)} days ({eg[2]}), at Hohenleuben from {E(eh[1],1)} days ({eh[0]}) to {E(eh[3],1)} days ({eh[2]}), i.e. over about three weeks."),
        bi(f"In den gemeinsamen Jahren 1853–1856 weichen die Indizes beider Stationen höchstens {F(max_gap,1)} Tage voneinander ab (r = {F(r_gh,2)}). Bei denselben Arten und Jahren blühte es in Hohenleuben im Mittel {F(mean_diff,1)} Tage später als in Gera ({n_pairs} Art-Jahr-Paare); Schüblers Regel von 8 Tagen je 1000 Fuß (S. 61) ergäbe für den Höhenunterschied der Ortslagen von rund {F(elev_ft,0)} Fuß (Höhenliste S. 12 und 20: Gera 505–600, Hohenleuben 975–1050) {F(schubler,1)} Tage.",
           f"In the common years 1853–1856 the indices of the two stations differ by at most {E(max_gap,1)} days (r = {E(r_gh,2)}). For the same species and years Hohenleuben flowered on average {E(mean_diff,1)} days later than Gera ({n_pairs} species-year pairs); Schübler’s rule of 8 days per 1000 feet (p. 61) would give {E(schubler,1)} days for the height difference of the two places of about {E(elev_ft,0)} feet (height list pp. 12 and 20: Gera 505–600, Hohenleuben 975–1050)."),
        bi(f"In Hohenleuben hängt der Index eng mit der Frühjahrstemperatur (März–Mai) zusammen: r = {F(r_t,2)} (acht Jahre), rund {F(-slope,1)} Tage früher je Kelvin Erwärmung. Das wärmste Frühjahr (1859) brachte die früheste, das kälteste (1855) eine späte Blüte.",
           f"At Hohenleuben the index is closely tied to spring temperature (March–May): r = {E(r_t,2)} (eight years), about {E(-slope,1)} days earlier per kelvin of warming. The warmest spring (1859) brought the earliest flowering, the coldest (1855) a late one."),
        bi(f"Die Spanne der Blühtermine einer Art über die Beobachtungsjahre reicht von {lo_s[9]} Tagen ({lo_s[2]}, {lo_s[0]}) bis {hi_s[9]} Tagen ({hi_s[2]}, {hi_s[0]}).",
           f"The spread of a species’ flowering dates over the observation years ranges from {lo_s[9]} days ({lo_s[3]}, {lo_s[0]}) to {hi_s[9]} days ({hi_s[3]}, {hi_s[0]})."),
        bi(f"Von der Blattknospe bis zur Entblätterung vergehen in Gera bei der Rosskastanie {dur_k} Tage, beim Birnbaum {dur_b} Tage; der Birnbaum zeigt seine erste Frucht {fruit_gap} Tage vor der Rosskastanie.",
           f"At Gera {dur_k} days pass from leaf bud to leaf fall in the horse chestnut and {dur_b} days in the pear; the pear shows its first fruit {fruit_gap} days before the horse chestnut."),
    ],
    "caveats": [
        bi("Die Termine sind »erstes Aufblühen«; Beobachter (Rob. und Rud. Schmidt), Standorte und Kriterien sind nicht näher beschrieben. Beide Reihen sind kurz (Gera 6, Hohenleuben 9 Jahre); Gera 1852 fehlt beim Veilchen, die Weinrebe wurde in Hohenleuben nur in vier Jahren notiert.",
           "The dates are “first flowering”; observers (Rob. and Rud. Schmidt), sites and criteria are not described. Both series are short (Gera 6, Hohenleuben 9 years); the violet is missing for Gera 1852, and the grapevine was recorded at Hohenleuben in four years only."),
        bi(f"In {len(mism)} der 25 Zeilen weicht die gedruckte »Tage der Differenz« um 1–3 Tage von der Spanne der gedruckten Daten ab ({'; '.join(f'{m[0]} {m[1]}: gedruckt {m[2]}, errechnet {m[3]}' for m in mism)}). Brückners Spalte beruht offenbar nicht durchweg auf den abgedruckten Daten; die Daten werden unverändert gezeigt.",
           f"In {len(mism)} of the 25 rows the printed “days of difference” departs by 1–3 days from the spread of the printed dates ({'; '.join(f'{m[0]} {m[1]}: printed {m[2]}, computed {m[3]}' for m in mism)}). Brückner’s column evidently does not rest throughout on the dates printed; the data are shown unchanged."),
        bi("Für den Weißdorn in Hohenleuben stehen 1858 der 3. Mai und 1860 der 2. Mai, vor der Apfelblüte (18. bzw. 15. Mai) – ungewöhnlich für diese spätere Art. Das Faksimile bestätigt die Zahlen; sie passen zur gedruckten Spanne von 35 Tagen und wurden beibehalten. Sie verzerren den Frühjahrsindex von Hohenleuben leicht.",
           "For hawthorn at Hohenleuben the 3rd of May in 1858 and the 2nd of May in 1860 precede apple blossom (18th and 15th of May) – unusual for this later species. The facsimile confirms the figures; they fit the printed spread of 35 days and were retained. They bias the Hohenleuben spring index slightly."),
        bi("Die Verbindung zur Temperatur stützt sich auf acht Jahre einer einzigen Station und ist explorativ; die Skala der Temperaturen (Réaumur) ist nicht ausdrücklich genannt (siehe Auswertung zu Gera). Die Tabelle der Entwicklungsstufen auf S. 61 nennt kein Jahr.",
           "The link to temperature rests on eight years of a single station and is exploratory; the temperature scale (Réaumur) is not stated explicitly (see the Gera analysis). The table of development stages on p. 61 names no year."),
    ],
    "conversions": [
        {"from": "Datumsbruch (Tag./Monat.)", "to": "ISO-Datum und Tag im Jahr", "factor_or_formula": "Tag im Jahr = Tage vor Monatsbeginn (Nicht-Schaltjahr) + Tag", "reference": "Erläuterung Brückner S. 60: Monat als Nenner, Tag als Zähler"},
        {"from": "Grad Réaumur (°R)", "to": "Grad Celsius (°C)", "factor_or_formula": "°C = °R × 1,25", "reference": "von Brückner nicht tabelliert"},
    ],
    "datasets": [
        {"name": "bloom", "title": bi("Termine des ersten Aufblühens", "Dates of first flowering"),
         "columns": [
             {"name": "station", "label": bi("Station", "Station"), "type": "string", "unit": None},
             {"name": "species", "label": bi("Art (vereinheitlicht)", "Species (standardised)"), "type": "string", "unit": None},
             {"name": "species_printed", "label": bi("Name im Druck", "Name as printed"), "type": "string", "unit": None},
             {"name": "species_de", "label": bi("Deutscher Name", "German name"), "type": "string", "unit": None},
             {"name": "species_en", "label": bi("Englischer Name", "English name"), "type": "string", "unit": None},
             {"name": "year", "label": YEAR, "type": "integer", "unit": None},
             {"name": "date", "label": bi("Datum", "Date"), "type": "date", "unit": None, "derived": True, "note": "ISO-Datum aus dem gedruckten Bruch Tag./Monat."},
             {"name": "doy", "label": bi("Tag im Jahr", "Day of year"), "type": "integer", "unit": "d", "derived": True, "note": "normiertes Jahr ohne Schalttag"},
             {"name": "printed", "label": bi("Gedruckt", "As printed"), "type": "string", "unit": None},
         ],
         "rows": bloom, "source_refs": [{"page": "60", "block": "b5", "rows": "r2-r13"}, {"page": "60", "block": "b7", "rows": "r2-r14"}]},
        {"name": "species_summary", "title": bi("Spanne der Blühtermine je Art und Station", "Spread of flowering dates by species and station"),
         "columns": [
             {"name": "station", "label": bi("Station", "Station"), "type": "string", "unit": None},
             {"name": "species", "label": bi("Art (vereinheitlicht)", "Species (standardised)"), "type": "string", "unit": None},
             {"name": "species_de", "label": bi("Deutscher Name", "German name"), "type": "string", "unit": None},
             {"name": "species_en", "label": bi("Englischer Name", "English name"), "type": "string", "unit": None},
             {"name": "n_years", "label": bi("Zahl der Jahre", "Number of years"), "type": "integer", "unit": None, "derived": True},
             {"name": "earliest_doy", "label": bi("Frühester Termin (Tag im Jahr)", "Earliest date (day of year)"), "type": "integer", "unit": "d", "derived": True},
             {"name": "latest_doy", "label": bi("Spätester Termin (Tag im Jahr)", "Latest date (day of year)"), "type": "integer", "unit": "d", "derived": True},
             {"name": "mean_doy", "label": bi("Mittlerer Termin (Tag im Jahr)", "Mean date (day of year)"), "type": "number", "unit": "d", "derived": True},
             {"name": "spread_printed", "label": bi("Tage der Differenz (gedruckt)", "Days of difference (printed)"), "type": "integer", "unit": "d"},
             {"name": "spread_computed", "label": bi("Spanne der gedruckten Daten", "Spread of the printed dates"), "type": "integer", "unit": "d", "derived": True},
         ],
         "rows": summary, "source_refs": [{"page": "60", "block": "b5", "rows": "r2-r13"}, {"page": "60", "block": "b7", "rows": "r2-r14"}]},
        {"name": "spring", "title": bi("Frühjahrsindex und Frühjahrstemperatur", "Spring index and spring temperature"),
         "columns": [
             {"name": "station", "label": bi("Station", "Station"), "type": "string", "unit": None},
             {"name": "year", "label": YEAR, "type": "integer", "unit": None},
             {"name": "n_species", "label": bi("Zahl der Arten", "Number of species"), "type": "integer", "unit": None, "derived": True},
             {"name": "index_days", "label": bi("Frühjahrsindex (Tage, + = spät)", "Spring index (days, + = late)"), "type": "number", "unit": "d", "derived": True},
             {"name": "temp_mar_may_c", "label": bi("Temperatur März–Mai (Hohenleuben)", "Temperature March–May (Hohenleuben)"), "type": "number", "unit": "°C", "derived": True, "note": "Mittel der Monatsmittel S. 56, °R × 1,25"},
         ],
         "rows": spring_rows, "source_refs": [{"page": "60", "block": "b5", "rows": "r2-r13"}, {"page": "60", "block": "b7", "rows": "r2-r14"}, {"page": "56", "block": "b2", "rows": "r2-r9"}]},
        {"name": "trend", "title": bi("Trendgerade Index–Temperatur", "Index–temperature trend line"),
         "columns": [
             {"name": "x0", "label": bi("Temperatur Anfang", "Temperature start"), "type": "number", "unit": "°C", "derived": True},
             {"name": "y0", "label": bi("Index Anfang", "Index start"), "type": "number", "unit": "d", "derived": True},
             {"name": "x1", "label": bi("Temperatur Ende", "Temperature end"), "type": "number", "unit": "°C", "derived": True},
             {"name": "y1", "label": bi("Index Ende", "Index end"), "type": "number", "unit": "d", "derived": True},
         ],
         "rows": trend_rows, "source_refs": [{"page": "56", "block": "b2", "rows": "r2-r9"}]},
        {"name": "trees", "title": bi("Entwicklungsstufen von Rosskastanie und Birnbaum in Gera", "Development stages of horse chestnut and pear at Gera"),
         "columns": [
             {"name": "tree_de", "label": bi("Baum (deutsch)", "Tree (German)"), "type": "string", "unit": None},
             {"name": "tree_en", "label": bi("Baum (englisch)", "Tree (English)"), "type": "string", "unit": None},
             {"name": "stage", "label": bi("Stufe (Kennung)", "Stage (key)"), "type": "string", "unit": None},
             {"name": "stage_de", "label": bi("Stufe (deutsch)", "Stage (German)"), "type": "string", "unit": None},
             {"name": "stage_en", "label": bi("Stufe (englisch)", "Stage (English)"), "type": "string", "unit": None},
             {"name": "stage_no", "label": bi("Reihenfolge der Stufe", "Stage order"), "type": "integer", "unit": None, "derived": True},
             {"name": "doy", "label": bi("Tag im Jahr", "Day of year"), "type": "integer", "unit": "d", "derived": True, "note": "normiertes Jahr ohne Schalttag"},
             {"name": "printed", "label": bi("Gedruckt", "As printed"), "type": "string", "unit": None},
         ],
         "rows": trees, "source_refs": [{"page": "61", "block": "b2", "rows": "r2-r3"}]},
    ],
}

# ---- charts -------------------------------------------------------------------------------------
order_sp = [s[1] for s in sorted({(k, st.mean(b[7] for b in bloom if b[1] == k)) for k in {b[1] for b in bloom}}, key=lambda t: t[1])]
order_sp = sorted({b[1] for b in bloom}, key=lambda k: st.mean(b[7] for b in bloom if b[1] == k))
name_of = {k: (de, en) for k, de, en in KEYS}
sort_sp = [bi(name_of[k][0], name_of[k][1]) for k in order_sp]
sp_expr = bi("datum.species_de", "datum.species_en")
x_doy = lambda: {"field": "doy", "type": "quantitative", "title": bi("Tag des ersten Aufblühens", "Day of first flowering"), "axis": doy_axis(3, 7), "scale": {"domain": [70, 196], "nice": False}}
y_sp = {"field": "sp", "type": "nominal", "title": None, "sort": sort_sp}
ST = ["Gera", "Hohenleuben"]
col_st = {"field": "station", "type": "nominal", "title": None, "scale": {"domain": ST}}

c1 = {"id": "c1", "dataset": "bloom",
      "title": bi("Termine des ersten Aufblühens je Art", "Dates of first flowering by species"),
      "caption": bi("Jeder Punkt ist ein Jahr, der Strich die Spanne zwischen frühestem und spätestem Termin der Station. Arten nach mittlerem Termin geordnet; Gera 1851–1856, Hohenleuben 1853–1861.",
                    "Each dot is one year, the line the span between the earliest and latest date at the station. Species ordered by mean date; Gera 1851–1856, Hohenleuben 1853–1861."),
      "vegalite": {
          "height": 520,
          "transform": [{"calculate": sp_expr, "as": "sp"}],
          "layer": [
              {"transform": [{"aggregate": [{"op": "min", "field": "doy", "as": "lo"}, {"op": "max", "field": "doy", "as": "hi"}], "groupby": ["station", "sp"]}],
               "mark": {"type": "rule", "strokeWidth": 2, "opacity": 0.6},
               "encoding": {"x": {"field": "lo", "type": "quantitative", "title": bi("Tag des ersten Aufblühens", "Day of first flowering"), "axis": doy_axis(3, 7), "scale": {"domain": [70, 196], "nice": False}}, "x2": {"field": "hi"},
                            "y": y_sp, "yOffset": {"field": "station"}, "color": col_st}},
              {"mark": {"type": "circle", "size": 55, "opacity": 0.9},
               "encoding": {"x": x_doy(), "y": y_sp, "yOffset": {"field": "station"}, "color": col_st,
                            "tooltip": [tip("station", "Station", "Station"), tip("species_printed", "Name im Druck", "Name as printed"), tip("species", "Art", "Species"),
                                        tip("year", "Jahr", "Year"), tip("printed", "Gedruckt (Tag./Monat.)", "Printed (day./month.)"), tip("date", "Datum", "Date")]}},
          ]}}

c2 = {"id": "c2", "dataset": "spring",
      "title": bi("Frühjahrsindex je Jahr", "Spring index by year"),
      "caption": bi("Mittlere Abweichung der Blühtermine vom Mittel der jeweiligen Art, in Tagen (+ = später, − = früher). 1853–1856 sind beide Stationen fast deckungsgleich; 1853 und 1855 waren späte, 1859 und 1851 frühe Jahre.",
                    "Mean deviation of the flowering dates from the mean of the species, in days (+ = later, − = earlier). In 1853–1856 the two stations almost coincide; 1853 and 1855 were late years, 1859 and 1851 early ones."),
      "vegalite": {
          "height": 300,
          "layer": [
              {"mark": {"type": "bar"},
               "encoding": {"x": {"field": "year", "type": "ordinal", "title": YEAR, "axis": {"labelAngle": 0}},
                            "xOffset": {"field": "station"},
                            "y": {"field": "index_days", "type": "quantitative", "title": bi("Abweichung (Tage)", "Deviation (days)")},
                            "color": col_st,
                            "tooltip": [tip("station", "Station", "Station"), tip("year", "Jahr", "Year"), tip("n_species", "Zahl der Arten", "Number of species"), tip("index_days", "Index (Tage)", "Index (days)", "+.1f")]}},
              {"mark": {"type": "rule"}, "encoding": {"y": {"datum": 0}}},
          ]}}

c3 = {"id": "c3", "dataset": "spring", "extra_datasets": ["trend"],
      "title": bi("Blüte und Frühjahrstemperatur in Hohenleuben", "Flowering and spring temperature at Hohenleuben"),
      "caption": bi(f"Je Jahr 1854–1861: Mittel der Monatsmittel März–Mai (°C) gegen den Frühjahrsindex der Blüte. Je wärmer das Frühjahr, desto früher die Blüte (r = {F(r_t,2)}, acht Punkte; die Gerade ist die Regression).",
                    f"For each year 1854–1861: mean of the monthly means March–May (°C) against the spring index of flowering. The warmer the spring, the earlier the flowering (r = {E(r_t,2)}, eight points; the line is the regression)."),
      "vegalite": {
          "height": 320,
          "layer": [
              {"data": {"name": "trend"}, "mark": {"type": "rule", "strokeDash": [5, 4]},
               "encoding": {"x": {"field": "x0", "type": "quantitative", "scale": {"domain": [5.6, 9.2]}}, "x2": {"field": "x1"},
                            "y": {"field": "y0", "type": "quantitative", "scale": {"domain": [-14, 16]}}, "y2": {"field": "y1"}}},
              {"transform": [{"filter": "datum.station == 'Hohenleuben' && isValid(datum.temp_mar_may_c)"}],
               "mark": {"type": "circle", "size": 110, "opacity": 1},
               "encoding": {"x": {"field": "temp_mar_may_c", "type": "quantitative", "title": bi("Mitteltemperatur März–Mai (°C)", "Mean temperature March–May (°C)"), "scale": {"domain": [5.6, 9.2]}},
                            "y": {"field": "index_days", "type": "quantitative", "title": bi("Frühjahrsindex der Blüte (Tage)", "Spring index of flowering (days)"), "scale": {"domain": [-14, 16]}},
                            "tooltip": [tip("year", "Jahr", "Year"), tip("temp_mar_may_c", "März–Mai (°C)", "March–May (°C)", ".1f"), tip("index_days", "Index (Tage)", "Index (days)", "+.1f")]}},
              {"transform": [{"filter": "datum.station == 'Hohenleuben' && isValid(datum.temp_mar_may_c)"}],
               "mark": {"type": "text", "align": "left", "dx": 9, "dy": -7, "fontSize": 11},
               "encoding": {"x": {"field": "temp_mar_may_c", "type": "quantitative"}, "y": {"field": "index_days", "type": "quantitative"}, "text": {"field": "year", "type": "ordinal"}}},
          ]}}

stage_expr = bi("datum.stage == 'leaf_bud' ? 'Blattansatz' : datum.stage == 'flower_bud' ? 'Blütenansatz' : datum.stage == 'full_bloom' ? 'Volle Blüte' : datum.stage == 'first_fruit' ? 'Erste Frucht' : 'Entblätterung'",
                "datum.stage == 'leaf_bud' ? 'Leaf bud' : datum.stage == 'flower_bud' ? 'Flower bud' : datum.stage == 'full_bloom' ? 'Full bloom' : datum.stage == 'first_fruit' ? 'First fruit' : 'Leaf fall'")
stage_dom = [bi(a, b) for _, a, b in STAGES]
tree_expr = bi("datum.tree_de", "datum.tree_en")
y_tree = {"field": "tree", "type": "nominal", "title": None, "sort": [bi("Rosskastanie", "Horse chestnut"), bi("Birnbaum", "Pear tree")]}
x_stage = lambda: {"field": "doy", "type": "quantitative", "title": bi("Tag im Jahr", "Day of year"), "axis": doy_axis(4, 11), "scale": {"domain": [100, 315], "nice": False}}
c4 = {"id": "c4", "dataset": "trees",
      "title": bi("Entwicklungsstufen von Rosskastanie und Birnbaum in Gera", "Development stages of horse chestnut and pear at Gera"),
      "caption": bi("Gera, Jahr nicht genannt. Der Birnbaum blüht früher als die Rosskastanie und zeigt schon Ende August die erste Frucht, die Rosskastanie erst Anfang Oktober; beide verlieren ihr Laub im Oktober.",
                    "Gera, year not stated. The pear blooms earlier than the horse chestnut and shows its first fruit at the end of August, the horse chestnut only at the beginning of October; both lose their leaves in October."),
      "vegalite": {
          "height": 200,
          "transform": [{"calculate": tree_expr, "as": "tree"}, {"calculate": stage_expr, "as": "stage_name"}],
          "layer": [
              {"transform": [{"aggregate": [{"op": "min", "field": "doy", "as": "lo"}, {"op": "max", "field": "doy", "as": "hi"}], "groupby": ["tree"]}],
               "mark": {"type": "rule", "strokeWidth": 2, "opacity": 0.6},
               "encoding": {"x": {"field": "lo", "type": "quantitative", "title": bi("Tag im Jahr", "Day of year"), "axis": doy_axis(4, 11), "scale": {"domain": [100, 315], "nice": False}}, "x2": {"field": "hi"}, "y": y_tree}},
              {"mark": {"type": "circle", "size": 160, "opacity": 1},
               "encoding": {"x": x_stage(), "y": y_tree,
                            "color": {"field": "stage_name", "type": "nominal", "title": None, "scale": {"domain": stage_dom}, "legend": {"columns": 3}},
                            "tooltip": [tip("tree", "Baum", "Tree"), tip("stage_name", "Stufe", "Stage"), tip("printed", "Gedruckt (Tag./Monat.)", "Printed (day./month.)"), tip("doy", "Tag im Jahr", "Day of year")]}},
          ]}}

ana["charts"] = [c1, c2, c3, c4]
ana["keywords"] = bi(["Phänologie", "Blüte", "Blühtermin", "Gera", "Hohenleuben", "Veilchen", "Buschwindröschen", "Obstbaumblüte", "Schlüsselblume", "Rosskastanie", "Birnbaum", "Frühjahr", "Vegetation"],
                     ["phenology", "flowering", "flowering date", "Gera", "Hohenleuben", "violet", "wood anemone", "fruit tree blossom", "cowslip", "horse chestnut", "pear", "spring", "vegetation"])
ana["related"] = ["klima-stationen-temperatur-vergleich", "phaenologie-zugvoegel-gera-1859-1864"]
ana["generated_by"] = "Claude Sonnet 5.5 (subagent A03)"
ana["date"] = "2026-10-01"
write(ana)
