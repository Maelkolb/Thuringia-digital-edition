"""Chart specs for the feature `staatsfinanzen`."""

GROUP_ORDER = "(datum.group_de == 'Indirekte Steuern' ? 1 : 2)"
HEADERS = "['Indirekte Steuern', 'Direkte Steuern', 'Indirect taxes', 'Direct taxes']"


def revenue_chart(total_revenue):
    group_share = f"format(datum.thaler / {total_revenue} * 100, '.0f')"
    return {
        "height": {"step": 24},
        "transform": [
            {"calculate": {"de": "datum.item_de", "en": "datum.item_en"}, "as": "row"},
            {"calculate": GROUP_ORDER + " * 1000000 - datum.thaler", "as": "ord"},
            {"calculate": {
                "de": "format(datum.thaler, ',d') + ' (' + format(datum.share_pct, datum.share_pct < 1 ? '.1f' : '.0f') + ' %)'",
                "en": "format(datum.thaler, ',d') + ' (' + format(datum.share_pct, datum.share_pct < 1 ? '.1f' : '.0f') + '%)'"},
             "as": "lab"},
        ],
        "encoding": {
            "y": {"field": "row", "type": "nominal", "sort": {"field": "ord", "op": "min", "order": "ascending"},
                  "axis": {"title": None, "labelLimit": 400,
                           "labelFontWeight": {"condition": {"test": f"indexof({HEADERS}, datum.value) >= 0", "value": 600}, "value": 400},
                           "labelColor": {"condition": {"test": f"indexof({HEADERS}, datum.value) >= 0", "value": "@ink"}, "value": "@ink2"}}},
            "x": {"field": "thaler", "type": "quantitative",
                  "scale": {"domainMin": 0, "domainMax": {"expr": "max(150000, 98000 * width / max(width - 92, 60))"}, "nice": False},
                  "axis": {"format": ",d", "values": [0, 25000, 50000, 75000, 100000, 125000, 150000],
                           "title": {"de": "Taler pro Jahr (veranschlagt)", "en": "Thalers per year (budgeted)"}}},
        },
        "layer": [
            {"transform": [
                {"aggregate": [{"op": "sum", "field": "thaler", "as": "thaler"}], "groupby": ["group_de", "group_en"]},
                {"calculate": {"de": "datum.group_de", "en": "datum.group_en"}, "as": "row"},
                {"calculate": GROUP_ORDER + " * 1000000 - 900000", "as": "ord"},
                {"calculate": {"de": "format(datum.thaler, ',d') + ' Taler (' + " + group_share + " + ' %)'",
                               "en": "format(datum.thaler, ',d') + ' thalers (' + " + group_share + " + '%)'"}, "as": "lab"},
            ],
             "mark": {"type": "text", "align": "left", "style": "label"},
             "encoding": {"x": {"datum": 0}, "text": {"field": "lab"}}},
            {"mark": {"type": "bar", "height": 14},
             "encoding": {"color": {"field": "group_de", "type": "nominal", "legend": None,
                                    "scale": {"domain": ["Indirekte Steuern", "Direkte Steuern"], "range": ["@accent", "@accent2"]}},
                          "tooltip": [{"field": "row", "title": {"de": "Posten", "en": "Item"}},
                                      {"field": "thaler", "title": {"de": "Taler", "en": "Thalers"}, "format": ",d"},
                                      {"field": "share_pct", "title": {"de": "Anteil an den Einnahmen (%)", "en": "Share of revenue (%)"}, "format": ".1f"}]}},
            {"mark": {"type": "text", "align": "left", "dx": 6, "style": "label"},
             "encoding": {"text": {"field": "lab"}}},
        ],
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
        {"mark": {"type": "bar", "color": "@accent", "cornerRadiusEnd": 3, "width": {"band": 0.62}},
         "encoding": {"tooltip": [{"field": "year", "title": {"de": "Jahr", "en": "Year"}, "format": "d"},
                                  {"field": "debt_thaler", "title": {"de": "Verzinsliche Schuld (Taler)", "en": "Interest-bearing debt (thalers)"}, "format": ",.0f"}]}},
        {"transform": [{"filter": "indexof([1857, 1861, 1866], datum.year) >= 0"}],
         "mark": {"type": "text", "align": "center", "dy": -8, "style": "label"},
         "encoding": {"text": {"field": "debt_thaler", "type": "quantitative", "format": ",.0f"}, "y": {"field": "debt_thaler"}}},
        # yardstick: the budgeted annual revenue (dataset `haushalt`)
        {"data": {"name": "haushalt"},
         "transform": [{"filter": "datum.side_de == 'Einnahmen'"}, {"aggregate": [{"op": "sum", "field": "thaler", "as": "revenue"}]}],
         "mark": {"type": "rule", "strokeDash": [4, 3], "color": "@ink2", "strokeWidth": 1.3},
         "encoding": {"y": {"field": "revenue", "type": "quantitative"}, "x": None, "color": None}},
        {"data": {"name": "haushalt"},
         "transform": [{"filter": "datum.side_de == 'Einnahmen'"}, {"aggregate": [{"op": "sum", "field": "thaler", "as": "revenue"}]}],
         "mark": {"type": "text", "align": "left", "baseline": "bottom", "dy": -21, "dx": 2, "lineBreak": "|", "style": "annotation"},
         "encoding": {"y": {"field": "revenue", "type": "quantitative"}, "x": {"datum": 1862, "type": "ordinal", "bandPosition": 0},
                      "text": {"value": {"de": "Veranschlagte|Jahreseinnahmen", "en": "Budgeted|annual revenue"}}, "color": None}},
        {"transform": [{"window": [{"op": "row_number", "as": "rn"}]}, {"filter": "datum.rn == 1"}],
         "mark": {"type": "text", "align": "center", "baseline": "middle", "style": "label-muted"},
         "encoding": {"x": {"datum": 1863, "bandPosition": 1}, "y": {"datum": 200000},
                      "text": {"value": {"de": "keine Angaben", "en": "no figures"}}}},
    ],
}

# ------------------------------------------------------------------ c3: fire insurance
c3 = {
    "height": {"step": 24},
    "padding": {"top": 36, "left": 4, "right": 8, "bottom": 4},
    "transform": [
        {"calculate": {"de": "datum.place_de", "en": "datum.place_en"}, "as": "place"},
        {"joinaggregate": [{"op": "sum", "field": "buildings_value", "as": "bv"}, {"op": "sum", "field": "buildings", "as": "bn"}],
         "groupby": ["kind_de"]},
        {"calculate": "datum.bv / datum.bn", "as": "avg"},
        {"calculate": "datum.buildings_value / datum.buildings", "as": "per_building"},
    ],
    "encoding": {
        "y": {"field": "place", "type": "nominal", "sort": {"field": "per_building", "order": "descending"},
              "axis": {"title": None, "labelLimit": 400}},
        "x": {"type": "quantitative", "scale": {"domainMin": 0, "domainMax": {"expr": "max(2000, 1806 * width / max(width - 48, 60))"}, "nice": False},
              "axis": {"format": ",d", "values": [0, 500, 1000, 1500, 2000], "labelExpr": "width < 300 && datum.value % 1000 != 0 ? '' : datum.label",
                       "title": {"de": "Taler je Gebäude", "en": "Thalers per building"}}},
        "color": {"field": "kind_de", "type": "nominal", "legend": None,
                  "scale": {"domain": ["Stadt", "Land"], "range": ["@accent", "@accent2"]}},
    },
    "layer": [
        {"transform": [{"aggregate": [{"op": "mean", "field": "avg", "as": "avg"}], "groupby": ["kind_de"]}],
         "mark": {"type": "rule", "strokeDash": [3, 3], "strokeWidth": 1.4},
         "encoding": {"x": {"field": "avg", "type": "quantitative"}, "y": None}},
        {"transform": [{"aggregate": [{"op": "mean", "field": "avg", "as": "avg"}], "groupby": ["kind_de"]},
                       {"calculate": {"de": "(datum.kind_de == 'Stadt' ? 'Städte Ø ' : 'Land Ø ') + format(datum.avg, ',.0f')",
                                      "en": "(datum.kind_de == 'Stadt' ? 'Town average ' : 'Rural average ') + format(datum.avg, ',.0f')"}, "as": "avg_label"}],
         "mark": {"type": "text", "style": "label", "baseline": "bottom", "dy": {"expr": "datum.kind_de == 'Stadt' ? -19 : -5"}, "align": "center"},
         "encoding": {"x": {"field": "avg", "type": "quantitative"}, "y": {"value": 0}, "text": {"field": "avg_label"}}},
        {"mark": {"type": "rule", "strokeWidth": 1.6},
         "encoding": {"x": {"field": "per_building"}, "x2": {"datum": 0}, "color": {"value": "@context"}}},
        {"mark": {"type": "point", "filled": True, "size": 80, "opacity": 1},
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
