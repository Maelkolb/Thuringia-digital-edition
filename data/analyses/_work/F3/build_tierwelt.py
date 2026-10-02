import sys, collections
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\F3")
from common import *

MERGES = [
    "fauna-artenzahlen-tiergruppen",
    "fauna-fische-gewaesser",
    "fauna-voegel-unterland-oberland",
    "fauna-voegel-zugzeiten-und-seltene-gaeste",
    "fauna-aenderungen-seit-1647",
    "fauna-tiernamen-in-flurnamen",
]

# ---------------------------------------------------------------- c1: changes
changes = dataset("fauna-aenderungen-seit-1647", "timeline")
YEAR_LABELS = {
    "Bär: letzte drei erlegt": ("um 1730", "c. 1730"),
    "Luchs ausgerottet": ("um 1730", "c. 1730"),
    "Wolf ausgerottet": ("1750 bis 1769", "1750 to 1769"),
    "Heuschreckenzüge enden": ("vor 1769", "before 1769"),
    "Hausrotschwanz im Oberland": ("um 1795", "c. 1795"),
    "Star nimmt stark zu": ("seit etwa 1809", "since c. 1809"),
    "Rotwild fehlt im Unterland": ("seit 1848", "since 1848"),
    "Wacholderdrossel brütet": ("seit etwa 1859", "since c. 1859"),
    "Gerstenammer im Unterland": ("1864 bis 1868", "1864 to 1868"),
    "Rohrammer im Oberland": ("seit etwa 1864", "since c. 1864"),
    "Kreuzschnabel brütet (Gera)": ("Winter 1867/68", "winter 1867/68"),
    "Elster nimmt wieder zu": ("seit etwa 1867", "since c. 1867"),
    "Großer Würger wieder da": ("Sommer 1869", "summer 1869"),
}
order_of = {}
shown = [d for d in dicts(changes) if d["kind_key"] != "event"]
shown.sort(key=lambda d: (d["year_ref"], d["year_from"], d["label_de"]))
for i, d in enumerate(shown, start=1):
    order_of[d["label_de"]] = i


def fn_changes(d):
    yl = YEAR_LABELS.get(d["label_de"], (None, None))
    short = {"loss": ("Verlust", "Loss"), "gain": ("Zuwanderung, Zunahme", "Arrival, increase"), "event": ("Ereignis", "Event")}[d["kind_key"]]
    return [yl[0], yl[1], order_of.get(d["label_de"]), short[0], short[1]]


add_columns(
    changes,
    [
        col("year_label_de", "Zeitangabe für die Grafik", "Time label for the chart", "string", None, True, "redaktionell aus den gedruckten Zeitangaben"),
        col("year_label_en", "Zeitangabe (en)", "Time label (en)", "string", None, True),
        col("chart_order", "Reihenfolge in der Grafik", "Order in the chart", "integer", None, True),
        col("kind_short_de", "Art der Veränderung (kurz)", "Kind of change (short)", "string", None, True),
        col("kind_short_en", "Art der Veränderung (kurz, en)", "Kind of change (short, en)", "string", None, True),
    ],
    fn_changes,
)
losses = [d for d in shown if d["kind_key"] == "loss"]
gains = [d for d in shown if d["kind_key"] == "gain"]
gains_recent = [d for d in gains if d["year_ref"] >= 1859]
print("losses", len(losses), "gains", len(gains), "recent", len(gains_recent))
bird_gains = len(gains)  # all gains are birds (checked below)
assert all(d["taxon_de"] in ("Hausrothschwänzchen", "Staar", "Wachholderdrossel", "Gersten- oder Grauammer", "Rohrammer", "Kreuzschnabel", "Elster", "Großer Würger") for d in gains), [d["taxon_de"] for d in gains]
events = [d for d in dicts(changes) if d["kind_key"] == "event"]

# ---------------------------------------------------------------- c2: names
names = dataset("fauna-tiernamen-in-flurnamen", "names")
nd = dicts(names)
count = collections.Counter(d["animal_de"] for d in nd)
status_of = {d["animal_de"]: d["status_de"] for d in nd}
ranking = sorted(count, key=lambda a: (-count[a], a))
rank_of = {a: i + 1 for i, a in enumerate(ranking)}
running = collections.Counter()
ks = []
for d in nd:
    running[d["animal_de"]] += 1
    ks.append(running[d["animal_de"]])


EXTINCT_NOTE = {
    "Bär": ("um 1730 ausgerottet", "exterminated around 1730"),
    "Luchs": ("um 1730 ausgerottet", "exterminated around 1730"),
    "Wolf": ("seit etwa einem Jahrhundert ausgerottet", "exterminated for about a century"),
    "Wisent": ("längst verschwunden", "long gone"),
}


def fn_names(d):
    idx = fn_names.i
    fn_names.i += 1
    note = EXTINCT_NOTE.get(d["animal_de"], (None, None)) if ks[idx] == 1 else (None, None)
    return [count[d["animal_de"]], rank_of[d["animal_de"]], ks[idx], 1 if d["status_de"].startswith("ausgerottet") else 2, note[0], note[1]]


fn_names.i = 0
add_columns(
    names,
    [
        col("n_animal", "Namen zu diesem Tier", "Names for this animal", "integer", "Namen", True),
        col("animal_rank", "Rang des Tiers", "Rank of the animal", "integer", None, True),
        col("k", "Laufnummer innerhalb des Tiers", "Running number within the animal", "integer", None, True),
        col("status_order", "Ordnung des Status", "Status order", "integer", None, True),
        col("note_de", "Anmerkung für die Grafik", "Note for the chart", "string", None, True, "nach Brückner S. 82 f.; nur bei der ersten Zeile eines ausgerotteten Tiers"),
        col("note_en", "Anmerkung (en)", "Note (en)", "string", None, True),
    ],
    fn_names,
)
extinct_names = sum(1 for d in nd if d["status_de"].startswith("ausgerottet"))
extinct_animals = sorted({d["animal_de"] for d in nd if d["status_de"].startswith("ausgerottet")})
total_names = len(nd)
mammal_names = sum(1 for d in nd if d["group_de"] == "Säugetier")
print("names", total_names, "extinct", extinct_names, extinct_animals, "share", extinct_names / total_names)

# ---------------------------------------------------------------- c3: fish
fish = dataset("fauna-fische-gewaesser", "fish_cells")
species = {d["species_no"]: d for d in dicts(dataset("fauna-fische-gewaesser", "fish_species"))}
fd = dicts(fish)
n_waters = collections.Counter()
for d in fd:
    if d["status_key"] != "absent":
        n_waters[d["species_no"]] += 1
species_order = sorted(species, key=lambda no: (-n_waters[no], no))
rank = {no: i + 1 for i, no in enumerate(species_order)}
water_order = {"saale": 1, "elster": 2, "wiesenthal": 3, "teiche": 4}
per_water = collections.Counter()
for d in fd:
    if d["status_key"] != "absent":
        per_water[d["water_key"]] += 1
print("per water", per_water)
WATER_LABEL = {
    "saale": ("Saale", "Saale"),
    "elster": ("Elster", "Elster"),
    "wiesenthal": ("Wiesenthal", "Wiesenthal"),
    "teiche": ("Teiche", "Ponds"),
}


def decline(d):
    t = (d["cell_text"] or "").lower()
    return any(w in t for w in ("jetzt", "früher", "sonst"))


decline_cells = [d for d in fd if decline(d)]
print("decline", [(d["species_label"], d["water_key"], d["cell_text"]) for d in decline_cells])
decline_species = sorted({species[d["species_no"]]["name_de"] for d in decline_cells})


def mark_key(d):
    if d["status_key"] == "absent":
        return ("none", 4, "nicht angegeben", "not given")
    if decline(d):
        return ("decline", 2, "Rückgang vermerkt", "decline noted")
    if d["status_key"] == "uncertain":
        return ("doubtful", 3, "fraglich", "doubtful")
    return ("named", 1, "genannt", "named")


def fn_fish(d):
    sp = species[d["species_no"]]
    nm_de = sp["name_de"] or sp["name_printed"]
    nm_en = sp["name_en"] or sp["name_printed"]
    mk = mark_key(d)
    wl = WATER_LABEL[d["water_key"]]
    return [
        nm_de,
        nm_en,
        n_waters[d["species_no"]],
        rank[d["species_no"]],
        mk[0],
        mk[1],
        mk[2],
        mk[3],
        water_order[d["water_key"]],
        f"{wl[0]} ({per_water[d['water_key']]})",
        f"{wl[1]} ({per_water[d['water_key']]})",
    ]


add_columns(
    fish,
    [
        col("name_de", "Name heute", "Name today", "string", None, True, "nur dort, wo die Zuordnung sicher ist; sonst der gedruckte zoologische Name"),
        col("name_en", "Name heute (en)", "Name today (en)", "string", None, True),
        col("n_waters", "Gewässer mit Angabe", "Waters with an entry", "integer", None, True),
        col("species_rank", "Rang für die Sortierung", "Sort rank", "integer", None, True),
        col("mark_key", "Darstellung", "Mark", "string", None, True),
        col("mark_order", "Ordnung der Darstellung", "Mark order", "integer", None, True),
        col("mark_de", "Darstellung (Text)", "Mark (text)", "string", None, True),
        col("mark_en", "Darstellung (en)", "Mark (en)", "string", None, True),
        col("water_order", "Ordnung des Gewässers", "Water order", "integer", None, True),
        col("water_label_de", "Gewässer mit Artenzahl", "Water with species count", "string", None, True),
        col("water_label_en", "Gewässer mit Artenzahl (en)", "Water with species count (en)", "string", None, True),
    ],
    fn_fish,
)
n_species = len(species)

# ---------------------------------------------------------------- overview table
counts = dataset("fauna-artenzahlen-tiergruppen", "overview")
cd = {d["group_key"]: d for d in dicts(counts)}
vertebrates = cd["birds"]["species"] + cd["mammals"]["species"] + cd["fish"]["species"] + cd["reptiles"]["species"]
print("vertebrates", vertebrates)

# ---------------------------------------------------------------- vega-lite specs
KIND_COLOR = {"field": {"de": "kind_short_de", "en": "kind_short_en"}, "type": "nominal", "sort": {"field": "kind_order", "op": "min"}, "scale": {"range": ["@negative", "@positive"]}}

c1 = {
    "height": {"step": 23},
    "transform": [{"filter": "datum.kind_key != 'event'"}],
    "encoding": {
        "y": {
            "field": {"de": "label_de", "en": "label_en"},
            "type": "nominal",
            "sort": {"field": "chart_order", "op": "min"},
            "axis": {"title": None, "labelLimit": 320, "grid": True},
        },
    },
    "layer": [
        {
            "transform": [{"filter": "datum.year_from != datum.year_to"}],
            "mark": {"type": "rule", "strokeWidth": 7, "strokeCap": "round", "opacity": 0.3},
            "encoding": {
                "x": {
                    "field": "year_from",
                    "type": "quantitative",
                    "scale": {"domain": [1700, 1925], "nice": False},
                    "axis": {"format": "d", "values": [1700, 1750, 1800, 1850], "title": None, "grid": True},
                },
                "x2": {"field": "year_to"},
                "color": {"condition": {"test": "datum.kind_key == 'loss'", "value": "@negative"}, "value": "@positive"},
            },
        },
        {
            "mark": {"type": "circle", "size": 110},
            "encoding": {
                "x": {"field": "year_ref", "type": "quantitative"},
                "color": {**KIND_COLOR, "legend": None},
                "tooltip": [
                    tip({"de": "label_de", "en": "label_en"}, "Angabe", "Entry"),
                    tip({"de": "year_label_de", "en": "year_label_en"}, "Zeit", "Time"),
                    tip({"de": "basis_de", "en": "basis_en"}, "Grundlage", "Basis"),
                    tip({"de": "precision_de", "en": "precision_en"}, "Genauigkeit", "Precision"),
                ],
            },
        },
        {
            "mark": {"type": "text", "style": "label-muted", "align": "left", "dx": 11},
            "encoding": {
                "x": {"field": "year_to", "type": "quantitative"},
                "text": {"field": {"de": "year_label_de", "en": "year_label_en"}},
                "color": {"value": "@ink2"},
            },
        },
        {
            "transform": [{"filter": "datum.label_de == 'Luchs ausgerottet'"}],
            "mark": {"type": "text", "style": "label", "align": "left"},
            "encoding": {
                "x": {"datum": 1795},
                "text": {"value": bi("Verlust oder Rückgang", "Loss or decline")},
                "color": {"value": "@negative"},
            },
        },
        {
            "transform": [{"filter": "datum.label_de == 'Rohrammer im Oberland'"}],
            "mark": {"type": "text", "style": "label", "align": "left"},
            "encoding": {
                "x": {"datum": 1715},
                "text": {"value": bi("Zuwanderung oder Zunahme", "Arrival or increase")},
                "color": {"value": "@positive"},
            },
        },
    ],
}

c2 = {
    "height": {"step": 14},
    "encoding": {
        "y": {
            "field": {"de": "animal_de", "en": "animal_en"},
            "type": "nominal",
            "sort": {"field": "animal_rank", "op": "min"},
            "axis": {"title": None, "labelFontSize": 11.5, "labelLimit": 200},
        },
        "x": {"field": "k", "type": "quantitative", "scale": {"domain": [0.5, 16]}, "axis": None},
    },
    "layer": [
        {
            "mark": {"type": "circle", "size": 95},
            "encoding": {
                "color": {
                    "condition": {"test": "datum.status_order == 1", "value": "@negative"},
                    "value": "@context",
                },
                "tooltip": [
                    tip("name", "Name", "Name"),
                    tip({"de": "animal_de", "en": "animal_en"}, "Tier", "Animal"),
                    tip({"de": "group_de", "en": "group_en"}, "Gruppe", "Group"),
                    tip({"de": "status_de", "en": "status_en"}, "Bestand nach Brückner", "Status according to Brückner"),
                ],
            },
        },
        {
            "transform": [{"filter": "datum.k == datum.n_animal && datum.status_order == 1"}],
            "mark": {"type": "text", "style": "label", "align": "left", "dx": 11},
            "encoding": {"text": {"field": "n_animal"}, "color": {"value": "@negative"}},
        },
        {
            "transform": [{"filter": "isValid(datum.note_de)"}],
            "mark": {"type": "text", "style": "annotation", "align": "left"},
            "encoding": {
                "x": {"datum": 8.6},
                "text": {"field": {"de": "note_de", "en": "note_en"}},
                "color": {"value": "@negative"},
            },
        },
    ],
}

c3 = {
    "height": {"step": 12.5},
    "encoding": {
        "y": {
            "field": {"de": "name_de", "en": "name_en"},
            "type": "nominal",
            "sort": {"field": "species_rank", "op": "min"},
            "axis": {"title": None, "labelFontSize": 10.5, "labelLimit": 320, "grid": False},
        },
        "x": {
            "field": {"de": "water_label_de", "en": "water_label_en"},
            "type": "nominal",
            "sort": {"field": "water_order", "op": "min"},
            "axis": {"title": None, "orient": "top", "labelAngle": 0, "labelFontSize": 12, "labelFontWeight": 600},
        },
    },
    "layer": [
        {
            "transform": [{"filter": "datum.mark_key == 'none'"}],
            "mark": {"type": "circle", "size": 14, "color": "@context"},
        },
        {
            "transform": [{"filter": "datum.mark_key != 'none'"}],
            "mark": {"type": "circle", "size": 85},
            "encoding": {
                "color": {
                    "field": {"de": "mark_de", "en": "mark_en"},
                    "type": "nominal",
                    "sort": {"field": "mark_order", "op": "min"},
                    "scale": {"range": ["@accent", "@negative", "@muted"]},
                    "legend": {"title": None},
                },
                "tooltip": [
                    tip("species_label", "Art (gedruckt)", "Species (as printed)"),
                    tip({"de": "name_de", "en": "name_en"}, "Name heute", "Name today"),
                    tip({"de": "water_de", "en": "water_en"}, "Gewässer", "Water"),
                    tip("cell_text", "Angabe im Druck", "Entry in print"),
                ],
            },
        },
    ],
}

# ---------------------------------------------------------------- texts
n_changes = len(shown)
share_names = extinct_names / total_names * 100
summary_de = (
    f"Brückner nennt für das Fürstentum rund {n_de(round(vertebrates, -1))} Wirbeltierarten und {n_de(cd['butterflies']['species'])} Schmetterlinge bei Zeulenroda. "
    f"Datierbare Angaben zeigen den Wandel: Bären, Luchse und Wölfe verschwanden im 18. Jahrhundert, {n_de(len(gains_recent))} der {n_de(len(gains))} neuen oder häufigeren Vogelarten kamen seit 1859. "
    f"Von den {n_de(n_species)} Fischarten der Gewässer sind einige im Rückgang."
)
summary_en = (
    f"Brückner lists around {n_en(round(vertebrates, -1))} vertebrate species for the principality and {n_en(cd['butterflies']['species'])} butterflies and moths near Zeulenroda. "
    f"Dated remarks show the change: bears, lynxes and wolves vanished in the 18th century, {len(gains_recent)} of {len(gains)} newly arrived or more common bird species date from 1859 or later. "
    f"Of the {n_species} fish species of the waters, some are declining."
)
print(words(summary_de), words(summary_en))

wolf = next(d for d in shown if d["label_de"] == "Wolf ausgerottet")
rotwild = next(d for d in shown if d["label_de"].startswith("Rotwild"))
finding1_de = (
    f"Die letzten drei Bären und die Luchse fallen um 1730, die Wölfe zwischen 1750 und 1769 (abgeleitet). Das Rotwild fehlt im Unterland seit {rotwild['year_ref']}. "
    f"Alle {len(gains)} Zunahmen betreffen Vögel."
)
finding1_en = (
    f"The last three bears and the lynxes fall around 1730, the wolves between 1750 and 1769 (derived). Red deer have been absent from the Unterland since {rotwild['year_ref']}. "
    f"All {len(gains)} increases concern birds."
)
finding2_de = (
    f"{n_de(extinct_names)} von {n_de(total_names)} Flur- und Ortsnamen mit Tierbezug ({n_de(share_names)} Prozent) gehören zu Wolf, Bär, Luchs und Wisent. "
    f"Wolf ({count['Wolf']}) und Bär ({count['Bär']}) sind die häufigsten Tiere in Namen."
)
finding2_en = (
    f"{n_en(extinct_names)} of {n_en(total_names)} field and place names with an animal element ({n_en(share_names)} percent) belong to wolf, bear, lynx and bison. "
    f"Wolf ({count['Wolf']}) and bear ({count['Bär']}) are the most frequent animals in names."
)
finding2_de = finding2_de.replace(n_de(share_names), n_de(round(share_names)))
finding2_en = finding2_en.replace(n_en(share_names), n_en(round(share_names)))
finding3_de = (
    f"Brückner führt {n_species} Fischarten auf: {per_water['saale']} für die Saale, {per_water['elster']} für die Elster, {per_water['wiesenthal']} für die Wiesenthal und {per_water['teiche']} für die Teiche. "
    f"Einen Rückgang vermerken {len(decline_cells)} Angaben, so bei Lachs, Äsche und Quappe."
)
finding3_en = (
    f"Brückner lists {n_species} fish species: {per_water['saale']} for the Saale, {per_water['elster']} for the Elster, {per_water['wiesenthal']} for the Wiesenthal and {per_water['teiche']} for the ponds. "
    f"{len(decline_cells)} entries note a decline, among them salmon, grayling and burbot."
)
print(decline_species)

title_c1 = bi(
    f"Raubtiere verschwanden im 18. Jahrhundert, {len(gains)} Vogelarten kamen hinzu oder nahmen zu",
    f"Large predators vanished in the 18th century; {len(gains)} bird species arrived or increased",
)
title_c2 = bi(
    f"Wolf, Bär, Luchs und Wisent sind verschwunden, doch {extinct_names} Namen erinnern an sie",
    f"Wolf, bear, lynx and bison are gone, yet {extinct_names} place and field names recall them",
)
title_c3 = bi(
    f"Saale und Elster nennen fast alle {n_species} Fischarten, die Teiche nur {per_water['teiche']}",
    f"The Saale and Elster have almost all {n_species} fish species, the ponds only {per_water['teiche']}",
)
caption_c1 = bi(
    f"Datierbare Veränderungen nach Brückner. Punkt: Jahr oder Mitte der Zeitspanne, Balken: Zeitspanne. Relative Angaben (»seit fünf Jahren«) sind von 1869 aus gerechnet. Weitere Ereignisse ohne Bestandsänderung ({len(events)}) stehen nur in der Tabelle. S. 82–90, 831.",
    f"Dated changes according to Brückner. Dot: year or middle of the span, bar: span. Relative statements (“for five years”) are counted back from 1869. Further events without a change in numbers ({len(events)}) are in the table only. Pp. 82–90, 831.",
)
caption_c2 = bi(
    f"Jeder Punkt ist ein Flur- oder Ortsname, den Brückner einem Tier zuordnet ({total_names} Namen, {len(count)} Tiere); rot: Tiere, die nach ihm ausgerottet sind oder verschwunden. S. 82–83.",
    f"Each dot is a field or place name that Brückner assigns to an animal ({total_names} names, {len(count)} animals); red: animals that he says are exterminated or gone. Pp. 82–83.",
)
caption_c3 = bi(
    "Brückners Tabelle der Fische nach Gewässern. Jede Zeile eine Art, sortiert nach Zahl der Gewässer; heutige Namen nur, wo die Zuordnung sicher ist. »Rückgang«: Angabe wie »jetzt sehr selten« oder »früher«. S. 87–88.",
    "Brückner’s table of fish by water. One row per species, sorted by number of waters; modern names only where the identification is certain. “Decline”: entries such as “now very rare” or “formerly”. Pp. 87–88.",
)

method_de = (
    "Die Zeitleiste fasst alle Angaben zusammen, die Brückner mit einem Jahr oder einem relativen Zeitbezug versieht (S. 82–90, 831). Relative Angaben wie »seit 60 Jahren« wurden von 1869 aus in ein ungefähres Jahr umgerechnet; sie sind als abgeleitet gekennzeichnet. "
    "Die Tiernamen in Flur- und Ortsnamen stammen aus Brückners Liste auf S. 82 und wurden nach dem Wortstamm einem Tier zugeordnet; ob ein Tier im Land vorkommt, richtet sich nach seinen Aussagen auf S. 82–83. "
    "Die Fischtabelle (S. 87–88, 34 Arten mal 4 Gewässer) wurde vollständig übernommen. Eine Angabe gilt als Rückgang, wenn sie »jetzt«, »früher« oder »sonst« enthält. Die heutigen Namen gelten nur dort, wo die Zuordnung sicher ist. "
    "Die Artenzahlen nach Tiergruppen stehen in der ergänzenden Tabelle; sie sind teils ungefähre Angaben (Vögel »ca. 280«) und gelten bei den Schmetterlingen nur für die Umgebung von Zeulenroda. "
    "Die Auswertungen der Vogelarten nach Unterland und Oberland, der Zugzeiten und der seltenen Gäste sind in dieses Stück nicht eingegangen."
)
method_en = (
    "The timeline gathers all statements to which Brückner attaches a year or a relative time reference (pp. 82–90, 831). Relative statements such as “for 60 years” were converted into an approximate year counted back from 1869; they are marked as derived. "
    "The animal names in field and place names come from Brückner’s list on p. 82 and were assigned to an animal by their word stem; whether an animal occurs in the country follows his statements on pp. 82–83. "
    "The fish table (pp. 87–88, 34 species by 4 waters) was taken over completely. An entry counts as a decline if it contains “now”, “formerly” or “otherwise”. Modern names are given only where the identification is certain. "
    "The species counts by animal group are in the supplementary table; some are approximate (birds “ca. 280”) and apply to butterflies and moths only for the area around Zeulenroda. "
    "The analyses of bird species by Unterland and Oberland, of arrival times and of rare visitors were not carried into this piece."
)
print(words(method_de), words(method_en))

caveats = [
    bi(
        "Die Jahre der Zeitleiste sind Näherungen: Bei »seit fünf Jahren« beträgt die Unsicherheit ein bis zwei Jahre, bei »einige Jahrzehnte darauf« und »seit 60 Jahren« zehn Jahre und mehr. Die Häufung jüngerer Vogelbeobachtungen spiegelt vermutlich die Beobachtungszeit Brückners und seiner Gewährsleute.",
        "The years in the timeline are approximations: for “for five years” the uncertainty is one to two years, for “some decades later” and “for 60 years” ten years or more. The cluster of recent bird observations probably reflects the period in which Brückner and his informants were observing.",
    ),
    bi(
        "Namen wie Ebersberg, Ebersdorf, Starenburg oder Falkenberg können auf Personen- oder Burgnamen zurückgehen; Brückner wertet alle als Zeugnisse der Fauna. Die Namen sind nicht datiert, Flur- und Ortsnamen sind nicht getrennt.",
        "Names such as Ebersberg, Ebersdorf, Starenburg or Falkenberg may derive from personal or castle names; Brückner treats all of them as evidence of the fauna. The names are undated, and field and place names are not separated.",
    ),
    bi(
        "Die Zahl 34 ist die Zahl der Tabellenzeilen, nicht gesicherter Arten: Nach heutiger Kenntnis enthält die Liste Dubletten und überholte Namen (etwa Nr. 5 neben Nr. 14). Ein Strich heißt nicht, dass die Art im Gewässer fehlt. Bachforelle und Lachsforelle gelten heute als eine Art.",
        "The number 34 counts table rows, not established species: by present knowledge the list contains duplicates and obsolete names (for example no. 5 beside no. 14). A dash does not mean the species is absent from the water. Brown trout and sea trout are now regarded as one species.",
    ),
    bi(
        "Die Artenzahlen sind sehr unterschiedlich belastbar: Säugetiere, Reptilien und Fische sind Landeszahlen, die Vögel eine Schätzung, die Schmetterlinge gelten nur für einen Teil des Landes. Brückner hält die Schmetterlingszahl selbst für zu klein.",
        "The species counts differ greatly in reliability: mammals, reptiles and fish are national figures, birds an estimate, and the butterflies apply to part of the country only. Brückner himself considers the butterfly figure too small.",
    ),
]

feature = {
    "id": "tierwelt",
    "title": bi("Tierwelt und ihr Wandel", "Fauna and its change"),
    "category": "fauna",
    "section": "t1-1-9",
    "merges": MERGES,
    "sources": union_sources("fauna-aenderungen-seit-1647", "fauna-tiernamen-in-flurnamen", "fauna-fische-gewaesser", "fauna-artenzahlen-tiergruppen"),
    "summary": bi(summary_de, summary_en),
    "findings": [bi(finding1_de, finding1_en), bi(finding2_de, finding2_en), bi(finding3_de, finding3_en)],
    "method": bi(method_de, method_en),
    "caveats": caveats,
    "datasets": [changes, names, fish, counts],
    "charts": [
        {"id": "c1", "dataset": "timeline", "title": title_c1, "caption": caption_c1, "vegalite": c1},
        {"id": "c2", "dataset": "names", "title": title_c2, "caption": caption_c2, "vegalite": c2},
        {"id": "c3", "dataset": "fish_cells", "title": title_c3, "caption": caption_c3, "vegalite": c3},
    ],
    "keywords": {
        "de": ["Tierwelt", "Fauna", "Wolf", "Bär", "Luchs", "Fische", "Flurnamen", "Aussterben", "Vögel", "Saale", "Elster"],
        "en": ["fauna", "wolf", "bear", "lynx", "fish", "field names", "extinction", "birds", "Saale", "Elster"],
    },
    "related": ["phaenologie", "pflanzenwelt", "gewaesser", "ortsnamen"],
    "generated_by": GENERATED_BY.format(k=len(MERGES)),
    "date": DATE,
}
ti = union_issues(*MERGES)
print("issues carried:", ti)
feature["transcription_issues"] = [t for t in ti if t["page"] in ("87", "88", "82", "83")]
if not feature["transcription_issues"]:
    del feature["transcription_issues"]
print(check_lengths(feature))
print(write_feature(feature))
