from common import *

MERGES = [
    "gesundheit-krankheitsstatistik-lobenstein-gera-hohenleuben",
    "gesundheit-medizinalwesen-und-seuchen-zeitleiste",
    "gesundheit-taubstumme-blinde-1864-1867",
    "gesundheit-militaer-tauglichkeit-1864-1866",
]

mean = dataset("gesundheit-militaer-tauglichkeit-1864-1866", "mean")
diseases = dataset("gesundheit-krankheitsstatistik-lobenstein-gera-hohenleuben", "diseases")
events = dataset("gesundheit-medizinalwesen-und-seuchen-zeitleiste", "events")
gera_skin = dataset("gesundheit-krankheitsstatistik-lobenstein-gera-hohenleuben", "gera_skin")
disability = dataset("gesundheit-taubstumme-blinde-1864-1867", "disability")
by_year = dataset("gesundheit-militaer-tauglichkeit-1864-1866", "by_year")
totals = dataset("gesundheit-militaer-tauglichkeit-1864-1866", "totals")

# ---------------------------------------------------------------- numbers
MEAN = rows_of(mean)
fit = next(r for r in MEAN if r["category_de"] == "Brauchbar")
top_reason = max((r for r in MEAN if r["category_de"] != "Brauchbar"), key=lambda r: r["pct_mean"])
assert top_reason["category_de"].startswith("Unterwüchsig")
TOT = rows_of(totals)
avg_conscripts = 799  # printed average (S. 173)
assert abs(fit["avg_count"] / fit["pct_mean"] * 100 - avg_conscripts) < 1
BY = {(r["year"], r["category_de"]): r["share_pct"] for r in rows_of(by_year)}
fit_1864, fit_1866 = BY[(1864, "Brauchbar")], BY[(1866, "Brauchbar")]
fit_1865 = BY[(1865, "Brauchbar")]

D = rows_of(diseases)
skin = {r["place"]: r["percent"] for r in D if r["disease_de"].startswith("Krätze")}
assert skin["Gera"] > 2 * skin["Lobenstein"] and skin["Gera"] > 2 * skin["Hohenleuben"]
GS = rows_of(gera_skin)
skin_a, skin_b, skin_c = (r["percent_printed"] for r in GS)
catarrh = {r["place"]: r["percent"] for r in D if r["disease_de"] == "Katarrhe"}
shared = [r for r in D if r["level"] == 0 and r["shared"] == 1 and r["place"] != "Tanna"]

DIS = rows_of(disability)
dis67 = {r["condition"]: r["count_total"] for r in DIS if r["district"] == "Reuß j. L." and r["year"] == 1867 and r["area"] == "Überhaupt"}
dis64 = {r["condition"]: r["count_total"] for r in DIS if r["district"] == "Reuß j. L." and r["year"] == 1864 and r["area"] == "Überhaupt"}

EV = rows_of(events)
ev_year = {(r["year"], r["place"]): r for r in EV}
smallpox_gera = next(r for r in EV if r["year"] == 1756)
decree = next(r for r in EV if r["year"] == 1826)
years_gap = decree["year"] - smallpox_gera["year"]
assert smallpox_gera["value"] == 208

# ---------------------------------------------------------------- events with positions and short labels
lane_order = ["Ärzte vor Ort", "Blattern und Impfung", "Weitere Epidemien"]
SHORT = {
    (1570, "Gera"): ("Gera: erster Stadtarzt (um 1570)", "Gera: first town physician (about 1570)"),
    (1600, "Schleiz"): ("Schleiz: erster Stadtarzt (um 1600)", "Schleiz: first town physician (about 1600)"),
    (1620, "Lobenstein"): ("Lobenstein: erster Stadtarzt (um 1620)", "Lobenstein: first town physician (about 1620)"),
    (1760, "Hohenleuben"): ("Hohenleuben: erster Arzt sucht Sitz (um 1760)", "Hohenleuben: first physician seeks a seat (about 1760)"),
    (1756, "Gera"): (f"Gera: {{v}} Kinder sterben an Blattern", "Gera: {v} children die of smallpox"),
    (1788, "Ebersdorf"): ("Ebersdorf: {v} Kinder an Blattern erkrankt", "Ebersdorf: {v} children ill with smallpox"),
    (1790, "Friesau und Remptendorf (Reuß ä. L.)"): ("Reuß ä. L.: Pfarrer Frotscher impft", "Reuss (Elder Line): pastor Frotscher inoculates"),
    (1791, "Lobenstein-Ebersdorf"): ("Lobenstein-Ebersdorf: über {v} % der Toten Blatternopfer", "Lobenstein-Ebersdorf: over {v} % of the dead die of smallpox"),
    (1807, "Fürstentum"): ("Fürstentum: {v} Kinder sterben an Blattern", "Principality: {v} children die of smallpox"),
    (1820, "Fürstentum"): ("Impfung setzt sich mehr und mehr durch", "vaccination gains ground"),
    (1826, "Fürstentum"): ("Mandat macht die Impfung zum Gesetz", "decree makes vaccination law"),
    (1844, "Schilbach"): ("Schilbach: Scharlach, auch Ältere erkranken", "Schilbach: scarlet fever, older people fall ill too"),
    (1845, "Tanna"): ("Tanna: Masern und Scharlach zugleich", "Tanna: measles and scarlet fever together"),
    (1866, "Hirschberg und Untermhaus"): ("Hirschberg, Untermhaus: Cholera, eingeschleppt", "Hirschberg, Untermhaus: cholera, brought in"),
}
events["columns"] += [
    {"name": "pos", "label": bi("Zeilenposition in der Zeitleiste", "Row position in the timeline"), "type": "number", "unit": None, "derived": True, "note": "redaktionell"},
    {"name": "lane_first", "label": bi("Erstes Ereignis der Zeile (1 = ja)", "First event of the lane (1 = yes)"), "type": "integer", "unit": None, "derived": True, "note": "redaktionell"},
    {"name": "label_de", "label": bi("Kurzbeschriftung (deutsch)", "Short label (German)"), "type": "string", "unit": None, "derived": True, "note": "redaktionelle Kurzfassung von event_de"},
    {"name": "label_en", "label": bi("Kurzbeschriftung (englisch)", "Short label (English)"), "type": "string", "unit": None, "derived": True, "note": "redaktionelle Kurzfassung von event_en"},
]
names = [c["name"] for c in events["columns"][:-4]]
by_lane = {l: [dict(zip(names, r)) for r in events["rows"] if r[names.index("lane_de")] == l] for l in lane_order}
new_rows, y = [], 0.0
for lane in lane_order:
    first = True
    y += 1.0
    for r in sorted(by_lane[lane], key=lambda r: r["year"]):
        de, en = SHORT[(r["year"], r["place"])]
        v = r["value"]
        de, en = de.replace("{v}", str(v) if v else ""), en.replace("{v}", str(v) if v else "")
        new_rows.append([r[c] for c in names] + [round(y, 2), 1 if first else 0, de, en])
        first = False
        y += 1.0
    y += 0.7
y_max = y - 0.7
events["rows"] = sorted(new_rows, key=lambda r: r[len(names)])
events["title"] = bi("Datierte Ereignisse des Gesundheitswesens", "Dated events of the health service")

n = lambda x, d=0: pair(x, d)
log = [("fit", fit), ("top_reason", top_reason), ("fit years", (fit_1864, fit_1865, fit_1866)), ("skin", skin),
       ("gera_skin", (skin_a, skin_b, skin_c)), ("catarrh", catarrh), ("dis67", dis67), ("dis64", dis64), ("gap", years_gap)]

# ---------------------------------------------------------------- chart 1: recruits
c1 = {
    "height": {"step": 28},
    "transform": [
        {"calculate": {"de": "datum.category_de", "en": "datum.category_en"}, "as": "cat"},
        {"calculate": "datum.category_de === 'Brauchbar'", "as": "isfit"},
    ],
    "encoding": {
        "y": {"field": "cat", "type": "nominal", "sort": {"field": "pct_mean", "op": "max", "order": "descending"},
              "axis": {"title": None, "labelLimit": 400, "ticks": False,
                       "labelFontWeight": {"condition": {"test": "datum.value === 'Brauchbar' || datum.value === 'Fit for service'", "value": 700}, "value": 400}}},
    },
    "layer": [
        {"mark": {"type": "bar", "size": 18},
         "encoding": {"x": {"field": "pct_mean", "type": "quantitative", "scale": {"domain": [0, 36]},
                            "axis": {"values": [0, 10, 20, 30], "title": {"de": "Prozent der Militärpflichtigen", "en": "Percent of conscripts"}}},
                      "color": {"condition": {"test": "datum.isfit", "value": "@accent"}, "value": "@context"},
                      "tooltip": [tooltip("cat", "Befund", "Finding"), tooltip("avg_count", "Personen im Jahresdurchschnitt", "Persons, annual average", ",d"),
                                  tooltip("pct_mean", "Prozent", "Percent", ".2f")]}},
        {"transform": [{"filter": "datum.isfit"}],
         "mark": {"type": "text", "style": "label", "align": "left", "dx": 6, "color": "@accent"},
         "encoding": {"x": {"field": "pct_mean", "type": "quantitative"}, "text": {"field": "pct_mean", "format": ".1f"}}},
        {"transform": [{"filter": "!datum.isfit"}],
         "mark": {"type": "text", "style": "label-muted", "align": "left", "dx": 6},
         "encoding": {"x": {"field": "pct_mean", "type": "quantitative"}, "text": {"field": "pct_mean", "format": ".1f"}}},
        {"transform": [{"filter": "datum.isfit"},
                       {"calculate": {"de": "datum.avg_count + ' von " + str(avg_conscripts) + " Pflichtigen im Jahresdurchschnitt'",
                                      "en": "datum.avg_count + ' of " + str(avg_conscripts) + " conscripts on average per year'"}, "as": "cnt"}],
         "mark": {"type": "text", "style": "label", "align": "left", "dx": 10, "color": "@paper"},
         "encoding": {"x": {"datum": 0}, "text": {"field": "cnt"}}},
    ],
}

# ---------------------------------------------------------------- chart 2: diseases by place (heatmap)
PLACES = ["Lobenstein", "Gera", "Hohenleuben"]
c2 = {
    "height": {"step": 34},
    "transform": [
        {"filter": "datum.level == 0 && datum.shared == 1 && datum.place !== 'Tanna'"},
        {"joinaggregate": [{"op": "count", "as": "n_places"}], "groupby": ["disease_de"]},
        {"filter": "datum.n_places == 3"},
        {"calculate": {"de": "datum.disease_de", "en": "datum.disease_en"}, "as": "dis"},
    ],
    "encoding": {
        "y": {"field": "dis", "type": "nominal", "sort": {"field": "percent", "op": "max", "order": "descending"},
              "axis": {"title": None, "labelLimit": 400, "ticks": False, "domain": False,
                       "labelFontWeight": {"condition": {"test": "indexof(['Krätze u. ähnl. Hautkrankheiten', 'Scabies, similar skin diseases'], datum.value) >= 0", "value": 700}, "value": 400}}},
        "x": {"field": "place", "type": "nominal", "sort": PLACES,
              "axis": {"orient": "top", "title": None, "ticks": False, "domain": False, "labelAngle": 0, "labelFontSize": 12,
                       "labelFontWeight": 600}},
    },
    "layer": [
        {"mark": {"type": "rect", "stroke": "@paper", "strokeWidth": 3, "cornerRadius": 3},
         "encoding": {"color": {"field": "percent", "type": "quantitative", "legend": None,
                                "scale": {"domain": [0, 14], "range": "heatmap", "clamp": True}},
                      "tooltip": [tooltip("dis", "Krankheit", "Disease"), tooltip("place", "Ort", "Place"),
                                  tooltip("percent", "Prozent der Erkrankten", "Percent of the sick", ".2f")]}},
        {"mark": {"type": "text", "style": "label"},
         "encoding": {"text": {"field": "percent", "format": ".1f"},
                      "color": {"condition": {"test": "datum.percent >= 8", "value": "@paper"}, "value": "@ink"}}},
    ],
}

# ---------------------------------------------------------------- chart 3: timeline
LANE_COL = {"field": "lane_de", "type": "nominal", "legend": None,
            "scale": {"domain": lane_order, "range": ["@accent3", "@accent", "@accent2"]}}
YPOS = {"field": "pos", "type": "quantitative", "scale": {"domain": [-0.8, y_max + 0.4], "reverse": True}, "axis": None}
c3 = {
    "height": 440,
    "layer": [
        {"mark": {"type": "circle", "stroke": "@paper", "strokeWidth": 1.5},
         "encoding": {
             "x": {"field": "year", "type": "quantitative", "scale": {"domain": [1560, 1880], "nice": False},
                   "axis": {"values": [1600, 1700, 1800], "format": "d", "grid": True, "title": None, "orient": "bottom"}},
             "y": YPOS, "color": LANE_COL,
             "size": {"condition": {"test": "datum.year == 1756 || datum.year == 1826", "value": 230}, "value": 110},
             "tooltip": [tooltip("year", "Jahr", "Year", "d"), tooltip("place", "Ort", "Place"),
                         {"field": "event_de", "title": "Ereignis"}]}},
        {"transform": [{"filter": "datum.year >= 1750"}],
         "mark": {"type": "text", "style": "label", "align": "right", "dx": -12, "color": "@ink2", "fontWeight": 400},
         "encoding": {"x": {"field": "year", "type": "quantitative"}, "y": YPOS,
                      "text": {"field": {"de": "label_de", "en": "label_en"}}}},
    ],
}
# field names cannot be bilingual: use calculate for the label text
c3["transform"] = [{"calculate": {"de": "datum.label_de", "en": "datum.label_en"}, "as": "label"},
                   {"calculate": {"de": "datum.lane_de", "en": "datum.lane_en"}, "as": "lane_label"},
                   {"calculate": "datum.pos - 1", "as": "head_pos"}]
c3["layer"][1]["encoding"]["text"] = {"field": "label"}
c3["layer"][0]["encoding"]["tooltip"] = [tooltip("year", "Jahr", "Year", "d"), tooltip("label", "Ereignis", "Event")]
c3["layer"] += [
    {"transform": [{"filter": "datum.year < 1750"}],
     "mark": {"type": "text", "style": "label", "align": "left", "dx": 12, "color": "@ink2", "fontWeight": 400},
     "encoding": {"x": {"field": "year", "type": "quantitative"}, "y": YPOS, "text": {"field": "label"}}},
    {"transform": [{"filter": "datum.lane_first == 1"}],
     "mark": {"type": "text", "style": "label", "align": "left", "fontSize": 13},
     "encoding": {"x": {"datum": 1560}, "y": {"field": "head_pos", "type": "quantitative"},
                  "text": {"field": "lane_label"}, "color": LANE_COL}},
]

# ---------------------------------------------------------------- texts
title = bi("Krankheit, Ärzte und Seuchen", "Illness, physicians and epidemics")
t_fit, t_pct = n(fit["avg_count"]), n(fit["pct_mean"], 1)
summary = bi(
    f"Brückner stützt sein Bild der Volkskrankheiten auf wenige Quellen: eine Arztpraxis in Lobenstein, die Krankenhausstation Gera, Hohenleuben und die Musterungen. "
    f"Von durchschnittlich {avg_conscripts} Militärpflichtigen galten {t_fit[0]} als brauchbar. In Gera betrafen {n(skin['Gera'], 1)[0]} Prozent der Erkrankungen Krätze und ähnliche Hautleiden. "
    f"Die Impfung wurde {decree['year']} Gesetz, die Cholera trat {EV[-1]['year']} einmalig auf. 1867 zählte er {n(dis67['Taubstumme'])[0]} Taubstumme und {n(dis67['Blinde'])[0]} Blinde.",
    f"Brückner bases his picture of the common diseases on few sources: a physician’s practice in Lobenstein, the hospital ward in Gera, Hohenleuben and the musters. "
    f"Of an average of {avg_conscripts} conscripts, {t_fit[1]} were fit for service. In Gera {n(skin['Gera'], 1)[1]} percent of the cases were scabies and similar skin diseases. "
    f"Vaccination became law in {decree['year']}, cholera occurred once, in {EV[-1]['year']}. In 1867 he counts {n(dis67['Taubstumme'])[1]} deaf-mutes and {n(dis67['Blinde'])[1]} blind people.",
)
findings = [
    bi(f"Der Anteil der Brauchbaren lag 1864 bei {n(fit_1864, 1)[0]}, 1865 bei {n(fit_1865, 1)[0]} und 1866 bei {n(fit_1866, 1)[0]} Prozent. Häufigster Grund der Rückstellung war eine Körpergröße unter 5′ 7″ ({n(top_reason['pct_mean'], 1)[0]} Prozent).",
       f"The share of fit conscripts was {n(fit_1864, 1)[1]} percent in 1864, {n(fit_1865, 1)[1]} in 1865 and {n(fit_1866, 1)[1]} in 1866. The most common reason for deferral was a height under 5′ 7″ ({n(top_reason['pct_mean'], 1)[1]} percent)."),
    bi(f"In der Station Gera stieg der Anteil der Hautkranken von {n(skin_a, 1)[0]} Prozent (1856 bis 1860) über {n(skin_b, 1)[0]} auf {n(skin_c, 1)[0]} Prozent (1865 bis 1867); Brückner führt das auf die Fabrikarbeiter zurück.",
       f"In the Gera ward the share of skin patients rose from {n(skin_a, 1)[1]} percent (1856 to 1860) via {n(skin_b, 1)[1]} to {n(skin_c, 1)[1]} percent (1865 to 1867); Brückner attributes this to factory workers."),
    bi(f"Die Blatternimpfung wurde {decree['year']} Gesetz, {years_gap} Jahre nach den {n(smallpox_gera['value'])[0]} toten Kindern in Gera. Die ersten Stadtärzte erscheinen um 1570 in Gera, um 1600 in Schleiz, um 1620 in Lobenstein.",
       f"Smallpox vaccination became law in {decree['year']}, {years_gap} years after the {n(smallpox_gera['value'])[1]} child deaths in Gera. The first town physicians appear in Gera about 1570, in Schleiz about 1600, in Lobenstein about 1620."),
]

charts = [
    {"id": "c1", "dataset": "mean",
     "title": bi("Nur drei von zehn Militärpflichtigen waren brauchbar, am häufigsten fehlte es an Körpergröße",
                 "Only three in ten conscripts were fit for service, most often they lacked height"),
     "caption": bi("Befund der Militärpflichtigen 1864 bis 1866 in Prozent des gedruckten Durchschnitts von 799 Pflichtigen jährlich. Unterwüchsig: unter 5′ 7″ sächsisches Maß, etwa 158 cm. Quelle: S. 173.",
                   "Findings for conscripts 1864 to 1866 as a percentage of the printed average of 799 conscripts a year. Undersized: under 5′ 7″ Saxon measure, about 158 cm. Source: p. 173."),
     "vegalite": c1},
    {"id": "c2", "dataset": "diseases",
     "title": bi(f"Krätze und Hautleiden betrafen in Gera {n(skin['Gera'], 1)[0]} Prozent der Kranken, in Lobenstein und Hohenleuben {n(skin['Lobenstein'])[0]}",
                 f"In Gera {n(skin['Gera'], 1)[1]} percent of the sick had skin diseases, in Lobenstein and Hohenleuben {n(skin['Lobenstein'])[1]}"),
     "caption": bi("Hauptkrankheiten in Prozent der Erkrankten, nach den Aufzeichnungen eines Arztes in Lobenstein, der Krankenhausstation Gera und des Orts Hohenleuben. Die Zahlen sind nicht streng vergleichbar. Quelle: S. 169 bis 172.",
                   "Main diseases as a percentage of the sick, from the records of a physician in Lobenstein, the hospital ward in Gera and the town of Hohenleuben. The figures are not strictly comparable. Source: pp. 169 to 172."),
     "vegalite": c2},
    {"id": "c3", "dataset": "events",
     "title": bi(f"{decree['year']} machte ein Mandat die Impfung zum Gesetz, {years_gap} Jahre nach {n(smallpox_gera['value'])[0]} toten Kindern in Gera",
                 f"In {decree['year']} a decree made vaccination law, {years_gap} years after smallpox killed {n(smallpox_gera['value'])[1]} children in Gera"),
     "caption": bi("Von Brückner datierte Ereignisse: erste Ärzte, Blattern und Impfung, weitere Epidemien. Die Beispiele sind keine vollständige Chronik; Zahlen und Einheiten der Blatternfälle sind nicht vergleichbar. Quelle: S. 170 f., 177.",
                   "Events dated by Brückner: first physicians, smallpox and vaccination, further epidemics. The examples are not a complete chronicle; the figures and units of the smallpox cases are not comparable. Source: pp. 170 f., 177."),
     "vegalite": c3},
]

datasets = [mean, diseases, events, gera_skin, disability]


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
convs = [c for aid in MERGES for c in archive(aid).get("conversions", [])]

feature = {
    "id": "gesundheit",
    "title": title,
    "category": "health",
    "section": "t1-2-6",
    "merges": MERGES,
    "sources": refs_pages(datasets),
    "summary": summary,
    "findings": findings,
    "method": bi(
        "Die Befunde der Militärpflichtigen stammen aus der Tabelle S. 173 (Jahre 1864 bis 1866, gedruckter Durchschnitt und Prozentspalte, bezogen auf 799 Pflichtige). "
        "Die Krankheitsprozente stammen aus Brückners Übersicht S. 172; Striche bedeuten »nicht angegeben«, Brüche wurden in Dezimalzahlen überführt (1/2 = 0,5). Das Diagramm zeigt die Krankheiten, die für mindestens zwei Orte genannt sind; Tanna liefert nur einen Wert (Nervenfieber 0,36 Prozent) und fehlt in der Grafik. "
        "Die Zahlen zur Krätze in Gera stehen im Text S. 171. Die Zeitleiste stellt die datierten Angaben aus S. 170, 171 und 177 zusammen; die Zuordnung zu drei Zeilen und die Kurzbeschriftungen sind redaktionell. "
        "Die Zahlen zu Taubstummen und Blinden (S. 117 f., Stände 1864 und 1867) liegen als Tabelle bei. "
        "Nicht verwendet wurden die Monatsverteilung der Erkrankungen in Hohenleuben, das Krankheitsbild in Lobenstein im Einzelnen, die Taubstummen und Blinden nach Bezirk und die Einzeljahre der Musterung; sie stehen in den Einzelauswertungen.",
        "The findings for conscripts come from the table on p. 173 (years 1864 to 1866, printed average and percentage column, based on 799 conscripts). "
        "The disease percentages come from Brückner’s overview on p. 172; dashes mean “not stated”, fractions were converted to decimals (1/2 = 0.5). The chart shows the diseases named for at least two places; Tanna supplies only one value (nervous fever 0.36 percent) and is left out. "
        "The figures on scabies in Gera are in the text on p. 171. The timeline assembles the dated statements from pp. 170, 171 and 177; the assignment to three lanes and the short labels are editorial. "
        "The figures on deaf-mutes and the blind (pp. 117 f., counts of 1864 and 1867) are attached as a table. "
        "Not used are the monthly distribution of cases in Hohenleuben, the disease profile of Lobenstein in detail, the deaf-mutes and blind by district and the single years of the musters; they are in the single analyses."),
    "conversions": convs,
    "caveats": [
        bi("Die drei Orte sind nicht unmittelbar vergleichbar: Lobenstein beruht auf der zehnjährigen Erfahrung eines Arztes, Gera auf der inneren Krankenhausstation, vor allem Fabrikarbeitern und Armen, Hohenleuben auf dem ganzen Ort. Zeitgenössische Krankheitsnamen sind nicht mit modernen Diagnosen gleichzusetzen.",
           "The three places are not directly comparable: Lobenstein rests on the ten years of experience of one physician, Gera on the internal hospital ward, mainly factory workers and the poor, Hohenleuben on the whole town. Contemporary disease names cannot be equated with modern diagnoses."),
        bi("Die gedruckten Prozentwerte der Krätze in Gera lassen sich nicht aus den gedruckten Fallzahlen ableiten (413 von 1010 wären 40,9, gedruckt sind 13,60 Prozent); Brückners Bezugsgröße ist unbekannt. Die Grafik zeigt die gedruckten Werte.",
           "The printed percentages of scabies in Gera cannot be derived from the printed case numbers (413 of 1010 would be 40.9, printed is 13.60 percent); Brückner’s base is unknown. The chart shows the printed values."),
        bi("Bei den Militärpflichtigen stimmt die gedruckte Summe für 1866 (575) nicht mit der Addition der Einzelzeilen (515) überein; die Einzelgründe ergeben deshalb nur 67,02 statt der gedruckten 69,71 Prozent. Die Prozentspalte bezieht sich auf den Durchschnitt von 799.",
           "For the conscripts the printed total for 1866 (575) does not match the sum of the single rows (515); the single reasons therefore add up to only 67.02 instead of the printed 69.71 percent. The percentage column refers to the average of 799."),
        bi("Die Zeitleiste enthält Beispiele, die Brückner anführt, keine vollständige Chronik der Epidemien. Die Jahre um 1570, 1600, 1620 und 1760 sind ungefähre Angaben; die Impfung von 1790 fand außerhalb des Fürstentums statt.",
           "The timeline contains examples cited by Brückner, not a complete chronicle of epidemics. The years about 1570, 1600, 1620 and 1760 are approximate; the inoculation of 1790 took place outside the principality."),
    ],
    "datasets": datasets,
    "charts": charts,
    "transcription_issues": issues,
    "keywords": {
        "de": ["Krankheiten", "Gesundheit", "Ärzte", "Seuchen", "Blattern", "Impfung", "Cholera", "Krätze", "Militärtauglichkeit", "Musterung", "Taubstumme", "Blinde"],
        "en": ["diseases", "health", "physicians", "epidemics", "smallpox", "vaccination", "cholera", "scabies", "fitness for service", "conscription", "deaf-mutes", "blind"],
    },
    "related": ["geburten-sterbefaelle", "alter-familie", "sagen-brauch", "verfassung-verwaltung"],
    "generated_by": "Claude Sonnet 5.5 (Agent F4), aus 4 Einzelauswertungen zusammengeführt",
    "date": "2026-10-02",
}
if not convs:
    del feature["conversions"]

if __name__ == "__main__":
    check_limits(feature)
    write_feature(feature)
    with open("C:/Users/totom/Projects/reuss-edition/data/analyses/_work/F4/check_gesundheit.txt", "w", encoding="utf-8") as f:
        for k, v in log:
            f.write(f"{k}: {v}\n")
