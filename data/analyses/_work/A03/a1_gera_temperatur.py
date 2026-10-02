"""Analysis 1: temperature at Gera 1856-1867 (p. 55, blocks b7 + b9)."""
import statistics as st
from common import *

gm = grid("55", "b7")
ga = grid("55", "b9")
monthly_r = {}  # year -> 12 values
for r in gm[1:13]:
    monthly_r[int(r[0])] = [num(x) for x in r[1:13]]
annual_r = {}
for r in ga[1:13]:
    annual_r[int(r[0])] = [num(x) for x in r[1:6]]  # summer, winter, max, min, annual
years = sorted(monthly_r)
assert years == sorted(annual_r) and len(years) == 12

mean_m = [st.mean(monthly_r[y][j] for y in years) for j in range(12)]  # Réaumur

monthly_rows = []
for y in years:
    for j in range(12):
        v = monthly_r[y][j]
        monthly_rows.append([y, j + 1, MONTHS_PRINT[j], v, r2c(v), round((v - mean_m[j]) * R2C, 2)])
annual_rows = []
for y in years:
    s, w, hi, lo, a = annual_r[y]
    annual_rows.append([y, s, w, hi, lo, a, r2c(s), r2c(w), r2c(hi), r2c(lo), r2c(a), round((hi - lo) * R2C, 2)])

# ---- statistics for the text ------------------------------------------------
ann = {y: annual_r[y][4] for y in years}
mean_ann = st.mean(ann.values())
warm = max(ann, key=ann.get)
cold = min(ann, key=ann.get)
hi_y = max(years, key=lambda y: annual_r[y][2])
lo_y = min(years, key=lambda y: annual_r[y][3])
span = {y: (annual_r[y][2] - annual_r[y][3]) * R2C for y in years}
span_mean = st.mean(span.values())
span_max = max(span, key=span.get)
span_min = min(span, key=span.get)
cold_m = min(range(12), key=lambda j: mean_m[j])
warm_m = max(range(12), key=lambda j: mean_m[j])
amp = (mean_m[warm_m] - mean_m[cold_m]) * R2C
sd = [st.stdev(monthly_r[y][j] for y in years) * R2C for j in range(12)]
tr = st.linear_regression(years, [ann[y] * R2C for y in years])
tr_r = st.correlation(years, [ann[y] for y in years])
mar56 = monthly_r[1856][2]
mar_anom = (mar56 - mean_m[2]) * R2C
print(mean_ann, warm, cold, hi_y, lo_y, span_mean, span_max, span_min, cold_m, warm_m, amp, sd, mar_anom)


def c(v):
    return v * R2C


F = fde
E = fen

ana = {
    "id": "klima-gera-temperatur-1856-1867",
    "title": bi("Temperatur in Gera 1856–1867", "Temperature at Gera, 1856–1867"),
    "category": "climate",
    "section": "t1-1-7",
    "sources": [
        {"page": "55", "block": "b7", "rows": "r2-r14"},
        {"page": "55", "block": "b9", "rows": "r2-r14"},
        {"page": "55", "block": "fn1"},
        {"page": "55", "block": "fn2"},
        {"page": "70", "block": "b1", "note": "Hinweis auf die Réaumur-Skala (»5 1/2° R.«)"},
    ],
    "summary": bi(
        f"Brückner druckt für Gera die Monatsmittel der Temperatur aller zwölf Jahre 1856–1867, dazu Sommer-, Winter- und Jahresmittel sowie den höchsten und tiefsten Thermometerstand jedes Jahres. Die Zahlen stehen in Grad Réaumur und sind hier in °C umgerechnet. Das Jahresmittel liegt bei {F(c(mean_ann))} °C; das kälteste Jahr ({cold}) blieb {F(c(ann[warm]-ann[cold]))} K unter dem wärmsten ({warm}), und der März 1856 lag {F(-mar_anom,0)} K unter dem Märzmittel.",
        f"For Gera Brückner prints the monthly mean temperatures for all twelve years 1856–1867, plus summer, winter and annual means and the highest and lowest thermometer reading of each year. The figures are in degrees Réaumur and are converted here to °C. The annual mean is {E(c(mean_ann))} °C; the coldest year ({cold}) stayed {E(c(ann[warm]-ann[cold]))} K below the warmest ({warm}), and March 1856 was {E(-mar_anom,0)} K below the March average."),
    "method": bi(
        "Übernommen wurden die 144 Monatsmittel (S. 55, Tabelle a) und die Tabelle b) mit Sommer-, Winter-, Höchst-, Tiefst- und Jahreswerten der zwölf Jahre. Die Skala nennt der Abschnitt nicht; wie auf S. 70 (»5 1/2° R.«) und nach der Plausibilität der Werte angenommen, handelt es sich um Grad Réaumur. Umrechnung: °C = °R × 1,25, gerundet auf zwei Stellen. Die Abweichungen (Heatmap) sind Monatswert minus Mittel desselben Kalendermonats über die zwölf Jahre; dieses Mittel wurde aus den 144 Werten neu berechnet und weicht von Brückners gedruckter Mittelzeile um höchstens 0,01 °R ab. Brückner definiert Sommer als April bis September, Winter als Oktober bis Dezember plus Januar bis März desselben Kalenderjahres (Fußnoten). Die gedruckten Sommer-, Winter- und Jahresmittel stimmen mit den Monatswerten bis auf höchstens 0,04 °R überein (Rundung der einstellig angegebenen Werte ab 1863); das gedruckte Minus des März 1856 (»— 6,8«) wurde am Faksimile geprüft und passt zum gedruckten Wintermittel 1856.",
        "The table takes in the 144 monthly means (p. 55, table a) and table b) with the summer, winter, highest, lowest and annual values of the twelve years. The section does not name the scale; as on p. 70 (“5 1/2° R.”) and judging by the plausibility of the values, it is degrees Réaumur. Conversion: °C = °R × 1.25, rounded to two decimals. The deviations (heat map) are the monthly value minus the mean of the same calendar month over the twelve years; this mean was recomputed from the 144 values and differs from Brückner’s printed mean row by 0.01 °R at most. Brückner defines summer as April to September and winter as October to December plus January to March of the same calendar year (footnotes). The printed summer, winter and annual means agree with the monthly values to within 0.04 °R (rounding of the one-decimal values from 1863 on); the printed minus sign of March 1856 (“— 6,8”) was checked on the facsimile and fits the printed winter mean of 1856."),
    "findings": [
        bi(f"Das Jahresmittel der zwölf Jahre beträgt {F(c(mean_ann))} °C ({F(mean_ann,2)} °R). Die Einzeljahre reichen von {F(c(ann[cold]))} °C ({cold}) bis {F(c(ann[warm]))} °C ({warm}); ein Trend ist nicht zu erkennen (Steigung {F(tr.slope*10)} K je Jahrzehnt, r = {F(tr_r,2)}).",
           f"The annual mean over the twelve years is {E(c(mean_ann))} °C ({E(mean_ann,2)} °R). Individual years range from {E(c(ann[cold]))} °C ({cold}) to {E(c(ann[warm]))} °C ({warm}); no trend is visible (slope {E(tr.slope*10)} K per decade, r = {E(tr_r,2)})."),
        bi(f"Im mittleren Jahresgang ist der Januar der kälteste Monat ({F(c(mean_m[cold_m]))} °C), der August der wärmste ({F(c(mean_m[warm_m]))} °C); die Amplitude der Monatsmittel beträgt {F(amp)} K.",
           f"In the mean annual cycle January is the coldest month ({E(c(mean_m[cold_m]))} °C) and August the warmest ({E(c(mean_m[warm_m]))} °C); the amplitude of the monthly means is {E(amp)} K."),
        bi(f"Die Monatsmittel streuen im Winter weit stärker als im Sommer: Die Standardabweichung über die Jahre beträgt im März {F(sd[2])} K und im Januar {F(sd[0])} K, im September nur {F(sd[8])} K. Der kälteste Einzelmonat ist der März 1856 ({F(c(mar56))} °C, {F(-mar_anom)} K unter dem Märzmittel).",
           f"Monthly means scatter far more in winter than in summer: the standard deviation across years is {E(sd[2])} K in March and {E(sd[0])} K in January, but only {E(sd[8])} K in September. The coldest single month is March 1856 ({E(c(mar56))} °C, {E(-mar_anom)} K below the March mean)."),
        bi(f"Der höchste Thermometerstand war {F(annual_r[hi_y][2])} °R = {F(c(annual_r[hi_y][2]))} °C ({hi_y}), der tiefste {F(annual_r[lo_y][3])} °R = {F(c(annual_r[lo_y][3]))} °C ({lo_y}). Die jährliche Spanne zwischen Höchst- und Tiefststand beträgt im Mittel {F(span_mean)} K, am größten {span_max} ({F(span[span_max])} K), am kleinsten {span_min} ({F(span[span_min])} K).",
           f"The highest reading was {E(annual_r[hi_y][2])} °R = {E(c(annual_r[hi_y][2]))} °C ({hi_y}), the lowest {E(annual_r[lo_y][3])} °R = {E(c(annual_r[lo_y][3]))} °C ({lo_y}). The yearly spread between highest and lowest reading averages {E(span_mean)} K, largest in {span_max} ({E(span[span_max])} K) and smallest in {span_min} ({E(span[span_min])} K)."),
    ],
    "caveats": [
        bi("Die Temperaturskala ist an dieser Stelle nicht genannt. Die Annahme Réaumur stützt sich auf die Angabe »° R.« auf S. 70 und auf die Plausibilität (umgerechnetes Jahresmittel 8,7 °C für Gera in rund 200 m Höhe). Wären die Werte Celsius-Angaben, lägen alle °C-Werte dieser Auswertung um 20 % niedriger.",
           "The temperature scale is not named at this point. The Réaumur assumption rests on the “° R.” notation on p. 70 and on plausibility (converted annual mean 8.7 °C for Gera at about 200 m). If the values were Celsius, all °C values of this analysis would be 20 % lower."),
        bi("Die frühere Darstellung (PNG) zeichnete die gedruckten Zahlen unumgerechnet als °C; ihre Extremwerte und Spannen waren daher um ein Fünftel zu klein.",
           "The earlier edition’s chart (PNG) plotted the printed figures unconverted as °C; its extremes and spans were therefore too small by a fifth."),
        bi("Einstationsreihe über zwölf Jahre mit wechselnden Beobachtern (Kratzsch: ein- bis zweimal täglich, Schmidt: dreimal täglich, S. 54); Instrument, Aufstellung und Termine sind nicht angegeben. Die Luftdruckreihe derselben Station zeigt 1865 einen Sprung – Homogenität der Temperaturreihe ist nicht belegt.",
           "A single-station series over twelve years with changing observers (Kratzsch: once or twice daily, Schmidt: three times daily, p. 54); instrument, exposure and observation hours are not stated. The air-pressure series of the same station jumps in 1865, so homogeneity of the temperature series is not demonstrated."),
        bi("Ab 1863 sind die Monatswerte nur noch auf 0,1 °R genau gedruckt (vorher 0,01 °R); die zwei Dezimalen der °C-Werte sind dort Rundungsergebnis und täuschen keine Genauigkeit vor.",
           "From 1863 on the monthly values are printed to 0.1 °R only (earlier 0.01 °R); the two decimals of the °C values there result from rounding and do not imply that precision."),
        bi("Der März 1856 (−6,8 °R) steht im Widerspruch zu Hohenleuben, wo für denselben Monat +0,28 °R gedruckt sind (S. 56, siehe Auswertung der Stationen); Geras gedruckte Winter- und Jahresmittel 1856 sind mit −6,8 gerechnet, der Fehler läge also in der Vorlage. Der Wert wird unverändert gezeigt, bestimmt aber die Extreme der Abb. 3 und 4.",
           "March 1856 (−6.8 °R) contradicts Hohenleuben, where +0.28 °R is printed for the same month (p. 56, see the station comparison); Gera’s printed winter and annual means for 1856 are computed with −6.8, so the error would lie in the source. The value is shown unchanged but determines the extremes in charts 3 and 4."),
    ],
    "conversions": [
        {"from": "Grad Réaumur (°R)", "to": "Grad Celsius (°C)", "factor_or_formula": "°C = °R × 1,25",
         "reference": "80 Teilstriche zwischen Eis- und Siedepunkt (Réaumur) gegenüber 100 (Celsius); von Brückner nicht tabelliert"},
    ],
    "datasets": [
        {"name": "monthly", "title": bi("Monatsmittel der Temperatur, Gera", "Monthly mean temperature, Gera"),
         "columns": [
             {"name": "year", "label": YEAR, "type": "integer", "unit": None},
             {"name": "month", "label": MONTH, "type": "integer", "unit": None, "derived": True, "note": "Monatsnummer 1-12, editorisch"},
             {"name": "month_label", "label": bi("Monat (Original)", "Month (original)"), "type": "string", "unit": None},
             {"name": "temp_r", "label": bi("Monatsmittel (gedruckt)", "Monthly mean (printed)"), "type": "number", "unit": "°R"},
             {"name": "temp_c", "label": bi("Monatsmittel", "Monthly mean"), "type": "number", "unit": "°C", "derived": True, "note": "°R × 1,25"},
             {"name": "anomaly_c", "label": bi("Abweichung vom Monatsmittel 1856–1867", "Deviation from the 1856–1867 monthly mean"), "type": "number", "unit": "K", "derived": True},
         ],
         "rows": monthly_rows, "source_refs": [{"page": "55", "block": "b7", "rows": "r2-r13"}]},
        {"name": "annual", "title": bi("Jahreswerte der Temperatur, Gera", "Annual temperature values, Gera"),
         "columns": [
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
             {"name": "span_c", "label": bi("Spanne Höchst–Tiefst", "Spread highest–lowest"), "type": "number", "unit": "K", "derived": True},
         ],
         "rows": annual_rows, "source_refs": [{"page": "55", "block": "b9", "rows": "r2-r13"}]},
    ],
}

# ---- charts -----------------------------------------------------------------
SER = {"summer_c": bi("Sommermittel", "Summer mean"),
       "annual_c": bi("Jahresmittel", "Annual mean"),
       "winter_c": bi("Wintermittel", "Winter mean")}


def expr_map(mapping, key="datum.key"):
    de = " : ".join(f"{key} == '{k}' ? '{v['de']}'" for k, v in mapping.items()) + " : ''"
    en = " : ".join(f"{key} == '{k}' ? '{v['en']}'" for k, v in mapping.items()) + " : ''"
    return bi(de, en)


x_year = {"field": "year", "type": "ordinal", "title": YEAR, "axis": {"labelAngle": 0}}

c1 = {"id": "c1", "dataset": "annual",
      "title": bi("Jahres-, Sommer- und Wintermittel", "Annual, summer and winter means"),
      "caption": bi("Gera, in °C. Das Sommermittel (April–September) schwankt wenig, das Wintermittel (Oktober–März) stark; 1864 war in beiden Jahreszeiten das kälteste Jahr der Reihe.",
                    "Gera, in °C. The summer mean (April–September) varies little, the winter mean (October–March) a lot; 1864 was the coldest year of the series in both seasons."),
      "vegalite": {
          "height": 280,
          "transform": [{"fold": ["summer_c", "annual_c", "winter_c"], "as": ["key", "value"]},
                        {"calculate": expr_map(SER), "as": "series"}],
          "mark": {"type": "line", "point": True},
          "encoding": {
              "x": x_year,
              "y": {"field": "value", "type": "quantitative", "title": "°C", "scale": {"zero": False}},
              "color": {"field": "series", "type": "nominal", "title": None,
                        "scale": {"domain": [SER["summer_c"], SER["annual_c"], SER["winter_c"]]}},
              "tooltip": [tip("year", "Jahr", "Year"), tip("series", "Größe", "Measure"), tip("value", "°C", None, ".2f")]}}}

HI = bi("Höchster Stand", "Highest reading")
LO = bi("Tiefster Stand", "Lowest reading")
ME = bi("Jahresmittel", "Annual mean")
c2 = {"id": "c2", "dataset": "annual",
      "title": bi("Höchster und tiefster Thermometerstand je Jahr", "Highest and lowest thermometer reading per year"),
      "caption": bi("Gera, in °C. Der Strich verbindet Tiefst- und Höchststand, der Balken markiert das Jahresmittel. Der Frost von 1861 (−28,4 °C) ist die tiefste Marke der Reihe.",
                    "Gera, in °C. The rule joins lowest and highest reading, the tick marks the annual mean. The frost of 1861 (−28.4 °C) is the lowest mark of the series."),
      "vegalite": {
          "height": 300,
          "encoding": {"x": x_year},
          "layer": [
              {"mark": {"type": "rule", "strokeWidth": 2},
               "encoding": {"y": {"field": "min_c", "type": "quantitative", "title": "°C"}, "y2": {"field": "max_c"}}},
              {"mark": {"type": "circle", "size": 90, "opacity": 1},
               "encoding": {"y": {"field": "max_c", "type": "quantitative"}, "color": {"datum": HI, "type": "nominal", "title": None, "scale": {"domain": [HI, LO, ME]}},
                            "tooltip": [tip("year", "Jahr", "Year"), tip("max_c", "Höchster Stand (°C)", "Highest reading (°C)", ".1f"), tip("max_r", "Höchster Stand (°R)", "Highest reading (°R)")]}},
              {"mark": {"type": "circle", "size": 90, "opacity": 1},
               "encoding": {"y": {"field": "min_c", "type": "quantitative"}, "color": {"datum": LO, "type": "nominal"},
                            "tooltip": [tip("year", "Jahr", "Year"), tip("min_c", "Tiefster Stand (°C)", "Lowest reading (°C)", ".1f"), tip("min_r", "Tiefster Stand (°R)", "Lowest reading (°R)")]}},
              {"mark": {"type": "tick", "size": 26, "thickness": 3},
               "encoding": {"y": {"field": "annual_c", "type": "quantitative"}, "color": {"datum": ME, "type": "nominal"},
                            "tooltip": [tip("year", "Jahr", "Year"), tip("annual_c", "Jahresmittel (°C)", "Annual mean (°C)", ".2f"), tip("annual_r", "Jahresmittel (°R)", "Annual mean (°R)")]}},
          ]}}

CM = bi("Mittel 1856–67", "Mean 1856–67")
CW = bi("1863 (warm)", "1863 (warm)")
CC = bi("1864 (kalt)", "1864 (cold)")
x_month = {"field": "month", "type": "quantitative", "title": MONTH,
           "axis": {"values": list(range(1, 13)), "labelExpr": MONTH_LABEL_EXPR, "labelAngle": 0}, "scale": {"domain": [1, 12], "nice": False}}
c3 = {"id": "c3", "dataset": "monthly",
      "title": bi("Mittlerer Jahresgang und Spannweite der Jahre", "Mean annual cycle and range across the years"),
      "caption": bi("Gera, Monatsmittel in °C. Das Band reicht vom kältesten bis zum wärmsten Wert jedes Kalendermonats in den zwölf Jahren; die Linien zeigen das Mittel sowie das wärmste (1863) und das kälteste Jahr (1864).",
                    "Gera, monthly means in °C. The band spans the coldest to the warmest value of each calendar month over the twelve years; the lines show the mean and the warmest (1863) and coldest year (1864)."),
      "vegalite": {
          "height": 320,
          "layer": [
              {"transform": [{"aggregate": [{"op": "min", "field": "temp_c", "as": "lo"}, {"op": "max", "field": "temp_c", "as": "hi"}], "groupby": ["month"]}],
               "mark": {"type": "area", "line": False},
               "encoding": {"x": x_month, "y": {"field": "lo", "type": "quantitative", "title": "°C"}, "y2": {"field": "hi"},
                            "tooltip": [tip("month", "Monat", "Month"), tip("lo", "Kältester Wert (°C)", "Lowest value (°C)", ".1f"), tip("hi", "Wärmster Wert (°C)", "Highest value (°C)", ".1f")]}},
              {"transform": [{"aggregate": [{"op": "mean", "field": "temp_c", "as": "m"}], "groupby": ["month"]}],
               "mark": {"type": "line", "point": True},
               "encoding": {"x": x_month, "y": {"field": "m", "type": "quantitative"},
                            "color": {"datum": CM, "type": "nominal", "title": None, "scale": {"domain": [CM, CW, CC]}},
                            "tooltip": [tip("month", "Monat", "Month"), tip("m", "Mittel (°C)", "Mean (°C)", ".1f")]}},
              {"transform": [{"filter": "datum.year == 1863"}],
               "mark": {"type": "line", "point": True},
               "encoding": {"x": x_month, "y": {"field": "temp_c", "type": "quantitative"}, "color": {"datum": CW, "type": "nominal"},
                            "tooltip": [tip("year", "Jahr", "Year"), tip("month", "Monat", "Month"), tip("temp_c", "°C", None, ".1f")]}},
              {"transform": [{"filter": "datum.year == 1864"}],
               "mark": {"type": "line", "point": True},
               "encoding": {"x": x_month, "y": {"field": "temp_c", "type": "quantitative"}, "color": {"datum": CC, "type": "nominal"},
                            "tooltip": [tip("year", "Jahr", "Year"), tip("month", "Monat", "Month"), tip("temp_c", "°C", None, ".1f")]}},
          ]}}

c4 = {"id": "c4", "dataset": "monthly",
      "title": bi("Abweichung der Monatsmittel vom Mittel des Kalendermonats", "Deviation of monthly means from the mean of the calendar month"),
      "caption": bi("Gera, in K (Kelvin = Differenz in °C). Blau: kälter, rot: wärmer als der Durchschnitt desselben Kalendermonats 1856–1867. Der März 1856, der Januar 1861, Januar und Dezember 1864 sowie der Februar 1865 fallen heraus.",
                    "Gera, in K (kelvin = difference in °C). Blue: colder, red: warmer than the average of the same calendar month 1856–1867. March 1856, January 1861, January and December 1864 and February 1865 stand out."),
      "vegalite": {
          "height": 320,
          "mark": "rect",
          "encoding": {
              "x": {"field": "month", "type": "ordinal", "title": MONTH, "axis": {"labelExpr": MONTH_LABEL_EXPR, "labelAngle": 0}},
              "y": {"field": "year", "type": "ordinal", "title": YEAR},
              "color": {"field": "anomaly_c", "type": "quantitative", "title": "K", "scale": {"range": "diverging", "domain": [-12, 12], "domainMid": 0}},
              "tooltip": [tip("year", "Jahr", "Year"), tip("month_label", "Monat", "Month"), tip("temp_r", "Monatsmittel (°R)", "Monthly mean (°R)"),
                          tip("temp_c", "Monatsmittel (°C)", "Monthly mean (°C)", ".1f"), tip("anomaly_c", "Abweichung (K)", "Deviation (K)", "+.1f")]}}}

ana["charts"] = [c1, c2, c3, c4]
ana["keywords"] = bi(["Temperatur", "Thermometer", "Gera", "Réaumur", "Jahresmittel", "Sommer", "Winter", "Meteorologie", "Klima", "Frost"],
                     ["temperature", "thermometer", "Gera", "Réaumur", "annual mean", "summer", "winter", "meteorology", "climate", "frost"])
ana["related"] = ["klima-gera-luftdruck-1856-1867", "klima-stationen-temperatur-vergleich", "klima-hoehenlage-temperatur-luftdruck"]
ana["supersedes_legacy"] = "p. 55 'Klimaübersicht Gera 1856–1867' (PNG, p55_img0)"
ana["generated_by"] = "Claude Sonnet 5.5 (subagent A03)"
ana["date"] = "2026-10-01"
write(ana)
