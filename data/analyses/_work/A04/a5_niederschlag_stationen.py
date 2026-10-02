"""A04 / analysis 5: precipitation days, fog and hoar frost at Gera, Hohenleuben, Schleiz, Rothenacker (pp. 66-67)."""
import sys
sys.path.insert(0, ".")
from common import *

STATIONS = ["Gera", "Hohenleuben", "Schleiz", "Rothenacker"]
PH = {"Nebel": 1, "Regen": 2, "Schnee": 3, "Reif": 4, "RegenSchnee": 5}
g66 = grid("66", "b3")   # Gera: cols 1 Nebel, 2 Regen, 3 Schnee-Graupen, 4 Reif, 5 Gewitter ; rows 1..12 months, 13 Summe
g66h = grid("66", "b5")  # Hohenleuben per-year means: cols 1 Nebel, 2 Regen und Schnee, 3 Reif
g67 = grid("67", "b2")   # Schleiz cols 1-5 (Nebel, Regen, Schnee, Reif, Gewitter), Rothenacker cols 6-10 ; rows 1..12, 13 Summe, 14 Mittel

rows = []
store = {}   # (station, ph, month) -> per_year
gew_total = {}


# Brueckner's corrigenda (p. 830): Gera table p. 66, column 3 (Regen): month -> (printed, corrected); Max. mark July instead of May
CORR_REGEN = {1: (79, 87), 7: (169, 181), 8: (142, 152), 12: (92, 84)}


def add(st, ph, m, mlabel, printed, total, years, per_year, mk, total_printed=None, corr=""):
    so = STATIONS.index(st) + 1
    rows.append([st, so, m, mlabel, ph, PH[ph], printed, total, total_printed if total_printed is not None else total, corr, years, round(per_year, 2), mk])
    store[(st, ph, m)] = per_year


for m in range(1, 13):
    # Gera, 12 years (sums)
    for ph, c in (("Nebel", 1), ("Regen", 2), ("Schnee", 3), ("Reif", 4)):
        cell = g66[m][c]
        v = num(cell)
        t = None if v is None else int(v)
        tp, corr, mk = t, "", mark(cell)
        if ph == "Regen":
            if m in CORR_REGEN:
                assert t == CORR_REGEN[m][0], (m, t)
                t = CORR_REGEN[m][1]
                corr = f"S. 830: {t} statt {tp}"
            if m == 5:
                assert mk == "Max."
                mk, corr = "", "S. 830: Max.-Vermerk im Juli statt im Mai"
            if m == 7:
                mk = "Max."
                corr += "; Max.-Vermerk (statt Mai)"
        add("Gera", ph, m, g66[m][0], cell.strip(), t, 12, (t or 0) / 12, mk, tp, corr)
    # Hohenleuben, per-year means of 15 years (fractions)
    for ph, c in (("Nebel", 1), ("RegenSchnee", 2), ("Reif", 3)):
        cell = g66h[m][c]
        add("Hohenleuben", ph, m, g66h[m][0].replace(".", "").strip(), cell.strip(), None, 15, frac(cell), mark(cell))
    # Schleiz / Rothenacker, 2 years (sums)
    for st, off in (("Schleiz", 0), ("Rothenacker", 5)):
        for ph, c in (("Nebel", 1), ("Regen", 2), ("Schnee", 3), ("Reif", 4)):
            cell = g67[m][c + off]
            v = num(cell)
            t = int(v)
            add(st, ph, m, g67[m][0], cell.strip(), t, 2, t / 2, mark(cell))
# Gewitter totals (not stored in monthly, used in annual_printed)
gew_total["Gera"] = sum(int(num(g66[m][5]) or 0) for m in range(1, 13)) / 12
gew_total["Schleiz"] = sum(int(num(g67[m][5])) for m in range(1, 13)) / 2
gew_total["Rothenacker"] = sum(int(num(g67[m][10])) for m in range(1, 13)) / 2

def ann(st, ph):
    return sum(store[(st, ph, m)] for m in range(1, 13))

# sanity vs printed sums
assert sum(r[7] for r in rows if r[0] == "Gera" and r[4] == "Nebel") == 811
assert sum(r[7] for r in rows if r[0] == "Gera" and r[4] == "Regen") == 1544   # corrected total (S. 830)
assert sum(r[7] for r in rows if r[0] == "Schleiz" and r[4] == "Reif") == 94
assert sum(r[7] for r in rows if r[0] == "Rothenacker" and r[4] == "Regen") == 291
precip = {st: (ann(st, "RegenSchnee") if st == "Hohenleuben" else ann(st, "Regen") + ann(st, "Schnee")) for st in STATIONS}
fog = {st: ann(st, "Nebel") for st in STATIONS}
reif = {st: ann(st, "Reif") for st in STATIONS}
snow = {st: ann(st, "Schnee") for st in ("Gera", "Schleiz", "Rothenacker")}
print("precip", precip); print("fog", fog); print("reif", reif); print("snow", snow); print("gew", gew_total)
# maxima/minima of rain (Regen; Hohenleuben Regen+Schnee) by month
def mm(st, ph):
    v = [(store[(st, ph, m)], m) for m in range(1, 13)]
    return max(v)[1], min(v)[1]
rain_mm = {"Gera": mm("Gera", "Regen"), "Hohenleuben": mm("Hohenleuben", "RegenSchnee"), "Schleiz": mm("Schleiz", "Regen"), "Rothenacker": mm("Rothenacker", "Regen")}
print(rain_mm)
# monthly precipitation days (Regen + Schnee)
pm = {}
for st in STATIONS:
    for m in range(1, 13):
        pm[(st, m)] = store[(st, "RegenSchnee", m)] if st == "Hohenleuben" else store[(st, "Regen", m)] + store[(st, "Schnee", m)]
for st in STATIONS:
    v = [(pm[(st, m)], m) for m in range(1, 13)]
    print(st, "precip days max", max(v), "min", min(v))
pmax = {st: [m for m in range(1, 13) if abs(pm[(st, m)] - max(pm[(st, k)] for k in range(1, 13))) < 1e-9] for st in STATIONS}
print('pmax', pmax)
# winter share
for st in ("Gera", "Schleiz", "Rothenacker"):
    print(st, "snow Dec-Feb per year", sum(store[(st, "Schnee", m)] for m in (12, 1, 2)), "of", snow[st])

# printed Zusammenstellung (p. 67 b4)
g4 = grid("67", "b4")
printed_rows = []
for r in range(1, 5):
    st = g4[r][0].replace(".", "").strip()
    assert st == STATIONS[r - 1], st
    for k, ph in enumerate(["Nebel", "Regen", "Schnee", "Reif", "Gewitter"], start=1):
        cell = g4[r][k]
        pv = num(cell)
        if ph == "Gewitter":
            comp = gew_total.get(st)
        elif ph == "Regen" and st == "Hohenleuben":
            comp = ann(st, "RegenSchnee")
        elif ph == "Schnee" and st == "Hohenleuben":
            comp = None
        else:
            comp = ann(st, ph)
        corrected = {("Gera", "Regen"): 128.6, ("Gera", "Gewitter"): 22.5}.get((st, ph))   # S. 830 (S. 67, Z. 20 v. o.)
        printed_rows.append([st, STATIONS.index(st) + 1, ph, pv, corrected, None if comp is None else round(comp, 1)])
for r in printed_rows:
    print(r)


def F(x, dec=1):
    return fmt(x, "de", dec), fmt(x, "en", dec)


MN_DE = MONTH_FULL_DE
MN_EN = MONTH_FULL_EN
G, H, S_, R = STATIONS
STATION_DOMAIN = STATIONS


def rain_groups(idx, lang):
    """'Juli (Gera, Schleiz, Rothenacker), September (Hohenleuben)' for the max (idx 0) or min (idx 1) month of rain days."""
    by = {}
    for st in STATIONS:
        by.setdefault(rain_mm[st][idx], []).append(st)
    names = MN_DE if lang == "de" else MN_EN
    return ", ".join(f"{names[m - 1]} ({', '.join(sts)})" for m, sts in sorted(by.items()))

PH_LABEL = {"Nebel": ("Nebel", "Fog"), "Regen": ("Regen", "Rain"), "Schnee": ("Schnee", "Snow"), "Reif": ("Reif", "Hoar frost"),
            "RegenSchnee": ("Regen und Schnee", "Rain and snow")}
GRP_CALC = {"calculate": "indexof(['Regen','Schnee','RegenSchnee'], datum.phenomenon) >= 0 ? 'Niederschlag' : datum.phenomenon", "as": "grp"}
GRP_LABEL = {"calculate": bi("{'Niederschlag':'Niederschlagstage','Nebel':'Nebel','Reif':'Reif'}[datum.grp]",
                             "{'Niederschlag':'Precipitation days','Nebel':'Fog','Reif':'Hoar frost'}[datum.grp]"), "as": "grp_label"}
GRP_ORDER = {"calculate": "{'Niederschlag':1,'Nebel':2,'Reif':3}[datum.grp]", "as": "grp_order"}
STATION_COLOR = {"field": "station", "type": "nominal", "title": None, "scale": {"domain": STATION_DOMAIN}}

ana = {
    "id": "klima-niederschlagstage-stationen",
    "title": bi("Niederschlagstage, Nebel und Reif an vier Orten", "Precipitation days, fog and hoar frost at four places"),
    "category": "climate",
    "section": "t1-1-7",
    "sources": [{"page": "66", "block": "b1"}, {"page": "66", "block": "b2"}, {"page": "66", "block": "b3", "rows": "r2-r15"},
                {"page": "66", "block": "b4"}, {"page": "66", "block": "b5", "rows": "r2-r14"},
                {"page": "67", "block": "b1"}, {"page": "67", "block": "b2", "rows": "r2-r15"}, {"page": "67", "block": "b3"},
                {"page": "67", "block": "b4", "rows": "r2-r5"}, {"page": "67", "block": "b5"}, {"page": "69", "block": "b1"},
                {"page": "830", "block": "b3"}, {"page": "830", "block": "b4", "rows": "i1-i3"}],
    "summary": bi(
        "Neben Gera (12 Jahre) verzeichnet Brückner Nebel, Regen, Schnee und Reif für Hohenleuben (15-jähriger Durchschnitt, Regen und Schnee zusammen) sowie für Schleiz und Rothenacker (je zwei Jahre). Die Auswertung rechnet alles auf Tage pro Jahr bzw. pro Monat um und stellt Niederschlagstage, Nebel und Reif der vier Orte gegenüber. Die Orte weichen stark voneinander ab; ein einfaches Höhenmuster ergibt sich nicht.",
        "Besides Gera (12 years), Brückner records fog, rain, snow and hoar frost for Hohenleuben (15-year average, rain and snow combined) and for Schleiz and Rothenacker (two years each). The analysis converts everything to days per year and per month and sets precipitation days, fog and hoar frost of the four places side by side. The places differ strongly; no simple pattern with elevation emerges."),
    "method": bi(
        "Quellen: Gera S. 66 b3 (Summen über 1856–1867, Spalten Nebel, Regen, Schnee-Graupen, Reif; die Regenspalte nach Brückners Berichtigung S. 830 b3: Januar 87 statt 79, Juli 181 statt 169, August 152 statt 142, Dezember 84 statt 92, Summe 1544 statt 1540, »Max.« im Juli statt im Mai); Hohenleuben S. 66 b5 (Jahresmittel eines 15-jährigen Durchschnitts, im Druck als gemischte Brüche wie »1 14/15«; die Spalte »Regen und Schnee« lässt sich nicht trennen); Schleiz und Rothenacker S. 67 b2 (Summen über zwei Jahre, 1866/67 bzw. Juni 1866–Mai 1868). Umrechnung auf Tage pro Monat und Jahr: Periodensumme ÷ Jahre bzw. Bruch in Dezimalzahl. »Niederschlagstage« = Regen + Schnee (Gera, Schleiz, Rothenacker) bzw. die Spalte »Regen und Schnee« (Hohenleuben); Brückner addiert Regen- und Schneetage selbst zur »Summe der Tage« (S. 69). Fällt beides auf denselben Tag, kann ein Tag doppelt gezählt sein. Die gedruckte Vergleichstabelle (S. 67 b4) steht als eigener Datensatz neben den aus den Monatswerten nachgerechneten Jahreswerten und den Berichtigungen aus S. 830 b4 (Gera: Regen 128,6 statt 148,4, Gewitter 22,5 statt 22,3); für die Charts gelten die nachgerechneten Werte. In der Monatstabelle enthält die Spalte »Summe über den Beobachtungszeitraum« die berichtigten Werte, »Summe laut Tabelle« die gedruckten; die Spalte »Berichtigung« kennzeichnet die betroffenen Zeilen. Ein Gedankenstrich im Druck gilt als 0. Gewitter sind in der Auswertung »Gewitter: Häufigkeit, Jahresgang und Zugrichtung« behandelt.",
        "Sources: Gera p. 66 b3 (totals over 1856–1867, columns fog, rain, snow/graupel, hoar frost; the rain column as corrected by Brückner on p. 830 b3: January 87 instead of 79, July 181 instead of 169, August 152 instead of 142, December 84 instead of 92, total 1544 instead of 1540, “Max.” in July instead of May); Hohenleuben p. 66 b5 (annual means of a 15-year average, printed as mixed fractions such as “1 14/15”; the column “rain and snow” cannot be separated); Schleiz and Rothenacker p. 67 b2 (totals over two years, 1866/67 and June 1866–May 1868). Conversion to days per month and year: period total ÷ years, or fraction to decimal. “Precipitation days” = rain + snow (Gera, Schleiz, Rothenacker) or the column “rain and snow” (Hohenleuben); Brückner himself adds rain and snow days to a “sum of days” (p. 69). If both fall on the same day, a day may be counted twice. The printed comparison table (p. 67 b4) is given as a separate dataset next to the annual values recomputed from the monthly figures and the corrections from p. 830 b4 (Gera: rain 128.6 instead of 148.4, thunderstorms 22.5 instead of 22.3); the charts use the recomputed values. In the monthly table the column “Total over the observation period” holds the corrected values, “Total as in the table” the printed ones, and the column “Correction” marks the rows concerned. A dash in the print counts as 0. Thunderstorms are treated in the analysis “Thunderstorms: frequency, annual cycle and direction”."),
    "findings": [
        bi(f"Die meisten Niederschlagstage (Regen + Schnee) meldet Rothenacker ({F(precip[R],0)[0]} pro Jahr), dann Gera ({F(precip[G],0)[0]}), Hohenleuben ({F(precip[H],0)[0]}) und Schleiz ({F(precip[S_],0)[0]}). Die drei Oberlandorte liegen damit weiter auseinander ({F(precip[S_],0)[0]} bis {F(precip[R],0)[0]}) als Gera und Hohenleuben; eine einfache Abhängigkeit von der Höhenlage zeigt sich nicht.",
           f"Rothenacker reports the most precipitation days (rain + snow; {F(precip[R],0)[1]} a year), then Gera ({F(precip[G],0)[1]}), Hohenleuben ({F(precip[H],0)[1]}) and Schleiz ({F(precip[S_],0)[1]}). The three Oberland places thus lie further apart ({F(precip[S_],0)[1]} to {F(precip[R],0)[1]}) than Gera and Hohenleuben; no simple dependence on elevation appears."),
        bi(f"Nebel: Rothenacker {F(fog[R])[0]}, Gera {F(fog[G])[0]}, Hohenleuben {F(fog[H])[0]} und Schleiz {F(fog[S_],0)[0]} Tage im Jahr. Reif dagegen zählen Schleiz ({F(reif[S_],0)[0]}) und Gera ({F(reif[G],0)[0]}) am häufigsten, Rothenacker {F(reif[R])[0]} und Hohenleuben {F(reif[H])[0]}.",
           f"Fog: Rothenacker {F(fog[R])[1]}, Gera {F(fog[G])[1]}, Hohenleuben {F(fog[H])[1]} and Schleiz {F(fog[S_],0)[1]} days a year. Hoar frost, by contrast, is counted most often at Schleiz ({F(reif[S_],0)[1]}) and Gera ({F(reif[G],0)[1]}), with Rothenacker {F(reif[R])[1]} and Hohenleuben {F(reif[H])[1]}."),
        bi(f"Rothenacker verzeichnet {F(snow['Rothenacker'],0)[0]} Schneetage im Jahr, Schleiz {F(snow['Schleiz'],0)[0]}, Gera {F(snow['Gera'],0)[0]}; im Dezember zählt Rothenacker {F(store[('Rothenacker','Schnee',12)],0)[0]} Schneetage, im Januar {F(store[('Rothenacker','Schnee',1)],0)[0]}.",
           f"Rothenacker records {F(snow['Rothenacker'],0)[1]} snow days a year, Schleiz {F(snow['Schleiz'],0)[1]}, Gera {F(snow['Gera'],0)[1]}; in December Rothenacker counts {F(store[('Rothenacker','Schnee',12)],0)[1]} snow days, in January {F(store[('Rothenacker','Schnee',1)],0)[1]}."),
        bi(f"Die Monate mit den meisten und den wenigsten Regentagen unterscheiden sich von Ort zu Ort, wie Brückner (S. 67, berichtigt S. 830) hervorhebt. Maximum: {rain_groups(0, 'de')}. Minimum: {rain_groups(1, 'de')}. (Für Gera gilt das berichtigte Maximum im Juli; im ursprünglichen Druck stand der Mai.)",
           f"The months with the most and the fewest rain days differ from place to place, as Brückner stresses (p. 67, corrected p. 830). Maximum: {rain_groups(0, 'en')}. Minimum: {rain_groups(1, 'en')}. (For Gera the corrected maximum is July; the original print had May.)"),
    ],
    "caveats": [
        bi("Die Reihen sind verschieden lang (12, 15, 2 und 2 Jahre) und stammen von verschiedenen Beobachtern ohne einheitliche Kriterien; Brückner selbst sagt, die Ergebnisse gingen »weit auseinander« (S. 67). Die Werte für Schleiz und Rothenacker beruhen nur auf zwei Jahren (Schleiz 1866/67, Rothenacker Juni 1866–Mai 1868).",
           "The series differ in length (12, 15, 2 and 2 years) and come from different observers without uniform criteria; Brückner himself says the results “differ widely” (p. 67). The values for Schleiz and Rothenacker rest on only two years (Schleiz 1866/67, Rothenacker June 1866–May 1868)."),
        bi("Gera, Regen: Im Druck ergeben die Monatswerte (S. 66) 1522, gedruckt ist 1540; die Vergleichstabelle S. 67 nennt 148,4. Brückner berichtigt das selbst (S. 830): vier Monatswerte, die Summe (1544), das Mittel (128,6; Vergleichstabelle: 128,6 statt 148,4) und den Höchstmonat (Juli statt Mai); die Auswertung verwendet diese Werte. Außerdem berichtigt er das Gera-Gewitter-Mittel auf 22,5 (statt 22,3). Nicht berichtigt sind: Rothenacker, Gewitter: Summe 35, gedrucktes Mittel 18,5 statt 17,5; Hohenleuben: Die Summe der Monatsbrüche beim Reif ergibt 17 8/15 (17,5), gedruckt sind 17 2/5 (17,4), die Nebel-Summe (28 2/3) steht auf S. 67 als 28,6.",
           "Gera, rain: in the print the monthly values (p. 66) add up to 1522, the printed total is 1540; the comparison table on p. 67 gives 148.4. Brückner corrects this himself (p. 830): four monthly values, the total (1544), the mean (128.6; comparison table: 128.6 instead of 148.4) and the peak month (July instead of May); the analysis uses these values. He also corrects the Gera thunderstorm mean to 22.5 (instead of 22.3). Not corrected are: Rothenacker, thunderstorms: total 35, printed mean 18.5 instead of 17.5; Hohenleuben: the monthly fractions for hoar frost add up to 17 8/15 (17.5), the printed total is 17 2/5 (17.4), the fog total (28 2/3) appears on p. 67 as 28.6."),
        bi("Bei Hohenleuben sind Regen und Schnee nicht getrennt; die Spalte »Regen« der Vergleichstabelle (141,1) ist dort die Summe beider. Auch bei den anderen Orten bleibt offen, wie ein Tag mit Regen und Schnee gezählt wurde.",
           "At Hohenleuben rain and snow are not separated; the “rain” column of the comparison table (141.1) is the sum of both there. For the other places, too, it is unclear how a day with both rain and snow was counted."),
    ],
    "datasets": [
        {"name": "monthly", "title": bi("Nebel, Regen, Schnee und Reif nach Ort und Monat", "Fog, rain, snow and hoar frost by station and month"),
         "columns": [
             col("station", "Beobachtungsort", "Station", "string"),
             col("station_order", "Reihenfolge des Ortes", "Station order", "integer", None, True),
             col("month", "Monat", "Month", "integer", None, True, "Monatsnummer 1–12, editorisch"),
             col("month_label", "Monat (Original)", "Month (original)", "string"),
             col("phenomenon", "Erscheinung", "Phenomenon", "string", None, True, "Nebel, Regen, Schnee (Gera: Schnee-Graupen), Reif, RegenSchnee (nur Hohenleuben: Regen und Schnee)"),
             col("phenomenon_order", "Reihenfolge der Erscheinung", "Phenomenon order", "integer", None, True),
             col("value_printed", "Wert im Druck", "Value as printed", "string", None, False, "Zahl oder gemischter Bruch, Gedankenstrich = nicht verzeichnet"),
             col("period_total", "Summe über den Beobachtungszeitraum", "Total over the observation period", "integer", "Tage bzw. Fälle", False, "nur Gera, Schleiz, Rothenacker; Hohenleuben druckt Jahresmittel; Gera, Regen: berichtigt nach S. 830"),
             col("period_total_printed", "Summe laut Tabelle", "Total as in the table", "integer", "Tage bzw. Fälle", False, "gedruckter Tabellenwert vor der Berichtigung (gleich der Summe, wo nichts berichtigt wurde)"),
             col("correction", "Berichtigung", "Correction", "string", None, False, "Hinweis auf die Berichtigung in Brückners Zusätzen (S. 830)"),
             col("years", "Jahre im Zeitraum", "Years in the period", "integer", "Jahre", True, "Gera 12 (1856–1867), Hohenleuben 15 (Durchschnitt), Schleiz 2, Rothenacker 2"),
             col("per_year", "Tage pro Monat und Jahr", "Days per month and year", "number", "Tage", True, "Periodensumme ÷ Jahre bzw. gedruckter Bruch als Dezimalzahl"),
             col("mark", "Druckvermerk", "Printed mark", "string", None, False, "»Min.« oder »Max.« im Original"),
         ], "rows": rows,
         "source_refs": [{"page": "66", "block": "b3", "rows": "r2-r13"}, {"page": "66", "block": "b5", "rows": "r2-r13"},
                         {"page": "67", "block": "b2", "rows": "r2-r13"}, {"page": "830", "block": "b3"}]},
        {"name": "annual_printed", "title": bi("Brückners Vergleichstabelle (S. 67) und nachgerechnete Jahreswerte", "Brückner's comparison table (p. 67) and recomputed annual values"),
         "columns": [
             col("station", "Beobachtungsort", "Station", "string"),
             col("station_order", "Reihenfolge des Ortes", "Station order", "integer", None, True),
             col("phenomenon", "Erscheinung", "Phenomenon", "string", None, True),
             col("mean_printed", "Jahresmittel laut Druck", "Annual mean as printed", "number", "pro Jahr", False, "leer = Gedankenstrich im Druck"),
             col("mean_corrected", "Jahresmittel nach Berichtigung (S. 830)", "Annual mean as corrected (p. 830)", "number", "pro Jahr", False, "nur Gera, Regen (128,6 statt 148,4) und Gewitter (22,5 statt 22,3)"),
             col("mean_computed", "Jahresmittel nachgerechnet", "Annual mean recomputed", "number", "pro Jahr", True, "Summe der Monatswerte ÷ Jahre; Hohenleuben »Regen« = Regen und Schnee"),
         ], "rows": printed_rows,
         "source_refs": [{"page": "67", "block": "b4", "rows": "r2-r5"}, {"page": "830", "block": "b4", "rows": "i1"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "monthly",
         "title": bi("Niederschlagstage, Nebel und Reif im Jahr", "Precipitation days, fog and hoar frost per year"),
         "caption": bi("Tage pro Jahr, aus den Monatswerten berechnet; Niederschlagstage = Regen- plus Schneetage (Hohenleuben: Regen und Schnee zusammen). Rothenacker hat die meisten Niederschlags- und Nebeltage, Schleiz und Gera die meisten Reiftage; Schleiz zählt die wenigsten Niederschlags- und Nebeltage.",
                       "Days per year, computed from the monthly values; precipitation days = rain plus snow days (Hohenleuben: rain and snow combined). Rothenacker has the most precipitation and fog days, Schleiz and Gera the most hoar frost days; Schleiz counts the fewest precipitation and fog days."),
         "vegalite": {
             "height": 300,
             "transform": [GRP_CALC, GRP_ORDER, GRP_LABEL,
                           {"aggregate": [{"op": "sum", "field": "per_year", "as": "days"}], "groupby": ["station", "station_order", "grp", "grp_order", "grp_label"]}],
             "mark": "bar",
             "encoding": {
                 "x": {"field": "grp_label", "type": "nominal", "title": None, "sort": {"field": "grp_order", "op": "min"}, "axis": {"labelAngle": 0}},
                 "xOffset": {"field": "station", "sort": {"field": "station_order", "op": "min"}},
                 "y": {"field": "days", "type": "quantitative", "title": bi("Tage pro Jahr", "Days per year")},
                 "color": STATION_COLOR,
                 "tooltip": [{"field": "station", "title": bi("Ort", "Station")},
                             {"field": "grp_label", "title": bi("Erscheinung", "Phenomenon")},
                             {"field": "days", "title": bi("Tage pro Jahr", "Days per year"), "format": ".1f"}]}}},
        {"id": "c2", "dataset": "monthly",
         "title": bi("Niederschlagstage im Jahresgang", "Precipitation days through the year"),
         "caption": bi(f"Tage mit Regen oder Schnee pro Monat und Jahr (Hohenleuben: Spalte »Regen und Schnee«). Die Höchstwerte liegen bei Gera im {MN_DE[pmax['Gera'][0]-1]}, bei Hohenleuben im {MN_DE[pmax['Hohenleuben'][0]-1]}, bei Schleiz im {' und '.join(MN_DE[m-1] for m in pmax['Schleiz'])}, bei Rothenacker im {' und '.join(MN_DE[m-1] for m in pmax['Rothenacker'])}; Schleiz und Rothenacker (zwei Jahre) schwanken stark.",
                       f"Days with rain or snow per month and year (Hohenleuben: column “rain and snow”). Maxima fall in {MN_EN[pmax['Gera'][0]-1]} at Gera, in {MN_EN[pmax['Hohenleuben'][0]-1]} at Hohenleuben, in {' and '.join(MN_EN[m-1] for m in pmax['Schleiz'])} at Schleiz and in {' and '.join(MN_EN[m-1] for m in pmax['Rothenacker'])} at Rothenacker; Schleiz and Rothenacker (two years) fluctuate strongly."),
         "vegalite": {
             "height": 320,
             "transform": [MONTH_ABBR_CALC,
                           {"filter": "indexof(['Regen','Schnee','RegenSchnee'], datum.phenomenon) >= 0"},
                           {"aggregate": [{"op": "sum", "field": "per_year", "as": "days"}], "groupby": ["station", "station_order", "month", "mlabel"]}],
             "mark": {"type": "line", "point": True},
             "encoding": {
                 "x": {"field": "mlabel", "type": "ordinal", "sort": {"field": "month", "op": "min"}, "title": bi("Monat", "Month"), "axis": {"labelAngle": 0}},
                 "y": {"field": "days", "type": "quantitative", "title": bi("Tage pro Monat", "Days per month")},
                 "color": STATION_COLOR,
                 "tooltip": [{"field": "station", "title": bi("Ort", "Station")},
                             {"field": "mlabel", "title": bi("Monat", "Month")},
                             {"field": "days", "title": bi("Tage pro Monat und Jahr", "Days per month and year"), "format": ".1f"}]}}},
        {"id": "c3", "dataset": "monthly",
         "title": bi("Nebel-, Reif- und Schneetage nach Monat", "Fog, hoar frost and snow days by month"),
         "caption": bi("Tage pro Monat und Jahr. Nebel ist im Oktober und November (Gera, Rothenacker) am häufigsten, Reif und Schnee treten im Winterhalbjahr auf; für Hohenleuben fehlt die Schneezeile, weil dort Regen und Schnee nicht getrennt sind.",
                       "Days per month and year. Fog is most frequent in October and November (Gera, Rothenacker), hoar frost and snow occur in the winter half-year; Hohenleuben has no snow panel because rain and snow are not separated there."),
         "vegalite": {
             "autosize": {"type": "pad"},
             "transform": [MONTH_ABBR_CALC,
                           {"filter": "indexof(['Nebel','Reif','Schnee'], datum.phenomenon) >= 0"},
                           {"calculate": bi("{'Nebel':'Nebel','Reif':'Reif','Schnee':'Schnee'}[datum.phenomenon]", "{'Nebel':'Fog','Reif':'Hoar frost','Schnee':'Snow'}[datum.phenomenon]"), "as": "ph_label"}],
             "facet": {"row": {"field": "ph_label", "type": "nominal", "title": None, "sort": {"field": "phenomenon_order", "op": "min"},
                               "header": {"labelAngle": 0, "labelOrient": "top", "labelAlign": "left", "labelPadding": 4}}},
             "spec": {
                 "width": 560, "height": 84,
                 "mark": {"type": "line", "point": True},
                 "encoding": {
                     "x": {"field": "mlabel", "type": "ordinal", "sort": {"field": "month", "op": "min"}, "title": None, "axis": {"labelAngle": 0}},
                     "y": {"field": "per_year", "type": "quantitative", "title": bi("Tage/Monat", "Days/month"), "scale": {"domain": [0, 18]}, "axis": {"tickCount": 4}},
                     "color": STATION_COLOR,
                     "tooltip": [{"field": "station", "title": bi("Ort", "Station")},
                                 {"field": "mlabel", "title": bi("Monat", "Month")},
                                 {"field": "ph_label", "title": bi("Erscheinung", "Phenomenon")},
                                 {"field": "value_printed", "title": bi("Wert im Druck", "Value as printed")},
                                 {"field": "per_year", "title": bi("Tage pro Monat und Jahr", "Days per month and year"), "format": ".1f"}]}}}},
    ],
    "keywords": {
        "de": ["Niederschlag", "Regentage", "Schnee", "Nebel", "Reif", "Gera", "Hohenleuben", "Schleiz", "Rothenacker", "Klimavergleich"],
        "en": ["precipitation", "rain days", "snow", "fog", "hoar frost", "Gera", "Hohenleuben", "Schleiz", "Rothenacker", "climate comparison"]},
    "related": ["klima-witterungserscheinungen-gera-1856-1867", "klima-gewitter-gera-stationen", "klima-regenmenge-gera-1860-1867"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(ana)
