"""A11-01: Staatshaushalt 1866/68 - veranschlagte Einnahmen, Steuern, benannte Ausgaben (pp. 272, 275-277)."""
from common import *

# --- printed numbers, read from the canonical blocks ---------------------------------
g_ind = grid("277", "b1")          # indirect taxes
g_dir = grid("277", "b3")          # direct taxes
ind = [num(r[0].split()[0]) if i == 0 else num(r[0]) for i, r in enumerate(g_ind[:6])]
assert ind == [98000, 25000, 29000, 600, 950, 1100], ind
ind_total_printed = num(g_ind[6][0].split()[0])
assert ind_total_printed == 154650
direct = [num(g_dir[0][0].split()[0]), num(g_dir[1][0].split()[0])]
assert direct == [53600, 27560], direct
direct_total_printed = num(g_dir[2][0].split()[0])
assert direct_total_printed == 81100
INCOME_EST, EXPEND_EST = 296000, 290000          # p. 276 b3 (text)
MIL = 54750                                       # p. 272 b1 (text)
BUILD = [num(r[0]) for r in grid("275", "b2")[:3]]  # 1700, 182, 130
assert sum(BUILD) == 2012
CHAUSSEE_UNTERHALT = 26835                        # p. 275 b5 (text)
WEGE_ZUSCHUSS = 1200                              # p. 275 b5 (text)

assert sum(ind) == ind_total_printed
direct_sum = sum(direct)                          # 81,160 (printed total: 81,100)
other_income = INCOME_EST - sum(ind) - direct_sum
named_exp = MIL + CHAUSSEE_UNTERHALT + sum(BUILD) + WEGE_ZUSCHUSS
other_exp = EXPEND_EST - named_exp

items = [
    ("zoll", "Zölle u. a. (Sammelposten)", "Customs duties etc. (combined item)", "a_ind", "indirekt", "Indirect", ind[0]),
    ("malz", "Braumalzsteuer", "Brewing-malt tax", "a_ind", "indirekt", "Indirect", ind[1]),
    ("salz", "Salzregie (Salzertrag)", "Salt monopoly revenue", "a_ind", "indirekt", "Indirect", ind[2]),
    ("hund", "Hundesteuer", "Dog tax", "a_ind", "indirekt", "Indirect", ind[3]),
    ("karten", "Spielkartenstempel", "Playing-card stamp duty", "a_ind", "indirekt", "Indirect", ind[4]),
    ("jagd", "Jagdkarten", "Hunting licences", "a_ind", "indirekt", "Indirect", ind[5]),
    ("grund", "Grundsteuer", "Land tax", "b_dir", "direkt", "Direct", direct[0]),
    ("gewerbe", "Gewerbe- und Personalsteuer", "Trade and personal tax", "b_dir", "direkt", "Direct", direct[1]),
]
income_rows = [[k, de, en, gk, gde, gen, v] for k, de, en, gk, gde, gen, v in items]

struct_rows = [
    ["a_einnahmen", "Einnahmen", "Revenue", "a_ind", "Indirekte Steuern", "Indirect taxes", sum(ind)],
    ["a_einnahmen", "Einnahmen", "Revenue", "b_dir", "Direkte Steuern", "Direct taxes", direct_sum],
    ["a_einnahmen", "Einnahmen", "Revenue", "c_ue", "Übrige Einnahmen", "Other revenue", other_income],
    ["b_ausgaben", "Ausgaben", "Expenditure", "d_mil", "Militär", "Military", MIL],
    ["b_ausgaben", "Ausgaben", "Expenditure", "e_chs", "Chausseeunterhaltung", "Highway upkeep", CHAUSSEE_UNTERHALT],
    ["b_ausgaben", "Ausgaben", "Expenditure", "f_geb", "Gebäude und Wege", "Buildings and roads", sum(BUILD) + WEGE_ZUSCHUSS],
    ["b_ausgaben", "Ausgaben", "Expenditure", "g_ua", "Übrige Ausgaben", "Other expenditure", other_exp],
]
# order of stack components must be stable
comp_order = ["Indirect taxes", "Direct taxes", "Other revenue", "Military (incl. pensions)", "Highway maintenance", "State buildings and village-road subsidy", "Other expenditure (remainder)"]

tax_total = sum(ind) + direct_sum


def share(x, tot):
    return 100 * x / tot


f_tax = share(tax_total, INCOME_EST)
f_ind = share(sum(ind), INCOME_EST)
f_dir = share(direct_sum, INCOME_EST)
f_oth = share(other_income, INCOME_EST)
f_mil = share(MIL, EXPEND_EST)
f_zoll = share(ind[0], sum(ind))
f_salz = share(ind[2], sum(ind))
POP = 14239 * 6.18   # pupils x inhabitants per pupil (p. 299) -> ~88,000
per_head = tax_total / POP
print(other_income, other_exp, round(f_tax, 1), round(f_ind, 1), round(f_dir, 1), round(f_oth, 1), round(f_mil, 1), round(f_zoll, 1), round(per_head, 2), round(POP))


def D(x):
    return fmt_de(x)


def E(x):
    return fmt_en(x)


def dec(x, nd=1):
    return fmt_de(x, nd)


def dene(x, nd=1):
    return fmt_en(x, nd)


ana = {
    "id": "staat-haushalt-einnahmen-ausgaben-1866-1868",
    "title": bi("Staatshaushalt 1866/68: Einnahmen, Steuern und benannte Ausgaben", "State budget 1866/68: revenue, taxes and itemised expenditure"),
    "category": "finance",
    "section": "t1-4-3",
    "sources": [
        {"page": "276", "block": "b3"}, {"page": "277", "block": "b1", "rows": "h1-r7"}, {"page": "277", "block": "b3"},
        {"page": "272", "block": "b1"}, {"page": "275", "block": "b2"}, {"page": "275", "block": "b5"},
    ],
    "summary": bi(
        f"Brückner nennt für die Finanzperiode 1866/68 veranschlagte Staatseinnahmen von {D(INCOME_EST)} und Staatsausgaben von {D(EXPEND_EST)} Thalern jährlich und schlüsselt die Steuern auf: sechs indirekte Posten (zusammen {D(sum(ind))} Thaler) und zwei direkte Steuern ({D(direct_sum)} Thaler). Die Auswertung stellt diese Posten dem Gesamtvoranschlag gegenüber und ergänzt die wenigen einzeln genannten Ausgaben (Militär, Chausseen, Staatsgebäude).",
        f"For the 1866/68 financial period Brückner gives estimated state revenue of {E(INCOME_EST)} and expenditure of {E(EXPEND_EST)} Thaler a year and itemises the taxes: six indirect items (together {E(sum(ind))} Thaler) and two direct taxes ({E(direct_sum)} Thaler). The analysis sets these items against the overall estimate and adds the few expenditure items named separately (military, highways, state buildings).",
    ),
    "method": bi(
        f"Zahlen aus S. 276 (Gesamtvoranschlag, Fließtext), S. 277 (Tabelle der indirekten Steuern, Zeilen h1–r7; direkte Steuern als Kurztabelle) sowie S. 272 (Militärkosten {D(MIL)}) und S. 275 (Staatsgebäude 1700 + 182 + 130 = {D(sum(BUILD))}; Chausseeunterhaltung {D(CHAUSSEE_UNTERHALT)}; Wegezuschuss {D(WEGE_ZUSCHUSS)}). Die Restposten »übrige Einnahmen« ({D(other_income)}) und »übrige Ausgaben« ({D(other_exp)}) sind Differenzen zum Gesamtvoranschlag und daher abgeleitet. Die direkten Steuern wurden aus den beiden gedruckten Einzelposten summiert ({D(direct_sum)}; gedruckt ist 81,100, siehe Hinweise). Währung: 1 Thaler = 30 Silbergroschen = 360 Pfennige (S. 278). Alle Beträge in Thalern.",
        f"Figures from p. 276 (overall estimate, running text), p. 277 (table of indirect taxes, rows h1–r7; direct taxes as a short table), p. 272 (military cost {E(MIL)}) and p. 275 (state buildings 1700 + 182 + 130 = {E(sum(BUILD))}; highway maintenance {E(CHAUSSEE_UNTERHALT)}; road subsidy {E(WEGE_ZUSCHUSS)}). The remainders “other revenue” ({E(other_income)}) and “other expenditure” ({E(other_exp)}) are differences from the overall estimate and therefore derived. Direct taxes were summed from the two printed items ({E(direct_sum)}; the printed total is 81,100, see caveats). Currency: 1 Thaler = 30 Silbergroschen = 360 Pfennige (p. 278). All amounts in Thaler.",
    ),
    "findings": [
        bi(f"Die genannten Steuern machen {dec(f_tax)} % der veranschlagten Jahreseinnahmen aus: {dec(f_ind)} % indirekte, {dec(f_dir)} % direkte Steuern; {dec(f_oth)} % ({D(other_income)} Thaler) bleiben ohne Aufschlüsselung.",
           f"The named taxes make up {dene(f_tax)} % of the estimated annual revenue: {dene(f_ind)} % indirect and {dene(f_dir)} % direct taxes; {dene(f_oth)} % ({E(other_income)} Thaler) are not itemised."),
        bi(f"Die indirekten Steuern übertreffen die direkten fast um das Doppelte ({D(sum(ind))} gegenüber {D(direct_sum)} Thaler); allein der Sammelposten aus Zöllen, Malz-, Übergangs- und Rübenzuckersteuer trägt {dec(f_zoll)} % der indirekten Einnahmen, die Salzregie weitere {dec(f_salz)} %.",
           f"Indirect taxes outweigh direct taxes by almost two to one ({E(sum(ind))} against {E(direct_sum)} Thaler); the combined item of customs, malt, transit and beet-sugar duties alone supplies {dene(f_zoll)} % of indirect revenue, the salt monopoly another {dene(f_salz)} %."),
        bi(f"Von den Ausgaben nennt Brückner nur wenige Posten einzeln: die Militärkosten ({D(MIL)} Thaler) wären, als Jahresbetrag gelesen, {dec(f_mil)} % des Ausgabenvoranschlags; zusammen mit Chausseeunterhaltung, Staatsgebäuden und Wegezuschuss sind {dec(share(named_exp, EXPEND_EST))} % benannt.",
           f"Of expenditure Brückner itemises only a few heads: the military cost ({E(MIL)} Thaler), read as an annual amount, would be {dene(f_mil)} % of the expenditure estimate; with highway maintenance, state buildings and the road subsidy {dene(share(named_exp, EXPEND_EST))} % are named."),
        bi(f"Der Voranschlag sieht einen Überschuss von {D(INCOME_EST - EXPEND_EST)} Thalern jährlich vor ({dec(share(INCOME_EST - EXPEND_EST, INCOME_EST))} % der Einnahmen). Auf den Kopf der rund {D(round(POP, -3))} Einwohner entfallen rund {dec(per_head)} Thaler an Steuern.",
           f"The estimate provides for a surplus of {E(INCOME_EST - EXPEND_EST)} Thaler a year ({dene(share(INCOME_EST - EXPEND_EST, INCOME_EST))} % of revenue). Per head of the roughly {E(round(POP, -3))} inhabitants this is about {dene(per_head)} Thaler in taxes."),
    ],
    "caveats": [
        bi("Gedruckt ist als Summe der direkten Steuern 81,100 Thaler; die beiden Posten (53,600 + 27,560) ergeben 81,160. Die Differenz von 60 Thalern steht so im Original (Faksimile geprüft); hier wird mit der Summe der Einzelposten gerechnet.",
           "The printed total of the direct taxes is 81,100 Thaler; the two items (53,600 + 27,560) add up to 81,160. The 60-Thaler difference is in the original print (checked against the facsimile); the sum of the items is used here."),
        bi("Brückner schreibt, die direkten Steuern hätten sich »seither« auf diese Beträge belaufen, ohne Jahr. Ob sie dem Voranschlag 1866/68 entsprechen, ist offen; 1868 trat zudem eine Klassen- und Einkommensteuer nach preußischem Muster hinzu (S. 276).",
           "Brückner says the direct taxes amounted “hitherto” to these sums, without a year. Whether they equal the 1866/68 estimate is unclear; in 1868 a class and income tax on the Prussian model was also introduced (p. 276)."),
        bi("Die Militärkosten werden »auf die Finanzperiode 1866/68« mit 54,750 Thalern angegeben; hier als Jahresbetrag gelesen, wie die Gesamtsummen der Einnahmen und Ausgaben. Bezöge sich die Zahl auf alle drei Jahre, läge der Anteil bei einem Drittel. Die Anteile der Ausgabenposten sind deshalb eine Lesart, kein gesicherter Wert.",
           "The military cost is given “for the financial period 1866/68” as 54,750 Thaler; it is read here as an annual amount, like the overall revenue and expenditure totals. If it covered all three years, the share would be one third. The expenditure shares are therefore one reading, not a secure figure."),
        bi("Die Einwohnerzahl (rund 88.000) ist aus den Schülerzahlen (14.239 × 6,18 Einwohner je Schüler, S. 299) abgeleitet; sie dient nur der Größenordnung.",
           "The population (about 88,000) is derived from the pupil figures (14,239 × 6.18 inhabitants per pupil, p. 299) and serves only as an order of magnitude."),
    ],
    "conversions": [
        {"from": "Thaler", "to": "Silbergroschen / Pfennige", "factor_or_formula": "1 Thaler = 30 Silbergroschen = 360 Pfennige", "reference": "Brückner S. 278 (Dreißigthalerfuß seit 1857)"},
    ],
    "datasets": [
        {"name": "income", "title": bi("Veranschlagte Steuereinnahmen nach Posten", "Estimated tax revenue by item"),
         "columns": [
             col("item_key", "Kürzel", "Key", "string"),
             col("item_de", "Posten", "Item", "string"), col("item_en", "Posten (englisch)", "Item (English)", "string"),
             col("group_key", "Kürzel Gruppe", "Group key", "string"), col("group_de", "Gruppe", "Group", "string"), col("group_en", "Gruppe (englisch)", "Group (English)", "string"),
             col("thaler", "Betrag", "Amount", "integer", "Thaler",),
         ],
         "rows": income_rows,
         "source_refs": [{"page": "277", "block": "b1", "rows": "h1-r7"}, {"page": "277", "block": "b3"}, {"page": "276", "block": "b3"}]},
        {"name": "structure", "title": bi("Struktur von Einnahmen und Ausgaben (Voranschlag)", "Structure of revenue and expenditure (estimate)"),
         "columns": [
             col("side_key", "Kürzel", "Key", "string"),
             col("side_de", "Seite", "Side", "string"), col("side_en", "Seite (englisch)", "Side (English)", "string"),
             col("comp_key", "Kürzel Posten", "Component key", "string"),
             col("comp_de", "Posten", "Component", "string"), col("comp_en", "Posten (englisch)", "Component (English)", "string"),
             col("thaler", "Betrag", "Amount", "integer", "Thaler", derived=True, note="Summen bzw. Restbeträge; Einzelposten siehe Datensatz income und Quellen."),
         ],
         "rows": struct_rows,
         "source_refs": [{"page": "276", "block": "b3"}, {"page": "277", "block": "b1", "rows": "h1-r7"}, {"page": "277", "block": "b3"},
                         {"page": "272", "block": "b1"}, {"page": "275", "block": "b2"}, {"page": "275", "block": "b5"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "income",
         "title": bi("Veranschlagte Steuereinnahmen nach Posten", "Estimated tax revenue by item"),
         "caption": bi("Thaler jährlich, wie von Brückner genannt. Die Posten decken 79,7 % der veranschlagten Einnahmen von 296.000 Thalern; der Rest ist nicht aufgeschlüsselt.",
                       "Thaler per year, as given by Brückner. The items cover 79.7 % of the estimated revenue of 296,000 Thaler; the rest is not itemised."),
         "vegalite": {
             "height": 300,
             "mark": "bar",
             "encoding": {
                 "y": {"field": F("item"), "type": "nominal", "sort": "-x", "title": None, "axis": {"labelLimit": 300}},
                 "x": {"field": "thaler", "type": "quantitative", "title": bi("Thaler", "Thaler"), "axis": {"format": ",d"}},
                 "color": {"field": F("group"), "type": "nominal", "title": bi("Gruppe", "Group"), "sort": {"field": "group_key", "op": "min"}},
                 "tooltip": [ttf("item", "Posten", "Item"), ttf("group", "Gruppe", "Group"), {"field": "thaler", "title": "Thaler", "format": ","}],
             }}},
        {"id": "c2", "dataset": "structure",
         "title": bi("Einnahmen und Ausgaben im Voranschlag", "Revenue and expenditure in the estimate"),
         "caption": bi("Jahresvoranschlag 1866/68 in Thalern. »Militär« einschließlich Pensionen, »Gebäude und Wege« = Staatsgebäude plus Wegezuschuss. Von den Ausgaben sind nur diese Posten benannt; der Rest ist die Differenz zu 290.000 Thalern.",
                       "Annual estimate 1866/68 in Thaler. “Military” includes pensions; “Buildings and roads” = state buildings plus road subsidy. Only these expenditure heads are named; the remainder is the difference to 290,000 Thaler."),
         "vegalite": {
             "height": 340,
             "mark": {"type": "bar", "width": 90},
             "encoding": {
                 "x": {"field": F("side"), "type": "nominal", "title": None, "sort": {"field": "side_key", "op": "min"}, "axis": {"labelAngle": 0}},
                 "y": {"field": "thaler", "type": "quantitative", "title": "Thaler", "axis": {"format": ",d"}},
                 "color": {"field": F("comp"), "type": "nominal", "title": None, "sort": {"field": "comp_key", "op": "min"}, "legend": {"columns": 3, "labelLimit": 200}},
                 "order": {"field": "comp_key", "type": "nominal", "sort": "ascending"},
                 "tooltip": [ttf("side", "Seite", "Side"), ttf("comp", "Posten", "Component"), {"field": "thaler", "title": "Thaler", "format": ","}],
             }}},
    ],
    "keywords": {"de": ["Staatshaushalt", "Staatseinnahmen", "Steuern", "Grundsteuer", "Salzregie", "Zölle", "Voranschlag", "Finanzperiode 1866/68"],
                 "en": ["state budget", "revenue", "taxes", "land tax", "salt monopoly", "customs duties", "estimate", "financial period 1866/68"]},
    "transcription_issues": [
        {"page": "277", "block": "b1", "cell": "r1c3", "transcribed": "Zollgefälle, Braumalzbesteuer-, Übergangsabgaben und Rübenzuckersteuer", "facsimile": "Zollgefälle, Braumalzsteuer-, Uebergangsabgaben und Rübenzuckersteuer", "checked_facsimile": True, "note": "Wortlaut der Postenbezeichnung (Wort Braumalzsteuer), keine Zahl betroffen."},
    ],
}
write(ana)
