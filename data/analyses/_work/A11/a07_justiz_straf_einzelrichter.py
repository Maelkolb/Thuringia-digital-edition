"""A11-07: Strafrechtspflege vor den Einzelrichtern 1864-1867 (p. 287)."""
from common import *

g4 = grid("287", "b4")
g6 = grid("287", "b6")
assert [r[0] for r in g4[2:]] == ["1864", "1865", "1866", "1867"]
N = lambda x: num(x) or 0

# --- year series of convictions for Uebertretungen (b4) ---------------------------------
years = {int(r[0]): [N(r[1]), N(r[2]), N(r[3]), N(r[4])] for r in g4[2:]}
for y, (a, b, c, s) in years.items():
    assert a + b + c == s, (y, a, b, c, s)
CAT = [("a", "Gemeine Übertretungen", "Common offences"), ("b", "Polizeiliche Übertretungen", "Police offences"), ("c", "Injurien", "Insults")]
yearly = []
for y in sorted(years):
    for (k, de, en), v in zip(CAT, years[y][:3]):
        yearly.append([y, k, de, en, v])

# --- 1867 by court (b6) -------------------------------------------------------------------
idx = {r[0].strip().rstrip(".").strip(): r for r in g6[2:]}
names = ["Gera I", "Gera II", "Hohenleuben", "Schleiz I", "Schleiz II", "Lobenstein I", "Lobenstein II", "Hirschberg"]
rows8 = {n: [N(x) for x in idx[n][1:]] for n in names}
tot = [N(x) for x in g6[12][1:]]
for i in range(14):
    assert sum(r[i] for r in rows8.values()) == tot[i], i
print(tot)
# columns (0-based within [1:]): 0 anz, 1 anz_forst, 2 verurt_gem, 3 verurt_forst, 4 frei_gem, 5 pol_verurt, 6 pol_frei, 7 defr_v, 8 defr_f, 9 ehre_v, 10 ehre_f, 11 summe, 12 hv, 13 tage
courts_long = []
courts = []
for n in names:
    r = rows8[n]
    forst, gem = r[3], r[2]
    sonst = gem - forst
    courts.append([n, gem, forst, sonst, round(100 * forst / gem, 1)])
    courts_long.append([n, "a", "Forstdiebstahl", "Forest theft", forst])
    courts_long.append([n, "b", "Übrige gemeine Übertretungen", "Other common offences", sonst])

# --- acquittals 1867 by offence group
ACQ = [
    ("a", "Gemeine Übertretungen", "Common offences", tot[2], tot[4]),
    ("b", "Polizeiliche Übertretungen", "Police offences", tot[5], tot[6]),
    ("c", "Defraudationen", "Defraudations", tot[7], tot[8]),
    ("d", "Ehrenkränkungen", "Insults to honour", tot[9], tot[10]),
]
acq = [[k, de, en, v, f, v + f, round(100 * f / (v + f), 1)] for k, de, en, v, f in ACQ]
print(acq)

# --- numbers for the text ------------------------------------------------------------------
pct = lambda a, b: 100 * a / b
S = {y: years[y][3] for y in years}
G = {y: years[y][0] for y in years}
P = {y: years[y][1] for y in years}
I = {y: years[y][2] for y in years}
row66 = [N(x) for x in g6[13][1:]]
forst66, gem66 = row66[3], row66[2]
forst_share67 = pct(tot[3], tot[2])
forst_share66 = pct(forst66, gem66)
by_share = sorted(courts, key=lambda c: c[4])
lob1 = [c for c in courts if c[0] == "Lobenstein I"][0]
kg_schleiz_forst = sum(rows8[n][3] for n in ["Schleiz I", "Schleiz II", "Lobenstein I", "Lobenstein II", "Hirschberg"])
print(forst_share67, forst_share66, by_share[0], by_share[-1], kg_schleiz_forst, pct(kg_schleiz_forst, tot[3]))


def D(x, nd=0):
    return fmt_de(x, nd)


def E(x, nd=0):
    return fmt_en(x, nd)


ana = {
    "id": "justiz-strafsachen-einzelrichter-uebertretungen-1864-1867",
    "title": bi("Strafrechtspflege vor den Einzelrichtern: Verurteilungen wegen Übertretungen 1864–1867", "Criminal justice before the single judges: convictions for minor offences, 1864–1867"),
    "category": "justice",
    "section": "t1-4-4",
    "sources": [{"page": "287", "block": "b4", "rows": "r3-r6"}, {"page": "287", "block": "b6", "rows": "r3-r14"}, {"page": "289", "block": "b1"}],
    "summary": bi(
        f"Vor den Einzelrichtern der Justizämter wurden 1867 insgesamt {D(S[1867])} Personen wegen Übertretungen verurteilt (1864: {D(S[1864])}). Brückner gliedert nach gemeinen, polizeilichen Übertretungen und Injurien und weist für 1867 die acht Gerichte einzeln aus. Die Auswertung zeigt den Anstieg, den hohen Anteil des Forstdiebstahls und die Unterschiede zwischen den Gerichtsbezirken.",
        f"Before the single judges of the Justizämter {E(S[1867])} persons were convicted of minor offences in 1867 (1864: {E(S[1864])}). Brückner distinguishes common offences, police offences and insults and lists the eight courts separately for 1867. The analysis shows the rise, the high share of forest theft and the differences between the court districts.",
    ),
    "method": bi(
        "Quelle sind die Tabellen »Allgemein für 1864 bis 1867« (S. 287, b4: Verurteilte nach Gruppen) und »Speciell für 1867« (S. 287, b6: je Gericht). Die Summenzeilen der beiden Kreisgerichtsbezirke wurden nicht als eigene Gerichte gezählt; die acht Justizämter addieren sich zur gedruckten Hauptsumme. Der Anteil des Forstdiebstahls = Verurteilungen wegen Forstdiebstahls : Verurteilungen wegen gemeiner Übertretungen (abgeleitet). Freispruchsanteil = Freisprüche : (Verurteilte + Freigesprochene).",
        "The sources are the tables “General for 1864 to 1867” (p. 287, b4: convicted by group) and “Special for 1867” (p. 287, b6: by court). The subtotal rows of the two Kreisgericht districts were not counted as separate courts; the eight Justizämter add up to the printed grand total. The share of forest theft = convictions for forest theft : convictions for common offences (derived). Acquittal share = acquittals : (convicted + acquitted).",
    ),
    "findings": [
        bi(f"Die Verurteilungen wegen Übertretungen stiegen von {D(S[1864])} (1864) auf {D(S[1867])} (1867), also um {D(pct(S[1867]-S[1864], S[1864]),1)} %; bei den gemeinen Übertretungen um {D(pct(G[1867]-G[1864], G[1864]),1)} % ({D(G[1864])} auf {D(G[1867])}), bei den Injurien um {D(pct(I[1867]-I[1864], I[1864]),1)} %, bei den polizeilichen nur um {D(pct(P[1867]-P[1864], P[1864]),1)} %.",
           f"Convictions for minor offences rose from {E(S[1864])} (1864) to {E(S[1867])} (1867), i.e. by {E(pct(S[1867]-S[1864], S[1864]),1)} %; common offences by {E(pct(G[1867]-G[1864], G[1864]),1)} % ({E(G[1864])} to {E(G[1867])}), insults by {E(pct(I[1867]-I[1864], I[1864]),1)} %, police offences by only {E(pct(P[1867]-P[1864], P[1864]),1)} %."),
        bi(f"Forstdiebstahl macht {D(forst_share67,1)} % der Verurteilungen wegen gemeiner Übertretungen aus ({D(tot[3])} von {D(tot[2])}); 1866 waren es {D(forst_share66,1)} % ({D(forst66)} von {D(gem66)}).",
           f"Forest theft accounts for {E(forst_share67,1)} % of the convictions for common offences ({E(tot[3])} of {E(tot[2])}); in 1866 it was {E(forst_share66,1)} % ({E(forst66)} of {E(gem66)})."),
        bi(f"Der Anteil schwankt stark zwischen den Gerichten: {D(by_share[0][4],1)} % in {by_share[0][0]}, aber {D(by_share[-1][4],1)} % in {by_share[-1][0]}. Die fünf Gerichte im Bezirk des Kreisgerichts Schleiz stellen {D(pct(kg_schleiz_forst, tot[3]),1)} % aller Forstdiebstahl-Verurteilungen; allein Lobenstein I zählt {D(lob1[2])}.",
           f"The share varies strongly between the courts: {E(by_share[0][4],1)} % in {by_share[0][0]}, but {E(by_share[-1][4],1)} % in {by_share[-1][0]}. The five courts in the Kreisgericht Schleiz district account for {E(pct(kg_schleiz_forst, tot[3]),1)} % of all forest-theft convictions; Lobenstein I alone counts {E(lob1[2])}."),
        bi(f"Bei den Ehrenkränkungen endeten {D(acq[3][6],1)} % der Verfahren mit Freispruch, bei gemeinen ({D(acq[0][6],1)} %) und polizeilichen Übertretungen ({D(acq[1][6],1)} %) nur rund jedes zwanzigste.",
           f"For insults to honour {E(acq[3][6],1)} % of the proceedings ended in acquittal, against only about one in twenty for common ({E(acq[0][6],1)} %) and police offences ({E(acq[1][6],1)} %)."),
    ],
    "caveats": [
        bi("Gezählt werden verurteilte Personen; die »Anzeigen« in der Tabelle für 1867 sind nicht direkt mit den Verurteilten vergleichbar (in einzelnen Gerichten übersteigen die Verurteilten die Anzeigen). Defraudationen (Zoll- und Steuerhinterziehung) sind nur mit 3 Verurteilten und 6 Freigesprochenen vertreten, ihre Quote ist statistisch bedeutungslos.",
           "The count is of convicted persons; the “reports” (Anzeigen) in the 1867 table are not directly comparable with the convicted (in some courts the convicted exceed the reports). Defraudations (customs and tax evasion) appear with only 3 convicted and 6 acquitted; their rate is statistically meaningless."),
        bi("Brückner nennt für 1867 eine Steigerung »gleichmäßig in allen Rubriken … (die Defraudationen ausgenommen)« und wertet die hiesigen Verhältnisse im Vergleich mit den ernestinischen und schwarzburgischen Landen als günstig (S. 289). Für 1864/65 liegen nur die Summen nach Gruppen vor, keine Zahlen für Freisprüche oder Forstdiebstahl.",
           "Brückner reports for 1867 an increase “uniformly in all heads … (defraudations excepted)” and judges conditions here as favourable compared with the Ernestine and Schwarzburg territories (p. 289). For 1864/65 only the totals by group are given, no figures for acquittals or forest theft."),
    ],
    "datasets": [
        {"name": "yearly", "title": bi("Verurteilte wegen Übertretungen nach Gruppe und Jahr", "Persons convicted of minor offences by group and year"),
         "columns": [
             col("year", "Jahr", "Year", "integer"),
             col("group_key", "Kürzel", "Key", "string"),
             col("group_de", "Gruppe", "Group", "string"), col("group_en", "Gruppe (englisch)", "Group (English)", "string"),
             col("convicted", "Verurteilte", "Convicted", "integer", "Personen"),
         ],
         "rows": yearly, "source_refs": [{"page": "287", "block": "b4", "rows": "r3-r6"}]},
        {"name": "courts", "title": bi("Verurteilungen wegen gemeiner Übertretungen 1867 nach Gericht", "Convictions for common offences in 1867 by court"),
         "columns": [
             col("court", "Gericht", "Court", "string"),
             col("convicted", "Verurteilte (gemeine Übertretungen)", "Convicted (common offences)", "integer", "Personen"),
             col("forest", "davon wegen Forstdiebstahls", "of which for forest theft", "integer", "Personen"),
             col("other", "übrige gemeine Übertretungen", "other common offences", "integer", "Personen", derived=True),
             col("forest_share", "Anteil Forstdiebstahl", "Share of forest theft", "number", "%", derived=True),
         ],
         "rows": courts, "source_refs": [{"page": "287", "block": "b6", "rows": "r3-r14"}]},
        {"name": "courts_long", "title": bi("Gemeine Übertretungen 1867, Forstdiebstahl und Übrige (lang)", "Common offences in 1867, forest theft and other (long format)"),
         "columns": [
             col("court", "Gericht", "Court", "string"),
             col("part_key", "Kürzel", "Key", "string"),
             col("part_de", "Art", "Kind", "string"), col("part_en", "Art (englisch)", "Kind (English)", "string"),
             col("convicted", "Verurteilte", "Convicted", "integer", "Personen", derived=True, note="Forstdiebstahl gedruckt; »Übrige« = gemeine − Forstdiebstahl"),
         ],
         "rows": courts_long, "source_refs": [{"page": "287", "block": "b6", "rows": "r3-r14"}]},
        {"name": "acquittals", "title": bi("Verurteilte und Freigesprochene 1867 nach Gruppe", "Convicted and acquitted in 1867 by group"),
         "columns": [
             col("group_key", "Kürzel", "Key", "string"),
             col("group_de", "Gruppe", "Group", "string"), col("group_en", "Gruppe (englisch)", "Group (English)", "string"),
             col("convicted", "Verurteilte", "Convicted", "integer", "Personen"),
             col("acquitted", "Freigesprochene", "Acquitted", "integer", "Personen"),
             col("total", "Verurteilte und Freigesprochene", "Convicted and acquitted", "integer", "Personen", derived=True),
             col("acquitted_share", "Anteil der Freisprüche", "Share of acquittals", "number", "%", derived=True),
         ],
         "rows": acq, "source_refs": [{"page": "287", "block": "b6", "rows": "r13"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "yearly",
         "title": bi("Verurteilte wegen Übertretungen vor den Einzelrichtern", "Persons convicted of minor offences before the single judges"),
         "caption": bi("Personen je Jahr nach Gruppe; alle Justizämter zusammen.", "Persons per year by group; all Justizämter together."),
         "vegalite": {
             "height": 280,
             "mark": {"type": "bar", "width": 55},
             "encoding": {
                 "x": {"field": "year", "type": "ordinal", "title": bi("Jahr", "Year"), "axis": {"labelAngle": 0}},
                 "y": {"field": "convicted", "type": "quantitative", "title": bi("Verurteilte", "Convicted"), "stack": "zero"},
                 "color": {"field": F("group"), "type": "nominal", "title": None, "sort": {"field": "group_key", "op": "min"}, "legend": {"labelLimit": 400}},
                 "order": {"field": "group_key", "type": "nominal", "sort": "ascending"},
                 "tooltip": [tt("year", "Jahr", "Year"), ttf("group", "Gruppe", "Group"), tt("convicted", "Verurteilte", "Convicted")]}}},
        {"id": "c2", "dataset": "courts_long",
         "title": bi("Gemeine Übertretungen 1867: Forstdiebstahl und Übriges", "Common offences in 1867: forest theft and the rest"),
         "caption": bi("Verurteilte Personen je Justizamt. In Lobenstein, Hirschberg und Hohenleuben dominiert der Forstdiebstahl, in Gera I spielt er kaum eine Rolle.",
                       "Convicted persons per Justizamt. In Lobenstein, Hirschberg and Hohenleuben forest theft dominates, in Gera I it hardly plays a role."),
         "vegalite": {
             "height": 300,
             "mark": "bar",
             "encoding": {
                 "y": {"field": "court", "type": "nominal", "title": None, "sort": {"field": "convicted", "op": "sum", "order": "descending"}},
                 "x": {"field": "convicted", "type": "quantitative", "title": bi("Verurteilte", "Convicted"), "stack": "zero"},
                 "color": {"field": F("part"), "type": "nominal", "title": None, "sort": {"field": "part_key", "op": "min"}, "legend": {"labelLimit": 400}},
                 "order": {"field": "part_key", "type": "nominal", "sort": "ascending"},
                 "tooltip": [tt("court", "Gericht", "Court"), ttf("part", "Art", "Kind"), tt("convicted", "Verurteilte", "Convicted")]}}},
        {"id": "c3", "dataset": "courts",
         "title": bi("Anteil des Forstdiebstahls an den gemeinen Übertretungen, 1867", "Share of forest theft among common offences, 1867"),
         "caption": bi("Prozent der Verurteilten wegen gemeiner Übertretungen.", "Per cent of those convicted of common offences."),
         "vegalite": {
             "height": 280,
             "mark": "bar",
             "encoding": {
                 "y": {"field": "court", "type": "nominal", "title": None, "sort": "-x"},
                 "x": {"field": "forest_share", "type": "quantitative", "title": bi("Anteil Forstdiebstahl (%)", "Share of forest theft (%)"), "scale": {"domain": [0, 100]}},
                 "tooltip": [tt("court", "Gericht", "Court"), {"field": "forest_share", "title": bi("Anteil (%)", "Share (%)"), "format": ".1f"}, tt("forest", "Forstdiebstahl", "Forest theft"), tt("convicted", "gemeine Übertretungen", "Common offences")]}}},
        {"id": "c4", "dataset": "acquittals",
         "title": bi("Freisprüche nach Gruppe, 1867", "Acquittals by group, 1867"),
         "caption": bi("Anteil der Freigesprochenen an Verurteilten und Freigesprochenen (Prozent). Die Defraudationen (nur neun Fälle) sind nicht dargestellt.",
                       "Share of acquitted among convicted and acquitted (per cent). Defraudations (only nine cases) are not shown."),
         "vegalite": {
             "height": 160,
             "transform": [{"filter": "datum.total >= 30"}],
             "mark": "bar",
             "encoding": {
                 "y": {"field": F("group"), "type": "nominal", "title": None, "sort": {"field": "group_key", "op": "min"}, "axis": {"labelLimit": 300}},
                 "x": {"field": "acquitted_share", "type": "quantitative", "title": bi("Freisprüche (%)", "Acquittals (%)"), "scale": {"domain": [0, 100]}},
                 "tooltip": [ttf("group", "Gruppe", "Group"), {"field": "acquitted_share", "title": bi("Freisprüche (%)", "Acquittals (%)"), "format": ".1f"}, tt("convicted", "Verurteilte", "Convicted"), tt("acquitted", "Freigesprochene", "Acquitted")]}}},
    ],
    "keywords": {"de": ["Strafrechtspflege", "Übertretungen", "Forstdiebstahl", "Forstfrevel", "Verurteilungen", "Injurien", "Kriminalität", "Einzelrichter", "Lobenstein"],
                 "en": ["criminal justice", "minor offences", "forest theft", "convictions", "insults", "crime", "single judge", "Lobenstein"]},
}
write(ana)
