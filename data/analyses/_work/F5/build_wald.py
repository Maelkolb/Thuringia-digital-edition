import copy
from common import *

ID = "wald-holz"
A1 = "forstwirtschaft-waldflaeche-besitz"
A2 = "forstwirtschaft-holzpreise-zuwachs"

wald = copy.deepcopy(dataset(A1, "wald"))
wa_old = rows_as_dicts(dataset(A1, "waldanteil"))
domaene = copy.deepcopy(dataset(A1, "domaene"))
holzpreise = copy.deepcopy(dataset(A2, "holzpreise"))
zuwachs = copy.deepcopy(dataset(A2, "zuwachs"))
wrows = rows_as_dicts(wald)

# ---------------------------------------------------------------- derived table per district
names_en = {"Gera": "Gera", "Schleiz": "Schleiz", "Lobenstein-Ebersdorf": "Lobenstein-Ebersdorf", "Fürstentum": "Principality"}
order = ["Gera", "Schleiz", "Lobenstein-Ebersdorf", "Fürstentum"]


def sums(lt):
    sel = [r for r in wrows if (lt == "Fürstentum" or r["landestheil_de"] == lt)]
    s = lambda owner=None, holz=None: sum((r["morgen"] or 0) for r in sel if (owner is None or r["besitzer_de"] in owner) and (holz is None or r["holzart_de"] == holz))
    return {
        "kammer": s(["Kammerforste"]),
        "gemeinde_stiftung": s(["Gemeindeforste", "Stiftungsforste"]),
        "privat": s(["Privatwald"]),
        "laub": s(holz="Laubwald"),
        "total": s(),
    }


wa_cols = [
    col("landestheil_de", "Landesteil", "District", "string"),
    col("landestheil_en", "Landesteil (englisch)", "District (English)", "string"),
    col("lt_nr", "Reihenfolge", "Order", "integer", derived=True),
    col("flaeche_morgen", "Gesamtfläche (Vermessung 1854)", "Total area (survey of 1854)", "number", "preuß. Morgen"),
    col("wald_morgen", "Waldfläche", "Forest area", "integer", "preuß. Morgen"),
    col("kammer_morgen", "Kammerforste", "Chamber forests", "integer", "preuß. Morgen", True, "Summe Laub + Nadel; für das Fürstentum gedruckt 63 767"),
    col("gemeinde_stiftung_morgen", "Gemeinde- und Stiftungsforste", "Municipal and foundation forests", "integer", "preuß. Morgen", True, "Gemeindeforste + Stiftungsforste"),
    col("privat_morgen", "Privatwald", "Private woodland", "integer", "preuß. Morgen", True, "Laub + Nadel; für Gera ist 15 191 gedruckt (Druckfehler, Summe 15 181)"),
    col("laub_morgen", "Laubwald", "Deciduous woodland", "integer", "preuß. Morgen", True),
    col("anteil_pct", "Waldanteil an der Fläche", "Forest share of area", "number", "%", True),
    col("pct_flaeche_kammer", "Kammerforste, Anteil an der Fläche", "Chamber forests, share of area", "number", "%", True),
    col("pct_flaeche_gemeinde_stiftung", "Gemeinde- und Stiftungsforste, Anteil an der Fläche", "Municipal and foundation forests, share of area", "number", "%", True),
    col("pct_flaeche_privat", "Privatwald, Anteil an der Fläche", "Private woodland, share of area", "number", "%", True),
    col("pct_wald_kammer", "Kammerforste, Anteil am Wald", "Chamber forests, share of forest", "number", "%", True),
    col("pct_wald_privat", "Privatwald, Anteil am Wald", "Private woodland, share of forest", "number", "%", True),
    col("laub_pct_wald", "Laubwald, Anteil am Wald", "Deciduous woodland, share of forest", "number", "%", True),
]
wa_rows = []
stats = {}
total_laub = sums("Fürstentum")["laub"]
for i, lt in enumerate(order, 1):
    o = [x for x in wa_old if x["landestheil_de"] == lt][0]
    s = sums(lt)
    assert s["total"] == o["wald_morgen"], (lt, s["total"], o["wald_morgen"])
    area = o["flaeche_morgen"]
    st = {
        "area": area, "wald": o["wald_morgen"], "anteil": o["wald_morgen"] / area * 100,
        "kammer_f": s["kammer"] / area * 100, "gs_f": s["gemeinde_stiftung"] / area * 100, "privat_f": s["privat"] / area * 100,
        "kammer_w": s["kammer"] / s["total"] * 100, "privat_w": s["privat"] / s["total"] * 100,
        "gs_w": s["gemeinde_stiftung"] / s["total"] * 100,
        "laub_w": s["laub"] / s["total"] * 100, "laub_share_of_all": s["laub"] / total_laub * 100,
        **s,
    }
    stats[lt] = st
    wa_rows.append([
        lt, names_en[lt], i, area, o["wald_morgen"], s["kammer"], s["gemeinde_stiftung"], s["privat"], s["laub"],
        round(st["anteil"], 2), round(st["kammer_f"], 2), round(st["gs_f"], 2), round(st["privat_f"], 2),
        round(st["kammer_w"], 2), round(st["privat_w"], 2), round(st["laub_w"], 2),
    ])
waldanteil = {
    "name": "waldanteil",
    "title": bi("Wald nach Landesteil und Besitzer, in Prozent der Fläche", "Forest by district and owner, as percent of the area"),
    "columns": wa_cols,
    "rows": wa_rows,
    "source_refs": [
        {"page": "240", "block": "b2", "rows": "r2-r8"},
        {"page": "217", "block": "b1", "rows": "t11"},
    ],
}

# ---------------------------------------------------------------- numbers for the text
S = stats
fu = S["Fürstentum"]
nadel_pct = 100 - fu["laub_w"]
dom1647 = [r for r in rows_as_dicts(domaene) if r["zeit_de"] == "1647"]
dom1647_total = sum(r["morgen"] for r in dom1647)
dom_now = [r for r in rows_as_dicts(domaene) if r["zeit_de"] != "1647"][0]["morgen"]
dom_wald = [r["morgen"] for r in dom1647 if r["art_de"] == "Wald"][0]
dom_gereumt = [r["morgen"] for r in dom1647 if r["art_de"] != "Wald"][0]
hp = rows_as_dicts(holzpreise)


def price(art, year):
    return [r for r in hp if r["holzart_de"] == art and r["jahr"] == year][0]["preis_mitte"]


fac = {a: price(a, 1868) / price(a, 1800) for a in ["Bauholz", "Blochholz", "Feuerholz"]}
fac1840_feuer = price("Feuerholz", 1840) / price("Feuerholz", 1800)
zu = rows_as_dicts(zuwachs)
zd = [r for r in zu if r["besitzart_nr"] == 1][0]
zp = [r for r in zu if r["besitzart_nr"] == 3][0]
rel_lo = zp["zuwachs_von"] / zd["zuwachs_von"]
rel_hi = zp["zuwachs_bis"] / zd["zuwachs_von"]
print("fac", fac, fac1840_feuer, "rel", rel_lo, rel_hi)
print({k: round(v["anteil"], 1) for k, v in S.items()}, {k: (round(v["kammer_w"], 1), round(v["privat_w"], 1)) for k, v in S.items()})
print("laub", {k: round(v["laub_w"], 1) for k, v in S.items()}, round(S["Gera"]["laub_share_of_all"], 1))
print("dom", dom1647_total, dom_now, dom1647_total - dom_now)

d1 = lambda x: num_de(x, 1)
e1 = lambda x: num_en(x, 1)
G, SC, L = S["Gera"], S["Schleiz"], S["Lobenstein-Ebersdorf"]

summary = bi(
    f"Der Wald des Fürstentums umfasste um 1868 {num_de(fu['wald'])} Morgen oder {num_de(round(fu['wald'] * 0.255322))} Hektar, {d1(fu['anteil'])} Prozent der Fläche, {d1(nadel_pct)} Prozent davon Nadelholz. "
    f"Er nimmt vom Unterland zum Oberland zu und gehört dort etwa zur Hälfte der Kammer, im Unterland überwiegend Privatbesitzern. "
    f"Die Holzpreise stiegen von 1800 bis 1868 auf das {d1(min(fac.values()))}- bis {d1(max(fac.values()))}-Fache.",
    f"Around 1868 the principality’s forest covered {num_en(fu['wald'])} Morgen or {num_en(round(fu['wald'] * 0.255322))} hectares, {e1(fu['anteil'])} percent of the area, {e1(nadel_pct)} percent of it conifers. "
    f"It increases from the Unterland to the Oberland and there belongs about half to the Chamber (the princely domain), in the Unterland mostly to private owners. "
    f"Timber prices rose to between {e1(min(fac.values()))} and {e1(max(fac.values()))} times their 1800 level by 1868.",
)

findings = [
    bi(
        f"Laubwald gibt es fast nur im Landesteil Gera: Er hat {d1(G['laub_share_of_all'])} Prozent des gesamten Laubwaldes; dort sind {d1(G['laub_w'])} Prozent des Waldes Laubholz, in Schleiz {d1(SC['laub_w'])}, in Lobenstein-Ebersdorf {d1(L['laub_w'])} Prozent.",
        f"Deciduous forest is almost confined to the district of Gera: it holds {e1(G['laub_share_of_all'])} percent of all deciduous forest, and {e1(G['laub_w'])} percent of its woodland is deciduous, against {e1(SC['laub_w'])} in Schleiz and {e1(L['laub_w'])} in Lobenstein-Ebersdorf.",
    ),
    bi(
        f"Der Domänenwald von 1647 ({num_de(dom_wald)} Morgen Wald und {num_de(dom_gereumt)} Morgen Geräumde, zusammen {num_de(dom1647_total)}) war nur {num_de(dom1647_total - dom_now)} Morgen größer als die Kammerforste von {num_de(dom_now)} Morgen um 1868.",
        f"The domain forest of 1647 ({num_en(dom_wald)} Morgen of forest and {num_en(dom_gereumt)} Morgen of cleared land, {num_en(dom1647_total)} in all) was only {num_en(dom1647_total - dom_now)} Morgen larger than the Chamber forests of {num_en(dom_now)} Morgen around 1868.",
    ),
    bi(
        f"Im Landesteil Gera gehören {d1(G['privat_w'])} Prozent des Waldes Privatbesitzern, im Oberland dagegen gut die Hälfte den Kammerforsten (Schleiz {d1(SC['kammer_w'])}, Lobenstein-Ebersdorf {d1(L['kammer_w'])} Prozent).",
        f"In the district of Gera {e1(G['privat_w'])} percent of the forest belongs to private owners, whereas in the Oberland a good half belongs to the Chamber forests (Schleiz {e1(SC['kammer_w'])}, Lobenstein-Ebersdorf {e1(L['kammer_w'])} percent).",
    ),
]

method = bi(
    "Flächen, Besitzer und Holzart stammen aus der Tabelle auf S. 240 (Block b2), die Gesamtfläche der Landesteile aus der Vermessung von 1854 (S. 217). "
    "Anteile an der Fläche und am Wald sind aus den Flächen berechnet, nicht aus Brückners Prozentzahlen. Kammerforste sind Brückners »Domainenwald«. "
    "Der Landesteil Schleiz setzt sich aus Pflege Reichenfels, Herrschaft Schleiz und Pflege Saalburg zusammen. "
    "Die Preise je Kubikfuß weiches Holz (S. 241, Block b6) stehen im Druck in Silbergroschen und gemischten Brüchen (1 1/6) und sind als Dezimalzahlen übernommen; für 1840 gibt Brückner Spannen an, das Diagramm zeigt deren Mitte. "
    "Der Index setzt den Preis von 1800 gleich 100. Den Zuwachs gibt Brückner in Klaftern je Morgen und Jahr an; er wurde mit 1 Klafter = 126 Kubikfuß = 2,8454 m³ (S. 832, Gera) und 1 Morgen = 0,255322 ha in Kubikmeter Raummaß je Hektar umgerechnet.",
    "Areas, owners and tree species come from the table on p. 240 (block b2), the total area of the districts from the survey of 1854 (p. 217). "
    "Shares of the area and of the forest are computed from the areas, not taken from Brückner’s percentages. Chamber forests are Brückner’s “Domainenwald”. "
    "The district of Schleiz consists of the Pflege Reichenfels, the Herrschaft Schleiz and the Pflege Saalburg. "
    "The prices per cubic foot of soft wood (p. 241, block b6) are printed in silver groschen and mixed fractions (1 1/6) and are converted to decimals; for 1840 Brückner gives ranges, and the chart shows their midpoint. "
    "The index sets the price of 1800 to 100. Brückner states growth in Klafter per Morgen and year; it was converted with 1 Klafter = 126 cubic feet = 2.8454 m³ (p. 832, Gera) and 1 Morgen = 0.255322 ha into cubic meters of stacked wood per hectare.",
)

caveats = [
    bi(
        "Waldfläche (um 1868, nach amtlichen Mitteilungen) und Gesamtfläche (Vermessung 1854, für Lobenstein-Ebersdorf nur croquirt) stammen aus verschiedenen Zeiten. Die Vermessung von 1854 (S. 217) weist weniger Wald aus (siehe »Boden, Besitz und Ernte«). Brückners Besitzprozente (Privatwald 48,23, Domänenwald 48,12) weichen leicht von den berechneten ab.",
        "Forest area (around 1868, from official reports) and total area (survey of 1854, only sketched for Lobenstein-Ebersdorf) date from different times. The survey of 1854 (p. 217) itself shows less forest (see “Land, ownership and harvest”). Brückner’s ownership percentages (private 48.23, domain 48.12) differ slightly from the computed ones.",
    ),
    bi(
        "Die Preisreihe hat nur vier Zeitpunkte (1800, 1820, 1840, 1868); was dazwischen geschah, ist nicht belegt. Brückner nennt nur »weiches Holz« und »Cubikfuß«, ob Fest- oder Raummaß, bleibt offen.",
        "The price series has only four points in time (1800, 1820, 1840, 1868); what happened in between is not documented. Brückner says only “soft wood” and “Cubikfuß”; whether solid or stacked volume is meant remains open.",
    ),
    bi(
        "Der Zuwachs je Besitzart ist eine Schätzung Brückners für nachhaltige Bewirtschaftung, keine Messung. Die Umrechnung in Kubikmeter benutzt die Klafter von Gera zu 126 Kubikfuß und ist eine Näherung.",
        "The growth by type of owner is an estimate by Brückner for sustained-yield management, not a measurement. The conversion into cubic meters uses the Gera Klafter of 126 cubic feet and is an approximation.",
    ),
]

conversions = [
    {"from": "preußischer Morgen", "to": "Hektar", "factor_or_formula": "ha = Morgen × 0,255322", "reference": "S. 832"},
    {"from": "Klafter (126 Kubikfuß, Gera)", "to": "Kubikmeter Raummaß", "factor_or_formula": "1 Klafter = 2,8454 m³", "reference": "S. 832"},
    {"from": "Klafter je Morgen und Jahr", "to": "Kubikmeter je Hektar und Jahr", "factor_or_formula": "× 2,8454 ÷ 0,255322", "reference": "S. 832"},
]

transcription_issues = [
    {
        "page": "240", "block": "b2", "cell": "r2c14", "transcribed": "15191", "facsimile": "15191", "checked_facsimile": True,
        "note": "Gera, Privatwald, Spalte Sa.: so gedruckt, aber Laub + Nadel = 4701 + 10480 = 15 181; die Summen des Landesteils (21 298) und des Fürstentums (64 959) passen zu 15 181. Die Auswertung rechnet mit 15 181. / Printed so, but deciduous + coniferous = 15,181, which the totals confirm.",
    }
]

# ---------------------------------------------------------------- charts
OWN_DOMAIN = ["kammer", "gemeinde", "privat"]
OWN_RANGE = ["@accent", "@accent2", "@accent3"]
OWN_LABEL_EXPR = {
    "de": "datum.value == 'kammer' ? 'Kammerforste' : datum.value == 'gemeinde' ? 'Gemeinde, Stiftung' : 'Privatwald'",
    "en": "datum.value == 'kammer' ? 'Chamber forests' : datum.value == 'gemeinde' ? 'Municipal, trust' : 'Private'",
}
OWN_NAME_CALC = {
    "de": "datum.besitzer == 'kammer' ? 'Kammerforste' : datum.besitzer == 'gemeinde' ? 'Gemeinde- und Stiftungswald' : 'Privatwald'",
    "en": "datum.besitzer == 'kammer' ? 'Chamber forests' : datum.besitzer == 'gemeinde' ? 'Municipal and foundation forests' : 'Private woodland'",
}

c1 = {
    "id": "c1",
    "dataset": "waldanteil",
    "title": bi(
        "Der Wald bedeckt in Lobenstein-Ebersdorf mehr als die Hälfte der Fläche, in Gera nur ein Viertel",
        "Forest covers more than half of Lobenstein-Ebersdorf but only a quarter of Gera",
    ),
    "caption": bi(
        "Wald in Prozent der Fläche des Landesteils, die Farben zeigen den Besitzer; Zahl am Balkenende: Waldanteil insgesamt. Waldfläche um 1868, Gesamtfläche nach der Vermessung von 1854. Quelle: S. 240, 217.",
        "Forest as percent of the district’s area, colors show the owner; number at the bar end: total forest share. Forest area around 1868, total area from the survey of 1854. Source: pp. 240, 217.",
    ),
    "vegalite": {
        "height": {"step": 44},
        "encoding": {
            "y": {
                "field": {"de": "landestheil_de", "en": "landestheil_en"}, "type": "nominal",
                "sort": {"field": "lt_nr", "op": "min", "order": "ascending"},
                "axis": {"title": None, "labelFontSize": 12, "labelLimit": 200},
            },
        },
        "layer": [
            {
                "transform": [
                    {"fold": ["pct_flaeche_kammer", "pct_flaeche_gemeinde_stiftung", "pct_flaeche_privat"], "as": ["besitzer_roh", "pct"]},
                    {"calculate": "datum.besitzer_roh == 'pct_flaeche_kammer' ? 'kammer' : datum.besitzer_roh == 'pct_flaeche_gemeinde_stiftung' ? 'gemeinde' : 'privat'", "as": "besitzer"},
                    {"calculate": OWN_NAME_CALC, "as": "besitzer_name"},
                    {"calculate": "datum.besitzer == 'kammer' ? 1 : datum.besitzer == 'privat' ? 2 : 3", "as": "besitzer_nr"},
                ],
                "mark": {"type": "bar", "height": {"band": 0.72}},
                "encoding": {
                    "x": {
                        "field": "pct", "type": "quantitative", "stack": "zero",
                        "scale": {"domain": [0, 62]},
                        "axis": {"title": {"de": "Wald in Prozent der Fläche", "en": "Forest as percent of area"}, "values": [0, 10, 20, 30, 40, 50, 60], "format": "d"},
                    },
                    "color": {
                        "field": "besitzer", "type": "nominal",
                        "scale": {"domain": OWN_DOMAIN, "range": OWN_RANGE},
                        "legend": {"title": None, "labelExpr": OWN_LABEL_EXPR, "columns": 3, "columnPadding": 8, "labelLimit": 220},
                    },
                    "order": {"field": "besitzer_nr", "type": "quantitative"},
                    "tooltip": [
                        tooltip("landestheil_de", "Landesteil", "District"),
                        {"field": "besitzer_name", "type": "nominal", "title": bi("Besitzer", "Owner")},
                        tooltip("pct", "Anteil an der Fläche, %", "Share of the area, %", ".1f"),
                    ],
                },
            },
            {
                "mark": {"type": "text", "align": "left", "dx": 6, "style": "label"},
                "encoding": {
                    "x": {"field": "anteil_pct", "type": "quantitative"},
                    "text": {"field": "anteil_pct", "type": "quantitative", "format": ".1f"},
                },
            },
        ],
    },
}
print(json.dumps(c1)[:200])

# prices: indexed lines
price_calc = [
    {"window": [{"op": "first_value", "field": "preis_mitte", "as": "basis"}], "groupby": ["holzart_de"], "sort": [{"field": "jahr"}], "frame": [None, None]},
    {"calculate": "datum.preis_mitte / datum.basis * 100", "as": "index"},
    {"calculate": "datum.preis_von / datum.basis * 100", "as": "index_von"},
    {"calculate": "datum.preis_bis / datum.basis * 100", "as": "index_bis"},
]
TIMBER_DOMAIN = ["Bauholz", "Blochholz", "Feuerholz"]
c2 = {
    "id": "c2",
    "dataset": "holzpreise",
    "title": bi(
        "Feuerholz verdreifachte sich schon bis 1840, Bau- und Blochholz stiegen bis 1868 weiter",
        "Firewood tripled in price by 1840; construction and log timber kept rising until 1868",
    ),
    "caption": bi(
        "Preis je Kubikfuß weiches Holz, 1800 gleich 100. Für 1840 nennt Brückner Spannen von Bau- und Blochholz; gezeigt ist die Mitte. Zahl am Linienende: Vielfaches des Preises von 1800. Quelle: S. 241.",
        "Price per cubic foot of soft wood, 1800 = 100. For 1840 Brückner gives ranges for construction and log timber; the midpoint is shown. Number at the line end: multiple of the 1800 price. Source: p. 241.",
    ),
    "vegalite": {
        "height": 300,
        "transform": price_calc,
        "encoding": {
            "x": {
                "field": "jahr", "type": "quantitative",
                "scale": {"domain": [1795, 1900], "nice": False},
                "axis": {"values": [1800, 1820, 1840, 1868], "format": "d", "title": None},
            },
            "color": {
                "field": "holzart_de", "type": "nominal", "legend": None,
                "scale": {"domain": TIMBER_DOMAIN, "range": ["@accent", "@accent3", "@accent2"]},
            },
        },
        "layer": [
            {"mark": {"type": "rule", "strokeDash": [3, 3], "color": "@muted"}, "encoding": {"y": {"datum": 100}, "x": None, "color": None}},
            {
                "mark": {"type": "line", "strokeWidth": 2.5},
                "encoding": {
                    "y": {"field": "index", "type": "quantitative", "scale": {"domain": [94, 316]}, "axis": {"title": {"de": "Preis, 1800 = 100", "en": "Price, 1800 = 100"}, "values": [100, 150, 200, 250, 300]}},
                },
            },
            {
                "mark": {"type": "point", "filled": True, "size": 60, "opacity": 1},
                "encoding": {
                    "y": {"field": "index", "type": "quantitative"},
                    "tooltip": [
                        {"field": {"de": "holzart_de", "en": "holzart_en"}, "type": "nominal", "title": bi("Sortiment", "Assortment")},
                        tooltip("jahr", "Jahr", "Year", "d"),
                        {"field": "preis_text", "type": "nominal", "title": bi("Preis, Sgr. je Kubikfuß (gedruckt)", "Price, Sgr. per cubic foot (as printed)")},
                        tooltip("index", "Index, 1800 = 100", "Index, 1800 = 100", ".0f"),
                    ],
                },
            },
            {
                "transform": [
                    {"filter": "datum.jahr == 1868"},
                    {"calculate": {"de": "datum.holzart_de + ' ×' + format(datum.index / 100, '.1f')", "en": "datum.holzart_en + ' ×' + format(datum.index / 100, '.1f')"}, "as": "endlabel"},
                ],
                "mark": {"type": "text", "align": "left", "dx": 9, "style": "label"},
                "encoding": {"y": {"field": "index", "type": "quantitative"}, "text": {"field": "endlabel"}, "color": None},
            },
        ],
    },
}

c3 = {
    "id": "c3",
    "dataset": "zuwachs",
    "title": bi(
        "Privatwald wächst nach Brückners Schätzung nur ein Fünftel bis zwei Fünftel so schnell wie Domänenwald",
        "Brückner estimates private woodland grows at only 20 to 40 percent of the domain forest’s rate",
    ),
    "caption": bi(
        "Geschätzter jährlicher Zuwachs je Hektar in Kubikmetern Raummaß, umgerechnet aus Klaftern je Morgen. Der Strich zeigt die Spanne, die Brückner nennt. Quelle: S. 241.",
        "Estimated annual growth per hectare in cubic meters of stacked wood, converted from Klafter per Morgen. The bar shows the range Brückner gives. Source: p. 241.",
    ),
    "vegalite": {
        "height": {"step": 56},
        "transform": [
            {"calculate": "datum.besitzart_nr == 1 ? 'kammer' : datum.besitzart_nr == 2 ? 'gemeinde' : 'privat'", "as": "besitzer"},
            {"calculate": "datum.rm_ha_von == datum.rm_ha_bis ? format(datum.rm_ha_von, '.1f') : format(datum.rm_ha_von, '.1f') + ' bis ' + format(datum.rm_ha_bis, '.1f')", "as": "label_de"},
            {"calculate": "datum.rm_ha_von == datum.rm_ha_bis ? format(datum.rm_ha_von, '.1f') : format(datum.rm_ha_von, '.1f') + ' to ' + format(datum.rm_ha_bis, '.1f')", "as": "label_en"},
        ],
        "encoding": {
            "y": {
                "field": {"de": "besitzart_de", "en": "besitzart_en"}, "type": "nominal",
                "sort": {"field": "besitzart_nr", "op": "min", "order": "ascending"},
                "axis": {"title": None, "labelLimit": 300, "labelFontSize": 12},
            },
            "color": {
                "field": "besitzer", "type": "nominal", "legend": None,
                "scale": {"domain": OWN_DOMAIN, "range": OWN_RANGE},
            },
        },
        "layer": [
            {
                "transform": [{"filter": "datum.besitzart_nr == 1"}],
                "mark": {"type": "rule", "strokeDash": [3, 3], "color": "@muted"},
                "encoding": {"x": {"field": "rm_ha_von", "type": "quantitative"}, "y": None, "color": None},
            },
            {
                "mark": {"type": "rule", "strokeWidth": 9, "strokeCap": "round"},
                "encoding": {
                    "x": {"field": "rm_ha_von", "type": "quantitative", "scale": {"domain": [0, 7]}, "axis": {"title": {"de": "Zuwachs, m³ je ha und Jahr", "en": "Growth, m³ per ha and year"}, "values": [0, 1, 2, 3, 4, 5, 6, 7], "format": "d"}},
                    "x2": {"field": "rm_ha_bis"},
                    "tooltip": [
                        {"field": {"de": "besitzart_de", "en": "besitzart_en"}, "type": "nominal", "title": bi("Besitzart", "Type of owner")},
                        {"field": "zuwachs_text", "type": "nominal", "title": bi("Zuwachs, Klafter je Morgen (gedruckt)", "Growth, Klafter per Morgen (as printed)")},
                        tooltip("rm_ha_von", "m³ je ha, untere Grenze", "m³ per ha, lower limit", ".1f"),
                        tooltip("rm_ha_bis", "m³ je ha, obere Grenze", "m³ per ha, upper limit", ".1f"),
                    ],
                },
            },
            {
                "mark": {"type": "text", "align": "left", "dx": 12, "style": "label"},
                "encoding": {
                    "x": {"field": "rm_ha_bis", "type": "quantitative"},
                    "text": {"field": {"de": "label_de", "en": "label_en"}, "type": "nominal"},
                    "color": None,
                },
            },
        ],
    },
}

datasets = [waldanteil, holzpreise, zuwachs, wald, domaene]

feature = {
    "id": ID,
    "title": bi("Wald und Holz", "Forests and timber"),
    "category": "forestry",
    "section": "t1-3-4",
    "merges": [A1, A2],
    "sources": [
        {"page": "240", "block": "b2"}, {"page": "240", "block": "b4"}, {"page": "217", "block": "b1"},
        {"page": "241", "block": "b2"}, {"page": "241", "block": "b3"}, {"page": "241", "block": "b6"}, {"page": "241", "block": "b7"},
        {"page": "832", "block": "b8"},
    ],
    "summary": summary,
    "findings": findings,
    "method": method,
    "conversions": conversions,
    "caveats": caveats,
    "transcription_issues": transcription_issues,
    "datasets": datasets,
    "charts": [c1, c2, c3],
    "keywords": {
        "de": ["Wald", "Forstwirtschaft", "Holzpreise", "Kammerforste", "Privatwald", "Nadelwald", "Laubwald", "Frankenwald", "Klafter"],
        "en": ["forest", "forestry", "timber prices", "chamber forests", "private woodland", "conifers", "deciduous woodland", "Frankenwald", "Klafter"],
    },
    "related": ["landwirtschaft", "pflanzenwelt", "bergbau", "berufe-gewerbe"],
    "generated_by": "Claude Sonnet 5.5 (Agent F5), aus 2 Einzelauswertungen zusammengeführt",
    "date": "2026-10-02",
}

if __name__ == "__main__":
    for k in ["title", "summary"]:
        for lang in ["de", "en"]:
            print(k, lang, words(feature[k][lang]))
    write_feature(feature)
    validate(ID)
