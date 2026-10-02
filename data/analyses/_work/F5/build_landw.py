import copy
from common import *

ID = "landwirtschaft"
A_NUTZ = "landwirtschaft-bodennutzung-1854"
A_BESITZ = "landwirtschaft-grundbesitz-1854"
A_ERNTE = "landwirtschaft-ernte-versorgung"
A_REFORM = "landwirtschaft-agrarreformen-1836-1868"
A_KAMMER = "landwirtschaft-kammer-rittergueter-1854"
A_LOHN = "wirtschaft-loehne-pacht-landwirtschaft-1860er"

nutzung = copy.deepcopy(dataset(A_NUTZ, "nutzung"))
bauern = copy.deepcopy(dataset(A_BESITZ, "bauerngueter"))
bilanz = copy.deepcopy(dataset(A_ERNTE, "bilanz"))
ritter = copy.deepcopy(dataset(A_REFORM, "rittergueter"))
loehne = copy.deepcopy(dataset(A_LOHN, "loehne"))

nu = rows_as_dicts(nutzung)
ba = rows_as_dicts(bauern)
bi_rows = rows_as_dicts(bilanz)
ri = rows_as_dicts(ritter)
lo = rows_as_dicts(loehne)

# ---------------------------------------------------------------- numbers: land use
GROUPS = {"Feld": "feld", "Wiese": "wiese", "Laubholz": "wald", "Nadelholz": "wald"}


def group_pct(lt):
    out = {"feld": 0, "wiese": 0, "wald": 0, "uebrig": 0}
    for r in nu:
        if r["landestheil_de"] == lt:
            out[GROUPS.get(r["nutzung_de"], "uebrig")] += r["pct"]
    return out


gp = {lt: group_pct(lt) for lt in DISTRICTS + ["Fürstentum"]}
print({k: {a: round(b, 1) for a, b in v.items()} for k, v in gp.items()})
total_morgen = sum(r["morgen"] for r in nu if r["landestheil_de"] == "Fürstentum")
print("total morgen", total_morgen, total_morgen * 0.255322)

# ---------------------------------------------------------------- numbers: farm sizes
size_groups = {1: "klein", 2: "mittel", 3: "mittel", 4: "gross", 5: "gross", 6: "gross"}
bz = {}
for lt in DISTRICTS + ["Fürstentum"]:
    sel = [r for r in ba if r["landestheil_de"] == lt]
    tot = sum(r["anzahl"] for r in sel)
    bz[lt] = {"total": tot}
    for g in ["klein", "mittel", "gross"]:
        bz[lt][g] = sum(r["anzahl"] for r in sel if size_groups[r["klasse_nr"]] == g) / tot * 100
print({k: {a: round(b, 1) for a, b in v.items()} for k, v in bz.items()})
n_farms = bz["Fürstentum"]["total"]
small_pct = bz["Fürstentum"]["klein"] + bz["Fürstentum"]["mittel"]

# ---------------------------------------------------------------- numbers: balance
bil = {r["landestheil_de"]: r for r in bi_rows}
for lt, r in bil.items():
    print(lt, r["produktion"], r["verbrauch"], r["ueberschuss_pct"])

# ---------------------------------------------------------------- numbers: estates, wages
ri_f = [r for r in ri if r["landestheil_de"] == "Fürstentum"]
n1647 = sum(r["anzahl"] for r in ri_f if r["jahr"] == 1647)
n1867 = sum(r["anzahl"] for r in ri_f if r["jahr"] == 1867)
own = {r["besitzer_de"]: r["anzahl"] for r in ri_f if r["jahr"] == 1867}
print(n1647, n1867, own)
lohn = {(r["merkmal_de"], r["gebiet_de"]): r for r in lo}
l_sommer = lohn[("Mann, Sommer", "Unterland")]
l_kost = lohn[("Mann, mit Kost", "Oberland")]
print(l_sommer["min"], l_sommer["max"], l_kost["min"], l_kost["max"])

d1 = lambda x: num_de(x, 1)
e1 = lambda x: num_en(x, 1)
d0 = lambda x: num_de(x, 0)
e0 = lambda x: num_en(x, 0)
G, S_, L_ = gp["Gera"], gp["Schleiz"], gp["Lobenstein-Ebersdorf"]
fub = bil["Land"]

summary = bi(
    f"Die Vermessung von 1854 verteilt {num_de(round(total_morgen))} Morgen auf Nutzungsarten: Das Unterland ist Ackerland ({d0(G['feld'])} Prozent Feld), das Oberland Wald und Wiese. "
    f"Von {num_de(n_farms)} geschlossenen Bauerngütern hatten {d1(small_pct)} Prozent weniger als 60 Morgen. "
    f"Nach Brückners Modellrechnung überstieg die Getreideerzeugung den Verbrauch im ganzen Land um {d1(fub['ueberschuss_pct'])} Prozent, in Lobenstein-Ebersdorf um {d1(bil['Lobenstein-Ebersdorf']['ueberschuss_pct'])} Prozent.",
    f"The survey of 1854 divides {num_en(round(total_morgen))} Morgen among kinds of use: the Unterland is arable land ({e0(G['feld'])} percent field), the Oberland woodland and meadow. "
    f"Of {num_en(n_farms)} closed peasant farms {e1(small_pct)} percent had less than 60 Morgen. "
    f"By Brückner’s model calculation grain production exceeded consumption by {e1(fub['ueberschuss_pct'])} percent in the country as a whole, by {e1(bil['Lobenstein-Ebersdorf']['ueberschuss_pct'])} percent in Lobenstein-Ebersdorf.",
)

findings = [
    bi(
        f"Die Zahl der Rittergüter sank von {n1647} (1647) auf {n1867} (1867); {own['Bürgerliche']} gehörten 1867 Bürgerlichen, {own['Adlige']} Adligen und {own['Fürstliche']} Mitgliedern des Fürstenhauses.",
        f"The number of manorial estates (Rittergüter) fell from {n1647} (1647) to {n1867} (1867); in 1867 {own['Bürgerliche']} belonged to commoners, {own['Adlige']} to nobles and {own['Fürstliche']} to members of the princely house.",
    ),
    bi(
        f"Ein Taglöhner verdiente im Unterland im Sommer {l_sommer['min']} bis {l_sommer['max']} Silbergroschen am Tag, im Oberland mit Kost {l_kost['min']} bis {l_kost['max']}; nach Brückner haben sich Löhne und Pachtgelder in etwa 40 Jahren verdoppelt.",
        f"A day laborer earned {l_sommer['min']} to {l_sommer['max']} silver groschen a day in summer in the Unterland, {l_kost['min']} to {l_kost['max']} with board in the Oberland; according to Brückner wages and rents doubled in about 40 years.",
    ),
    bi(
        f"Auf die Quadratmeile umgerechnet betrug der Überschuss in Gera {num_de(round(bil['Gera']['ueberschuss_je_qm']))} Zentner Roggenwert, in Schleiz {num_de(round(bil['Schleiz']['ueberschuss_je_qm']))} und in Lobenstein-Ebersdorf {num_de(round(bil['Lobenstein-Ebersdorf']['ueberschuss_je_qm']))}.",
        f"Per square mile the surplus was {num_en(round(bil['Gera']['ueberschuss_je_qm']))} hundredweights of rye value in Gera, {num_en(round(bil['Schleiz']['ueberschuss_je_qm']))} in Schleiz and {num_en(round(bil['Lobenstein-Ebersdorf']['ueberschuss_je_qm']))} in Lobenstein-Ebersdorf.",
    ),
]

method = bi(
    "Die Nutzungsarten stammen aus der Tabelle der Landesvermessung von 1854 (S. 217). Für das Diagramm sind Laub- und Nadelholz zu »Wald« zusammengefasst; »Übrige« sind Gärten, Hutung, Gehöfte, Teiche und steuerfreier Boden. "
    "Die Größenklassen der geschlossenen Bauerngüter (S. 224) sind zu drei Gruppen vereinigt; die Grenze von 60 Morgen ist Brückners eigene Unterscheidung von kleinen und großen Gütern. "
    "Produktion und Verbrauch (S. 227) sind Brückners Schätzungen für mittlere Erntejahre in Zentnern Roggenwert (Roggen gleich 1, Weizen und Hülsenfrüchte 1,29, Gerste 0,76, Hafer 0,47, Kartoffeln 0,25), der Verbrauch mit festen Sätzen je Kopf und Tier angesetzt. "
    "Rittergüter 1647 und 1867 stehen auf S. 230, für Gera 1867 gilt Brückners Berichtigung (S. 831: 26 statt 29). Löhne und Pachtpreise stammen aus dem Fließtext auf S. 227. "
    "Die Zahlen sind unverändert übernommen; Hektarwerte stehen in den Datensätzen, Prozente sind aus den gedruckten Zahlen berechnet.",
    "The kinds of use come from the table of the land survey of 1854 (p. 217). For the chart deciduous and coniferous woodland are combined as “Wald”; “Übrige” are gardens, pasture, farmsteads, ponds and tax-exempt land. "
    "The size classes of the closed peasant farms (p. 224) are merged into three groups; the limit of 60 Morgen is Brückner’s own distinction between small and large farms. "
    "Production and consumption (p. 227) are Brückner’s estimates for average harvest years in hundredweights of rye value (rye = 1, wheat and pulses 1.29, barley 0.76, oats 0.47, potatoes 0.25), with consumption set at fixed rates per head and animal. "
    "Manorial estates in 1647 and 1867 are on p. 230; for Gera in 1867 Brückner’s correction applies (p. 831: 26 instead of 29). Wages and rents come from the running text on p. 227. "
    "The figures are taken over unchanged; hectare values are in the datasets, percentages are computed from the printed numbers.",
)

conversions = [
    {"from": "preußischer Morgen", "to": "Hektar", "factor_or_formula": "ha = Morgen × 0,255322", "reference": "S. 832"},
    {"from": "Taler", "to": "Silbergroschen", "factor_or_formula": "1 Taler = 30 Silbergroschen", "reference": "preußisches Münzsystem; nicht in Brückners Tabelle"},
    {"from": "Zentner Roggenwert", "to": "Zentner Roggen", "factor_or_formula": "Roggen = 1; Weizen, Hülsenfrüchte 1,29; Gerste 0,76; Hafer 0,47; Kartoffeln 0,25", "reference": "S. 226"},
]

caveats = [
    bi(
        "Die Zahlen beruhen auf der Vermessung von 1854, Lobenstein-Ebersdorf war nur skizziert. Der Waldanteil weicht von den späteren Waldzahlen auf S. 240 ab (siehe »Wald und Holz«); die Quellen stammen aus verschiedenen Zeiten.",
        "The figures rest on the survey of 1854; Lobenstein-Ebersdorf was only sketched. The forest share differs from the later forest figures on p. 240 (see “Forests and timber”); the sources date from different times.",
    ),
    bi(
        "Die Getreidebilanz ist eine Modellrechnung, keine Erntestatistik. Für Gera weicht die Produktion der Bilanz (275 485 Zentner) von der Summe der Fruchtarten (260 714) ab; beide Werte sind so gedruckt.",
        "The grain balance is a model calculation, not a harvest statistic. For Gera the production in the balance (275,485 hundredweights) differs from the sum of the crops (260,714); both values are printed so.",
    ),
    bi(
        "Die Größenklassen zählen geschlossene Bauerngüter, nicht Flächen. Die Landesteil-Zeilen für Grundstücksverbände und ledige Grundstücke ergeben nicht die gedruckten Summen; verwendet sind die Zahlen der Größenklassen.",
        "The size classes count closed peasant farms, not areas. The district rows for plot associations and detached plots do not add up to the printed totals; the size-class figures are used.",
    ),
    bi(
        "Löhne und Pachtpreise sind Spannen aus dem Fließtext ohne Jahresangabe (um 1868); der Wert der Kost ist nicht beziffert.",
        "Wages and rents are ranges from the running text without a year (around 1868); the value of board is not stated.",
    ),
]

transcription_issues = [
    {
        "page": "230", "block": "b4", "cell": "r2c6", "transcribed": "29", "facsimile": "29", "checked_facsimile": True,
        "note": "Rittergüter im Landesteil Gera 1867: so gedruckt; Brückners Berichtigung (S. 831) verlangt 26, was zu den Besitzerzahlen (14 + 7 + 5) und zur Summe 41 passt. Die Auswertung rechnet mit 26. / Printed as 29; Brückner’s own correction (p. 831) gives 26.",
    }
]

# ---------------------------------------------------------------- charts
USE_CODE = "datum.nutzung_de == 'Feld' ? 'feld' : datum.nutzung_de == 'Wiese' ? 'wiese' : (datum.nutzung_de == 'Laubholz' || datum.nutzung_de == 'Nadelholz') ? 'wald' : 'uebrig'"
USE_NR = "datum.gruppe == 'feld' ? 1 : datum.gruppe == 'wiese' ? 2 : datum.gruppe == 'wald' ? 3 : 4"

c1 = {
    "id": "c1",
    "dataset": "nutzung",
    "title": bi(
        "Gera ist vor allem Ackerland, in Lobenstein-Ebersdorf bedeckt Wald fast die Hälfte der Fläche",
        "Gera is mostly arable land, while in Lobenstein-Ebersdorf woodland covers almost half of the area",
    ),
    "caption": bi(
        "Anteil der Nutzungsarten an der Fläche der Landesteile nach der Vermessung von 1854, in Prozent. Wald: Laub- und Nadelholz; Übrige: Gärten, Hutung, Gehöfte, Teiche, steuerfreier Boden. Quelle: S. 217.",
        "Share of the kinds of use in the area of the districts according to the survey of 1854, percent. Wald: deciduous and coniferous woodland; Übrige: gardens, pasture, farmsteads, ponds, tax-exempt land. Source: p. 217.",
    ),
    "vegalite": {
        "height": {"step": 46},
        "transform": [
            {"calculate": USE_CODE, "as": "gruppe"},
            {"calculate": USE_NR, "as": "gruppe_nr"},
            {"aggregate": [{"op": "sum", "field": "pct", "as": "pct_sum"}], "groupby": ["landestheil_de", "landestheil_en", "lt_nr", "gruppe", "gruppe_nr"]},
            {"stack": "pct_sum", "groupby": ["landestheil_de"], "sort": [{"field": "gruppe_nr", "order": "ascending"}], "offset": "zero", "as": ["x0", "x1"]},
            {"calculate": "(datum.x0 + datum.x1) / 2", "as": "xm"},
        ],
        "encoding": {
            "y": {
                "field": {"de": "landestheil_de", "en": "landestheil_en"}, "type": "nominal",
                "sort": {"field": "lt_nr", "op": "min", "order": "ascending"},
                "axis": {"title": None, "labelFontSize": 12, "labelLimit": 260},
            },
        },
        "layer": [
            {
                "mark": {"type": "bar", "height": {"band": 0.74}},
                "encoding": {
                    "x": {"field": "x0", "type": "quantitative", "scale": {"domain": [0, 100]}, "axis": {"title": {"de": "Anteil an der Fläche, %", "en": "Share of the area, %"}, "values": [0, 20, 40, 60, 80, 100]}},
                    "x2": {"field": "x1"},
                    "color": {
                        "field": "gruppe", "type": "nominal",
                        "scale": {"domain": ["feld", "wiese", "wald", "uebrig"], "range": ["@accent2", "@accent", "@accent3", "@context"]},
                        "legend": None,
                    },
                    "tooltip": [
                        tooltip("landestheil_de", "Landesteil", "District"),
                        {"field": "gruppe", "type": "nominal", "title": bi("Nutzung (feld, wiese, wald, uebrig)", "Use (feld, wiese, wald, uebrig)")},
                        tooltip("pct_sum", "Anteil, %", "Share, %", ".1f"),
                    ],
                },
            },
            {
                "transform": [{"filter": "datum.pct_sum >= 5"}],
                "mark": {"type": "text", "style": "label"},
                "encoding": {
                    "x": {"field": "xm", "type": "quantitative"},
                    "text": {"field": "pct_sum", "type": "quantitative", "format": ".0f"},
                    "color": {"condition": {"test": "datum.gruppe == 'wiese'", "value": "@paper"}, "value": "@ink"},
                },
            },
            {
                "transform": [
                    {"filter": "datum.lt_nr == 1"},
                    {"calculate": {
                        "de": "datum.gruppe == 'feld' ? 'Feld' : datum.gruppe == 'wiese' ? 'Wiese' : datum.gruppe == 'wald' ? 'Wald' : 'Übrige'",
                        "en": "datum.gruppe == 'feld' ? 'Field' : datum.gruppe == 'wiese' ? 'Meadow' : datum.gruppe == 'wald' ? 'Woodland' : 'Other'"},
                     "as": "gruppe_name"},
                ],
                "mark": {"type": "text", "style": "label", "dy": -27},
                "encoding": {"x": {"field": "xm", "type": "quantitative"}, "text": {"field": "gruppe_name", "type": "nominal"}},
            },
        ],
    },
}

SIZE_CALC = "datum.klasse_nr == 1 ? 'klein' : datum.klasse_nr <= 3 ? 'mittel' : 'gross'"
c2 = {
    "id": "c2",
    "dataset": "bauerngueter",
    "title": bi(
        f"Schleiz hatte die größten Bauerngüter: {d0(bz['Schleiz']['gross'])} Prozent über 60 Morgen, in Gera {d0(bz['Gera']['gross'])}, in Lobenstein-Ebersdorf {d0(bz['Lobenstein-Ebersdorf']['gross'])}",
        f"Schleiz had the largest farms: {e0(bz['Schleiz']['gross'])} percent over 60 Morgen, in Gera {e0(bz['Gera']['gross'])}, in Lobenstein-Ebersdorf {e0(bz['Lobenstein-Ebersdorf']['gross'])}",
    ),
    "caption": bi(
        f"Geschlossene Bauerngüter nach Größe, in Prozent der Güter des Landesteils. Brückner nennt Güter über 60 Morgen »große«. Zahl der Güter: Gera {num_de(bz['Gera']['total'])}, Schleiz {num_de(bz['Schleiz']['total'])}, Lobenstein-Ebersdorf {num_de(bz['Lobenstein-Ebersdorf']['total'])}. Quelle: S. 224.",
        f"Closed peasant farms by size, percent of the farms of the district. Brückner calls farms over 60 Morgen “large”. Number of farms: Gera {num_en(bz['Gera']['total'])}, Schleiz {num_en(bz['Schleiz']['total'])}, Lobenstein-Ebersdorf {num_en(bz['Lobenstein-Ebersdorf']['total'])}. Source: p. 224.",
    ),
    "vegalite": {
        "height": {"step": 46},
        "transform": [
            {"filter": "datum.lt_nr < 4"},
            {"calculate": SIZE_CALC, "as": "groesse"},
            {"calculate": "datum.groesse == 'klein' ? 1 : datum.groesse == 'mittel' ? 2 : 3", "as": "groesse_nr"},
            {"joinaggregate": [{"op": "sum", "field": "anzahl", "as": "gesamt"}], "groupby": ["landestheil_de"]},
            {"aggregate": [{"op": "sum", "field": "anzahl", "as": "n"}, {"op": "min", "field": "gesamt", "as": "gesamt"}], "groupby": ["landestheil_de", "landestheil_en", "lt_nr", "groesse", "groesse_nr"]},
            {"calculate": "datum.n / datum.gesamt * 100", "as": "pct"},
            {"stack": "pct", "groupby": ["landestheil_de"], "sort": [{"field": "groesse_nr", "order": "ascending"}], "offset": "zero", "as": ["x0", "x1"]},
            {"calculate": "(datum.x0 + datum.x1) / 2", "as": "xm"},
            {"calculate": {
                "de": "datum.landestheil_de == 'Gera' ? (datum.groesse == 'klein' ? 'bis 20 Morgen ' : datum.groesse == 'mittel' ? '20 bis 60 Morgen ' : 'über 60 Morgen ') + format(datum.pct, '.1f') : format(datum.pct, '.1f')",
                "en": "datum.landestheil_de == 'Gera' ? (datum.groesse == 'klein' ? 'up to 20 Morgen ' : datum.groesse == 'mittel' ? '20 to 60 Morgen ' : 'over 60 Morgen ') + format(datum.pct, '.1f') : format(datum.pct, '.1f')"},
             "as": "segment_label"},
        ],
        "encoding": {
            "y": {
                "field": {"de": "landestheil_de", "en": "landestheil_en"}, "type": "nominal",
                "sort": {"field": "lt_nr", "op": "min", "order": "ascending"},
                "axis": {"title": None, "labelFontSize": 12, "labelLimit": 260},
            },
        },
        "layer": [
            {
                "mark": {"type": "bar", "height": {"band": 0.74}},
                "encoding": {
                    "x": {"field": "x0", "type": "quantitative", "scale": {"domain": [0, 100]}, "axis": {"title": {"de": "Anteil der Bauerngüter, %", "en": "Share of peasant farms, %"}, "values": [0, 20, 40, 60, 80, 100]}},
                    "x2": {"field": "x1"},
                    "color": {
                        "field": "groesse", "type": "nominal", "legend": None,
                        "scale": {"domain": ["klein", "mittel", "gross"], "range": ["@accent2", "@context", "@accent"]},
                    },
                    "tooltip": [
                        tooltip("landestheil_de", "Landesteil", "District"),
                        {"field": "groesse", "type": "nominal", "title": bi("Größe (klein, mittel, gross)", "Size (klein, mittel, gross)")},
                        tooltip("n", "Güter", "Farms", ",d"),
                        tooltip("pct", "Anteil, %", "Share, %", ".1f"),
                    ],
                },
            },
            {
                "mark": {"type": "text", "style": "label"},
                "encoding": {
                    "x": {"field": "xm", "type": "quantitative"},
                    "text": {"field": "segment_label", "type": "nominal"},
                    "color": {"condition": {"test": "datum.groesse == 'gross'", "value": "@paper"}, "value": "@ink"},
                },
            },
        ],
    },
}

c3 = {
    "id": "c3",
    "dataset": "bilanz",
    "title": bi(
        f"Die Getreideerzeugung überstieg den Verbrauch um {d0(fub['ueberschuss_pct'])} Prozent, in Lobenstein-Ebersdorf nur um {d0(bil['Lobenstein-Ebersdorf']['ueberschuss_pct'])} Prozent",
        f"Grain production exceeded consumption by {e0(fub['ueberschuss_pct'])} percent, in Lobenstein-Ebersdorf by only {e0(bil['Lobenstein-Ebersdorf']['ueberschuss_pct'])} percent",
    ),
    "caption": bi(
        f"Brückners Schätzung von Erzeugung und Verbrauch in Zentnern Roggenwert für mittlere Erntejahre; Zahl am Ende: Überschuss in Prozent des Verbrauchs. Im ganzen Land {num_de(round(fub['produktion']))} gegen {num_de(fub['verbrauch'])} Zentner. Quelle: S. 226 bis 227.",
        f"Brückner’s estimate of production and consumption in hundredweights of rye value for average harvest years; number at the end: surplus as percent of consumption. For the whole country {num_en(round(fub['produktion']))} against {num_en(fub['verbrauch'])} hundredweights. Source: pp. 226 to 227.",
    ),
    "vegalite": {
        "height": {"step": 56},
        "transform": [{"filter": "datum.lt_nr < 4"}],
        "encoding": {
            "y": {
                "field": {"de": "landestheil_de", "en": "landestheil_en"}, "type": "nominal",
                "sort": {"field": "lt_nr", "op": "min", "order": "ascending"},
                "axis": {"title": None, "labelFontSize": 12, "labelLimit": 260},
            },
        },
        "layer": [
            {
                "mark": {"type": "rule", "strokeWidth": 3, "color": "@context"},
                "encoding": {
                    "x": {"field": "verbrauch", "type": "quantitative", "scale": {"domain": [100000, 300000]}, "axis": {"title": {"de": "Zentner Roggenwert", "en": "Hundredweights of rye value"}, "format": ",d", "values": [100000, 150000, 200000, 250000, 300000]}},
                    "x2": {"field": "produktion"},
                },
            },
            {
                "mark": {"type": "point", "filled": True, "size": 110, "color": "@muted"},
                "encoding": {
                    "x": {"field": "verbrauch", "type": "quantitative"},
                    "tooltip": [
                        tooltip("landestheil_de", "Landesteil", "District"),
                        tooltip("verbrauch", "Verbrauch, Zentner", "Consumption, cwt", ",d"),
                    ],
                },
            },
            {
                "mark": {"type": "point", "filled": True, "size": 110, "color": "@accent3"},
                "encoding": {
                    "x": {"field": "produktion", "type": "quantitative"},
                    "tooltip": [
                        tooltip("landestheil_de", "Landesteil", "District"),
                        tooltip("produktion", "Erzeugung, Zentner", "Production, cwt", ",d"),
                        tooltip("ueberschuss_pct", "Überschuss, %", "Surplus, %", ".1f"),
                    ],
                },
            },
            {
                "mark": {"type": "text", "align": "left", "dx": 12, "style": "label"},
                "encoding": {
                    "x": {"field": "produktion", "type": "quantitative"},
                    "text": {"field": "ueberschuss_pct", "type": "quantitative", "format": "+.1f"},
                },
            },
            {
                "transform": [{"filter": "datum.lt_nr == 1"}],
                "mark": {"type": "text", "align": "right", "dx": -11, "dy": -14, "style": "annotation"},
                "encoding": {"x": {"field": "verbrauch", "type": "quantitative"}, "text": {"value": {"de": "Verbrauch", "en": "Consumption"}}},
            },
            {
                "transform": [{"filter": "datum.lt_nr == 1"}],
                "mark": {"type": "text", "align": "left", "dx": 11, "dy": -14, "style": "annotation"},
                "encoding": {"x": {"field": "produktion", "type": "quantitative"}, "text": {"value": {"de": "Erzeugung", "en": "Production"}}},
            },
        ],
    },
}

datasets = [nutzung, bauern, bilanz, ritter, loehne]

sources = [
    {"page": "217", "block": "b1"}, {"page": "224", "block": "b2"}, {"page": "224", "block": "b3"}, {"page": "226", "block": "b3"},
    {"page": "226", "block": "b4"}, {"page": "227", "block": "b1"}, {"page": "227", "block": "b3"}, {"page": "230", "block": "b4"},
]

feature = {
    "id": ID,
    "title": bi("Boden, Besitz und Ernte", "Land, ownership and harvest"),
    "category": "agriculture",
    "section": "t1-3-2",
    "merges": [A_NUTZ, A_BESITZ, A_ERNTE, A_REFORM, A_KAMMER, A_LOHN],
    "sources": sources,
    "summary": summary,
    "findings": findings,
    "method": method,
    "conversions": conversions,
    "caveats": caveats,
    "transcription_issues": transcription_issues,
    "datasets": datasets,
    "charts": [c1, c2, c3],
    "keywords": {
        "de": ["Landwirtschaft", "Bodennutzung", "Grundbesitz", "Bauerngüter", "Rittergüter", "Ernte", "Getreide", "Taglohn", "Pacht", "Ablösung"],
        "en": ["agriculture", "land use", "landholding", "peasant farms", "manorial estates", "harvest", "grain", "day wages", "rent", "redemption of dues"],
    },
    "related": ["viehzucht", "wald-holz", "dorfleben", "berufe-gewerbe"],
    "generated_by": "Claude Sonnet 5.5 (Agent F5), aus 6 Einzelauswertungen zusammengeführt",
    "date": "2026-10-02",
}

if __name__ == "__main__":
    for k in ["title", "summary"]:
        for lang in ["de", "en"]:
            print(k, lang, words(feature[k][lang]))
    write_feature(feature)
    validate(ID)
