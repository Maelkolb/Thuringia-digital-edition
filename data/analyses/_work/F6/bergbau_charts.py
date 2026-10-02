"""Chart specs for the feature `bergbau` (no data, only Vega-Lite)."""

c1 = {
    "height": {"step": 18},
    "transform": [
        {"calculate": "datum.fate_group == 'In Betrieb' ? 0 : (datum.fate_group == 'Aufgegeben' ? 2 : 1)", "as": "fate_rank"},
        {"calculate": "datum.fate_rank * 10000 + datum.start_year + datum.plot_end / 10000", "as": "sortkey"},
        {"calculate": "datum.fate_rank == 0 ? 'a' : (datum.fate_rank == 1 ? 'b' : 'c')", "as": "fate_cls"},
        {"calculate": {
            "de": "{'In Betrieb': 'in Betrieb', 'Aufgegeben': 'aufgegeben', 'Gerberei': 'Gerberei', 'Mühle/Ziegelei': 'Mühle oder Ziegelei', 'Textilfabrik': 'Textilfabrik'}[datum.fate_group]",
            "en": "{'In Betrieb': 'in operation', 'Aufgegeben': 'abandoned', 'Gerberei': 'tannery', 'Mühle/Ziegelei': 'mill or brickworks', 'Textilfabrik': 'textile mill'}[datum.fate_group]"},
         "as": "end_label"},
        {"calculate": {"de": "datum.note_de", "en": "datum.note_en"}, "as": "note"},
    ],
    "encoding": {
        "y": {"field": "name", "type": "nominal", "sort": {"field": "sortkey", "order": "ascending"},
              "axis": {"title": None, "labelLimit": 320}},
    },
    "layer": [
        {"mark": {"type": "bar", "size": 9, "cornerRadius": 2},
         "encoding": {
             "x": {"field": "start_year", "type": "quantitative",
                   "scale": {"domain": [1640, 1960]},
                   "axis": {"format": "d", "values": [1650, 1700, 1750, 1800, 1850], "title": None}},
             "x2": {"field": "plot_end"},
             "color": {"field": "fate_cls", "type": "nominal", "legend": None,
                       "scale": {"domain": ["a", "b", "c"], "range": ["@accent", "@accent2", "@context"]}},
             "tooltip": [
                 {"field": "name", "title": {"de": "Werk", "en": "Works"}},
                 {"field": "place", "title": {"de": "Ort", "en": "Place"}},
                 {"field": "start_year", "title": {"de": "Beginn", "en": "Start"}, "format": "d"},
                 {"field": "end_year", "title": {"de": "Ende", "en": "End"}, "format": "d"},
                 {"field": "end_label", "title": {"de": "Später", "en": "Afterwards"}},
                 {"field": "note", "title": {"de": "Brückner", "en": "Brückner"}},
             ]}},
        {"mark": {"type": "text", "align": "left", "dx": 6, "style": "label-muted"},
         "encoding": {"x": {"field": "plot_end", "type": "quantitative"}, "text": {"field": "end_label"}}},
    ],
}

c2 = {
    "height": {"step": 20},
    "padding": {"top": 20, "left": 4, "right": 8, "bottom": 4},
    "transform": [
        {"filter": "datum.region == 'Unterland'"},
        {"joinaggregate": [{"op": "min", "field": "start_plot", "as": "lane_first"}], "groupby": ["lane"]},
        {"calculate": {"de": "datum.note_de", "en": "datum.note_en"}, "as": "note"},
    ],
    "encoding": {
        "y": {"field": "lane", "type": "nominal", "sort": {"field": "lane_first", "order": "ascending"},
              "axis": {"title": None}},
        "x": {"field": "start_plot", "type": "quantitative",
              "scale": {"domain": [1540, 1760], "nice": False},
              "axis": {"format": "d", "values": [1550, 1600, 1650, 1700, 1750], "title": None}},
    },
    "layer": [
        {"transform": [{"window": [{"op": "row_number", "as": "rn"}]}, {"filter": "datum.rn == 1"}],
         "mark": {"type": "rect", "color": "@context", "opacity": 0.45},
         "encoding": {"x": {"datum": 1618}, "x2": {"datum": 1648}, "y": {"value": 0}, "y2": {"value": {"expr": "height"}}}},
        {"transform": [{"window": [{"op": "row_number", "as": "rn"}]}, {"filter": "datum.rn == 1"}],
         "mark": {"type": "text", "style": "annotation", "baseline": "bottom", "dy": -6, "align": "center"},
         "encoding": {"x": {"datum": 1633}, "y": {"value": 0},
                      "text": {"value": {"de": "Dreißigjähriger Krieg", "en": "Thirty Years’ War"}}}},
        {"transform": [{"filter": "datum.record_type == 'Zeitraum'"}],
         "mark": {"type": "rule", "strokeWidth": 8, "strokeCap": "round", "color": "@accent"},
         "encoding": {
             "x2": {"field": "end_plot"},
             "tooltip": [
                 {"field": "name", "title": {"de": "Betrieb", "en": "Enterprise"}},
                 {"field": "metal", "title": {"de": "Erz", "en": "Ore"}},
                 {"field": "start_year", "title": {"de": "von", "en": "from"}, "format": "d"},
                 {"field": "end_year", "title": {"de": "bis", "en": "to"}, "format": "d"},
                 {"field": "note", "title": {"de": "Brückner", "en": "Brückner"}}]}},
        {"transform": [{"filter": "datum.record_type == 'Einzelbeleg'"}],
         "mark": {"type": "circle", "size": 55, "color": "@accent", "opacity": 1},
         "encoding": {
             "tooltip": [
                 {"field": "name", "title": {"de": "Beleg", "en": "Record"}},
                 {"field": "metal", "title": {"de": "Erz", "en": "Ore"}},
                 {"field": "start_year", "title": {"de": "Jahr", "en": "Year"}, "format": "d"},
                 {"field": "note", "title": {"de": "Brückner", "en": "Brückner"}}]}},
    ],
}

_tip_salt = [{"field": "place", "title": {"de": "Debitstelle", "en": "Sales outlet"}},
             {"field": "ctr_1857", "title": "1857", "format": ",d"},
             {"field": "ctr_1863", "title": "1863", "format": ",d"},
             {"field": "change", "title": {"de": "Veränderung", "en": "Change"}, "format": "+,d"}]

c3 = {
    "height": {"step": 18},
    "transform": [
        {"calculate": "isValid(datum.ctr_1863) ? datum.ctr_1863 : 0", "as": "v63"},
        {"calculate": "isValid(datum.ctr_1863) ? 'a' : 'b'", "as": "kind"},
    ],
    "encoding": {
        "y": {"field": "place", "type": "nominal", "sort": {"field": "ctr_1857", "order": "descending"},
              "axis": {"title": None, "labelLimit": 220}},
        "x": {"type": "quantitative", "scale": {"domain": [0, 6200], "nice": False},
              "axis": {"format": ",d", "values": [0, 1000, 2000, 3000, 4000, 5000, 6000],
                       "title": {"de": "Kochsalz in Zentnern (Ctr.)", "en": "Table salt in hundredweight (Ctr.)"}}},
    },
    "layer": [
        {"mark": {"type": "rule", "strokeWidth": 2.5},
         "encoding": {"x": {"field": "ctr_1857"}, "x2": {"field": "v63"},
                      "color": {"field": "kind", "type": "nominal", "legend": None,
                                "scale": {"domain": ["a", "b"], "range": ["@context", "@negative"]}}}},
        {"mark": {"type": "point", "filled": True, "size": 60, "color": "@muted"},
         "encoding": {"x": {"field": "ctr_1857"}, "tooltip": _tip_salt}},
        {"transform": [{"filter": "datum.kind == 'a'"}],
         "mark": {"type": "point", "filled": True, "size": 70, "color": "@accent"},
         "encoding": {"x": {"field": "ctr_1863"}, "tooltip": _tip_salt}},
        {"transform": [{"filter": "datum.kind == 'b'"}],
         "mark": {"type": "text", "align": "left", "dx": 10, "color": "@negative", "fontWeight": 600, "fontSize": 11},
         "encoding": {"x": {"field": "ctr_1857"},
                      "text": {"value": {"de": "1863 keine Abgabe", "en": "no delivery in 1863"}}}},
        {"transform": [{"filter": "datum.place == 'Hof'"}],
         "mark": {"type": "text", "align": "left", "dx": 9, "style": "label"},
         "encoding": {"x": {"field": "ctr_1863"}, "text": {"field": "ctr_1863", "format": ",d"}}},
        {"transform": [{"filter": "datum.place == 'Gera'"}],
         "mark": {"type": "text", "align": "right", "dx": -9, "style": "annotation"},
         "encoding": {"x": {"field": "ctr_1857"}, "text": {"value": "1857"}}},
        {"transform": [{"filter": "datum.place == 'Gera'"}],
         "mark": {"type": "text", "align": "left", "dx": 9, "style": "annotation"},
         "encoding": {"x": {"field": "ctr_1863"}, "text": {"value": "1863"}}},
    ],
}
