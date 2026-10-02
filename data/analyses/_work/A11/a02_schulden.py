"""A11-02: Staatsschuld 1857-1866 und Staatskassenscheine je Kopf im Staatenvergleich (pp. 277-278)."""
import re
from common import *

# ---- interest-bearing debt (p. 277 b6) ----------------------------------------------
g = grid("277", "b6")
debt_rows = []
for r in g:
    year = int(r[0].rstrip(":"))
    thlr = num(r[1])
    sgr = num(r[3]) if num(r[3]) is not None else None
    pf = num(r[5]) if num(r[5]) is not None else None
    dec_val = thlr + (sgr or 0) / 30 + (pf or 0) / 360
    debt_rows.append([year, thlr, sgr, pf, round(dec_val, 2)])
print(debt_rows)

# ---- Kassenscheine per head (p. 278 b1) -----------------------------------------------
g2 = grid("278", "b1")
nums = []
for r in g2:
    nums += re.findall(r"\d,\d{2}", " ".join(r))
assert nums == ["6,08", "2,96", "4,43", "2,88", "3,63", "2,88", "3,60", "2,66", "3,30", "2,12"], nums
names = [  # order of reading: left, right per row
    ("Waldeck", "Waldeck"), ("Reuß ä. L.", "Reuss (elder line)"),
    ("Anhalt", "Anhalt"), ("Königreich Sachsen", "Kingdom of Saxony"),
    ("Reuß j. L.", "Reuss (younger line)"), ("S.-Altenburg", "Saxe-Altenburg"),
    ("S.-Coburg-Gotha", "Saxe-Coburg-Gotha"), ("Schwarzburg-Rudolstadt", "Schwarzburg-Rudolstadt"),
    ("S.-Meiningen", "Saxe-Meiningen"), ("S.-Weimar", "Saxe-Weimar"),
]
ks_rows = []
for (nde, nen), v in zip(names, nums):
    ks_rows.append([nde, nen, "Reuß j. L." if "j. L." in nde else "Andere Staaten", "Reuss (younger line)" if "j. L." in nde else "Other states", num(v)])
rank = sorted([r[4] for r in ks_rows], reverse=True).index(3.63) + 1
others = [r[4] for r in ks_rows if r[0] != "Reuß j. L."]
mean_others = sum(others) / len(others)

# ---- derived measures -----------------------------------------------------------------
d57 = debt_rows[0][4]
d61 = debt_rows[4][4]
d66 = debt_rows[5][4]
chg_57_61 = d61 - d57
chg_61_66 = d66 - d61
INT = 0.04 * d66
REV = 296000
KS = 320000
tot_debt = d66 + KS
print(d57, d61, d66, chg_57_61, chg_61_66, INT, tot_debt, rank, mean_others)


def D(x, nd=0):
    return fmt_de(x, nd)


def E(x, nd=0):
    return fmt_en(x, nd)


ana = {
    "id": "staat-schulden-kassenscheine-1857-1866",
    "title": bi("Staatsschuld 1857–1866 und Kassenscheine im Vergleich", "State debt 1857–1866 and treasury notes compared"),
    "category": "finance",
    "section": "t1-4-3",
    "sources": [
        {"page": "277", "block": "b6"}, {"page": "277", "block": "b7"}, {"page": "277", "block": "b8"},
        {"page": "277", "block": "b9"}, {"page": "278", "block": "b1"}, {"page": "276", "block": "b3"},
    ],
    "summary": bi(
        f"Brückner nennt die verzinsliche Staatsschuld für 1857–1861 und 1866 (von {D(d57)} auf {D(d66)} Thaler) und erwähnt zusätzlich 320.000 Thaler unverzinsliche Kassenscheine, die er mit neun anderen deutschen Staaten je Kopf vergleicht. Die Auswertung zeigt den Schuldenabbau und die Stellung des Fürstentums im Vergleich.",
        f"Brückner gives the interest-bearing state debt for 1857–1861 and 1866 (falling from {E(d57)} to {E(d66)} Thaler) and mentions a further 320,000 Thaler of non-interest-bearing treasury notes, which he compares per head with nine other German states. The analysis shows the reduction of the debt and the principality's place in the comparison.",
    ),
    "method": bi(
        "Die sechs Jahreswerte stammen aus der Tabelle S. 277 (b6) in Thalern, Silbergroschen und Pfennigen; sie wurden mit 1 Thaler = 30 Sgr = 360 Pf in Dezimal-Thaler umgerechnet (abgeleitete Spalte). Für 1866 steht »—« bei Silbergroschen und Pfennigen (als 0 gelesen, hier leer gelassen). Die Kassenschein-Werte je Kopf stehen im Text S. 277–278 (10 Staaten). Zinslast (4 %) und Summen sind aus Brückners Angaben berechnet.",
        "The six annual values come from the table on p. 277 (b6) in Thaler, Silbergroschen and Pfennige; they were converted into decimal Thaler with 1 Thaler = 30 Sgr = 360 Pf (derived column). For 1866 the Silbergroschen and Pfennige are “—” (read as zero, left empty here). The per-head treasury-note values are in the text on pp. 277–278 (10 states). Interest burden (4 %) and sums are computed from Brückner's figures.",
    ),
    "findings": [
        bi(f"Die verzinsliche Staatsschuld sank von {D(d57)} Thalern (1857) auf {D(d61)} (1861), also um {D(-chg_57_61)} Thaler oder {D(100*-chg_57_61/d57,1)} %, und bis 1866 auf {D(d66)} Thaler; insgesamt ein Rückgang um {D(100*(d57-d66)/d57,1)} %.",
           f"The interest-bearing debt fell from {E(d57)} Thaler (1857) to {E(d61)} (1861), i.e. by {E(-chg_57_61)} Thaler or {E(100*-chg_57_61/d57,1)} %, and to {E(d66)} Thaler by 1866; altogether a decline of {E(100*(d57-d66)/d57,1)} %."),
        bi(f"Bei 4 % Verzinsung kostet die Schuld von 1866 rechnerisch {D(INT)} Thaler jährlich, das sind {D(100*INT/REV,1)} % der veranschlagten Jahreseinnahmen von {D(REV)} Thalern (S. 276).",
           f"At 4 % interest the 1866 debt costs about {E(INT)} Thaler a year, i.e. {E(100*INT/REV,1)} % of the estimated annual revenue of {E(REV)} Thaler (p. 276)."),
        bi(f"Rechnet man die 320.000 Thaler Kassenscheine hinzu, beträgt die Gesamtverschuldung rund {D(tot_debt)} Thaler, etwa das {D(tot_debt/REV,1)}fache der Jahreseinnahmen.",
           f"Adding the 320,000 Thaler of treasury notes gives a total indebtedness of about {E(tot_debt)} Thaler, roughly {E(tot_debt/REV,1)} times annual revenue."),
        bi(f"Mit 3,63 Thalern Staatskassenscheinen je Kopf steht Reuß j. L. an {rank}. Stelle von {len(ks_rows)} Staaten; der Durchschnitt der übrigen neun liegt bei {D(mean_others,2)} Thalern. Waldeck hat mit 6,08 den höchsten, S.-Weimar mit 2,12 den niedrigsten Wert.",
           f"With 3.63 Thaler of treasury notes per head Reuss j. L. ranks {rank}rd of {len(ks_rows)} states; the average of the other nine is {E(mean_others,2)} Thaler. Waldeck has the highest value (6.08), Saxe-Weimar the lowest (2.12)."),
    ],
    "caveats": [
        bi("Die Reihe hat eine Lücke: für 1862–1865 gibt Brückner keine Werte. Die gestrichelte Linie in Abb. 1 verbindet 1861 und 1866 daher nur zur Orientierung.",
           "The series has a gap: Brückner gives no values for 1862–1865. The dashed line in chart 1 therefore connects 1861 and 1866 only for orientation."),
        bi("Seit dem 27. Dezember 1857 besteht die Schuld nur noch aus unkündbaren, mit 4 % verzinsten Staatsschuldscheinen; alle drei Jahre werden 12.600 Thaler ausgelost. Die Rückgänge 1857–1861 sind größer, als diese Planung erwarten ließe; Brückner erklärt dies nicht.",
           "Since 27 December 1857 the debt consists only of irredeemable 4 % state bonds; 12,600 Thaler are drawn for repayment every three years. The declines in 1857–1861 are larger than this schedule suggests; Brückner does not explain this."),
        bi("Das Jahr des Staatenvergleichs der Kassenscheine ist nicht genannt; die Einwohnerbasis für Reuß j. L. (320.000 : 3,63 ≈ 88.200) entspricht der Größenordnung der Bevölkerung.",
           "The year of the treasury-note comparison is not stated; the population base implied for Reuss j. L. (320,000 : 3.63 ≈ 88,200) matches the order of magnitude of the population."),
    ],
    "conversions": [
        {"from": "Thaler, Silbergroschen, Pfennig", "to": "Dezimal-Thaler", "factor_or_formula": "Thlr + Sgr/30 + Pf/360", "reference": "1 Thaler = 30 Silbergroschen, 1 Silbergroschen = 12 Pfennige (Brückner S. 278)"},
    ],
    "datasets": [
        {"name": "debt", "title": bi("Verzinsliche Staatsschuld", "Interest-bearing state debt"),
         "columns": [
             col("year", "Jahr", "Year", "integer"),
             col("thlr", "Thaler", "Thaler", "integer", "Thlr."),
             col("sgr", "Silbergroschen", "Silbergroschen", "integer", "Sgr."),
             col("pf", "Pfennige", "Pfennige", "integer", "Pf."),
             col("debt_thaler", "Schuld in Dezimal-Thalern", "Debt in decimal Thaler", "number", "Thaler", derived=True),
         ],
         "rows": debt_rows, "source_refs": [{"page": "277", "block": "b6"}]},
        {"name": "notes", "title": bi("Staatskassenscheine je Kopf der Bevölkerung", "State treasury notes per head of population"),
         "columns": [
             col("state_de", "Staat", "State", "string"), col("state_en", "Staat (englisch)", "State (English)", "string"),
             col("grp_de", "Gruppe", "Group", "string"), col("grp_en", "Gruppe (englisch)", "Group (English)", "string"),
             col("thaler_per_head", "Kassenscheine je Kopf", "Treasury notes per head", "number", "Thaler"),
         ],
         "rows": ks_rows, "source_refs": [{"page": "278", "block": "b1"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "debt",
         "title": bi("Verzinsliche Staatsschuld 1857–1866", "Interest-bearing state debt, 1857–1866"),
         "caption": bi("Thaler; Beschriftung = gedruckte volle Thaler (ohne Silbergroschen und Pfennige). Für 1862–1865 liegen keine Angaben vor; die gestrichelte Linie verbindet 1861 und 1866 nur optisch.", "Thaler; labels = printed whole Thaler (without Silbergroschen and Pfennige). No figures are given for 1862–1865; the dashed line joins 1861 and 1866 for orientation only."),
         "vegalite": {
             "height": 260,
             "layer": [
                 {"transform": [{"filter": "datum.year <= 1861"}],
                  "mark": {"type": "line"},
                  "encoding": {
                      "x": {"field": "year", "type": "quantitative", "title": bi("Jahr", "Year"), "axis": {"format": "d", "values": [1857, 1858, 1859, 1860, 1861, 1862, 1863, 1864, 1865, 1866]}, "scale": {"domain": [1856.5, 1866.5]}},
                      "y": {"field": "debt_thaler", "type": "quantitative", "title": "Thaler", "scale": {"zero": True}, "axis": {"format": ",d"}}}},
                 {"transform": [{"filter": "datum.year >= 1861"}],
                  "mark": {"type": "line", "strokeDash": [4, 4]},
                  "encoding": {
                      "x": {"field": "year", "type": "quantitative"},
                      "y": {"field": "debt_thaler", "type": "quantitative"}}},
                 {"mark": {"type": "point", "filled": True},
                  "encoding": {
                      "x": {"field": "year", "type": "quantitative"},
                      "y": {"field": "debt_thaler", "type": "quantitative"},
                      "tooltip": [tt("year", "Jahr", "Year"), {"field": "thlr", "title": "Thlr.", "format": ","}, tt("sgr", "Sgr.", "Sgr."), tt("pf", "Pf.", "Pf."), {"field": "debt_thaler", "title": bi("Dezimal-Thaler", "Decimal Thaler"), "format": ",.2f"}]}},
                 {"mark": {"type": "text", "dy": -12, "fontSize": 11},
                  "encoding": {
                      "x": {"field": "year", "type": "quantitative"},
                      "y": {"field": "debt_thaler", "type": "quantitative"},
                      "text": {"field": "thlr", "type": "quantitative", "format": ",d"}}},
             ]}},
        {"id": "c2", "dataset": "notes",
         "title": bi("Staatskassenscheine je Kopf im Vergleich", "State treasury notes per head, compared"),
         "caption": bi("Thaler je Einwohner; Reuß j. L. hervorgehoben (Jahr der Angabe nicht genannt).", "Thaler per inhabitant; Reuss j. L. highlighted (year of the figures not stated)."),
         "vegalite": {
             "height": 300,
             "mark": "bar",
             "encoding": {
                 "y": {"field": F("state"), "type": "nominal", "sort": "-x", "title": None, "axis": {"labelLimit": 260}},
                 "x": {"field": "thaler_per_head", "type": "quantitative", "title": bi("Thaler je Kopf", "Thaler per head")},
                 "color": {"field": F("grp"), "type": "nominal", "title": None, "sort": {"field": "grp_de", "op": "min"}},
                 "tooltip": [ttf("state", "Staat", "State"), {"field": "thaler_per_head", "title": bi("Thaler je Kopf", "Thaler per head"), "format": ".2f"}]}}},
    ],
    "keywords": {"de": ["Staatsschuld", "Staatsschulden", "Kassenscheine", "Papiergeld", "Amortisation", "Staatsschuldscheine", "Gera", "Finanzen"],
                 "en": ["state debt", "public debt", "treasury notes", "paper money", "amortisation", "bonds", "finance"]},
}
write(ana)
