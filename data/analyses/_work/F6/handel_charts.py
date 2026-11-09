"""Chart specs for the feature `handel-verkehr`."""

# ------------------------------------------------------------------ c1: Begleitscheine (index 1858 = 100)
c1 = {
    "height": 320,
    "padding": {"top": 22, "left": 4, "right": 8, "bottom": 4},
    "transform": [
        {"aggregate": [{"op": "sum", "field": "count", "as": "n"}], "groupby": ["region", "year"]},
        {"window": [{"op": "first_value", "field": "n", "as": "base"}], "groupby": ["region"],
         "sort": [{"field": "year"}], "frame": [None, None]},
        {"calculate": "datum.n / datum.base * 100", "as": "index"},
        {"calculate": {
            "de": "(datum.region == 'Unterland' ? 'Unterland (Amt Gera) ' : 'Oberland ') + format(datum.index - 100, '+.0f') + ' %'",
            "en": "(datum.region == 'Unterland' ? 'Unterland (Gera office) ' : 'Oberland ') + format(datum.index - 100, '+.0f') + ' %'"},
         "as": "endlabel"},
    ],
    "encoding": {
        "x": {"field": "year", "type": "quantitative",
              "scale": {"domain": [1858, 1867], "nice": False},
              "axis": {"format": "d", "values": [1858, 1859, 1860, 1861, 1862, 1863, 1864, 1865, 1866, 1867], "labelExpr": "datum.value % 2 == 0 ? format(datum.value, 'd') : ''", "labelOverlap": False, "title": None}},
        "y": {"field": "index", "type": "quantitative", "scale": {"domain": [0, 240]},
              "axis": {"values": [0, 50, 100, 150, 200],
                       "title": {"de": "Erledigte Begleitscheine, 1858 = 100", "en": "Customs transit documents processed, 1858 = 100"}}},
        "color": {"field": "region", "type": "nominal", "legend": None,
                  "scale": {"domain": ["Unterland", "Oberland"], "range": ["@accent", "@accent2"]}},
    },
    "layer": [
        {"mark": {"type": "rule", "strokeDash": [3, 3], "color": "@muted"}, "encoding": {"y": {"datum": 100}, "x": None, "color": None}},
        {"data": {"name": "ereignisse"},
         "transform": [{"filter": "datum.kind == 'Eisenbahn' && isValid(datum.date_end)"},
                       {"calculate": "toNumber(substring(datum.date_end, 0, 4))", "as": "yr"}],
         "mark": {"type": "rule", "strokeDash": [2, 3], "color": "@muted"},
         "encoding": {"x": {"field": "yr", "type": "quantitative"},
                      "y": {"value": 0}, "y2": {"value": {"expr": "height"}}, "color": None}},
        {"data": {"name": "ereignisse"},
         "transform": [{"filter": "datum.kind == 'Eisenbahn' && isValid(datum.date_end)"},
                       {"calculate": "toNumber(substring(datum.date_end, 0, 4))", "as": "yr"},
                       {"calculate": {"de": "'Bahn ' + datum.yr", "en": "'Railway ' + datum.yr"}, "as": "evt"}],
         "mark": {"type": "text", "style": "annotation", "align": "center", "baseline": "bottom", "dy": -4},
         "encoding": {"x": {"field": "yr", "type": "quantitative"}, "y": {"value": 0},
                      "text": {"field": "evt"}, "color": None}},
        {"mark": {"type": "line", "strokeWidth": 2.5}},
        {"mark": {"type": "point", "filled": True, "size": 36},
         "encoding": {"tooltip": [
             {"field": "region", "title": {"de": "Landesteil", "en": "Region"}},
             {"field": "year", "title": {"de": "Jahr", "en": "Year"}, "format": "d"},
             {"field": "n", "title": {"de": "Begleitscheine", "en": "Documents"}, "format": ",d"},
             {"field": "index", "title": "1858 = 100", "format": ".0f"}]}},
        {"transform": [{"filter": "datum.year == 1867 && datum.region == 'Unterland'"}],
         "mark": {"type": "text", "align": "right", "dy": -12, "style": "label"},
         "encoding": {"text": {"field": "endlabel"}, "color": None}},
        {"transform": [{"filter": "datum.year == 1867 && datum.region == 'Oberland'"}],
         "mark": {"type": "text", "align": "right", "baseline": "top", "dy": 10, "style": "label"},
         "encoding": {"text": {"field": "endlabel"}, "color": None}},
    ],
}

# ------------------------------------------------------------------ c2: markets on a map
_xy = {"longitude": {"field": "lon", "type": "quantitative"}, "latitude": {"field": "lat", "type": "quantitative"}}
_agg = [{"aggregate": [{"op": "sum", "field": "count", "as": "n"}], "groupby": ["place", "district", "lon", "lat"]}]
_label_text = {"calculate": "datum.place + ' ' + datum.n", "as": "lab"}


def _labels(places, align, dx, dy, style):
    cond = "indexof(%s, datum.place) >= 0" % repr(places)
    return {"transform": _agg + [{"filter": cond}, _label_text],
            "mark": {"type": "text", "style": style, "align": align, "dx": dx, "dy": dy},
            "encoding": {**_xy, "text": {"field": "lab"}}}


c2 = {
    "height": 540,
    "padding": {"top": 4, "left": 18, "right": 8, "bottom": 4},
    "projection": {"type": "mercator"},
    "layer": [
        {"data": {"name": "fluesse_basis"},
         "mark": {"type": "line", "color": "@river", "strokeWidth": 1.2},
         "encoding": {**_xy, "detail": {"field": "abschnitt"}, "order": {"field": "folge"}}},
        {"data": {"name": "orte_basis"},
         "mark": {"type": "circle", "size": 10, "color": "@land"},
         "encoding": _xy},
        {"transform": _agg,
         "mark": {"type": "circle", "stroke": "@paper", "strokeWidth": 0.8, "opacity": 0.85},
         "encoding": {**_xy,
                      "size": {"field": "n", "type": "quantitative",
                               "scale": {"type": "sqrt", "domain": [0, 14], "range": [0, 1000]},
                               "legend": {"title": {"de": "Märkte im Jahr", "en": "Markets per year"},
                                          "values": [1, 5, 10, 14], "orient": "top-left", "direction": "vertical",
                                          "symbolFillColor": "@muted", "symbolStrokeColor": "@paper"}},
                      "color": {"field": "district", "type": "nominal",
                                "scale": {"domain": ["Gera", "Schleiz", "Lobenstein-Ebersdorf"], "range": ["@accent", "@accent2", "@accent3"]},
                                "legend": {"title": None, "orient": "top-left", "direction": "vertical", "labelLimit": 300}},
                      "tooltip": [{"field": "place", "title": {"de": "Marktort", "en": "Market town"}},
                                  {"field": "district", "title": {"de": "Landesteil", "en": "District"}},
                                  {"field": "n", "title": {"de": "Märkte im Jahr", "en": "Markets per year"}}]}},
    ],
}
# place labels: (places, side, offset); the offset grows with the bubble radius
_LABELS = [
    (["Wurzbach"], "center", 0, 27), (["Ruppersdorf"], "right", -18, 0), (["Thimmendorf"], "right", -14, 0),
    (["Titschendorf"], "left", 14, 0), (["Ebersdorf", "Schleiz"], "left", 19, 0), (["Lobenstein", "Gera"], "left", 17, 0),
    (["Tanna"], "left", 15, 0), (["Hirschberg"], "left", 14, 0), (["Hohenleuben"], "center", 0, -17), (["Saalburg"], "center", 0, -15),
]
for _style in ("place-halo", "place-label"):
    for _pl, _al, _dx, _dy in _LABELS:
        c2["layer"].append(_labels(_pl, _al, _dx, _dy, _style))

# ------------------------------------------------------------------ c3: railways, banks, law (timeline)
_NUM_START = "toNumber(substring(datum.date_start, 0, 4)) + (length(datum.date_start) > 4 ? (toNumber(substring(datum.date_start, 5, 7)) - 1) / 12 + (toNumber(substring(datum.date_start, 8, 10)) - 1) / 365 : 0)"
_NUM_END = "isValid(datum.date_end) ? toNumber(substring(datum.date_end, 0, 4)) + (toNumber(substring(datum.date_end, 5, 7)) - 1) / 12 + (toNumber(substring(datum.date_end, 8, 10)) - 1) / 365 : null"
_TOOLTIP = [{"field": "name", "title": {"de": "Einrichtung", "en": "Institution"}},
            {"field": "date_start", "title": {"de": "Datum bzw. Vertrag", "en": "Date or treaty"}},
            {"field": "date_end", "title": {"de": "Eröffnung", "en": "Opened"}},
            {"field": "note", "title": {"de": "Brückner", "en": "Brückner"}}]
_LATE = "datum.t0 >= 1854"

c3 = {
    "height": {"step": 26},
    "padding": {"top": 6, "left": 4, "right": 8, "bottom": 4},
    "transform": [
        {"calculate": _NUM_START, "as": "t0"},
        {"calculate": _NUM_END, "as": "t1"},
        {"calculate": "isValid(datum.t1) ? datum.t1 : datum.t0", "as": "t_last"},
        {"calculate": {"de": "datum.name_de", "en": "datum.name_en"}, "as": "name"},
        {"calculate": {"de": "datum.note_de", "en": "datum.note_en"}, "as": "note"},
    ],
    "encoding": {
        "y": {"field": "name", "type": "nominal", "sort": {"field": "t0", "order": "ascending"}, "axis": None},
        "x": {"field": "t0", "type": "quantitative", "scale": {"domain": [1840, 1870], "nice": False},
              "axis": {"format": "d", "values": [1840, 1845, 1850, 1855, 1860, 1865, 1870], "grid": True, "title": None}},
        "color": {"field": "kind", "type": "nominal", "legend": None,
                  "scale": {"domain": ["Eisenbahn", "Geldinstitut", "Recht und Verwaltung"], "range": ["@accent", "@accent2", "@muted"]}},
    },
    "layer": [
        {"transform": [{"filter": "isValid(datum.t1)"}],
         "mark": {"type": "rule", "strokeWidth": 2},
         "encoding": {"x2": {"field": "t1"}}},
        {"transform": [{"filter": "datum.kind == 'Eisenbahn'"}],
         "mark": {"type": "point", "filled": False, "fill": "@paper", "size": 70, "strokeWidth": 2, "opacity": 1},
         "encoding": {"tooltip": _TOOLTIP}},
        {"transform": [{"filter": "datum.kind != 'Eisenbahn' || isValid(datum.t1)"}],
         "mark": {"type": "circle", "size": 80, "opacity": 1},
         "encoding": {"x": {"field": "t_last"}, "tooltip": _TOOLTIP}},
        {"transform": [{"filter": _LATE}],
         "mark": {"type": "text", "align": "right", "dx": -10, "style": "annotation"},
         "encoding": {"text": {"field": "name"}, "color": None}},
        {"transform": [{"filter": "!(" + _LATE + ")"}],
         "mark": {"type": "text", "align": "left", "dx": 10, "style": "annotation"},
         "encoding": {"x": {"field": "t_last"}, "text": {"field": "name"}, "color": None}},
        {"transform": [{"filter": "isValid(datum.t1)"}, {"calculate": "substring(datum.date_end, 0, 4)", "as": "opened"}],
         "mark": {"type": "text", "align": "left", "dx": 10, "style": "label"},
         "encoding": {"x": {"field": "t1"}, "text": {"field": "opened"}, "color": None}},
    ],
}
