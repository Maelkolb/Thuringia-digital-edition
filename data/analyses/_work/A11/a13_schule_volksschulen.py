"""A11-13: Volksschulen Ende 1868 nach Landestheilen, Stadt und Land (p. 299)."""
from common import *

g = grid("299", "b3")
N = lambda x: num(x)
AREAS = [  # grid index, key, de, en, region
    (1, "a", "Gera Stadt", "Gera town", "Gera"),
    (2, "b", "Gera Land", "Gera country", "Gera"),
    (5, "c", "Schleiz Städte", "Schleiz towns", "Schleiz"),
    (6, "d", "Schleiz Land", "Schleiz country", "Schleiz"),
    (9, "e", "Lobenstein-Ebersdorf Städte", "Lobenstein-Ebersdorf towns", "Lobenstein-Ebersdorf"),
    (10, "f", "Lobenstein-Ebersdorf Land", "Lobenstein-Ebersdorf country", "Lobenstein-Ebersdorf"),
]
rows = []
for gi, k, de, en, reg in AREAS:
    r = g[gi]
    sch, leh, s63, s68, kn, md, r_lsch, r_sl, r_es = [N(x) for x in r[1:]]
    assert kn + md == s68
    ppt = round(s68 / leh, 2)
    growth = round(100 * (s68 - s63) / s63, 1)
    girls = round(100 * md / s68, 1)
    share = round(100 / r_es, 1)
    rows.append([k, de, en, reg, int(sch), int(leh), int(s63), int(s68), int(kn), int(md), r_sl, r_es, ppt, growth, girls, share])
tot = {n: sum(r[i] for r in rows) for n, i in (("sch", 4), ("leh", 5), ("s63", 6), ("s68", 7), ("kn", 8), ("md", 9))}
assert tot["sch"] == 115 and tot["leh"] == 206 and tot["s63"] == 12919 and tot["s68"] == 14239
print(tot, rows)

pct = lambda a, b: 100 * a / b
ppt_total = tot["s68"] / tot["leh"]
over = [r for r in rows if r[12] > 50]
worst = max(rows, key=lambda r: r[12])
best_growth = max(rows, key=lambda r: r[13])
lowest_growth = min(rows, key=lambda r: r[13])
rural = [r for r in rows if r[0] in "bdf"]
rural_sch = sum(r[4] for r in rural)
rural_leh = sum(r[5] for r in rural)
rural_pup = sum(r[7] for r in rural)
share_pop = 100 / 6.18
hi_share = max(rows, key=lambda r: r[15])
lo_share = min(rows, key=lambda r: r[15])
print(ppt_total, worst, best_growth, lowest_growth, rural_sch, rural_leh, rural_pup / rural_leh, hi_share[1], hi_share[15], lo_share[1], lo_share[15])


def D(x, nd=0):
    return fmt_de(x, nd)


def E(x, nd=0):
    return fmt_en(x, nd)


ana = {
    "id": "schule-volksschulen-schueler-lehrer-1863-1868",
    "title": bi("Volksschulen 1863–1868: Schüler und Lehrer nach Landestheilen, Stadt und Land", "Elementary schools 1863–1868: pupils and teachers by region, town and country"),
    "category": "education",
    "section": "t1-4-6",
    "sources": [{"page": "299", "block": "b3", "rows": "r2-r16"}, {"page": "299", "block": "b4"}],
    "summary": bi(
        f"Ende 1868 bestanden im Fürstentum {D(tot['sch'])} Volksschulen mit {D(tot['leh'])} Lehrern und {D(tot['s68'])} Schülern (1863: {D(tot['s63'])}). Brückner gliedert nach den drei Landestheilen und nach Städten und Landorten und errechnet das Verhältnis von Schülern zu Lehrern und von Einwohnern zu Schülern. Die Auswertung stellt die Klassenstärke dem von Brückner genannten Normalmaß von 50 Schülern je Lehrer gegenüber.",
        f"At the end of 1868 the principality had {E(tot['sch'])} elementary schools with {E(tot['leh'])} teachers and {E(tot['s68'])} pupils (1863: {E(tot['s63'])}). Brückner divides by the three regions and by towns and rural places and calculates the ratios of pupils to teachers and of inhabitants to pupils. The analysis sets class size against the norm of 50 pupils per teacher that Brückner mentions.",
    ),
    "method": bi(
        "Quelle ist die Tabelle »Es bestanden im Fürstenthume Ende 1868« (S. 299, b3). Verwendet werden die sechs Grundzeilen (Gera, Schleiz und Lobenstein-Ebersdorf je Stadt und Land); die Summenzeilen wurden nachgerechnet. Abgeleitet sind die Schüler je Lehrer (Schüler 1868 : Lehrer), der Zuwachs 1863–1868, der Mädchenanteil und der Schüleranteil an der Bevölkerung (100 : Einwohner je Schüler nach Brückners Verhältniszahl). Das Normalmaß von 50 Schülern je Lehrer stammt von Brückner (S. 299, b4).",
        "The source is the table “At the end of 1868 the principality had” (p. 299, b3). The six base rows are used (Gera, Schleiz and Lobenstein-Ebersdorf, each town and country); the total rows were recalculated. Derived are the pupils per teacher (pupils 1868 : teachers), the growth 1863–1868, the share of girls and the pupils' share of the population (100 : inhabitants per pupil according to Brückner's ratio). The norm of 50 pupils per teacher is Brückner's (p. 299, b4).",
    ),
    "findings": [
        bi(f"Die Zahl der Schüler wuchs von {D(tot['s63'])} (1863) auf {D(tot['s68'])} (1868), um {D(pct(tot['s68']-tot['s63'], tot['s63']),1)} %; am stärksten in der Stadt Gera ({D(best_growth[13],1)} %, von {D(best_growth[6])} auf {D(best_growth[7])}), in den Städten des Landestheils Lobenstein-Ebersdorf sank sie leicht ({D(lowest_growth[13],1)} %).",
           f"The number of pupils grew from {E(tot['s63'])} (1863) to {E(tot['s68'])} (1868), by {E(pct(tot['s68']-tot['s63'], tot['s63']),1)} %; most strongly in the town of Gera ({E(best_growth[13],1)} %, from {E(best_growth[6])} to {E(best_growth[7])}); in the towns of the Lobenstein-Ebersdorf region it fell slightly ({E(lowest_growth[13],1)} %)."),
        bi(f"Im Landesdurchschnitt kommen {D(ppt_total,1)} Schüler auf einen Lehrer. Nur die Stadt Gera ({D(rows[0][12],1)}) bleibt unter dem Normalmaß von 50; die übrigen fünf Gruppen liegen zwischen {D(min(r[12] for r in over),1)} und {D(worst[12],1)}, am höchsten im Landgebiet von Gera ({worst[1]}).",
           f"On national average there are {E(ppt_total,1)} pupils per teacher. Only the town of Gera ({E(rows[0][12],1)}) stays below the norm of 50; the other five groups lie between {E(min(r[12] for r in over),1)} and {E(worst[12],1)}, highest in the country area of Gera ({worst[2]})."),
        bi(f"Auf dem Land bestehen {D(rural_sch)} Schulen mit {D(rural_leh)} Lehrern, also nur {D(rural_leh/rural_sch,2)} Lehrer je Schule bei {D(rural_pup/rural_leh,0)} Schülern je Lehrer; in den Städten kommen im Durchschnitt {D(sum(r[5] for r in rows if r[0] in 'ace')/sum(r[4] for r in rows if r[0] in 'ace'),1)} Lehrer auf eine Schule.",
           f"The country has {E(rural_sch)} schools with {E(rural_leh)} teachers, i.e. only {E(rural_leh/rural_sch,2)} teachers per school at {E(rural_pup/rural_leh,0)} pupils per teacher; in the towns there are on average {E(sum(r[5] for r in rows if r[0] in 'ace')/sum(r[4] for r in rows if r[0] in 'ace'),1)} teachers per school."),
        bi(f"Die Schüler machen im Fürstentum rund {D(share_pop,1)} % der Bevölkerung aus; der Anteil reicht von {D(lo_share[15],1)} % ({lo_share[1]}) bis {D(hi_share[15],1)} % ({hi_share[1]}).",
           f"Pupils make up about {E(share_pop,1)} % of the population; the share ranges from {E(lo_share[15],1)} % ({lo_share[2]}) to {E(hi_share[15],1)} % ({hi_share[2]})."),
    ],
    "caveats": [
        bi("Die gedruckten Summen der Knaben (7426) und Mädchen (7613) für das Fürstentum stimmen nicht mit der Summe der Landestheile überein (7526 und 6713); die Gesamtzahl 14239 stimmt. Die Ziffern sind im Original so gedruckt (Faksimile geprüft) und werden hier nicht verwendet; der Mädchenanteil ist aus den Zeilen berechnet.",
           "The printed totals of boys (7,426) and girls (7,613) for the principality do not agree with the sum of the regions (7,526 and 6,713); the grand total 14,239 does. The figures are printed so in the original (facsimile checked) and are not used here; the share of girls is calculated from the rows."),
        bi("Die Lehrerzahl der Stadt Gera (59) schließt nach der Fußnote die Lehrerinnen ein; für die übrigen Gruppen ist das nicht gesagt. Brückners Verhältniszahlen für Schleiz (Summe: 1,36 Lehrer je Schule, 84,28 Schüler je Lehrer) weichen von der Nachrechnung (1,37; 84,45) leicht ab; hier werden eigene Werte verwendet. »Schüler« sind die in den Volksschulen eingeschriebenen Kinder, nicht der tatsächliche Schulbesuch.",
           "The number of teachers in the town of Gera (59) includes women teachers according to the footnote; for the other groups this is not stated. Brückner's ratios for Schleiz (total: 1.36 teachers per school, 84.28 pupils per teacher) differ slightly from the recalculation (1.37; 84.45); our own values are used here. “Pupils” are the children enrolled in the elementary schools, not actual attendance."),
    ],
    "datasets": [
        {"name": "schools", "title": bi("Volksschulen Ende 1868 nach Landestheil und Stadt/Land", "Elementary schools at the end of 1868 by region and town/country"),
         "columns": [
             col("area_key", "Kürzel", "Key", "string"),
             col("area_de", "Gebiet", "Area", "string"), col("area_en", "Gebiet (englisch)", "Area (English)", "string"),
             col("region", "Landestheil", "Region", "string"),
             col("schools", "Schulen", "Schools", "integer", "Schulen"), col("teachers", "Lehrer", "Teachers", "integer", "Lehrer"),
             col("pupils_1863", "Schüler 1863", "Pupils 1863", "integer", "Schüler"), col("pupils_1868", "Schüler 1868", "Pupils 1868", "integer", "Schüler"),
             col("boys_1868", "Knaben 1868", "Boys 1868", "integer", "Schüler"), col("girls_1868", "Mädchen 1868", "Girls 1868", "integer", "Schüler"),
             col("ppt_printed", "Schüler je Lehrer (gedruckt)", "Pupils per teacher (printed)", "number", "Schüler"),
             col("inh_per_pupil", "Einwohner je Schüler (gedruckt)", "Inhabitants per pupil (printed)", "number", "Einwohner"),
             col("ppt", "Schüler je Lehrer (nachgerechnet)", "Pupils per teacher (recalculated)", "number", "Schüler", derived=True),
             col("growth_pct", "Zuwachs der Schüler 1863–1868", "Growth of pupils 1863–1868", "number", "%", derived=True),
             col("girls_pct", "Mädchenanteil 1868", "Share of girls 1868", "number", "%", derived=True),
             col("pop_share", "Schüler in % der Einwohner", "Pupils as % of inhabitants", "number", "%", derived=True),
         ],
         "rows": rows, "source_refs": [{"page": "299", "block": "b3", "rows": "r2-r16"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "schools",
         "title": bi("Schüler je Lehrer, 1868", "Pupils per teacher, 1868"),
         "caption": bi("Die gestrichelte Linie markiert das von Brückner genannte Normalmaß von 50 Schülern je Lehrer.", "The dashed line marks the norm of 50 pupils per teacher mentioned by Brückner."),
         "vegalite": {
             "height": 280,
             "layer": [
                 {"mark": "bar",
                  "encoding": {
                      "y": {"field": F("area"), "type": "nominal", "sort": "-x", "title": None, "axis": {"labelLimit": 300}},
                      "x": {"field": "ppt", "type": "quantitative", "title": bi("Schüler je Lehrer", "Pupils per teacher")},
                      "tooltip": [ttf("area", "Gebiet", "Area"), {"field": "ppt", "title": bi("Schüler je Lehrer", "Pupils per teacher"), "format": ".1f"}, tt("pupils_1868", "Schüler", "Pupils"), tt("teachers", "Lehrer", "Teachers")]}},
                 {"mark": {"type": "rule", "strokeDash": [4, 3]}, "encoding": {"x": {"datum": 50}}},
             ]}},
        {"id": "c2", "dataset": "schools",
         "title": bi("Veränderung der Schülerzahl 1863–1868", "Change in pupil numbers 1863–1868"),
         "caption": bi("Prozent; die Stadt Gera wächst am stärksten.", "Per cent; the town of Gera grows most."),
         "vegalite": {
             "height": 280,
             "mark": "bar",
             "encoding": {
                 "y": {"field": F("area"), "type": "nominal", "sort": "-x", "title": None, "axis": {"labelLimit": 300}},
                 "x": {"field": "growth_pct", "type": "quantitative", "title": bi("Veränderung (%)", "Change (%)")},
                 "tooltip": [ttf("area", "Gebiet", "Area"), {"field": "growth_pct", "title": bi("Veränderung (%)", "Change (%)"), "format": ".1f"}, tt("pupils_1863", "Schüler 1863", "Pupils 1863"), tt("pupils_1868", "Schüler 1868", "Pupils 1868")]}}},
        {"id": "c3", "dataset": "schools",
         "title": bi("Schüler in Prozent der Einwohner", "Pupils as a percentage of inhabitants"),
         "caption": bi("Nach Brückners Zahl der Einwohner je Schüler (100 : Einwohner je Schüler).", "Based on Brückner's number of inhabitants per pupil (100 : inhabitants per pupil)."),
         "vegalite": {
             "height": 280,
             "mark": "bar",
             "encoding": {
                 "y": {"field": F("area"), "type": "nominal", "sort": "-x", "title": None, "axis": {"labelLimit": 300}},
                 "x": {"field": "pop_share", "type": "quantitative", "title": bi("Schüler (% der Einwohner)", "Pupils (% of inhabitants)")},
                 "tooltip": [ttf("area", "Gebiet", "Area"), {"field": "pop_share", "title": bi("% der Einwohner", "% of inhabitants"), "format": ".1f"}, tt("inh_per_pupil", "Einwohner je Schüler", "Inhabitants per pupil")]}}},
    ],
    "related": ["bevoelkerung-stadt-land-1833-1867"],
    "keywords": {"de": ["Volksschule", "Schüler", "Lehrer", "Schulstatistik", "Klassenstärke", "Schulbesuch", "Gera", "Schleiz", "Lobenstein"],
                 "en": ["elementary school", "pupils", "teachers", "school statistics", "class size", "school attendance", "Gera", "Schleiz", "Lobenstein"]},
    "transcription_issues": [],
}
ana.pop("transcription_issues")
write(ana)
