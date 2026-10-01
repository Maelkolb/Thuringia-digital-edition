"""Builds the reference analysis (Gera air pressure, p. 54) that serves as the
worked example for the analysis subagents. Values are read from the canonical
page JSON, never typed by hand."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = json.loads((ROOT / "data/pages/0066.json").read_text(encoding="utf-8"))
grid = next(b for b in p["blocks"] if b["id"] == "b4")["grid"]
MONTHS = ["Jan.", "Febr.", "März", "April", "Mai", "Juni", "Juli", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
LINE_MM = 2.255829  # 1 Pariser Linie in mm
HPA_PER_MMHG = 1.333224


def num(s):
    return float(s.replace(",", "."))


monthly, annual = [], []
for row in grid[1:13]:
    y = int(row[0])
    for m in range(12):
        v = num(row[1 + m])
        monthly.append([y, m + 1, MONTHS[m], v, round(v * LINE_MM * HPA_PER_MMHG, 1)])
    a = num(row[13])
    annual.append([y, a, round(a * LINE_MM * HPA_PER_MMHG, 1)])

YEAR = {"de": "Jahr", "en": "Year"}
ana = {
    "id": "klima-gera-luftdruck-1856-1867",
    "title": {"de": "Luftdruck in Gera 1856–1867", "en": "Air pressure at Gera, 1856–1867"},
    "category": "climate",
    "section": "t1-1-7",
    "sources": [{"page": "54", "block": "b4", "rows": "r2-r14"}, {"page": "54", "block": "b5"}],
    "summary": {
        "de": "Brückner druckt die Monatsmittel des Barometerstands in Gera für zwölf Jahre (1856–1867), beobachtet von C. Kratzsch und Dr. Robert Schmidt. Umgerechnet liegen die Werte um 990 hPa, wie es der Höhenlage Geras (rund 200 m) entspricht. Auffällig ist der sprunghafte Anstieg ab 1865.",
        "en": "Brückner prints monthly mean barometer readings for Gera over twelve years (1856–1867), observed by C. Kratzsch and Dr Robert Schmidt. Converted, the values lie around 990 hPa, as expected for the town's elevation of about 200 m. The abrupt rise from 1865 onward stands out.",
    },
    "method": {
        "de": "Die 144 Monatswerte und 12 Jahresmittel wurden aus der Tabelle auf S. 54 übernommen. Die Überschrift nennt »pariser Zolle«, die Zahlen sind aber Pariser Linien (1 Zoll = 12 Linien); 326,40 Linien entsprechen 27 Zoll 2,4 Linien. Umrechnung: 1 Pariser Linie = 2,2558 mm Quecksilbersäule; 1 mm Hg = 1,3332 hPa. Eine Reduktion auf Meeresniveau oder 0 °C ist nicht möglich, da Höhe und Temperatur des Instruments nicht angegeben sind.",
        "en": "The 144 monthly values and 12 annual means were taken from the table on p. 54. The heading says “Paris inches”, but the figures are Paris lines (1 inch = 12 lines); 326.40 lines equal 27 inches 2.4 lines. Conversion: 1 Paris line = 2.2558 mm of mercury; 1 mm Hg = 1.3332 hPa. Reduction to sea level or 0 °C is not possible because the instrument's height and temperature are not stated.",
    },
    "findings": [
        {"de": "1856–1864 schwanken die Jahresmittel nur zwischen 328,94 und 330,40 Linien (989,3–993,7 hPa).",
         "en": "From 1856 to 1864 the annual means vary only between 328.94 and 330.40 lines (989.3–993.7 hPa)."},
        {"de": "1865–1867 liegen alle Jahresmittel um 2,6–3,6 Linien (8–11 hPa) über dem Mittel der Vorjahre; ein so abrupter, anhaltender Sprung deutet eher auf einen Wechsel von Instrument, Aufstellungsort oder Reduktion als auf eine klimatische Änderung.",
         "en": "In 1865–1867 all annual means lie 2.6–3.6 lines (8–11 hPa) above the mean of the preceding years; such an abrupt, lasting step points to a change of instrument, location or reduction rather than to a climatic change."},
        {"de": "Die Monatsmittel streuen im Winter deutlich stärker als im Sommer – ein typisches Muster des mitteleuropäischen Luftdrucks.",
         "en": "Monthly means scatter much more in winter than in summer, a typical pattern of central European air pressure."},
        {"de": "Brückner nennt als Extreme 342,0 Linien (März 1867) und 316,00 Linien (1856), eine Spanne von 26 Linien (≈ 78 hPa).",
         "en": "Brückner gives extremes of 342.0 lines (March 1867) and 316.00 lines (1856), a range of 26 lines (≈ 78 hPa)."},
    ],
    "caveats": [
        {"de": "Der Text nennt die Einheit »pariser Zolle«; die Werte sind Linien. Die Umrechnung in hPa dient nur dem Vergleich.",
         "en": "The text names the unit “Paris inches”; the values are lines. The hPa conversion is for comparison only."},
    ],
    "conversions": [
        {"from": "Pariser Linie (Barometer)", "to": "hPa", "factor_or_formula": "hPa = Linien × 2.2558 mm × 1.3332 hPa/mm",
         "reference": "1 Pariser Fuß = 324.84 mm; 1 Linie = 1/144 Fuß"},
    ],
    "datasets": [
        {"name": "monthly", "title": {"de": "Monatsmittel des Barometerstands", "en": "Monthly mean barometer readings"},
         "columns": [
             {"name": "year", "label": YEAR, "type": "integer", "unit": None},
             {"name": "month", "label": {"de": "Monat", "en": "Month"}, "type": "integer", "unit": None, "derived": True, "note": "Monatsnummer 1-12, editorisch"},
             {"name": "month_label", "label": {"de": "Monat (Original)", "en": "Month (original)"}, "type": "string", "unit": None},
             {"name": "pressure_lines", "label": {"de": "Barometerstand", "en": "Barometer reading"}, "type": "number", "unit": "Pariser Linien"},
             {"name": "pressure_hpa", "label": {"de": "Luftdruck", "en": "Air pressure"}, "type": "number", "unit": "hPa", "derived": True},
         ],
         "rows": monthly, "source_refs": [{"page": "54", "block": "b4", "rows": "r2-r13"}]},
        {"name": "annual", "title": {"de": "Jahresmittel", "en": "Annual means"},
         "columns": [
             {"name": "year", "label": YEAR, "type": "integer", "unit": None},
             {"name": "pressure_lines", "label": {"de": "Jahresmittel", "en": "Annual mean"}, "type": "number", "unit": "Pariser Linien"},
             {"name": "pressure_hpa", "label": {"de": "Jahresmittel", "en": "Annual mean"}, "type": "number", "unit": "hPa", "derived": True},
         ],
         "rows": annual, "source_refs": [{"page": "54", "block": "b4", "rows": "r2-r13"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "annual",
         "title": {"de": "Jahresmittel des Luftdrucks", "en": "Annual mean air pressure"},
         "caption": {"de": "Gera, umgerechnet in hPa. Die gestrichelte Linie markiert das Mittel 1856–1864; ab 1865 liegen alle Werte deutlich darüber.",
                     "en": "Gera, converted to hPa. The dashed rule marks the 1856–1864 mean; from 1865 all values lie clearly above it."},
         "vegalite": {
             "height": 260,
             "layer": [
                 {"mark": {"type": "line", "point": True},
                  "encoding": {
                      "x": {"field": "year", "type": "ordinal", "title": YEAR, "axis": {"labelAngle": 0}},
                      "y": {"field": "pressure_hpa", "type": "quantitative", "title": "hPa", "scale": {"zero": False}},
                      "tooltip": [{"field": "year", "title": YEAR},
                                  {"field": "pressure_lines", "title": {"de": "Pariser Linien", "en": "Paris lines"}},
                                  {"field": "pressure_hpa", "title": "hPa"}]}},
                 {"transform": [{"filter": "datum.year <= 1864"}, {"aggregate": [{"op": "mean", "field": "pressure_hpa", "as": "m"}]}],
                  "mark": {"type": "rule", "strokeDash": [4, 3]},
                  "encoding": {"y": {"field": "m", "type": "quantitative"}}},
             ]}},
        {"id": "c2", "dataset": "monthly",
         "title": {"de": "Monatsmittel nach Jahr und Monat", "en": "Monthly means by year and month"},
         "caption": {"de": "Jede Zelle ist ein Monatsmittel (hPa). Der dunkle Block ab 1865 zeigt den Niveausprung der Messreihe.",
                     "en": "Each cell is a monthly mean (hPa). The dark block from 1865 shows the level shift of the series."},
         "vegalite": {
             "height": 300,
             "mark": "rect",
             "encoding": {
                 "x": {"field": "month_label", "type": "ordinal", "sort": {"field": "month", "op": "min"}, "title": {"de": "Monat", "en": "Month"}, "axis": {"labelAngle": 0}},
                 "y": {"field": "year", "type": "ordinal", "title": YEAR},
                 "color": {"field": "pressure_hpa", "type": "quantitative", "title": "hPa"},
                 "tooltip": [{"field": "year", "title": YEAR}, {"field": "month_label", "title": {"de": "Monat", "en": "Month"}},
                             {"field": "pressure_lines", "title": {"de": "Pariser Linien", "en": "Paris lines"}},
                             {"field": "pressure_hpa", "title": "hPa"}]}}},
    ],
    "keywords": {"de": ["Luftdruck", "Barometer", "Barometerstand", "Gera", "Meteorologie", "Pariser Linie"],
                 "en": ["air pressure", "barometer", "Gera", "meteorology", "Paris line"]},
    "supersedes_legacy": "p. 54 'Mittlerer Barometerstand in Gera (1856-1867)' (PNG)",
    "generated_by": "Claude Opus 5.5 (reference example)",
    "date": "2026-10-01",
}
out = ROOT / "data/analyses" / f"{ana['id']}.json"
out.write_text(json.dumps(ana, ensure_ascii=False, indent=1), encoding="utf-8")
print(out)
