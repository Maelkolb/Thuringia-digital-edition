"""A11-19: Staatliche und medizinische Versorgung nach Landestheilen: Gendarmen, Ärzte, Justizämter je 10.000 Einwohner (pp. 273-274, 280; Einwohner 1867 von p. 95)."""
from common import *

# population 1867 by Landestheil: p. 95 b4 rows r7 (Gera), r13 (Schleiz), r19 (Lobenstein-Ebersdorf)
g95 = grid("95", "b4")
pop = {}
for r in g95:
    if r[0] == "1867":
        pop[len(pop)] = int(num(r[3]))
print(pop)
POP = [pop[0], pop[1], pop[2]]
assert POP == [38252, 27368, 22354], POP

REG = [("a", "Gera", "Gera"), ("b", "Schleiz", "Schleiz"), ("c", "Lobenstein-Ebersdorf", "Lobenstein-Ebersdorf")]
GEND = [7, 9, 8]          # p. 273 b3 : 7 Unterland, 9 Schleiz, 8 Lobenstein-Ebersdorf (total 24)
DOC = [14, 10, 8]         # p. 274 b1 : promovirte Aerzte Gera 14, Schleiz 10, Lobenstein-Ebersdorf 8
JA = [3, 2, 3]           # p. 280 b5 / p. 281 b1 : Justizaemter Gera (I, II) + Hohenleuben; Schleiz I, II; Lobenstein I, II + Hirschberg
assert sum(GEND) == 24 and sum(DOC) == 32 and sum(JA) == 8
MEAS = [("a", "Gendarmen", "Gendarmes", GEND), ("b", "Promovierte Ärzte", "Qualified physicians", DOC), ("c", "Justizämter", "Justizämter", JA)]
counts = []
rates = []
for mk, mde, men, vals in MEAS:
    for (rk, rde, ren), v, p in zip(REG, vals, POP):
        counts.append([rk, rde, ren, mk, mde, men, v])
        rates.append([rk, rde, ren, mk, mde, men, v, p, round(10000 * v / p, 2)])
pop_rows = [[rk, rde, ren, p] for (rk, rde, ren), p in zip(REG, POP)]
print(rates)
tot_pop = sum(POP)
insh = [round(p / d) for p, d in zip(POP, DOC)]
print(insh, tot_pop, 10000 * 24 / tot_pop, 10000 * 32 / tot_pop)
gend_rate = [r[8] for r in rates if r[3] == "a"]
doc_rate = [r[8] for r in rates if r[3] == "b"]
ja_rate = [r[8] for r in rates if r[3] == "c"]


def D(x, nd=0):
    return fmt_de(x, nd)


def E(x, nd=0):
    return fmt_en(x, nd)


ana = {
    "id": "verwaltung-aerzte-gendarmen-justizaemter-landestheile",
    "title": bi("Ärzte, Gendarmen und Justizämter in den drei Landestheilen", "Physicians, gendarmes and Justizämter in the three regions"),
    "category": "state",
    "section": "t1-4-3",
    "sources": [{"page": "273", "block": "b3"}, {"page": "274", "block": "b1"}, {"page": "280", "block": "b5"}, {"page": "281", "block": "b1"}, {"page": "95", "block": "b4", "rows": "r7, r13, r19", "note": "Einwohner 1867 je Landestheil"}],
    "summary": bi(
        f"Brückner nennt für die drei Landestheile Gera, Schleiz und Lobenstein-Ebersdorf die Zahl der Gendarmen (zusammen 24), der promovierten Ärzte (zusammen 32) und die Justizämter (acht). Setzt man diese Zahlen zu den Einwohnern 1867 in Beziehung, zeigt sich, wie gleichmäßig die ärztliche Versorgung, wie ungleich dagegen Gendarmerie und Gerichtsorganisation über das Land verteilt waren.",
        f"For the three regions Gera, Schleiz and Lobenstein-Ebersdorf Brückner gives the number of gendarmes (24 in total), qualified physicians (32 in total) and the Justizämter (eight). Related to the 1867 population this shows how evenly medical provision, but how unevenly the gendarmerie and the court organisation, were spread over the country.",
    ),
    "method": bi(
        "Gendarmen (S. 273: 7 Unterland, 9 Schleiz, 8 Lobenstein-Ebersdorf) und Ärzte (S. 274: 14, 10, 8) stehen im Fließtext; die Justizämter wurden aus der Aufzählung S. 280–281 den Landestheilen zugeordnet (Gera: Gera I, II und Hohenleuben; Schleiz: Schleiz I und II; Lobenstein-Ebersdorf: Lobenstein I, II und Hirschberg). Die Einwohnerzahlen 1867 (38.252; 27.368; 22.354) stammen aus der Bevölkerungstabelle S. 95. Raten je 10.000 Einwohner und Einwohner je Arzt sind abgeleitet.",
        "Gendarmes (p. 273: 7 Unterland, 9 Schleiz, 8 Lobenstein-Ebersdorf) and physicians (p. 274: 14, 10, 8) are in the running text; the Justizämter were assigned to the regions from the list on pp. 280–281 (Gera: Gera I, II and Hohenleuben; Schleiz: Schleiz I and II; Lobenstein-Ebersdorf: Lobenstein I, II and Hirschberg). The 1867 population figures (38,252; 27,368; 22,354) come from the population table on p. 95. Rates per 10,000 inhabitants and inhabitants per physician are derived.",
    ),
    "findings": [
        bi(f"Auf einen promovierten Arzt kommen in allen drei Landestheilen fast gleich viele Einwohner: {D(insh[0])} (Gera), {D(insh[1])} (Schleiz) und {D(insh[2])} (Lobenstein-Ebersdorf), also {D(doc_rate[0],1)}, {D(doc_rate[1],1)} und {D(doc_rate[2],1)} Ärzte je 10.000 Einwohner.",
           f"In all three regions there are almost the same number of inhabitants per qualified physician: {E(insh[0])} (Gera), {E(insh[1])} (Schleiz) and {E(insh[2])} (Lobenstein-Ebersdorf), i.e. {E(doc_rate[0],1)}, {E(doc_rate[1],1)} and {E(doc_rate[2],1)} physicians per 10,000 inhabitants."),
        bi(f"Die Gendarmerie ist ungleicher verteilt: {D(gend_rate[0],1)} Gendarmen je 10.000 Einwohner im Landestheil Gera, aber {D(gend_rate[1],1)} in Schleiz und {D(gend_rate[2],1)} in Lobenstein-Ebersdorf. Eine mögliche Erklärung (Deutung): Die Stadt Gera untersteht nach Brückner unmittelbar dem Ministerium, die Gendarmerie ist den Landräten zugewiesen (S. 273).",
           f"The gendarmerie is distributed more unevenly: {E(gend_rate[0],1)} gendarmes per 10,000 inhabitants in the Gera region, but {E(gend_rate[1],1)} in Schleiz and {E(gend_rate[2],1)} in Lobenstein-Ebersdorf. One possible explanation (interpretation): according to Brückner the town of Gera is directly under the ministry, while the gendarmerie is assigned to the Landräte (p. 273)."),
        bi(f"Auf die acht Justizämter bezogen kommen auf ein Justizamt im Landestheil Gera {D(POP[0]/JA[0],0)}, in Schleiz {D(POP[1]/JA[1],0)} und in Lobenstein-Ebersdorf {D(POP[2]/JA[2],0)} Einwohner; Schleiz hat damit die größte Last je Amt.",
           f"Per Justizamt there are {E(POP[0]/JA[0],0)} inhabitants in the Gera region, {E(POP[1]/JA[1],0)} in Schleiz and {E(POP[2]/JA[2],0)} in Lobenstein-Ebersdorf; Schleiz thus has the largest burden per office."),
    ],
    "caveats": [
        bi("Die Zuordnung der Justizämter zu den Landestheilen und die Zahl der Landestheile folgen der Verwaltungseinteilung von 1868; die Gerichtsbezirke (Hohenleuben, Hirschberg, Saalburg, Tanna) decken sich nicht überall mit den Landestheilen. Die Zahlen der Ärzte betreffen nur promovierte Ärzte; Wundärzte, Hebammen und Tierärzte sind nicht gezählt. Brückner nennt keinen Stichtag.",
           "The assignment of the Justizämter to the regions and the number of regions follow the 1868 administrative division; the judicial districts (Hohenleuben, Hirschberg, Saalburg, Tanna) do not coincide everywhere with the regions. The figures for physicians concern only qualified physicians; surgeons, midwives and veterinary surgeons are not counted. Brückner gives no reference date."),
        bi("Die Einwohnerzahlen sind die der Volkszählung 1867 (S. 95), die Zahlen der Gendarmen und Ärzte beziehen sich auf den Stand der Beschreibung (1868/69). Die Einwohner des Landestheils Schleiz (27.368) schließen die Städte Schleiz, Tanna und Saalburg ein.",
           "The population figures are those of the 1867 census (p. 95), while the numbers of gendarmes and physicians refer to the state at the time of the description (1868/69). The inhabitants of the Schleiz region (27,368) include the towns of Schleiz, Tanna and Saalburg."),
    ],
    "datasets": [
        {"name": "rates", "title": bi("Gendarmen, Ärzte und Justizämter je 10.000 Einwohner", "Gendarmes, physicians and Justizämter per 10,000 inhabitants"),
         "columns": [col("region_key", "Kürzel", "Key", "string"), col("region_de", "Landestheil", "Region", "string"), col("region_en", "Landestheil (englisch)", "Region (English)", "string"),
                     col("measure_key", "Kürzel Messgröße", "Measure key", "string"), col("measure_de", "Messgröße", "Measure", "string"), col("measure_en", "Messgröße (englisch)", "Measure (English)", "string"),
                     col("count", "Anzahl", "Count", "integer", "Anzahl", derived=True, note="Gendarmen und Ärzte wie gedruckt; Justizämter aus der Aufzählung S. 280–281 den Landestheilen zugeordnet und gezählt"),
                     col("population", "Einwohner 1867", "Population 1867", "integer", "Einwohner"),
                     col("per_10000", "je 10.000 Einwohner", "per 10,000 inhabitants", "number", "je 10.000", derived=True)],
         "rows": rates, "source_refs": [{"page": "273", "block": "b3"}, {"page": "274", "block": "b1"}, {"page": "95", "block": "b4", "rows": "r7, r13, r19"}, {"page": "280", "block": "b5"}, {"page": "281", "block": "b1"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "rates",
         "title": bi("Gendarmen, Ärzte und Justizämter je Landestheil", "Gendarmes, physicians and Justizämter by region"),
         "caption": bi("Anzahl nach Brückner.", "Counts according to Brückner."),
         "vegalite": {
             "height": 260,
             "mark": "bar",
             "encoding": {
                 "x": {"field": F("region"), "type": "nominal", "title": None, "sort": {"field": "region_key", "op": "min"}, "axis": {"labelAngle": 0}},
                 "xOffset": {"field": F("measure"), "sort": {"field": "measure_key", "op": "min"}},
                 "y": {"field": "count", "type": "quantitative", "title": bi("Anzahl", "Count"), "axis": {"tickMinStep": 1, "format": "d"}},
                 "color": {"field": F("measure"), "type": "nominal", "title": None, "sort": {"field": "measure_key", "op": "min"}},
                 "tooltip": [ttf("region", "Landestheil", "Region"), ttf("measure", "Messgröße", "Measure"), tt("count", "Anzahl", "Count")]}}},
        {"id": "c2", "dataset": "rates",
         "title": bi("Je 10.000 Einwohner", "Per 10,000 inhabitants"),
         "caption": bi("Einwohner 1867 (S. 95). Die Zahl der Ärzte je 10.000 Einwohner ist überall fast gleich, bei Gendarmen und Justizämtern unterscheiden sich die Werte deutlich.", "Population of 1867 (p. 95). The number of physicians per 10,000 inhabitants is almost the same everywhere, while the values for gendarmes and Justizämter differ markedly."),
         "vegalite": {
             "height": 260,
             "mark": "bar",
             "encoding": {
                 "x": {"field": F("region"), "type": "nominal", "title": None, "sort": {"field": "region_key", "op": "min"}, "axis": {"labelAngle": 0}},
                 "xOffset": {"field": F("measure"), "sort": {"field": "measure_key", "op": "min"}},
                 "y": {"field": "per_10000", "type": "quantitative", "title": bi("je 10.000 Einwohner", "per 10,000 inhabitants")},
                 "color": {"field": F("measure"), "type": "nominal", "title": None, "sort": {"field": "measure_key", "op": "min"}},
                 "tooltip": [ttf("region", "Landestheil", "Region"), ttf("measure", "Messgröße", "Measure"), {"field": "per_10000", "title": bi("je 10.000", "per 10,000"), "format": ".2f"}, tt("population", "Einwohner", "Population")]}}},
    ],
    "related": ["bevoelkerung-stadt-land-1833-1867"],
    "keywords": {"de": ["Gendarmerie", "Ärzte", "Medizinalwesen", "Justizämter", "Landräte", "Verwaltung", "Landestheile", "Versorgung"],
                 "en": ["gendarmerie", "physicians", "medical services", "Justizämter", "administration", "regions", "provision"]},
}
write(ana)
