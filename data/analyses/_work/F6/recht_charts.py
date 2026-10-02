"""Chart specs for the feature `rechtspflege`. Stacks are computed with the stack transform so that bars and labels agree."""

# ------------------------------------------------------------------ c1: new lawsuits by outcome
c1 = {
    "padding": {"top": 8, "left": 4, "right": 96, "bottom": 4},
    "transform": [
        {"calculate": "datum.outcome_key == 'b' ? 0 : (datum.outcome_key == 'a' ? 1 : 2)", "as": "ord"},
        {"calculate": {"de": "{'a': 'Urteil', 'b': 'Vergleich', 'c': 'unerledigt'}[datum.outcome_key]",
                       "en": "{'a': 'judgment', 'b': 'settlement', 'c': 'unresolved'}[datum.outcome_key]"}, "as": "outcome"},
        {"joinaggregate": [{"op": "sum", "field": "cases", "as": "tot"}], "groupby": ["level", "year"]},
        {"stack": "cases", "groupby": ["level", "year"], "sort": [{"field": "ord", "order": "ascending"}], "as": ["v0", "v1"]},
        {"calculate": "(datum.v0 + datum.v1) / 2", "as": "mid"},
    ],
    "facet": {"column": {"field": "level", "type": "nominal", "sort": ["Justizämter", "Kreisgerichte"],
                         "header": {"title": None, "labelOrient": "top", "labelAnchor": "start", "labelFontSize": 12.5,
                                    "labelFontWeight": 600, "labelColor": "@ink", "labelPadding": 8,
                                    "labelExpr": {"de": "datum.label == 'Justizämter' ? 'Justizämter (Streitwert bis 100 Taler)' : 'Kreisgerichte (größere Streitsachen)'",
                                                  "en": "datum.label == 'Justizämter' ? 'Justizämter (suits up to 100 thalers)' : 'Kreisgerichte (larger suits)'"}}}},
    "spec": {
        "width": 250,
        "height": 290,
        "encoding": {
            "x": {"field": "year", "type": "ordinal", "axis": {"title": None, "labelAngle": 0, "format": "d"}},
            "color": {"field": "outcome_key", "type": "nominal", "legend": None,
                      "scale": {"domain": ["b", "a", "c"], "range": ["@accent", "@accent2", "@context"]}},
        },
        "layer": [
            {"mark": {"type": "bar"},
             "encoding": {"y": {"field": "v0", "type": "quantitative", "scale": {"domain": [0, 2500]},
                                "axis": {"format": ",d", "values": [0, 500, 1000, 1500, 2000, 2500],
                                         "title": {"de": "Neue förmliche Rechtsstreitigkeiten", "en": "New formal lawsuits"}}},
                          "y2": {"field": "v1"},
                          "tooltip": [{"field": "level", "title": {"de": "Gerichtsebene", "en": "Court level"}},
                                      {"field": "year", "title": {"de": "Jahr", "en": "Year"}, "format": "d"},
                                      {"field": "outcome", "title": {"de": "Ausgang", "en": "Outcome"}},
                                      {"field": "cases", "title": {"de": "Fälle", "en": "Cases"}, "format": ",d"}]}},
            {"mark": {"type": "text", "baseline": "middle", "style": "label"},
             "encoding": {"y": {"field": "mid", "type": "quantitative"},
                          "text": {"field": "cases", "type": "quantitative", "format": ",d"},
                          "color": {"condition": {"test": "datum.outcome_key == 'c'", "value": "@ink2"}, "value": "@paper"}}},
            {"transform": [{"filter": "datum.ord == 2"}],
             "mark": {"type": "text", "baseline": "bottom", "dy": -4, "style": "label-muted"},
             "encoding": {"y": {"field": "v1", "type": "quantitative"},
                          "text": {"field": "tot", "type": "quantitative", "format": ",d"}, "color": None}},
            {"transform": [{"filter": "datum.level == 'Kreisgerichte' && datum.year == 1867"}],
             "mark": {"type": "text", "baseline": "middle", "align": "left", "dx": 6, "style": "label"},
             "encoding": {"x": {"datum": 1867, "type": "ordinal", "bandPosition": 1},
                          "y": {"field": "mid", "type": "quantitative"},
                          "text": {"field": "outcome"},
                          "color": {"condition": [{"test": "datum.outcome_key == 'c'", "value": "@muted"},
                                                  {"test": "datum.outcome_key == 'a'", "value": "@accent2"}], "value": "@accent"}}},
        ],
    },
}

# ------------------------------------------------------------------ c2: offences, stacked by court district
OFFENCE_ORDER = ["forest_convicted", "police_convicted", "common_other", "honour_convicted", "defraud_convicted"]
_OFFENCE_DE = ("{'forest_convicted': 'Forstdiebstahl', 'police_convicted': 'Polizeiliche Übertretungen', "
               "'common_other': 'Übrige gemeine Übertretungen', 'honour_convicted': 'Injurien (Ehrenkränkungen)', "
               "'defraud_convicted': 'Defraudationen'}[datum.value]")
_OFFENCE_EN = ("{'forest_convicted': 'Forest theft', 'police_convicted': 'Police offences', "
               "'common_other': 'Other common offences', 'honour_convicted': 'Insults to honour', "
               "'defraud_convicted': 'Defraudations'}[datum.value]")

c2 = {
    "height": {"step": 40},
    "padding": {"top": 4, "left": 4, "right": 44, "bottom": 4},
    "transform": [
        {"fold": ["forest_convicted", "common_other", "police_convicted", "honour_convicted", "defraud_convicted"], "as": ["offence", "n"]},
        {"calculate": "isValid(datum.n) ? datum.n : 0", "as": "n"},
        {"aggregate": [{"op": "sum", "field": "n", "as": "n"}], "groupby": ["kreisgericht", "offence"]},
        {"joinaggregate": [{"op": "sum", "field": "n", "as": "tot"}], "groupby": ["offence"]},
        {"calculate": "datum.kreisgericht == 'Gera' ? 0 : 1", "as": "ord"},
        {"stack": "n", "groupby": ["offence"], "sort": [{"field": "ord", "order": "ascending"}], "as": ["x0", "x1"]},
        {"calculate": "(datum.x0 + datum.x1) / 2", "as": "mid"},
        {"calculate": {"de": "{'forest_convicted': 'Forstdiebstahl', 'police_convicted': 'Polizeiliche Übertretungen', 'common_other': 'Übrige gemeine Übertretungen', 'honour_convicted': 'Injurien (Ehrenkränkungen)', 'defraud_convicted': 'Defraudationen'}[datum.offence]",
                       "en": "{'forest_convicted': 'Forest theft', 'police_convicted': 'Police offences', 'common_other': 'Other common offences', 'honour_convicted': 'Insults to honour', 'defraud_convicted': 'Defraudations'}[datum.offence]"}, "as": "offence_label"},
        {"calculate": "(datum.offence == 'forest_convicted' ? datum.kreisgericht + ' ' : '') + datum.n", "as": "seg_label"},
    ],
    "encoding": {
        "y": {"field": "offence", "type": "nominal", "sort": OFFENCE_ORDER,
              "axis": {"title": None, "labelLimit": 300, "labelExpr": {"de": _OFFENCE_DE, "en": _OFFENCE_EN}}},
        "color": {"field": "kreisgericht", "type": "nominal", "legend": None,
                  "scale": {"domain": ["Gera", "Schleiz"], "range": ["@accent", "@accent2"]}},
    },
    "layer": [
        {"mark": {"type": "bar", "size": 26},
         "encoding": {"x": {"field": "x0", "type": "quantitative", "scale": {"domain": [0, 760]},
                            "axis": {"format": ",d", "values": [0, 200, 400, 600],
                                     "title": {"de": "Verurteilte Personen 1867", "en": "Persons convicted, 1867"}}},
                      "x2": {"field": "x1"},
                      "tooltip": [{"field": "offence_label", "title": {"de": "Art", "en": "Kind"}},
                                  {"field": "kreisgericht", "title": {"de": "Bezirk des Kreisgerichts", "en": "Court district"}},
                                  {"field": "n", "title": {"de": "Verurteilte", "en": "Convicted"}, "format": ",d"}]}},
        {"transform": [{"filter": "datum.n >= 40"}],
         "mark": {"type": "text", "baseline": "middle", "style": "label"},
         "encoding": {"x": {"field": "mid", "type": "quantitative"}, "text": {"field": "seg_label"}, "color": {"value": "@paper"}}},
        {"transform": [{"filter": "datum.ord == 1"}],
         "mark": {"type": "text", "align": "left", "dx": 6, "style": "label"},
         "encoding": {"x": {"field": "x1", "type": "quantitative"}, "text": {"field": "tot", "type": "quantitative", "format": ",d"},
                      "color": None}},
    ],
}

# ------------------------------------------------------------------ c3: persons taken into custody
c3 = {
    "height": 300,
    "padding": {"top": 8, "left": 4, "right": 130, "bottom": 4},
    "transform": [
        {"aggregate": [{"op": "sum", "field": "prisoners", "as": "n"}], "groupby": ["year", "haftart"]},
        {"calculate": "datum.haftart == 'Strafhaft' ? 0 : 1", "as": "ord"},
        {"calculate": {"de": "datum.haftart == 'Strafhaft' ? 'Strafhaft' : 'Untersuchungshaft'",
                       "en": "datum.haftart == 'Strafhaft' ? 'imprisonment' : 'pre-trial detention'"}, "as": "haft"},
        {"joinaggregate": [{"op": "sum", "field": "n", "as": "tot"}], "groupby": ["year"]},
        {"stack": "n", "groupby": ["year"], "sort": [{"field": "ord", "order": "ascending"}], "as": ["v0", "v1"]},
        {"calculate": "(datum.v0 + datum.v1) / 2", "as": "mid"},
    ],
    "encoding": {
        "x": {"field": "year", "type": "ordinal", "axis": {"title": None, "labelAngle": 0, "format": "d"}},
        "color": {"field": "haftart", "type": "nominal", "legend": None,
                  "scale": {"domain": ["Strafhaft", "Untersuchungshaft"], "range": ["@accent", "@accent2"]}},
    },
    "layer": [
        {"mark": {"type": "bar"},
         "encoding": {"y": {"field": "v0", "type": "quantitative", "scale": {"domain": [0, 1600]},
                            "axis": {"format": ",d", "values": [0, 400, 800, 1200, 1600],
                                     "title": {"de": "Personen in Haft", "en": "Persons in custody"}}},
                      "y2": {"field": "v1"},
                      "tooltip": [{"field": "year", "title": {"de": "Jahr", "en": "Year"}, "format": "d"},
                                  {"field": "haft", "title": {"de": "Haftart", "en": "Kind"}},
                                  {"field": "n", "title": {"de": "Personen", "en": "Persons"}, "format": ",d"}]}},
        {"mark": {"type": "text", "baseline": "middle", "style": "label"},
         "encoding": {"y": {"field": "mid", "type": "quantitative"},
                      "text": {"field": "n", "type": "quantitative", "format": ",d"}, "color": {"value": "@paper"}}},
        {"transform": [{"filter": "datum.ord == 1"}],
         "mark": {"type": "text", "baseline": "bottom", "dy": -5, "style": "label"},
         "encoding": {"y": {"field": "v1", "type": "quantitative"},
                      "text": {"field": "tot", "type": "quantitative", "format": ",d"}, "color": None}},
        {"transform": [{"filter": "datum.year == 1867"}],
         "mark": {"type": "text", "baseline": "middle", "align": "left", "dx": 8, "style": "label"},
         "encoding": {"x": {"datum": 1867, "type": "ordinal", "bandPosition": 1},
                      "y": {"field": "mid", "type": "quantitative"},
                      "text": {"field": "haft"},
                      "color": {"field": "haftart", "type": "nominal", "legend": None,
                                "scale": {"domain": ["Strafhaft", "Untersuchungshaft"], "range": ["@accent", "@accent2"]}}}},
    ],
}
