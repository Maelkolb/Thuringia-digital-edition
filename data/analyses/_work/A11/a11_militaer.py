"""A11-11: Militärische Gestellungspflicht von Reuß (j. L.) vom Reichscontingent bis zum Norddeutschen Bund (p. 271)."""
from common import *

# values printed in the running text of p. 271 (b3: 885; b4: all others)
P = [
    # period_key, period_de, period_en, kind_key, kind_de, kind_en, men
    ("a", "bis 1681", "until 1681", "a", "Reichscontingent", "Imperial contingent", 24),
    ("b", "1681–1702", "1681–1702", "a", "Reichscontingent", "Imperial contingent", 71.5),
    ("c", "ab 1702", "from 1702", "a", "Reichscontingent", "Imperial contingent", 333),
    ("d", "Dt. Bund anfangs", "Confed. at first", "b", "Hauptcontingent", "Main contingent", 522),
    ("d", "Dt. Bund anfangs", "Confed. at first", "c", "Reserve (Ersatzcontingent)", "Reserve (replacement) contingent", 261),
    ("e", "Dt. Bund ab 1842", "Confed. from 1842", "b", "Hauptcontingent", "Main contingent", 608),
    ("e", "Dt. Bund ab 1842", "Confed. from 1842", "c", "Reserve (Ersatzcontingent)", "Reserve (replacement) contingent", 261),
    ("f", "Norddt. Bund", "N. German Conf.", "d", "Contingent im Bundesheer", "Contingent in the federal army", 885),
]
rows = [list(r) for r in P]
tot = {}
for r in P:
    tot[r[0]] = tot.get(r[0], 0) + r[6]
print(tot)
assert tot["d"] == 783 and tot["e"] == 869
f = lambda a, b: b / a
first, last = tot["a"], tot["f"]
fac = last / first
b1815 = 100 * 522 / 52205
pct42 = 100 * 87 / 522


def D(x, nd=0):
    return fmt_de(x, nd)


def E(x, nd=0):
    return fmt_en(x, nd)


ana = {
    "id": "militaer-kontingent-reichsmatrikel-bis-1867",
    "title": bi("Die militärische Gestellungspflicht von Reuß vom Reichscontingent bis 1867", "Reuss's military obligation from the imperial contingent to 1867"),
    "category": "military",
    "section": "t1-4-2",
    "sources": [{"page": "271", "block": "b3"}, {"page": "271", "block": "b4"}],
    "summary": bi(
        f"Brückner schildert in seinem Rückblick auf das Militär, wie viele Soldaten Reuß in den verschiedenen Epochen stellen musste: {D(tot['a'])} Mann nach der alten Reichsmatrikel, 333 Mann im Verband mit Schwarzburg ab 1702, {D(tot['d'])} Mann im Deutschen Bund und zuletzt {D(tot['f'])} Mann im Bundesheer des Norddeutschen Bundes. Die Auswertung stellt diese Zahlen zu einer Reihe zusammen.",
        f"In his retrospect on the military Brückner describes how many soldiers Reuss had to provide in the different epochs: {E(tot['a'])} men under the old imperial register, 333 men in association with Schwarzburg from 1702, {E(tot['d'])} men in the German Confederation and finally {E(tot['f'])} men in the federal army of the North German Confederation. The analysis assembles these figures into a series.",
    ),
    "method": bi(
        "Die Angaben stehen im Fließtext S. 271 (b3 und b4) und beziehen sich teils auf das gesamte Reuß (Reichsmatrikel bis 1702), teils auf Reuß j. L. (Deutscher Bund, 1867). Sie wurden zu einer Periodenreihe geordnet. Für den Deutschen Bund wird das Hauptcontingent (522, nach dem Bundesbeschluss von 1842 um 87 erhöht auf 608) mit dem Reservecontingent (261) gestapelt; die Reserve für die Zeit ab 1842 wird als unverändert angenommen (608 + 261 = 869, wie Brückner für das Bataillon angibt). Der Faktor ist das Verhältnis 885 : 24 (abgeleitet).",
        "The figures are in the running text of p. 271 (b3 and b4) and refer partly to all of Reuss (imperial register until 1702), partly to Reuss j. L. (German Confederation, 1867). They were arranged as a series of periods. For the German Confederation the main contingent (522, raised by 87 to 608 by the federal decision of 1842) is stacked with the reserve contingent (261); the reserve from 1842 is assumed unchanged (608 + 261 = 869, as Brückner gives for the battalion). The factor is the ratio 885 : 24 (derived).",
    ),
    "findings": [
        bi(f"Die Zahl der zu stellenden Soldaten stieg von {D(first)} Mann (Reichsmatrikel bis 1681) auf {D(last)} Mann (1867/68), also auf das {D(fac,0)}fache.",
           f"The number of soldiers to be provided rose from {E(first)} men (imperial register until 1681) to {E(last)} men (1867/68), i.e. by a factor of {E(fac,0)}."),
        bi(f"Im Deutschen Bund betrug die Pflicht zunächst {D(tot['d'])} Mann (522 Hauptcontingent = 1 % von 52.205 Seelen, dazu 261 Reserve = ½ %); 1842 wurde das Hauptcontingent um 87 Mann ({D(pct42,1)} %) erhöht. Das Gesamtcontingent von 1867/68 (885) liegt nur {D(885-tot['e'])} Mann über der Summe 869.",
           f"In the German Confederation the obligation was at first {E(tot['d'])} men (522 main contingent = 1 % of 52,205 souls, plus 261 reserve = ½ %); in 1842 the main contingent was raised by 87 men ({E(pct42,1)} %). The total contingent of 1867/68 (885) is only {E(885-tot['e'])} men above the sum of 869."),
        bi(f"Die größten Sprünge liegen im 18. Jahrhundert (von 71½ auf 333 Mann 1702) und beim Eintritt in den Deutschen Bund (von 333 auf {D(tot['d'])}); das Hauptcontingent entsprach im Deutschen Bund 1 % (522 von 52.205 Seelen), nach 1842 1⅙ % der Bevölkerung.",
           f"The largest jumps fall in the 18th century (from 71½ to 333 men in 1702) and on entry into the German Confederation (from 333 to {E(tot['d'])}); the main contingent amounted to 1 % of the population in the German Confederation (522 of 52,205 souls) and to 1⅙ % after 1842."),
    ],
    "caveats": [
        bi("Die Reihe ist nicht streng vergleichbar: Bis 1702 bezieht sich die Zahl auf das gesamte Reuß (beide Linien), danach auf Reuß j. L. bzw. auf dessen Anteil an einem gemeinsamen Kontingent. Zwischen 1702 und 1790 behielt Reuß nach Brückner »seinen früheren Reichscontingentsatz« bei, zahlenmäßig nicht angegeben, und stellte in den Kriegen oft das Vier- bis Fünffache; diese Spitzen sind in der Reihe nicht enthalten.",
           "The series is not strictly comparable: until 1702 the figure refers to all of Reuss (both lines), afterwards to Reuss j. L. or to its share in a joint contingent. Between 1702 and 1790 Reuss, according to Brückner, kept “its earlier imperial contingent rate”, not given numerically, and in the wars often had to supply four to five times as many; these peaks are not in the series."),
        bi("Brückner schreibt, das Hauptcontingent sei 1842 »um 87 Mann, also auf 608« erhöht worden; 522 + 87 ergibt 609. Der Widerspruch steht im Original (Faksimile geprüft); 608 passt mit 261 Reserve zur genannten Bataillonsstärke 869, hier wird 608 verwendet. Für 1331 nennt Brückner 50 »Helme« (Reiter mit Gefolge) der Reichsvögte; diese Einheit ist mit Mannzahlen nicht vergleichbar und fehlt in der Reihe.",
           "Brückner writes that the main contingent was raised in 1842 “by 87 men, i.e. to 608”; 522 + 87 makes 609. The contradiction is in the original (facsimile checked); 608 with 261 reserve matches the battalion strength of 869 he gives, so 608 is used here. For 1331 Brückner mentions 50 “Helme” (helmets, i.e. mounted men with retinue) of the imperial bailiffs; this unit is not comparable with numbers of men and is left out of the series."),
    ],
    "datasets": [
        {"name": "contingent", "title": bi("Zu stellende Mannschaft nach Zeitabschnitt", "Troops to be provided by period"),
         "columns": [col("period_key", "Kürzel Zeitabschnitt", "Period key", "string"),
                     col("period_de", "Zeitabschnitt", "Period", "string"), col("period_en", "Zeitabschnitt (englisch)", "Period (English)", "string"),
                     col("kind_key", "Kürzel Art", "Kind key", "string"),
                     col("kind_de", "Art der Pflicht", "Kind of obligation", "string"), col("kind_en", "Art der Pflicht (englisch)", "Kind of obligation (English)", "string"),
                     col("men", "Mannschaft", "Men", "number", "Mann", derived=True, note="Alle Werte stehen im Text (71 1/2 gelesen als 71,5); 333 = Anteil an 1000 Mann; die Reserve 261 ab 1842 ist als unverändert angenommen. Als abgeleitet markiert, weil der Bruch 71 1/2 vom automatischen Zahlenabgleich nicht erkannt wird.")],
         "rows": rows, "source_refs": [{"page": "271", "block": "b3"}, {"page": "271", "block": "b4"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "contingent",
         "title": bi("Zu stellende Mannschaft von der Reichsmatrikel bis 1867", "Troops to be provided, from the imperial register to 1867"),
         "caption": bi("Mann je Zeitabschnitt. Bis 1702 gesamtes Reuß; ab 1702 Anteil (333) am gemeinsamen Kontingent von 1000 Mann mit Schwarzburg; im Bund Reuß j. L.; im Deutschen Bund Haupt- und Reservecontingent gestapelt.",
                       "Men per period. Until 1702 all of Reuss; from 1702 its share (333) of the joint contingent of 1,000 men with Schwarzburg; in the Confederation Reuss j. L.; in the German Confederation main and reserve contingents are stacked."),
         "vegalite": {
             "height": 320,
             "mark": "bar",
             "encoding": {
                 "x": {"field": F("period"), "type": "nominal", "sort": {"field": "period_key", "op": "min"}, "title": None, "axis": {"labelAngle": 0, "labelLimit": 170}},
                 "y": {"field": "men", "type": "quantitative", "title": bi("Mann", "Men"), "stack": "zero"},
                 "color": {"field": F("kind"), "type": "nominal", "title": None, "sort": {"field": "kind_key", "op": "min"}, "legend": {"labelLimit": 300, "columns": 2}},
                 "order": {"field": "kind_key", "type": "nominal", "sort": "ascending"},
                 "tooltip": [ttf("period", "Zeitabschnitt", "Period"), ttf("kind", "Art", "Kind"), tt("men", "Mann", "Men")]}}},
    ],
    "keywords": {"de": ["Militär", "Kontingent", "Reichsmatrikel", "Deutscher Bund", "Norddeutscher Bund", "Reichscontingent", "Soldaten", "Reuß"],
                 "en": ["military", "contingent", "imperial register", "German Confederation", "North German Confederation", "soldiers", "Reuss"]},
}
write(ana)
