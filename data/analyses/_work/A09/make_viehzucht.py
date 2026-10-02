"""A09 / analysis 8: Viehbestand 1843-1867 (pp. 233-235)."""
import sys, re
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent))
from a09common import *

DASHES = {"—", "–", "-"}


def cell(raw):
    """None = nothing printed (blank), 0 = dash ('keine'), else number."""
    r = raw.strip()
    if r == "":
        return None
    if r in DASHES:
        return 0
    return num(r)


COMP = ["pferde", "fuellen", "stiere", "ochsen", "kuehe", "jungvieh", "ganz", "halb", "unv", "ziegen", "schweine"]


def parse_rows(page, bid, first, last):
    g = grid(page, bid)
    out = {}
    for rn in range(first, last + 1):
        r = g[rn - 1]
        year = int(r[0])
        vals = {c: cell(x) for c, x in zip(COMP, r[1:12])}
        out[year] = (vals, rn)
    return out


GERA = parse_rows("233", "b4", 5, 13)
SCHL = parse_rows("233", "b4", 15, 23)
LOBE = parse_rows("234", "b1", 4, 12)
FUER = parse_rows("234", "b1", 14, 19)
YEARS = [1843, 1849, 1858, 1861, 1864, 1867]   # years with complete counts for all three districts


def totals(v):
    """returns dict pferde, rinder, schafe, ziegen, schweine (derived sums or printed merged totals) and components for sheep"""
    z = lambda x: x or 0
    # horses: Pferde + Füllen; if Füllen blank the printed number is the total
    pf = v["pferde"] if v["fuellen"] is None else v["pferde"] + z(v["fuellen"])
    # cattle: sum of the four columns, or the merged total printed in the 'Ochsen' column
    if v["stiere"] is None and v["kuehe"] is None and v["jungvieh"] is None and v["ochsen"] is not None:
        ri = v["ochsen"]
        merged_r = True
    else:
        ri = z(v["stiere"]) + z(v["ochsen"]) + z(v["kuehe"]) + z(v["jungvieh"])
        merged_r = False
    if v["ganz"] is None and v["unv"] is None and v["halb"] is not None:
        sc = v["halb"]
        merged_s = True
    else:
        sc = z(v["ganz"]) + z(v["halb"]) + z(v["unv"])
        merged_s = False
    return dict(pferde=pf, rinder=ri, schafe=sc, ziegen=v["ziegen"], schweine=v["schweine"], merged_s=merged_s)


# ---------------------------------------------------------------- long table of totals
SPECIES = [("pferde", "Pferde", "Horses", 1), ("rinder", "Rinder", "Cattle", 2), ("schafe", "Schafe", "Sheep", 3),
           ("ziegen", "Ziegen", "Goats", 4), ("schweine", "Schweine", "Pigs", 5)]
LT = [("Gera", "Gera", 1, GERA), ("Schleiz", "Schleiz", 2, SCHL), ("Lobenstein-Ebersdorf", "Lobenstein-Ebersdorf", 3, LOBE), ("Fürstenthum", "Principality", 4, None)]
bestand = []
tot_d = {}   # (lt, year) -> totals dict
for lt, lten, ln, T in LT[:3]:
    for y in YEARS:
        t = totals(T[y][0])
        tot_d[(lt, y)] = t
for y in YEARS:
    s = {k: sum(tot_d[(lt, y)][k] for lt in ("Gera", "Schleiz", "Lobenstein-Ebersdorf")) for k, *_ in SPECIES}
    tot_d[("Fürstenthum", y)] = s
# verification against the printed Fürstenthum rows of p. 234
for y in YEARS:
    pf = totals(FUER[y][0])
    for k in ("pferde", "rinder", "schafe", "ziegen", "schweine"):
        if pf[k] != tot_d[("Fürstenthum", y)][k]:
            print("printed F differs from sum of districts:", y, k, pf[k], tot_d[("Fürstenthum", y)][k])
for lt, lten, ln, T in LT:
    for y in YEARS:
        for k, de, en, kn in SPECIES:
            bestand.append([lt, lten, ln, y, de, en, kn, tot_d[(lt, y)][k]])

# ---------------------------------------------------------------- sheep structure (printed components)
stufen = []
STU = [("ganz", "ganz veredelt", "fully improved", 1), ("halb", "halb veredelt", "half improved", 2), ("unv", "unveredelt", "unimproved", 3)]
for lt, lten, ln, T in LT[:3]:
    for y in YEARS:
        v = T[y][0]
        if tot_d[(lt, y)]["merged_s"]:
            continue
        for k, de, en, kn in STU:
            stufen.append([lt, lten, ln, y, de, en, kn, v[k] or 0])
for y in YEARS:
    ys = [r for r in stufen if r[3] == y and r[0] != "Fürstenthum"]
    if len({r[0] for r in ys}) == 3:
        for k, de, en, kn in STU:
            stufen.append(["Fürstenthum", "Principality", 4, y, de, en, kn, sum(r[7] for r in ys if r[6] == kn)])
print("sheep stages", len(stufen))
stufen_F = {(r[3], r[6]): r[7] for r in stufen if r[0] == "Fürstenthum"}
print(stufen_F)

# ---------------------------------------------------------------- p. 234 b3: Tabelle A/B (1843 / 1867)
g = grid("234", "b3")
je100 = []
ROWMAP = [(3, "Gera", "Gera", 1, 1843), (4, "Gera", "Gera", 1, 1867), (5, "Schleiz", "Schleiz", 2, 1843), (6, "Schleiz", "Schleiz", 2, 1867),
          (7, "Lobenstein-Ebersdorf", "Lobenstein-Ebersdorf", 3, 1843), (8, "Lobenstein-Ebersdorf", "Lobenstein-Ebersdorf", 3, 1867),
          (9, "Fürstenthum", "Principality", 4, 1843), (10, "Fürstenthum", "Principality", 4, 1867)]
tabA = {}
tabB = {}
for rn, lt, lten, ln, y in ROWMAP:
    r = g[rn]
    A = [num(x) for x in r[2:7]]
    B = [num(x) for x in r[7:12]]
    for (k, de, en, kn), a, b in zip(SPECIES, A, B):
        tabA[(lt, y, k)] = a
        tabB[(lt, y, k)] = b
# Q01: misprint in table A (p. 234 b3, Gera 1867 Pferde printed 1774). The detailed table (p. 233/234 b1: 1731 + 143), the table on
# p. 235 b3 (1874) and the printed total 2689 (1874 + 551 + 264) all give 1874; the per-100 value printed in table B (4,63) follows
# the misprint (1774), so it is recomputed with the Gera population of 1867 (38 252, p. 91; the same base reproduces the printed
# per-100 values of the other species of Gera).
POP_GERA_1867 = 38252
PRINT_FIX = {}
if tabA[("Gera", 1867, SPECIES[0][0])] == 1774:
    PRINT_FIX[("Gera", 1867, SPECIES[0][0])] = (1774, tabB[("Gera", 1867, SPECIES[0][0])])
    tabA[("Gera", 1867, SPECIES[0][0])] = 1874
    tabB[("Gera", 1867, SPECIES[0][0])] = round(100 * 1874 / POP_GERA_1867, 2)
    print("table A/B corrected:", PRINT_FIX, "->", tabA[("Gera", 1867, SPECIES[0][0])], tabB[("Gera", 1867, SPECIES[0][0])])
for lt, lten, ln, _ in LT:
    for k, de, en, kn in SPECIES:
        b43, b67 = tabB[(lt, 1843, k)], tabB[(lt, 1867, k)]
        a43, a67 = tabA[(lt, 1843, k)], tabA[(lt, 1867, k)]
        je100.append([lt, lten, ln, de, en, kn, a43, a67, b43, b67, round(100 * (a67 / a43 - 1), 1), round(100 * (b67 / b43 - 1), 1)])
# compare table A with sums
for lt in ("Gera", "Schleiz", "Lobenstein-Ebersdorf", "Fürstenthum"):
    for k, *_ in SPECIES:
        for y in (1843, 1867):
            if tabA[(lt, y, k)] != tot_d[(lt, y)][k]:
                print("Table A vs sum of columns:", lt, y, k, tabA[(lt, y, k)], tot_d[(lt, y)][k])

# ---------------------------------------------------------------- p. 235 b3: working animals 1867
g3 = grid("235", "b3")
arb = []
for k, (lt, lten, ln, _) in enumerate(LT):
    r = g3[1 + k]
    rin, rin_a, rin_p, pf, pf_a, pf_p, stu, hen, wal = [num(x) for x in r[1:10]]
    arb.append([lt, lten, ln, rin, rin_a, rin_p, pf, pf_a, pf_p, stu, hen, wal])
print(arb)

# ---------------------------------------------------------------- numbers for the text
F = {(y, k): tot_d[("Fürstenthum", y)][k] for y in YEARS for k, *_ in SPECIES}
chg = {k: 100 * (F[(1867, k)] / F[(1843, k)] - 1) for k, *_ in SPECIES}
print({k: round(v, 1) for k, v in chg.items()}, [F[(1843, k)] for k, *_ in SPECIES], [F[(1867, k)] for k, *_ in SPECIES])
pc = {(r[0], r[3]): r[11] for r in je100}
pa = {(r[0], r[3]): r for r in je100}
print({k: v for k, v in pc.items() if k[0] == "Fürstenthum"})
print({k: v for k, v in pc.items()})
b43 = {(r[0], r[3]): r[8] for r in je100}
b67 = {(r[0], r[3]): r[9] for r in je100}
a_ = {r[0]: r for r in arb}
un67 = stufen_F[(1867, 3)]
sch_tot67 = sum(stufen_F[(1867, k)] for k in (1, 2, 3))
sch_tot49 = sum(stufen_F[(1849, k)] for k in (1, 2, 3))
print(un67 / sch_tot67 * 100, stufen_F[(1849, 3)] / sch_tot49 * 100, stufen_F[(1849, 2)] / sch_tot49 * 100, stufen_F[(1867, 2)] / sch_tot67 * 100)
schafe_min = min(YEARS, key=lambda y: F[(y, "schafe")])
schafe_max = max(YEARS, key=lambda y: F[(y, "schafe")])
print(schafe_min, schafe_max, [(y, F[(y, "schafe")]) for y in YEARS])
print([(y, F[(y, "rinder")]) for y in YEARS])

R_BZ = [{"page": "233", "block": "b4", "rows": "r5-r13; r15-r23"}, {"page": "234", "block": "b1", "rows": "r4-r12; r14-r19"}]
R_AB = {"page": "234", "block": "b3", "rows": "r4-r11"}
R_AR = {"page": "235", "block": "b3", "rows": "r2-t5"}
R_TXT = [{"page": "233", "block": "b3"}, {"page": "234", "block": "b4"}, {"page": "235", "block": "b1"}, {"page": "235", "block": "b2"}, {"page": "235", "block": "b4"}]


def col(name, de, en, typ, unit=None, derived=False, note=None):
    d = {"name": name, "label": bi(de, en), "type": typ, "unit": unit}
    if derived:
        d["derived"] = True
    if note:
        d["note"] = note
    return d


SUMNOTE = "Summe der gedruckten Teilzahlen (Pferde + Füllen; Stiere + Ochsen + Kühe + Jungvieh; ganz + halb + unveredelt) bzw. gedruckter Gesamtwert; Fürstenthum = Summe der drei Landestheile"

ana = {
    "id": "viehzucht-bestand-1843-1867",
    "title": bi("Viehbestand im Fürstenthum Reuß j. L. 1843–1867", "Livestock in the Principality of Reuss (younger line), 1843–1867"),
    "category": "livestock",
    "section": "t1-3-3",
    "sources": R_BZ + [R_AB, R_AR] + R_TXT,
    "summary": bi(
        "Brückner stellt die Ergebnisse der Viehzählungen von 1843 bis 1867 für die drei Landestheile zusammen (Pferde, Rindvieh, Schafe nach Veredelungsgrad, Ziegen, Schweine) und vergleicht 1843 mit 1867 absolut und je 100 Einwohner. Die Diagramme zeigen die Entwicklung der fünf Tierarten, die Veränderung je 100 Einwohner nach Landestheilen, den Wandel der Schafzucht und den Einsatz von Pferden und Rindern als Arbeitstieren 1867.",
        "Brückner compiles the results of the livestock counts from 1843 to 1867 for the three districts (horses, cattle, sheep by degree of improvement, goats, pigs) and compares 1843 with 1867 in absolute figures and per 100 inhabitants. The charts show the development of the five kinds of animals, the change per 100 inhabitants by district, the change in sheep farming, and the use of horses and cattle as working animals in 1867."),
    "method": bi(
        "Die Zählergebnisse stammen aus den Tabellen auf S. 233–234 (Blöcke b4 bzw. b1), der Vergleichstabelle A/B (S. 234, Block b3) und der Tabelle zu den Arbeitsthieren 1867 (S. 235, Block b3). Für die Zeitreihen wurden nur die Jahre aufgenommen, für die alle drei Landestheile gezählt sind (1843, 1849, 1858, 1861, 1864, 1867); die Jahre 1846, 1852 und 1855 sind nach Brückner unvollständig. »Pferde« umfasst Pferde und Füllen; »Rinder« ist die Summe aus Stieren, Ochsen, Kühen und Jungvieh (1843 und 1864 druckt Brückner nur eine Gesamtzahl, die hier übernommen wird); »Schafe« ist die Summe der drei Veredelungsstufen. Die Werte für das Fürstenthum sind die Summen der Landestheile; sie stimmen bis auf wenige Ausnahmen mit den gedruckten Fürstenthum-Zeilen überein (siehe Hinweise). Die Prozentwerte je 100 Seelen und die Veränderungsraten (Spalten pct_change_*) wurden aus Tabelle A bzw. B berechnet.",
        "The counts come from the tables on pp. 233–234 (blocks b4 and b1), the comparison table A/B (p. 234, block b3) and the table on working animals in 1867 (p. 235, block b3). For the time series only the years in which all three districts were counted are used (1843, 1849, 1858, 1861, 1864, 1867); according to Brückner the years 1846, 1852 and 1855 are incomplete. “Horses” comprises horses and foals; “cattle” is the sum of bulls, oxen, cows and young cattle (for 1843 and 1864 Brückner prints only a total, which is taken over); “sheep” is the sum of the three degrees of improvement. The figures for the principality are the sums of the districts; with few exceptions they agree with the printed rows for the principality (see notes). The percentages per 100 inhabitants and the rates of change (columns pct_change_*) were computed from table A and B respectively."),
    "findings": [
        bi(f"Von 1843 bis 1867 hat sich der Bestand an Schafen um {de_num(-chg['schafe'],1)} % verringert ({de_num(F[(1843,'schafe')],0)} auf {de_num(F[(1867,'schafe')],0)}), während Ziegen um {de_num(chg['ziegen'],1)} %, Schweine um {de_num(chg['schweine'],1)} %, Pferde um {de_num(chg['pferde'],1)} % und Rinder nur um {de_num(chg['rinder'],1)} % zunahmen.",
           f"From 1843 to 1867 the number of sheep fell by {en_num(-chg['schafe'],1)} % ({en_num(F[(1843,'schafe')],0)} to {en_num(F[(1867,'schafe')],0)}), while goats rose by {en_num(chg['ziegen'],1)} %, pigs by {en_num(chg['schweine'],1)} %, horses by {en_num(chg['pferde'],1)} % and cattle by only {en_num(chg['rinder'],1)} %."),
        bi(f"Die Entwicklung verläuft nicht gleichmäßig: Der Rinderbestand steigt bis 1861 auf {de_num(F[(1861,'rinder')],0)} und fällt bis 1867 auf {de_num(F[(1867,'rinder')],0)}; die Schafe haben 1858 mit {de_num(F[(1858,'schafe')],0)} ihren Tiefstand, erreichen 1864 wieder {de_num(F[(1864,'schafe')],0)} und fallen bis 1867 auf {de_num(F[(1867,'schafe')],0)}.",
           f"The development is not even: cattle rise to {en_num(F[(1861,'rinder')],0)} by 1861 and fall to {en_num(F[(1867,'rinder')],0)} by 1867; sheep reach their low in 1858 at {en_num(F[(1858,'schafe')],0)}, climb again to {en_num(F[(1864,'schafe')],0)} in 1864 and fall to {en_num(F[(1867,'schafe')],0)} by 1867."),
        bi(f"Auf 100 Einwohner gerechnet gehen Rinder ({de_num(b43[('Fürstenthum','Rinder')],2)} auf {de_num(b67[('Fürstenthum','Rinder')],2)}) und Schafe ({de_num(b43[('Fürstenthum','Schafe')],2)} auf {de_num(b67[('Fürstenthum','Schafe')],2)}) zurück; Pferde, Ziegen und Schweine nehmen zu. Am stärksten sinkt der Schafbestand je 100 Einwohner in Gera ({de_num(b43[('Gera','Schafe')],2)} auf {de_num(b67[('Gera','Schafe')],2)}); am stärksten steigen die Ziegen in Lobenstein-Ebersdorf ({de_num(b43[('Lobenstein-Ebersdorf','Ziegen')],2)} auf {de_num(b67[('Lobenstein-Ebersdorf','Ziegen')],2)}).",
           f"Per 100 inhabitants cattle ({en_num(b43[('Fürstenthum','Rinder')],2)} to {en_num(b67[('Fürstenthum','Rinder')],2)}) and sheep ({en_num(b43[('Fürstenthum','Schafe')],2)} to {en_num(b67[('Fürstenthum','Schafe')],2)}) decline; horses, goats and pigs increase. Sheep per 100 inhabitants fall most in Gera ({en_num(b43[('Gera','Schafe')],2)} to {en_num(b67[('Gera','Schafe')],2)}); goats rise most in Lobenstein-Ebersdorf ({en_num(b43[('Lobenstein-Ebersdorf','Ziegen')],2)} to {en_num(b67[('Lobenstein-Ebersdorf','Ziegen')],2)})."),
        bi(f"Der Rückgang der Schafe geht auf die halb veredelten Schafe zurück ({de_num(stufen_F[(1849,2)],0)} im Jahr 1849, {de_num(stufen_F[(1867,2)],0)} im Jahr 1867); die unveredelten Schafe nehmen von {de_num(stufen_F[(1849,3)],0)} auf {de_num(stufen_F[(1867,3)],0)} zu, die ganz veredelten von {de_num(stufen_F[(1849,1)],0)} auf {de_num(stufen_F[(1867,1)],0)}.",
           f"The decline of sheep is due to the half-improved sheep ({en_num(stufen_F[(1849,2)],0)} in 1849, {en_num(stufen_F[(1867,2)],0)} in 1867); unimproved sheep rise from {en_num(stufen_F[(1849,3)],0)} to {en_num(stufen_F[(1867,3)],0)}, fully improved ones from {en_num(stufen_F[(1849,1)],0)} to {en_num(stufen_F[(1867,1)],0)}."),
        bi(f"1867 werden im Fürstenthum {de_num(a_['Fürstenthum'][5])} % der Rinder zur Arbeit herangezogen, im Landestheil Gera nur {de_num(a_['Gera'][5])} %, in Schleiz {de_num(a_['Schleiz'][5])} % und in Lobenstein-Ebersdorf {de_num(a_['Lobenstein-Ebersdorf'][5])} %; von den Pferden sind {de_num(a_['Fürstenthum'][8])} % Arbeitspferde (Wallache {de_num(a_['Fürstenthum'][11],0)}, Stuten {de_num(a_['Fürstenthum'][9],0)}, Hengste {de_num(a_['Fürstenthum'][10],0)}).",
           f"In 1867, {en_num(a_['Fürstenthum'][5])} % of the cattle in the principality are used for work, in the district of Gera only {en_num(a_['Gera'][5])} %, in Schleiz {en_num(a_['Schleiz'][5])} % and in Lobenstein-Ebersdorf {en_num(a_['Lobenstein-Ebersdorf'][5])} %; {en_num(a_['Fürstenthum'][8])} % of the horses are working horses (geldings {en_num(a_['Fürstenthum'][11],0)}, mares {en_num(a_['Fürstenthum'][9],0)}, stallions {en_num(a_['Fürstenthum'][10],0)})."),
    ],
    "caveats": [
        bi("Die Vorlage ist nicht in allen Zahlen stimmig: Für Gera 1867 steht in Tabelle A 1774 Pferde, die Einzeltabelle (S. 233) und die Tabelle S. 235 ergeben 1731 + 143 = 1874; die Summe 2689 für das Fürstenthum passt zu 1874. Die Auswertung verwendet 1874; die gedruckte Angabe in Tabelle B (4,63 Pferde auf 100 Seelen) folgt dem Druckfehler und wurde mit 1874 und der Einwohnerzahl 38 252 neu berechnet (4,90). Die Ziegen von Lobenstein-Ebersdorf 1843 sind in der Einzeltabelle mit 1162, in Tabelle A mit 1167 gedruckt (Fürstenthum 3073 bzw. 3078); für 1867 steht beim Fürstenthum für Pferde 2482 (Summe der Landestheile 2486) und für unveredelte Schafe 13 293 (Summe der Landestheile 14 266, wozu Tabelle A mit 30 117 Schafen passt). Alle Stellen wurden am Faksimile geprüft; die Auswertung rechnet mit den Summen der Landestheile, nur Tabelle A/B (Diagramm 2) gibt Brückners Werte unverändert wieder, abgesehen von der genannten Korrektur für Gera/Pferde 1867.",
           "The source is not consistent in all figures: for Gera in 1867 table A gives 1774 horses, whereas the detailed table (p. 233) and the table on p. 235 give 1731 + 143 = 1874; the total of 2689 for the principality fits 1874. The analysis uses 1874; the figure printed in table B (4.63 horses per 100 inhabitants) follows the misprint and was recomputed with 1874 and the population of 38,252 (4.90). The goats of Lobenstein-Ebersdorf in 1843 are printed as 1162 in the detailed table and 1167 in table A (principality 3073 and 3078); for 1867 the principality shows 2482 horses (sum of the districts 2486) and 13,293 unimproved sheep (sum of the districts 14,266, which fits table A with 30,117 sheep). All places were checked against the facsimile; the analysis uses the sums of the districts, only table A/B (chart 2) reproduces Brückner's values unchanged, apart from the correction for Gera/horses 1867."),
        bi("Die Zählungen 1846, 1852 und 1855 sind unvollständig oder fehlen und wurden nicht aufgenommen; die Gliederung der Tiere nach Alter und Veredelung beginnt erst 1849 (1843 im Landestheil Lobenstein-Ebersdorf nur summarisch). Pferde schließen die Füllen ein; Maulthiere und Esel (1864 sechs, 1867 vier) sind nicht gesondert ausgewiesen.",
           "The counts of 1846, 1852 and 1855 are incomplete or missing and were not used; the classification of the animals by age and improvement begins only in 1849 (1843 only in summary for Lobenstein-Ebersdorf). Horses include foals; mules and donkeys (six in 1864, four in 1867) are not shown separately."),
        bi("Die Veränderung je 100 Einwohner hängt von der Bevölkerungsentwicklung ab, die Brückner hier nicht ausweist; die Bezugsbevölkerung lässt sich nur indirekt aus den Verhältniszahlen erschließen.",
           "The change per 100 inhabitants depends on population growth, which Brückner does not show here; the reference population can be inferred only indirectly from the ratios."),
    ],
    "datasets": [
        {"name": "bestand", "title": bi("Viehbestand nach Landestheilen und Jahren", "Livestock by district and year"),
         "columns": [
             col("landestheil_de", "Landestheil", "District", "string"),
             col("landestheil_en", "Landestheil (englisch)", "District (English)", "string"),
             col("lt_nr", "Reihenfolge Landestheil", "District order", "integer", derived=True),
             col("jahr", "Jahr", "Year", "integer"),
             col("tierart_de", "Tierart", "Kind of animal", "string"),
             col("tierart_en", "Tierart (englisch)", "Kind of animal (English)", "string"),
             col("tierart_nr", "Reihenfolge Tierart", "Animal order", "integer", derived=True),
             col("anzahl", "Bestand", "Number of animals", "integer", "Tiere", derived=True, note=SUMNOTE),
         ],
         "rows": bestand, "source_refs": R_BZ},
        {"name": "schafe_stufen", "title": bi("Schafe nach Veredelungsgrad", "Sheep by degree of improvement"),
         "columns": [
             col("landestheil_de", "Landestheil", "District", "string"),
             col("landestheil_en", "Landestheil (englisch)", "District (English)", "string"),
             col("lt_nr", "Reihenfolge Landestheil", "District order", "integer", derived=True),
             col("jahr", "Jahr", "Year", "integer"),
             col("stufe_de", "Veredelungsgrad", "Degree of improvement", "string"),
             col("stufe_en", "Veredelungsgrad (englisch)", "Degree of improvement (English)", "string"),
             col("stufe_nr", "Reihenfolge", "Order", "integer", derived=True),
             col("anzahl", "Schafe", "Sheep", "integer", "Tiere", derived=True, note="Landestheile: gedruckte Werte (Strich = 0); Fürstenthum: Summe der Landestheile"),
         ],
         "rows": stufen, "source_refs": R_BZ},
        {"name": "je100", "title": bi("Vergleich 1843 und 1867 (Tabelle A und B)", "Comparison of 1843 and 1867 (tables A and B)"),
         "columns": [
             col("landestheil_de", "Landestheil", "District", "string"),
             col("landestheil_en", "Landestheil (englisch)", "District (English)", "string"),
             col("lt_nr", "Reihenfolge Landestheil", "District order", "integer", derived=True),
             col("tierart_de", "Tierart", "Kind of animal", "string"),
             col("tierart_en", "Tierart (englisch)", "Kind of animal (English)", "string"),
             col("tierart_nr", "Reihenfolge Tierart", "Animal order", "integer", derived=True),
             col("anzahl_1843", "Bestand 1843", "Number 1843", "integer", "Tiere"),
             col("anzahl_1867", "Bestand 1867", "Number 1867", "integer", "Tiere"),
             col("je100_1843", "auf 100 Seelen 1843", "per 100 inhabitants 1843", "number", "Tiere je 100 Einwohner"),
             col("je100_1867", "auf 100 Seelen 1867", "per 100 inhabitants 1867", "number", "Tiere je 100 Einwohner"),
             col("pct_change_abs", "Veränderung des Bestands", "Change of the number", "number", "%", derived=True),
             col("pct_change_je100", "Veränderung je 100 Einwohner", "Change per 100 inhabitants", "number", "%", derived=True),
         ],
         "rows": je100, "source_refs": [R_AB]},
        {"name": "arbeitstiere", "title": bi("Arbeitsthiere 1867", "Working animals 1867"),
         "columns": [
             col("landestheil_de", "Landestheil", "District", "string"),
             col("landestheil_en", "Landestheil (englisch)", "District (English)", "string"),
             col("lt_nr", "Reihenfolge Landestheil", "District order", "integer", derived=True),
             col("rinder", "Zahl der Rinder", "Number of cattle", "integer", "Tiere"),
             col("rinder_arbeit", "davon Arbeitsthiere", "of which working animals", "integer", "Tiere"),
             col("rinder_pct", "Arbeitsthiere in % der Rinder", "Working animals as % of cattle", "number", "%"),
             col("pferde", "Zahl der Pferde", "Number of horses", "integer", "Tiere"),
             col("pferde_arbeit", "davon Arbeitsthiere", "of which working animals", "integer", "Tiere"),
             col("pferde_pct", "Arbeitsthiere in % der Pferde", "Working animals as % of horses", "number", "%"),
             col("stuten", "Stuten", "Mares", "integer", "Tiere"),
             col("hengste", "Hengste", "Stallions", "integer", "Tiere"),
             col("wallache", "Wallachen", "Geldings", "integer", "Tiere"),
         ],
         "rows": arb, "source_refs": [R_AR]},
    ],
    "charts": [
        {"id": "c1", "dataset": "bestand",
         "title": bi("Entwicklung des Viehbestands (1843 = 100)", "Development of the livestock (1843 = 100)"),
         "caption": bi("Fürstenthum insgesamt, Bestand der fünf Tierarten in Prozent des Bestands von 1843 (Summe der Landestheile). Ziegen und Schweine nehmen stark zu; die Schafe erreichen 1858 ihren Tiefstand, die Rinder 1861 ihren Höchststand.",
                       "Principality as a whole, number of the five kinds of animals as a percentage of the 1843 figure (sum of the districts). Goats and pigs increase strongly; sheep reach their low in 1858, cattle their peak in 1861."),
         "vegalite": {
             "height": 300,
             "transform": [{"filter": "datum.landestheil_de == 'Fürstenthum'"},
                           {"window": [{"op": "first_value", "field": "anzahl", "as": "basis"}], "groupby": ["tierart_de"], "sort": [{"field": "jahr", "order": "ascending"}],
                            "frame": [None, None]},
                           {"calculate": "100 * datum.anzahl / datum.basis", "as": "index"}],
             "mark": {"type": "line", "point": True},
             "encoding": {
                 "x": {"field": "jahr", "type": "quantitative", "title": bi("Jahr", "Year"), "axis": {"format": "d", "values": YEARS}, "scale": {"domain": [1841, 1869]}},
                 "y": {"field": "index", "type": "quantitative", "title": bi("Bestand (1843 = 100)", "Number (1843 = 100)"), "scale": {"zero": False}},
                 "color": {"field": {"de": "tierart_de", "en": "tierart_en"}, "type": "nominal", "title": None,
                           "scale": {"domain": [bi(s[1], s[2]) for s in SPECIES]}, "legend": {"columns": 3, "labelLimit": 160}},
                 "tooltip": [{"field": {"de": "tierart_de", "en": "tierart_en"}, "title": bi("Tierart", "Animal")},
                             {"field": "jahr", "title": bi("Jahr", "Year"), "format": "d"},
                             {"field": "anzahl", "title": bi("Bestand", "Number"), "format": ","},
                             {"field": "index", "title": bi("1843 = 100", "1843 = 100"), "format": ".1f"}]}}},
        {"id": "c2", "dataset": "je100",
         "title": bi("Veränderung je 100 Einwohner 1843–1867", "Change per 100 inhabitants, 1843–1867"),
         "caption": bi("Prozentuale Veränderung der Zahl der Tiere je 100 Einwohner (Brückners Tabelle B). Positive Werte: mehr Tiere je Einwohner als 1843. Ziegen und Schweine nehmen überall zu, Schafe und Rinder ab; Pferde nehmen nur in Schleiz stark zu, in Gera ab.",
                       "Percentage change of the number of animals per 100 inhabitants (Brückner's table B). Positive values: more animals per inhabitant than in 1843. Goats and pigs increase everywhere, sheep and cattle decrease; horses increase strongly only in Schleiz and decrease in Gera."),
         "vegalite": {
             "height": 320,
             "mark": "bar",
             "encoding": {
                 "x": {"field": {"de": "tierart_de", "en": "tierart_en"}, "type": "nominal", "sort": {"field": "tierart_nr", "op": "min"}, "title": None, "axis": {"labelAngle": 0, "labelLimit": 120}},
                 "xOffset": {"field": {"de": "landestheil_de", "en": "landestheil_en"}, "type": "nominal", "sort": ["Gera", "Schleiz", "Lobenstein-Ebersdorf", bi("Fürstenthum", "Principality")]},
                 "y": {"field": "pct_change_je100", "type": "quantitative", "title": bi("% Veränderung je 100 Einwohner", "% change per 100 inhabitants")},
                 "color": {"field": {"de": "landestheil_de", "en": "landestheil_en"}, "type": "nominal", "title": None,
                           "scale": {"domain": ["Gera", "Schleiz", "Lobenstein-Ebersdorf", bi("Fürstenthum", "Principality")]}, "legend": {"columns": 2, "labelLimit": 220}},
                 "tooltip": [{"field": {"de": "landestheil_de", "en": "landestheil_en"}, "title": bi("Landestheil", "District")},
                             {"field": {"de": "tierart_de", "en": "tierart_en"}, "title": bi("Tierart", "Animal")},
                             {"field": "je100_1843", "title": bi("je 100 Einwohner 1843", "per 100 inhabitants 1843"), "format": ".2f"},
                             {"field": "je100_1867", "title": bi("je 100 Einwohner 1867", "per 100 inhabitants 1867"), "format": ".2f"},
                             {"field": "pct_change_je100", "title": bi("Veränderung, %", "change, %"), "format": ".1f"}]}}},
        {"id": "c3", "dataset": "schafe_stufen",
         "title": bi("Schafe nach Veredelungsgrad", "Sheep by degree of improvement"),
         "caption": bi("Schafbestand des Fürstenthums nach Veredelungsgrad (Summe der Landestheile). Die halb veredelten Schafe gehen zurück, die unveredelten nehmen zu.",
                       "Sheep of the principality by degree of improvement (sum of the districts). Half-improved sheep decline, unimproved sheep increase."),
         "vegalite": {
             "height": 300,
             "transform": [{"filter": "datum.landestheil_de == 'Fürstenthum'"}],
             "mark": "bar",
             "encoding": {
                 "x": {"field": "jahr", "type": "ordinal", "title": bi("Jahr", "Year"), "axis": {"labelAngle": 0}},
                 "y": {"field": "anzahl", "type": "quantitative", "title": bi("Schafe", "Sheep"), "axis": {"format": ",.0f"}},
                 "color": {"field": {"de": "stufe_de", "en": "stufe_en"}, "type": "nominal", "title": None,
                           "scale": {"domain": [bi(s[1], s[2]) for s in STU]}},
                 "order": {"field": "stufe_nr", "type": "quantitative"},
                 "tooltip": [{"field": "jahr", "title": bi("Jahr", "Year"), "format": "d"},
                             {"field": {"de": "stufe_de", "en": "stufe_en"}, "title": bi("Veredelungsgrad", "Degree of improvement")},
                             {"field": "anzahl", "title": bi("Schafe", "Sheep"), "format": ","}]}}},
        {"id": "c4", "dataset": "arbeitstiere",
         "title": bi("Arbeitsthiere unter Rindern und Pferden 1867", "Working animals among cattle and horses, 1867"),
         "caption": bi("Anteil der Arbeitsthiere an den Rindern und Pferden (Viehzählung 1867, erstmals mit Angabe der Arbeitsthiere). Im Oberland (Schleiz, Lobenstein-Ebersdorf) wird mehr als doppelt so oft Rindvieh zur Arbeit herangezogen wie in Gera.",
                       "Share of working animals among cattle and horses (livestock count of 1867, the first to record working animals). In the Upper Land (Schleiz, Lobenstein-Ebersdorf) cattle are used for work more than twice as often as in Gera."),
         "vegalite": {
             "height": 280,
             "transform": [{"fold": ["rinder_pct", "pferde_pct"], "as": ["art", "pct"]},
                           {"calculate": {"de": "datum.art == 'rinder_pct' ? 'Rinder' : 'Pferde'", "en": "datum.art == 'rinder_pct' ? 'Cattle' : 'Horses'"}, "as": "art_label"}],
             "mark": "bar",
             "encoding": {
                 "x": {"field": {"de": "landestheil_de", "en": "landestheil_en"}, "type": "nominal", "sort": {"field": "lt_nr", "op": "min"}, "title": None, "axis": {"labelAngle": 0}},
                 "xOffset": {"field": "art_label", "type": "nominal", "sort": [bi("Rinder", "Cattle"), bi("Pferde", "Horses")]},
                 "y": {"field": "pct", "type": "quantitative", "title": bi("% Arbeitsthiere", "% working animals"), "scale": {"domain": [0, 100]}},
                 "color": {"field": "art_label", "type": "nominal", "title": None, "scale": {"domain": [bi("Rinder", "Cattle"), bi("Pferde", "Horses")]}},
                 "tooltip": [{"field": {"de": "landestheil_de", "en": "landestheil_en"}, "title": bi("Landestheil", "District")},
                             {"field": "art_label", "title": bi("Tierart", "Animal")},
                             {"field": "pct", "title": "%", "format": ".2f"},
                             {"field": "rinder", "title": bi("Rinder", "Cattle"), "format": ","}, {"field": "pferde", "title": bi("Pferde", "Horses"), "format": ","}]}}},
    ],
    "transcription_issues": [
        {"page": "234", "block": "b3", "cell": "r5c3", "transcribed": "1774", "facsimile": "1774", "checked_facsimile": True,
         "note": "Druckfehler für 1874 (Einzeltabelle S. 233/234: 1731 + 143; Tabelle S. 235: 1874; Summe 2689 = 1874 + 551 + 264). In der Auswertung 1874; der Wert 4,63 auf 100 Seelen (r5c8) folgt dem Druckfehler und ist mit 1874 / 38 252 Einwohnern zu 4,90 neu berechnet."},
    ],
    "keywords": {
        "de": ["Viehzucht", "Viehzählung", "Viehbestand", "Pferde", "Rinder", "Rindvieh", "Schafe", "Schafzucht", "Ziegen", "Schweine", "Arbeitstiere", "Veredelung"],
        "en": ["livestock", "cattle", "horses", "sheep", "goats", "pigs", "working animals", "livestock census", "sheep farming"],
    },
    "related": ["landwirtschaft-ernte-versorgung"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(ana)
