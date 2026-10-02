"""Feature gewaesser (agent F1): merges gewaesser-hauptfluesse-lauf-gefaelle, gewaesser-quellen-muendungen-hoehen,
gewaesser-nebenfluesse-verzeichnis, gewaesser-heilquellen-lobenstein-analyse."""
import collections
from common import *

a_haupt = load("gewaesser-hauptfluesse-lauf-gefaelle")
a_hoehe = load("gewaesser-quellen-muendungen-hoehen")
a_zufl = load("gewaesser-nebenfluesse-verzeichnis")
a_heil = load("gewaesser-heilquellen-lobenstein-analyse")

reaches_ds = ds_of(a_hoehe, "reaches")
points_ds = json.loads(json.dumps(ds_of(a_hoehe, "points")))
for row in points_ds["rows"]:
    if row[0] == "Wioschwitz (zur Selbitz)":      # print: "Moschwitz" (checked in the facsimile)
        row[0] = "Moschwitz (zur Selbitz)"
rivers_ds = ds_of(a_haupt, "rivers")
trib_ds = ds_of(a_zufl, "tributaries")
comp_ds = ds_of(a_heil, "composition")
prop = rows_as_dicts(ds_of(a_heil, "properties"))

# ------------------------------------------------------------------ numbers
reaches = rows_as_dicts(reaches_ds)
points = rows_as_dicts(points_ds)
rivers = {r["river"]: r for r in rows_as_dicts(rivers_ds)}
trib = rows_as_dicts(trib_ds)
comp = rows_as_dicts(comp_ds)

n_streams = len({p["stream"] for p in points})
r_ = {r["stream"]: r for r in reaches}
wettera, sieglitz, elster = r_["Wettera"], r_["Sieglitzbach"], r_["Elster"]
print("streams", n_streams, "reaches", len(reaches), "Wettera", wettera["fall_m"], "Sieglitz", sieglitz["fall_m"], "Elster", elster["fall_m"])
fall_o = {r["stream"]: r["fall_m"] for r in reaches}
src_o = [p["height_m"] for p in points if p["point_type"] == "source" and p["region"] == "Oberland"]
src_u = [p["height_m"] for p in points if p["point_type"] == "source" and p["region"] == "Unterland"]
print("Oberland sources", len(src_o), min(src_o), max(src_o), "Unterland", len(src_u), min(src_u), max(src_u))

n_trib = len(trib)
by_river = collections.Counter(t["river"] for t in trib)
bank = collections.Counter((t["river"], t["bank"]) for t in trib)
print("tributaries", n_trib, dict(by_river), {k: v for k, v in bank.items()})
right_more = [rv for rv in ("Saale", "Elster", "Weida", "Rodach") if bank[(rv, "rechts")] > bank[(rv, "links")]]
assert right_more == ["Saale", "Elster", "Weida"]
ober = [t for t in trib if t["region"] == "Oberland"]
unter = [t for t in trib if t["region"] == "Unterland"]
bach_o = sum(t["name_type"] == "bach" for t in ober)
bach_u = sum(t["name_type"] == "bach" for t in unter)
gg_u = sum(t["name_type"] in ("graben", "grund") for t in unter)
gg_o = sum(t["name_type"] in ("graben", "grund") for t in ober)
print("names Oberland", len(ober), "bach", bach_o, "Unterland", len(unter), "bach", bach_u, "graben/grund", gg_u, gg_o)

tot = collections.defaultdict(float)
grp = collections.defaultdict(float)
for c in comp:
    tot[c["spring"]] += c["parts_per_10000"]
    grp[(c["group"], c["spring"])] += c["parts_per_10000"]
printed = {p["spring"]: p["solids_total"] for p in prop}
assert all(abs(tot[k] - printed[k]) < 1e-9 for k in printed), (tot, printed)
ratio_total = tot["Neue Quelle"] / tot["Agnesquelle"]
iron_nq, iron_aq = grp[("iron", "Neue Quelle")], grp[("iron", "Agnesquelle")]
ratio_iron = iron_nq / iron_aq
fe_nq = next(c["parts_per_10000"] for c in comp if c["order"] == 9 and c["spring"] == "Neue Quelle")
fe_aq = next(c["parts_per_10000"] for c in comp if c["order"] == 9 and c["spring"] == "Agnesquelle")
share_fe_aq = fe_aq / tot["Agnesquelle"] * 100
largest_aq = max((c for c in comp if c["spring"] == "Agnesquelle"), key=lambda c: c["parts_per_10000"])
assert largest_aq["order"] == 9
print("totals", dict(tot), "ratio", ratio_total, "iron group", iron_nq, iron_aq, ratio_iron, "Fe only", fe_nq, fe_aq, fe_nq / fe_aq, "share Fe AQ", share_fe_aq)
for k in ("Neue Quelle", "Agnesquelle"):
    print(k, {g: round(grp[(g, k)], 4) for g in ("earth", "iron", "alkali", "other")})

sin = {k: v["sinuosity"] for k, v in rivers.items()}
fps = {k: v["fall_per_stunde_ft"] for k, v in rivers.items()}
print("sinuosity", sin, "fall per Stunde", fps, "fall m", {k: v["fall_m"] for k, v in rivers.items()})

# ------------------------------------------------------------------ charts
OBER, UNTER = "@accent2", "@accent"
MAIN = "['Saale','Weida','Elster']"
FOCUS = "['Wettera','Sieglitzbach','Elster']"

c1 = {
    "height": {"step": 25},
    "transform": [{"calculate": "format(datum.fall_m, '.0f') + ' m'", "as": "fall_label"}],
    "encoding": {"y": {"field": "stream", "type": "nominal", "sort": {"field": "upper_m", "op": "max", "order": "descending"},
                       "axis": {"title": None, "labelLimit": 300,
                                "labelFontWeight": {"condition": {"test": f"indexof({MAIN}, datum.value) >= 0", "value": 700}, "value": 400}}}},
    "layer": [
        {"mark": {"type": "bar", "cornerRadius": 3, "height": {"band": 0.6}},
         "encoding": {"x": {"field": "lower_m", "type": "quantitative", "scale": {"domain": [150, 720]},
                            "axis": {"title": {"de": "Höhe über dem Meer in m", "en": "Altitude above sea level in m"}, "values": [200, 300, 400, 500, 600], "format": "d"}},
                      "x2": {"field": "upper_m"},
                      "color": {"field": "region", "type": "nominal", "legend": None, "scale": {"domain": ["Oberland", "Unterland"], "range": [OBER, UNTER]}},
                      "tooltip": tooltip(("stream", "Gewässer", "Watercourse"), ("region", "Gebiet (Brückners Gliederung)", "Region (Brückner’s division)"),
                                         ("upper_ft", "obere Höhe (Dezimalfuß)", "upper height (decimal feet)", ",.1~f"),
                                         ("lower_ft", "untere Höhe (Dezimalfuß)", "lower height (decimal feet)", ",.1~f"),
                                         ("upper_m", "obere Höhe (m)", "upper height (m)", ".0f"), ("lower_m", "untere Höhe (m)", "lower height (m)", ".0f"),
                                         ("fall_m", "Gefälle (m)", "fall (m)", ".0f"))}},
        {"transform": [{"filter": f"indexof({FOCUS}, datum.stream) >= 0"}],
         "mark": {"type": "text", "style": "label", "align": "left", "dx": 7},
         "encoding": {"x": {"field": "upper_m", "type": "quantitative"}, "text": {"field": "fall_label"}}},
        {"transform": [{"filter": f"indexof({FOCUS}, datum.stream) < 0"}],
         "mark": {"type": "text", "style": "label-muted", "align": "left", "dx": 7},
         "encoding": {"x": {"field": "upper_m", "type": "quantitative"}, "text": {"field": "fall_label"}}},
        {"transform": [{"filter": "datum.stream == 'Weida'"}],
         "mark": {"type": "text", "style": "label", "align": "right", "color": OBER},
         "encoding": {"x": {"datum": 300, "type": "quantitative"}, "text": {"value": {"de": "Oberland", "en": "Oberland"}}}},
        {"transform": [{"filter": "datum.stream == 'Brambach'"}],
         "mark": {"type": "text", "style": "label", "align": "left", "color": UNTER},
         "encoding": {"x": {"datum": 450, "type": "quantitative"}, "text": {"value": {"de": "Unterland", "en": "Unterland"}}}},
    ],
}

c2 = {
    "height": {"step": 40},
    "padding": {"top": 26, "left": 4, "right": 4, "bottom": 4},
    "transform": [{"aggregate": [{"op": "count", "as": "n"}], "groupby": ["river", "bank"]},
                  {"calculate": "datum.bank == 'links' ? -datum.n : datum.n", "as": "signed"}],
    "encoding": {"y": {"field": "river", "type": "nominal", "sort": {"field": "n", "op": "sum", "order": "descending"},
                       "axis": {"title": None, "labelFontWeight": 600, "labelFontSize": 12, "labelPadding": 8}}},
    "layer": [
        {"mark": {"type": "bar", "cornerRadius": 3, "height": {"band": 0.62}},
         "encoding": {"x": {"field": "signed", "type": "quantitative", "scale": {"domain": [-27, 27]},
                            "axis": {"title": {"de": "Zahl der Zuflüsse erster Ordnung", "en": "Number of first-order tributaries"},
                                     "values": [-20, -10, 0, 10, 20], "labelExpr": "abs(datum.value)", "grid": True}},
                      "color": {"condition": {"test": "datum.bank == 'rechts'", "value": "@accent"}, "value": "@context"},
                      "tooltip": tooltip(("river", "Fluss", "River"), ("bank", "Ufer", "Bank"), ("n", "Zuflüsse", "Tributaries"))}},
        {"mark": {"type": "text", "style": "label", "baseline": "middle", "align": {"expr": "datum.signed < 0 ? 'right' : 'left'"}, "dx": {"expr": "datum.signed < 0 ? -6 : 6"}},
         "encoding": {"x": {"field": "signed", "type": "quantitative"}, "text": {"field": "n", "type": "quantitative"}}},
        {"data": {"name": "tributaries"}, "transform": [{"aggregate": [{"op": "count", "as": "k"}]}],
         "mark": {"type": "text", "style": "label-muted", "align": "right", "baseline": "bottom", "dx": -4, "dy": -8},
         "encoding": {"x": {"datum": 0, "type": "quantitative"}, "y": {"value": 0}, "text": {"value": {"de": "← linkes Ufer", "en": "← left bank"}}}},
        {"data": {"name": "tributaries"}, "transform": [{"aggregate": [{"op": "count", "as": "k"}]}],
         "mark": {"type": "text", "style": "label", "align": "left", "baseline": "bottom", "dx": 4, "dy": -8, "color": "@accent"},
         "encoding": {"x": {"datum": 0, "type": "quantitative"}, "y": {"value": 0}, "text": {"value": {"de": "rechtes Ufer →", "en": "right bank →"}}}},
    ],
}

GROUP_LABEL = {"de": "datum.group == 'earth' ? 'Kalk und Magnesia' : datum.group == 'iron' ? 'Eisen und Mangan' : datum.group == 'alkali' ? 'Natron- und Kalisalze' : 'Übrige Stoffe'",
               "en": "datum.group == 'earth' ? 'Lime and magnesia' : datum.group == 'iron' ? 'Iron and manganese' : datum.group == 'alkali' ? 'Sodium and potassium salts' : 'Other constituents'"}
SPRING = {"field": "spring", "type": "nominal", "legend": None, "scale": {"domain": ["Neue Quelle", "Agnesquelle"], "range": ["@accent", "@accent2"]}}
c3 = {
    "height": {"step": 48},
    "transform": [{"aggregate": [{"op": "sum", "field": "parts_per_10000", "as": "v"}], "groupby": ["group", "spring"]},
                  {"calculate": GROUP_LABEL, "as": "group_label"},
                  {"joinaggregate": [{"op": "min", "field": "v", "as": "lo"}, {"op": "max", "field": "v", "as": "hi"}], "groupby": ["group"]}],
    "encoding": {"y": {"field": "group_label", "type": "nominal", "sort": {"field": "hi", "op": "max", "order": "descending"},
                       "axis": {"title": None, "labelLimit": 260, "labelPadding": 8}}},
    "layer": [
        {"mark": {"type": "rule", "strokeWidth": 3, "color": "@context"},
         "encoding": {"x": {"field": "lo", "type": "quantitative", "scale": {"domain": [-0.14, 1.4]},
                            "axis": {"title": {"de": "Gelöste Stoffe, Teile in 10 000 Teilen Wasser", "en": "Dissolved matter, parts in 10,000 parts of water"},
                                     "values": [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4], "format": ".1f"}},
                      "x2": {"field": "hi"}}},
        {"mark": {"type": "point", "filled": True, "size": 190, "opacity": 1},
         "encoding": {"x": {"field": "v", "type": "quantitative"}, "color": SPRING,
                      "tooltip": tooltip(("group_label", "Stoffgruppe", "Group of constituents"), ("spring", "Quelle", "Spring"),
                                         ("v", "Teile in 10 000 Teilen Wasser", "Parts in 10,000 parts of water", ".4f"))}},
        {"transform": [{"filter": "datum.spring == 'Neue Quelle'"}],
         "mark": {"type": "text", "style": "label", "align": "left", "dx": 11},
         "encoding": {"x": {"field": "v", "type": "quantitative"}, "text": {"field": "v", "type": "quantitative", "format": ".2f"}}},
        {"transform": [{"filter": "datum.spring == 'Agnesquelle'"}],
         "mark": {"type": "text", "style": "label", "align": "right", "dx": -11},
         "encoding": {"x": {"field": "v", "type": "quantitative"}, "text": {"field": "v", "type": "quantitative", "format": ".2f"}}},
        {"transform": [{"filter": "datum.group == 'earth'"}],
         "mark": {"type": "text", "style": "label", "align": "center", "dy": -17},
         "encoding": {"x": {"field": "v", "type": "quantitative"}, "color": SPRING, "text": {"field": "spring"}}},
    ],
}

# ------------------------------------------------------------------ texts
lead_de = (f"Brückner gliedert das Gewässernetz in vier Flusssysteme, zählt {n_trib} Zuflüsse erster Ordnung auf und gibt für {n_streams} Bäche und Flüsse Höhen an. Die Saale fällt im Land "
           f"{de(rivers['Saale']['fall_m'], 0)} m, die Weida {de(rivers['Weida']['fall_m'], 0)} m, die Elster nur {de(rivers['Elster']['fall_m'], 0)} m. Für die 1868 eröffnete "
           f"Badeanstalt in Lobenstein druckt er die Analyse von zwei Eisenquellen.")
lead_en = (f"Brückner divides the drainage network into four river systems, lists {n_trib} first-order tributaries and gives heights for {n_streams} streams and rivers. The Saale falls "
           f"{en(rivers['Saale']['fall_m'], 0)} m within the country, the Weida {en(rivers['Weida']['fall_m'], 0)} m, the Elster only {en(rivers['Elster']['fall_m'], 0)} m. For the spa "
           f"opened at Lobenstein in 1868 he prints the analysis of two iron springs.")
f1_de = (f"Die Saale legt im Land das {de(sin['Saale'], 2)}fache der Luftlinie zurück, die Weida das {de(sin['Weida'], 2)}fache, die Elster das {de(sin['Elster'], 2)}fache. "
         f"Je Stunde Lauf fällt die Weida mit {de(fps['Weida'], 0)} Fuß am stärksten, die Elster mit {de(fps['Elster'], 0)} am schwächsten.")
f1_en = (f"Within the country the Saale covers {en(sin['Saale'], 2)} times its straight-line distance, the Weida {en(sin['Weida'], 2)} times, the Elster {en(sin['Elster'], 2)} times. "
         f"Per Stunde of course the Weida falls most ({en(fps['Weida'], 0)} feet), the Elster least ({en(fps['Elster'], 0)}).")
f2_de = (f"Im Oberland enden {de(bach_o / len(ober) * 100, 0)} Prozent der {len(ober)} Zuflussnamen auf -bach, im Unterland {de(bach_u / len(unter) * 100, 0)} Prozent von {len(unter)}. "
         f"Namen auf -graben oder -grund tragen {gg_u} Zuflüsse im Unterland, im Oberland keiner.")
f2_en = (f"In the Oberland {en(bach_o / len(ober) * 100, 0)} percent of {len(ober)} tributary names end in -bach, in the Unterland {en(bach_u / len(unter) * 100, 0)} percent of {len(unter)}. "
         f"Names in -graben or -grund occur for {gg_u} Unterland tributaries, for none in the Oberland.")
assert gg_o == 0
f3_de = (f"Die Neue Quelle enthält {de(tot['Neue Quelle'], 2)} Teile feste Stoffe in 10.000 Teilen Wasser, die Agnesquelle {de(tot['Agnesquelle'], 2)}. In der Agnesquelle ist Eisen "
         f"der größte Einzelbestandteil ({de(share_fe_aq, 0)} Prozent).")
f3_en = (f"The Neue Quelle contains {en(tot['Neue Quelle'], 2)} parts of solids in 10,000 parts of water, the Agnesquelle {en(tot['Agnesquelle'], 2)}. In the Agnesquelle iron "
         f"is the largest single constituent ({en(share_fe_aq, 0)} percent).")

title1_de = (f"Wettera und Sieglitzbach fallen über 200 m, die Elster im ganzen Land nur {de(elster['fall_m'], 0)} m")
title1_en = (f"The Wettera and Sieglitzbach fall over 200 m, the Elster only {en(elster['fall_m'], 0)} m across the country")
assert wettera["fall_m"] > 200 and sieglitz["fall_m"] > 200
cap1_de = ("Höhe in Metern (aus Dezimalfuß umgerechnet) am oberen und unteren Ende der Strecken, die Brückner angibt: meist Quelle bis Mündung, bei Saale, Weida, Elster, "
           "Leuba und Triebes Eintritt bis Austritt, bei vier Bächen Teilstrecken. Zahl: Gefälle. Quelle: S. 45 bis 53.")
cap1_en = ("Altitude in meters (converted from decimal feet) at the upper and lower end of the reaches Brückner gives: mostly spring to mouth, for the Saale, Weida, Elster, "
           "Leuba and Triebes entry to exit, for four streams partial reaches. Number: fall. Source: pp. 45 to 53.")
title2_de = "Bei Saale, Elster und Weida münden rechts mehr Zuflüsse als links"
title2_en = "On the Saale, Elster and Weida more tributaries join on the right than on the left"
cap2_de = (f"Von Brückner einzeln aufgeführte Zuflüsse erster Ordnung nach Fluss und Ufer, in Flussrichtung gesehen; insgesamt {n_trib}. "
           f"Nur an der Rodach überwiegt das linke Ufer. Quelle: S. 45 bis 53.")
cap2_en = (f"First-order tributaries listed individually by Brückner, by river and bank, seen in the direction of flow; {n_trib} in all. "
           f"Only on the Rodach does the left bank prevail. Source: pp. 45 to 53.")
title3_de = f"Die Neue Quelle ist {de(ratio_total, 1)}-mal so stark mineralisiert, hat aber nur {de(ratio_iron, 1)}-mal so viel Eisen"
title3_en = f"The Neue Quelle is {en(ratio_total, 1)} times as mineralized but has only {en(ratio_iron, 1)} times as much iron"
cap3_de = ("Analyse von Prof. Reichardt (Jena) für die 1868 eröffnete Badeanstalt in Lobenstein: Bestandteile in vier Gruppen, in Teilen auf 10.000 Teile Wasser. "
           "Die Salze sind die damals berechneten Verbindungen. Quelle: S. 44.")
cap3_en = ("Analysis by Prof. Reichardt (Jena) for the spa opened at Lobenstein in 1868: constituents in four groups, in parts per 10,000 parts of water. "
           "The salts are the compounds computed at the time. Source: p. 44.")

for k, v in (("lead", lead_de), ("f1", f1_de), ("f2", f2_de), ("f3", f3_de), ("t1", title1_de), ("cap1", cap1_de), ("t2", title2_de), ("cap2", cap2_de),
             ("t3", title3_de), ("cap3", cap3_de), ("t1en", title1_en), ("t2en", title2_en), ("t3en", title3_en)):
    print(f"[{words(v)}] {k}: {v}")

method_de = (
    "Die Längen und Höhen stammen aus den Gewässerbeschreibungen auf S. 45 bis 53, die Analyse der Eisenquellen aus der Tabelle auf S. 44. Alle Höhen sind preußische "
    "Dezimalfuß, auf den Pegel bei Swinemünde bezogen (S. 11 Anm.), und wurden mit 0,3766242 m je Fuß in Meter umgerechnet. Aufgenommen sind nur Höhen, die sich eindeutig "
    "einem Punkt eines Gewässers zuordnen lassen; Spannenangaben und Höhen nicht benannter Zuflüsse fehlen. Das Gefälle ist die Differenz zwischen oberer und unterer Höhe "
    "einer Strecke; bei Flüssen, die das Land durchqueren, gilt es zwischen Eintritt und Austritt. Die Gebiete folgen Brückners Gliederung (die Weida steht beim Oberland). "
    "Die Zuflüsse wurden aus den durchnummerierten Listen gezählt; die Nummerierung läuft bei jedem Fluss und Ufer lückenlos. Der Namenstyp ist nach dem Wortausgang "
    "editorisch zugeordnet. Bei der Analyse sind die 14 Bestandteile Reichardts zu vier Gruppen zusammengefasst (Natron und Kali; Kalk und Magnesia; Eisen und Mangan; übrige); "
    "ihre Summen ergeben genau die gedruckten Gesamtwerte 2,5232 und 1,0082.")
method_en = (
    "The lengths and heights come from the descriptions of the watercourses on pp. 45 to 53, the analysis of the iron springs from the table on p. 44. All heights are Prussian "
    "decimal feet referred to the Swinemünde gauge (p. 11 note) and were converted to meters at 0.3766242 m per foot. Only heights that can be assigned unambiguously to one "
    "point of a watercourse are included; range statements and heights of unnamed tributaries are missing. The fall is the difference between the upper and lower height of a "
    "reach; for rivers crossing the country it applies between entry and exit. The regions follow Brückner’s division (the Weida is listed under the Oberland). The "
    "tributaries were counted from the numbered lists; the numbering runs without gaps on every river and bank. The name type is assigned editorially from the ending. For the "
    "analysis Reichardt’s 14 constituents are combined into four groups (sodium and potassium; lime and magnesia; iron and manganese; other); their sums add up exactly to "
    "the printed totals 2.5232 and 1.0082.")
assert words(method_de) <= 260 and words(method_en) <= 260, (words(method_de), words(method_en))

caveats = [
    {"de": "Brückner erklärt die Längeneinheit Stunde nicht; vermutlich ist es eine Wegstunde. Windungsverhältnis und Gefälle je Stunde hängen davon nicht ab, Kilometerwerte lassen sich aus dem Text nicht belegen. Die Länge der Saale ist als »über 11 Stunden« gedruckt und hier als 11 gerechnet.",
     "en": "Brückner does not explain the unit Stunde; presumably it is a walking hour. Sinuosity and fall per Stunde do not depend on it, but kilometer values cannot be derived from the text. The length of the Saale is printed as “over 11 Stunden” and is taken here as 11."},
    {"de": "Höhen sind nur für 28 von rund 300 Gewässern angegeben und ungleich verteilt: viele Bäche im Oberland, wenige im Unterland. Die Strecken beginnen und enden nicht überall an Quelle und Mündung. Alle drei Hauptflüsse entspringen außerhalb des Landes, ihre Werte gelten nur für die Strecke im reußischen Gebiet.",
     "en": "Heights are given for only 28 of about 300 watercourses and are unevenly distributed: many streams in the Oberland, few in the Unterland. The reaches do not everywhere start and end at spring and mouth. All three main rivers rise outside the country; their values apply only to the stretch in Reuss territory."},
    {"de": "Die Listen führen nur Zuflüsse erster Ordnung als eigene Einträge, Brückners Gesamtzahl von 300 Quellrieseln, Bächen und Flüssen ist deshalb viel höher. Die Aussage über die Namen beruht auf den Hauptnamen der Einträge; die Einteilung nach dem Wortausgang ist grob.",
     "en": "The lists give only first-order tributaries as separate entries, so Brückner’s total of 300 spring rills, brooks and rivers is far higher. The statement about the names rests on the main names of the entries; the classification by ending is rough."},
    {"de": "Die Salze der Analyse sind rechnerische Verbindungen der damals nachgewiesenen Bestandteile, keine tatsächlich gelösten Stoffe; ein Vergleich mit heutigen Mineralwasseranalysen verlangt eine Umrechnung. Die freie Kohlensäure (336,93 und 235,0 C. C.) steht ohne Bezugsmenge im Druck und ist nicht gezeichnet.",
     "en": "The salts in the analysis are computed combinations of the constituents detected at the time, not compounds actually dissolved; comparison with modern mineral-water analyses requires a conversion. The free carbonic acid (336.93 and 235.0 C. C.) is printed without a reference quantity and is not plotted."},
]
for c in caveats:
    assert words(c["de"]) <= 60 and words(c["en"]) <= 60, (words(c["de"]), words(c["en"]))

sources = []
for a_ in (a_haupt, a_hoehe, a_heil):
    for s_ in a_["sources"]:
        if s_ not in sources:
            sources.append(s_)
sources += [{"page": "45", "block": "b9", "note": "Zuflusslisten S. 45 bis 53 (erster Eintrag)"}, {"page": "53", "block": "b8", "note": "Zuflusslisten S. 45 bis 53 (letzter Eintrag)"}]
print("sources", len(sources))

conversions = a_haupt["conversions"]
feature = {
    "id": "gewaesser",
    "title": T("Flüsse, Quellen und Heilquellen", "Rivers, springs and mineral springs"),
    "category": "hydrology",
    "section": "t1-1-6",
    "merges": ["gewaesser-hauptfluesse-lauf-gefaelle", "gewaesser-quellen-muendungen-hoehen", "gewaesser-nebenfluesse-verzeichnis", "gewaesser-heilquellen-lobenstein-analyse"],
    "sources": sources,
    "summary": T(lead_de, lead_en),
    "findings": [T(f1_de, f1_en), T(f2_de, f2_en), T(f3_de, f3_en)],
    "method": T(method_de, method_en),
    "conversions": conversions,
    "caveats": caveats,
    "transcription_issues": [
        {"page": "48", "block": "b4", "transcribed": "Wioschwitz", "facsimile": "Moschwitz", "checked_facsimile": True,
         "note": "Name des Zuflusses der Selbitz (Quelle 1647′ am Südwestfuß des Kulm); die Zahl stimmt. Im Datensatz nach dem Faksimile korrigiert."},
        {"page": "47", "block": "b4", "transcribed": "Wettera (Wetterau, Bittera, Wetterbach)", "facsimile": "Wettera (Wetterau, Wittera, Wetterbach)", "checked_facsimile": True,
         "note": "Nebenname im Text; Quelle 1646′ und Mündung 945′ stimmen."},
    ],
    "datasets": [reaches_ds, trib_ds, comp_ds, rivers_ds, points_ds],
    "charts": [
        {"id": "c1", "dataset": "reaches", "title": T(title1_de, title1_en), "caption": T(cap1_de, cap1_en), "vegalite": c1},
        {"id": "c2", "dataset": "tributaries", "title": T(title2_de, title2_en), "caption": T(cap2_de, cap2_en), "vegalite": c2},
        {"id": "c3", "dataset": "composition", "title": T(title3_de, title3_en), "caption": T(cap3_de, cap3_en), "vegalite": c3},
    ],
    "keywords": {
        "de": ["Gewässer", "Saale", "Weiße Elster", "Weida", "Quellen", "Gefälle", "Zuflüsse", "Heilquellen", "Lobenstein", "Eisenquelle", "Mineralwasser"],
        "en": ["watercourses", "Saale", "White Elster", "Weida", "springs", "gradient", "tributaries", "mineral springs", "Lobenstein", "iron spring", "mineral water"],
    },
    "related": ["relief-hoehen", "land-lage-grenzen", "geologie-boden", "klima-stationen"],
    "generated_by": "Claude Sonnet 5.5 (Agent F1), aus 4 Einzelauswertungen zusammengeführt",
    "date": "2026-10-02",
}
dump(feature)
if "--no-validate" not in sys.argv:
    validate("gewaesser")
