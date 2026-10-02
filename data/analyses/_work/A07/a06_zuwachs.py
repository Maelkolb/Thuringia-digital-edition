"""A06: Geburtenueberschuss 1858-1867: Geborene (p.107) - Gestorbene (p.114); stillbirths (p.111) as variant."""
from common import *

YEARS = list(range(1858, 1868))
b = grid("107", "b3")
st = grid("111", "b1")
d = grid("114", "b1")
rows = {}
for r in b[1:11]:
    y = int(r[0])
    for k, ja in zip(DISTRICTS, (1, 3, 5, 7)):
        rows[(y, k)] = {"births": inum(r[ja])}
BL = {"Gera": (3, 13), "Schleiz": (15, 25), "Lobenstein-Ebersdorf": (27, 37), "Reuß j. L.": (39, 49)}
for k, (a, c) in BL.items():
    for r in st[a:c]:
        rows[(int(r[0]), k)]["still"] = inum(r[3])
LAY = [("Gera", d[3:13], 1), ("Schleiz", d[3:13], 7), ("Lobenstein-Ebersdorf", d[15:25], 1), ("Reuß j. L.", d[15:25], 7)]
for k, rr, j0 in LAY:
    for r in rr:
        rows[(int(r[0]), k)]["deaths"] = inum(r[j0 + 2])

# columns: year, district, births, stillborn, deaths | balance, live_births, balance_live, births_per_death
vital = []
for y in YEARS:
    for k in DISTRICTS:
        r = rows[(y, k)]
        live = r["births"] - r["still"]
        vital.append([y, k, r["births"], r["still"], r["deaths"], r["births"] - r["deaths"], live, live - r["deaths"],
                      round(r["births"] / r["deaths"], 2)])

# ---- numbers for the texts
V = {(r[0], r[1]): r for r in vital}
F = "Reuß j. L."
tot = {k: {"births": sum(V[(y, k)][2] for y in YEARS), "still": sum(V[(y, k)][3] for y in YEARS),
           "deaths": sum(V[(y, k)][4] for y in YEARS), "bal": sum(V[(y, k)][5] for y in YEARS),
           "live": sum(V[(y, k)][6] for y in YEARS), "bal_live": sum(V[(y, k)][7] for y in YEARS)} for k in DISTRICTS}
print(tot)
bal = {y: V[(y, F)][5] for y in YEARS}
lo = min(bal, key=bal.get)
hi = max(bal, key=bal.get)
assert all(v[5] > 0 and v[7] > 0 for v in vital)
for y in YEARS:
    assert sum(V[(y, k)][5] for k in DISTRICTS[:3]) == V[(y, F)][5]
ratio = {k: tot[k]["births"] / tot[k]["deaths"] for k in DISTRICTS}
share_gera = tot["Gera"]["bal"] / tot[F]["bal"] * 100
best_ratio = max(DISTRICTS[:3], key=lambda k: ratio[k])
worst_ratio = min(DISTRICTS[:3], key=lambda k: ratio[k])
lowest = min(vital, key=lambda r: r[5])
print(bal, lo, hi, ratio, lowest, share_gera)
assert lo == 1865 and lowest[0] == 1865 and lowest[1] == "Lobenstein-Ebersdorf"
assert best_ratio == "Gera" and worst_ratio == "Lobenstein-Ebersdorf"
min_ratio = min(r[8] for r in vital)
assert min_ratio > 1
# comparison with the three-year balances printed on pp. 98-99 (see analysis bevoelkerung-geburtensaldo-wanderung-1859-1867)
bal_5967 = sum(bal[y] for y in range(1859, 1868))
print("1859-67:", bal_5967)
assert bal_5967 == 9315
stillpct = tot[F]["still"] / tot[F]["bal"] * 100
print(stillpct)

SRC107 = ref("107", "b3", "r2-r11")
SRCS = [SRC107, ref("111", "b1", "r4-r13"), ref("111", "b1", "r16-r25"), ref("111", "b1", "r28-r37"), ref("111", "b1", "r40-r49"),
        ref("114", "b1", "r4-r13"), ref("114", "b1", "r16-r25")]
ana = {
    "id": "bevoelkerung-natuerlicher-zuwachs-1858-1867",
    "title": bi("Geborene und Gestorbene 1858–1867: Geburtenüberschuss", "Births and deaths 1858–1867: natural increase"),
    "category": "population",
    "section": "t1-2-1",
    "sources": SRCS,
    "summary": bi(
        f"Aus Brückners Jahrestabellen zu Geborenen (S. 107), Todtgeborenen (S. 111) und Gestorbenen (S. 114) lässt sich für jeden Landrathsbezirk und jedes Jahr 1858–1867 der Überschuss der Geborenen über die Gestorbenen berechnen. Im Fürstenthum standen {fint_de(tot[F]['births'])} Geborenen {fint_de(tot[F]['deaths'])} Gestorbene gegenüber, ein Überschuss von {fint_de(tot[F]['bal'])} Personen; er war in jedem Jahr und in jedem Bezirk positiv und lag zwischen {bal[lo]} ({lo}) und {bal[hi]} ({hi}) Personen im Jahr. Ohne die Todtgeborenen verringert er sich auf {fint_de(tot[F]['bal_live'])}.",
        f"From Brückner's annual tables of births (p. 107), stillbirths (p. 111) and deaths (p. 114) the surplus of births over deaths can be computed for every district and every year from 1858 to 1867. In the principality {fint_en(tot[F]['births'])} births faced {fint_en(tot[F]['deaths'])} deaths, a surplus of {fint_en(tot[F]['bal'])} people; it was positive in every year and every district and ranged between {fint_en(bal[lo])} ({lo}) and {fint_en(bal[hi])} ({hi}) people a year. Without the stillbirths it falls to {fint_en(tot[F]['bal_live'])}."),
    "method": bi(
        "Je Landrathsbezirk und Jahr wurden die Geborenen (S. 107), die Todtgeborenen (S. 111, Spalte „Zusam.“) und die Gestorbenen (S. 114, Spalte „Zus.“) als gedruckte Zahlen übernommen. Berechnet (derived) wurden der Überschuss (Geborene minus Gestorbene, so wie Brückner die Spalte „Mehr Geborene als Gestorbene“ auf S. 98–99 bildet), die Lebendgeborenen (Geborene minus Todtgeborene, da die Geborenen die Todtgeborenen einschließen), der Überschuss ohne Todtgeborene und die Zahl der Geborenen je Gestorbenen. Die Werte des Fürstenthums sind die gedruckten Summen; sie stimmen mit der Summe der drei Bezirke überein. Wanderungen sind nicht berücksichtigt; die Gegenüberstellung mit den Zählungen und der Wanderungssaldo (S. 98–99) steht in der Auswertung „Geburtenüberschuss, Bevölkerungszunahme und Wanderung 1859–1867“.",
        "For each district and year the births (p. 107), the stillbirths (p. 111, column “Zusam.”) and the deaths (p. 114, column “Zus.”) were taken as printed figures. Computed (derived) were the surplus (births minus deaths, as Brückner forms the column “Mehr Geborene als Gestorbene” on pp. 98–99), the live births (births minus stillbirths, since the births include the stillbirths), the surplus without stillbirths and the number of births per death. The figures for the principality are the printed totals; they agree with the sum of the three districts. Migration is not taken into account; the comparison with the censuses and the migration balance (pp. 98–99) is in the analysis “Natural increase, population change and migration, 1859–1867”."),
    "findings": [
        bi(f"1858–1867 wurden im Fürstenthum {fint_de(tot[F]['births'])} Kinder geboren (darunter {fint_de(tot[F]['still'])} todt) und {fint_de(tot[F]['deaths'])} Menschen starben. Der Überschuss beträgt {fint_de(tot[F]['bal'])}, im Jahresdurchschnitt {fde(tot[F]['bal'] / 10, 0)}; ohne die Todtgeborenen sind es {fint_de(tot[F]['bal_live'])} ({fde(stillpct, 0)} Procent weniger).",
           f"In 1858–1867 {fint_en(tot[F]['births'])} children were born in the principality ({fint_en(tot[F]['still'])} of them stillborn) and {fint_en(tot[F]['deaths'])} people died. The surplus is {fint_en(tot[F]['bal'])}, {fint_en(tot[F]['bal'] / 10)} a year on average; without the stillbirths it is {fint_en(tot[F]['bal_live'])} ({fen(stillpct, 0)} per cent less)."),
        bi(f"Der jährliche Überschuss schwankt zwischen {bal[lo]} ({lo}, dem Jahr mit der höchsten Sterblichkeit, S. 114) und {bal[hi]} ({hi}); auf einen Gestorbenen kommen im Zehnjahresmittel {fde(ratio[F])} Geborene.",
           f"The annual surplus varies between {fint_en(bal[lo])} ({lo}, the year of highest mortality, p. 114) and {fint_en(bal[hi])} ({hi}); over the ten years there are {fen(ratio[F])} births per death."),
        bi(f"Gera trägt {fde(share_gera, 1)} Procent des Überschusses; das Verhältnis von Geborenen zu Gestorbenen ist in Gera am günstigsten ({fde(ratio['Gera'])}) und in Lobenstein-Ebersdorf am niedrigsten ({fde(ratio['Lobenstein-Ebersdorf'])}; Schleiz {fde(ratio['Schleiz'])}).",
           f"Gera accounts for {fen(share_gera, 1)} per cent of the surplus; the ratio of births to deaths is most favourable in Gera ({fen(ratio['Gera'])}) and lowest in Lobenstein-Ebersdorf ({fen(ratio['Lobenstein-Ebersdorf'])}; Schleiz {fen(ratio['Schleiz'])})."),
        bi(f"Der kleinste Überschuss eines Bezirks ist {lowest[5]} (Lobenstein-Ebersdorf {lowest[0]}), im Jahr mit der höchsten Sterblichkeit dieses Bezirks (3,36 Procent, S. 114); auch dort kamen mehr Geborene als Gestorbene (Verhältnis {fde(lowest[8])}).",
           f"The smallest surplus of a district is {lowest[5]} (Lobenstein-Ebersdorf {lowest[0]}), in that district's year of highest mortality (3.36 per cent, p. 114); even there births exceeded deaths (ratio {fen(lowest[8])})."),
    ],
    "caveats": [
        bi("Der Überschuss ist rein rechnerisch und enthält keine Wanderung. Brückner bildet ihn aus allen Geborenen (einschließlich Todtgeborener) minus Gestorbene; ob die Gestorbenen die Todtgeborenen mitzählen, sagt er nicht. Falls nicht, überschätzt diese Rechnung den Zuwachs um die Todtgeborenen (" + fint_de(tot[F]['still']) + " in zehn Jahren), und der aus dem Vergleich mit den Zählungen gewonnene Wanderungsverlust (S. 98 f.) fiele entsprechend kleiner aus.",
           "The surplus is purely arithmetical and contains no migration. Brückner forms it from all births (including stillbirths) minus deaths; he does not say whether the deaths include stillbirths. If they do not, this calculation overstates the increase by the number of stillbirths (" + fint_en(tot[F]['still']) + " over ten years), and the migration loss derived from the comparison with the censuses (p. 98 f.) would be correspondingly smaller."),
        bi("Die Quellen widersprechen sich leicht: Für Lobenstein-Ebersdorf 1866 nennt S. 107 925 Geborene (Fürstenthum 3623), S. 98 dagegen 922 (3620); für Schleiz 1865 sind die Geborenen unsicher (S. 107: 1064; die Prozentzahlen auf S. 108/109/111 setzen etwa 1136 voraus). Einzelne Gestorbenenzahlen (Gera 1864) sind ebenfalls uneinheitlich.",
           "The sources differ slightly: for Lobenstein-Ebersdorf 1866 p. 107 gives 925 births (principality 3,623), p. 98 gives 922 (3,620); for Schleiz 1865 the number of births is uncertain (p. 107: 1,064; the percentages on pp. 108/109/111 imply about 1,136). Some death figures (Gera 1864) are also inconsistent."),
    ],
    "datasets": [
        {"name": "vital", "title": bi("Geborene, Todtgeborene, Gestorbene und Überschuss", "Births, stillbirths, deaths and surplus"),
         "columns": [col("year", "Jahr", "Year", "integer"),
                     col("district", "Landrathsbezirk", "District", "string", note="„Reuß j. L.“ = Fürstenthum insgesamt"),
                     col("births", "Geborene (einschl. Todtgeborene)", "Births (incl. stillbirths)", "integer", "Personen"),
                     col("stillborn", "Todtgeborene", "Stillbirths", "integer", "Personen"),
                     col("deaths", "Gestorbene", "Deaths", "integer", "Personen"),
                     col("balance", "Überschuss der Geborenen über die Gestorbenen", "Surplus of births over deaths", "integer", "Personen", derived=True, note="Geborene minus Gestorbene"),
                     col("live_births", "Lebendgeborene", "Live births", "integer", "Personen", derived=True, note="Geborene minus Todtgeborene"),
                     col("balance_live", "Überschuss ohne Todtgeborene", "Surplus without stillbirths", "integer", "Personen", derived=True, note="Lebendgeborene minus Gestorbene"),
                     col("births_per_death", "Geborene je Gestorbenen", "Births per death", "number", None, derived=True)],
         "rows": vital, "source_refs": SRCS},
    ],
    "charts": [
        {"id": "c1", "dataset": "vital",
         "title": bi("Geborene und Gestorbene im Fürstenthum", "Births and deaths in the principality"),
         "caption": bi("Personen je Jahr, 1858–1867. Der Abstand zwischen der Linie der Geborenen und der der Gestorbenen ist der Überschuss; er ist 1865 am kleinsten. Die mittlere Linie zeigt die Lebendgeborenen.",
                       "People per year, 1858–1867. The distance between the line of births and that of deaths is the surplus; it is smallest in 1865. The middle line shows live births."),
         "vegalite": {"height": 300,
                      "transform": [{"filter": "datum.district == 'Reuß j. L.'"}, {"fold": ["births", "live_births", "deaths"], "as": ["series", "persons"]}],
                      "mark": {"type": "line", "point": True},
                      "encoding": {
                          "x": YEAR_AX,
                          "y": {"field": "persons", "type": "quantitative", "title": bi("Personen", "people"), "scale": {"domain": [1500, 3800]}},
                          "color": {"field": "series", "type": "nominal", "title": None, "scale": {"domain": ["births", "live_births", "deaths"]},
                                    "legend": {"labelExpr": lab_expr2({"births": "Geborene", "live_births": "Lebendgeborene", "deaths": "Gestorbene"},
                                                                      {"births": "Births", "live_births": "Live births", "deaths": "Deaths"})}},
                          "tooltip": [tip("year", "Jahr", "Year"), tip("births", "Geborene", "Births"), tip("live_births", "Lebendgeborene", "Live births"),
                                      tip("deaths", "Gestorbene", "Deaths"), tip("balance", "Überschuss", "Surplus")]}}},
        {"id": "c2", "dataset": "vital",
         "title": bi("Überschuss der Geborenen nach Landrathsbezirk", "Surplus of births by district"),
         "caption": bi("Geborene minus Gestorbene, je Jahr; die Gesamthöhe der Säule ist der Überschuss des Fürstenthums.",
                       "Births minus deaths, per year; the total height of the bar is the surplus of the principality."),
         "vegalite": {"height": 300, "transform": [{"filter": "datum.district != 'Reuß j. L.'"}, ordk("district", DISTRICTS[:3])],
                      "mark": "bar",
                      "encoding": {
                          "x": YEAR_AX,
                          "y": {"field": "balance", "type": "quantitative", "title": bi("Überschuss (Personen)", "surplus (people)"), "stack": "zero"},
                          "color": {"field": "district", "type": "nominal", "title": None, "scale": {"domain": DISTRICTS[:3]}, "legend": {"labelLimit": 260}},
                          "order": {"field": "ordk", "type": "quantitative", "sort": "ascending"},
                          "tooltip": [tip("district", "Landrathsbezirk", "District"), tip("year", "Jahr", "Year"),
                                      tip("births", "Geborene", "Births"), tip("deaths", "Gestorbene", "Deaths"),
                                      tip("balance", "Überschuss", "Surplus")]}}},
        {"id": "c3", "dataset": "vital",
         "title": bi("Geborene je Gestorbenen", "Births per death"),
         "caption": bi("Werte über 1 bedeuten einen Überschuss der Geborenen. Die gestrichelte Linie markiert 1; in keinem Bezirk und Jahr wird sie erreicht oder unterschritten.",
                       "Values above 1 mean a surplus of births. The dashed rule marks 1; no district or year reaches or falls below it."),
         "vegalite": {"height": 300,
                      "layer": [
                          {"mark": {"type": "line", "point": True},
                           "encoding": {
                               "x": YEAR_AX,
                               "y": {"field": "births_per_death", "type": "quantitative", "title": bi("Geborene je Gestorbenen", "births per death"), "scale": {"domain": [0.8, 1.8]}},
                               "color": {"field": "district", "type": "nominal", "title": None, "scale": {"domain": DISTRICTS}, "legend": {"labelLimit": 260}},
                               "tooltip": [tip("district", "Landrathsbezirk", "District"), tip("year", "Jahr", "Year"),
                                           tip("births_per_death", "Geborene je Gestorbenen", "Births per death", ".2f")]}},
                          {"mark": {"type": "rule", "strokeDash": [4, 3]}, "encoding": {"y": {"datum": 1}}}]}},
    ],
    "keywords": {"de": ["Geburtenüberschuss", "natürlicher Zuwachs", "Bevölkerungsentwicklung", "Geborene", "Gestorbene", "Todtgeborene", "Bevölkerungsstatistik"],
                 "en": ["natural increase", "population growth", "births", "deaths", "stillbirths", "vital statistics"]},
    "related": ["bevoelkerung-geburtensaldo-wanderung-1859-1867", "bevoelkerung-geburten-1858-1867", "bevoelkerung-todtgeborene-1858-1867", "bevoelkerung-sterblichkeit-1858-1867"],
    "generated_by": GEN,
    "date": DATE,
}
write(ana)
