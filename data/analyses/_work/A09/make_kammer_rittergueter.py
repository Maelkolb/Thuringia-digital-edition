"""A09 / analysis 4: Kammergüter und Rittergüter (pp. 218-223): Flächen je Gut."""
import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent))
from a09common import *
import estates_parse as ep

K, KT = ep.kammer_rows()
R, RT = ep.ritter_estates()

# ---------------------------------------------------------------- names / owners
RENAME = {
    "ob. u. mittl. Theils": "Köstritz, ob. u. mittl. Theil",
    "unteren Theils": "Köstritz, unterer Theil",
    "Frössen: a) ein Grundstücksverband": "Frössen, a) Grundstücksverband",
    "b) Hohenpreis": "Frössen, b) Hohenpreis",
    "a) Rittergut r. A": "Mödlareuth, a) Rittergut r. A.",
    "b) Ritterg. Töpen r. A": "Mödlareuth, b) Rittergut Töpen r. A.",
    "Roschitz r. A": "Roschitz r. A.",
    "Hartmannsdorf": "Hartmannsdorf",
}
FUERST = "Heinrich LXIX., Fürst Reuß-Köstritz"
OWNER_FIX = {
    "ob. u. mittl. Theils": FUERST, "unteren Theils": FUERST, "Pohlitz": FUERST, "Hartmannsdorf": FUERST, "Dürrenberg": FUERST,
    "Frössen: a) ein Grundstücksverband": "Carl Fr. Wieprecht, Stadtrath; Wittwe Julie Amalie Hartenstein",
    "b) Ritterg. Töpen r. A": "Hauptmann Karl v. Reitzenstein in Bayreuth; Ehefrau Charlotte geb. v. Tettenborn",
}
LTEN = {"Gera": "Gera", "Schleiz": "Schleiz", "Lobenstein-Ebersdorf": "Lobenstein-Ebersdorf"}
LTNR = {"Gera": 1, "Schleiz": 2, "Lobenstein-Ebersdorf": 3}


def clean_owner(s):
    s = s.strip().rstrip(".")
    return s


rows = []
FIELDS = ["hof", "garten", "feld", "wiese", "nadel", "laub", "hut", "wasser"]
for e in K:
    gew = e["gewinn"].strip() or None
    tot = round(sum((e[f] or 0) for f in FIELDS), 2)
    rows.append(["Kammergut", "Chamber estate (Kammergut)", e["lt"], LTEN[e["lt"]], e["name"], e["hof"], e["garten"], e["feld"], e["wiese"], e["nadel"], e["laub"], e["hut"], e["wasser"],
                 e["steuer"], tot, round(tot * MORGEN_HA, 1), None, gew])
for e in R:
    own = OWNER_FIX.get(e["name"]) or clean_owner(e["besitzer"]) or None
    nm = RENAME.get(e["name"], e["name"])
    tot = round(sum((e[f] or 0) for f in FIELDS), 2)
    rows.append(["Rittergut", "Manorial estate (Rittergut)", e["lt"], LTEN[e["lt"]], nm, e["hof"], e["garten"], e["feld"], e["wiese"], e["nadel"], e["laub"], e["hut"], e["wasser"],
                 e["steuer"], tot, round(tot * MORGEN_HA, 1), own, None])
print(len(K), "Kammergüter;", len(R), "Rittergüter")

COLS = ["art_de", "art_en", "landestheil_de", "landestheil_en", "name", "hof", "garten", "feld", "wiese", "nadel", "laub", "hut", "wasser", "steuer", "gesamt_morgen", "gesamt_ha", "besitzer", "gewinnzeit"]
idx = {c: i for i, c in enumerate(COLS)}

# ---------------------------------------------------------------- summary dataset (derived sums)
CATS = [  # nr, de, en, fields
    (1, "Hof und Garten", "Farmstead and garden", ("hof", "garten")),
    (2, "Feld", "Arable land", ("feld",)),
    (3, "Wiese", "Meadow", ("wiese",)),
    (4, "Hut und Weg", "Pasture and tracks", ("hut",)),
    (5, "Nadelwald", "Coniferous wood", ("nadel",)),
    (6, "Laubwald", "Deciduous wood", ("laub",)),
    (7, "Wasser", "Water", ("wasser",)),
]
ARTS = [("Kammergut", "Kammergüter", "Chamber estates", 1), ("Rittergut", "Rittergüter", "Manorial estates", 2)]
REG = [("Gera", "Gera", 1), ("Schleiz", "Schleiz", 2), ("Lobenstein-Ebersdorf", "Lobenstein-Ebersdorf", 3), ("zusammen", "total", 4)]
summ = []
group_tot = {}
for a, ade, aen, an in ARTS:
    for lt, lten, ln in REG:
        sel = [r for r in rows if r[0] == a and (lt == "zusammen" or r[2] == lt)]
        sums = {}
        for cn, cde, cen, flds in CATS:
            sums[cn] = round(sum((r[idx[f]] or 0) for r in sel for f in flds), 2)
        tot = sum(sums.values())
        group_tot[(a, lt)] = (tot, len(sel), sums)
        for cn, cde, cen, flds in CATS:
            summ.append([ade, aen, an, lt if lt != "zusammen" else "Zusammen", lten if lt != "zusammen" else "Total", ln,
                         f"{ade}, {lt}" if lt != "zusammen" else f"{ade}, zusammen", f"{aen}, {lten}" if lt != "zusammen" else f"{aen}, total",
                         an * 10 + ln, cde, cen, cn, sums[cn], round(sums[cn] * MORGEN_HA, 0), round(100 * sums[cn] / tot, 2), len(sel)])
for k, v in group_tot.items():
    print(k, round(v[0], 1), v[1])

# ---------------------------------------------------------------- top estates (long format)
est = sorted(rows, key=lambda r: -r[idx["gesamt_morgen"]])[:15]
top = []
for rk, r in enumerate(est, 1):
    de_art = "Kammergut" if r[0] == "Kammergut" else "Rittergut"
    en_art = "chamber estate" if r[0] == "Kammergut" else "manorial estate"
    short = {"Lobenstein-Ebersdorf": "Lob.-Ebersd."}
    lab_de = f"{r[idx['name']]} ({de_art}, {short.get(r[2], r[2])})"
    lab_en = f"{r[idx['name']]} ({en_art}, {short.get(r[3], r[3])})"
    for cn, cde, cen, flds in CATS:
        v = round(sum((r[idx[f]] or 0) for f in flds), 2)
        top.append([rk, lab_de, lab_en, de_art, r[2], cde, cen, cn, v, round(v * MORGEN_HA, 1), r[idx["gesamt_morgen"]], r[idx["gesamt_ha"]]])
print([(r[idx['name']], r[idx['gesamt_morgen']], r[0]) for r in est])

# ---------------------------------------------------------------- numbers for the text
def share(a, lt, cats):
    tot, n, sums = group_tot[(a, lt)]
    return 100 * sum(sums[c] for c in cats) / tot


K_tot, K_n, K_s = group_tot[("Kammergut", "zusammen")]
R_tot, R_n, R_s = group_tot[("Rittergut", "zusammen")]
wald_K, wald_R = share("Kammergut", "zusammen", (5, 6)), share("Rittergut", "zusammen", (5, 6))
feld_K, feld_R = share("Kammergut", "zusammen", (2,)), share("Rittergut", "zusammen", (2,))
feldK = {lt: share("Kammergut", lt, (2,)) for lt in ("Gera", "Schleiz", "Lobenstein-Ebersdorf")}
waldK = {lt: share("Kammergut", lt, (5, 6)) for lt in ("Gera", "Schleiz", "Lobenstein-Ebersdorf")}
wiesK = {lt: share("Kammergut", lt, (3,)) for lt in ("Gera", "Schleiz", "Lobenstein-Ebersdorf")}
waldR = {lt: share("Rittergut", lt, (5, 6)) for lt in ("Gera", "Schleiz", "Lobenstein-Ebersdorf")}
feldR = {lt: share("Rittergut", lt, (2,)) for lt in ("Gera", "Schleiz", "Lobenstein-Ebersdorf")}
Rn = {lt: group_tot[("Rittergut", lt)][1] for lt in ("Gera", "Schleiz", "Lobenstein-Ebersdorf")}
mean_K = K_tot / K_n
mean_R = R_tot / R_n
big = est[:3]
steuer_K = sum(r[idx["steuer"]] or 0 for r in rows if r[0] == "Kammergut")
steuer_R = sum(r[idx["steuer"]] or 0 for r in rows if r[0] == "Rittergut")
print(wald_K, wald_R, feld_K, feld_R, feldK, waldK, wiesK, waldR, feldR, Rn, mean_K, mean_R, steuer_K, steuer_R)
print("ha", K_tot * MORGEN_HA, R_tot * MORGEN_HA)
ritter_ge_mean = group_tot[("Rittergut", "Gera")][0] / Rn["Gera"]
ritter_sc_mean = group_tot[("Rittergut", "Schleiz")][0] / Rn["Schleiz"]
ritter_le_mean = group_tot[("Rittergut", "Lobenstein-Ebersdorf")][0] / Rn["Lobenstein-Ebersdorf"]
print(ritter_ge_mean, ritter_sc_mean, ritter_le_mean)

R_REFS = [
    {"page": "218", "block": "b2", "rows": "r3-r38"}, {"page": "219", "block": "b1", "rows": "r2-r35"},
    {"page": "220", "block": "b1", "rows": "r2-r24"}, {"page": "221", "block": "b1", "rows": "r2-r23"},
    {"page": "220", "block": "b3", "rows": "r3-r11"}, {"page": "221", "block": "b2", "rows": "r2-r11"},
    {"page": "222", "block": "b1", "rows": "r2-r43"}, {"page": "223", "block": "b1", "rows": "r3-r42"},
]


def col(name, de, en, typ, unit=None, derived=False, note=None):
    d = {"name": name, "label": bi(de, en), "type": typ, "unit": unit}
    if derived:
        d["derived"] = True
    if note:
        d["note"] = note
    return d


ISS = [dict(page=a["page"], block=a["block"], cell=a["cell"], transcribed=a["transcribed"], facsimile=a["facsimile"], checked_facsimile=True,
            note=f"{a['estate']}, Spalte {a['field']}; Ziffer 7 als 1 gelesen / digit 7 read as 1" if a["transcribed"][-2] == "1" and a["facsimile"][-2] == "7" else f"{a['estate']}, Spalte {a['field']}")
       for a in ep.APPLIED]
print(len(ISS), "transcription issues")

CATLIST = [bi(c[1], c[2]) for c in CATS]
ana = {
    "id": "landwirtschaft-kammer-rittergueter-1854",
    "title": bi("Kammergüter und Rittergüter: Fläche und Nutzung der einzelnen Güter", "Chamber estates and manorial estates: area and use of the individual estates"),
    "category": "agriculture",
    "section": "t1-3-2",
    "sources": R_REFS + [{"page": "831", "block": "b5"}],
    "summary": bi(
        f"Brückner listet alle Kammergüter ({K_n} Einträge) und Rittergüter ({R_n} Einträge) des Fürstenthums mit Hofraum, Gärten, Feld, Wiese, Wald, Hutung, Wasser und Steuerwerth. Zusammen umfassen sie rund {de_num(K_tot+R_tot,0)} Morgen ({de_num((K_tot+R_tot)*MORGEN_HA,0)} ha). Die Diagramme vergleichen die Zusammensetzung der Flächen nach Besitzart und Landestheil und zeigen die größten Güter.",
        f"Brückner lists all chamber estates ({K_n} entries) and manorial estates ({R_n} entries) of the principality with farmstead, gardens, arable land, meadow, woodland, pasture, water and tax value. Together they cover about {en_num(K_tot+R_tot,0)} Morgen ({en_num((K_tot+R_tot)*MORGEN_HA,0)} ha). The charts compare the composition of the land by type of owner and district and show the largest estates."),
    "method": bi(
        "Die Gutstabellen sind über je zwei Seiten gebrochen (links die Flächen bis Nadelwald bzw. Laubwald, rechts Hutung, Wasser, Steuerwerth und Gewinnzeit bzw. Besitzer); die Hälften wurden zeilenweise zusammengeführt (S. 218/219, 220/221 für die Kammergüter, S. 220/222 und 221/223 für die Rittergüter). Die Zuordnung der Besitzerzeilen bei Frössen und Mödlareuth folgt der Klammerung im Faksimile. Alle Summen und Anteile in den Diagrammen sind aus den Einzelwerten der Güter berechnet, nicht aus Brückners gedruckten Summenzeilen. Zehn Zahlen wurden nach Prüfung am Faksimile berichtigt (siehe transcription_issues). »Hof und Garten« fasst Hofraum und Gärten zusammen. Umrechnung in Hektar mit Brückners Tabelle (S. 832): 1 preuß. Morgen = 0,255322 ha.",
        "The estate tables are split across two pages (on the left the areas up to coniferous or deciduous wood, on the right pasture, water, tax value and date of acquisition or owner); the halves were merged row by row (pp. 218/219, 220/221 for the chamber estates, pp. 220/222 and 221/223 for the manorial estates). The assignment of the owner rows for Frössen and Mödlareuth follows the bracketing in the facsimile. All sums and shares in the charts are computed from the values of the individual estates, not from Brückner's printed total rows. Ten figures were corrected after checking the facsimile (see transcription_issues). “Farmstead and garden” combines Hofraum and Gärten. Conversion to hectares with Brückner's table (p. 832): 1 Prussian Morgen = 0.255322 ha."),
    "findings": [
        bi(f"Die {K_n} Kammergut-Einträge umfassen zusammen {de_num(K_tot,0)} Morgen ({de_num(K_tot*MORGEN_HA,0)} ha), die {R_n} Rittergut-Einträge {de_num(R_tot,0)} Morgen ({de_num(R_tot*MORGEN_HA,0)} ha); ein Kammergut ist im Mittel {de_num(mean_K,0)} Morgen groß, ein Rittergut {de_num(mean_R,0)} Morgen.",
           f"The {K_n} chamber-estate entries together cover {en_num(K_tot,0)} Morgen ({en_num(K_tot*MORGEN_HA,0)} ha), the {R_n} manorial-estate entries {en_num(R_tot,0)} Morgen ({en_num(R_tot*MORGEN_HA,0)} ha); a chamber estate averages {en_num(mean_K,0)} Morgen, a manorial estate {en_num(mean_R,0)} Morgen."),
        bi(f"Die Kammergüter sind stärker mit Wald ausgestattet ({de_num(wald_K)} % ihrer Fläche) als die Rittergüter ({de_num(wald_R)} %), die dafür mehr Feld haben ({de_num(feld_R)} % gegenüber {de_num(feld_K)} %).",
           f"The chamber estates have more woodland ({en_num(wald_K)} % of their area) than the manorial estates ({en_num(wald_R)} %), which in turn have more arable land ({en_num(feld_R)} % against {en_num(feld_K)} %)."),
        bi(f"Die Kammergüter des Oberlandes haben deutlich mehr Wiese ({de_num(wiesK['Schleiz'])} % in Schleiz, {de_num(wiesK['Lobenstein-Ebersdorf'])} % in Lobenstein-Ebersdorf) als die des Unterlandes ({de_num(wiesK['Gera'])} % in Gera); der Feldanteil liegt bei {de_num(feldK['Gera'])} %, {de_num(feldK['Schleiz'])} % und {de_num(feldK['Lobenstein-Ebersdorf'])} %. Bei den Rittergütern ist der Gegensatz stärker: Gera {de_num(feldR['Gera'])} % Feld und {de_num(waldR['Gera'])} % Wald, Schleiz dagegen {de_num(feldR['Schleiz'])} % Feld und {de_num(waldR['Schleiz'])} % Wald.",
           f"The chamber estates of the Upper Land have markedly more meadow ({en_num(wiesK['Schleiz'])} % in Schleiz, {en_num(wiesK['Lobenstein-Ebersdorf'])} % in Lobenstein-Ebersdorf) than those of the Lower Land ({en_num(wiesK['Gera'])} % in Gera); the share of arable land is {en_num(feldK['Gera'])} %, {en_num(feldK['Schleiz'])} % and {en_num(feldK['Lobenstein-Ebersdorf'])} %. For the manorial estates the contrast is stronger: Gera {en_num(feldR['Gera'])} % arable and {en_num(waldR['Gera'])} % woodland, Schleiz {en_num(feldR['Schleiz'])} % arable and {en_num(waldR['Schleiz'])} % woodland."),
        bi(f"Die Rittergüter liegen überwiegend im Unterland: {Rn['Gera']} der {R_n} Einträge im Landestheil Gera, {Rn['Schleiz']} in Schleiz und {Rn['Lobenstein-Ebersdorf']} in Lobenstein-Ebersdorf; im Mittel sind sie in Schleiz mit {de_num(ritter_sc_mean,0)} Morgen am größten, in Gera {de_num(ritter_ge_mean,0)} Morgen und in Lobenstein-Ebersdorf mit {de_num(ritter_le_mean,0)} Morgen am kleinsten.",
           f"The manorial estates lie mainly in the Lower Land: {Rn['Gera']} of the {R_n} entries in the district of Gera, {Rn['Schleiz']} in Schleiz and {Rn['Lobenstein-Ebersdorf']} in Lobenstein-Ebersdorf; on average they are largest in Schleiz at {en_num(ritter_sc_mean,0)} Morgen, {en_num(ritter_ge_mean,0)} Morgen in Gera and smallest in Lobenstein-Ebersdorf at {en_num(ritter_le_mean,0)} Morgen."),
        bi(f"Das größte Gut ist {est[0][idx['name']]} ({est[0][0]}, {est[0][2]}) mit {de_num(est[0][idx['gesamt_morgen']],0)} Morgen ({de_num(est[0][idx['gesamt_ha']],0)} ha), gefolgt von {est[1][idx['name']]} ({de_num(est[1][idx['gesamt_morgen']],0)} Morgen) und {est[2][idx['name']]} ({de_num(est[2][idx['gesamt_morgen']],0)} Morgen). Unter den 15 größten Gütern befinden sich {sum(1 for r in est if r[0]=='Kammergut')} Kammergüter und {sum(1 for r in est if r[0]=='Rittergut')} Rittergüter.",
           f"The largest estate is {est[0][idx['name']]} ({'chamber estate' if est[0][0]=='Kammergut' else 'manorial estate'}, {est[0][2]}) with {en_num(est[0][idx['gesamt_morgen']],0)} Morgen ({en_num(est[0][idx['gesamt_ha']],0)} ha), followed by {est[1][idx['name']]} ({en_num(est[1][idx['gesamt_morgen']],0)} Morgen) and {est[2][idx['name']]} ({en_num(est[2][idx['gesamt_morgen']],0)} Morgen). Among the 15 largest estates there are {sum(1 for r in est if r[0]=='Kammergut')} chamber estates and {sum(1 for r in est if r[0]=='Rittergut')} manorial estates."),
    ],
    "caveats": [
        bi("Brückners gedruckte Summenzeilen stimmen nicht durchgehend mit den Einzelwerten überein: Die Nadelwald-Summe der Kammergüter im Landestheil Gera lautet 3409,31 Morgen, die Einzelwerte ergeben 1962,92; die Feld-Summe der Kammergüter in Schleiz ist mit 2400,00 gedruckt, die Einzelwerte ergeben 2379,98; bei den Rittergütern in Gera steht für Hutung und Weg 809,99 gedruckt, die Einzelwerte ergeben 899,98 (die Hauptsumme 1132,93 passt zu 899,99). Kleinere Abweichungen (bis etwa 2 Morgen, beim Steuerwerth bis etwa 160 Einheiten) kommen hinzu. Die Auswertung rechnet daher mit den Einzelwerten.",
           "Brückner's printed total rows do not consistently agree with the individual values: the coniferous-wood total of the chamber estates in the district of Gera is 3,409.31 Morgen, the individual values give 1,962.92; the arable total of the chamber estates in Schleiz is printed as 2,400.00, the individual values give 2,379.98; for the manorial estates in Gera 809.99 is printed for pasture and tracks, the individual values give 899.98 (the grand total 1,132.93 fits 899.99). Smaller deviations (up to about 2 Morgen, for the tax value up to about 160 units) are added. The analysis therefore works with the individual values."),
        bi("Die Spalte »Steuerwerth« trägt in der Vorlage die Überschrift »Thaler«; nach Brückners Berichtigung (S. 831) ist sie in Steuereinheiten zu 10 Thlr. zu lesen. Die Werte sind hier unverändert als Steuereinheiten übernommen.",
           "In the source the column “Steuerwerth” is headed “Thaler”; according to Brückner's correction (p. 831) it is to be read in tax units of 10 Thlr. The values are taken over unchanged as tax units."),
        bi("Die Tabellen führen Güter, nicht Besitzungen: Köstritz erscheint in zwei Teilen, Frössen und Mödlareuth in je zwei Einträgen, Hartmannsdorf und Dürrenberg getrennt; die Rittergut-Tabelle enthält 40 Einträge, während Brückner im Text von 41 Rittergütern im Jahr 1867 spricht (S. 230). Die Spalte »Hut und Weg« enthält bei den Rittergütern auch die Wege.",
           "The tables list estates, not holdings: Köstritz appears in two parts, Frössen and Mödlareuth in two entries each, Hartmannsdorf and Dürrenberg separately; the manorial-estate table has 40 entries whereas Brückner speaks of 41 manorial estates in 1867 in the text (p. 230). For the manorial estates the column “Hut und Weg” also includes tracks."),
    ],
    "conversions": [
        {"from": "preußischer Morgen", "to": "Hektar", "factor_or_formula": "ha = Morgen × 0,255322", "reference": "Brückner S. 832: 1 preuß. Morgen (180 Quadratruthen) = 0,255322 Hectaren"},
        {"from": "Steuerwerth (gedruckt »Thaler«)", "to": "Steuereinheiten", "factor_or_formula": "1 Steuereinheit = 10 Thlr.; Zahlen unverändert", "reference": "Brückner S. 831 (Berichtigung zu S. 219, 221, 223)"},
    ],
    "datasets": [
        {"name": "gueter", "title": bi("Kammergüter und Rittergüter", "Chamber estates and manorial estates"),
         "columns": [
             col("art_de", "Art des Guts", "Kind of estate", "string"),
             col("art_en", "Art des Guts (englisch)", "Kind of estate (English)", "string"),
             col("landestheil_de", "Landestheil", "District", "string"),
             col("landestheil_en", "Landestheil (englisch)", "District (English)", "string"),
             col("name", "Gut", "Estate", "string"),
             col("hof", "Hofraum", "Farmstead", "number", "preuß. Morgen"),
             col("garten", "Gärten", "Gardens", "number", "preuß. Morgen"),
             col("feld", "Feld", "Arable land", "number", "preuß. Morgen"),
             col("wiese", "Wiese", "Meadow", "number", "preuß. Morgen"),
             col("nadel", "Nadelwald", "Coniferous wood", "number", "preuß. Morgen"),
             col("laub", "Laubwald", "Deciduous wood", "number", "preuß. Morgen"),
             col("hut", "Hut (Rittergüter: Hut, Weg)", "Pasture (manorial estates: pasture, tracks)", "number", "preuß. Morgen"),
             col("wasser", "Wasser", "Water", "number", "preuß. Morgen"),
             col("steuer", "Steuerwerth", "Tax value", "number", "Steuereinheiten (10 Thlr.)", note="gedruckt »Thaler«, nach der Berichtigung S. 831 Steuereinheiten zu 10 Thlr."),
             col("gesamt_morgen", "Fläche insgesamt", "Total area", "number", "preuß. Morgen", derived=True, note="Summe der Flächenspalten"),
             col("gesamt_ha", "Fläche insgesamt in Hektar", "Total area in hectares", "number", "ha", derived=True, note="Morgen × 0,255322"),
             col("besitzer", "Besitzer 1867 (Rittergüter)", "Owner (manorial estates)", "string"),
             col("gewinnzeit", "Gewinnzeit (Kammergüter)", "Date of acquisition (chamber estates)", "string"),
         ],
         "rows": rows, "source_refs": R_REFS},
        {"name": "zusammensetzung", "title": bi("Flächen der Güter nach Besitzart, Landestheil und Nutzung", "Estate land by type of owner, district and use"),
         "columns": [
             col("art_de", "Besitzart", "Type of owner", "string", derived=True),
             col("art_en", "Besitzart (englisch)", "Type of owner (English)", "string", derived=True),
             col("art_nr", "Reihenfolge Besitzart", "Order of owner type", "integer", derived=True),
             col("landestheil_de", "Landestheil", "District", "string", derived=True),
             col("landestheil_en", "Landestheil (englisch)", "District (English)", "string", derived=True),
             col("lt_nr", "Reihenfolge Landestheil", "District order", "integer", derived=True),
             col("region_de", "Gruppe", "Group", "string", derived=True),
             col("region_en", "Gruppe (englisch)", "Group (English)", "string", derived=True),
             col("region_nr", "Reihenfolge Gruppe", "Group order", "integer", derived=True),
             col("nutzung_de", "Nutzung", "Use", "string", derived=True),
             col("nutzung_en", "Nutzung (englisch)", "Use (English)", "string", derived=True),
             col("nutzung_nr", "Reihenfolge Nutzung", "Use order", "integer", derived=True),
             col("morgen", "Fläche", "Area", "number", "preuß. Morgen", derived=True, note="Summe der Einzelgüter"),
             col("ha", "Fläche in Hektar", "Area in hectares", "number", "ha", derived=True),
             col("pct", "Anteil an der Gesamtfläche der Gruppe", "Share of the group's total area", "number", "%", derived=True),
             col("n_gueter", "Zahl der Einträge", "Number of entries", "integer", derived=True),
         ],
         "rows": summ, "source_refs": R_REFS},
        {"name": "groesste", "title": bi("Die 15 größten Güter", "The 15 largest estates"),
         "columns": [
             col("rang", "Rang nach Fläche", "Rank by area", "integer", derived=True),
             col("gut_de", "Gut", "Estate", "string", derived=True),
             col("gut_en", "Gut (englisch)", "Estate (English)", "string", derived=True),
             col("art_de", "Art des Guts", "Kind of estate", "string", derived=True),
             col("landestheil_de", "Landestheil", "District", "string", derived=True),
             col("nutzung_de", "Nutzung", "Use", "string", derived=True),
             col("nutzung_en", "Nutzung (englisch)", "Use (English)", "string", derived=True),
             col("nutzung_nr", "Reihenfolge Nutzung", "Use order", "integer", derived=True),
             col("morgen", "Fläche", "Area", "number", "preuß. Morgen", derived=True),
             col("ha", "Fläche in Hektar", "Area in hectares", "number", "ha", derived=True),
             col("gesamt_morgen", "Fläche des Guts", "Area of the estate", "number", "preuß. Morgen", derived=True),
             col("gesamt_ha", "Fläche des Guts in Hektar", "Area of the estate in hectares", "number", "ha", derived=True),
         ],
         "rows": top, "source_refs": R_REFS},
    ],
    "charts": [
        {"id": "c1", "dataset": "zusammensetzung",
         "title": bi("Zusammensetzung der Gutsflächen", "Composition of the estate land"),
         "caption": bi("Anteile der Nutzungen an der Gesamtfläche der Kammergüter und Rittergüter je Landestheil (aus den Einzelwerten berechnet). Die Rittergüter im Unterland (Gera) bestehen vor allem aus Feld, die im Oberland (Schleiz, Lobenstein-Ebersdorf) zu großen Teilen aus Nadelwald; bei den Kammergütern ist die Wiese im Oberland stärker vertreten.",
                       "Shares of the uses in the total area of the chamber and manorial estates per district (computed from the individual values). The manorial estates of the Lower Land (Gera) consist mainly of arable land, those of the Upper Land (Schleiz, Lobenstein-Ebersdorf) largely of coniferous wood; among the chamber estates meadow is more prominent in the Upper Land."),
         "vegalite": {
             "height": 320,
             "mark": "bar",
             "encoding": {
                 "y": {"field": {"de": "region_de", "en": "region_en"}, "type": "nominal", "sort": {"field": "region_nr", "op": "min"}, "title": None, "axis": {"labelLimit": 300}},
                 "x": {"field": "pct", "type": "quantitative", "scale": {"domain": [0, 100]}, "title": bi("% der Gutsfläche", "% of the estate area")},
                 "color": {"field": {"de": "nutzung_de", "en": "nutzung_en"}, "type": "nominal", "title": None, "scale": {"domain": CATLIST}, "legend": {"columns": 2, "labelLimit": 220}},
                 "order": {"field": "nutzung_nr", "type": "quantitative"},
                 "tooltip": [{"field": {"de": "region_de", "en": "region_en"}, "title": bi("Gruppe", "Group")},
                             {"field": {"de": "nutzung_de", "en": "nutzung_en"}, "title": bi("Nutzung", "Use")},
                             {"field": "morgen", "title": bi("Morgen", "Morgen"), "format": ",.0f"},
                             {"field": "ha", "title": "ha", "format": ",.0f"},
                             {"field": "pct", "title": bi("% der Gutsfläche", "% of the estate area"), "format": ".1f"},
                             {"field": "n_gueter", "title": bi("Zahl der Einträge", "Number of entries")}]}}},
        {"id": "c2", "dataset": "zusammensetzung",
         "title": bi("Gesamtfläche der Güter nach Landestheil (Hektar)", "Total area of the estates by district (hectares)"),
         "caption": bi("Fläche aller Kammergüter und Rittergüter je Landestheil, umgerechnet in Hektar. Im Landestheil Gera liegt der größte Teil der Rittergüter, bei den Kammergütern ist Lobenstein-Ebersdorf am größten.",
                       "Area of all chamber and manorial estates per district, converted to hectares. The district of Gera holds the largest part of the manorial estates, while for the chamber estates Lobenstein-Ebersdorf is largest."),
         "vegalite": {
             "height": 280,
             "transform": [{"filter": "datum.lt_nr < 4"},
                           {"aggregate": [{"op": "sum", "field": "ha", "as": "ha_sum"}, {"op": "sum", "field": "morgen", "as": "morgen_sum"}, {"op": "max", "field": "n_gueter", "as": "n"}],
                            "groupby": ["art_de", "art_en", "art_nr", "landestheil_de", "landestheil_en", "lt_nr"]}],
             "mark": "bar",
             "encoding": {
                 "x": {"field": {"de": "landestheil_de", "en": "landestheil_en"}, "type": "nominal", "sort": {"field": "lt_nr", "op": "min"}, "title": None, "axis": {"labelAngle": 0}},
                 "xOffset": {"field": {"de": "art_de", "en": "art_en"}, "type": "nominal", "sort": [bi("Kammergüter", "Chamber estates"), bi("Rittergüter", "Manorial estates")]},
                 "y": {"field": "ha_sum", "type": "quantitative", "title": "ha", "axis": {"format": ",.0f"}},
                 "color": {"field": {"de": "art_de", "en": "art_en"}, "type": "nominal", "title": None, "scale": {"domain": [bi("Kammergüter", "Chamber estates"), bi("Rittergüter", "Manorial estates")]}},
                 "tooltip": [{"field": {"de": "landestheil_de", "en": "landestheil_en"}, "title": bi("Landestheil", "District")},
                             {"field": {"de": "art_de", "en": "art_en"}, "title": bi("Besitzart", "Type of owner")},
                             {"field": "n", "title": bi("Zahl der Einträge", "Number of entries")},
                             {"field": "morgen_sum", "title": bi("Morgen", "Morgen"), "format": ",.0f"},
                             {"field": "ha_sum", "title": "ha", "format": ",.0f"}]}}},
        {"id": "c3", "dataset": "groesste",
         "title": bi("Die 15 größten Güter", "The 15 largest estates"),
         "caption": bi("Gesamtfläche in Hektar, nach Nutzungen gegliedert. Unter den größten Gütern sind Kammergüter mit viel Nadelwald (Oschitz, Harra, Niederndorf) und Rittergüter des Unterlandes (Steinbrücken, Caaschwitz).",
                       "Total area in hectares, divided by use. Among the largest estates are chamber estates with much coniferous wood (Oschitz, Harra, Niederndorf) and manorial estates of the Lower Land (Steinbrücken, Caaschwitz)."),
         "vegalite": {
             "height": 420,
             "mark": "bar",
             "encoding": {
                 "y": {"field": {"de": "gut_de", "en": "gut_en"}, "type": "nominal", "sort": {"field": "rang", "op": "min"}, "title": None, "axis": {"labelLimit": 400}},
                 "x": {"field": "ha", "type": "quantitative", "title": "ha", "axis": {"format": ",.0f"}},
                 "color": {"field": {"de": "nutzung_de", "en": "nutzung_en"}, "type": "nominal", "title": None, "scale": {"domain": CATLIST}, "legend": {"columns": 2, "labelLimit": 220}},
                 "order": {"field": "nutzung_nr", "type": "quantitative"},
                 "tooltip": [{"field": {"de": "gut_de", "en": "gut_en"}, "title": bi("Gut", "Estate")},
                             {"field": {"de": "nutzung_de", "en": "nutzung_en"}, "title": bi("Nutzung", "Use")},
                             {"field": "morgen", "title": bi("Morgen", "Morgen"), "format": ",.1f"},
                             {"field": "ha", "title": "ha", "format": ",.1f"},
                             {"field": "gesamt_morgen", "title": bi("Gut insgesamt, Morgen", "Estate in total, Morgen"), "format": ",.0f"}]}}},
    ],
    "transcription_issues": ISS,
    "keywords": {
        "de": ["Kammergüter", "Rittergüter", "Güter", "Gutsflächen", "Steuerwerth", "Gewinnzeit", "Besitzer", "Domänen", "Landwirtschaft", "Wald", "Landestheil"],
        "en": ["chamber estates", "manorial estates", "estates", "land use", "tax value", "owners", "domains", "agriculture", "woodland"],
    },
    "related": ["landwirtschaft-grundbesitz-1854", "landwirtschaft-bodennutzung-1854", "landwirtschaft-agrarreformen-1836-1868"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(ana)
