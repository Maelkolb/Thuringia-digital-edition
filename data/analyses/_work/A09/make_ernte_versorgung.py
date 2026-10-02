"""A09 / analysis 6: Anbau, Ertrag und Versorgung (pp. 225-227)."""
import sys, re
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent))
from a09common import *


def nn(s):
    """number or mixed fraction, footnote markers stripped; dash -> None"""
    return num(s)


# ---------------------------------------------------------------- p. 226 b3 / b4: acreage, sacks, rye value
g3 = grid("226", "b3")
g4 = grid("226", "b4")
CROPS = [("Weizen", "Wheat", 1), ("Korn", "Rye (Korn)", 2), ("Gerste", "Barley", 3), ("Hafer", "Oats", 4), ("Kartoffeln", "Potatoes", 5),
         ("Hülsenfrüchte", "Pulses", 6), ("Hackfrüchte", "Root crops", 7)]
LT = [("Gera", "Gera", 1), ("Schleiz", "Schleiz", 2), ("Lobenstein-Ebersdorf", "Lobenstein-Ebersdorf", 3), ("Fürstenthum", "Principality", 4)]
anbau = []
for ci, (cde, cen, cn) in enumerate(CROPS):
    r3 = g3[2 + ci]
    r4 = g4[1 + ci]
    assert r3[0] == cde and r4[0] == cde, (r3[0], r4[0], cde)
    cells = {
        "Gera": r3[1:4], "Schleiz": r3[4:7], "Lobenstein-Ebersdorf": r4[1:4], "Fürstenthum": r4[4:7],
    }
    for lt, lten, ln in LT:
        m, s_, rw = cells[lt]
        m = re.sub(r"\s*\*+\)", "", m)
        mv, sv, rv = nn(m), nn(s_), nn(rw)
        anbau.append([lt, lten, ln, cde, cen, cn, m, mv, round(mv * MORGEN_HA, 0), s_, sv, rv, round(sv / mv, 1)])
# totals check
tot = {}
for lt, _, _ in LT:
    tot[lt] = sum(r[7] for r in anbau if r[0] == lt)
print({k: round(v, 2) for k, v in tot.items()})
printed_tot = {"Gera": nn(g3[9][1]), "Schleiz": nn(g3[9][4]), "Lobenstein-Ebersdorf": nn(g4[8][1]), "Fürstenthum": nn(g4[8][4])}
print(printed_tot)
for lt in tot:
    assert abs(tot[lt] - printed_tot[lt]) < 0.01, lt

# ---------------------------------------------------------------- p. 227 b1: balance
g1 = grid("227", "b1")
bilanz = []
for k, (lt, lten, ln) in enumerate(LT):
    r = g1[1 + k]
    prod_t, cons_t, sur_t, per_qm_t = r[1], r[2], r[3], r[4]
    prod, cons, sur, per_qm = nn(prod_t), nn(cons_t), nn(sur_t), nn(per_qm_t)
    bilanz.append([lt if lt != "Fürstenthum" else "Land", lten if lten != "Principality" else "Country as a whole", ln, prod_t, prod, cons_t, cons, sur_t, sur, per_qm,
                   round(100 * sur / cons, 1)])
    assert abs(prod - cons - sur) < 0.02, (lt, prod, cons, sur)
print(bilanz)

# ---------------------------------------------------------------- p. 227 b5: day labourers and farm servants
g5 = grid("227", "b5")
arb = []
for k, (lt, lten, ln) in enumerate(LT):
    r = g5[1 + k]
    tag, dien = nn(r[1]), nn(r[2])
    e_tag = nn(r[3].replace("Einw.", "").replace('"', "").strip())
    e_dien = nn(r[4].replace("Einw.", "").replace('"', "").strip())
    arb.append([lt if lt != "Fürstenthum" else "Land", lten if lten != "Principality" else "Country as a whole", ln, tag, dien, e_tag, e_dien, round(1000 / e_tag, 1), round(1000 / e_dien, 1)])
print(arb)

# ---------------------------------------------------------------- numbers for the text
def share_crop(lt, crop):
    t = sum(r[7] for r in anbau if r[0] == lt)
    return 100 * [r[7] for r in anbau if r[0] == lt and r[3] == crop][0] / t


sh = {(lt, c[0]): share_crop(lt, c[0]) for lt, _, _ in LT for c in CROPS}
yld = {(r[0], r[3]): r[12] for r in anbau}
print({k: round(v, 1) for k, v in sh.items()})
print(yld)
b = {r[0]: r for r in bilanz}
a = {r[0]: r for r in arb}
ha_ackerland = {lt: tot[lt] * MORGEN_HA for lt in tot}
# Hafer / Kartoffeln / Weizen shares
w_G, w_S, w_L = sh[("Gera", "Weizen")], sh[("Schleiz", "Weizen")], sh[("Lobenstein-Ebersdorf", "Weizen")]
h_G, h_S, h_L = sh[("Gera", "Hafer")], sh[("Schleiz", "Hafer")], sh[("Lobenstein-Ebersdorf", "Hafer")]
k_G, k_S, k_L = sh[("Gera", "Kartoffeln")], sh[("Schleiz", "Kartoffeln")], sh[("Lobenstein-Ebersdorf", "Kartoffeln")]
sum_roggenwert_G = sum(r[11] or 0 for r in anbau if r[0] == "Gera")
print("Gera Roggenwerth sum", sum_roggenwert_G, "vs production", b["Gera"][4])

R_A1 = {"page": "226", "block": "b3", "rows": "r3-t10"}
R_A2 = {"page": "226", "block": "b4", "rows": "r2-t9"}
R_B = {"page": "227", "block": "b1", "rows": "r2-r5"}
R_T = {"page": "227", "block": "b5", "rows": "r2-r5"}
R_TXT = [{"page": "226", "block": "b1", "rows": "r3-g5"}, {"page": "226", "block": "b2"}, {"page": "226", "block": "b5"}, {"page": "227", "block": "b2"}, {"page": "227", "block": "b3"}]


def col(name, de, en, typ, unit=None, derived=False, note=None):
    d = {"name": name, "label": bi(de, en), "type": typ, "unit": unit}
    if derived:
        d["derived"] = True
    if note:
        d["note"] = note
    return d


FR = "gedruckt als gemischter Bruch (z. B. 5666 2/3), hier als Dezimalzahl"
ana = {
    "id": "landwirtschaft-ernte-versorgung",
    "title": bi("Anbau, Ertrag und Selbstversorgung: Produktion und Verbrauch des Getreidelandes", "Cultivation, yield and self-sufficiency: production and consumption of the arable land"),
    "category": "agriculture",
    "section": "t1-3-2",
    "sources": R_TXT + [R_A1, R_A2, R_B, R_T],
    "summary": bi(
        "Da dem Land »specielle Erndteresultate« fehlen, rechnet Brückner mit Schätzungen für mittlere Erntejahre: Verteilung der Fruchtarten auf die Ackerfläche, Ertrag je Morgen, Nährwert (in Roggenwert) und den Bedarf von Menschen und Vieh. Die Diagramme zeigen die angenommene Fruchtverteilung, die Erträge, die Bilanz von Produktion und Verbrauch in Centnern Roggenwert und die Zahl der Taglöhner und landwirthschaftlichen Dienstboten.",
        "Because the country lacks “special harvest results”, Brückner calculates with estimates for average harvest years: the distribution of crops over the arable area, yield per Morgen, nutritional value (in rye equivalent) and the requirements of people and livestock. The charts show the assumed crop distribution, the yields, the balance of production and consumption in hundredweights of rye equivalent, and the number of day labourers and farm servants."),
    "method": bi(
        "Die Zahlen stammen aus den beiden Tabellen zu Fruchtvertheilung und Ertrag (S. 226, Blöcke b3 und b4), der Bilanztabelle (S. 227, Block b1) und der Tabelle zu Taglöhnern und Dienstboten 1864 (S. 227, Block b5). Brückner übernimmt für Schleiz und Lobenstein-Ebersdorf die Ansätze des Landraths Fuchs (1861) und für Gera eigene Erfahrungswerte; die Ackerfläche entspricht der »Gegenwart« (S. 226, Fußnote **). Die Mengen sind in Morgen, Säcken (1 Sack = 2 preußische Scheffel) und Centnern Roggenwerth angegeben; Brückner setzt Roggen = 1 und rechnet Weizen und Hülsenfrüchte mit 1,29, Gerste mit 0,76, Hafer mit 0,47 und Kartoffeln mit 0,25. Gemischte Brüche der Vorlage (z. B. 5666 2/3) wurden als Dezimalzahlen übernommen (Spalten *_text enthalten den gedruckten Wortlaut). Der Ertrag je Morgen (Sack/Morgen) ist Säcke geteilt durch Morgen. Morgen wurden mit Brückners Faktor 0,255322 in Hektar umgerechnet (S. 832). Eine Umrechnung von Sack und Centner in metrische Einheiten ist nach Brückners Tabelle (S. 831–832) nicht möglich (nur ein Zollpfund = 0,5 kg ist angegeben) und unterbleibt.",
        "The figures come from the two tables on crop distribution and yield (p. 226, blocks b3 and b4), the balance table (p. 227, block b1) and the table on day labourers and servants in 1864 (p. 227, block b5). For Schleiz and Lobenstein-Ebersdorf Brückner adopts the assumptions of Landrath Fuchs (1861) and for Gera his own experience; the arable area corresponds to “the present” (p. 226, footnote **). Quantities are given in Morgen, sacks (1 sack = 2 Prussian bushels) and hundredweights of rye value (Roggenwerth); Brückner sets rye = 1 and counts wheat and pulses at 1.29, barley at 0.76, oats at 0.47 and potatoes at 0.25. Mixed fractions of the source (e.g. 5666 2/3) were converted to decimals (the *_text columns contain the printed wording). Yield per Morgen (sack/Morgen) is sacks divided by Morgen. Morgen were converted to hectares with Brückner's factor 0.255322 (p. 832). A conversion of sacks and hundredweights into metric units is not possible with Brückner's table (pp. 831–832; only a Zollpfund = 0.5 kg is given) and is omitted."),
    "findings": [
        bi(f"Die angenommene Fruchtverteilung unterscheidet Unter- und Oberland: Weizen nimmt in Gera {de_num(w_G)} % der Ackerfläche ein, in Schleiz und Lobenstein-Ebersdorf (dort mit gleichen Ansätzen) nur {de_num(w_S)} %; Hafer {de_num(h_G)} % gegenüber {de_num(h_S)} %; Kartoffeln {de_num(k_G)} % gegenüber {de_num(k_S)} %. Die Anteile von Schleiz und Lobenstein-Ebersdorf sind identisch, weil Brückner die Ansätze des Landraths Fuchs für beide übernimmt.",
           f"The assumed crop distribution differs between the Lower and the Upper Land: wheat takes up {en_num(w_G)} % of the arable area in Gera but only {en_num(w_S)} % in Schleiz and Lobenstein-Ebersdorf (which use the same assumptions); oats {en_num(h_G)} % against {en_num(h_S)} %; potatoes {en_num(k_G)} % against {en_num(k_S)} %. The shares for Schleiz and Lobenstein-Ebersdorf are identical because Brückner adopts Landrath Fuchs's assumptions for both."),
        bi(f"Der angenommene Ertrag liegt im Unterland höher: Weizen und Roggen {de_num(yld[('Gera','Weizen')],0)}, Gerste {de_num(yld[('Gera','Gerste')],0)} und Hafer {de_num(yld[('Gera','Hafer')],0)} Sack je Morgen gegenüber durchweg {de_num(yld[('Schleiz','Weizen')],0)} Sack im Oberland (nur bei den Hülsenfrüchten ist es umgekehrt: {de_num(yld[('Gera','Hülsenfrüchte')],0)} gegenüber {de_num(yld[('Schleiz','Hülsenfrüchte')],0)}); Kartoffeln {de_num(yld[('Gera','Kartoffeln')],0)} Sack und Hackfrüchte {de_num(yld[('Gera','Hackfrüchte')],0)} Sack je Morgen in beiden Gebieten.",
           f"The assumed yield is higher in the Lower Land: wheat and rye {en_num(yld[('Gera','Weizen')],0)}, barley {en_num(yld[('Gera','Gerste')],0)} and oats {en_num(yld[('Gera','Hafer')],0)} sacks per Morgen against {en_num(yld[('Schleiz','Weizen')],0)} sacks throughout in the Upper Land (only for pulses it is the other way round: {en_num(yld[('Gera','Hülsenfrüchte')],0)} against {en_num(yld[('Schleiz','Hülsenfrüchte')],0)}); potatoes {en_num(yld[('Gera','Kartoffeln')],0)} sacks and root crops {en_num(yld[('Gera','Hackfrüchte')],0)} sacks per Morgen in both areas."),
        bi(f"Nach Brückners Bilanz übersteigt die Produktion den Verbrauch im ganzen Land um {de_num(b['Land'][8],0)} Centner Roggenwert ({de_num(b['Land'][10])} % des Verbrauchs): Gera {de_num(b['Gera'][10])} %, Schleiz {de_num(b['Schleiz'][10])} %, Lobenstein-Ebersdorf nur {de_num(b['Lobenstein-Ebersdorf'][10])} %. Je Quadratmeile beträgt der Überschuss in Gera {de_num(b['Gera'][9],0)} Centner, in Schleiz {de_num(b['Schleiz'][9],0)} und in Lobenstein-Ebersdorf {de_num(b['Lobenstein-Ebersdorf'][9],0)}.",
           f"According to Brückner's balance, production exceeds consumption in the country as a whole by {en_num(b['Land'][8],0)} hundredweights of rye equivalent ({en_num(b['Land'][10])} % of consumption): Gera {en_num(b['Gera'][10])} %, Schleiz {en_num(b['Schleiz'][10])} %, Lobenstein-Ebersdorf only {en_num(b['Lobenstein-Ebersdorf'][10])} %. Per square mile the surplus is {en_num(b['Gera'][9],0)} hundredweights in Gera, {en_num(b['Schleiz'][9],0)} in Schleiz and {en_num(b['Lobenstein-Ebersdorf'][9],0)} in Lobenstein-Ebersdorf."),
        bi(f"1864 kommt in Gera ein Taglöhner auf {de_num(a['Gera'][5],2)} Einwohner ({de_num(a['Gera'][7])} je 1000), in Schleiz erst auf {de_num(a['Schleiz'][5],2)} ({de_num(a['Schleiz'][7])} je 1000) und in Lobenstein-Ebersdorf auf {de_num(a['Lobenstein-Ebersdorf'][5],2)} ({de_num(a['Lobenstein-Ebersdorf'][7])} je 1000); landwirthschaftliche Dienstboten sind im Landestheil Schleiz am häufigsten ({de_num(a['Schleiz'][8])} je 1000).",
           f"In 1864 there is one day labourer for every {en_num(a['Gera'][5],2)} inhabitants in Gera ({en_num(a['Gera'][7])} per 1,000), only one for every {en_num(a['Schleiz'][5],2)} in Schleiz ({en_num(a['Schleiz'][7])} per 1,000) and one for every {en_num(a['Lobenstein-Ebersdorf'][5],2)} in Lobenstein-Ebersdorf ({en_num(a['Lobenstein-Ebersdorf'][7])} per 1,000); farm servants are most frequent in the district of Schleiz ({en_num(a['Schleiz'][8])} per 1,000)."),
    ],
    "caveats": [
        bi(f"Die Bilanz ist eine Modellrechnung, keine Erntestatistik: Fruchtverteilung und Erträge sind Schätzungen für mittlere Jahre, der Verbrauch ist mit festen Sätzen angesetzt (je Kopf der Bevölkerung 4 Centner Roggenwert, je Pferd 20, je Rind 2,5, je Schwein 4,5, je Schaf oder Ziege 0,1 Centner).",
           "The balance is a model calculation, not harvest statistics: crop distribution and yields are estimates for average years, consumption is set with fixed rates (per head of population 4 hundredweights of rye value, per horse 20, per head of cattle 2.5, per pig 4.5, per sheep or goat 0.1 hundredweight)."),
        bi(f"Für Gera weicht die Produktion der Bilanz (275 485 Centner, S. 227) von der Summe der Roggenwerte der Fruchtarten (260 714, S. 226) um 14 771 Centner ab; bei Schleiz und Lobenstein-Ebersdorf stimmen beide Seiten überein. Beide Werte sind so gedruckt (am Faksimile geprüft); die Landessumme 599 531,78 enthält die höhere Zahl.",
           "For Gera the production in the balance (275,485 hundredweights, p. 227) differs by 14,771 hundredweights from the sum of the rye values of the crops (260,714, p. 226); for Schleiz and Lobenstein-Ebersdorf both sides agree. Both values are printed as given (checked against the facsimile); the national total of 599,531.78 contains the higher figure."),
        bi("Die Zahlen zu Taglöhnern und Dienstboten (S. 227) stammen aus der Zählung 1864; sie stimmen nicht mit den Summen der Berufsklassen auf S. 209–211 überein (dort für Lobenstein-Ebersdorf z. B. 2867 Personen in der Klasse »Handarbeiter u. Taglöhner«), so dass der Zählbegriff verschieden sein muss.",
           "The figures on day labourers and servants (p. 227) come from the 1864 count; they do not agree with the class totals on pp. 209–211 (e.g. 2,867 persons in the class “Handarbeiter u. Taglöhner” for Lobenstein-Ebersdorf), so the counting concept must differ."),
    ],
    "conversions": [
        {"from": "preußischer Morgen", "to": "Hektar", "factor_or_formula": "ha = Morgen × 0,255322", "reference": "Brückner S. 832: 1 preuß. Morgen (180 Quadratruthen) = 0,255322 Hectaren"},
        {"from": "Sack", "to": "preußischer Scheffel", "factor_or_formula": "1 Sack = 2 preuß. Scheffel", "reference": "Brückner S. 226 (Text)"},
        {"from": "Centner Roggenwerth", "to": "Centner Roggen", "factor_or_formula": "Roggen = 1; Weizen, Hülsenfrüchte 1,29; Gerste 0,76; Hafer 0,47; Kartoffeln 0,25", "reference": "Brückner S. 226 (Text)"},
    ],
    "datasets": [
        {"name": "anbau", "title": bi("Fruchtvertheilung und Ertrag nach Landestheilen", "Crop distribution and yield by district"),
         "columns": [
             col("landestheil_de", "Landestheil", "District", "string"),
             col("landestheil_en", "Landestheil (englisch)", "District (English)", "string"),
             col("lt_nr", "Reihenfolge Landestheil", "District order", "integer", derived=True),
             col("frucht_de", "Fruchtart", "Crop", "string"),
             col("frucht_en", "Fruchtart (englisch)", "Crop (English)", "string"),
             col("frucht_nr", "Reihenfolge Fruchtart", "Crop order", "integer", derived=True),
             col("morgen_text", "Fläche (gedruckt)", "Area (as printed)", "string"),
             col("morgen", "Fläche", "Area", "number", "preuß. Morgen", derived=True, note=FR),
             col("ha", "Fläche in Hektar", "Area in hectares", "number", "ha", derived=True, note="Morgen × 0,255322"),
             col("saecke_text", "Ertrag in Säcken (gedruckt)", "Yield in sacks (as printed)", "string"),
             col("saecke", "Ertrag in Säcken", "Yield in sacks", "number", "Säcke", derived=True, note=FR),
             col("roggenwerth", "Roggenwerth", "Rye value", "number", "Centner", derived=True, note=FR),
             col("sack_je_morgen", "Ertrag je Morgen", "Yield per Morgen", "number", "Säcke/Morgen", derived=True, note="Säcke geteilt durch Morgen"),
         ],
         "rows": anbau, "source_refs": [R_A1, R_A2]},
        {"name": "bilanz", "title": bi("Produktion und Verbrauch (Roggenwerth)", "Production and consumption (rye value)"),
         "columns": [
             col("landestheil_de", "Landestheil", "District", "string"),
             col("landestheil_en", "Landestheil (englisch)", "District (English)", "string"),
             col("lt_nr", "Reihenfolge", "Order", "integer", derived=True),
             col("produktion_text", "Produktion (gedruckt)", "Production (as printed)", "string"),
             col("produktion", "Produktion", "Production", "number", "Centner", derived=True, note=FR),
             col("verbrauch_text", "Verbrauch (gedruckt)", "Consumption (as printed)", "string"),
             col("verbrauch", "Verbrauch", "Consumption", "number", "Centner", derived=True, note=FR),
             col("ueberschuss_text", "Überschuss (gedruckt)", "Surplus (as printed)", "string"),
             col("ueberschuss", "Überschuss", "Surplus", "number", "Centner", derived=True, note=FR),
             col("ueberschuss_je_qm", "Überschuss auf 1 Quadratmeile", "Surplus per square mile", "number", "Centner/□Meile"),
             col("ueberschuss_pct", "Überschuss in % des Verbrauchs", "Surplus as % of consumption", "number", "%", derived=True),
         ],
         "rows": bilanz, "source_refs": [R_B]},
        {"name": "arbeitskraefte", "title": bi("Taglöhner und landwirthschaftliche Dienstboten 1864", "Day labourers and farm servants, 1864"),
         "columns": [
             col("landestheil_de", "Landestheil", "District", "string"),
             col("landestheil_en", "Landestheil (englisch)", "District (English)", "string"),
             col("lt_nr", "Reihenfolge", "Order", "integer", derived=True),
             col("taglohner", "Taglöhner", "Day labourers", "integer", "Personen"),
             col("dienstboten", "Landwirthschaftliche Dienstboten", "Farm servants", "integer", "Personen"),
             col("einw_je_taglohner", "Einwohner auf 1 Taglöhner", "Inhabitants per day labourer", "number", "Einwohner"),
             col("einw_je_dienstbote", "Einwohner auf 1 landw. Dienstboten", "Inhabitants per farm servant", "number", "Einwohner"),
             col("taglohner_je_1000", "Taglöhner je 1000 Einwohner", "Day labourers per 1,000 inhabitants", "number", "‰", derived=True, note="1000 / Einwohner auf 1 Taglöhner"),
             col("dienstboten_je_1000", "Dienstboten je 1000 Einwohner", "Farm servants per 1,000 inhabitants", "number", "‰", derived=True, note="1000 / Einwohner auf 1 Dienstboten"),
         ],
         "rows": arb, "source_refs": [R_T]},
    ],
    "charts": [
        {"id": "c1", "dataset": "anbau",
         "title": bi("Angenommene Fruchtverteilung auf der Ackerfläche", "Assumed crop distribution on the arable area"),
         "caption": bi("Anteil der Fruchtarten an der Ackerfläche des Landestheils (Brückners Rechnungsansatz; Ackerfläche der Gegenwart). Im Unterland spielen Weizen und Hafer eine größere Rolle, im Oberland Gerste, Kartoffeln und Roggen (Korn); für Schleiz und Lobenstein-Ebersdorf legt Brückner dieselben Anteile zugrunde (Ansätze des Landraths Fuchs).",
                       "Share of the crops in the arable area of the district (Brückner's calculation basis; present arable area). In the Lower Land wheat and oats play a larger role, in the Upper Land barley, potatoes and rye (Korn); for Schleiz and Lobenstein-Ebersdorf Brückner uses the same shares (assumptions of Landrath Fuchs)."),
         "vegalite": {
             "height": 260,
             "mark": "bar",
             "encoding": {
                 "y": {"field": {"de": "landestheil_de", "en": "landestheil_en"}, "type": "nominal", "sort": {"field": "lt_nr", "op": "min"}, "title": None, "axis": {"labelLimit": 220}},
                 "x": {"field": "morgen", "type": "quantitative", "stack": "normalize", "title": bi("Anteil an der Ackerfläche", "Share of the arable area"), "axis": {"format": "%"}},
                 "color": {"field": {"de": "frucht_de", "en": "frucht_en"}, "type": "nominal", "title": None,
                           "scale": {"domain": [bi(c[0], c[1]) for c in CROPS]}, "legend": {"columns": 3, "labelLimit": 140}},
                 "order": {"field": "frucht_nr", "type": "quantitative"},
                 "tooltip": [{"field": {"de": "landestheil_de", "en": "landestheil_en"}, "title": bi("Landestheil", "District")},
                             {"field": {"de": "frucht_de", "en": "frucht_en"}, "title": bi("Fruchtart", "Crop")},
                             {"field": "morgen_text", "title": bi("Morgen (gedruckt)", "Morgen (printed)")},
                             {"field": "ha", "title": "ha", "format": ",.0f"}]}}},
        {"id": "c2", "dataset": "anbau",
         "title": bi("Angenommener Ertrag je Morgen", "Assumed yield per Morgen"),
         "caption": bi("Ertrag nach Abzug des Saatkorns in Säcken (1 Sack = 2 preuß. Scheffel) je Morgen. Dargestellt sind Getreide und Hülsenfrüchte; Kartoffeln (40 Sack) und Hackfrüchte (78 Sack) sind in allen Landestheilen gleich angesetzt.",
                       "Yield after deduction of seed corn in sacks (1 sack = 2 Prussian bushels) per Morgen. Grains and pulses are shown; potatoes (40 sacks) and root crops (78 sacks) are set equal in all districts."),
         "vegalite": {
             "height": 280,
             "transform": [{"filter": "datum.frucht_nr <= 4 || datum.frucht_nr == 6"}, {"filter": "datum.lt_nr <= 3"}],
             "mark": "bar",
             "encoding": {
                 "x": {"field": {"de": "frucht_de", "en": "frucht_en"}, "type": "nominal", "sort": {"field": "frucht_nr", "op": "min"}, "title": None, "axis": {"labelAngle": 0}},
                 "xOffset": {"field": "landestheil_de", "type": "nominal", "sort": ["Gera", "Schleiz", "Lobenstein-Ebersdorf"]},
                 "y": {"field": "sack_je_morgen", "type": "quantitative", "title": bi("Säcke je Morgen", "Sacks per Morgen")},
                 "color": {"field": "landestheil_de", "type": "nominal", "title": None, "scale": {"domain": ["Gera", "Schleiz", "Lobenstein-Ebersdorf"]}, "legend": {"labelLimit": 260}},
                 "tooltip": [{"field": "landestheil_de", "title": bi("Landestheil", "District")},
                             {"field": {"de": "frucht_de", "en": "frucht_en"}, "title": bi("Fruchtart", "Crop")},
                             {"field": "sack_je_morgen", "title": bi("Säcke je Morgen", "Sacks per Morgen"), "format": ".1f"}]}}},
        {"id": "c3", "dataset": "bilanz",
         "title": bi("Produktion und Verbrauch in Roggenwert", "Production and consumption in rye value"),
         "caption": bi("Jährliche Erzeugung und Verbrauch von Menschen und Vieh in Centnern Roggenwert, nach Brückners Modellrechnung. In allen Landestheilen übersteigt die Produktion den Verbrauch, in Lobenstein-Ebersdorf nur knapp.",
                       "Annual production and consumption by people and livestock in hundredweights of rye equivalent, according to Brückner's model calculation. In all districts production exceeds consumption, in Lobenstein-Ebersdorf only narrowly."),
         "vegalite": {
             "height": 280,
             "transform": [{"fold": ["produktion", "verbrauch"], "as": ["art", "ctr"]},
                           {"calculate": {"de": "datum.art == 'produktion' ? 'Produktion' : 'Verbrauch'", "en": "datum.art == 'produktion' ? 'Production' : 'Consumption'"}, "as": "art_label"}],
             "mark": "bar",
             "encoding": {
                 "x": {"field": {"de": "landestheil_de", "en": "landestheil_en"}, "type": "nominal", "sort": {"field": "lt_nr", "op": "min"}, "title": None, "axis": {"labelAngle": 0}},
                 "xOffset": {"field": "art_label", "type": "nominal", "sort": [bi("Produktion", "Production"), bi("Verbrauch", "Consumption")]},
                 "y": {"field": "ctr", "type": "quantitative", "title": bi("Centner Roggenwert", "Hundredweights of rye value"), "axis": {"format": ",.0f"}},
                 "color": {"field": "art_label", "type": "nominal", "title": None, "scale": {"domain": [bi("Produktion", "Production"), bi("Verbrauch", "Consumption")]}},
                 "tooltip": [{"field": {"de": "landestheil_de", "en": "landestheil_en"}, "title": bi("Landestheil", "District")},
                             {"field": "art_label", "title": bi("Größe", "Quantity")},
                             {"field": "ctr", "title": "Ctr.", "format": ",.0f"},
                             {"field": "ueberschuss", "title": bi("Überschuss (Ctr.)", "Surplus (Ctr.)"), "format": ",.0f"},
                             {"field": "ueberschuss_pct", "title": bi("Überschuss in % des Verbrauchs", "Surplus as % of consumption"), "format": ".1f"}]}}},
        {"id": "c4", "dataset": "arbeitskraefte",
         "title": bi("Taglöhner und landwirthschaftliche Dienstboten", "Day labourers and farm servants"),
         "caption": bi("Personen je 1000 Einwohner, 1864. Taglöhner sind in Gera, dem Gebiet mit der stärksten Industrie, am häufigsten.",
                       "Persons per 1,000 inhabitants, 1864. Day labourers are most frequent in Gera, the district with the strongest industry."),
         "vegalite": {
             "height": 280,
             "transform": [{"fold": ["taglohner_je_1000", "dienstboten_je_1000"], "as": ["gruppe", "je1000"]},
                           {"calculate": {"de": "datum.gruppe == 'taglohner_je_1000' ? 'Taglöhner' : 'Landw. Dienstboten'", "en": "datum.gruppe == 'taglohner_je_1000' ? 'Day labourers' : 'Farm servants'"}, "as": "gruppe_label"}],
             "mark": "bar",
             "encoding": {
                 "x": {"field": {"de": "landestheil_de", "en": "landestheil_en"}, "type": "nominal", "sort": {"field": "lt_nr", "op": "min"}, "title": None, "axis": {"labelAngle": 0}},
                 "xOffset": {"field": "gruppe_label", "type": "nominal", "sort": [bi("Taglöhner", "Day labourers"), bi("Landw. Dienstboten", "Farm servants")]},
                 "y": {"field": "je1000", "type": "quantitative", "title": bi("Personen je 1000 Einwohner", "Persons per 1,000 inhabitants")},
                 "color": {"field": "gruppe_label", "type": "nominal", "title": None, "scale": {"domain": [bi("Taglöhner", "Day labourers"), bi("Landw. Dienstboten", "Farm servants")]}},
                 "tooltip": [{"field": {"de": "landestheil_de", "en": "landestheil_en"}, "title": bi("Landestheil", "District")},
                             {"field": "gruppe_label", "title": bi("Gruppe", "Group")},
                             {"field": "je1000", "title": bi("je 1000 Einwohner", "per 1,000 inhabitants"), "format": ".1f"},
                             {"field": "taglohner", "title": bi("Taglöhner", "Day labourers")},
                             {"field": "dienstboten", "title": bi("Dienstboten", "Servants")}]}}},
    ],
    "keywords": {
        "de": ["Ernte", "Ertrag", "Fruchtarten", "Weizen", "Roggen", "Gerste", "Hafer", "Kartoffeln", "Roggenwert", "Verbrauch", "Selbstversorgung", "Taglöhner", "Dienstboten", "Landwirtschaft"],
        "en": ["harvest", "yield", "crops", "wheat", "rye", "barley", "oats", "potatoes", "rye value", "consumption", "self-sufficiency", "day labourers", "servants", "agriculture"],
    },
    "related": ["landwirtschaft-bodennutzung-1854", "viehzucht-bestand-1843-1867"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(ana)
