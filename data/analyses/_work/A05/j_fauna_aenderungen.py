"""Analysis: dated changes in the fauna 1647-1869 (pp. 82-90, 831)."""
from collections import Counter
from common import *

BASE = 1869  # relative statements ("seit fünf Jahren") are counted back from 1869
K = {"loss": (1, "Verlust oder Rückgang", "Loss or decline"), "gain": (2, "Zuwanderung oder Zunahme", "Arrival or increase"),
     "event": (3, "Ereignis oder Zustand", "Event or state")}
# (kind, label_de, label_en, taxon_de, year_printed, year_from, year_to, year_ref, precision_de, precision_en, basis_de, basis_en, quote, page, block)
EV = [
    ("event", "Forellenbäche im ganzen Land", "Trout in all streams", "Forelle", 1647, 1647, 1647, 1647, "genau", "exact",
     "»noch 1647 sämmtliche Bäche … Forellenbäche«", "“in 1647 all streams … trout streams”",
     "Waren noch 1647 sämmtliche Bäche im Ober- und Unterlande Forellenbäche", "87", "b1"),
    ("event", "Wildschwein als Abgabe", "Wild boar as a due", "Wildschwein", 1647, 1647, 1647, 1647, "genau", "exact",
     "im Oberland zahlreich; 1647 noch unter den Abgaben an die Herrschaft", "numerous in the Oberland; in 1647 still among the dues to the lord",
     "weshalb sie noch 1647 unter die Abgaben an die Herrschaft gezählt wurden", "83", "b1"),
    ("loss", "Bär: letzte drei erlegt", "Bear: last three killed", "Bär", None, 1730, 1730, 1730, "ungefähr", "approximate",
     "»um 1730«, Hart bei Langenwetzendorf", "“around 1730”, Hart near Langenwetzendorf",
     "Die drei letzten Bären wurden in einem Winter um 1730 in der Hart bei Langenwetzendorf erlegt", "82", "b2"),
    ("loss", "Luchs ausgerottet", "Lynx exterminated", "Luchs", None, 1730, 1730, 1730, "ungefähr", "approximate",
     "»zu gleicher Zeit« wie die Bären (um 1730)", "“at the same time” as the bears (around 1730)",
     "Zu gleicher Zeit wurde auch das Luchsgeschlecht", "82", "b2"),
    ("loss", "Wolf ausgerottet", "Wolf exterminated", "Wolf", None, 1750, 1769, 1760, "abgeleitet", "derived",
     "»einige Jahrzehnte darauf« (nach 1730), »seit einem Jahrhundert« (vor 1769)", "“some decades later” (after 1730), “for a century” (before 1769)",
     "einige Jahrzehnte darauf das Geschlecht der Wölfe", "82", "b2"),
    ("loss", "Heuschreckenzüge enden", "Locust swarms cease", "Wanderheuschrecke", None, 1769, 1769, 1769, "abgeleitet", "derived",
     "»seit mehr als 100 Jahren« keine Züge mehr (vor 1769)", "no swarms “for more than 100 years” (before 1769)",
     "Seit mehr als 100 Jahren sind derartige Züge nicht mehr vorgekommen", "90", "b4"),
    ("gain", "Hausrotschwanz im Oberland", "Black redstart arrives", "Hausrothschwänzchen", None, 1790, 1800, 1795, "abgeleitet", "derived",
     "»Ende des vorigen Jahrhunderts«", "“at the end of the last century”",
     "von denen sich letzteres Ende des vorigen Jahrhunderts daselbst eingethan hat", "84", "b2"),
    ("gain", "Star nimmt stark zu", "Starling increases strongly", "Staar", None, 1809, 1869, 1809, "abgeleitet", "derived",
     "»seit 60 Jahren stark vermehrt«", "“greatly increased for 60 years”",
     "wohl aber hat er sich seit 60 Jahren stark vermehrt", "84", "b2"),
    ("event", "Reicher Meisenfang", "Rich tit catch", "Meisen", 1813, 1813, 1813, 1813, "genau (18. Oktober)", "exact (18 October)",
     "18. Oktober 1813, nach dem Kanonendonner bei Leipzig", "18 October 1813, after the cannon thunder at Leipzig",
     "In gutem Andenken steht noch der reiche Meisenfang am 18. October 1813", "84", "b2"),
    ("event", "Raupenfraß an Obstbäumen", "Fruit-tree caterpillars", "Schmetterlingsraupen", 1828, 1828, 1828, 1828, "genau (und Folgejahre)", "exact (and following years)",
     "»Im Jahre 1828 und in den folgenden Jahren«", "“in 1828 and the following years”",
     "Im Jahre 1828 und in den folgenden Jahren haben hier die Obstbäume durch den Raupenfraß bedeutenden Schaden erlitten", "831", "b4"),
    ("event", "Prämie auf weiße Falter", "Bounty: white butterflies", "Weißlinge", 1829, 1829, 1829, 1829, "genau (27. Juni)", "exact (27 June)",
     "1 Thlr. Current für 100 Stück weißer Schmetterlinge oder Puppen", "1 Thlr. Current for 100 white butterflies or pupae",
     "Durch Bekanntmachung vom 27. Juni 1829 ist sogar eine Prämie von 1 Thlr. Current für die Einlieferung von 100 Stück weißer Schmetterlinge oder deren Puppen festgesetzt worden", "831", "b4"),
    ("loss", "Rotwild fehlt im Unterland", "Red deer gone (Unterland)", "Edelhirsch", 1848, 1848, 1848, 1848, "genau", "exact",
     "»seit 1848 im Unterlande gar nicht mehr«", "“not at all in the Unterland since 1848”",
     "doch kommt dies Rothwild seit 1848 im Unterlande gar nicht mehr vor", "83", "b1"),
    ("gain", "Wacholderdrossel brütet", "Fieldfare breeds", "Wachholderdrossel", None, 1859, 1859, 1859, "abgeleitet", "derived",
     "»seit etwas mehr als zehn Jahren«", "“for slightly more than ten years”",
     "Seit etwas mehr als zehn Jahren ist im pöllwitzer Walde die Wachholderdrossel", "84", "b2"),
    ("gain", "Gerstenammer im Unterland", "Corn bunting arrives", "Gersten- oder Grauammer", 1868, 1864, 1868, 1864, "abgeleitet", "derived",
     "»seit fünf Jahren« im Unterland (1864), »seit 1868« bei Schleiz", "“for five years” in the Unterland (1864), “since 1868” near Schleiz",
     "seit fünf Jahren in den warmen Thälern des Unterlandes und seit 1868 bei Schleiz die Gersten- oder Grauammer", "84", "b2"),
    ("gain", "Rohrammer im Oberland", "Reed bunting arrives", "Rohrammer", None, 1864, 1864, 1864, "abgeleitet", "derived",
     "»seit fünf Jahren« in den Teichstrichen des Oberlandes", "“for five years” in the pond areas of the Oberland",
     "seit fünf Jahren in den Teichstrichen des Oberlandes die Rohrammer eingezogen", "84", "b2"),
    ("gain", "Kreuzschnabel brütet (Gera)", "Crossbills breed near Gera", "Kreuzschnabel", None, 1867, 1868, 1867, "genau (Winter 1867/68)", "exact (winter 1867/68)",
     "»im Winter 1867/68«", "“in the winter of 1867/68”",
     "brüten auch hier in einzelnen Jahren, wie namentlich im Winter 1867/68", "85", "b1"),
    ("gain", "Elster nimmt wieder zu", "Magpie increases again", "Elster", None, 1867, 1867, 1867, "abgeleitet", "derived",
     "»seit zwei Jahren« (Berichtigungen, 1869)", "“for two years” (corrigenda, 1869)",
     "Seit zwei Jahren haben sich die Elstern wieder stark vermehrt", "831", "b2"),
    ("gain", "Großer Würger wieder da", "Great grey shrike back", "Großer Würger", 1869, 1869, 1869, 1869, "genau (Sommer 1869)", "exact (summer 1869)",
     "»der Sommer 1869 hat ihn wieder als einheimisch nachgewiesen«", "“the summer of 1869 has shown him again to be native”",
     "indes der Sommer 1869 hat ihn wieder als einheimisch nachgewiesen", "831", "b1"),
]
for r in EV:
    need(r[12], r[13], r[14])
EV.sort(key=lambda r: (r[7], r[5]))
rows = []
for kind, lde, len_, tax, yp, yf, yt, yr, pde, pen, bde, ben, q, pg, bk in EV:
    rows.append([lde, len_, tax, kind, K[kind][0], K[kind][1], K[kind][2], yp, yf, yt, yr, pde, pen, bde, ben, q, pg, bk])
cnt = Counter(r[3] for r in rows)
print(dict(cnt), len(rows))
recent = [r for r in rows if r[3] == "gain" and r[10] >= 1859]
print("recent gains", len(recent), [r[0] for r in recent])
n = len(rows)
n_loss, n_gain, n_event = cnt["loss"], cnt["gain"], cnt["event"]
n_recent = len(recent)

ana = {
    "id": "fauna-aenderungen-seit-1647",
    "title": bi("Veränderungen der Tierwelt 1647–1869", "Changes in the fauna, 1647–1869"),
    "category": "fauna",
    "section": "t1-1-9",
    "sources": [{"page": "82", "block": "b2"}, {"page": "83", "block": "b1"}, {"page": "84", "block": "b2"}, {"page": "85", "block": "b1"}, {"page": "87", "block": "b1"},
                {"page": "90", "block": "b4"}, {"page": "831", "block": "b1"}, {"page": "831", "block": "b2"}, {"page": "831", "block": "b4"}],
    "summary": bi(
        f"Brückner belegt das Verschwinden und das Neuauftreten von Tierarten mit Jahres- und Zeitangaben: Bären und Luchse um 1730, Wölfe wenig später, das Rotwild im Unterland seit 1848 und, in den letzten Jahren vor 1869, eine Reihe neu eingewanderter oder wieder häufiger gewordener Vögel. Die {n} datierbaren Angaben sind zu einer Zeitleiste zusammengestellt.",
        f"Brückner documents the disappearance and new appearance of animal species with years and time statements: bears and lynx around 1730, wolves shortly afterwards, red deer in the Unterland since 1848 and, in the last years before 1869, a series of newly arrived or again more frequent birds. The {n} datable statements are put together as a timeline."),
    "method": bi(
        f"Aus S. 82–90 und den Berichtigungen S. 831 wurden alle Angaben erfasst, die eine Jahreszahl oder einen relativen Zeitbezug enthalten ({n_loss} Verluste, {n_gain} Zuwanderungen oder Zunahmen, {n_event} Ereignisse oder Zustände). Gedruckte Jahre stehen unverändert in der Spalte »Jahr im Druck«. Relative Angaben (»seit fünf Jahren«, »seit 60 Jahren«, »seit mehr als 100 Jahren«, »Ende des vorigen Jahrhunderts«) wurden vom Jahr 1869 aus in ein ungefähres Jahr umgerechnet (abgeleitet): Das jüngste im Haupttext genannte Jahr ist 1868, die Berichtigungen nennen den Sommer 1869. Die Spalten »von«, »bis« und »Bezugsjahr« sind daher bei abgeleiteten Angaben nur auf wenige Jahre genau; bei Wolf und Star überspannen sie eine Zeitspanne. Jahre für das Hauptflugjahr der Maikäfer nennt Brückner nicht (nur eine vierjährige Periode, S. 831); sie fehlen deshalb.",
        f"All statements on pp. 82–90 and in the corrigenda on p. 831 that contain a year or a relative time reference were captured ({n_loss} losses, {n_gain} arrivals or increases, {n_event} events or states). Printed years are given unchanged in the column “year in print”. Relative statements (“for five years”, “for 60 years”, “for more than 100 years”, “at the end of the last century”) were converted into an approximate year counted back from 1869 (derived): the most recent year named in the main text is 1868, the corrigenda name the summer of 1869. The columns “from”, “to” and “reference year” are therefore accurate only to within a few years for derived statements; for wolf and starling they span a period. Brückner gives no years for the main flight year of the cockchafer (only a four-year period, p. 831); they are therefore missing."),
    "findings": [
        bi(f"Für die großen Raubtiere ergibt sich eine klare Abfolge: Die letzten drei Bären und die Luchse fallen um 1730, die Wölfe einige Jahrzehnte später (vor etwa 1769); Wolfseinfälle in strengen Wintern bleiben möglich. Seit mehr als 100 Jahren, also vor etwa 1769, gibt es keine Heuschreckenzüge mehr.",
           f"For the large predators a clear sequence results: the last three bears and the lynx fall around 1730, the wolves some decades later (before about 1769); incursions of wolves in hard winters remain possible. For more than 100 years, that is before about 1769, there have been no locust swarms."),
        bi(f"Von den {n_gain} Zuwanderungen oder Zunahmen liegen {n_recent} in den zehn Jahren vor 1869 (Wacholderdrossel, Gerstenammer, Rohrammer, Kreuzschnäbel, Elster, großer Würger); ältere sind Hausrotschwanz (Ende des 18. Jahrhunderts) und Star (seit rund 1809). Alle {n_gain} betreffen Vögel.",
           f"Of the {n_gain} arrivals or increases, {n_recent} fall in the ten years before 1869 (fieldfare, corn bunting, reed bunting, crossbills, magpie, great grey shrike); older ones are the black redstart (end of the 18th century) and the starling (since about 1809). All {n_gain} concern birds."),
        bi("Die Häufung jüngerer Vogelbeobachtungen spiegelt vermutlich vor allem die Beobachtungszeit Brückners und seiner Gewährsleute wider; für frühere Jahrhunderte liegen nur Verlustmeldungen und einzelne Urkundenjahre (1647, 1829) vor.",
           "The accumulation of recent bird observations probably reflects above all the observation period of Brückner and his informants; for earlier centuries only reports of losses and individual documentary years (1647, 1829) exist."),
    ],
    "caveats": [
        bi("Die umgerechneten Jahre sind Näherungen (±1–2 Jahre bei »seit fünf Jahren«, ±10 Jahre und mehr bei »einige Jahrzehnte« und »seit 60 Jahren«); es wurde kein genaueres Datum erfunden. Wo Brückner nur »um 1730« oder »Ende des vorigen Jahrhunderts« schreibt, ist dies in der Spalte »Genauigkeit« vermerkt.",
           "The converted years are approximations (±1–2 years for “for five years”, ±10 years or more for “some decades” and “for 60 years”); no more precise date was invented. Where Brückner writes only “around 1730” or “at the end of the last century”, this is noted in the column “precision”."),
        bi("Nicht aufgenommen sind Angaben ohne Zeitbezug (z. B. Wisent »längst verschwunden«, Wildkatze »längst«, Saatkrähe »jetzt nicht mehr« im Unterland, Schwarzspecht »noch vor Kurzem«) sowie die Rückgänge der Fische (S. 87), für die nur der Zustand von 1647 datiert ist.",
           "Statements without a time reference are not included (e.g. wisent “long vanished”, wildcat “long ago”, rook “no longer” in the Unterland, black woodpecker “until recently”), nor are the declines of the fish (p. 87), for which only the state of 1647 is dated."),
        bi("Die Berichtigungen S. 831 (Elster, großer Würger) beziehen sich auf den Zeitpunkt ihrer Niederschrift (1869 oder 1870); »seit zwei Jahren« wurde daher von 1869 aus gerechnet.",
           "The corrigenda on p. 831 (magpie, great grey shrike) refer to the time of writing (1869 or 1870); “for two years” was therefore counted from 1869."),
    ],
    "datasets": [
        {"name": "timeline",
         "title": bi("Datierbare Veränderungen der Tierwelt (S. 82–90, 831)", "Datable changes in the fauna (pp. 82–90, 831)"),
         "columns": [
             col("label_de", "Angabe", "Statement", "string", None, True),
             col("label_en", "Angabe (EN)", "Statement (EN)", "string", None, True),
             col("taxon_de", "Tier (Druck)", "Animal (print)", "string", None),
             col("kind_key", "Art (Schlüssel)", "Kind (key)", "string", None, True),
             col("kind_order", "Art (Reihenfolge)", "Kind (order)", "integer", None, True),
             col("kind_de", "Art", "Kind", "string", None, True),
             col("kind_en", "Art (EN)", "Kind (EN)", "string", None, True),
             col("year_printed", "Jahr im Druck", "Year in print", "integer", None),
             col("year_from", "von (Jahr)", "From (year)", "integer", None, True, "gedrucktes Jahr oder umgerechnet von 1869"),
             col("year_to", "bis (Jahr)", "To (year)", "integer", None, True),
             col("year_ref", "Bezugsjahr", "Reference year", "integer", None, True, "Punktschätzung für die Zeitleiste"),
             col("precision_de", "Genauigkeit", "Precision", "string", None, True),
             col("precision_en", "Genauigkeit (EN)", "Precision (EN)", "string", None, True),
             col("basis_de", "Zeitangabe bei Brückner", "Time statement in Brückner", "string", None),
             col("basis_en", "Zeitangabe (Übersetzung)", "Time statement (translation)", "string", None, True),
             col("quote", "Wortlaut", "Wording", "string", None),
             col("page", "Seite", "Page", "string", None),
             col("block", "Block", "Block", "string", None),
         ],
         "rows": rows,
         "source_refs": [{"page": "82", "block": "b2"}, {"page": "83", "block": "b1"}, {"page": "84", "block": "b2"}, {"page": "85", "block": "b1"}, {"page": "87", "block": "b1"},
                         {"page": "90", "block": "b4"}, {"page": "831", "block": "b1"}, {"page": "831", "block": "b2"}, {"page": "831", "block": "b4"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "timeline",
         "title": bi("Zeitleiste: Verluste, Zuwanderungen und Ereignisse in der Tierwelt", "Timeline: losses, arrivals and events in the fauna"),
         "caption": bi("Punkte: Bezugsjahr; Linien: Zeitspanne bei ungenauen Angaben. Relative Angaben (»seit fünf Jahren«) sind vom Jahr 1869 aus zurückgerechnet.",
                       "Dots: reference year; lines: period for imprecise statements. Relative statements (“for five years”) are counted back from 1869."),
         "vegalite": {"height": 420,
                      "layer": [
                          {"mark": {"type": "rule", "strokeWidth": 3},
                           "encoding": {
                               "y": {"field": {"de": "label_de", "en": "label_en"}, "type": "nominal", "sort": {"field": "year_ref", "op": "min"}, "title": None, "axis": {"labelLimit": 250}},
                               "x": {"field": "year_from", "type": "quantitative", "scale": {"domain": [1630, 1880]}, "axis": {"format": "d", "tickMinStep": 25}, "title": bi("Jahr", "Year")},
                               "x2": {"field": "year_to"},
                               "color": {"field": {"de": "kind_de", "en": "kind_en"}, "type": "nominal", "title": bi("Art", "Kind"),
                                         "scale": {"domain": [{"de": K[k][1], "en": K[k][2]} for k in ("loss", "gain", "event")]}}}},
                          {"mark": {"type": "point", "filled": True, "size": 90},
                           "encoding": {
                               "y": {"field": {"de": "label_de", "en": "label_en"}, "type": "nominal", "sort": {"field": "year_ref", "op": "min"}},
                               "x": {"field": "year_ref", "type": "quantitative"},
                               "color": {"field": {"de": "kind_de", "en": "kind_en"}, "type": "nominal", "title": bi("Art", "Kind"), "legend": {"columns": 1, "labelLimit": 300},
                                         "scale": {"domain": [{"de": K[k][1], "en": K[k][2]} for k in ("loss", "gain", "event")]}},
                               "tooltip": [{"field": {"de": "label_de", "en": "label_en"}, "title": bi("Angabe", "Statement")},
                                           {"field": {"de": "kind_de", "en": "kind_en"}, "title": bi("Art", "Kind")},
                                           {"field": "year_from", "title": bi("von", "from"), "format": "d"},
                                           {"field": "year_to", "title": bi("bis", "to"), "format": "d"},
                                           {"field": {"de": "basis_de", "en": "basis_en"}, "title": bi("Zeitangabe bei Brückner", "Time statement in Brückner")},
                                           {"field": {"de": "precision_de", "en": "precision_en"}, "title": bi("Genauigkeit", "Precision")}]}},
                      ]}},
    ],
    "keywords": {"de": ["Tierwelt", "Wolf", "Bär", "Luchs", "ausgerottet", "Zuwanderung", "Vögel", "Heuschrecken", "Rotwild", "Zeitleiste", "Fauna"],
                 "en": ["fauna", "wolf", "bear", "lynx", "extirpation", "immigration", "birds", "locusts", "red deer", "timeline"]},
    "related": ["fauna-tiernamen-in-flurnamen", "fauna-voegel-unterland-oberland"],
    "generated_by": GEN,
    "date": DATE,
}
write(ana)
