from common import *

MERGES = [
    "bevoelkerung-natuerlicher-zuwachs-1858-1867",
    "bevoelkerung-geburten-1858-1867",
    "bevoelkerung-sterblichkeit-1858-1867",
    "bevoelkerung-uneheliche-geburten-1858-1867",
    "bevoelkerung-todtgeborene-1858-1867",
    "bevoelkerung-geburtensaldo-wanderung-1859-1867",
    "bevoelkerung-eheschliessungen-1858-1867",
    "bevoelkerung-sterblichkeit-lobenstein-1794-1804",
    "gesundheit-selbstmord-unglueck-1858-1867",
]

vital = dataset("bevoelkerung-natuerlicher-zuwachs-1858-1867", "vital")
illegit_mean = dataset("bevoelkerung-uneheliche-geburten-1858-1867", "illegit_mean")
periods = dataset("bevoelkerung-geburtensaldo-wanderung-1859-1867", "periods")
illegit = dataset("bevoelkerung-uneheliche-geburten-1858-1867", "illegit")
marriages_mean = dataset("bevoelkerung-eheschliessungen-1858-1867", "marriages_mean")

# ---------------------------------------------------------------- numbers
V = rows_of(vital)
fs = [r for r in V if r["district"] == "Reuß j. L."]
births = sum(r["births"] for r in fs)
deaths = sum(r["deaths"] for r in fs)
still = sum(r["stillborn"] for r in fs)
surplus = births - deaths
assert surplus == sum(r["balance"] for r in fs)
live_surplus = surplus - still
low = min(fs, key=lambda r: r["balance"])
high = max(fs, key=lambda r: r["balance"])
peak_deaths = max(fs, key=lambda r: r["deaths"])
assert low["year"] == 1865 and peak_deaths["year"] == 1865
assert all(r["balance"] > 0 for r in V)
years = len(fs)
M = {r["district"] + "|" + r["area"]: r for r in rows_of(marriages_mean)}
marr_year = M["Reuß j. L.|Zusammen"]["pairs"]

IM = {r["district"] + "|" + r["area"]: r["illegit_pct"] for r in rows_of(illegit_mean)}
il_all = IM["Reuß j. L.|Zusammen"]
il_lob = IM["Lobenstein-Ebersdorf|Zusammen"]
il_sch = IM["Schleiz|Zusammen"]
il_ger = IM["Gera|Zusammen"]
IL = {(r["year"], r["district"], r["area"]): r["illegit_pct"] for r in rows_of(illegit)}
il_1858 = IL[(1858, "Reuß j. L.", "Zusammen")]
il_1867 = IL[(1867, "Reuß j. L.", "Zusammen")]
for d in ["Gera", "Schleiz", "Lobenstein-Ebersdorf", "Reuß j. L."]:
    assert IM[d + "|Landorte"] > IM[d + "|Städte"]

P = rows_of(periods)
agg = {}
for r in P:
    a = agg.setdefault(r["district"], {"nat": 0, "inc": 0, "mig": 0})
    a["nat"] += r["natural_increase"]
    a["inc"] += r["increase"]
    a["mig"] += r["net_migration"]
for a in agg.values():
    assert a["nat"] - a["inc"] == -a["mig"]
mig_total = -agg["Fürstentum"]["mig"]
share_lost = mig_total / agg["Fürstentum"]["nat"] * 100

n = lambda x, d=0: pair(x, d)
log = []


def say(label, v):
    log.append((label, v))


say("births", births); say("deaths", deaths); say("still", still); say("surplus", surplus)
say("live_surplus", live_surplus); say("low", (low["year"], low["balance"])); say("high", (high["year"], high["balance"]))
say("peak_deaths", peak_deaths["deaths"]); say("marr_year", marr_year)
say("il", (il_all, il_lob, il_sch, il_ger, il_1858, il_1867))
say("agg", agg); say("share_lost", share_lost)

# ---------------------------------------------------------------- charts
YEARS = list(range(1858, 1868))

c1 = {
    "height": 330,
    "transform": [{"filter": "datum.district === 'Reuß j. L.'"}],
    "encoding": {
        "x": {"field": "year", "type": "quantitative", "scale": {"domain": [1858, 1867], "nice": False},
              "axis": {"format": "d", "values": YEARS, "title": None}},
    },
    "layer": [
        {"mark": {"type": "area", "color": "@accent", "opacity": 0.16, "line": False},
         "encoding": {
             "y": {"field": "births", "type": "quantitative", "scale": {"domain": [1800, 3800]},
                   "axis": {"title": {"de": "Personen im Jahr", "en": "Persons per year"}, "format": ",d", "values": [2000, 2500, 3000, 3500]}},
             "y2": {"field": "deaths"}}},
        {"mark": {"type": "line", "color": "@accent", "strokeWidth": 2.5},
         "encoding": {"y": {"field": "births", "type": "quantitative"}}},
        {"mark": {"type": "line", "color": "@accent2", "strokeWidth": 2.5},
         "encoding": {"y": {"field": "deaths", "type": "quantitative"}}},
        {"mark": {"type": "point", "filled": True, "size": 46, "color": "@accent"},
         "encoding": {"y": {"field": "births", "type": "quantitative"},
                      "tooltip": [tooltip("year", "Jahr", "Year", "d"), tooltip("births", "Geborene", "Births", ",d"),
                                  tooltip("stillborn", "darunter Totgeborene", "of these stillborn", ",d"),
                                  tooltip("deaths", "Gestorbene", "Deaths", ",d"), tooltip("balance", "Überschuss", "Surplus", ",d")]}},
        {"mark": {"type": "point", "filled": True, "size": 46, "color": "@accent2"},
         "encoding": {"y": {"field": "deaths", "type": "quantitative"},
                      "tooltip": [tooltip("year", "Jahr", "Year", "d"), tooltip("births", "Geborene", "Births", ",d"),
                                  tooltip("deaths", "Gestorbene", "Deaths", ",d"), tooltip("balance", "Überschuss", "Surplus", ",d")]}},
        # direct labels at the start of the lines
        {"transform": [{"filter": "datum.year == 1858"}],
         "mark": {"type": "text", "style": "label", "align": "left", "dy": -24, "color": "@accent"},
         "encoding": {"y": {"field": "births", "type": "quantitative"},
                      "text": {"value": {"de": "Geborene", "en": "Births"}}}},
        {"transform": [{"filter": "datum.year == 1858"}],
         "mark": {"type": "text", "style": "label", "align": "left", "dy": 27, "color": "@accent2"},
         "encoding": {"y": {"field": "deaths", "type": "quantitative"},
                      "text": {"value": {"de": "Gestorbene", "en": "Deaths"}}}},
        # surplus brackets at the largest and smallest gap
        {"transform": [{"filter": "datum.year == 1860 || datum.year == 1865"}],
         "mark": {"type": "rule", "color": "@ink2", "strokeWidth": 1.5},
         "encoding": {"y": {"field": "births", "type": "quantitative"}, "y2": {"field": "deaths"}}},
        {"transform": [{"filter": "datum.year == 1860 || datum.year == 1865"},
                       {"calculate": "(datum.births + datum.deaths) / 2", "as": "mid"},
                       {"calculate": "'+' + format(datum.balance, ',d')", "as": "lab"}],
         "mark": {"type": "text", "style": "label", "align": "left", "dx": 7, "color": "@ink"},
         "encoding": {"y": {"field": "mid", "type": "quantitative"}, "text": {"field": "lab"}}},
        {"transform": [{"filter": "datum.year == 1862"},
                       {"calculate": "(datum.births + datum.deaths) / 2", "as": "mid"}],
         "mark": {"type": "text", "style": "annotation", "align": "center", "color": "@accent"},
         "encoding": {"y": {"field": "mid", "type": "quantitative"},
                      "text": {"value": {"de": "Überschuss der Geborenen", "en": "surplus of births"}}}},
        {"transform": [{"filter": "datum.year == 1865"},
                       {"calculate": {"de": "'Höchststand ' + format(datum.deaths, ',d')", "en": "'peak ' + format(datum.deaths, ',d')"}, "as": "dlab"}],
         "mark": {"type": "text", "style": "label", "align": "right", "dx": -9, "dy": -10, "color": "@accent2"},
         "encoding": {"y": {"field": "deaths", "type": "quantitative"}, "text": {"field": "dlab"}}},
    ],
}

SORT3 = ["Lobenstein-Ebersdorf", "Schleiz", "Gera", "Reuß j. L."]
DISTRICT_LABEL = "datum.value == 'Reuß j. L.' ? '" + "{FS}" + "' : datum.value"


def district_axis(order, title=None):
    return {"field": "district", "type": "nominal", "sort": order,
            "axis": {"title": title, "labelLimit": 220,
                     "labelExpr": {"de": DISTRICT_LABEL.replace("{FS}", "Fürstentum"), "en": DISTRICT_LABEL.replace("{FS}", "Principality")},
                     "labelFontWeight": {"condition": {"test": "datum.value == 'Reuß j. L.'", "value": 700}, "value": 400}}}


c2 = {
    "height": {"step": 56},
    "transform": [
        {"filter": "datum.area === 'Städte' || datum.area === 'Landorte'"},
        {"pivot": "area", "value": "illegit_pct", "groupby": ["district"]},
    ],
    "encoding": {
        "y": district_axis(SORT3),
    },
    "layer": [
        {"mark": {"type": "rule", "color": "@context", "strokeWidth": 3},
         "encoding": {"x": {"field": "Städte", "type": "quantitative", "scale": {"domain": [10, 28]},
                            "axis": {"values": [10, 15, 20, 25], "title": {"de": "Uneheliche Geburten in Prozent aller Geburten", "en": "Illegitimate births as a percentage of all births"}}},
                      "x2": {"field": "Landorte"}}},
        {"mark": {"type": "point", "filled": True, "size": 110, "color": "@muted"},
         "encoding": {"x": {"field": "Städte", "type": "quantitative"},
                      "tooltip": [tooltip("district", "Bezirk", "District"),
                                  tooltip("Städte", "Städte, Prozent", "Towns, percent", ".2f"),
                                  tooltip("Landorte", "Landorte, Prozent", "Villages, percent", ".2f")]}},
        {"mark": {"type": "point", "filled": True, "size": 130, "color": "@accent"},
         "encoding": {"x": {"field": "Landorte", "type": "quantitative"},
                      "tooltip": [tooltip("district", "Bezirk", "District"),
                                  tooltip("Städte", "Städte, Prozent", "Towns, percent", ".2f"),
                                  tooltip("Landorte", "Landorte, Prozent", "Villages, percent", ".2f")]}},
        {"mark": {"type": "text", "style": "label-muted", "align": "right", "dx": -11},
         "encoding": {"x": {"field": "Städte", "type": "quantitative"}, "text": {"field": "Städte", "format": ".1f"}}},
        {"mark": {"type": "text", "style": "label", "align": "left", "dx": 12, "color": "@accent"},
         "encoding": {"x": {"field": "Landorte", "type": "quantitative"}, "text": {"field": "Landorte", "format": ".1f"}}},
        {"transform": [{"filter": "datum.district === 'Lobenstein-Ebersdorf'"}],
         "mark": {"type": "text", "style": "label-muted", "align": "center", "dy": -17},
         "encoding": {"x": {"field": "Städte", "type": "quantitative"},
                      "text": {"value": {"de": "Städte", "en": "Towns"}}}},
        {"transform": [{"filter": "datum.district === 'Lobenstein-Ebersdorf'"}],
         "mark": {"type": "text", "style": "label", "align": "center", "dy": -17, "color": "@accent"},
         "encoding": {"x": {"field": "Landorte", "type": "quantitative"},
                      "text": {"value": {"de": "Landorte", "en": "Villages"}}}},
    ],
}

ORDER3 = ["Gera", "Schleiz", "Lobenstein-Ebersdorf", "Fürstentum"]
TT3 = [tooltip("district", "Bezirk", "District"), tooltip("nat", "Geburtenüberschuss", "Surplus of births", ",d"),
       tooltip("inc", "Zunahme der Bevölkerung", "Population increase", ",d"), tooltip("mig", "Wanderungssaldo", "Net migration", ",d")]
SIGN = {"condition": {"test": "datum.mig >= 0", "value": "@positive"}, "value": "@negative"}
c3 = {
    "height": {"step": 60},
    "transform": [
        {"aggregate": [{"op": "sum", "field": "natural_increase", "as": "nat"},
                       {"op": "sum", "field": "increase", "as": "inc"}], "groupby": ["district"]},
        {"calculate": "datum.inc - datum.nat", "as": "mig"},
        {"calculate": "(datum.mig >= 0 ? '+' : '−') + format(abs(datum.mig), ',d')", "as": "miglab"},
        {"calculate": "(datum.nat + datum.inc) / 2", "as": "midx"},
    ],
    "encoding": {
        "y": {"field": "district", "type": "nominal", "sort": ORDER3,
              "axis": {"title": None, "labelLimit": 220,
                       "labelExpr": {"de": "datum.value", "en": "datum.value == 'Fürstentum' ? 'Principality' : datum.value"},
                       "labelFontWeight": {"condition": {"test": "datum.value == 'Fürstentum'", "value": 700}, "value": 400}}},
    },
    "layer": [
        {"mark": {"type": "rule", "strokeWidth": 4},
         "encoding": {"x": {"field": "nat", "type": "quantitative", "scale": {"domain": [-1500, 10800]},
                            "axis": {"values": [0, 2000, 4000, 6000, 8000, 10000], "format": ",d",
                                     "title": {"de": "Personen, 1859 bis 1867 zusammen", "en": "Persons, 1859 to 1867 combined"}}},
                      "x2": {"field": "inc"}, "color": SIGN}},
        {"mark": {"type": "point", "filled": True, "size": 120, "color": "@muted"},
         "encoding": {"x": {"field": "nat", "type": "quantitative"}, "tooltip": TT3}},
        {"mark": {"type": "point", "filled": True, "size": 150, "color": "@accent"},
         "encoding": {"x": {"field": "inc", "type": "quantitative"}, "tooltip": TT3}},
        # value labels on the outer side of each dot
        {"transform": [{"filter": "datum.nat >= datum.inc"}],
         "mark": {"type": "text", "style": "label-muted", "align": "left", "dx": 12},
         "encoding": {"x": {"field": "nat", "type": "quantitative"}, "text": {"field": "nat", "format": ",d"}}},
        {"transform": [{"filter": "datum.nat < datum.inc"}],
         "mark": {"type": "text", "style": "label-muted", "align": "right", "dx": -12},
         "encoding": {"x": {"field": "nat", "type": "quantitative"}, "text": {"field": "nat", "format": ",d"}}},
        {"transform": [{"filter": "datum.nat >= datum.inc"}],
         "mark": {"type": "text", "style": "label", "align": "right", "dx": -12, "color": "@accent"},
         "encoding": {"x": {"field": "inc", "type": "quantitative"}, "text": {"field": "inc", "format": ",d"}}},
        {"transform": [{"filter": "datum.nat < datum.inc"}],
         "mark": {"type": "text", "style": "label", "align": "left", "dx": 12, "color": "@accent"},
         "encoding": {"x": {"field": "inc", "type": "quantitative"}, "text": {"field": "inc", "format": ",d"}}},
        {"mark": {"type": "text", "style": "label", "align": "center", "dy": -15},
         "encoding": {"x": {"field": "midx", "type": "quantitative"}, "text": {"field": "miglab"}, "color": SIGN}},
        {"transform": [{"filter": "datum.district === 'Fürstentum'"}],
         "mark": {"type": "text", "style": "label-muted", "align": "center", "dy": 19},
         "encoding": {"x": {"field": "nat", "type": "quantitative"},
                      "text": {"value": {"de": "Geburtenüberschuss", "en": "surplus of births"}}}},
        {"transform": [{"filter": "datum.district === 'Fürstentum'"}],
         "mark": {"type": "text", "style": "label", "align": "center", "dy": 19, "color": "@accent"},
         "encoding": {"x": {"field": "inc", "type": "quantitative"},
                      "text": {"value": {"de": "Zunahme", "en": "increase"}}}},
    ],
}

# ---------------------------------------------------------------- texts
b, d_, s_, sur = n(births), n(deaths), n(still), n(surplus)
lowb = n(low["balance"])
pk = n(peak_deaths["deaths"])
hi = n(high["balance"])
lost = n(mig_total)
natf = n(agg["Fürstentum"]["nat"])
incf = n(agg["Fürstentum"]["inc"])
lob_nat = agg["Lobenstein-Ebersdorf"]["nat"]
lob_mig = -agg["Lobenstein-Ebersdorf"]["mig"]
lob_inc = agg["Lobenstein-Ebersdorf"]["inc"]
ger_mig = agg["Gera"]["mig"]
sch_mig = -agg["Schleiz"]["mig"]

title = bi("Geburten, Ehen, Sterbefälle und Wanderung 1858–1867", "Births, marriages, deaths and migration, 1858–1867")
summary = bi(
    f"Brückner verzeichnet für 1858 bis 1867 im Durchschnitt {n(births / years)[0]} Geburten, {n(deaths / years)[0]} Sterbefälle und {n(marr_year)[0]} Trauungen im Jahr. "
    f"Der Geburtenüberschuss von {sur[0]} Personen war in jedem Jahr positiv. Fast jedes fünfte Kind kam unehelich zur Welt, in Lobenstein-Ebersdorf fast jedes vierte. "
    f"Die Zählungen ergaben {incf[0]} Einwohner mehr; den Rest führt Brückner auf Wanderung zurück.",
    f"For 1858 to 1867 Brückner records on average {n(births / years)[1]} births, {n(deaths / years)[1]} deaths and {n(marr_year)[1]} marriages a year. "
    f"The surplus of births, {sur[1]} persons, was positive in every year. Almost one child in five was born out of wedlock, in Lobenstein-Ebersdorf almost one in four. "
    f"The censuses show {incf[1]} more inhabitants; Brückner ascribes the rest to migration.",
)
findings = [
    bi(f"1858 bis 1867 wurden {b[0]} Kinder geboren, darunter {s_[0]} tot, und {d_[0]} Menschen starben. Der Überschuss war 1865 mit {lowb[0]} am kleinsten, 1860 mit {hi[0]} am größten.",
       f"Between 1858 and 1867, {b[1]} children were born, {s_[1]} of them stillborn, and {d_[1]} people died. The surplus was smallest in 1865 ({lowb[1]}) and largest in 1860 ({hi[1]})."),
    bi(f"Im gedruckten Zehnjahresmittel waren {n(il_all, 1)[0]} Prozent der Geborenen unehelich: {n(il_lob, 1)[0]} in Lobenstein-Ebersdorf, {n(il_sch, 1)[0]} in Schleiz, {n(il_ger, 1)[0]} in Gera. Der Anteil sank von {n(il_1858, 1)[0]} (1858) auf {n(il_1867, 1)[0]} Prozent (1867).",
       f"In the printed ten-year mean {n(il_all, 1)[1]} percent of births were illegitimate: {n(il_lob, 1)[1]} in Lobenstein-Ebersdorf, {n(il_sch, 1)[1]} in Schleiz, {n(il_ger, 1)[1]} in Gera. The share fell from {n(il_1858, 1)[1]} (1858) to {n(il_1867, 1)[1]} percent (1867)."),
    bi(f"Dem Geburtenüberschuss von {natf[0]} (1859 bis 1867) stand eine Zunahme von nur {incf[0]} gegenüber; {lost[0]} Personen ({n(share_lost)[0]} Prozent) gingen durch Wanderung verloren, {n(lob_mig)[0]} davon in Lobenstein-Ebersdorf.",
       f"The surplus of births ({natf[1]}, 1859 to 1867) was matched by an increase of only {incf[1]}; {lost[1]} persons ({n(share_lost)[1]} percent) were lost through migration, {n(lob_mig)[1]} of them in Lobenstein-Ebersdorf."),
]

charts = [
    {"id": "c1", "dataset": "vital",
     "title": bi(f"Jedes Jahr wurden mehr Kinder geboren als Menschen starben, 1865 nur {lowb[0]} mehr",
                 f"In every year more children were born than people died, in 1865 only {lowb[1]} more"),
     "caption": bi("Geborene (einschließlich Totgeborener) und Gestorbene im Fürstentum 1858 bis 1867; die Fläche dazwischen ist der Überschuss der Geborenen. Quelle: S. 107, 111, 114.",
                   "Births (including stillbirths) and deaths in the principality, 1858 to 1867; the area between the lines is the surplus of births. Source: pp. 107, 111, 114."),
     "vegalite": c1},
    {"id": "c2", "dataset": "illegit_mean",
     "title": bi("Uneheliche Kinder waren auf dem Land häufiger als in den Städten, am häufigsten in Lobenstein-Ebersdorf",
                 "Illegitimate births were more common in villages than in towns, most of all in Lobenstein-Ebersdorf"),
     "caption": bi("Uneheliche Geborene in Prozent aller Geborenen, gedrucktes Mittel 1858 bis 1867, getrennt nach Städten und Landorten. Quelle: S. 109.",
                   "Illegitimate births as a percentage of all births, printed mean 1858 to 1867, towns and villages shown separately. Source: p. 109."),
     "vegalite": c2},
    {"id": "c3", "dataset": "periods",
     "title": bi("Gera gewann Einwohner durch Zuwanderung; Lobenstein-Ebersdorf verlor mehr, als der Geburtenüberschuss einbrachte",
                 "Gera gained inhabitants through migration; Lobenstein-Ebersdorf lost more than its surplus of births added"),
     "caption": bi("Geburtenüberschuss (grau) und tatsächliche Zunahme der Bevölkerung (blau) 1859 bis 1867, Summe der drei Dreijahreszeiträume. Die Differenz ist Brückners Wanderungssaldo, ein Restwert. Quelle: S. 98 f.",
                   "Surplus of births (grey) and actual population increase (blue), 1859 to 1867, sum of the three three-year periods. The difference is Brückner’s migration balance, a residual. Source: pp. 98 f."),
     "vegalite": c3},
]

# ---------------------------------------------------------------- assemble
datasets = [vital, illegit_mean, periods, illegit, marriages_mean]
datasets[3]["title"] = bi("Uneheliche Geburten nach Jahr, Bezirk, Städten und Landorten", "Illegitimate births by year, district, towns and villages")


def refs_pages(dss):
    out, seen = [], set()
    for ds in dss:
        for r in ds["source_refs"]:
            k = (r["page"], r["block"])
            if k not in seen:
                seen.add(k)
                out.append({"page": r["page"], "block": r["block"]})
    return out


sources = refs_pages(datasets)

issues = []
for aid in MERGES:
    for t in archive(aid).get("transcription_issues", []):
        issues.append(t)

feature = {
    "id": "geburten-sterbefaelle",
    "title": title,
    "category": "population",
    "section": "t1-2-1",
    "merges": MERGES,
    "sources": sources,
    "summary": summary,
    "findings": findings,
    "method": bi(
        "Übernommen wurden Brückners Jahrestabellen: Geborene (S. 107), Totgeborene (S. 111) und Gestorbene (S. 114) je Landratsbezirk, die unehelichen Geburten (S. 109), die Trauungen (S. 112) sowie die Dreijahresbilanz von Geburtenüberschuss, Zunahme und Wanderung (S. 98 f.). "
        "Berechnet wurden der Überschuss (Geborene minus Gestorbene, so wie Brückner ihn auf S. 98 f. bildet) und im dritten Diagramm die Summen der drei gedruckten Dreijahreswerte. Der Wanderungssaldo ist Brückners Restwert: Geburtenüberschuss minus Zunahme der Bevölkerung zwischen zwei Zählungen. "
        "Die Zehnjahresmittel für Städte und Landorte sind die von Brückner gedruckten Mittelzeilen. Die Jahreszahlen des ersten Diagramms folgen S. 107 und S. 114; für Lobenstein-Ebersdorf 1866 nennt S. 98 abweichend 922 statt 925 Geborene, die Dreijahressummen im dritten Diagramm stützen sich auf S. 98 f. "
        "Nicht verwendet wurden die Tabellen zu Totgeborenen, Geschlecht der Geborenen, Staatenvergleichen, Selbstmorden und Unglücksfällen sowie die Reihe für den Bezirk Lobenstein-Ebersdorf 1794 bis 1804; sie sind in den Einzelauswertungen erhalten.",
        "Brückner’s annual tables were used: births (p. 107), stillbirths (p. 111) and deaths (p. 114) for each district, illegitimate births (p. 109), marriages (p. 112), and the three-year balance of surplus, increase and migration (pp. 98 f.). "
        "Computed are the surplus (births minus deaths, as Brückner forms it on pp. 98 f.) and, in the third chart, the sums of the three printed three-year values. The migration balance is Brückner’s residual: surplus of births minus the increase of the population between two censuses. "
        "The ten-year means for towns and villages are the mean rows printed by Brückner. The annual figures of the first chart follow pp. 107 and 114; for Lobenstein-Ebersdorf in 1866 p. 98 gives 922 instead of 925 births, and the three-year sums in the third chart rest on pp. 98 f. "
        "Not used are the tables on stillbirths, the sex of newborns, comparisons between states, suicides and accidents, and the series for the district of Lobenstein-Ebersdorf for 1794 to 1804; they are preserved in the earlier single analyses."),
    "caveats": [
        bi("Brückners Zahlen sind nicht überall stimmig: Für Schleiz 1865 setzen die Prozentzahlen etwa 1136 statt der gedruckten 1064 Geborenen voraus; für Lobenstein-Ebersdorf 1866 nennen S. 98 und S. 107 922 und 925 Geborene. Alle Werte stehen wie gedruckt im Datensatz.",
           "Brückner’s figures are not consistent everywhere: for Schleiz in 1865 the percentages imply about 1136 births instead of the printed 1064; for Lobenstein-Ebersdorf in 1866 pp. 98 and 107 give 922 and 925 births. All values are given as printed in the dataset."),
        bi("Der Wanderungssaldo ist ein Restwert und enthält alle Zähl- und Registrierungsfehler sowie Unterschiede zwischen Wohn- und anwesender Bevölkerung. Er ist keine Auswanderungsstatistik; die gemeldeten Auswanderer von 1867 (S. 118) erklären nur einen Teil.",
           "The migration balance is a residual and contains all counting and registration errors as well as differences between resident and present population. It is not emigration statistics; the emigrants reported for 1867 (p. 118) explain only part of it."),
        bi("Brückner nennt keine Todesursachen und keinen Grund für die hohe Sterblichkeit 1865. Ob die Gestorbenen die Totgeborenen mitzählen, sagt er nicht; falls nicht, wäre der Überschuss um die " + s_[0] + " Totgeborenen zu groß.",
           "Brückner names no causes of death and no reason for the high mortality of 1865. He does not say whether the deaths include stillbirths; if not, the surplus would be too large by the " + s_[1] + " stillborn."),
        bi("Uneheliche Geburten: Die Anteile für Schleiz und das Fürstentum 1865 passen nicht zu den Geburtenzahlen (sie setzen etwa 1136 bzw. 3585 Geborene voraus), und für Lobenstein-Ebersdorf 1865 ergeben die gedruckten Anteile 101 Prozent. Die Mittel für Städte und Landorte beruhen auf kleinen Fallzahlen.",
           "Illegitimate births: the shares for Schleiz and the principality in 1865 do not fit the birth figures (they imply about 1136 and 3585 births), and for Lobenstein-Ebersdorf in 1865 the printed shares add up to 101 percent. The means for towns and villages rest on small numbers."),
    ],
    "datasets": datasets,
    "charts": charts,
    "transcription_issues": issues,
    "keywords": {
        "de": ["Geburten", "Sterbefälle", "Gestorbene", "Geburtenüberschuss", "uneheliche Geburten", "Eheschließungen", "Wanderung", "Auswanderung", "Bevölkerungsbewegung"],
        "en": ["births", "deaths", "surplus of births", "illegitimate births", "marriages", "migration", "emigration", "vital statistics"],
    },
    "related": ["bevoelkerung-1647-1867", "alter-familie", "gesundheit", "haus-reuss"],
    "generated_by": "Claude Sonnet 5.5 (Agent F4), aus 9 Einzelauswertungen zusammengeführt",
    "date": "2026-10-02",
}

if __name__ == "__main__":
    check_limits(feature)
    write_feature(feature)
    with open("C:/Users/totom/Projects/reuss-edition/data/analyses/_work/F4/check_geburten.txt", "w", encoding="utf-8") as f:
        for k, v in log:
            f.write(f"{k}: {v}\n")
