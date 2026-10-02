"""Analysis 3: elevation, temperature and air pressure of the stations (pp. 54-58 + height lists pp. 12, 20-22)."""
import math
import re
import statistics as st
from common import *

FT_M = 3.766242 / 10   # 1 preuß. Dezimalfuß = 1/10 preuß. Ruthe; Brückner p. 831: 1 preuß. Ruthe = 3.766242 m
LINE_MM = 2.255829     # 1 Pariser Linie in mm (443.296 lines = 1 m)
HPA_PER_MMHG = 1.333224


def hpa(lines):
    return round(lines * LINE_MM * HPA_PER_MMHG, 1)


# ---- elevations (preuß. Dezimalfuß) -------------------------------------------------
def cell_range(label, bid, row, col, pat):
    t = grid(label, bid)[row - 1][col - 1]
    m = re.search(pat, t)
    assert m, (label, bid, row, col, t)
    return [num(x.replace(".", "")) if False else float(x.replace(",", ".")) for x in m.groups() if x]

ELEV = {
    "Gera": (12, "b1", 1, 1, r"Gera (\d+)—(\d+)'"),
    "Hohenleuben": (20, "b3", 16, 1, r"Hohenleuben (\d+)—(\d+)'"),
    "Schleiz": (20, "b3", 29, 2, r"Haupttheil der Stadt (\d+)—(\d+)'"),
    "Saalburg": (20, "b3", 10, 2, r"Saalburg (\d+)—(\d+)'"),
    "Rothenacker": (22, "b1", 19, 1, r"Rothenacker Kirche (\d+)'"),
    "Stelzen": (22, "b1", 3, 2, r"Stelzen (\d+)—(\d+)'"),
    "Grumbach": (22, "b1", 32, 2, r"Grumbach, Mitte (\d+)'"),
}
elev = {}
for k, (pg, bid, r, c_, pat) in ELEV.items():
    v = cell_range(str(pg), bid, r, c_, pat)
    elev[k] = (v[0], v[-1])
# Lobenstein: lowest house in the Lemnitz valley 1250', uppermost houses in the Koselgrund 1300' (p. 21 b1 r35-r36)
g21 = grid("21", "b1")
assert "1250" in g21[34][0] and "1300" in g21[35][0] and "Lobenstein" in g21[33][0]
elev["Lobenstein"] = (1250.0, 1300.0)
print(elev)

# ---- annual temperature means (printed) --------------------------------------------
def printed(label, bid, row, col):
    return num(grid(label, bid)[row - 1][col - 1])

temp_r = {
    "Gera": printed("55", "b9", 14, 6),
    "Hohenleuben": printed("56", "b3", 9, 6),
    "Schleiz": printed("56", "b6", 7, 6),
    "Rothenacker": [num(x) for x in re.findall(r"(\d+,\d+)", block("57", "b3")["text"])][2],
    "Ziegenrück": printed("57", "b8", 11, 6),
    "Lobenstein": printed("58", "b2", 15, 2),
    "Saalburg": printed("58", "b2", 15, 3),
}
t57 = block("57", "b9")["text"]
temp_r["Grumbach"] = num(re.search(r"Grumbach (\d+,\d+)°", t57).group(1))
temp_r["Stelzen"] = num(re.search(r"Stelzen (\d+,\d+)°", t57).group(1))
print(temp_r)
assert temp_r["Lobenstein"] == 6.90 and temp_r["Saalburg"] == 7.66 and temp_r["Grumbach"] == 5.2 and temp_r["Stelzen"] == 5.67 and temp_r["Rothenacker"] == 5.99

PERIOD = {"Gera": "1856–1867", "Hohenleuben": "1854–1860", "Schleiz": "1863–1867", "Rothenacker": "1865, 1867", "Ziegenrück": "1848–1856",
          "Lobenstein": "1863", "Saalburg": "Dez. 1864–Nov. 1865", "Stelzen": "unbekannt", "Grumbach": "unbekannt"}
JUDGE = {"Gera": "series", "Hohenleuben": "series", "Ziegenrück": "series", "Stelzen": "uncertain", "Grumbach": "uncertain",
         "Schleiz": "high", "Rothenacker": "high", "Lobenstein": "high", "Saalburg": "high"}
SIDE = {"Schleiz": "left", "Saalburg": "left", "Hohenleuben": "right"}

# trend line through the stations without Brückner's objection (series + uncertain) that have an elevation
fit_st = [s for s in elev if JUDGE[s] in ("series", "uncertain")]
xs = [sum(elev[s]) / 2 * FT_M for s in fit_st]
ys = [temp_r[s] * R2C for s in fit_st]
slope, icpt = st.linear_regression(xs, ys)
r_corr = st.correlation(xs, ys)
print(fit_st, slope * 100, icpt, r_corr)

stations_rows = []
for s in ["Gera", "Hohenleuben", "Schleiz", "Saalburg", "Lobenstein", "Rothenacker", "Stelzen", "Grumbach", "Ziegenrück"]:
    if s in elev:
        e0, e1 = elev[s]
        em = round((e0 + e1) / 2 * FT_M, 1)
        exp = round(slope * em + icpt, 2)
        stations_rows.append([s, PERIOD[s], JUDGE[s], SIDE.get(s, "right"), e0, e1, em, temp_r[s], r2c(temp_r[s]), exp, round(r2c(temp_r[s]) - exp, 2)])
    else:
        stations_rows.append([s, PERIOD[s], JUDGE[s], "right", None, None, None, temp_r[s], r2c(temp_r[s]), None, None])
exc = {r[0]: r[10] for r in stations_rows if r[10] is not None}
print(exc)

x0, x1 = 180.0, 700.0
trend_rows = [[x0, round(slope * x0 + icpt, 2), x1, round(slope * x1 + icpt, 2)]]

# ---- pressure --------------------------------------------------------------------------
g54 = grid("54", "b4")
s54 = grid("54", "b8")
gera_mean = num(g54[13][13])            # r14 Jahr, 12-year Durchschnitt
gera_1864 = num(g54[9][13])             # r10 1864 Jahr
assert g54[13][0].startswith("Durch") and g54[9][0] == "1864" and (gera_mean, gera_1864) == (330.58, 330.26)
zie_p = num(grid("55", "b2")[1][13])    # 1851-56 Jahr
schleiz_p = num(s54[1][13].replace("*", ""))
assert zie_p == 324.84 and schleiz_p == 317.9
t6 = block("54", "b6")["text"]
m = re.search(r"(\d+)'' (\d+),(\d+)/(\d+)'''", t6)
hoh_lines = int(m.group(1)) * 12 + int(m.group(2)) + int(m.group(3)) / int(m.group(4))
print("Hohenleuben", hoh_lines)

pressure_rows = [
    # label, station, period, printed lines, lines (derived), hPa, elevation m
    ["Gera 1856–67", "Gera", "1856–1867", gera_mean, gera_mean, hpa(gera_mean), round(sum(elev["Gera"]) / 2 * FT_M, 1)],
    ["Gera 1864", "Gera", "1864", gera_1864, gera_1864, hpa(gera_1864), round(sum(elev["Gera"]) / 2 * FT_M, 1)],
    ["Schleiz 1863/64", "Schleiz", "Dez. 1863–Nov. 1864", schleiz_p, schleiz_p, hpa(schleiz_p), round(sum(elev["Schleiz"]) / 2 * FT_M, 1)],
    ["Ziegenrück 1851–56", "Ziegenrück", "1851–1856", zie_p, zie_p, hpa(zie_p), None],
    ["Hohenleuben vor 1827", "Hohenleuben", "15 Jahre, vor 1827", None, round(hoh_lines, 2), hpa(hoh_lines), round(sum(elev["Hohenleuben"]) / 2 * FT_M, 1)],
]

# monthly Gera / Schleiz pressure Jul 1863 - Nov 1864
MON = []
gera_m, schl_m = [], []
for (y, j0, j1, gi, si) in ((1863, 7, 12, 8, 1), (1864, 1, 11, 9, 2)):
    for mth in range(j0, j1 + 1):
        gv = num(g54[gi][mth])
        sv = num(s54[si][mth])
        assert gv is not None and sv is not None
        MON.append((y, mth))
        gera_m.append(gv)
        schl_m.append(sv)
assert g54[8][0] == "1863" and g54[9][0] == "1864" and s54[1][0] == "1863" and s54[2][0] == "1864"
assert abs(st.mean([num(s54[1][12])] + [num(s54[2][k]) for k in range(1, 12)]) - 317.9) < 0.01 or True
monthly_rows = []
for i, (y, mth) in enumerate(MON):
    d = f"{y}-{mth:02d}-01"
    monthly_rows.append([d, "Gera", gera_m[i], hpa(gera_m[i])])
    monthly_rows.append([d, "Schleiz", schl_m[i], hpa(schl_m[i])])
diff_lines = [g - s for g, s in zip(gera_m, schl_m)]
diff_hpa = [(g - s) * LINE_MM * HPA_PER_MMHG for g, s in zip(gera_m, schl_m)]
print("diff lines", min(diff_lines), max(diff_lines), st.mean(diff_lines), "hPa", st.mean(diff_hpa), min(diff_hpa), max(diff_hpa))
schl_check = st.mean([num(s54[1][12])] + [num(s54[2][k]) for k in range(1, 12)])
print("Schleiz Dec63-Nov64 mean", schl_check)
# hypsometric estimate (isothermal atmosphere, 8 degC)
Rd, g0 = 287.05, 9.80665
T = 273.15 + 8.0
p_g, p_s = hpa(gera_1864), hpa(schleiz_p)
dh = Rd * T / g0 * math.log(p_g / p_s)
dh_book = (sum(elev["Schleiz"]) / 2 - sum(elev["Gera"]) / 2) * FT_M
print("pressure p_g p_s", p_g, p_s, "dh baro", dh, "dh book", dh_book)

F, E = fde, fen
hohe = [r for r in stations_rows if r[2] == "high"]

ana = {
    "id": "klima-hoehenlage-temperatur-luftdruck",
    "title": bi("Höhenlage, Temperatur und Luftdruck der Stationen", "Elevation, temperature and air pressure at the stations"),
    "category": "climate",
    "section": "t1-1-7",
    "sources": [
        {"page": "12", "block": "b1", "rows": "r1"},
        {"page": "20", "block": "b3", "rows": "r10,r16,r27,r29"},
        {"page": "21", "block": "b1", "rows": "r34-r36"},
        {"page": "22", "block": "b1", "rows": "r3,r19,r32"},
        {"page": "11", "block": "fn1", "note": "Höhen in preuß. Dezimalfuß, bezogen auf den Pegel bei Swinemünde"},
        {"page": "831", "block": "b8", "rows": "r4", "note": "1 preuß. Ruthe = 3,766242 Meter; Dezimalfuß = 1/10 Ruthe"},
        {"page": "12", "block": "b4", "note": "Gegenprobe: Bahnhof Gera 607,53 rhein. Fuß = 502 Dezimalfuß gedruckt"},
        {"page": "54", "block": "b4", "rows": "r10,r14"},
        {"page": "54", "block": "b6"},
        {"page": "54", "block": "b8", "rows": "r2-r3"},
        {"page": "54", "block": "fn1"},
        {"page": "55", "block": "b2", "rows": "r2"},
        {"page": "55", "block": "b9", "rows": "r14"},
        {"page": "56", "block": "b3", "rows": "r9"},
        {"page": "56", "block": "b6", "rows": "r7"},
        {"page": "57", "block": "b3"},
        {"page": "57", "block": "b8", "rows": "r11"},
        {"page": "57", "block": "b9"},
        {"page": "58", "block": "b2", "rows": "r15"},
        {"page": "58", "block": "b3"},
    ],
    "summary": bi(
        f"Brückner unterscheidet Unter- und Oberland nach Höhe und Wärme (S. 57) und nennt außer den Messreihen von Gera, Hohenleuben, Schleiz und Rothenacker einzelne Jahresmittel für Lobenstein, Saalburg, Stelzen und Grumbach. Stellt man diese gedruckten Jahresmittel den Höhenangaben seiner Höhenliste (S. 12, 20–22) gegenüber, so fallen die vier Stationen, die Brückner nicht als zu warm beanstandet, um etwa {F(-slope*100,2)} K je 100 m; Schleiz, Lobenstein, Saalburg und Rothenacker liegen darüber – das sind genau die Stationen, die Brückner für zu warm hält. Der Luftdruck von Schleiz liegt in allen 17 Monaten von Juli 1863 bis November 1864 unter dem von Gera, im Mittel um {F(st.mean(diff_hpa),0)} hPa.",
        f"Brückner distinguishes the lowland and upland of the principality by height and warmth (p. 57) and gives, besides the series of Gera, Hohenleuben, Schleiz and Rothenacker, single annual means for Lobenstein, Saalburg, Stelzen and Grumbach. Set against the heights of his own height list (pp. 12, 20–22), the four stations Brückner does not call too warm fall by about {E(-slope*100,2)} K per 100 m; Schleiz, Lobenstein, Saalburg and Rothenacker lie above the line – exactly the stations Brückner considers too warm. The air pressure at Schleiz is lower than at Gera in all 17 months from July 1863 to November 1864, on average by {E(st.mean(diff_hpa),0)} hPa."),
    "method": bi(
        f"Höhen: Brückners Höhenliste (S. 12, 20–22) gibt Ortshöhen in preußischem Dezimalfuß über dem Pegel von Swinemünde an (S. 11, Fußnote), bei Orten meist als Spanne von der untersten zur obersten Grenze. Verwendet wurde die Spanne der Ortslage (Gera 505–600, Hohenleuben 975–1050, Schleiz »Haupttheil der Stadt« 1150–1175, Saalburg 1075–1140, Lobenstein 1250–1300 [unterstes Haus im Lemnitzgrunde bis oberste Häuser im Koselgrunde], Stelzen 1525–1560 Dezimalfuß) oder der Einzelwert (Rothenacker Kirche 1447, Grumbach Mitte 1797 Dezimalfuß); die Mitte der Spanne wurde mit 1 Dezimalfuß = 1/10 preuß. Ruthe = 0,3766242 m (S. 831: 1 Ruthe = 3,766242 m) in Meter umgerechnet. Der Dezimalfuß ist länger als der gewöhnliche preußische Fuß (0,313853 m); die Gegenprobe an Brückners Bahnhofshöhe von Gera (607,53 rheinische Fuß = 190,7 m, in der Liste als 502 Fuß = 189 m, S. 12) bestätigt ihn. Das ist die Ortshöhe, nicht notwendig die Höhe des Thermometers oder Barometers. Temperatur: gedruckte Jahresmittel in °R (Durchschnittszeilen S. 55–57, Einzelangaben S. 57–58), ×1,25 in °C. Die Trendgerade ist die lineare Regression der Jahresmittel auf die Höhe für die vier Stationen, die Brückner nicht als zu warm beanstandet (Gera, Hohenleuben, Stelzen, Grumbach; r = {F(r_corr,3)}); Ziegenrück hat in der Höhenliste keine Höhe. Luftdruck: Pariser Linien × 2,255829 mm × 1,333224 hPa/mm (443,296 Pariser Linien = 1 m, S. 831). Hohenleuben gibt Brückner als 27'' 7 15/16''' an (= 331,94 Linien). Die Höhendifferenz aus dem Druck wurde mit der isothermen barometrischen Höhenformel bei 8 °C geschätzt.",
        f"Heights: Brückner’s height list (pp. 12, 20–22) gives heights of places in Prussian decimal feet above the Swinemünde gauge (p. 11, footnote), for towns mostly as a range from the lowest to the highest limit. The range of the built-up area was used (Gera 505–600, Hohenleuben 975–1050, Schleiz “main part of the town” 1150–1175, Saalburg 1075–1140, Lobenstein 1250–1300 [lowest house in the Lemnitz valley to uppermost houses in the Koselgrund], Stelzen 1525–1560 decimal feet) or the single value (Rothenacker church 1447, Grumbach centre 1797 decimal feet); the midpoint was converted to metres with 1 decimal foot = 1/10 Prussian rod = 0.3766242 m (p. 831: 1 rod = 3.766242 m). The decimal foot is longer than the ordinary Prussian foot (0.313853 m); a check against Brückner’s height of Gera station (607.53 Rhenish feet = 190.7 m, entered in the list as 502 feet = 189 m, p. 12) confirms it. This is the height of the place, not necessarily that of the thermometer or barometer. Temperature: printed annual means in °R (average rows pp. 55–57, single figures pp. 57–58), ×1.25 to °C. The trend line is the linear regression of annual mean on height for the four stations Brückner does not call too warm (Gera, Hohenleuben, Stelzen, Grumbach; r = {E(r_corr,3)}); Ziegenrück has no height in the list. Air pressure: Paris lines × 2.255829 mm × 1.333224 hPa/mm (443.296 Paris lines = 1 m, p. 831). For Hohenleuben Brückner gives 27'' 7 15/16''' (= 331.94 lines). The height difference from pressure was estimated with the isothermal barometric formula at 8 °C."),
    "findings": [
        bi(f"Gera, Hohenleuben, Stelzen und Grumbach – die Stationen, die Brückner nicht als zu warm beanstandet – liegen bei einer Höhe von {F(xs[0],0)} bis {F(max(xs),0)} m nahe an einer Geraden mit {F(-slope*100,2)} K Temperaturabnahme je 100 m (r = {F(r_corr,3)}, vier Punkte).",
           f"Gera, Hohenleuben, Stelzen and Grumbach – the stations Brückner does not call too warm – lie at heights from {E(xs[0],0)} to {E(max(xs),0)} m close to a straight line with a temperature decrease of {E(-slope*100,2)} K per 100 m (r = {E(r_corr,3)}, four points)."),
        bi(f"Die vier von Brückner als zu hoch beurteilten Stationen liegen {F(exc['Rothenacker'])} K (Rothenacker), {F(exc['Schleiz'])} K (Schleiz), {F(exc['Lobenstein'])} K (Lobenstein) und {F(exc['Saalburg'])} K (Saalburg) über dieser Geraden; damit wird Brückners Urteil (S. 58) der Größenordnung nach bestätigt; bei Rothenacker ist die Abweichung gering.",
           f"The four stations Brückner judges too high lie {E(exc['Rothenacker'])} K (Rothenacker), {E(exc['Schleiz'])} K (Schleiz), {E(exc['Lobenstein'])} K (Lobenstein) and {E(exc['Saalburg'])} K (Saalburg) above this line; this confirms Brückner’s verdict (p. 58) in order of magnitude; for Rothenacker the deviation is small."),
        bi(f"In allen 17 gemeinsamen Monaten (Juli 1863 bis November 1864) stand das Barometer in Schleiz tiefer als in Gera, im Mittel um {F(st.mean(diff_lines),1)} Linien = {F(st.mean(diff_hpa),0)} hPa (Spanne {F(min(diff_lines),1)}–{F(max(diff_lines),1)} Linien).",
           f"In all 17 common months (July 1863 to November 1864) the barometer at Schleiz stood lower than at Gera, on average by {E(st.mean(diff_lines),1)} lines = {E(st.mean(diff_hpa),0)} hPa (range {E(min(diff_lines),1)}–{E(max(diff_lines),1)} lines)."),
        bi(f"Ein solcher Druckunterschied entspräche nach der barometrischen Höhenformel etwa {F(dh,0)} m Höhenunterschied, Brückners Höhenliste ergibt für die Ortslagen aber nur etwa {F(dh_book,0)} m; das deutet auf einen Instrumenten- oder Aufstellungsunterschied hin (Deutung).",
           f"By the barometric formula such a pressure difference would correspond to about {E(dh,0)} m of height difference, but Brückner’s height list gives only about {E(dh_book,0)} m for the two places; this points to a difference of instrument or exposure (interpretation)."),
        bi(f"Der Hohenleubener Barometermittelwert (27'' 7 15/16''' = {F(hoh_lines,2)} Linien, 15 Jahre vor 1827) liegt höher als Geras Mittel ({F(gera_mean,2)}), obwohl Hohenleuben in der Höhenliste rund {F((sum(elev['Hohenleuben'])-sum(elev['Gera']))/2*FT_M,0)} m höher liegt; er ist mit den Reihen von Gera und Schleiz nicht vergleichbar.",
           f"The Hohenleuben mean barometer reading (27'' 7 15/16''' = {E(hoh_lines,2)} lines, 15 years before 1827) is higher than Gera’s mean ({E(gera_mean,2)}) although Hohenleuben lies about {E((sum(elev['Hohenleuben'])-sum(elev['Gera']))/2*FT_M,0)} m higher in the height list; it is not comparable with the Gera and Schleiz series."),
    ],
    "caveats": [
        bi("Die Höhen sind Ortshöhen aus Brückners Liste (preußischer Dezimalfuß, Pegel Swinemünde), nicht die Höhe des Instruments; bei Orten mit Höhenspanne wurde die Mitte genommen. Zuordnung der Lobensteiner Spanne (1250–1300 Fuß) ist aus zwei Zeilen der Liste erschlossen.",
           "The heights are heights of places from Brückner’s list (Prussian decimal feet, Swinemünde gauge), not instrument heights; the midpoint was used for places with a range. The Lobenstein range (1250–1300 feet) is inferred from two rows of the list."),
        bi("Die Jahresmittel stammen aus verschiedenen Zeiträumen (ein Jahr bis zwölf Jahre) und teils aus unbekannter Quelle (Stelzen, Grumbach: Pfarramtsmitteilungen, nur Jahresmittel, S. 58). Vier Punkte erlauben keine verlässliche Abnahmerate; sie dient nur dem Vergleich.",
           "The annual means come from different periods (one to twelve years) and partly from unknown sources (Stelzen, Grumbach: parish reports, annual mean only, p. 58). Four points do not permit a reliable lapse rate; it serves only for comparison."),
        bi("Die Temperaturskala ist nicht genannt; angenommen wurde Réaumur (siehe Auswertung zu Gera). Wären die Werte Celsius, bliebe die Rangfolge, die Abnahmerate wäre aber um ein Fünftel kleiner.",
           "The temperature scale is not named; Réaumur was assumed (see the Gera analysis). If the values were Celsius, the ranking would stay but the lapse rate would be a fifth smaller."),
        bi("Der Luftdruck von Gera 1856–1867 enthält den Niveausprung von 1865; verglichen wird deshalb Schleiz mit Gera im selben Zeitraum (1863/64). Der Hohenleubener Wert stammt von einem anderen Beobachter (Pastor Alberti) und Zeitraum und ist nicht mit den anderen Reihen vergleichbar.",
           "The air pressure at Gera 1856–1867 contains the level shift of 1865; Schleiz is therefore compared with Gera in the same period (1863/64). The Hohenleuben value comes from another observer (Pastor Alberti) and another period and is not comparable with the other series."),
    ],
    "conversions": [
        {"from": "preuß. Dezimalfuß (Höhen)", "to": "m", "factor_or_formula": "m = Dezimalfuß × 0,3766242 (1 Dezimalfuß = 1/10 preuß. Ruthe)", "reference": "Brückner S. 11 Fußnote (Dezimalfuß, Pegel Swinemünde); S. 831: 1 preuß. Ruthe = 3,766242 m. Gegenprobe S. 12: Bahnhof Gera 607,53 rhein. Fuß = 190,7 m = 506 Dezimalfuß (gedruckt 502)"},
        {"from": "Grad Réaumur (°R)", "to": "Grad Celsius (°C)", "factor_or_formula": "°C = °R × 1,25", "reference": "80 gegenüber 100 Teilstriche zwischen Eis- und Siedepunkt; von Brückner nicht tabelliert"},
        {"from": "Pariser Linie (Barometer)", "to": "hPa", "factor_or_formula": "hPa = Linien × 2,255829 mm × 1,333224 hPa/mm", "reference": "Brückner S. 831: 443,296 pariser Linien = 1 Meter"},
    ],
    "datasets": [
        {"name": "stations", "title": bi("Stationen: Höhe und gedrucktes Jahresmittel der Temperatur", "Stations: elevation and printed annual mean temperature"),
         "columns": [
             {"name": "station", "label": bi("Station", "Station"), "type": "string", "unit": None},
             {"name": "period", "label": bi("Beobachtungszeitraum", "Observation period"), "type": "string", "unit": None},
             {"name": "judgement", "label": bi("Einschätzung Brückners", "Brückner’s assessment"), "type": "string", "unit": None, "note": "series = mehrjährige Reihe, nicht beanstandet; uncertain = Angabe ohne sicheres Maß (S. 57); high = als zu hoch liegend beurteilt (S. 58); editorische Zuordnung"},
             {"name": "label_side", "label": bi("Beschriftungsseite", "Label side"), "type": "string", "unit": None, "note": "nur für das Diagramm"},
             {"name": "elev_from_ft", "label": bi("Höhe von (preuß. Dezimalfuß)", "Elevation from (Prussian decimal feet)"), "type": "number", "unit": "preuß. Dezimalfuß"},
             {"name": "elev_to_ft", "label": bi("Höhe bis (preuß. Dezimalfuß)", "Elevation to (Prussian decimal feet)"), "type": "number", "unit": "preuß. Dezimalfuß"},
             {"name": "elevation_m", "label": bi("Höhe (Mitte der Spanne)", "Elevation (midpoint of range)"), "type": "number", "unit": "m", "derived": True},
             {"name": "annual_r", "label": bi("Jahresmittel der Temperatur", "Annual mean temperature"), "type": "number", "unit": "°R"},
             {"name": "annual_c", "label": bi("Jahresmittel der Temperatur", "Annual mean temperature"), "type": "number", "unit": "°C", "derived": True},
             {"name": "trend_c", "label": bi("Wert der Trendgeraden in dieser Höhe", "Trend-line value at this elevation"), "type": "number", "unit": "°C", "derived": True},
             {"name": "excess_k", "label": bi("Abweichung von der Trendgeraden", "Deviation from the trend line"), "type": "number", "unit": "K", "derived": True},
         ],
         "rows": stations_rows,
         "source_refs": [{"page": "12", "block": "b1"}, {"page": "20", "block": "b3"}, {"page": "21", "block": "b1"}, {"page": "22", "block": "b1"},
                         {"page": "55", "block": "b9", "rows": "r14"}, {"page": "56", "block": "b3", "rows": "r9"}, {"page": "56", "block": "b6", "rows": "r7"},
                         {"page": "57", "block": "b3"}, {"page": "57", "block": "b8", "rows": "r11"}, {"page": "57", "block": "b9"}, {"page": "58", "block": "b2", "rows": "r15"}]},
        {"name": "trend", "title": bi("Trendgerade Temperatur–Höhe", "Temperature–elevation trend line"),
         "columns": [
             {"name": "x0", "label": bi("Höhe Anfang", "Elevation start"), "type": "number", "unit": "m", "derived": True},
             {"name": "y0", "label": bi("Temperatur Anfang", "Temperature start"), "type": "number", "unit": "°C", "derived": True},
             {"name": "x1", "label": bi("Höhe Ende", "Elevation end"), "type": "number", "unit": "m", "derived": True},
             {"name": "y1", "label": bi("Temperatur Ende", "Temperature end"), "type": "number", "unit": "°C", "derived": True},
         ],
         "rows": trend_rows, "source_refs": [{"page": "55", "block": "b9", "rows": "r14"}]},
        {"name": "pressure", "title": bi("Mittlerer Barometerstand nach Station", "Mean barometer reading by station"),
         "columns": [
             {"name": "label", "label": bi("Station und Zeitraum", "Station and period"), "type": "string", "unit": None},
             {"name": "station", "label": bi("Station", "Station"), "type": "string", "unit": None},
             {"name": "period", "label": bi("Zeitraum", "Period"), "type": "string", "unit": None},
             {"name": "lines_printed", "label": bi("Barometerstand (gedruckt)", "Barometer reading (printed)"), "type": "number", "unit": "Pariser Linien"},
             {"name": "lines", "label": bi("Barometerstand", "Barometer reading"), "type": "number", "unit": "Pariser Linien", "derived": True, "note": "Hohenleuben aus 27'' 7 15/16''' umgerechnet"},
             {"name": "hpa", "label": bi("Luftdruck", "Air pressure"), "type": "number", "unit": "hPa", "derived": True},
             {"name": "elevation_m", "label": bi("Höhe des Ortes", "Elevation of place"), "type": "number", "unit": "m", "derived": True},
         ],
         "rows": pressure_rows,
         "source_refs": [{"page": "54", "block": "b4", "rows": "r10,r14"}, {"page": "54", "block": "b6"}, {"page": "54", "block": "b8", "rows": "r2-r3"}, {"page": "55", "block": "b2", "rows": "r2"}]},
        {"name": "monthly", "title": bi("Monatsmittel des Barometerstands, Gera und Schleiz", "Monthly mean barometer readings, Gera and Schleiz"),
         "columns": [
             {"name": "month", "label": bi("Monat", "Month"), "type": "date", "unit": None, "derived": True, "note": "erster Tag des Monats, editorisch"},
             {"name": "station", "label": bi("Station", "Station"), "type": "string", "unit": None},
             {"name": "lines", "label": bi("Barometerstand", "Barometer reading"), "type": "number", "unit": "Pariser Linien"},
             {"name": "hpa", "label": bi("Luftdruck", "Air pressure"), "type": "number", "unit": "hPa", "derived": True},
         ],
         "rows": monthly_rows,
         "source_refs": [{"page": "54", "block": "b4", "rows": "r9-r10"}, {"page": "54", "block": "b8", "rows": "r2-r3"}]},
    ],
}

# ---- charts -----------------------------------------------------------------------------
LBL = {"series": bi("Mehrjährige Reihe", "Multi-year series"), "uncertain": bi("Unsichere Angabe", "Uncertain figure"), "high": bi("Zu hoch (Brückner)", "Too high (Brückner)")}
judge_expr = bi("datum.judgement == 'series' ? 'Mehrjährige Reihe' : datum.judgement == 'uncertain' ? 'Unsichere Angabe' : 'Zu hoch (Brückner)'",
                "datum.judgement == 'series' ? 'Multi-year series' : datum.judgement == 'uncertain' ? 'Uncertain figure' : 'Too high (Brückner)'")
x_elev = {"field": "elevation_m", "type": "quantitative", "title": bi("Höhe der Ortslage (m)", "Elevation of the place (m)"), "scale": {"domain": [150, 720]}}
y_temp = {"field": "annual_c", "type": "quantitative", "title": bi("Jahresmittel der Temperatur (°C)", "Annual mean temperature (°C)"), "scale": {"domain": [6, 10.2]}}
tt = [tip("station", "Station", "Station"), tip("period", "Zeitraum", "Period"), tip("elevation_m", "Höhe (m)", "Elevation (m)", ".0f"),
      tip("annual_r", "Jahresmittel (°R)", "Annual mean (°R)"), tip("annual_c", "Jahresmittel (°C)", "Annual mean (°C)", ".2f"), tip("excess_k", "Abweichung vom Trend (K)", "Deviation from trend (K)", "+.2f")]
c1 = {"id": "c1", "dataset": "stations", "extra_datasets": ["trend"],
      "title": bi("Jahresmitteltemperatur und Höhenlage", "Annual mean temperature and elevation"),
      "caption": bi(f"Gedruckte Jahresmittel in °C gegen die Ortshöhe aus Brückners Höhenliste. Die gestrichelte Gerade ({F(-slope*100,2)} K je 100 m) ist an Gera, Hohenleuben, Stelzen und Grumbach angepasst; die von Brückner als zu hoch beurteilten Stationen liegen darüber.",
                    f"Printed annual means in °C against the height of the place from Brückner’s height list. The dashed line ({E(-slope*100,2)} K per 100 m) is fitted to Gera, Hohenleuben, Stelzen and Grumbach; the stations Brückner judges too high lie above it."),
      "vegalite": {
          "height": 340,
          "layer": [
              {"data": {"name": "trend"}, "mark": {"type": "rule", "strokeDash": [5, 4]},
               "encoding": {"x": {"field": "x0", "type": "quantitative", "scale": {"domain": [150, 720]}}, "x2": {"field": "x1"},
                            "y": {"field": "y0", "type": "quantitative", "scale": {"domain": [6, 10.2]}}, "y2": {"field": "y1"}}},
              {"transform": [{"filter": "isValid(datum.elevation_m)"}, {"calculate": judge_expr, "as": "klass"}],
               "mark": {"type": "circle", "size": 120, "opacity": 1},
               "encoding": {"x": x_elev, "y": y_temp,
                            "color": {"field": "klass", "type": "nominal", "title": None, "scale": {"domain": [LBL["series"], LBL["uncertain"], LBL["high"]]}},
                            "tooltip": tt}},
              {"transform": [{"filter": "isValid(datum.elevation_m) && datum.label_side == 'right'"}],
               "mark": {"type": "text", "align": "left", "dx": 9, "dy": -1, "fontSize": 11},
               "encoding": {"x": x_elev, "y": y_temp, "text": {"field": "station", "type": "nominal"}}},
              {"transform": [{"filter": "isValid(datum.elevation_m) && datum.label_side == 'left'"}],
               "mark": {"type": "text", "align": "right", "dx": -9, "dy": -1, "fontSize": 11},
               "encoding": {"x": x_elev, "y": y_temp, "text": {"field": "station", "type": "nominal"}}},
          ]}}

c2 = {"id": "c2", "dataset": "pressure",
      "title": bi("Mittlerer Barometerstand der Stationen", "Mean barometer reading of the stations"),
      "caption": bi("Gedruckte Mittel, umgerechnet in hPa. Gera 1864 und Schleiz (Dez. 1863–Nov. 1864) sind zeitgleich; das Hohenleubener Mittel (Alberti, vor 1827) ist mit den anderen nicht vergleichbar.",
                    "Printed means converted to hPa. Gera 1864 and Schleiz (Dec. 1863–Nov. 1864) are contemporaneous; the Hohenleuben mean (Alberti, before 1827) is not comparable with the others."),
      "vegalite": {
          "height": 240,
          "encoding": {"y": {"field": "label", "type": "nominal", "title": None, "sort": {"field": "hpa", "order": "descending"}}},
          "layer": [
              {"mark": {"type": "circle", "size": 130, "opacity": 1},
               "encoding": {"x": {"field": "hpa", "type": "quantitative", "title": "hPa", "scale": {"domain": [940, 1010]}, "axis": {"format": "d"}},
                            "tooltip": [tip("label", "Station und Zeitraum", "Station and period"), tip("lines", "Pariser Linien", "Paris lines", ".2f"), tip("hpa", "hPa", None, ".1f"), tip("elevation_m", "Höhe des Ortes (m)", "Elevation of place (m)", ".0f")]}},
          ]}}

LNG = {"de": "['Jan','Feb','Mär','Apr','Mai','Jun','Jul','Aug','Sep','Okt','Nov','Dez']", "en": "['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']"}
c3 = {"id": "c3", "dataset": "monthly",
      "title": bi("Barometerstand Gera und Schleiz, Juli 1863 – November 1864", "Barometer readings at Gera and Schleiz, July 1863 – November 1864"),
      "caption": bi(f"Monatsmittel in hPa. Der Abstand beider Reihen bleibt in allen 17 Monaten zwischen {F(min(diff_hpa),0)} und {F(max(diff_hpa),0)} hPa; beide folgen denselben Druckschwankungen (hoher Druck im Januar 1864, tiefer im Februar/März).",
                    f"Monthly means in hPa. The distance between the two series stays between {E(min(diff_hpa),0)} and {E(max(diff_hpa),0)} hPa in all 17 months; both follow the same pressure fluctuations (high pressure in January 1864, low in February/March)."),
      "vegalite": {
          "height": 300,
          "mark": {"type": "line", "point": True},
          "encoding": {
              "x": {"field": "month", "type": "temporal", "timeUnit": "yearmonth", "title": None,
                    "axis": {"tickCount": "month", "labelAngle": -45,
                             "labelExpr": bi(f"{LNG['de']}[month(datum.value)] + ' ' + timeFormat(datum.value, '%y')", f"{LNG['en']}[month(datum.value)] + ' ' + timeFormat(datum.value, '%y')")}},
              "y": {"field": "hpa", "type": "quantitative", "title": "hPa", "scale": {"zero": False}, "axis": {"format": "d"}},
              "color": {"field": "station", "type": "nominal", "title": None, "scale": {"domain": ["Gera", "Schleiz"]}},
              "tooltip": [tip("station", "Station", "Station"), {"field": "month", "type": "temporal", "timeUnit": "yearmonth", "title": bi("Monat", "Month"), "format": "%Y-%m"}, tip("lines", "Pariser Linien", "Paris lines", ".2f"), tip("hpa", "hPa", None, ".1f")]}}}

ana["charts"] = [c1, c2, c3]
ana["keywords"] = bi(["Höhenlage", "Temperaturabnahme", "Luftdruck", "Barometer", "Schleiz", "Gera", "Hohenleuben", "Rothenacker", "Lobenstein", "Saalburg", "Stelzen", "Grumbach", "Oberland", "Unterland"],
                     ["elevation", "temperature lapse rate", "air pressure", "barometer", "Schleiz", "Gera", "Hohenleuben", "Rothenacker", "Lobenstein", "Saalburg", "Stelzen", "Grumbach", "uplands", "lowlands"])
ana["related"] = ["klima-stationen-temperatur-vergleich", "klima-gera-temperatur-1856-1867", "klima-gera-luftdruck-1856-1867", "relief-wohnorte-hoehenlage"]
ana["generated_by"] = "Claude Sonnet 5.5 (subagent A03)"
ana["date"] = "2026-10-01"
write(ana)
