"""A09 / analysis 5: Agrarreformen: Rittergüter 1647/1867, Ablösungsrenten 1867, Gesetze und Zerschlagung, Vereine (pp. 228-231)."""
import sys, re
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent))
from a09common import *

# ---------------------------------------------------------------- Rittergüter 1647 / 1867 (p. 230 b4)
g = grid("230", "b4")
LT = [("Gera", "Gera", 1), ("Schleiz", "Schleiz", 2), ("Lobenstein-Ebersdorf", "Lobenstein-Ebersdorf", 3), ("Fürstenthum", "Principality", 4)]
OWN = [("Adlige", "Nobility"), ("Bürgerliche", "Commoners"), ("Fürstliche", "Princely house")]
OWN_NR = {"Adlige": 1, "Bürgerliche": 2, "Fürstliche": 3}
ritter = []
printed_1867 = {}
for k, (lt, lten, ln) in enumerate(LT):
    r = g[1 + k]
    n1647 = num(r[1])
    n1867_printed = num(r[3])
    printed_1867[lt] = n1867_printed
    ritter.append([lt, lten, ln, 1647, "Adlige", "Nobility", 1, n1647, f"{lt} 1647", f"{lten} 1647"])
    parts = {}
    for n, w in re.findall(r'(\d+)\s+(Bürgerliche|"|Adlige|Adliger|Fürstliche)', r[4]):
        w = {'"': "Bürgerliche", "Adliger": "Adlige"}.get(w, w)
        parts[w] = parts.get(w, 0) + int(n)
    for w, (den, enn) in zip(("Adlige", "Bürgerliche", "Fürstliche"), OWN):
        if parts.get(w):
            ritter.append([lt, lten, ln, 1867, w, enn, OWN_NR[w], parts[w], f"{lt} 1867", f"{lten} 1867"])
    # check against count
    print(lt, n1647, n1867_printed, parts, sum(parts.values()))
# Gera 1867: printed 29, correction p. 831 lists 26
by = {}
for r in ritter:
    by[(r[0], r[3])] = by.get((r[0], r[3]), 0) + r[7]
print(by)
assert by[("Gera", 1867)] == 26 and by[("Schleiz", 1867)] == 6 and by[("Lobenstein-Ebersdorf", 1867)] == 9 and by[("Fürstenthum", 1867)] == 41

# ---------------------------------------------------------------- Ablösungsrenten (p. 230 b2)
items = block("230", "b2")["items"]
abl = []
for k, it in enumerate(items):
    t = it["text"]
    m = re.match(r'(\d+)\s*(?:Thlr\.|")\s*(\d+)\s*(?:Sgr\.|")', t)
    thlr, sgr = int(m.group(1)), int(m.group(2))
    lt, lten, ln = LT[k]
    # order in the list: Gera, Schleiz, Lobenstein-Ebersdorf, Fürstenthum
    abl.append([lt, lten, ln, thlr, sgr, round(thlr + sgr / 30, 2)])
print(abl)
assert sum(r[3] for r in abl[:3]) + (sum(r[4] for r in abl[:3])) // 30 == abl[3][3]
assert (sum(r[4] for r in abl[:3])) % 30 == abl[3][4]

# population 1864 per Landestheil (p. 211 b2, class 14 'Alle Berufsklassen zusammen', Summe)
g211 = grid("211", "b2")
pop = {"Gera": num(g211[4][10]), "Schleiz": num(g211[7][10]), "Lobenstein-Ebersdorf": num(g211[10][10]), "Fürstenthum": num(g211[13][10])}
print(pop)
for r in abl:
    r.append(pop[r[0]])
    r.append(round(100 * r[5] / abl[3][5], 1))
    r.append(round(100 * pop[r[0]] / pop["Fürstenthum"], 1))
    r.append(round(r[5] / pop[r[0]], 2))

# ---------------------------------------------------------------- Ereignisse (timeline)
EV = [
    # typ, label_de, label_en, von, bis, datum, geltung_de, geltung_en, faktor
    ("Gesetz", "Ablösung der Frohnen, Hutungsbefugnisse und Naturalabgaben (Lobenstein-Ebersdorf)", "Redemption of corvées, grazing rights and dues in kind (Lobenstein-Ebersdorf)", 1836, 1836, "1836-03-22", "Lobenstein-Ebersdorf", "Lobenstein-Ebersdorf", 20),
    ("Gesetz", "Ablösung aller Feudallasten (Gera)", "Redemption of all feudal burdens (Gera)", 1838, 1838, "1838-03-23", "Gera", "Gera", 25),
    ("Gesetz", "Ablösung der Triften auf Verlangen (Schleiz)", "Redemption of grazing servitudes on demand (Schleiz)", 1842, 1842, "1842-12-27", "Schleiz", "Schleiz", 25),
    ("Gesetz", "Freiwillige Ablösung weiterer Reallasten (Schleiz)", "Voluntary redemption of further real burdens (Schleiz)", 1843, 1843, "1843-02-18", "Schleiz", "Schleiz", None),
    ("Gesetz", "Beete- und Klauensteuer in Geldrente umwandelbar (Schleiz)", "Beete and Klauen taxes convertible into money rent (Schleiz)", 1845, 1845, "1845-07-17", "Schleiz", "Schleiz", 20),
    ("Gesetz", "Entwurf eines Ablösungsgesetzes für das Gesamtfürstenthum (nicht anerkannt)", "Draft redemption law for the whole principality (not recognized)", 1849, 1849, None, "Fürstenthum", "Principality", None),
    ("Gesetz", "Geraisches Gesetz von 1838 gilt für das ganze Fürstenthum; Landrentenbank", "Gera law of 1838 made valid for the whole principality; land annuity bank", 1858, 1858, "1858-01-15", "Fürstenthum", "Principality", 20),
    ("Gesetz", "Gesetz über die Zusammenlegung von Grundstücken (bisher nicht angewendet)", "Law on consolidation of plots (not yet applied)", 1860, 1860, "1860-10-08", "Fürstenthum", "Principality", None),
    ("Gesetz", "Novelle: Ablösung auch auf Verlangen der Berechtigten; Rauchzehnt in Körnerabgabe", "Amendment: redemption also on demand of the entitled; smoke tithe into grain levy", 1864, 1864, "1864-07-16", "Fürstenthum", "Principality", None),
    ("Gesetz", "Abspaltungs- und Zerschlagungssachen an die Bezirksausschüsse", "Cases of splitting and breaking up farms to the district committees", 1866, 1866, "1866-04-30", "Fürstenthum", "Principality", None),
    ("Zerschlagung", "Vorwerk Gräfenwarth", "Outlying farm Gräfenwarth", 1614, 1614, None, None, None, None),
    ("Zerschlagung", "Altengesees (Rittergut)", "Altengesees (manor)", 1763, 1763, None, None, None, None),
    ("Zerschlagung", "Gut Rödern", "Estate Rödern", 1783, 1783, None, None, None, None),
    ("Zerschlagung", "Halbes Rittergut Heinersdorf", "Half manor Heinersdorf", 1829, 1829, None, None, None, None),
    ("Zerschlagung", "Vorwerk Grumbach", "Outlying farm Grumbach", 1830, 1830, None, None, None, None),
    ("Zerschlagung", "Gut Pottiga", "Estate Pottiga", 1834, 1834, None, None, None, None),
    ("Zerschlagung", "Gut Mödlareuth", "Estate Mödlareuth", 1834, 1843, None, None, None, None),
    ("Zerschlagung", "Marstallwiesen bei Zollgrün", "Marstall meadows near Zollgrün", 1844, 1844, None, None, None, None),
    ("Zerschlagung", "Gut Benzka", "Estate Benzka", 1847, 1847, None, None, None, None),
    ("Zerschlagung", "Gut Frössen", "Estate Frössen", 1867, 1867, None, None, None, None),
]
TYP = {"Gesetz": ("Reformgesetz", "Reform law", 1), "Zerschlagung": ("Gutszerschlagung", "Break-up of an estate", 2)}
SHORT = {'Ablösung der Frohnen, Hutungsbefugnisse und Naturalabgaben (Lobenstein-Ebersdorf)': ('Ablösung (Lobenstein-Ebersdorf)', 'Redemption (Lobenstein-Ebersdorf)'), 'Ablösung aller Feudallasten (Gera)': ('Ablösung (Gera)', 'Redemption (Gera)'), 'Ablösung der Triften auf Verlangen (Schleiz)': ('Triftablösung (Schleiz)', 'Grazing servitudes (Schleiz)'), 'Freiwillige Ablösung weiterer Reallasten (Schleiz)': ('Weitere Reallasten (Schleiz)', 'Further burdens (Schleiz)'), 'Beete- und Klauensteuer in Geldrente umwandelbar (Schleiz)': ('Beete, Klauensteuer (Schleiz)', 'Beete, Klauen tax (Schleiz)'), 'Entwurf eines Ablösungsgesetzes für das Gesamtfürstenthum (nicht anerkannt)': ('Entwurf Gesamtgesetz', 'Draft general law'), 'Geraisches Gesetz von 1838 gilt für das ganze Fürstenthum; Landrentenbank': ('Ablösungsgesetz, ganzes Land', 'Redemption law, whole country'), 'Gesetz über die Zusammenlegung von Grundstücken (bisher nicht angewendet)': ('Zusammenlegung von Grundstücken', 'Consolidation of plots'), 'Novelle: Ablösung auch auf Verlangen der Berechtigten; Rauchzehnt in Körnerabgabe': ('Novelle zum Ablösungsgesetz', 'Amendment to the redemption law'), 'Abspaltungs- und Zerschlagungssachen an die Bezirksausschüsse': ('Zerschlagung von Bauerngütern', 'Break-up of peasant farms')}
ev_sorted = sorted(EV, key=lambda e: (TYP[e[0]][2], e[3], e[4]))
ereign = []
for k, e in enumerate(ev_sorted, 1):
    typ, lde, len_, von, bis, datum, gde, gen, fak = e
    ksd, kse = SHORT.get(lde, (lde, len_))
    ereign.append([TYP[typ][0], TYP[typ][1], TYP[typ][2], k, ksd, kse, lde, len_, von, bis, datum, gde, gen, fak])

# ---------------------------------------------------------------- Vereine (p. 231 b1)
g231 = grid("231", "b1")
vereine = []
for k in range(1, 5):
    r = g231[k]
    sitz = r[0].replace(" .", "").strip(" .")
    grund = int(re.match(r"(\d{4})", r[1]).group(1))
    erneut = 1855 if "1855" in r[1] else None
    members = num(r[2])
    baende = int(re.search(r"(\d+)", r[3]).group(1))
    vereine.append([sitz, k, grund, erneut, members, baende])
print(vereine)

# ---------------------------------------------------------------- numbers for the text
n47 = by[("Fürstenthum", 1647)]
n67 = by[("Fürstenthum", 1867)]
red = {lt: 100 * (by[(lt, 1647)] - by[(lt, 1867)]) / by[(lt, 1647)] for lt, _, _ in LT}
own67 = {w: sum(r[7] for r in ritter if r[0] == "Fürstenthum" and r[3] == 1867 and r[4] == w) for w, _ in OWN}
print(n47, n67, red, own67)
tot_abl = abl[3]
share_abl = {r[0]: (r[7], r[8]) for r in abl}
print(share_abl)
mem = sum(v[4] for v in vereine)
first_ev = [e for e in ev_sorted if e[0] == "Zerschlagung" and 1829 <= e[3] <= 1847]
n_zers = len([e for e in ev_sorted if e[0] == "Zerschlagung"])
print(mem, len(first_ev), n_zers)
oldest = min(vereine, key=lambda v: v[2])
largest = max(vereine, key=lambda v: v[4])

R_RITTER = {"page": "230", "block": "b4", "rows": "r2-r5"}
R_ABL = {"page": "230", "block": "b2", "rows": "i1-i4"}
R_VER = {"page": "231", "block": "b1", "rows": "r2-r5"}
R_EV = [{"page": "229", "block": "b1"}, {"page": "230", "block": "b3"}, {"page": "225", "block": "b1"}, {"page": "231", "block": "b3"}]
R_POP = {"page": "211", "block": "b2", "rows": "r5; r8; r11; r14"}
R_CORR = {"page": "831", "block": "b5"}


def col(name, de, en, typ, unit=None, derived=False, note=None):
    d = {"name": name, "label": bi(de, en), "type": typ, "unit": unit}
    if derived:
        d["derived"] = True
    if note:
        d["note"] = note
    return d


ana = {
    "id": "landwirtschaft-agrarreformen-1836-1868",
    "title": bi("Agrarreformen: Ablösung, Rittergüter und Vereine (1836–1868)", "Agrarian reforms: redemption of burdens, manors and societies (1836–1868)"),
    "category": "agriculture",
    "section": "t1-3-2",
    "sources": R_EV + [R_RITTER, R_ABL, R_VER, R_POP, R_CORR, {"page": "230", "block": "b5"}, {"page": "230", "block": "b6"}],
    "summary": bi(
        "Im Abschnitt »Geschichte der Landwirthschaft« nennt Brückner als Hebel des Aufschwungs die Ablösung der Feudallasten, die Zerschlagung von Kammer- und Rittergütern und die landwirthschaftlichen Vereine. Die Diagramme zeigen den Rückgang der Rittergüter und den Wandel ihrer Besitzer von 1647 bis 1867, die 1867 überwiesenen Ablösungsrenten, die Zeitleiste von Reformgesetzen und Gutszerschlagungen und die Mitgliederzahlen der vier Vereine.",
        "In the section “History of agriculture” Brückner names the redemption of feudal burdens, the break-up of chamber and manorial estates and the agricultural societies as levers of the upswing. The charts show the decline of the manors and the change of their owners from 1647 to 1867, the annual rents assigned for redemption in 1867, a timeline of reform laws and break-ups of estates, and the membership of the four societies."),
    "method": bi(
        f"Die Zahlen stammen aus der Tabelle der Rittergüter 1647 und 1867 (S. 230, Block b4), der Liste der Ablösungsrenten (S. 230, Block b2), der Vereinstabelle (S. 231) und den Datumsangaben im Fließtext (S. 225, 229–231). Die Besitzerangaben 1867 wurden aus den Zeilentexten (»14 Bürgerliche, 7 Adlige, 5 Fürstliche«) in Zahlen zerlegt; die Ditto-Zeichen (»\"«) stehen für »Bürgerliche«. Für die Zahl der Rittergüter in Gera 1867 gilt Brückners Berichtigung (S. 831, zu S. 230): 26 statt der gedruckten 29; sie stimmt mit der Summe der Besitzerangaben (14 + 7 + 5) überein. Ablösungsrenten sind als Thaler und Silbergroschen gedruckt; für den Vergleich wurden sie mit 1 Thaler = 30 Silbergroschen in Thaler umgerechnet (Währungsfaktor des preußischen Münzsystems, nicht aus Brückners Maßtabelle). Die Bevölkerung nach Landestheilen (1864) stammt aus der Berufsklassen-Tabelle (S. 211). In der Zeitleiste sind alle im Text mit Jahr genannten Reformgesetze und Gutszerschlagungen verzeichnet; undatierte Fälle (Lothra, Löhma) fehlen.",
        "The figures come from the table of manors in 1647 and 1867 (p. 230, block b4), the list of redemption rents (p. 230, block b2), the table of societies (p. 231) and the dates in the running text (pp. 225, 229–231). The owner statements for 1867 were split into numbers from the row texts (“14 Bürgerliche, 7 Adlige, 5 Fürstliche”); the ditto marks (“\"”) stand for “Bürgerliche”. For the number of manors in Gera in 1867 Brückner's correction (p. 831, to p. 230) applies: 26 instead of the printed 29; it agrees with the sum of the owner statements (14 + 7 + 5). Redemption rents are printed as Thaler and Silbergroschen; for comparison they were converted to Thaler with 1 Thaler = 30 Silbergroschen (conversion factor of the Prussian monetary system, not from Brückner's table of measures). The population by district (1864) comes from the occupational-class table (p. 211). The timeline lists all reform laws and break-ups of estates dated with a year in the text; undated cases (Lothra, Löhma) are omitted."),
    "findings": [
        bi(f"Die Zahl der Rittergüter sank von {n47} (1647, alle in adligem Besitz) auf {n67} (1867), also um {de_num(100*(n47-n67)/n47,0)} %; am stärksten in Schleiz ({de_num(red['Schleiz'],0)} %) und Lobenstein-Ebersdorf ({de_num(red['Lobenstein-Ebersdorf'],0)} %), am schwächsten in Gera ({de_num(red['Gera'],0)} %).",
           f"The number of manors fell from {n47} (1647, all in noble hands) to {n67} (1867), i.e. by {en_num(100*(n47-n67)/n47,0)} %; most in Schleiz ({en_num(red['Schleiz'],0)} %) and Lobenstein-Ebersdorf ({en_num(red['Lobenstein-Ebersdorf'],0)} %), least in Gera ({en_num(red['Gera'],0)} %)."),
        bi(f"1867 sind {own67['Bürgerliche']} der {n67} Rittergüter in bürgerlichem Besitz ({de_num(100*own67['Bürgerliche']/n67,0)} %), {own67['Adlige']} bei Adligen und {own67['Fürstliche']} bei Mitgliedern des Fürstenhauses; in Lobenstein-Ebersdorf gehören 8 von 9 Gütern Bürgerlichen.",
           f"In 1867, {own67['Bürgerliche']} of the {n67} manors are in bourgeois hands ({en_num(100*own67['Bürgerliche']/n67,0)} %), {own67['Adlige']} belong to nobles and {own67['Fürstliche']} to members of the princely house; in Lobenstein-Ebersdorf 8 of 9 estates belong to commoners."),
        bi(f"Ende Juli 1867 waren jährliche Ablösungsrenten von {tot_abl[3]} Thlr. {tot_abl[4]} Sgr. überwiesen; davon entfallen {de_num(share_abl['Lobenstein-Ebersdorf'][0])} % auf Lobenstein-Ebersdorf, das nur {de_num(share_abl['Lobenstein-Ebersdorf'][1])} % der Bevölkerung stellt, und {de_num(share_abl['Gera'][0])} % auf Gera ({de_num(share_abl['Gera'][1])} % der Bevölkerung). Brückner bemerkt dazu, dass ein großer Teil der Ablösungen, namentlich in Gera, durch Kapitalabfindung ohne Landrentenbank erfolgte.",
           f"At the end of July 1867 annual redemption rents of {tot_abl[3]} Thlr. {tot_abl[4]} Sgr. had been assigned; {en_num(share_abl['Lobenstein-Ebersdorf'][0])} % of this fall on Lobenstein-Ebersdorf, which has only {en_num(share_abl['Lobenstein-Ebersdorf'][1])} % of the population, and {en_num(share_abl['Gera'][0])} % on Gera ({en_num(share_abl['Gera'][1])} % of the population). Brückner remarks that a large part of the redemptions, notably in Gera, was settled by capital payment without the land annuity bank."),
        bi(f"Von den {n_zers} datierten Gutszerschlagungen fallen {len(first_ev)} in die Jahre 1829–1847; die Reformgesetze folgen von 1836 (Lobenstein-Ebersdorf) über 1838 (Gera) und 1842–45 (Schleiz) bis zum einheitlichen Gesetz von 1858 und der Novelle von 1864.",
           f"Of the {n_zers} dated break-ups of estates, {len(first_ev)} fall in the years 1829–1847; the reform laws run from 1836 (Lobenstein-Ebersdorf) through 1838 (Gera) and 1842–45 (Schleiz) to the uniform law of 1858 and the amendment of 1864."),
        bi(f"Die vier landwirthschaftlichen Vereine hatten 1868 zusammen {mem} Mitglieder; der älteste ist der geraer Verein ({oldest[2]}), der mitgliederstärkste der ebersdorfer ({largest[4]} Mitglieder, gegründet {largest[2]}).",
           f"The four agricultural societies had {mem} members in total in 1868; the oldest is the Gera society ({oldest[2]}), the largest the Ebersdorf society ({largest[4]} members, founded {largest[2]})."),
    ],
    "caveats": [
        bi("Die Zahl der Rittergüter in Gera 1867 ist in der Tabelle mit 29 gedruckt; Brückners Berichtigung (S. 831) verlangt 26, was zu den Besitzerzahlen und zur Summe 41 passt. Der Text (S. 230) nennt 31 zerschlagene oder in Kammergüter verwandelte Rittergüter; die Differenz 72 − 41 = 31 stimmt damit überein.",
           "The number of manors in Gera in 1867 is printed as 29 in the table; Brückner's correction (p. 831) requires 26, which fits the owner figures and the total of 41. The text (p. 230) mentions 31 manors broken up or converted into chamber estates; the difference 72 − 41 = 31 agrees with this."),
        bi("Die Ablösungsrenten sind Jahresrenten (Stand Ende Juli 1867), keine Kapitalbeträge; die Ablösung durch Kapitalzahlung (20- bis 25faches der Rente) ist darin nicht enthalten. Ein Vergleich der Landestheile ist wegen der unterschiedlichen Gesetze (1836, 1838, 1842–45) nur bedingt aussagekräftig.",
           "The redemption rents are annual rents (as of end of July 1867), not capital sums; redemption by capital payment (20 to 25 times the rent) is not included. A comparison of the districts is of limited value because of the different laws (1836, 1838, 1842–45)."),
        bi("Die Zeitleiste enthält nur Ereignisse, die Brückner mit einer Jahreszahl nennt; bei Mödlareuth gibt er den Zeitraum 1834 bis 1843 an. Die Zuordnung der Zerschlagungen zu den Landestheilen ist im Text nicht angegeben.",
           "The timeline contains only events that Brückner dates with a year; for Mödlareuth he gives the period 1834 to 1843. The text does not state in which district each break-up took place."),
    ],
    "conversions": [
        {"from": "Silbergroschen", "to": "Thaler", "factor_or_formula": "1 Thaler = 30 Silbergroschen", "reference": "preußisches Münzsystem; nicht in Brückners Tabelle (S. 830–832)"},
    ],
    "datasets": [
        {"name": "rittergueter", "title": bi("Rittergüter 1647 und 1867 nach Besitzern", "Manors in 1647 and 1867 by owner"),
         "columns": [
             col("landestheil_de", "Landestheil", "District", "string"),
             col("landestheil_en", "Landestheil (englisch)", "District (English)", "string"),
             col("lt_nr", "Reihenfolge Landestheil", "District order", "integer", derived=True),
             col("jahr", "Jahr", "Year", "integer"),
             col("besitzer_de", "Besitzer", "Owner", "string"),
             col("besitzer_en", "Besitzer (englisch)", "Owner (English)", "string"),
             col("besitzer_nr", "Reihenfolge Besitzer", "Owner order", "integer", derived=True),
             col("anzahl", "Zahl der Rittergüter", "Number of manors", "integer", "Rittergüter", note="Gera 1867 insgesamt 26 nach Brückners Berichtigung S. 831 (gedruckt 29)"),
             col("balken_de", "Balken", "Bar label", "string", derived=True),
             col("balken_en", "Balken (englisch)", "Bar label (English)", "string", derived=True),
         ],
         "rows": ritter, "source_refs": [R_RITTER, R_CORR]},
        {"name": "abloesung", "title": bi("Ablösungsrenten Ende Juli 1867", "Redemption rents, end of July 1867"),
         "columns": [
             col("landestheil_de", "Landestheil", "District", "string"),
             col("landestheil_en", "Landestheil (englisch)", "District (English)", "string"),
             col("lt_nr", "Reihenfolge", "Order", "integer", derived=True),
             col("thlr", "Jahresrente (Thaler)", "Annual rent (Thaler)", "integer", "Thlr."),
             col("sgr", "Jahresrente (Silbergroschen)", "Annual rent (Silbergroschen)", "integer", "Sgr."),
             col("thaler", "Jahresrente in Thalern", "Annual rent in Thaler", "number", "Thlr.", derived=True, note="Thaler + Silbergroschen / 30"),
             col("bevoelkerung", "Bevölkerung 1864", "Population 1864", "integer", "Personen"),
             col("anteil_rente", "Anteil an der Gesamtrente", "Share of total rent", "number", "%", derived=True),
             col("anteil_bev", "Anteil an der Bevölkerung", "Share of population", "number", "%", derived=True),
             col("rente_je_kopf", "Rente je Einwohner", "Rent per inhabitant", "number", "Thlr.", derived=True),
         ],
         "rows": abl, "source_refs": [R_ABL, R_POP]},
        {"name": "ereignisse", "title": bi("Reformgesetze und Gutszerschlagungen", "Reform laws and break-ups of estates"),
         "columns": [
             col("typ_de", "Art des Ereignisses", "Kind of event", "string"),
             col("typ_en", "Art des Ereignisses (englisch)", "Kind of event (English)", "string"),
             col("typ_nr", "Reihenfolge Art", "Order of kind", "integer", derived=True),
             col("nr", "Laufende Nummer", "Serial number", "integer", derived=True),
             col("kurz_de", "Ereignis (Kurzform)", "Event (short)", "string"),
             col("kurz_en", "Ereignis (Kurzform, englisch)", "Event (short, English)", "string"),
             col("ereignis_de", "Ereignis", "Event", "string"),
             col("ereignis_en", "Ereignis (englisch)", "Event (English)", "string"),
             col("jahr_von", "Jahr (Beginn)", "Year (start)", "integer"),
             col("jahr_bis", "Jahr (Ende)", "Year (end)", "integer"),
             col("datum", "Datum des Gesetzes", "Date of the law", "date"),
             col("geltung_de", "Geltungsbereich", "Scope", "string"),
             col("geltung_en", "Geltungsbereich (englisch)", "Scope (English)", "string"),
             col("kapitalfaktor", "Kapitalisierung der Rente (Vielfaches)", "Capitalization of the rent (multiple)", "integer", "×"),
         ],
         "rows": ereign, "source_refs": R_EV},
        {"name": "vereine", "title": bi("Land- und forstwirthschaftliche Vereine", "Agricultural and forestry societies"),
         "columns": [
             col("sitz", "Sitz", "Seat", "string"),
             col("nr", "Reihenfolge", "Order", "integer", derived=True),
             col("gruendung", "Gründungsjahr", "Year of foundation", "integer"),
             col("erneuert", "erneut", "Renewed", "integer"),
             col("mitglieder", "Mitglieder 1868", "Members 1868", "integer", "Personen"),
             col("baende", "Bände der Bibliothek", "Volumes in the library", "integer", "Bände"),
         ],
         "rows": vereine, "source_refs": [R_VER]},
    ],
    "charts": [
        {"id": "c1", "dataset": "rittergueter",
         "title": bi("Rittergüter 1647 und 1867 nach Besitzern", "Manors in 1647 and 1867 by owner"),
         "caption": bi("Zahl der Rittergüter je Landestheil. 1647 waren alle in adligem Besitz; 1867 gehört die Mehrzahl Bürgerlichen. Gera 1867 nach Brückners Berichtigung (26 statt 29).",
                       "Number of manors per district. In 1647 all were in noble hands; in 1867 the majority belong to commoners. Gera 1867 according to Brückner's correction (26 instead of 29)."),
         "vegalite": {
             "height": 300,
             "mark": "bar",
             "encoding": {
                 "y": {"field": {"de": "balken_de", "en": "balken_en"}, "type": "nominal", "sort": {"field": "lt_nr", "op": "min"}, "title": None, "axis": {"labelLimit": 260}},
                 "x": {"field": "anzahl", "type": "quantitative", "title": bi("Zahl der Rittergüter", "Number of manors")},
                 "color": {"field": {"de": "besitzer_de", "en": "besitzer_en"}, "type": "nominal", "title": None,
                           "scale": {"domain": [bi("Adlige", "Nobility"), bi("Bürgerliche", "Commoners"), bi("Fürstliche", "Princely house")]}},
                 "order": {"field": "besitzer_nr", "type": "quantitative"},
                 "tooltip": [{"field": {"de": "balken_de", "en": "balken_en"}, "title": bi("Landestheil und Jahr", "District and year")},
                             {"field": {"de": "besitzer_de", "en": "besitzer_en"}, "title": bi("Besitzer", "Owner")},
                             {"field": "anzahl", "title": bi("Zahl", "Number")}]}}},
        {"id": "c2", "dataset": "abloesung",
         "title": bi("Überwiesene Ablösungsrenten 1867", "Redemption rents assigned in 1867"),
         "caption": bi("Jährliche Rente in Thalern je Landestheil (Stand Ende Juli 1867). Lobenstein-Ebersdorf liegt weit vorn, obwohl es die kleinste Bevölkerung hat.",
                       "Annual rent in Thaler per district (as of end of July 1867). Lobenstein-Ebersdorf is far ahead although it has the smallest population."),
         "vegalite": {
             "height": 240,
             "transform": [{"filter": "datum.lt_nr < 4"}],
             "mark": "bar",
             "encoding": {
                 "x": {"field": {"de": "landestheil_de", "en": "landestheil_en"}, "type": "nominal", "sort": {"field": "lt_nr", "op": "min"}, "title": None, "axis": {"labelAngle": 0}},
                 "y": {"field": "thaler", "type": "quantitative", "title": bi("Thaler im Jahr", "Thaler per year"), "axis": {"format": ",.0f"}},
                 "tooltip": [{"field": {"de": "landestheil_de", "en": "landestheil_en"}, "title": bi("Landestheil", "District")},
                             {"field": "thlr", "title": "Thlr.", "format": ","}, {"field": "sgr", "title": "Sgr."},
                             {"field": "anteil_rente", "title": bi("% der Gesamtrente", "% of total rent"), "format": ".1f"},
                             {"field": "anteil_bev", "title": bi("% der Bevölkerung", "% of population"), "format": ".1f"},
                             {"field": "rente_je_kopf", "title": bi("Thaler je Einwohner", "Thaler per inhabitant"), "format": ".2f"}]}}},
        {"id": "c3", "dataset": "ereignisse",
         "title": bi("Reformgesetze und Gutszerschlagungen", "Reform laws and break-ups of estates"),
         "caption": bi("Von Brückner mit Jahr genannte Ereignisse seit 1750 (die Zerschlagung des Vorwerks Gräfenwarth 1614 ist nicht dargestellt); die Linie bei Mödlareuth zeigt den Zeitraum 1834–1843. Die Zerschlagungen häufen sich in den Jahren der Ablösungsgesetze.",
                       "Events dated with a year by Brückner since 1750 (the break-up of the outlying farm Gräfenwarth in 1614 is not shown); the line for Mödlareuth shows the period 1834–1843. The break-ups cluster in the years of the redemption laws."),
         "vegalite": {
             "height": 440,
             "transform": [{"filter": "datum.jahr_von >= 1750"}],
             "layer": [
                 {"mark": {"type": "rule", "strokeWidth": 5, "opacity": 1},
                  "transform": [{"filter": "datum.jahr_bis > datum.jahr_von"}],
                  "encoding": {"y": {"field": {"de": "kurz_de", "en": "kurz_en"}, "type": "nominal", "sort": {"field": "nr", "op": "min"}, "title": None, "axis": {"labelLimit": 260}},
                               "x": {"field": "jahr_von", "type": "quantitative", "scale": {"domain": [1750, 1880]}, "axis": {"format": "d", "values": [1750, 1775, 1800, 1825, 1850, 1875]}, "title": bi("Jahr", "Year")},
                               "x2": {"field": "jahr_bis"},
                               "color": {"field": {"de": "typ_de", "en": "typ_en"}, "type": "nominal", "title": None,
                                         "scale": {"domain": [bi("Reformgesetz", "Reform law"), bi("Gutszerschlagung", "Break-up of an estate")]}}}},
                 {"mark": {"type": "point", "filled": True, "size": 100, "opacity": 1},
                  "encoding": {"y": {"field": {"de": "kurz_de", "en": "kurz_en"}, "type": "nominal", "sort": {"field": "nr", "op": "min"}, "title": None, "axis": {"labelLimit": 260}},
                               "x": {"field": "jahr_von", "type": "quantitative", "scale": {"domain": [1750, 1880]}, "axis": {"format": "d", "values": [1750, 1775, 1800, 1825, 1850, 1875]}, "title": bi("Jahr", "Year")},
                               "color": {"field": {"de": "typ_de", "en": "typ_en"}, "type": "nominal", "title": None,
                                         "scale": {"domain": [bi("Reformgesetz", "Reform law"), bi("Gutszerschlagung", "Break-up of an estate")]}},
                               "tooltip": [{"field": {"de": "ereignis_de", "en": "ereignis_en"}, "title": bi("Ereignis", "Event")},
                                           {"field": "jahr_von", "title": bi("Jahr", "Year"), "format": "d"},
                                           {"field": "jahr_bis", "title": bi("bis", "until"), "format": "d"},
                                           {"field": "datum", "title": bi("Datum", "Date")},
                                           {"field": "kapitalfaktor", "title": bi("Kapitalisierung (Vielfaches)", "Capitalization (multiple)")}]}}]}},
        {"id": "c4", "dataset": "vereine",
         "title": bi("Land- und forstwirthschaftliche Vereine 1868", "Agricultural and forestry societies, 1868"),
         "caption": bi("Mitglieder der vier Vereine 1868 (Gründungsjahr und Bibliotheksbestand im Tooltip). Der ebersdorfer Verein, 1853 gegründet, hat die meisten Mitglieder.",
                       "Members of the four societies in 1868 (year of foundation and library holdings in the tooltip). The Ebersdorf society, founded in 1853, has the most members."),
         "vegalite": {
             "height": 240,
             "mark": "bar",
             "encoding": {
                 "x": {"field": "sitz", "type": "nominal", "sort": {"field": "gruendung", "op": "min"}, "title": bi("Sitz des Vereins (nach Gründungsjahr)", "Seat of the society (by year of foundation)"), "axis": {"labelAngle": 0}},
                 "y": {"field": "mitglieder", "type": "quantitative", "title": bi("Mitglieder", "Members")},
                 "tooltip": [{"field": "sitz", "title": bi("Sitz", "Seat")}, {"field": "gruendung", "title": bi("gegründet", "founded"), "format": "d"},
                             {"field": "mitglieder", "title": bi("Mitglieder 1868", "Members 1868")}, {"field": "baende", "title": bi("Bände der Bibliothek", "Library volumes")}]}}},
    ],
    "keywords": {
        "de": ["Ablösung", "Feudallasten", "Frohnen", "Rittergüter", "Kammergüter", "Zerschlagung", "Landrentenbank", "landwirtschaftlicher Verein", "Agrarreform", "Gewerbefreiheit"],
        "en": ["redemption", "feudal burdens", "corvée", "manors", "chamber estates", "break-up of estates", "land annuity bank", "agricultural society", "agrarian reform"],
    },
    "related": ["landwirtschaft-kammer-rittergueter-1854", "landwirtschaft-grundbesitz-1854"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
# drop the unneeded keyword that is not covered by this analysis
ana["keywords"]["de"].remove("Gewerbefreiheit")
write_analysis(ana)
