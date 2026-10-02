"""Analysis 2: temperature at the stations Gera, Hohenleuben, Schleiz, Rothenacker (+ Ziegenrueck, Lobenstein, Saalburg), pp. 55-58."""
import re
import statistics as st
from common import *


def rows_by_year(label, bid, ncol, first=1):
    out = {}
    for r in grid(label, bid)[first:]:
        k = r[0].strip()
        out[k] = [num(x) for x in r[1:1 + ncol]]
    return out


STATIONS = ["Gera", "Hohenleuben", "Schleiz", "Rothenacker", "Ziegenrück", "Lobenstein", "Saalburg"]

monthly_src = {
    "Gera": rows_by_year("55", "b7", 12),
    "Hohenleuben": rows_by_year("56", "b2", 12),
    "Schleiz": rows_by_year("56", "b5", 12),
    "Rothenacker": rows_by_year("57", "b2", 12),
}
# Rothenacker "Mittel" row: minus sign lost in transcription for March (checked on facsimile) -> not used (we recompute means)
zie = rows_by_year("57", "b6", 12)["1848 bis 1856"]

# Lobenstein (1863) and Saalburg (Dec 1864 - Nov 1865), p. 58 b2
g58 = grid("58", "b2")
lob = [num(g58[i][1]) for i in range(2, 14)]            # r3..r14 -> Jan..Dec 1863
saal_dec64 = num(g58[1][2])                              # r2 col3
saal_1865 = [num(g58[i][2]) for i in range(2, 13)]       # r3..r13 -> Jan..Nov 1865
lob_annual = num(g58[14][1])
saal_annual = num(g58[14][2])
saal_max = num(re.search(r"([\d,]+)", g58[13][2]).group(1))
saal_min = num("-" + re.search(r"([\d,]+)", g58[13][3]).group(1))
assert (lob_annual, saal_annual, saal_max, saal_min) == (6.90, 7.66, 25.0, -17.2), (lob_annual, saal_annual, saal_max, saal_min)
assert abs(st.mean(lob) - lob_annual) < 0.006 and abs(st.mean([saal_dec64] + saal_1865) - saal_annual) < 0.006

PERIOD = {"Gera": "1856–1867", "Hohenleuben": "1854–1861", "Schleiz": "1863–1867", "Rothenacker": "1865, 1867",
          "Ziegenrück": "1848–1856", "Lobenstein": "1863", "Saalburg": "Dez. 1864–Nov. 1865"}

monthly_rows = []
GERA = {(int(y), j + 1): v for y, vals in monthly_src["Gera"].items() if y.isdigit() for j, v in enumerate(vals)}
SERIES_ORDER = ["Hohenleuben", "Schleiz", "Rothenacker", "Lobenstein", "Saalburg"]


def add_month(station, year, m, v, n):
    if v is None:
        return
    g = GERA.get((year, m)) if station != "Gera" and year is not None else None
    if station == "Saalburg":
        label = "Saalburg 1864/65"
    elif station in ("Hohenleuben",):
        label = f"{station} {year}" if year is not None and year <= 1861 and (year, m) in GERA else None
    else:
        label = f"{station} {year}" if year is not None else None
    if g is None or label is None:
        label = None
        diff = None
    else:
        diff = round((v - g) * R2C, 2)
    order = None if label is None else SERIES_ORDER.index(station) * 10000 + (year or 0)
    monthly_rows.append([station, PERIOD[station], n, year, m, MONTHS_PRINT[m - 1], v, r2c(v), label, order, diff])


for stn in ["Gera", "Hohenleuben", "Schleiz", "Rothenacker"]:
    d = monthly_src[stn]
    years = [k for k in d if k.isdigit()]
    for y in years:
        for j in range(12):
            add_month(stn, int(y), j + 1, d[y][j], len(years))
for j in range(12):
    add_month("Ziegenrück", None, j + 1, zie[j], 9)
for j in range(12):
    add_month("Lobenstein", 1863, j + 1, lob[j], 1)
add_month("Saalburg", 1864, 12, saal_dec64, 1)
for j in range(11):
    add_month("Saalburg", 1865, j + 1, saal_1865[j], 1)

# ---- annual table -----------------------------------------------------------
annual_rows = []


def add_annual(stn, d):
    for k, v in d.items():
        if not k.isdigit():
            continue
        s, w, hi, lo, a = v
        annual_rows.append([stn, int(k), s, w, hi, lo, a, r2c(s), r2c(w), r2c(hi), r2c(lo), r2c(a)])


add_annual("Gera", rows_by_year("55", "b9", 5))
add_annual("Hohenleuben", rows_by_year("56", "b3", 5))
add_annual("Schleiz", rows_by_year("56", "b6", 5))
add_annual("Ziegenrück", rows_by_year("57", "b8", 5))

# ---- station summary (printed Durchschnitt rows) ---------------------------------
def printed_avg(label, bid, key):
    r = rows_by_year(label, bid, 5)[key]
    return r[0], r[1], r[4]


b3 = block("57", "b3")["text"]
rot_s, rot_w, rot_a = [num(x) for x in re.findall(r"(\d+,\d+)", b3)][:3]
summary_src = {
    "Gera": printed_avg("55", "b9", "Durchschnitt"),
    "Hohenleuben": printed_avg("56", "b3", "Durchschnitt"),
    "Schleiz": printed_avg("56", "b6", "Durchschnitt"),
    "Rothenacker": (rot_s, rot_w, rot_a),
    "Ziegenrück": printed_avg("57", "b8", "Durchschnitt"),
}
NYEARS = {"Gera": 12, "Hohenleuben": 7, "Schleiz": 5, "Rothenacker": 2, "Ziegenrück": 8}
summary_rows = []
for stn in STATIONS:
    if stn in summary_src:
        s, w, a = summary_src[stn]
        summary_rows.append([stn, PERIOD[stn], s, w, a, r2c(s), r2c(w), r2c(a)])
    elif stn == "Lobenstein":
        summary_rows.append([stn, PERIOD[stn], None, None, lob_annual, None, None, r2c(lob_annual)])
    else:
        summary_rows.append([stn, PERIOD[stn], None, None, saal_annual, None, None, r2c(saal_annual)])
print(summary_src)

# ---- statistics ------------------------------------------------------------------
A = {(r[0], r[1]): r for r in annual_rows}
def diffs(a, b):
    ys = sorted(y for (s, y) in A if s == a and (b, y) in A and A[(a, y)][6] is not None and A[(b, y)][6] is not None)
    return ys, [(A[(a, y)][6] - A[(b, y)][6]) * R2C for y in ys]

ys_h, d_h = diffs("Gera", "Hohenleuben")
ys_s, d_s = diffs("Gera", "Schleiz")
print(ys_h, d_h, ys_s, d_s)
ann_c = {r[0]: r[7] for r in summary_rows}
def cyc(stn):
    rows = [r for r in monthly_rows if r[0] == stn]
    mm = [st.mean(r[6] for r in rows if r[4] == m) for m in range(1, 13)]
    return mm
amp = {s: (max(cyc(s)) - min(cyc(s))) * R2C for s in ["Gera", "Hohenleuben", "Schleiz"]}
print(amp)
# Rothenacker vs Gera in the same years
def yr_mean(stn, y):
    return st.mean(r[6] for r in monthly_rows if r[0] == stn and r[3] == y)
rot_g = {y: (yr_mean("Rothenacker", y) - yr_mean("Gera", y)) * R2C for y in (1865, 1867)}
sch_g = {y: (yr_mean("Schleiz", y) - yr_mean("Gera", y)) * R2C for y in (1865, 1867)}
print(rot_g, sch_g)
# implied December of Ziegenrueck
zs, zw, za = summary_src["Ziegenrück"]
summer_calc = st.mean(zie[3:9])
dec_implied = zw * 6 - (zie[9] + zie[10] + zie[0] + zie[1] + zie[2])
print("Ziegenrück summer calc", summer_calc, "dec implied", dec_implied, "annual calc", st.mean(zie))
zie_year_means = [v for k, v in [(r[1], r[6]) for r in annual_rows if r[0] == "Ziegenrück"] if v is not None]
assert abs(st.mean(zie_year_means) - za) < 0.01

F, E = fde, fen
gera_c, schl_c, hoh_c, rot_c, zie_c = (ann_c[s] for s in ["Gera", "Schleiz", "Hohenleuben", "Rothenacker", "Ziegenrück"])
sch_vs_gera_k = st.mean(d_s)
n_sch_warmer = sum(1 for x in d_s if x < 0)
dh_m = (1162.5 - 552.5) * 0.3766242  # midpoints of the height ranges (p. 12, 20), 1 Dezimalfuß = 0.3766242 m
assert all(x > 0 for x in d_h) and n_sch_warmer == 3 and len(d_s) == 5
hoh_vs_gera_k = st.mean(d_h)

ana = {
    "id": "klima-stationen-temperatur-vergleich",
    "title": bi("Temperatur an den Messstationen des Landes im Vergleich", "Temperature at the country's observing stations compared"),
    "category": "climate",
    "section": "t1-1-7",
    "sources": [
        {"page": "55", "block": "b7", "rows": "r2-r14"},
        {"page": "55", "block": "b9", "rows": "r2-r14"},
        {"page": "56", "block": "b2", "rows": "r2-r10"},
        {"page": "56", "block": "b3", "rows": "r2-r9"},
        {"page": "56", "block": "b5", "rows": "r2-r7"},
        {"page": "56", "block": "b6", "rows": "r2-r7"},
        {"page": "57", "block": "b2", "rows": "r2-r4"},
        {"page": "57", "block": "b3"},
        {"page": "57", "block": "b6", "rows": "r2"},
        {"page": "57", "block": "b8", "rows": "r2-r11"},
        {"page": "57", "block": "fn1"},
        {"page": "58", "block": "b2", "rows": "r2-r15"},
        {"page": "58", "block": "b3"},
        {"page": "12", "block": "b1", "rows": "r1", "note": "Höhe von Gera (505–600 Dezimalfuß)"},
        {"page": "20", "block": "b3", "rows": "r29", "note": "Höhe von Schleiz (1150–1175 Dezimalfuß)"},
        {"page": "70", "block": "b1", "note": "Hinweis auf die Réaumur-Skala (»5 1/2° R.«)"},
    ],
    "summary": bi(
        f"Neben Gera (12 Jahre) führt Brückner Thermometerreihen für Hohenleuben (1854–1861), Schleiz (1863–1867) und Rothenacker (1865, 1867) an, zur Vergleichung auch für das preußische Ziegenrück (1848–1856), außerdem je ein Jahr für Lobenstein und Saalburg. Umgerechnet in °C liegt das Jahresmittel in Gera bei {F(gera_c)} °C, in Hohenleuben bei {F(hoh_c)} °C und in Ziegenrück bei {F(zie_c)} °C; Schleiz ({F(schl_c)} °C) erscheint nicht kühler als Gera. Die Diagramme zeigen den mittleren Jahresgang, Sommer-, Winter- und Jahresmittel, die Jahresmittel der einzelnen Jahre und die Monatsreihen derselben Jahre an verschiedenen Orten.",
        f"Besides Gera (12 years) Brückner gives thermometer series for Hohenleuben (1854–1861), Schleiz (1863–1867) and Rothenacker (1865, 1867), for comparison also for Prussian Ziegenrück (1848–1856), and one year each for Lobenstein and Saalburg. Converted to °C the annual mean is {E(gera_c)} °C at Gera, {E(hoh_c)} °C at Hohenleuben and {E(zie_c)} °C at Ziegenrück; Schleiz ({E(schl_c)} °C) appears no cooler than Gera. The charts show the mean annual cycle, summer, winter and annual means, the annual means of the individual years, and the monthly series of the same years at different places."),
    "method": bi(
        "Aus den Tabellen auf S. 55–58 wurden die Monatsmittel (Réaumur) aller Stationen und Jahre übernommen, ferner die gedruckten Jahres-, Sommer- und Wintermittel je Jahr (Gera, Hohenleuben, Schleiz, Ziegenrück) sowie die gedruckten Durchschnittszeilen. Für Rothenacker nennt der Text nur die gemeinsamen Mittel der Jahre 1865 und 1867. Umrechnung °C = °R × 1,25. Der mittlere Jahresgang (Abb. 1) ist das ungewichtete Mittel der Monatswerte aller gedruckten Jahre der Station (Hohenleuben: 1854–1861 mit lückenhaftem Jahr 1861; Ziegenrück: gedrucktes 9-Jahres-Mittel); Brückners gedruckte Mittelzeilen weichen davon höchstens um 0,03 °R ab, mit einer Ausnahme (Rothenacker, März, siehe Transkriptionsprobleme). Die Station Saalburg beginnt im Dezember 1864 und läuft bis November 1865; ihr Dezemberwert (1864) wird in Abb. 4 nicht gezeigt. Sommer = April–September, Winter = Oktober–März (S. 55). Vergleiche zwischen Stationen betreffen nur Jahre, in denen beide Stationen gedruckt sind.",
        "The monthly means (Réaumur) of all stations and years were taken from the tables on pp. 55–58, together with the printed annual, summer and winter means per year (Gera, Hohenleuben, Schleiz, Ziegenrück) and the printed average rows. For Rothenacker the text gives only the joint means of 1865 and 1867. Conversion °C = °R × 1.25. The mean annual cycle (chart 1) is the unweighted mean of the monthly values of all printed years of a station (Hohenleuben: 1854–1861 with the incomplete year 1861; Ziegenrück: the printed 9-year mean); Brückner’s printed mean rows differ from it by 0.03 °R at most, with one exception (Rothenacker, March, see transcription issues). The Saalburg series runs from December 1864 to November 1865; its December value (1864) is not shown in chart 4. Summer = April–September, winter = October–March (p. 55). Comparisons between stations use only years printed for both stations."),
    "findings": [
        bi(f"Die Jahresmittel fallen in der Reihenfolge Gera ({F(gera_c)} °C), Schleiz ({F(schl_c)} °C), Hohenleuben ({F(hoh_c)} °C), Rothenacker ({F(rot_c)} °C), Ziegenrück ({F(zie_c)} °C); die Beobachtungszeiträume sind verschieden.",
           f"The annual means fall in the order Gera ({E(gera_c)} °C), Schleiz ({E(schl_c)} °C), Hohenleuben ({E(hoh_c)} °C), Rothenacker ({E(rot_c)} °C), Ziegenrück ({E(zie_c)} °C); the observation periods differ."),
        bi(f"In den gemeinsamen Jahren 1856–1860 war Gera im Jahresmittel um {F(hoh_vs_gera_k,2)} K wärmer als Hohenleuben (in allen fünf Jahren wärmer, Spanne {F(min(d_h),2)}–{F(max(d_h),2)} K).",
           f"In the common years 1856–1860 Gera was {E(hoh_vs_gera_k,2)} K warmer than Hohenleuben on annual average (warmer in all five years, range {E(min(d_h),2)}–{E(max(d_h),2)} K)."),
        bi(f"1863–1867 war Schleiz im Jahresmittel im Durchschnitt um {F(-sch_vs_gera_k,2)} K wärmer als Gera (in drei von fünf Jahren wärmer). Bei einer um rund {F(dh_m,0)} m höheren Lage (S. 12 und 20: Gera 505–600, Schleiz 1150–1175 Dezimalfuß) ist das unplausibel; Brückner selbst nennt die Angaben von Schleiz »zu hoch liegend« (S. 58).",
           f"In 1863–1867 Schleiz was on average {E(-sch_vs_gera_k,2)} K warmer than Gera on annual mean (warmer in three of five years). For a site about {E(dh_m,0)} m higher (pp. 12 and 20: Gera 505–600, Schleiz 1150–1175 decimal feet) this is implausible; Brückner himself calls the Schleiz figures “too high” (p. 58)."),
        bi(f"Rothenacker lag 1865 im Mittel {F(-rot_g[1865],2)} K, 1867 aber {F(-rot_g[1867],2)} K unter Gera; Schleiz weicht in beiden Jahren nur wenig von Gera ab ({F(sch_g[1865],2).replace('0,','+0,') if sch_g[1865] > 0 else F(sch_g[1865],2)} bzw. {F(sch_g[1867],2)} K).",
           f"Rothenacker was {E(-rot_g[1865],2)} K below Gera on average in 1865 but {E(-rot_g[1867],2)} K in 1867; Schleiz departs only slightly from Gera in both years ({E(sch_g[1865],2)} and {E(sch_g[1867],2)} K)."),
        bi(f"Der mittlere Jahresgang hat in Hohenleuben eine größere Amplitude ({F(amp['Hohenleuben'])} K) als in Gera ({F(amp['Gera'])} K) und Schleiz ({F(amp['Schleiz'])} K); die Zeiträume sind jedoch kurz und verschieden.",
           f"The mean annual cycle has a larger amplitude at Hohenleuben ({E(amp['Hohenleuben'])} K) than at Gera ({E(amp['Gera'])} K) and Schleiz ({E(amp['Schleiz'])} K); the periods are, however, short and different."),
    ],
    "caveats": [
        bi("Temperaturskala nicht ausdrücklich genannt; Annahme Grad Réaumur (siehe S. 70, »° R.«), Umrechnung ×1,25. Gilt für alle Stationen.",
           "Temperature scale not stated explicitly; assumed to be degrees Réaumur (see p. 70, “° R.”), conversion ×1.25. This holds for all stations."),
        bi("Die Stationen haben verschiedene, kurze und teils nicht überlappende Beobachtungszeiträume (Rothenacker nur 2 Jahre, Lobenstein und Saalburg je 1 Jahr, Ziegenrück vor 1857). Unterschiede zwischen Mitteln verschiedener Zeiträume mischen Standort und Witterung; belastbarer sind nur die Vergleiche gleicher Jahre (Abb. 3 und 4).",
           "The stations have different, short and partly non-overlapping observation periods (Rothenacker only 2 years, Lobenstein and Saalburg one year each, Ziegenrück before 1857). Differences between means of different periods mix location and weather; only the same-year comparisons (charts 3 and 4) are more robust."),
        bi("Brückner hält die Werte von Schleiz, Rothenacker, Lobenstein und Saalburg im Vergleich mit Ziegenrück und Hohenleuben und gemessen an der Vegetation für zu hoch (S. 58); Instrumenttyp, Aufstellung und Beobachtungstermine sind nirgends angegeben.",
           "Brückner considers the values of Schleiz, Rothenacker, Lobenstein and Saalburg too high compared with Ziegenrück and Hohenleuben and judged by vegetation (p. 58); instrument type, exposure and observation times are nowhere given."),
        bi(f"Der gedruckte Dezember-Wert von Ziegenrück (−4,33 °R) passt nicht zu den gedruckten Winter- (1,25) und Jahresmitteln (5,65); diese verlangen rechnerisch etwa {F(dec_implied,2)} °R. Die Transkription stimmt mit dem Druck überein; der Fehler liegt im Druck oder in der Vorlage. Der Wert wird unverändert gezeigt.",
           f"The printed December value for Ziegenrück (−4.33 °R) does not fit the printed winter (1.25) and annual means (5.65); these require about {E(dec_implied,2)} °R by calculation. The transcription agrees with the print; the error lies in the print or its source. The value is shown unchanged."),
        bi("Die Oktober- bis Dezemberwerte von Lobenstein (1863) sind mit 7,98, 3,17 und 1,00 identisch mit denen von Rothenacker 1865; ob eine Verwechslung in der Vorlage oder ein Zufall vorliegt, lässt sich nicht entscheiden. Juni und Juli 1863 sind in Lobenstein ebenfalls identisch (12,32).",
           "The October to December values of Lobenstein (1863) – 7.98, 3.17 and 1.00 – are identical to those of Rothenacker in 1865; whether this is a mix-up in the source or a coincidence cannot be decided. June and July 1863 are also identical at Lobenstein (12.32)."),
        bi("Gera März 1856 (−6,8 °R) steht im selben Monat Hohenleuben (+0,28 °R) gegenüber; die Differenz von 7,1 °R fällt in Abb. 4 als dunkelrote Zelle auf. Eine der beiden Angaben ist vermutlich fehlerhaft (Druck oder Vorlage); die gedruckten Winter- und Jahresmittel von Gera sind allerdings mit −6,8 gerechnet. Die Werte werden unverändert gezeigt.",
           "Gera March 1856 (−6.8 °R) is matched in the same month by Hohenleuben (+0.28 °R); the difference of 7.1 °R shows as a dark red cell in chart 4. One of the two figures is probably wrong (print or source); the printed winter and annual means of Gera are, however, computed with −6.8. The values are shown unchanged."),
    ],
    "transcription_issues": [
        {"page": "57", "block": "b2", "cell": "r4c4", "transcribed": "0,56", "facsimile": "—0,56", "checked_facsimile": True,
         "note": "Mittel-Zeile Rothenacker, März: Das Minuszeichen fehlt in der Transkription; rechnerisch (−1,67 + 0,54) / 2 = −0,56. Die Mittelzeile wird hier nicht verwendet."},
    ],
    "conversions": [
        {"from": "Grad Réaumur (°R)", "to": "Grad Celsius (°C)", "factor_or_formula": "°C = °R × 1,25",
         "reference": "80 Teilstriche zwischen Eis- und Siedepunkt (Réaumur) gegenüber 100 (Celsius); von Brückner nicht tabelliert"},
    ],
    "datasets": [
        {"name": "monthly", "title": bi("Monatsmittel der Temperatur nach Station und Jahr", "Monthly mean temperature by station and year"),
         "columns": [
             {"name": "station", "label": bi("Station", "Station"), "type": "string", "unit": None},
             {"name": "period", "label": bi("Beobachtungszeitraum", "Observation period"), "type": "string", "unit": None},
             {"name": "n_years", "label": bi("Zahl der Jahre", "Number of years"), "type": "integer", "unit": None, "derived": True, "note": "editorisch gezählt"},
             {"name": "year", "label": YEAR, "type": "integer", "unit": None, "note": "leer bei Ziegenrück (gedrucktes 9-Jahres-Mittel)"},
             {"name": "month", "label": MONTH, "type": "integer", "unit": None, "derived": True, "note": "Monatsnummer 1-12, editorisch"},
             {"name": "month_label", "label": bi("Monat (Original)", "Month (original)"), "type": "string", "unit": None},
             {"name": "temp_r", "label": bi("Monatsmittel (gedruckt)", "Monthly mean (printed)"), "type": "number", "unit": "°R"},
             {"name": "temp_c", "label": bi("Monatsmittel", "Monthly mean"), "type": "number", "unit": "°C", "derived": True, "note": "°R × 1,25"},
             {"name": "series", "label": bi("Reihe (Station und Jahr)", "Series (station and year)"), "type": "string", "unit": None, "note": "nur für Monate, in denen Gera im selben Jahr gedruckt ist; editorisch"},
             {"name": "series_order", "label": bi("Sortierschlüssel der Reihe", "Series sort key"), "type": "integer", "unit": None, "derived": True},
             {"name": "diff_gera_c", "label": bi("Abweichung von Gera im selben Monat", "Deviation from Gera in the same month"), "type": "number", "unit": "K", "derived": True, "note": "(Monatsmittel Station − Monatsmittel Gera, gleiches Jahr und gleicher Monat) × 1,25"},
         ],
         "rows": monthly_rows,
         "source_refs": [{"page": "55", "block": "b7", "rows": "r2-r13"}, {"page": "56", "block": "b2", "rows": "r2-r9"},
                         {"page": "56", "block": "b5", "rows": "r2-r6"}, {"page": "57", "block": "b2", "rows": "r2-r3"},
                         {"page": "57", "block": "b6", "rows": "r2"}, {"page": "58", "block": "b2", "rows": "r2-r14"}]},
        {"name": "annual", "title": bi("Jahreswerte der Temperatur nach Station", "Annual temperature values by station"),
         "columns": [
             {"name": "station", "label": bi("Station", "Station"), "type": "string", "unit": None},
             {"name": "year", "label": YEAR, "type": "integer", "unit": None},
             {"name": "summer_r", "label": bi("Sommermittel (Apr–Sep)", "Summer mean (Apr–Sep)"), "type": "number", "unit": "°R"},
             {"name": "winter_r", "label": bi("Wintermittel (Okt–Mär)", "Winter mean (Oct–Mar)"), "type": "number", "unit": "°R"},
             {"name": "max_r", "label": bi("Höchster Stand", "Highest reading"), "type": "number", "unit": "°R"},
             {"name": "min_r", "label": bi("Tiefster Stand", "Lowest reading"), "type": "number", "unit": "°R"},
             {"name": "annual_r", "label": bi("Jahresmittel", "Annual mean"), "type": "number", "unit": "°R"},
             {"name": "summer_c", "label": bi("Sommermittel (Apr–Sep)", "Summer mean (Apr–Sep)"), "type": "number", "unit": "°C", "derived": True},
             {"name": "winter_c", "label": bi("Wintermittel (Okt–Mär)", "Winter mean (Oct–Mar)"), "type": "number", "unit": "°C", "derived": True},
             {"name": "max_c", "label": bi("Höchster Stand", "Highest reading"), "type": "number", "unit": "°C", "derived": True},
             {"name": "min_c", "label": bi("Tiefster Stand", "Lowest reading"), "type": "number", "unit": "°C", "derived": True},
             {"name": "annual_c", "label": bi("Jahresmittel", "Annual mean"), "type": "number", "unit": "°C", "derived": True},
         ],
         "rows": annual_rows,
         "source_refs": [{"page": "55", "block": "b9", "rows": "r2-r13"}, {"page": "56", "block": "b3", "rows": "r2-r8"},
                         {"page": "56", "block": "b6", "rows": "r2-r6"}, {"page": "57", "block": "b8", "rows": "r2-r10"}]},
        {"name": "summary", "title": bi("Gedruckte Mittel je Station", "Printed means per station"),
         "columns": [
             {"name": "station", "label": bi("Station", "Station"), "type": "string", "unit": None},
             {"name": "period", "label": bi("Beobachtungszeitraum", "Observation period"), "type": "string", "unit": None},
             {"name": "summer_r", "label": bi("Sommermittel (Apr–Sep)", "Summer mean (Apr–Sep)"), "type": "number", "unit": "°R"},
             {"name": "winter_r", "label": bi("Wintermittel (Okt–Mär)", "Winter mean (Oct–Mar)"), "type": "number", "unit": "°R"},
             {"name": "annual_r", "label": bi("Jahresmittel", "Annual mean"), "type": "number", "unit": "°R"},
             {"name": "summer_c", "label": bi("Sommermittel (Apr–Sep)", "Summer mean (Apr–Sep)"), "type": "number", "unit": "°C", "derived": True},
             {"name": "winter_c", "label": bi("Wintermittel (Okt–Mär)", "Winter mean (Oct–Mar)"), "type": "number", "unit": "°C", "derived": True},
             {"name": "annual_c", "label": bi("Jahresmittel", "Annual mean"), "type": "number", "unit": "°C", "derived": True},
         ],
         "rows": summary_rows,
         "source_refs": [{"page": "55", "block": "b9", "rows": "r14"}, {"page": "56", "block": "b3", "rows": "r9"},
                         {"page": "56", "block": "b6", "rows": "r7"}, {"page": "57", "block": "b3"},
                         {"page": "57", "block": "b8", "rows": "r11"}, {"page": "58", "block": "b2", "rows": "r15"}]},
    ],
}

# ---- charts -----------------------------------------------------------------
DOMAIN = int(max(abs(r[10]) for r in monthly_rows if r[10] is not None)) + 1
print("heat domain", DOMAIN)
STN_ALL = ["Gera", "Hohenleuben", "Schleiz", "Rothenacker", "Ziegenrück", "Lobenstein", "Saalburg"]
STN5 = STN_ALL[:5]
col_station = lambda legend=None: {"field": "station", "type": "nominal", "title": None, "scale": {"domain": STN_ALL}, **({"legend": legend} if legend else {})}
x_month = {"field": "month", "type": "quantitative", "title": MONTH,
           "axis": {"values": list(range(1, 13)), "labelExpr": MONTH_LABEL_EXPR, "labelAngle": 0}, "scale": {"domain": [1, 12], "nice": False}}

c1 = {"id": "c1", "dataset": "monthly",
      "title": bi("Mittlerer Jahresgang nach Station", "Mean annual cycle by station"),
      "caption": bi("Mittel der Monatswerte aller gedruckten Jahre, in °C. Zeiträume: Gera 1856–1867, Hohenleuben 1854–1861, Schleiz 1863–1867, Rothenacker 1865 und 1867, Ziegenrück 1848–1856. Der starke Dezember-Abfall bei Ziegenrück beruht auf einem gedruckten Wert, der zu den gedruckten Winter- und Jahresmitteln nicht passt (siehe Hinweise).",
                    "Mean of the monthly values of all printed years, in °C. Periods: Gera 1856–1867, Hohenleuben 1854–1861, Schleiz 1863–1867, Rothenacker 1865 and 1867, Ziegenrück 1848–1856."),
      "vegalite": {
          "height": 320,
          "transform": [{"filter": "datum.n_years > 1 || datum.station == 'Ziegenrück'"},
                        {"aggregate": [{"op": "mean", "field": "temp_c", "as": "m"}], "groupby": ["station", "month"]}],
          "mark": {"type": "line", "point": True},
          "encoding": {"x": x_month, "y": {"field": "m", "type": "quantitative", "title": "°C"},
                       "color": col_station({"values": STN5}),
                       "tooltip": [tip("station", "Station", "Station"), tip("month", "Monat", "Month"), tip("m", "Mittel (°C)", "Mean (°C)", ".1f")]}}}

SUM = bi("Sommer", "Summer")
WIN = bi("Winter", "Winter")
YRM = bi("Jahr", "Year")
sc_series = {"de": "datum.key == 'summer_c' ? 'Sommer' : datum.key == 'winter_c' ? 'Winter' : 'Jahr'",
             "en": "datum.key == 'summer_c' ? 'Summer' : datum.key == 'winter_c' ? 'Winter' : 'Year'"}
y_station = {"field": "station", "type": "nominal", "title": None, "sort": {"field": "annual_c", "op": "max", "order": "descending"}}
c2 = {"id": "c2", "dataset": "summary",
      "title": bi("Sommer-, Winter- und Jahresmittel nach Station", "Summer, winter and annual means by station"),
      "caption": bi("Gedruckte Mittel, in °C: Sommer = April–September, Winter = Oktober–März. Der Strich verbindet Winter- und Sommermittel; Stationen nach Jahresmittel geordnet. Lobenstein und Saalburg haben nur ein Jahresmittel und fehlen hier.",
                    "Printed means, in °C: summer = April–September, winter = October–March. The rule joins winter and summer means; stations sorted by annual mean. Lobenstein and Saalburg have only an annual mean and are absent here."),
      "vegalite": {
          "height": 240,
          "transform": [{"filter": "isValid(datum.summer_c)"}],
          "encoding": {"y": y_station},
          "layer": [
              {"mark": {"type": "rule", "strokeWidth": 2},
               "encoding": {"x": {"field": "winter_c", "type": "quantitative", "title": "°C", "scale": {"zero": False}}, "x2": {"field": "summer_c"}}},
              {"transform": [{"fold": ["winter_c", "annual_c", "summer_c"], "as": ["key", "value"]}, {"calculate": sc_series, "as": "series"}],
               "mark": {"type": "circle", "size": 110, "opacity": 1},
               "encoding": {"x": {"field": "value", "type": "quantitative", "scale": {"zero": False}},
                            "color": {"field": "series", "type": "nominal", "title": None, "scale": {"domain": [WIN, YRM, SUM]}},
                            "tooltip": [tip("station", "Station", "Station"), tip("period", "Zeitraum", "Period"), tip("series", "Größe", "Measure"), tip("value", "°C", None, ".2f")]}},
          ]}}

c3 = {"id": "c3", "dataset": "annual",
      "title": bi("Jahresmittel der einzelnen Jahre", "Annual means of the individual years"),
      "caption": bi("In °C. Nur gedruckte Jahresmittel; bei Ziegenrück fehlt 1854. In den gemeinsamen Jahren liegt Hohenleuben stets unter Gera, Schleiz dagegen nahe bei Gera.",
                    "In °C. Printed annual means only; Ziegenrück lacks 1854. In the common years Hohenleuben is always below Gera, whereas Schleiz is close to Gera."),
      "vegalite": {
          "height": 300,
          "mark": {"type": "line", "point": True, "invalid": "break-paths-filter-domains"},
          "encoding": {
              "x": {"field": "year", "type": "ordinal", "title": YEAR, "axis": {"labelAngle": -45}},
              "y": {"field": "annual_c", "type": "quantitative", "title": "°C", "scale": {"zero": False}},
              "color": col_station({"values": ["Gera", "Hohenleuben", "Schleiz", "Ziegenrück"]}),
              "tooltip": [tip("station", "Station", "Station"), tip("year", "Jahr", "Year"), tip("annual_r", "Jahresmittel (°R)", "Annual mean (°R)"), tip("annual_c", "Jahresmittel (°C)", "Annual mean (°C)", ".2f")]}}}

c4 = {"id": "c4", "dataset": "monthly",
      "title": bi("Abweichung der Stationen von Gera im selben Monat", "Deviation of the stations from Gera in the same month"),
      "caption": bi("Monatsmittel der Station minus Monatsmittel Gera im selben Jahr, in K. Rot: wärmer, blau: kälter als Gera. Hohenleuben liegt überwiegend unter Gera, Rothenacker 1867 durchgehend; Schleiz weicht kaum und ohne feste Richtung ab. Saalburg: Dezember 1864 bis November 1865.",
                    "Monthly mean of the station minus monthly mean at Gera in the same year, in K. Red: warmer, blue: colder than Gera. Hohenleuben is mostly below Gera, Rothenacker throughout in 1867; Schleiz departs only slightly and with no fixed sign. Saalburg: December 1864 to November 1865."),
      "vegalite": {
          "height": 400,
          "transform": [{"filter": "isValid(datum.diff_gera_c)"}],
          "mark": "rect",
          "encoding": {
              "x": {"field": "month", "type": "ordinal", "title": MONTH, "axis": {"labelExpr": MONTH_LABEL_EXPR, "labelAngle": 0}},
              "y": {"field": "series", "type": "nominal", "title": None, "sort": {"field": "series_order", "op": "min"}},
              "color": {"field": "diff_gera_c", "type": "quantitative", "title": "K", "scale": {"range": "diverging", "domain": [-DOMAIN, DOMAIN], "domainMid": 0}},
              "tooltip": [tip("series", "Reihe", "Series"), tip("month_label", "Monat", "Month"), tip("temp_c", "Monatsmittel (°C)", "Monthly mean (°C)", ".1f"),
                          tip("diff_gera_c", "Abweichung von Gera (K)", "Deviation from Gera (K)", "+.1f")]}}}

ana["charts"] = [c1, c2, c3, c4]
ana["keywords"] = bi(["Temperatur", "Stationen", "Hohenleuben", "Schleiz", "Rothenacker", "Ziegenrück", "Lobenstein", "Saalburg", "Gera", "Jahresgang", "Oberland", "Unterland"],
                     ["temperature", "stations", "Hohenleuben", "Schleiz", "Rothenacker", "Ziegenrück", "Lobenstein", "Saalburg", "Gera", "annual cycle", "uplands", "lowlands"])
ana["related"] = ["klima-gera-temperatur-1856-1867", "klima-hoehenlage-temperatur-luftdruck", "klima-gera-luftdruck-1856-1867"]
ana["supersedes_legacy"] = "pp. 56/57 'Klimaübersicht Rothenacker 1865 & 1867' (PNG, p56_img0 = p57_img0) und 'Klimaübersicht Ziegenrück 1848–1856' (PNG, p56_img1 = p57_img1)"
ana["generated_by"] = "Claude Sonnet 5.5 (subagent A03)"
ana["date"] = "2026-10-01"
write(ana)
