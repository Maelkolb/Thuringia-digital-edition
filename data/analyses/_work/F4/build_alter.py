from common import *

MERGES = [
    "bevoelkerung-altersaufbau-1864",
    "bevoelkerung-familienstand-ehen-1864",
    "bevoelkerung-geschlecht-alter-1834-1867",
    "bevoelkerung-wanderung-1864-1867",
]

single_years = dataset("bevoelkerung-altersaufbau-1864", "single_years")
married_by_age = dataset("bevoelkerung-familienstand-ehen-1864", "married_by_age")
birthplace = dataset("bevoelkerung-wanderung-1864-1867", "birthplace")
age_classes = dataset("bevoelkerung-altersaufbau-1864", "age_classes_econ")
civil_counts = dataset("bevoelkerung-familienstand-ehen-1864", "civil_counts")

# ---------------------------------------------------------------- numbers
SY = rows_of(single_years)
men = sum(r["persons"] for r in SY if r["sex"] == "männlich")
women = sum(r["persons"] for r in SY if r["sex"] == "weiblich")
women_per_100 = women / men * 100
first_year = sum(r["persons"] for r in SY if r["age"] == 1)

AC = {r["age_class"]: r for r in rows_of(age_classes) if r["region"] == "Reuß j. L. (1864)"}
youth = AC["Jugend (0–14 Jahre)"]["permille_total"] / 10
work = AC["Schaffendes Alter (15–60 Jahre)"]["permille_total"] / 10
old = AC["Greisenalter (über 60 Jahre)"]["permille_total"] / 10
pop64 = sum(AC[k]["total"] for k in AC)

MB = {(r["age_class"], r["sex"]): r["share_pct"] for r in rows_of(married_by_age) if r["area"] == "Fürstentum"}
m60, f60 = MB[("über 60", "männlich")], MB[("über 60", "weiblich")]
assert all(MB[(a, "männlich")] > MB[(a, "weiblich")] for a in ["unter 30", "30–45", "45–60", "über 60"])
CC = {(r["sex"], r["status"]): r["persons"] for r in rows_of(civil_counts) if r["district"] == "Fürstentum" and r["settlement"] == "insgesamt"}
widowers, widows = CC[("männlich", "verwitwet")], CC[("weiblich", "verwitwet")]

BP = {(r["district"], r["origin"]): r["pct"] for r in rows_of(birthplace) if r["area"] == "Zusammen"}
home = {d: BP[(d, "Geburtsgemeinde")] for d in ["Gera", "Schleiz", "Lobenstein-Ebersdorf", "Reuß j. L."]}
away_all = BP[("Reuß j. L.", "auswärts")]
other_all = BP[("Reuß j. L.", "andere Gemeinde")]
for d in home:
    assert abs(sum(BP[(d, o)] for o in ["Geburtsgemeinde", "andere Gemeinde", "auswärts"]) - 100) < 0.05

n = lambda x, d=0: pair(x, d)
log = [("men", men), ("women", women), ("women_per_100", women_per_100), ("first_year", first_year),
       ("classes", (youth, work, old)), ("pop64", pop64), ("married over60", (m60, f60)), ("widows", (widowers, widows)),
       ("home", home), ("away_all", away_all), ("other_all", other_all)]

# ---------------------------------------------------------------- charts
SEXCOL = {"field": "sex", "type": "nominal", "legend": None,
          "scale": {"domain": ["männlich", "weiblich"], "range": ["@accent", "@accent2"]}}
LIM = 2000


def class_label(pct, age_mid, de, en):
    pct_de, pct_en = n(pct, 1)
    base = {"transform": [{"filter": "datum.age == 1 && datum.sex === 'männlich'"}]}
    return [
        {**base, "mark": {"type": "text", "style": "label", "align": "right", "dy": -8, "color": "@ink"},
         "encoding": {"x": {"datum": LIM}, "y": {"datum": age_mid, "type": "quantitative"},
                      "text": {"value": {"de": pct_de + " %", "en": pct_en + " %"}}}},
        {**base, "mark": {"type": "text", "style": "annotation", "align": "right", "dy": 8},
         "encoding": {"x": {"datum": LIM}, "y": {"datum": age_mid, "type": "quantitative"},
                      "text": {"value": {"de": de, "en": en}}}},
    ]


c1 = {
    "height": 470,
    "transform": [
        {"calculate": "datum.sex === 'männlich' ? -datum.persons : datum.persons", "as": "signed"},
        {"calculate": "datum.age - 1", "as": "age_from"},
    ],
    "layer": [
        {"mark": {"type": "bar", "stroke": None, "strokeWidth": 0},
         "encoding": {
             "y": {"field": "age_from", "type": "quantitative", "scale": {"domain": [0, 90], "nice": False},
                   "axis": {"values": [0, 14, 30, 45, 60, 75, 90], "grid": False, "ticks": True,
                            "title": {"de": "Lebensjahr", "en": "Year of life"}}},
             "y2": {"field": "age"},
             "x2": {"datum": 0},
             "x": {"field": "signed", "type": "quantitative", "scale": {"domain": [-LIM, LIM]},
                   "axis": {"values": [-1000, -500, 0, 500, 1000], "labelExpr": "format(abs(datum.value), ',d')",
                            "title": {"de": "Personen je Lebensjahr", "en": "Persons per year of life"}}},
             "color": SEXCOL,
             "tooltip": [tooltip("age", "Lebensjahr", "Year of life", "d"), tooltip("sex", "Geschlecht", "Sex"),
                         tooltip("persons", "Personen", "Persons", ",d")]}},
        {"transform": [{"filter": "datum.age == 1 && datum.sex === 'männlich'"}],
         "mark": {"type": "rule", "color": "@ink2", "strokeDash": [4, 3], "strokeWidth": 1},
         "encoding": {"y": {"datum": 14, "type": "quantitative"}}},
        {"transform": [{"filter": "datum.age == 1 && datum.sex === 'männlich'"}],
         "mark": {"type": "rule", "color": "@ink2", "strokeDash": [4, 3], "strokeWidth": 1},
         "encoding": {"y": {"datum": 60, "type": "quantitative"}}},
        *class_label(youth, 7, "bis 14 Jahre", "up to 14 years"),
        *class_label(work, 37, "15 bis 60 Jahre", "15 to 60 years"),
        *class_label(old, 75, "über 60 Jahre", "over 60 years"),
        {"transform": [{"filter": "datum.age == 1 && datum.sex === 'männlich'"}],
         "mark": {"type": "text", "style": "label", "align": "right", "dx": -8, "color": "@accent"},
         "encoding": {"x": {"datum": 0}, "y": {"datum": 88, "type": "quantitative"},
                      "text": {"value": {"de": "Männer", "en": "Men"}}}},
        {"transform": [{"filter": "datum.age == 1 && datum.sex === 'männlich'"}],
         "mark": {"type": "text", "style": "label", "align": "left", "dx": 8, "color": "@accent2"},
         "encoding": {"x": {"datum": 0}, "y": {"datum": 88, "type": "quantitative"},
                      "text": {"value": {"de": "Frauen", "en": "Women"}}}},
    ],
}

AGES = ["unter 30", "30–45", "45–60", "über 60"]
c2 = {
    "height": 330,
    "transform": [{"filter": "datum.area === 'Fürstentum'"}],
    "encoding": {
        "x": {"field": "age_class", "type": "ordinal", "sort": AGES, "scale": {"paddingOuter": 0.45},
              "axis": {"labelAngle": 0, "ticks": False,
                       "title": {"de": "Altersklasse (Jahre)", "en": "Age group (years)"}}},
        "color": {"field": "sex", "type": "nominal", "legend": None,
                  "scale": {"domain": ["männlich", "weiblich"], "range": ["@accent", "@accent2"]}},
    },
    "layer": [
        {"mark": {"type": "line", "strokeWidth": 3},
         "encoding": {"y": {"field": "share_pct", "type": "quantitative", "scale": {"domain": [0, 100]},
                            "axis": {"values": [0, 25, 50, 75, 100], "title": {"de": "Verheiratete in Prozent der Altersklasse", "en": "Married, percent of the age group"}}}}},
        {"mark": {"type": "point", "filled": True, "size": 90},
         "encoding": {"y": {"field": "share_pct", "type": "quantitative"},
                      "tooltip": [tooltip("sex", "Geschlecht", "Sex"), tooltip("age_class", "Altersklasse", "Age group"),
                                  tooltip("married", "Verheiratete", "Married", ",d"), tooltip("share_pct", "Prozent der Altersklasse", "Percent of age group", ".1f")]}},
        {"transform": [{"filter": "datum.sex === 'männlich'"}],
         "mark": {"type": "text", "style": "label", "dy": -16},
         "encoding": {"y": {"field": "share_pct", "type": "quantitative"}, "text": {"field": "share_pct", "format": ".1f"}}},
        {"transform": [{"filter": "datum.sex === 'weiblich'"}],
         "mark": {"type": "text", "style": "label", "dy": 19},
         "encoding": {"y": {"field": "share_pct", "type": "quantitative"}, "text": {"field": "share_pct", "format": ".1f"}}},
        {"transform": [{"filter": "datum.sex === 'männlich' && datum.age_class === 'über 60'"}],
         "mark": {"type": "text", "style": "label", "align": "left", "dx": 13},
         "encoding": {"y": {"field": "share_pct", "type": "quantitative"}, "text": {"value": {"de": "Männer", "en": "Men"}}}},
        {"transform": [{"filter": "datum.sex === 'weiblich' && datum.age_class === 'über 60'"}],
         "mark": {"type": "text", "style": "label", "align": "left", "dx": 13},
         "encoding": {"y": {"field": "share_pct", "type": "quantitative"}, "text": {"value": {"de": "Frauen", "en": "Women"}}}},
    ],
}

ORDER_ORIGIN = "datum.origin === 'Geburtsgemeinde' ? 0 : (datum.origin === 'andere Gemeinde' ? 1 : 2)"
SEG_COLOR = {"field": "origin", "type": "nominal", "legend": None,
             "scale": {"domain": ["Geburtsgemeinde", "andere Gemeinde", "auswärts"], "range": ["@accent", "@context", "@accent2"]}}
ORDER4 = ["Gera", "Reuß j. L.", "Schleiz", "Lobenstein-Ebersdorf"]
Y4 = {"field": "district", "type": "nominal", "sort": ORDER4,
      "axis": {"title": None, "labelLimit": 400, "ticks": False,
               "labelExpr": {"de": "datum.value == 'Reuß j. L.' ? 'Fürstentum' : (datum.value == 'Gera' ? 'Bezirk Gera' : (datum.value == 'Schleiz' ? 'Bezirk Schleiz' : 'Bezirk Lobenstein-Ebersdorf'))",
                             "en": "datum.value == 'Reuß j. L.' ? 'Principality' : (datum.value == 'Gera' ? 'Gera district' : (datum.value == 'Schleiz' ? 'Schleiz district' : 'Lobenstein-Ebersdorf district'))"},
               "labelFontWeight": {"condition": {"test": "datum.value == 'Reuß j. L.'", "value": 700}, "value": 400}}}
TT_BP = [tooltip("district", "Bezirk", "District"), tooltip("origin", "Geburtsort", "Place of birth"),
         tooltip("persons", "Personen", "Persons", ",d"), tooltip("pct", "Prozent", "Percent", ".2f")]
c3 = {
    "height": {"step": 60},
    "transform": [
        {"filter": "datum.area === 'Zusammen'"},
        {"calculate": ORDER_ORIGIN, "as": "ord"},
        {"window": [{"op": "sum", "field": "pct", "as": "seg_end"}], "groupby": ["district"],
         "sort": [{"field": "ord"}], "frame": [None, 0]},
        {"calculate": "datum.seg_end - datum.pct", "as": "seg_start"},
        {"calculate": "(datum.seg_start + datum.seg_end) / 2", "as": "seg_mid"},
    ],
    "encoding": {"y": Y4},
    "layer": [
        {"mark": {"type": "bar", "size": 40, "cornerRadiusEnd": 0},
         "encoding": {"x": {"field": "seg_start", "type": "quantitative", "scale": {"domain": [0, 100]},
                            "axis": {"values": [0, 25, 50, 75, 100], "format": "d", "title": {"de": "Prozent der Einwohner 1864", "en": "Percent of inhabitants, 1864"}}},
                      "x2": {"field": "seg_end"}, "color": SEG_COLOR, "tooltip": TT_BP}},
        {"transform": [{"filter": "datum.origin === 'Geburtsgemeinde'"}],
         "mark": {"type": "text", "style": "label", "color": "@paper"},
         "encoding": {"x": {"field": "seg_mid", "type": "quantitative"}, "text": {"field": "pct", "format": ".1f"}}},
        {"transform": [{"filter": "datum.origin !== 'Geburtsgemeinde'"}],
         "mark": {"type": "text", "style": "label", "color": "@ink"},
         "encoding": {"x": {"field": "seg_mid", "type": "quantitative"}, "text": {"field": "pct", "format": ".1f"}}},
        {"transform": [{"filter": "datum.district === 'Gera' && datum.origin === 'Geburtsgemeinde'"}],
         "mark": {"type": "text", "style": "label", "color": "@accent", "dy": -33},
         "encoding": {"x": {"field": "seg_mid", "type": "quantitative"},
                      "text": {"value": {"de": "in der Geburtsgemeinde", "en": "in municipality of birth"}}}},
        {"transform": [{"filter": "datum.district === 'Gera' && datum.origin === 'andere Gemeinde'"}],
         "mark": {"type": "text", "style": "label-muted", "dy": -33},
         "encoding": {"x": {"field": "seg_mid", "type": "quantitative"},
                      "text": {"value": {"de": "anderer Ort", "en": "other place"}}}},
        {"transform": [{"filter": "datum.district === 'Gera' && datum.origin === 'auswärts'"}],
         "mark": {"type": "text", "style": "label", "color": "@accent2", "dy": -33},
         "encoding": {"x": {"field": "seg_mid", "type": "quantitative"},
                      "text": {"value": {"de": "auswärts", "en": "elsewhere"}}}},
    ],
}

# ---------------------------------------------------------------- texts
title = bi("Alter, Geschlecht und Familienstand 1864", "Age, sex and marital status in 1864")
summary = bi(
    f"Die Zählung von 1864 gliedert die {n(pop64)[0]} Einwohner nach Lebensjahren, Familienstand und Geburtsort. {n(youth, 1)[0]} Prozent waren bis 14 Jahre alt, {n(old, 1)[0]} Prozent über 60. "
    f"Auf 100 Männer kamen {n(women_per_100)[0]} Frauen. Von den über 60-Jährigen waren {n(m60)[0]} Prozent der Männer, aber nur {n(f60)[0]} Prozent der Frauen verheiratet. "
    f"{n(home['Reuß j. L.'])[0]} Prozent lebten in ihrer Geburtsgemeinde.",
    f"The census of 1864 classifies the {n(pop64)[1]} inhabitants by year of life, marital status and place of birth. {n(youth, 1)[1]} percent were up to 14 years old, {n(old, 1)[1]} percent over 60. "
    f"There were {n(women_per_100)[1]} women to 100 men. Over 60, {n(m60)[1]} percent of the men but only {n(f60)[1]} percent of the women were married. "
    f"{n(home['Reuß j. L.'])[1]} percent lived in their municipality of birth.",
)
findings = [
    bi(f"Brückner rechnet {n(youth, 1)[0]} Prozent zur Jugend, {n(work, 1)[0]} Prozent zum schaffenden Alter und {n(old, 1)[0]} Prozent zum Greisenalter. Das erste Lebensjahr zählt {n(first_year)[0]} Personen; auf 100 Männer kommen {n(women_per_100, 1)[0]} Frauen.",
       f"Brückner assigns {n(youth, 1)[1]} percent to youth, {n(work, 1)[1]} percent to working age and {n(old, 1)[1]} percent to old age. The first year of life counts {n(first_year)[1]} persons; there are {n(women_per_100, 1)[1]} women to 100 men."),
    bi(f"In jeder Altersklasse waren mehr Männer als Frauen verheiratet (über 60: {n(m60, 1)[0]} gegenüber {n(f60, 1)[0]} Prozent). 1864 gab es {n(widows)[0]} Witwen und {n(widowers)[0]} Witwer; Brückner nennt auch die leichtere Wiederheirat der Witwer.",
       f"In every age group more men than women were married (over 60: {n(m60, 1)[1]} against {n(f60, 1)[1]} percent). In 1864 there were {n(widows)[1]} widows and {n(widowers)[1]} widowers; Brückner also cites the easier remarriage of widowers."),
    bi(f"Am sesshaftesten war Lobenstein-Ebersdorf ({n(home['Lobenstein-Ebersdorf'], 2)[0]} Prozent in der Geburtsgemeinde), am beweglichsten der Bezirk Gera ({n(home['Gera'], 2)[0]}). Insgesamt waren {n(away_all, 1)[0]} Prozent der Einwohner auswärts geboren.",
       f"Lobenstein-Ebersdorf was the most settled ({n(home['Lobenstein-Ebersdorf'], 2)[1]} percent in their municipality of birth), the district of Gera the most mobile ({n(home['Gera'], 2)[1]}). Overall {n(away_all, 1)[1]} percent of the inhabitants were born elsewhere."),
]

charts = [
    {"id": "c1", "dataset": "single_years",
     "title": bi(f"Ein Drittel der Einwohner war 1864 bis 14 Jahre alt, nur {n(old, 1)[0]} Prozent über 60",
                 f"One third were up to 14 years old in 1864, only {n(old, 1)[1]} percent over 60"),
     "caption": bi("Einwohner des Fürstentums 1864 nach Lebensjahren und Geschlecht; Brückners Altersklassen mit ihrem Anteil an der Bevölkerung. Der gezackte Verlauf ab etwa 30 Jahren deutet auf gerundete Altersangaben. Quelle: S. 101 f.",
                   "Inhabitants of the principality in 1864 by year of life and sex; Brückner’s age classes with their share of the population. The jagged profile from about age 30 suggests rounded ages. Source: pp. 101 f."),
     "vegalite": c1},
    {"id": "c2", "dataset": "married_by_age",
     "title": bi(f"Von den über 60-Jährigen waren {n(m60)[0]} Prozent der Männer, aber nur {n(f60)[0]} Prozent der Frauen verheiratet",
                 f"Of those over 60, {n(m60)[1]} percent of men but only {n(f60)[1]} percent of women were married"),
     "caption": bi("Verheiratete in Prozent der jeweiligen Altersklasse, Fürstentum 1864, nach Brückners gedruckten Prozentzahlen. Der Nenner der Prozentzahlen ist nicht angegeben. Quelle: S. 104.",
                   "Married persons as a percentage of the respective age group, principality, 1864, as printed by Brückner. The denominator of the percentages is not stated. Source: p. 104."),
     "vegalite": c2},
    {"id": "c3", "dataset": "birthplace",
     "title": bi(f"Sieben von zehn Einwohnern lebten 1864 in der Geburtsgemeinde, im Bezirk Gera nur {n(home['Gera'])[0]} Prozent",
                 f"Seven in ten lived where they were born, in Gera district only {n(home['Gera'])[1]} percent"),
     "caption": bi("Einwohner 1864 nach Geburtsort: in der Wohngemeinde, in einer anderen Gemeinde des Fürstentums (anderer Ort) oder auswärts geboren. Prozent der Bezirksbevölkerung. Quelle: S. 105.",
                   "Inhabitants in 1864 by place of birth: in the municipality of residence, in another municipality of the principality (other place) or elsewhere. Percent of the district population. Source: p. 105."),
     "vegalite": c3},
]

datasets = [single_years, married_by_age, birthplace, age_classes, civil_counts]


def refs_pages(dss):
    out, seen = [], set()
    for ds in dss:
        for r in ds["source_refs"]:
            k = (r["page"], r["block"])
            if k not in seen:
                seen.add(k)
                out.append({"page": r["page"], "block": r["block"]})
    return out


issues = []
for aid in MERGES:
    issues.extend(archive(aid).get("transcription_issues", []))

feature = {
    "id": "alter-familie",
    "title": title,
    "category": "population",
    "section": "t1-2-1",
    "merges": MERGES,
    "sources": refs_pages(datasets),
    "summary": summary,
    "findings": findings,
    "method": bi(
        "Die Bevölkerung nach Lebensjahren und Geschlecht stammt aus der Tabelle S. 101 (Lebensjahre 1 bis 90). Die drei Altersklassen und ihre Anteile (Brückners »Procente«, die Promille der Gesamtbevölkerung sind) stehen auf S. 102. "
        "Der Familienstand (Zählung nach Geschlecht, Bezirk, Städten und Dörfern, S. 103) und die Verheirateten nach Altersklassen (S. 104) wurden unverändert übernommen, ebenso die Bevölkerung nach Geburtsort (S. 105). "
        "Im ersten Diagramm ist Brückners Lebensjahr 1 vermutlich das erste Lebensjahr, also das Alter von null bis unter einem Jahr; der Balken eines Lebensjahrs reicht deshalb von n minus 1 bis n. Die Altersklasse »bis 14 Jahre« umfasst die Lebensjahre 1 bis 14. "
        "Die Zahl der Frauen auf 100 Männer wurde aus den Einzeljahren (Lebensjahre 1 bis 90) berechnet; die Einzeljahre ergeben nicht ganz Brückners Altersklassensummen, weil er 143 Personen ohne Altersangabe und 6 über 90 Jahre getrennt führt. "
        "Die Prozentzahlen der Verheirateten sind die gedruckten; für Männer liegen den Klassen vermutlich die Lebensjahre ab 25, für Frauen ab 17 zugrunde. "
        "Nicht verwendet wurden die Altersaufbau-Abweichungen, Staatenvergleiche, die Altersunterschiede der Ehepartner, die Entwicklung des Frauenüberschusses 1834 bis 1867 und die Auswanderung 1867; sie stehen in den Einzelauswertungen.",
        "The population by year of life and sex comes from the table on p. 101 (years of life 1 to 90). The three age classes and their shares (Brückner’s “Procente”, which are per mille of the total population) are on p. 102. "
        "Marital status (census by sex, district, towns and villages, p. 103) and the married by age group (p. 104) were taken over unchanged, as was the population by place of birth (p. 105). "
        "In the first chart Brückner’s year of life 1 is presumably the first year of life, that is the age from zero to under one; the bar of a year of life therefore runs from n minus 1 to n. The age class “up to 14 years” covers the years of life 1 to 14. "
        "The number of women per 100 men was computed from the single years (years of life 1 to 90); the single years do not quite add up to Brückner’s class totals because he lists 143 persons of unknown age and 6 over 90 separately. "
        "The percentages of the married are the printed ones; for men the classes presumably rest on the years of life from 25, for women from 17. "
        "Not used are the deviations of the age profile, comparisons of states, the age differences of spouses, the development of the surplus of women 1834 to 1867 and the emigration of 1867; they are in the single analyses."),
    "caveats": [
        bi("Die Altersklassen auf S. 102 lassen sich aus der Einzeljahrtabelle nicht genau nachrechnen: Brückner verteilt offenbar die 143 Personen ohne Altersangabe auf die Klassen. Die Geschlechtersummen weichen je nach Tabelle um etwa 25 Personen ab.",
           "The age classes on p. 102 cannot be reproduced exactly from the single-year table: Brückner evidently distributes the 143 persons of unknown age over the classes. The totals by sex differ by about 25 persons between tables."),
        bi("Der gezackte Altersaufbau (die Lebensjahre 31, 41 und 61 sind überbesetzt, 32, 42, 52 und 62 unterbesetzt) deutet eher auf ungenaue, gerundete Altersangaben als auf wirkliche Geburtenschwankungen. Brückner kommentiert das nicht.",
           "The jagged age profile (years of life 31, 41 and 61 are overfull, 32, 42, 52 and 62 underfull) points to inexact, rounded ages rather than real fluctuations in births. Brückner does not comment on it."),
        bi("Bei den Verheirateten nach Alter nennt Brückner den Nenner nicht; die Klasse »unter 30« ist bei Männern und Frauen vermutlich unterschiedlich abgegrenzt. Die Zahl der verheirateten Männer (14.433) und Frauen (14.395) ist nicht gleich, die Ehepaare werden mit 13.945 angegeben.",
           "For the married by age Brückner does not state the denominator; the class “under 30” is presumably delimited differently for men and women. The numbers of married men (14,433) and women (14,395) are not equal, and the couples are given as 13,945."),
        bi("Die Angaben zum Geburtsort sind ein Bestand (Bevölkerung 1864), keine Zuwanderung eines Jahres. Für Lobenstein-Ebersdorf, Plattland, ergeben die drei gedruckten Prozentzahlen 101; die Zahlen führen auf 10,24 statt 11,23 Prozent auswärts Geborene.",
           "The information on place of birth is a stock (population in 1864), not immigration in a given year. For Lobenstein-Ebersdorf, rural area, the three printed percentages add up to 101; the numbers give 10.24 instead of 11.23 percent born elsewhere."),
    ],
    "conversions": [],
    "datasets": datasets,
    "charts": charts,
    "transcription_issues": issues,
    "keywords": {
        "de": ["Altersaufbau", "Bevölkerungspyramide", "Altersklassen", "Familienstand", "Verheiratete", "Witwen", "Geburtsort", "Wanderung", "Frauenüberschuss"],
        "en": ["age structure", "population pyramid", "age groups", "marital status", "married", "widows", "place of birth", "migration", "sex ratio"],
    },
    "related": ["geburten-sterbefaelle", "bevoelkerung-1647-1867", "berufe-gewerbe", "gesundheit"],
    "generated_by": "Claude Sonnet 5.5 (Agent F4), aus 4 Einzelauswertungen zusammengeführt",
    "date": "2026-10-02",
}
del feature["conversions"]

if __name__ == "__main__":
    check_limits(feature)
    write_feature(feature)
    with open("C:/Users/totom/Projects/reuss-edition/data/analyses/_work/F4/check_alter.txt", "w", encoding="utf-8") as f:
        for k, v in log:
            f.write(f"{k}: {v}\n")
