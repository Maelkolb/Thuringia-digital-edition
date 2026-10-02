"""A11-10: Landtag und Gemeinderäte nach der Verfassung von 1852/56 und der Gemeindeordnung von 1850 (pp. 268-269)."""
import math
from common import *

# --- Landtag composition (p. 268 b2): 1 + 3 + 6 + 3 -------------------------------------
landtag = [
    ["a", "Köstritzer Paragium", "Köstritz appanage", 1, "a", "Eigene Stimme", "Seat by right"],
    ["b", "Übrige Rittergutsbesitzer", "Other manor owners", 3, "b", "Urwahl, ein Wahlbezirk für das ganze Land", "Direct election, one district for the whole country"],
    ["c", "Stadtgemeinden", "Towns", 6, "c", "Wahlmänner", "Electors (indirect election)"],
    ["d", "Übrige Gemeinden", "Other communities", 3, "c", "Wahlmänner", "Electors (indirect election)"],
]
seats = [r[3] for r in landtag]
total = sum(seats)
elected_general = 6 + 3
quorum = math.ceil(total * 2 / 3)
pct = lambda a, b: 100 * a / b
print(total, elected_general, quorum, pct(elected_general, total))

# --- Gemeinderat sizes (p. 269 b2) ---------------------------------------------------------
council = [
    (300, 500, 6), (501, 1000, 9), (1001, 1500, 12), (1501, 2000, 15), (2001, 3000, 18), (3001, 4000, 21), (4001, 8000, 24),
]
council_rows = []
for i, (lo, hi, n) in enumerate(council):
    council_rows.append([f"{i+1}", f"{lo}–{hi}", f"{lo}–{hi}", lo, hi, n, round(1000 * n / hi + 1e-9, 1)])
print(council_rows)
# population by towns / country, from the school table (p. 299): pupils 1868 x inhabitants per pupil
g299 = {r[0].replace("-", ""): r for r in grid("299", "b3")}
st = [r for k, r in g299.items() if k.startswith("Fürstenthum Städte")][0]
la = [r for k, r in g299.items() if k.startswith("Fürstenthum Land")][0]
pop_town = num(st[4]) * num(st[9])
pop_land = num(la[4]) * num(la[9])
print(st, la, pop_town, pop_land)
per_seat_town = pop_town / 6
per_seat_land = pop_land / 3
hi_up = council_rows[0][6]
lo_up = council_rows[-1][6]


def D(x, nd=0):
    return fmt_de(x, nd)


def E(x, nd=0):
    return fmt_en(x, nd)


ana = {
    "id": "verfassung-landtag-gemeinderaete-vertretung",
    "title": bi("Landtag und Gemeinderäte: Wer vertritt wen?", "Landtag and municipal councils: who represents whom?"),
    "category": "state",
    "section": "t1-4-1b",
    "sources": [{"page": "268", "block": "b1"}, {"page": "268", "block": "b2"}, {"page": "268", "block": "b3"}, {"page": "269", "block": "b2"}, {"page": "299", "block": "b3", "rows": "r14-r15", "note": "Schülerzahlen Städte/Land für die Hochrechnung der Bevölkerung"}],
    "summary": bi(
        f"Nach dem Gesetz über die Zusammensetzung und Wahl der Landesvertretung von 1856 besteht der Landtag aus {D(total)} Mitgliedern: dem Besitzer des Köstritzer Paragiums, drei Rittergutsbesitzern, sechs Stadt- und drei Landgemeindevertretern. Die Gemeindeordnung von 1850 legt die Größe der Gemeinderäte nach Einwohnerklassen fest. Die Auswertung macht beide Schlüssel sichtbar.",
        f"Under the 1856 law on the composition and election of the representative body the Landtag consists of {E(total)} members: the holder of the Köstritz appanage, three manor owners, six town representatives and three representatives of the other communities. The municipal ordinance of 1850 fixes the size of the municipal councils by population class. The analysis makes both keys visible.",
    ),
    "method": bi(
        "Die Sitzverteilung steht im Fließtext S. 268 (Zusammensetzung des Landtags), die Gemeinderatsgrößen in S. 269 (Gemeindeverfassung). Beide Schlüssel wurden in Tabellen übertragen. Für die Gemeinderäte wurde zusätzlich die Zahl der Ratsmitglieder je 1000 Einwohner an der oberen Klassengrenze berechnet (abgeleitet). Für Gemeinden über 8000 Einwohner kommt je 1000 Seelen ein Mitglied hinzu; sie sind hier nicht eingetragen. Die Beschlussfähigkeit (zwei Drittel der Abgeordneten, S. 268) wurde auf 13 Mitglieder angewandt.",
        "The seat allocation is in the running text of p. 268 (composition of the Landtag), the council sizes in p. 269 (municipal constitution). Both keys were transferred into tables. For the councils the number of councillors per 1,000 inhabitants at the upper class limit was added (derived). For communities above 8,000 inhabitants one further member is added per 1,000 souls; they are not entered here. The quorum (two thirds of the deputies, p. 268) was applied to 13 members.",
    ),
    "findings": [
        bi(f"Von den {D(total)} Mitgliedern des Landtags gehen {D(elected_general)} ({D(pct(elected_general, total),0)} %) aus allgemeinen Wahlen der Stadt- und Landgemeinden hervor; vier Sitze ({D(pct(4, total),0)} %) entfallen auf den Besitzer des Köstritzer Paragiums und drei Rittergutsbesitzer.",
           f"Of the {E(total)} members of the Landtag, {E(elected_general)} ({E(pct(elected_general, total),0)} %) come from general elections in the towns and other communities; four seats ({E(pct(4, total),0)} %) go to the holder of the Köstritz appanage and three manor owners."),
        bi(f"Die Städte stellen sechs, die übrigen Gemeinden drei Abgeordnete, obwohl nach den Schulzahlen von 1868 auf dem Land etwa doppelt so viele Menschen leben: hochgerechnet rund {D(round(pop_town,-2))} in den Städten und {D(round(pop_land,-2))} auf dem Land. Auf einen städtischen Sitz kommen so rund {D(round(per_seat_town,-2))}, auf einen ländlichen rund {D(round(per_seat_land,-2))} Einwohner (Faktor {D(per_seat_land/per_seat_town,1)}).",
           f"The towns have six seats, the other communities three, although according to the 1868 school figures about twice as many people live in the countryside: about {E(round(pop_town,-2))} in the towns and {E(round(pop_land,-2))} in the countryside. This gives roughly {E(round(per_seat_town,-2))} inhabitants per urban seat and {E(round(per_seat_land,-2))} per rural seat (a factor of {E(per_seat_land/per_seat_town,1)})."),
        bi(f"Für die Beschlussfähigkeit genügen zwei Drittel der Abgeordneten, bei {D(total)} Mitgliedern also {D(quorum)}; das sind genau die {D(elected_general)} gewählten Stadt- und Gemeindevertreter. Die gewählten Vertreter könnten also allein beschlussfähig sein, brauchen dafür aber vollzählige Anwesenheit.",
           f"A quorum needs two thirds of the deputies, with {E(total)} members i.e. {E(quorum)}; this equals exactly the {E(elected_general)} elected town and community representatives. The elected representatives could therefore form a quorum on their own, but only if all of them attend."),
        bi(f"Die Gemeinderatsgrößen sind stark degressiv: an der oberen Klassengrenze kommen in der kleinsten Klasse (bis 500 Einwohner) {D(hi_up,0)} Ratsmitglieder auf 1000 Einwohner, in der Klasse bis 8000 Einwohner nur {D(lo_up,0)}.",
           f"The council sizes are strongly degressive: at the upper limit of the smallest class (up to 500 inhabitants) there are {E(hi_up,0)} councillors per 1,000 inhabitants, in the class up to 8,000 inhabitants only {E(lo_up,0)}."),
    ],
    "caveats": [
        bi("Brückner nennt weder Wahlberechtigte noch Einwohnerzahlen je Wahlkörper; ein Vergleich von Sitzen und Wählerzahl ist deshalb nicht möglich. Die Bevölkerung von »Städten« und »Land« im zweiten Befund ist aus den Schülerzahlen und Einwohnern je Schüler von S. 299 hochgerechnet (Schüler 1868 × Einwohner je Schüler) und setzt voraus, dass die »Städte« der Schulstatistik den »Stadtgemeinden« des Wahlgesetzes entsprechen; es ist ein Näherungswert, der mit der Volkszählung 1867 (Städte 28.922, Land 59.052; siehe die Auswertung zu Stadt und Land) bis auf 0,1 % übereinstimmt.",
           "Brückner gives neither the eligible voters nor population figures per electoral body, so seats cannot be compared with voters. The populations of “towns” and “countryside” in the second finding are extrapolated from the pupil figures and inhabitants per pupil on p. 299 (pupils 1868 × inhabitants per pupil) and assume that the “towns” of the school statistics correspond to the “urban communities” of the electoral law; it is an approximation that agrees to within 0.1 % with the 1867 census (towns 28,922, countryside 59,052; see the analysis of town and country)."),
        bi("Ob der »Besitzer des Reuß-Köstritzer Paragiums« bei der Beschlussfähigkeit als Abgeordneter zählt, sagt Brückner nicht ausdrücklich; die Rechnung nimmt es an. Die Gemeinderatsgrößen gelten nach dem Text für Gemeinden ab 300 Einwohnern; kleinere Gemeinden können die Gemeindeversammlung an die Stelle des Rats setzen.",
           "Brückner does not state explicitly whether the “holder of the Reuss-Köstritz appanage” counts as a deputy for the quorum; the calculation assumes so. According to the text the council sizes apply to communities of 300 inhabitants and more; smaller communities may let the community assembly replace the council."),
    ],
    "datasets": [
        {"name": "landtag", "title": bi("Zusammensetzung des Landtags", "Composition of the Landtag"),
         "columns": [col("group_key", "Kürzel", "Key", "string"),
                     col("group_de", "Gruppe", "Group", "string"), col("group_en", "Gruppe (englisch)", "Group (English)", "string"),
                     col("seats", "Sitze", "Seats", "integer", "Sitze"),
                     col("mode_key", "Kürzel Wahlart", "Mode key", "string"),
                     col("mode_de", "Wahlart", "Mode of selection", "string"), col("mode_en", "Wahlart (englisch)", "Mode of selection (English)", "string")],
         "rows": landtag, "source_refs": [{"page": "268", "block": "b2"}, {"page": "268", "block": "b3"}]},
        {"name": "council", "title": bi("Größe des Gemeinderats nach Einwohnerklasse", "Size of the municipal council by population class"),
         "columns": [col("class_key", "Kürzel", "Key", "string"),
                     col("class_de", "Einwohnerklasse", "Population class", "string"), col("class_en", "Einwohnerklasse (englisch)", "Population class (English)", "string"),
                     col("lower", "untere Klassengrenze", "Lower class limit", "integer", "Einwohner"),
                     col("upper", "obere Klassengrenze", "Upper class limit", "integer", "Einwohner"),
                     col("members", "Mitglieder des Gemeinderats", "Council members", "integer", "Mitglieder"),
                     col("per_1000", "Ratsmitglieder je 1000 Einwohner (obere Klassengrenze)", "Councillors per 1,000 inhabitants (upper class limit)", "number", "je 1000", derived=True)],
         "rows": council_rows, "source_refs": [{"page": "269", "block": "b2"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "landtag",
         "title": bi("Sitze im Landtag nach Gruppe", "Landtag seats by group"),
         "caption": bi("Insgesamt 13 Sitze; Farbe = Art der Bestellung. Das Köstritzer Paragium wird durch seinen fürstlichen Besitzer oder dessen Stellvertreter vertreten.", "13 seats in total; colour = mode of selection. The Köstritz appanage is represented by its princely holder or his deputy."),
         "vegalite": {
             "height": 180,
             "mark": "bar",
             "encoding": {
                 "y": {"field": F("group"), "type": "nominal", "sort": "-x", "title": None, "axis": {"labelLimit": 360}},
                 "x": {"field": "seats", "type": "quantitative", "title": bi("Sitze", "Seats"), "axis": {"tickMinStep": 1, "format": "d"}},
                 "color": {"field": F("mode"), "type": "nominal", "title": None, "sort": {"field": "mode_key", "op": "min"}, "legend": {"labelLimit": 400, "columns": 1}},
                 "tooltip": [ttf("group", "Gruppe", "Group"), ttf("mode", "Wahlart", "Mode"), tt("seats", "Sitze", "Seats")]}}},
        {"id": "c2", "dataset": "council",
         "title": bi("Größe des Gemeinderats nach Einwohnerzahl", "Size of the municipal council by population"),
         "caption": bi("Mitglieder des Gemeinderats je Einwohnerklasse (Gemeindeordnung 1850).", "Council members per population class (municipal ordinance of 1850)."),
         "vegalite": {
             "height": 260,
             "mark": "bar",
             "encoding": {
                 "x": {"field": F("class"), "type": "nominal", "sort": {"field": "class_key", "op": "min"}, "title": bi("Einwohner der Gemeinde", "Inhabitants of the community"), "axis": {"labelAngle": 0}},
                 "y": {"field": "members", "type": "quantitative", "title": bi("Ratsmitglieder", "Councillors")},
                 "tooltip": [ttf("class", "Einwohnerklasse", "Population class"), tt("members", "Ratsmitglieder", "Councillors")]}}},
        {"id": "c3", "dataset": "council",
         "title": bi("Ratsmitglieder je 1000 Einwohner", "Councillors per 1,000 inhabitants"),
         "caption": bi("Berechnet für die obere Grenze jeder Einwohnerklasse: Mitglieder : Einwohner × 1000.", "Calculated for the upper limit of each population class: members : inhabitants × 1,000."),
         "vegalite": {
             "height": 260,
             "mark": "bar",
             "encoding": {
                 "x": {"field": F("class"), "type": "nominal", "sort": {"field": "class_key", "op": "min"}, "title": bi("Einwohner der Gemeinde", "Inhabitants of the community"), "axis": {"labelAngle": 0}},
                 "y": {"field": "per_1000", "type": "quantitative", "title": bi("Ratsmitglieder je 1000 Einwohner", "Councillors per 1,000 inhabitants")},
                 "tooltip": [ttf("class", "Einwohnerklasse", "Population class"), {"field": "per_1000", "title": bi("je 1000 Einwohner", "per 1,000 inhabitants"), "format": ".1f"}]}}},
    ],
    "related": ["bevoelkerung-stadt-land-1833-1867", "bevoelkerung-gemeindegroessen-1867"],
    "keywords": {"de": ["Landtag", "Landesvertretung", "Wahlrecht", "Abgeordnete", "Rittergutsbesitzer", "Gemeinderat", "Gemeindeordnung", "Verfassung", "Köstritz"],
                 "en": ["Landtag", "representation", "suffrage", "deputies", "manor owners", "municipal council", "municipal ordinance", "constitution", "Köstritz"]},
}
write(ana)
