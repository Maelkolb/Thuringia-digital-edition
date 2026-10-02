import copy
import re
from common import *

ID = "berufe-gewerbe"
A_KL = "wirtschaft-berufsklassen-1864"
A_GW = "industrie-gewerbe-1864-einzelne-gewerbe"
A_ZW = "industrie-hauptzweige-staedte-plattland-1864"
A_HA = "handel-gewerbe-nach-landesteilen-1864"

klassen = copy.deepcopy(dataset(A_KL, "klassen"))
gewerbe = copy.deepcopy(dataset(A_GW, "gewerbe"))
fuerst = copy.deepcopy(dataset(A_GW, "fuerstenthum"))
zweige = copy.deepcopy(dataset(A_ZW, "zweige"))
handel_old = copy.deepcopy(dataset(A_HA, "handel"))

kl = rows_as_dicts(klassen)
gw = rows_as_dicts(gewerbe)
fu = rows_as_dicts(fuerst)
zw = rows_as_dicts(zweige)

# ---------------------------------------------------------------- classes
KURZ = {
    10: ("Wissenschaft und Kunst", "Science and the arts"),
    12: ("Ohne Berufsausübung", "Without occupation"),
    13: ("Ohne angegebenen Beruf", "No stated occupation"),
}
klassen["columns"] = klassen["columns"] + [
    col("klasse_kurz_de", "Berufsklasse, Kurzform", "Occupational class, short form", "string", derived=True, note="Brückners Klassenname, bei langen Namen gekürzt"),
    col("klasse_kurz_en", "Berufsklasse, Kurzform (englisch)", "Occupational class, short form (English)", "string", derived=True),
]
for row, r in zip(klassen["rows"], kl):
    nr = r["klasse_nr"]
    row += list(KURZ.get(nr, (r["klasse_de"], r["klasse_en"])))
    for k, v in enumerate(row):
        if isinstance(v, str):
            row[k] = v.replace("labourers", "laborers")

pop = [r for r in kl if r["klasse_nr"] == 14 and r["landestheil_de"] == "Fürstentum" and r["gebiet_de"] == "zusammen"][0]["summe"]


def klasse(nr, gebiet):
    return [r for r in kl if r["klasse_nr"] == nr and r["landestheil_de"] == "Fürstentum" and r["gebiet_de"] == gebiet][0]


ind_t, ind_p, ind_z = klasse(3, "Städte")["share_pct"], klasse(3, "Plattland")["share_pct"], klasse(3, "zusammen")["share_pct"]
agr_t, agr_p, agr_z = klasse(1, "Städte")["share_pct"], klasse(1, "Plattland")["share_pct"], klasse(1, "zusammen")["share_pct"]
print("pop", pop, "industry", ind_t, ind_p, ind_z, "agri", agr_t, agr_p, agr_z)

# ---------------------------------------------------------------- trades by district
trades = {}
for r in gw:
    trades.setdefault(r["trade"], {"en": r["trade_en"], "branch": r["branch"], "d": {}})
    trades[r["trade"]]["d"][r["district"]] = r
for t, v in trades.items():
    v["persons"] = sum(x["persons"] for x in v["d"].values())
    v["s"] = sum((x["s"] or 0) for x in v["d"].values())
    v["g"] = sum((x["g"] or 0) for x in v["d"].values())
    v["sg"] = v["s"] + v["g"]
CATCH_ALL = ["Fabrikarbeiter ohne angegebenen Fabrikzweig", "Nichtbenannte Nahrungszweige"]
ranked = sorted([kv for kv in trades.items() if kv[0] not in CATCH_ALL], key=lambda kv: -kv[1]["persons"])
rank = {t: i + 1 for i, (t, _) in enumerate(ranked)}
for t, v in ranked[:16]:
    print(rank[t], t, v["persons"], {d: x["persons"] for d, x in v["d"].items()})

dist_sg = {d: sum(((r["s"] or 0) + (r["g"] or 0)) for r in gw if r["district"] == d) for d in DISTRICTS}
weber = trades["Weber"]
weber_sg_share = {d: ((weber["d"][d]["s"] or 0) + (weber["d"][d]["g"] or 0)) / dist_sg[d] * 100 for d in DISTRICTS}
print(dist_sg, {k: round(v, 1) for k, v in weber_sg_share.items()})
maurer, zimmer = trades["Maurer, Steinhauer"], trades["Zimmerleute"]
g_per_s = lambda t: trades[t]["g"] / trades[t]["s"]
big = [t for t, v in trades.items() if v["s"] >= 40 and t not in CATCH_ALL]
more_g = [t for t in big if trades[t]["g"] > trades[t]["s"]]
print(len(big), len(more_g), g_per_s("Maurer, Steinhauer"), g_per_s("Zimmerleute"))
weber_schleiz_share = weber["d"]["Schleiz"]["persons"] / weber["persons"] * 100
second = ranked[1][1]["persons"]
print("weber", weber["persons"], weber_schleiz_share, weber["persons"] / second, weber["persons"] / pop * 100)

# gewerbe dataset with rank columns (derived)
gewerbe["columns"] = gewerbe["columns"][:-1] + [
    col("persons_total", "Personen im Fürstentum (Summe der Landesteile)", "Persons in the principality (sum of the districts)", "integer", "Personen", True),
    col("rang", "Rang nach Personen (ohne Sammelposten)", "Rank by persons (without catch-all items)", "integer", None, True),
] + gewerbe["columns"][-1:]
for row, r in zip(gewerbe["rows"], gw):
    row[-1:] = [trades[r["trade"]]["persons"], rank.get(r["trade"]), row[-1]]

# ---------------------------------------------------------------- trade and commerce (p. 260)
page260 = (ROOT / "data" / "text" / "pages" / "260.txt").read_text(encoding="utf-8")
lines = [l for l in page260.splitlines() if re.match(r"\s+r(\d+) \|", l)]
parsed = []
for l in lines:
    cells = [c.strip() for c in l.strip().split("|")]
    n = int(cells[0][1:])
    if 3 <= n <= 17:
        vals = [None if c in ("—", "") else int(c) for c in cells[2:14]]
        parsed.append((n, cells[1], vals))
assert len(parsed) == 15, len(parsed)
old_names = []
for r in rows_as_dicts(handel_old):
    if r["trade"] not in [x[0] for x in old_names]:
        old_names.append((r["trade"], r["trade_en"]))
assert len(old_names) == 15
SHORT = {
    "Colonial- und Materialhändler": ("Colonial- u. Materialhändler", "Colonial and general goods"),
    "Victualienhändler": ("Victualienhändler", "Provisions dealers"),
    "Getreidehändler": ("Getreidehändler", "Grain dealers"),
    "Viehhändler": ("Viehhändler", "Cattle dealers"),
    "Lederhändler": ("Lederhändler", "Leather dealers"),
    "Schnitt-, Putz- und Modewaarenhändler": ("Schnitt- u. Modewaarenhändler", "Drapers and fashion dealers"),
    "Strumpf- und Zwirnhändler": ("Strumpf- u. Zwirnhändler", "Hosiery and thread dealers"),
    "Galanteriewaarenhändler": ("Galanteriewaarenhändler", "Fancy-goods dealers"),
    "Holzhändler": ("Holzhändler", "Timber dealers"),
    "Buch-, Kunst- und Musikalienhändler": ("Buch-, Kunst-, Musikalienh.", "Book, art and music dealers"),
    "Banquiers": ("Banquiers", "Bankers"),
    "Agenten, Spediteurs, Mäkler und Commissionäre": ("Agenten, Spediteurs u. a.", "Agents, forwarders, brokers"),
    "Schenk- und Gastwirthe": ("Schenk- u. Gastwirthe", "Innkeepers and publicans"),
    "Miethkutscher und Frachtfuhrleute": ("Miethkutscher, Frachtfuhrleute", "Coachmen and carriers"),
    "Sonstige Händler": ("Sonstige Händler", "Other dealers"),
}
handel_cols = [
    col("trade", "Gewerbe", "Trade", "string"),
    col("trade_en", "Gewerbe (englisch)", "Trade (English)", "string", derived=True),
    col("s_staedte", "Städte, Selbständige", "Towns, self-employed", "integer", "Personen"),
    col("g_staedte", "Städte, Gehilfen", "Towns, assistants", "integer", "Personen"),
    col("d_staedte", "Städte, Dienstboten", "Towns, servants", "integer", "Personen"),
    col("f_staedte", "Städte, Familienglieder", "Towns, family members", "integer", "Personen"),
    col("s_plattland", "Plattland, Selbständige", "Countryside, self-employed", "integer", "Personen"),
    col("g_plattland", "Plattland, Gehilfen", "Countryside, assistants", "integer", "Personen"),
    col("d_plattland", "Plattland, Dienstboten", "Countryside, servants", "integer", "Personen"),
    col("f_plattland", "Plattland, Familienglieder", "Countryside, family members", "integer", "Personen"),
    col("s_gesamt", "Selbständige zusammen", "Self-employed, total", "integer", "Personen", True),
    col("share_staedte", "Anteil der Selbständigen in den Städten", "Share of the self-employed in the towns", "number", "%", True),
    col("label_de", "Beschriftung (deutsch)", "Label (German)", "string", derived=True, note="Gewerbename gekürzt, Zahl der Selbständigen in Klammern"),
    col("label_en", "Beschriftung (englisch)", "Label (English)", "string", derived=True),
]
handel_rows = []
for (n, name, vals), (tname, ten) in zip(parsed, old_names):
    s_t, s_p = vals[0] or 0, vals[4] or 0
    tot = s_t + s_p
    share = s_t / tot * 100
    de_short, en_short = SHORT[tname]
    handel_rows.append([tname, ten, *vals[0:4], *vals[4:8], tot, round(share, 2), f"{de_short} ({tot})", f"{en_short} ({tot})"])
handel = {
    "name": "handel_fuerstentum",
    "title": bi("Handel und Transport 1864 im Fürstentum, Städte und Plattland", "Trade and transport in 1864 in the principality, towns and countryside"),
    "columns": handel_cols,
    "rows": handel_rows,
    "source_refs": [{"page": "260", "block": "b1", "rows": "r3-t18"}],
}
hh = {r[0]: r for r in handel_rows}
for r in sorted(handel_rows, key=lambda r: -r[11]):
    print(r[0], r[10], round(r[11], 1))
wirte = hh["Schenk- und Gastwirthe"]
vieh = hh["Viehhändler"]
holz = hh["Holzhändler"]

# ---------------------------------------------------------------- industrial branches (extra table)
sg_by_area = {}
for r in zw:
    sg_by_area[r["area"]] = sg_by_area.get(r["area"], 0) + r["sg"]
land_share = sg_by_area["Plattland"] / sum(sg_by_area.values()) * 100
bau = {a: sum(r["sg"] for r in zw if r["branch"] == "Bauhandwerker" and r["area"] == a) for a in ["Städte", "Plattland"]}
bau_land_share = bau["Plattland"] / sum(bau.values()) * 100
print("zweige", sg_by_area, land_share, bau_land_share)

# ---------------------------------------------------------------- text
d1 = lambda x: num_de(x, 1)
e1 = lambda x: num_en(x, 1)
d0 = lambda x: num_de(x, 0)
e0 = lambda x: num_en(x, 0)

summary = bi(
    f"Die Erhebung von 1864 ordnet alle {num_de(pop)} Einwohner 13 Berufsklassen zu. Von der Industrie einschließlich des Handwerks lebten {d1(ind_z)} Prozent, von Land- und Forstwirtschaft {d1(agr_z)} Prozent; auch auf dem Plattland überwog die Industrie. "
    f"Größtes Gewerbe war die Weberei: Sie ernährte {num_de(weber['persons'])} Personen, mehr als ein Neuntel der Bevölkerung, fast zwei Drittel davon im Landesteil Schleiz.",
    f"The survey of 1864 assigns all {num_en(pop)} inhabitants to 13 occupational classes. {e1(ind_z)} percent lived from industry including crafts and {e1(agr_z)} percent from agriculture and forestry; even in the countryside industry predominated. "
    f"The largest trade was weaving: it supported {num_en(weber['persons'])} persons, more than one ninth of the population, almost two thirds of them in the district of Schleiz.",
)

findings = [
    bi(
        f"Im Landesteil Schleiz gehörten {d1(weber_sg_share['Schleiz'])} Prozent aller Selbständigen und Gehilfen der erfassten Gewerbe zur Weberei, in Gera {d1(weber_sg_share['Gera'])} und in Lobenstein-Ebersdorf {d1(weber_sg_share['Lobenstein-Ebersdorf'])} Prozent.",
        f"In the district of Schleiz {e1(weber_sg_share['Schleiz'])} percent of all self-employed and assistants in the recorded trades belonged to weaving, in Gera {e1(weber_sg_share['Gera'])} and in Lobenstein-Ebersdorf {e1(weber_sg_share['Lobenstein-Ebersdorf'])} percent.",
    ),
    bi(
        f"Auf einen selbständigen Maurer oder Steinhauer kamen {d1(g_per_s('Maurer, Steinhauer'))} Gehilfen, auf einen Zimmermann {d1(g_per_s('Zimmerleute'))}; unter den {len(big)} Gewerben mit mindestens 40 Selbständigen haben nur {len(more_g)} mehr Gehilfen als Selbständige.",
        f"For each self-employed mason or stonecutter there were {e1(g_per_s('Maurer, Steinhauer'))} assistants, for each carpenter {e1(g_per_s('Zimmerleute'))}; among the {len(big)} trades with at least 40 self-employed only {len(more_g)} have more assistants than masters.",
    ),
    bi(
        f"{d1(land_share)} Prozent der Selbständigen und Gehilfen der Industrie lebten auf dem Plattland; bei den Bauhandwerkern waren es {d1(bau_land_share)} Prozent. Brückner nennt das einen Wandel gegenüber dem Mittelalter.",
        f"{e1(land_share)} percent of the self-employed and assistants in industry lived in the countryside; among the building trades the share was {e1(bau_land_share)} percent. Brückner calls this a change from the Middle Ages.",
    ),
]

method = bi(
    "Die Berufsklassen stammen aus den Tabellen auf S. 209 bis 211 (13 Klassen mit Selbständigen, Gehilfen, Dienstboten und Familiengliedern, getrennt nach Städten und Plattland). "
    "Der Anteil einer Klasse ist ihre Summe geteilt durch die Summe aller Klassen im selben Gebiet und stimmt mit Brückners Prozentzahlen auf S. 212 überein. "
    "Die einzelnen Gewerbe stammen aus den Tabellen auf S. 252 bis 254 (68 Gewerbe nach Landesteilen); »ernährte Personen« ist die Summe aus Selbständigen, Gehilfen, Dienstboten und Familiengliedern. "
    "Fünf Gewerbe ohne jeden Eintrag fehlen. Das Diagramm zeigt die zwölf Gewerbe mit den meisten Personen; die Sammelposten »Fabrikarbeiter ohne angegebenen Fabrikzweig« und »Nichtbenannte Nahrungszweige« sind ausgenommen. Gesamtzahl und Rang sind aus den Zahlen der drei Landesteile berechnet. "
    "Die Zahlen zu Handel und Transport stehen für das Fürstentum auf S. 260; der Anteil der Städte bezieht sich auf die Selbständigen. "
    "Die Gewerbegruppen (Nahrung, Kleidung, Bauhandwerker, Hausausstattung, Sonstige) stehen auf S. 255; Städte und Plattland sind aus den Teilzahlen neu summiert, weil die gedruckten Summenspalten dort mehrfach abweichen. "
    "Striche im Druck sind leere Werte. Die Gewerbenamen sind ausgeschrieben, die Schreibweise ist die der Vorlage.",
    "The occupational classes come from the tables on pp. 209 to 211 (13 classes with self-employed, assistants, servants and family members, separately for towns and countryside). "
    "A class’s share is its total divided by the total of all classes in the same area and agrees with Brückner’s percentages on p. 212. "
    "The individual trades come from the tables on pp. 252 to 254 (68 trades by district); “persons supported” is the sum of self-employed, assistants, servants and family members. "
    "Five trades without any entry are missing. The chart shows the twelve trades with the most persons; the catch-all items “Fabrikarbeiter ohne angegebenen Fabrikzweig” (factory workers of unstated branch) and “Nichtbenannte Nahrungszweige” (unnamed food trades) are excluded. Totals and ranks are computed from the figures of the three districts. "
    "The figures for trade and transport are those for the principality on p. 260; the share of the towns refers to the self-employed. "
    "The trade groups (food, clothing, building, household goods, other) are on p. 255; towns and countryside are re-summed from the partial figures because the printed total columns deviate there in several places. "
    "Dashes in the print are empty values. Trade names are spelled out, spelling as in the source.",
)

caveats = [
    bi(
        "Die Zahlen gelten für 1864. Dienstboten und Familienglieder sind der Klasse des Haushaltsvorstands zugerechnet, die Personenzahlen eines Gewerbes zählen also ernährte Personen, nicht Erwerbstätige. Die Klasse »Industrie« schließt das Handwerk ein.",
        "The figures apply to 1864. Servants and family members are counted in the class of the head of household, so the number of persons in a trade counts persons supported, not people at work. The class “Industrie” includes crafts.",
    ),
    bi(
        "Im Druck stimmen einzelne Summen nicht: In Klasse 10 ergibt die Zeile Plattland Gera 56 statt der gedruckten 52, in Klasse 13 stehen für das Fürstentum 1780 statt 1786. Bei den Fleischern steht für Lobenstein-Ebersdorf 26 Familienglieder, die Summe verlangt 206; das Diagramm gibt den gedruckten Wert wieder.",
        "Some printed totals do not add up: in class 10 the row for the countryside of Gera gives 56 instead of the printed 52, in class 13 the principality shows 1780 instead of 1786. For butchers Lobenstein-Ebersdorf has 26 family members where the total requires 206; the chart shows the printed value.",
    ),
    bi(
        "Brückner hält die ermittelten Zahlen der Agenten und der Wirte in der Stadt Gera für »offenbar zu niedrig« und die Gesamtgröße des Handels für nicht ausreichend erhoben. Händler mit mehreren Zweigen sind nur einer Gruppe zugeordnet.",
        "Brückner considers the figures found for agents and innkeepers in the town of Gera “evidently too low” and the overall size of trade not sufficiently surveyed. Dealers with several lines of business are counted in one group only.",
    ),
    bi(
        "Welche Städte zur Stadtbevölkerung zählen, sagt die Tabelle nicht; Brückner kennt sechs Städte (Gera, Schleiz, Tanna, Lobenstein, Hirschberg, Saalburg). Offen bleibt auch, welche Klassen er als »producirend« zählt.",
        "The table does not say which places count as towns; Brückner knows six towns (Gera, Schleiz, Tanna, Lobenstein, Hirschberg, Saalburg). It also remains open which classes he counts as “producing”.",
    ),
]

transcription_issues = [
    {
        "page": "210", "block": "b1", "cell": "r30c8", "transcribed": "9", "facsimile": "9", "checked_facsimile": True,
        "note": "Klasse 10, Plattland Gera, Gehilfen: so gedruckt; die Landesteil-Summe 153 und die Zeilensumme 52 verlangen 5. / Printed as 9; the district total 153 and the row total 52 require 5.",
    },
    {
        "page": "211", "block": "b2", "cell": "r14c6", "transcribed": "1780", "facsimile": "1780", "checked_facsimile": True,
        "note": "Klasse 13, Fürstentum, Summe: so gedruckt; die Summe der Landesteile und der Spalten verlangt 1786. / Printed as 1780; the sum of the districts and of the columns requires 1786.",
    },
    {
        "page": "252", "block": "b4", "cell": "r6c13", "transcribed": "26", "facsimile": "26", "checked_facsimile": True,
        "note": "Fleischer, Lobenstein-Ebersdorf, Familienglieder: so gedruckt; die Spalte des Fürstentums (696) verlangt 206. / Printed as 26; the principality column (696) requires 206.",
    },
]

# ---------------------------------------------------------------- charts
c1 = {
    "id": "c1",
    "dataset": "klassen",
    "title": bi(
        "Auch auf dem Land lebten mehr Menschen vom Gewerbe als von der Landwirtschaft",
        "Even in the countryside more people lived from industry and crafts than from agriculture",
    ),
    "caption": bi(
        f"Anteil der 13 Berufsklassen an der Bevölkerung der Städte ({num_de(klasse(14, 'Städte')['summe'])} Einwohner) und des Plattlandes ({num_de(klasse(14, 'Plattland')['summe'])}) im Fürstentum 1864, in Prozent; sortiert nach dem Anteil an der ganzen Bevölkerung. Quelle: S. 209 bis 212.",
        f"Share of the 13 occupational classes in the population of the towns ({num_en(klasse(14, 'Städte')['summe'])} inhabitants) and of the countryside ({num_en(klasse(14, 'Plattland')['summe'])}) in the principality in 1864, percent; sorted by the share in the whole population. Source: pp. 209 to 212.",
    ),
    "vegalite": {
        "height": {"step": 25},
        "transform": [
            {"filter": "datum.landestheil_de == 'Fürstentum' && datum.klasse_nr < 14"},
            {"pivot": "gebiet_de", "value": "share_pct", "groupby": ["klasse_nr", "klasse_kurz_de", "klasse_kurz_en"]},
            {"calculate": {
                "de": "datum.klasse_nr == 3 ? 'Städte ' + format(datum['Städte'], '.1f') : format(datum['Städte'], '.1f')",
                "en": "datum.klasse_nr == 3 ? 'Towns ' + format(datum['Städte'], '.1f') : format(datum['Städte'], '.1f')"}, "as": "label_staedte"},
            {"calculate": {
                "de": "datum.klasse_nr == 3 ? 'Plattland ' + format(datum['Plattland'], '.1f') : format(datum['Plattland'], '.1f')",
                "en": "datum.klasse_nr == 3 ? 'Countryside ' + format(datum['Plattland'], '.1f') : format(datum['Plattland'], '.1f')"}, "as": "label_plattland"},
        ],
        "encoding": {
            "y": {
                "field": {"de": "klasse_kurz_de", "en": "klasse_kurz_en"}, "type": "nominal",
                "sort": {"field": "zusammen", "op": "min", "order": "descending"},
                "axis": {"title": None, "labelLimit": 340, "labelFontSize": 12},
            },
        },
        "layer": [
            {
                "mark": {"type": "rule", "strokeWidth": 3, "color": "@context"},
                "encoding": {
                    "x": {"field": "Städte", "type": "quantitative", "scale": {"domain": [-3, 74]}, "axis": {"title": {"de": "Anteil an der Bevölkerung, %", "en": "Share of the population, %"}, "values": [0, 10, 20, 30, 40, 50, 60, 70]}},
                    "x2": {"field": "Plattland"},
                },
            },
            {
                "mark": {"type": "point", "filled": True, "size": 90, "color": "@accent", "opacity": 1},
                "encoding": {
                    "x": {"field": "Städte", "type": "quantitative"},
                    "tooltip": [
                        {"field": {"de": "klasse_kurz_de", "en": "klasse_kurz_en"}, "type": "nominal", "title": bi("Berufsklasse", "Occupational class")},
                        tooltip("Städte", "Städte, %", "Towns, %", ".1f"),
                        tooltip("Plattland", "Plattland, %", "Countryside, %", ".1f"),
                        tooltip("zusammen", "Fürstentum, %", "Principality, %", ".1f"),
                    ],
                },
            },
            {
                "mark": {"type": "point", "filled": True, "size": 90, "color": "@accent2", "opacity": 1},
                "encoding": {
                    "x": {"field": "Plattland", "type": "quantitative"},
                    "tooltip": [
                        {"field": {"de": "klasse_kurz_de", "en": "klasse_kurz_en"}, "type": "nominal", "title": bi("Berufsklasse", "Occupational class")},
                        tooltip("Städte", "Städte, %", "Towns, %", ".1f"),
                        tooltip("Plattland", "Plattland, %", "Countryside, %", ".1f"),
                        tooltip("zusammen", "Fürstentum, %", "Principality, %", ".1f"),
                    ],
                },
            },
            {
                "transform": [{"filter": "datum.klasse_nr == 1 || datum.klasse_nr == 3 || datum.klasse_nr == 6"}],
                "mark": {"type": "text", "align": "center", "dy": -13, "style": "label", "color": "@accent"},
                "encoding": {"x": {"field": "Städte", "type": "quantitative"}, "text": {"field": "label_staedte", "type": "nominal"}},
            },
            {
                "transform": [{"filter": "datum.klasse_nr == 1 || datum.klasse_nr == 3 || datum.klasse_nr == 6"}],
                "mark": {"type": "text", "align": "center", "dy": -13, "style": "label", "color": "@accent2"},
                "encoding": {"x": {"field": "Plattland", "type": "quantitative"}, "text": {"field": "label_plattland", "type": "nominal"}},
            },
        ],
    },
}

DIST_RANGE = DISTRICT_COLORS
c2 = {
    "id": "c2",
    "dataset": "gewerbe",
    "title": bi(
        "Die Weberei ernährte doppelt so viele Menschen wie jedes andere Gewerbe, fast zwei Drittel in Schleiz",
        "Weaving supported twice as many people as any other trade, almost two thirds in Schleiz",
    ),
    "caption": bi(
        f"Die zwölf größten Gewerbe (ohne Sammelposten) nach ernährten Personen (Selbständige, Gehilfen, Dienstboten, Familienglieder) im Fürstentum 1864, nach Landesteilen. Weber: {num_de(weber['persons'])}, davon {num_de(weber['d']['Schleiz']['persons'])} in Schleiz. Quelle: S. 252 bis 254.",
        f"The twelve largest trades (without catch-all items) by persons supported (self-employed, assistants, servants, family members) in the principality in 1864, by district. Weavers: {num_en(weber['persons'])}, of them {num_en(weber['d']['Schleiz']['persons'])} in Schleiz. Source: pp. 252 to 254.",
    ),
    "vegalite": {
        "height": {"step": 25},
        "transform": [
            {"filter": "isValid(datum.rang) && datum.rang <= 12"},
            {"calculate": "datum.district == 'Gera' ? 1 : datum.district == 'Schleiz' ? 2 : 3", "as": "dnr"},
            {"stack": "persons", "groupby": ["trade"], "sort": [{"field": "dnr", "order": "ascending"}], "offset": "zero", "as": ["x0", "x1"]},
            {"calculate": "(datum.x0 + datum.x1) / 2", "as": "xm"},
        ],
        "encoding": {
            "y": {
                "field": {"de": "trade", "en": "trade_en"}, "type": "nominal",
                "sort": {"field": "persons_total", "op": "min", "order": "descending"},
                "axis": {"title": None, "labelLimit": 330, "labelFontSize": 12},
            },
        },
        "layer": [
            {
                "mark": {"type": "bar", "height": {"band": 0.74}},
                "encoding": {
                    "x": {"field": "x0", "type": "quantitative", "axis": {"title": {"de": "ernährte Personen", "en": "persons supported"}, "format": ",d", "values": [0, 2000, 4000, 6000, 8000, 10000]}, "scale": {"domain": [0, 11800]}},
                    "x2": {"field": "x1"},
                    "color": {
                        "field": "district", "type": "nominal", "legend": None,
                        "scale": {"domain": DISTRICTS, "range": DIST_RANGE},
                    },
                    "tooltip": [
                        {"field": {"de": "trade", "en": "trade_en"}, "type": "nominal", "title": bi("Gewerbe", "Trade")},
                        tooltip("district", "Landesteil", "District"),
                        tooltip("persons", "Personen", "Persons", ",d"),
                        tooltip("s", "Selbständige", "Self-employed", ",d"),
                        tooltip("g", "Gehilfen", "Assistants", ",d"),
                    ],
                },
            },
            {
                "transform": [{"filter": "datum.rang == 1"}],
                "mark": {"type": "text", "style": "label", "dy": -23},
                "encoding": {"x": {"field": "xm", "type": "quantitative"}, "text": {"field": "district", "type": "nominal"}},
            },
            {
                "transform": [{"aggregate": [{"op": "sum", "field": "persons", "as": "total"}], "groupby": ["trade", "trade_en", "persons_total"]}],
                "mark": {"type": "text", "align": "left", "dx": 6, "style": "label"},
                "encoding": {"x": {"field": "total", "type": "quantitative"}, "text": {"field": "total", "type": "quantitative", "format": ",d"}},
            },
        ],
    },
}

c3 = {
    "id": "c3",
    "dataset": "handel_fuerstentum",
    "title": bi(
        "Wirte, Viehhändler und Holzhändler saßen auf dem Land, Bankiers, Agenten und Buchhändler in den Städten",
        "Innkeepers, cattle and timber dealers sat in the countryside, bankers, agents and booksellers in towns",
    ),
    "caption": bi(
        f"Anteil der Selbständigen in den Städten an allen Selbständigen des jeweiligen Handels- und Transportgewerbes im Fürstentum 1864, in Prozent; in Klammern die Zahl der Selbständigen. Wirte: {wirte[2]} von {wirte[10]} in den Städten. Quelle: S. 260.",
        f"Share of the self-employed living in the towns among all self-employed of each trade or transport business in the principality in 1864, percent; in brackets the number of self-employed. Innkeepers: {wirte[2]} of {wirte[10]} in the towns. Source: p. 260.",
    ),
    "vegalite": {
        "height": {"step": 24},
        "transform": [{"calculate": "50", "as": "mitte"}],
        "encoding": {
            "y": {
                "field": {"de": "label_de", "en": "label_en"}, "type": "nominal",
                "sort": {"field": "share_staedte", "op": "min", "order": "descending"},
                "axis": {"title": None, "labelLimit": 380, "labelFontSize": 12},
            },
        },
        "layer": [
            {"mark": {"type": "rule", "strokeDash": [3, 3], "color": "@muted"}, "encoding": {"x": {"datum": 50}, "y": None}},
            {
                "mark": {"type": "rule", "strokeWidth": 3},
                "encoding": {
                    "x": {"field": "mitte", "type": "quantitative"},
                    "x2": {"field": "share_staedte"},
                    "color": {"condition": {"test": "datum.share_staedte >= 50", "value": "@accent"}, "value": "@accent2"},
                },
            },
            {
                "mark": {"type": "point", "filled": True, "size": 90, "opacity": 1},
                "encoding": {
                    "x": {
                        "field": "share_staedte", "type": "quantitative", "scale": {"domain": [0, 114]},
                        "axis": {
                            "title": {"de": "Anteil der Selbständigen in den Städten, %", "en": "Share of the self-employed in the towns, %"},
                            "values": [0, 25, 50, 75, 100],
                        },
                    },
                    "color": {"condition": {"test": "datum.share_staedte >= 50", "value": "@accent"}, "value": "@accent2"},
                    "tooltip": [
                        {"field": {"de": "trade", "en": "trade_en"}, "type": "nominal", "title": bi("Gewerbe", "Trade")},
                        tooltip("s_staedte", "Selbständige in den Städten", "Self-employed in the towns", ",d"),
                        tooltip("s_plattland", "Selbständige auf dem Plattland", "Self-employed in the countryside", ",d"),
                        tooltip("share_staedte", "Anteil der Städte, %", "Share of the towns, %", ".1f"),
                    ],
                },
            },
            {
                "transform": [{"filter": "datum.share_staedte >= 50"}],
                "mark": {"type": "text", "align": "left", "dx": 9, "style": "label"},
                "encoding": {"x": {"field": "share_staedte", "type": "quantitative"}, "text": {"field": "share_staedte", "type": "quantitative", "format": ".0f"}},
            },
            {
                "transform": [{"filter": "datum.share_staedte < 50"}],
                "mark": {"type": "text", "align": "right", "dx": -9, "style": "label"},
                "encoding": {"x": {"field": "share_staedte", "type": "quantitative"}, "text": {"field": "share_staedte", "type": "quantitative", "format": ".0f"}},
            },
            {
                "transform": [{"filter": "datum.trade == 'Banquiers'"}],
                "mark": {"type": "text", "align": "right", "dx": -8, "style": "label", "color": "@accent"},
                "encoding": {"x": {"datum": 50}, "text": {"value": {"de": "Städte überwiegen", "en": "towns predominate"}}},
            },
            {
                "transform": [{"filter": "datum.trade == 'Viehhändler'"}],
                "mark": {"type": "text", "align": "left", "dx": 8, "style": "label", "color": "@accent2"},
                "encoding": {"x": {"datum": 50}, "text": {"value": {"de": "Plattland überwiegt", "en": "countryside predominates"}}},
            },
        ],
    },
}

datasets = [klassen, gewerbe, handel, zweige]

feature = {
    "id": ID,
    "title": bi("Berufe, Gewerbe und Industrie 1864", "Occupations, trades and industry in 1864"),
    "category": "economy",
    "section": "t1-3-1",
    "merges": [A_KL, A_GW, A_ZW, A_HA],
    "sources": [
        {"page": "209", "block": "b3"}, {"page": "210", "block": "b1"}, {"page": "211", "block": "b1"}, {"page": "211", "block": "b2"}, {"page": "212", "block": "b2"},
        {"page": "252", "block": "b4"}, {"page": "253", "block": "b1"}, {"page": "254", "block": "b1"}, {"page": "255", "block": "b1"}, {"page": "256", "block": "b1"},
        {"page": "260", "block": "b1"},
    ],
    "summary": summary,
    "findings": findings,
    "method": method,
    "caveats": caveats,
    "transcription_issues": transcription_issues,
    "datasets": datasets,
    "charts": [c1, c2, c3],
    "keywords": {
        "de": ["Berufe", "Berufsklassen", "Gewerbe", "Industrie", "Handwerk", "Weberei", "Handel", "Wirte", "Städte", "Plattland"],
        "en": ["occupations", "occupational classes", "trades", "industry", "crafts", "weaving", "trade", "innkeepers", "towns", "countryside"],
    },
    "related": ["landwirtschaft", "handel-verkehr", "dorfleben", "bergbau"],
    "generated_by": "Claude Sonnet 5.5 (Agent F5), aus 4 Einzelauswertungen zusammengeführt",
    "date": "2026-10-02",
}

if __name__ == "__main__":
    for k in ["title", "summary"]:
        for lang in ["de", "en"]:
            print(k, lang, words(feature[k][lang]))
    write_feature(feature)
    validate(ID)
