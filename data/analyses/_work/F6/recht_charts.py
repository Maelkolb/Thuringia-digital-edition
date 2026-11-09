"""Chart specs for the feature `rechtspflege`. Stacks are computed with the stack transform so that bars and labels agree."""

FITS = "abs(scale('x', datum.x1) - scale('x', datum.x0)) >= 30 ? 1 : 0"

# ------------------------------------------------------------------ lawsuits by outcome
LAWSUIT_ROWS = ["Justizämter 1864", "Justizämter 1865", "Justizämter 1866", "Justizämter 1867", " ",
                "Kreisgerichte 1864", "Kreisgerichte 1865", "Kreisgerichte 1866", "Kreisgerichte 1867"]
OUTCOME_ORDER = "datum.outcome_de == 'Vergleich' ? 0 : (datum.outcome_de == 'Erkenntnis' ? 1 : 2)"

lawsuits = {
    "height": {"step": 24},
    "padding": {"top": 30, "left": 4, "right": 8, "bottom": 4},
    "transform": [
        {"calculate": "datum.level + ' ' + datum.year", "as": "row"},
        {"calculate": OUTCOME_ORDER, "as": "ord"},
        {"calculate": {"de": "datum.ord == 0 ? 'Vergleich' : (datum.ord == 1 ? 'Urteil' : 'unerledigt')",
                       "en": "datum.ord == 0 ? 'settlement' : (datum.ord == 1 ? 'judgment' : 'unresolved')"}, "as": "outcome"},
        {"joinaggregate": [{"op": "sum", "field": "cases", "as": "tot"}], "groupby": ["row"]},
        {"stack": "cases", "groupby": ["row"], "sort": [{"field": "ord", "order": "ascending"}], "as": ["x0", "x1"]},
        {"calculate": "(datum.x0 + datum.x1) / 2", "as": "mid"},
    ],
    "encoding": {
        "y": {"field": "row", "type": "nominal", "scale": {"domain": LAWSUIT_ROWS},
              "axis": {"title": None, "labelLimit": 300,
                       "labelExpr": "indexof(datum.value, '1864') >= 0 ? datum.value : substring(datum.value, length(datum.value) - 4)"}},
        "x": {"type": "quantitative",
              "scale": {"domainMin": 0, "domainMax": {"expr": "max(2400, 2269 * width / max(width - 44, 60))"}, "nice": False},
              "axis": {"format": ",d", "values": [0, 500, 1000, 1500, 2000], "labelExpr": "width < 360 && datum.value % 1000 != 0 ? '' : datum.label",
                       "title": {"de": "Neue förmliche Rechtsstreitigkeiten", "en": "New formal lawsuits"}}},
        "color": {"field": "ord", "type": "nominal", "legend": None,
                  "scale": {"domain": [0, 1, 2], "range": ["@accent", "@accent2", "@context"]}},
    },
    "layer": [
        {"mark": {"type": "bar", "height": 16},
         "encoding": {"x": {"field": "x0"}, "x2": {"field": "x1"},
                      "tooltip": [{"field": "level", "title": {"de": "Gerichtsebene", "en": "Court level"}},
                                  {"field": "year", "title": {"de": "Jahr", "en": "Year"}, "format": "d"},
                                  {"field": "outcome", "title": {"de": "Ausgang", "en": "Outcome"}},
                                  {"field": "cases", "title": {"de": "Fälle", "en": "Cases"}, "format": ",d"}]}},
        {"transform": [{"filter": "datum.ord < 2"}],
         "mark": {"type": "text", "baseline": "middle", "style": "label", "opacity": {"expr": FITS}},
         "encoding": {"x": {"field": "mid"}, "text": {"field": "cases", "type": "quantitative", "format": ",d"}, "color": {"value": "@paper"}}},
        {"transform": [{"filter": "datum.ord == 2"}],
         "mark": {"type": "text", "align": "left", "dx": 5, "style": "label-muted"},
         "encoding": {"x": {"field": "x1"}, "text": {"field": "tot", "type": "quantitative", "format": ",d"}, "color": None}},
        {"transform": [{"filter": "datum.row == 'Justizämter 1864'"}],
         "mark": {"type": "text", "align": "left", "baseline": "bottom", "style": "label",
                  "dy": {"expr": "datum.ord == 2 && width < 520 ? -24 : -10"}},
         "encoding": {"x": {"field": "x0"}, "text": {"field": "outcome"},
                      "color": {"condition": {"test": "datum.ord == 2", "value": "@ink2"}, "value": "@ink"}}},
    ],
}

# ------------------------------------------------------------------ offences, stacked by court district
OFFENCE_ORDER = ["forest_convicted", "police_convicted", "common_other", "honour_convicted", "defraud_convicted"]
_OFFENCE_DE = ("{'forest_convicted': 'Forstdiebstahl', 'police_convicted': 'Polizeiliche Übertretungen', "
               "'common_other': 'Übrige gemeine Übertretungen', 'honour_convicted': 'Injurien (Ehrenkränkungen)', "
               "'defraud_convicted': 'Defraudationen'}")
_OFFENCE_EN = ("{'forest_convicted': 'Forest theft', 'police_convicted': 'Police offences', "
               "'common_other': 'Other common offences', 'honour_convicted': 'Insults to honour', "
               "'defraud_convicted': 'Tax and customs fraud'}")

offences = {
    "height": {"step": 40},
    "padding": {"top": 20, "left": 4, "right": 8, "bottom": 4},
    "transform": [
        {"fold": ["forest_convicted", "common_other", "police_convicted", "honour_convicted", "defraud_convicted"], "as": ["offence", "n"]},
        {"calculate": "isValid(datum.n) ? datum.n : 0", "as": "n"},
        {"aggregate": [{"op": "sum", "field": "n", "as": "n"}], "groupby": ["kreisgericht", "offence"]},
        {"joinaggregate": [{"op": "sum", "field": "n", "as": "tot"}], "groupby": ["offence"]},
        {"calculate": "datum.kreisgericht == 'Gera' ? 0 : 1", "as": "ord"},
        {"stack": "n", "groupby": ["offence"], "sort": [{"field": "ord", "order": "ascending"}], "as": ["x0", "x1"]},
        {"calculate": "(datum.x0 + datum.x1) / 2", "as": "mid"},
        {"calculate": {"de": _OFFENCE_DE + "[datum.offence]", "en": _OFFENCE_EN + "[datum.offence]"}, "as": "offence_label"},
    ],
    "encoding": {
        "y": {"field": "offence", "type": "nominal", "sort": OFFENCE_ORDER,
              "axis": {"title": None, "labelLimit": 300, "labelExpr": {"de": _OFFENCE_DE + "[datum.value]", "en": _OFFENCE_EN + "[datum.value]"}}},
        "x": {"type": "quantitative",
              "scale": {"domainMin": 0, "domainMax": {"expr": "max(760, 686 * width / max(width - 40, 60))"}, "nice": False},
              "axis": {"format": ",d", "values": [0, 200, 400, 600],
                       "title": {"de": "Verurteilte Personen 1867", "en": "Persons convicted, 1867"}}},
        "color": {"field": "kreisgericht", "type": "nominal", "legend": None,
                  "scale": {"domain": ["Gera", "Schleiz"], "range": ["@accent", "@accent2"]}},
    },
    "layer": [
        {"mark": {"type": "bar", "size": 26},
         "encoding": {"x": {"field": "x0"}, "x2": {"field": "x1"},
                      "tooltip": [{"field": "offence_label", "title": {"de": "Art", "en": "Kind"}},
                                  {"field": "kreisgericht", "title": {"de": "Bezirk des Kreisgerichts", "en": "Court district"}},
                                  {"field": "n", "title": {"de": "Verurteilte", "en": "Convicted"}, "format": ",d"}]}},
        {"mark": {"type": "text", "baseline": "middle", "style": "label", "opacity": {"expr": FITS}},
         "encoding": {"x": {"field": "mid"}, "text": {"field": "n", "type": "quantitative", "format": ",d"}, "color": {"value": "@paper"}}},
        {"transform": [{"filter": "datum.ord == 1"}],
         "mark": {"type": "text", "align": "left", "dx": 6, "style": "label"},
         "encoding": {"x": {"field": "x1"}, "text": {"field": "tot", "type": "quantitative", "format": ",d"}, "color": None}},
        {"transform": [{"filter": "datum.offence == 'forest_convicted'"}],
         "mark": {"type": "text", "align": "left", "baseline": "bottom", "dy": -15, "style": "label"},
         "encoding": {"x": {"field": "x0"}, "text": {"field": "kreisgericht"}, "color": {"value": "@ink"}}},
    ],
}

# ------------------------------------------------------------------ persons taken into custody
custody = {
    "height": {"step": 40},
    "padding": {"top": 20, "left": 4, "right": 8, "bottom": 4},
    "transform": [
        {"aggregate": [{"op": "sum", "field": "prisoners", "as": "n"}], "groupby": ["year", "haftart"]},
        {"calculate": "datum.haftart == 'Strafhaft' ? 0 : 1", "as": "ord"},
        {"calculate": {"de": "datum.haftart", "en": "datum.haftart == 'Strafhaft' ? 'imprisonment' : 'pre-trial detention'"}, "as": "haft"},
        {"joinaggregate": [{"op": "sum", "field": "n", "as": "tot"}], "groupby": ["year"]},
        {"stack": "n", "groupby": ["year"], "sort": [{"field": "ord", "order": "ascending"}], "as": ["x0", "x1"]},
        {"calculate": "(datum.x0 + datum.x1) / 2", "as": "mid"},
    ],
    "encoding": {
        "y": {"field": "year", "type": "ordinal", "axis": {"title": None, "format": "d"}},
        "x": {"type": "quantitative",
              "scale": {"domainMin": 0, "domainMax": {"expr": "max(1600, 1443 * width / max(width - 48, 60))"}, "nice": False},
              "axis": {"format": ",d", "values": [0, 400, 800, 1200, 1600],
                       "title": {"de": "Personen in Haft", "en": "Persons in custody"}}},
        "color": {"field": "haftart", "type": "nominal", "legend": None,
                  "scale": {"domain": ["Strafhaft", "Untersuchungshaft"], "range": ["@accent", "@accent2"]}},
    },
    "layer": [
        {"mark": {"type": "bar", "size": 26},
         "encoding": {"x": {"field": "x0"}, "x2": {"field": "x1"},
                      "tooltip": [{"field": "year", "title": {"de": "Jahr", "en": "Year"}, "format": "d"},
                                  {"field": "haft", "title": {"de": "Haftart", "en": "Kind"}},
                                  {"field": "n", "title": {"de": "Personen", "en": "Persons"}, "format": ",d"}]}},
        {"mark": {"type": "text", "baseline": "middle", "style": "label", "opacity": {"expr": FITS}},
         "encoding": {"x": {"field": "mid"}, "text": {"field": "n", "type": "quantitative", "format": ",d"}, "color": {"value": "@paper"}}},
        {"transform": [{"filter": "datum.ord == 1"}],
         "mark": {"type": "text", "align": "left", "dx": 6, "style": "label"},
         "encoding": {"x": {"field": "x1"}, "text": {"field": "tot", "type": "quantitative", "format": ",d"}, "color": None}},
        {"transform": [{"filter": "datum.year == 1864"}],
         "mark": {"type": "text", "align": "left", "baseline": "bottom", "dy": -15, "style": "label"},
         "encoding": {"x": {"field": "x0"}, "text": {"field": "haft"}, "color": {"value": "@ink"}}},
    ],
}
