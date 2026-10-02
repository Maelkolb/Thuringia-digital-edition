"""Chart specs for the feature `staatsfinanzen`. Group totals are filled in by the build script."""


def revenue_panel(group_key, title_de, title_en, color, show_x):
    return {
        "width": 460,
        "height": {"step": 24},
        "title": {"text": {"de": title_de, "en": title_en}, "anchor": "start", "color": "@ink", "fontSize": 12.5,
                  "fontWeight": 600, "offset": 8},
        "transform": [
            {"filter": f"datum.group_key == '{group_key}'"},
            {"calculate": {"de": "datum.item_de", "en": "datum.item_en"}, "as": "item"},
            {"calculate": {
                "de": "format(datum.thaler, ',d') + ' (' + format(datum.share_pct, datum.share_pct < 1 ? '.1f' : '.0f') + ' %)'",
                "en": "format(datum.thaler, ',d') + ' (' + format(datum.share_pct, datum.share_pct < 1 ? '.1f' : '.0f') + '%)'"},
             "as": "lab"},
        ],
        "encoding": {
            "y": {"field": "item", "type": "nominal", "sort": {"field": "thaler", "order": "descending"},
                  "axis": {"title": None, "labelLimit": 380, "minExtent": 210}},
            "x": {"field": "thaler", "type": "quantitative", "scale": {"domain": [0, 150000], "nice": False},
                  "axis": ({"format": ",d", "values": [0, 25000, 50000, 75000, 100000],
                            "title": {"de": "Taler pro Jahr (veranschlagt)", "en": "Thalers per year (budgeted)"}} if show_x else None)},
        },
        "layer": [
            {"mark": {"type": "bar", "size": 14, "color": color},
             "encoding": {"tooltip": [{"field": "item", "title": {"de": "Posten", "en": "Item"}},
                                      {"field": "thaler", "title": {"de": "Taler", "en": "Thalers"}, "format": ",d"},
                                      {"field": "share_pct", "title": {"de": "Anteil an den Einnahmen (%)", "en": "Share of revenue (%)"}, "format": ".1f"}]}},
            {"mark": {"type": "text", "align": "left", "dx": 6, "style": "label"},
             "encoding": {"text": {"field": "lab"}}},
        ],
    }


def revenue_chart(ind_de, ind_en, dir_de, dir_en):
    return {
        "vconcat": [
            revenue_panel("a_ind", ind_de, ind_en, "@accent", False),
            revenue_panel("b_dir", dir_de, dir_en, "@accent2", True),
        ],
        "spacing": 26,
    }


# ------------------------------------------------------------------ c2: debt
c2 = {
    "height": 300,
    "padding": {"top": 8, "left": 4, "right": 8, "bottom": 4},
    "encoding": {
        "x": {"field": "year", "type": "ordinal",
              "scale": {"domain": [1857, 1858, 1859, 1860, 1861, 1862, 1863, 1864, 1865, 1866]},
              "axis": {"labelAngle": 0, "title": None, "format": "d"}},
        "y": {"field": "debt_thaler", "type": "quantitative", "scale": {"domain": [0, 500000]},
              "axis": {"format": ",d", "values": [0, 100000, 200000, 300000, 400000, 500000],
                       "title": {"de": "Taler", "en": "Thalers"}}},
    },
    "layer": [
        {"mark": {"type": "bar", "color": "@accent", "cornerRadiusEnd": 3},
         "encoding": {"tooltip": [{"field": "year", "title": {"de": "Jahr", "en": "Year"}, "format": "d"},
                                  {"field": "debt_thaler", "title": {"de": "Verzinsliche Schuld (Taler)", "en": "Interest-bearing debt (thalers)"}, "format": ",.0f"}]}},
        {"mark": {"type": "text", "align": "center", "dy": -8, "style": "label"},
         "encoding": {"text": {"field": "debt_thaler", "type": "quantitative", "format": ",.0f"}, "y": {"field": "debt_thaler"}}},
        # yardstick: the budgeted annual revenue (dataset `haushalt`)
        {"data": {"name": "haushalt"},
         "transform": [{"filter": "datum.side_key == 'a_einnahmen'"}, {"aggregate": [{"op": "sum", "field": "thaler", "as": "revenue"}]}],
         "mark": {"type": "rule", "strokeDash": [4, 3], "color": "@ink2", "strokeWidth": 1.3},
         "encoding": {"y": {"field": "revenue", "type": "quantitative"}, "x": None, "color": None}},
        {"data": {"name": "haushalt"},
         "transform": [{"filter": "datum.side_key == 'a_einnahmen'"}, {"aggregate": [{"op": "sum", "field": "thaler", "as": "revenue"}]}],
         "mark": {"type": "text", "align": "left", "baseline": "bottom", "dy": -6, "dx": 2, "style": "annotation"},
         "encoding": {"y": {"field": "revenue", "type": "quantitative"}, "x": {"datum": 1862, "type": "ordinal", "bandPosition": 0},
                      "text": {"value": {"de": "Veranschlagte Jahreseinnahmen", "en": "Budgeted annual revenue"}}, "color": None}},
        {"transform": [{"window": [{"op": "row_number", "as": "rn"}]}, {"filter": "datum.rn == 1"}],
         "mark": {"type": "text", "align": "center", "baseline": "middle", "style": "label-muted"},
         "encoding": {"x": {"datum": 1863, "bandPosition": 1}, "y": {"datum": 200000},
                      "text": {"value": {"de": "keine Angaben", "en": "no figures"}}}},
    ],
}

# ------------------------------------------------------------------ c3: fire insurance
c3 = {
    "height": {"step": 24},
    "padding": {"top": 22, "left": 4, "right": 8, "bottom": 4},
    "transform": [
        {"calculate": {"de": "datum.place_de", "en": "datum.place_en"}, "as": "place"},
        {"joinaggregate": [{"op": "sum", "field": "buildings_value", "as": "bv"}, {"op": "sum", "field": "buildings", "as": "bn"}],
         "groupby": ["kind_key"]},
        {"calculate": "datum.bv / datum.bn", "as": "avg"},
        {"calculate": "datum.buildings_value / datum.buildings", "as": "per_building"},
    ],
    "encoding": {
        "y": {"field": "place", "type": "nominal", "sort": {"field": "per_building", "order": "descending"},
              "axis": {"title": None, "labelLimit": 400}},
        "x": {"type": "quantitative", "scale": {"domain": [0, 2000], "nice": False},
              "axis": {"format": ",d", "values": [0, 500, 1000, 1500, 2000],
                       "title": {"de": "Versicherungssumme je Gebäude (Taler)", "en": "Insured sum per building (thalers)"}}},
        "color": {"field": "kind_key", "type": "nominal", "legend": None,
                  "scale": {"domain": ["a", "b"], "range": ["@accent", "@accent2"]}},
    },
    "layer": [
        {"transform": [{"aggregate": [{"op": "mean", "field": "avg", "as": "avg"}], "groupby": ["kind_key"]}],
         "mark": {"type": "rule", "strokeDash": [3, 3], "strokeWidth": 1.4},
         "encoding": {"x": {"field": "avg", "type": "quantitative"}, "y": None}},
        {"transform": [{"aggregate": [{"op": "mean", "field": "avg", "as": "avg"}], "groupby": ["kind_key"]},
                       {"calculate": {"de": "(datum.kind_key == 'a' ? 'Städte Ø ' : 'Land Ø ') + format(datum.avg, ',.0f')",
                                      "en": "(datum.kind_key == 'a' ? 'Towns avg. ' : 'Country avg. ') + format(datum.avg, ',.0f')"}, "as": "avg_label"}],
         "mark": {"type": "text", "style": "label", "baseline": "bottom", "dy": -5, "align": "center"},
         "encoding": {"x": {"field": "avg", "type": "quantitative"}, "y": {"value": 0}, "text": {"field": "avg_label"}}},
        {"mark": {"type": "rule", "strokeWidth": 1.6},
         "encoding": {"x": {"field": "per_building"}, "x2": {"datum": 0}, "color": {"value": "@context"}}},
        {"mark": {"type": "point", "filled": True, "size": 80},
         "encoding": {"x": {"field": "per_building"},
                      "tooltip": [{"field": "place", "title": {"de": "Ort", "en": "Place"}},
                                  {"field": "buildings", "title": {"de": "Gebäude", "en": "Buildings"}, "format": ",d"},
                                  {"field": "buildings_value", "title": {"de": "Versicherungssumme (Taler)", "en": "Insured sum (thalers)"}, "format": ",d"},
                                  {"field": "per_building", "title": {"de": "je Gebäude (Taler)", "en": "per building (thalers)"}, "format": ",.0f"}]}},
        {"mark": {"type": "text", "align": "left", "dx": 9, "fontSize": 11, "color": "@paper", "stroke": "@paper", "strokeWidth": 4},
         "encoding": {"x": {"field": "per_building", "type": "quantitative"}, "text": {"field": "per_building", "type": "quantitative", "format": ",.0f"}, "color": None}},
        {"mark": {"type": "text", "align": "left", "dx": 9, "style": "label-muted"},
         "encoding": {"x": {"field": "per_building", "type": "quantitative"}, "text": {"field": "per_building", "type": "quantitative", "format": ",.0f"}, "color": None}},
    ],
}
