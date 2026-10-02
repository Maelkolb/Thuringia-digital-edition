"""A11-17: Selbsthilfe der arbeitenden Klassen: Sterbe-, Kranken- und Vorschusskassen nach Gründungsjahr (pp. 302-303)."""
from common import *

TYPES = {
    "a": ("Sterbekasse", "Death-benefit society", "p302 b4"),
    "b": ("Begräbnis- mit Krankenkasse", "Burial and sickness fund", "p302 b5"),
    "c": ("Krankenunterstützungsverein", "Sickness-benefit society", "p302 b6 / p303 b1"),
    "d": ("Vorschussverein (Kredit)", "Credit association", "p303 b3-b4"),
}
G, S, L = ("a", "Gera und Unterland", "Gera and Lower Land"), ("b", "Schleiz und Oberland", "Schleiz and Upper Land"), ("c", "Lobenstein-Ebersdorf", "Lobenstein-Ebersdorf")
# key, type, place_de, place_en, year, region
ROWS = [
    ("a1", "a", "Schleiz", "Schleiz", 1777, S), ("a2", "a", "Schleiz", "Schleiz", 1782, S),
    ("a3", "a", "Hirschberg", "Hirschberg", 1804, L), ("a4", "a", "Hirschberg", "Hirschberg", 1806, L),
    ("a5", "a", "Wurzbach", "Wurzbach", 1853, L), ("a6", "a", "Harra", "Harra", 1859, L), ("a7", "a", "Tanna", "Tanna", 1864, S),
    ("a8", "a", "Gera (Sterbefiscus mehrerer Innungen)", "Gera (burial fund of several guilds)", 1860, G),
    ("a9", "a", "Gera (Sterbefiscus der Zeugmacherinnung)", "Gera (burial fund of the cloth-weavers' guild)", 1867, G),
    ("b1", "b", "Gera und Nachbarorte (Hand- und Fabrikarbeiter)", "Gera and neighbouring places (manual and factory workers)", 1849, G),
    ("b2", "b", "Gera (Krankenhilfsverein der Heimatberechtigten)", "Gera (sickness-aid society of the residents)", 1852, G),
    ("b3", "b", "Gera (Sterbefiscus des Krankenhilfsvereins)", "Gera (burial fund of the sickness-aid society)", 1864, G),
    ("b4", "b", "Triebes, Niederböhmsdorf, Weissendorf (Gewerbsgehilfen)", "Triebes, Niederböhmsdorf, Weissendorf (trade assistants)", 1858, G),
    ("b5", "b", "Langenberg (Einwohner)", "Langenberg (inhabitants)", 1861, G),
    ("b6", "b", "Roschitz (Einwohner)", "Roschitz (inhabitants)", 1863, G),
    ("b7", "b", "Gera (Frauensterbefiscus)", "Gera (women's burial fund)", 1865, G),
    ("b8", "b", "Gera (Frauenkrankenhilfsverein)", "Gera (women's sickness-aid society)", 1868, G),
    ("b9", "b", "Frankenthal (Einwohner)", "Frankenthal (inhabitants)", 1865, G),
    ("b10", "b", "Naundorf und Umgegend (arbeitende Klassen)", "Naundorf and surroundings (working classes)", 1866, G),
    ("b11", "b", "Leumnitz, Laasen, Trebnitz, Zwötzen, Zschippern, Kaimberg (Arbeiter)", "Leumnitz, Laasen, Trebnitz, Zwötzen, Zschippern, Kaimberg (workers)", 1866, G),
    ("b12", "b", "Hohenleuben (Gesellen und Arbeitsgehilfen)", "Hohenleuben (journeymen and assistants)", 1867, G),
    ("b13", "b", "Dürrenebersdorf, Weissig, Zeulsdorf (Einwohner)", "Dürrenebersdorf, Weissig, Zeulsdorf (inhabitants)", 1869, G),
    ("c1", "c", "Grüna, Stübnitz, Rüdersdorf, Hartmannsdorf (Maurer, Zimmerleute)", "Grüna, Stübnitz, Rüdersdorf, Hartmannsdorf (masons, carpenters)", 1864, G),
    ("c2", "c", "Großsaara und Nachbarorte (Maurer, Zimmerleute)", "Großsaara and neighbouring places (masons, carpenters)", 1864, G),
    ("c3", "c", "Gera (Schmiedegesellen)", "Gera (journeymen smiths)", 1866, G),
    ("c4", "c", "Köstritz und Umgegend (Maurer, Zimmergesellen)", "Köstritz and surroundings (masons, journeymen carpenters)", 1866, G),
    ("c5", "c", "Langenberg (Zeugmacher, Webergehülfen)", "Langenberg (cloth-weavers, weaver assistants)", 1866, G),
    ("c6", "c", "Gera und Umgegend (Buchdruckergehülfen)", "Gera and surroundings (printers' assistants)", 1867, G),
    ("c7", "c", "Gera (Arbeiter auf Webstühlen)", "Gera (loom workers)", 1867, G),
    ("c8", "c", "Gera (Zeugmachergehülfen)", "Gera (cloth-weaver assistants)", 1867, G),
    ("d1", "d", "Schleiz (Vorschussverein)", "Schleiz (credit association)", 1848, S),
    ("d2", "d", "Gera (Darlehnskassenverein, seit 1869 Gewerbebank)", "Gera (loan-fund association, since 1869 trade bank)", 1859, G),
]
assoc = []
for k, t, pde, pen, yr, reg in ROWS:
    assoc.append([k, t, TYPES[t][0], TYPES[t][1], pde, pen, yr, reg[0], reg[1], reg[2]])
n = len(assoc)
years = [r[6] for r in assoc]
pre1850 = [y for y in years if y < 1850]
y1860s = [y for y in years if 1860 <= y <= 1869]
by_region = {}
for r in assoc:
    by_region[r[9]] = by_region.get(r[9], 0) + 1
by_type = {}
for r in assoc:
    by_type[r[2]] = by_type.get(r[2], 0) + 1
print(n, len(pre1850), len(y1860s), by_region, by_type)

# per-year counts 1848-1869 by type (long) ---------------------------------------------------
peryear = []
for y in range(1848, 1870):
    for t in "abcd":
        c = len([r for r in assoc if r[6] == y and r[1] == t])
        if c:
            peryear.append([y, t, TYPES[t][0], TYPES[t][1], c])
# cumulative
cum = []
c = 0
for y in sorted(set(years)):
    c += years.count(y)
    cum.append([y, c, years.count(y)])
print(cum)
peak = max(set(years), key=lambda y: years.count(y))

# --- credit associations (p. 303 b3, b4) ------------------------------------------------------
credit = [
    ["Gera", "Gera (Gewerbebank)", "Gera (trade bank)", 846, 291196, 983084, 3717],
    ["Schleiz", "Schleiz", "Schleiz", 720, 24526, 104422, 509],
]
for c_ in credit:
    c_.append(round(c_[4] / c_[3], 1))
    c_.append(round(c_[5] / c_[3], 1))
print(credit)
ratio_assets = credit[0][4] / credit[1][4]
ratio_members = credit[0][3] / credit[1][3]
ratio_turn = credit[0][5] / credit[1][5]


def D(x, nd=0):
    return fmt_de(x, nd)


def E(x, nd=0):
    return fmt_en(x, nd)


gera_n = by_region["Gera and Lower Land"]
ana = {
    "id": "armenwesen-selbsthilfe-kassen-gruendungsjahre-1777-1869",
    "title": bi("Selbsthilfe der arbeitenden Klassen: Sterbe-, Kranken- und Vorschusskassen nach Gründungsjahr", "Self-help of the working classes: burial, sickness and credit societies by year of founding"),
    "category": "welfare",
    "section": "t1-4-8",
    "sources": [{"page": "302", "block": "b4"}, {"page": "302", "block": "b5"}, {"page": "302", "block": "b6"}, {"page": "303", "block": "b1"}, {"page": "303", "block": "b2"}, {"page": "303", "block": "b3"}, {"page": "303", "block": "b4"}, {"page": "302", "block": "b3"}],
    "summary": bi(
        f"Brückner zählt unter dem Armenwesen {n} Selbsthilfeeinrichtungen der arbeitenden Klassen auf: Leichencommunen und Sterbefisci, Begräbnis- mit Krankenkassen, Krankenunterstützungsvereine und zwei Vorschussvereine, jeweils mit Gründungsjahr. Die Auswertung macht den raschen Anstieg der Gründungen seit 1849 sichtbar und vergleicht die beiden Vorschussvereine in Gera und Schleiz.",
        f"Under poor relief Brückner lists {n} self-help institutions of the working classes: death-benefit societies, burial funds with sickness funds, sickness-benefit societies and two credit associations, each with its year of founding. The analysis shows the rapid rise of foundings since 1849 and compares the two credit associations in Gera and Schleiz.",
    ),
    "method": bi(
        "Aus den Aufzählungen S. 302–303 wurde jede genannte Einrichtung als eine Zeile mit Gründungsjahr erfasst; Einrichtungen, die Brückner mit zwei Jahreszahlen nennt (z. B. Krankenhilfsverein 1852 mit Sterbefiscus 1864), sind als zwei Einrichtungen gezählt. Die Zuordnung zu den Landestheilen (Gera und Unterland, Schleiz und Oberland, Lobenstein-Ebersdorf) ist editorisch nach den Ortsnamen vorgenommen. Die Vorschussvereine stehen im Text S. 303 (Mitglieder, Aktiva/Passiva, Jahreseinnahme, Gewinn, jeweils Ende 1867); Thaler ohne Silbergroschen und Pfennige; Kennzahlen je Mitglied sind abgeleitet.",
        "From the lists on pp. 302–303 each institution named was recorded as one row with its year of founding; institutions that Brückner gives with two years (e.g. sickness-aid society 1852 with burial fund 1864) are counted as two. The assignment to the regions (Gera and Lower Land, Schleiz and Upper Land, Lobenstein-Ebersdorf) was made editorially from the place names. The credit associations are in the text of p. 303 (members, assets/liabilities, annual income, profit, each at the end of 1867); Thaler without Silbergroschen and Pfennige; per-member figures are derived.",
    ),
    "findings": [
        bi(f"Von den {n} genannten Einrichtungen entstanden nur {len(pre1850)} vor 1850 (1777, 1782, 1804, 1806, der schleizer Vorschussverein 1848 und die geraer Arbeiterkasse 1849); {len(y1860s)} ({D(100*len(y1860s)/n,0)} %) wurden in den zehn Jahren 1860–1869 gegründet, die meisten 1866 und 1867 ({D(years.count(1866))} und {D(years.count(1867))} Gründungen).",
           f"Of the {n} institutions named only {len(pre1850)} arose before 1850 (1777, 1782, 1804, 1806, the Schleiz credit association of 1848 and the Gera workers' fund of 1849); {len(y1860s)} ({E(100*len(y1860s)/n,0)} %) were founded in the ten years 1860–1869, most in 1866 and 1867 ({E(years.count(1866))} and {E(years.count(1867))} foundings)."),
        bi(f"Die Mehrzahl liegt im Gebiet um Gera: {D(gera_n)} von {n} Einrichtungen ({D(100*gera_n/n,0)} %); Schleiz und Oberland haben {D(by_region['Schleiz and Upper Land'])}, Lobenstein-Ebersdorf {D(by_region['Lobenstein-Ebersdorf'])}. Das bestätigt Brückners Bemerkung, die Selbsthilfe sei im geraer und reichenfelser Gebiet weiter fortgeschritten (S. 302).",
           f"The majority lie in the area around Gera: {E(gera_n)} of {n} institutions ({E(100*gera_n/n,0)} %); Schleiz and Upper Land have {E(by_region['Schleiz and Upper Land'])}, Lobenstein-Ebersdorf {E(by_region['Lobenstein-Ebersdorf'])}. This confirms Brückner's remark that self-help was further advanced in the Gera and Reichenfels areas (p. 302)."),
        bi(f"Die älteren Sterbekassen (Schleiz 1777/1782, Hirschberg 1804/1806) haben feste Beiträge; die Krankenkassen kommen erst seit 1849 hinzu und überwiegen: {D(by_type['Begräbnis- mit Krankenkasse'])} Begräbnis- mit Krankenkassen und {D(by_type['Krankenunterstützungsverein'])} reine Krankenunterstützungsvereine gegenüber {D(by_type['Sterbekasse'])} Sterbekassen.",
           f"The older death-benefit societies (Schleiz 1777/1782, Hirschberg 1804/1806) have fixed contributions; sickness funds appear only from 1849 and predominate: {E(by_type['Begräbnis- mit Krankenkasse'])} burial funds with sickness funds and {E(by_type['Krankenunterstützungsverein'])} pure sickness-benefit societies against {E(by_type['Sterbekasse'])} death-benefit societies."),
        bi(f"Der Vorschussverein in Gera hat mit {D(credit[0][3])} Mitgliedern nur das {D(ratio_members,1)}fache der Mitglieder des schleizer Vereins ({D(credit[1][3])}), aber das {D(ratio_assets,0)}fache an Aktiva und das {D(ratio_turn,1)}fache an Jahreseinnahme; je Mitglied sind es {D(credit[0][7],0)} gegenüber {D(credit[1][7],0)} Thalern an Aktiva.",
           f"The credit association in Gera has only {E(ratio_members,1)} times the members of the Schleiz association ({E(credit[0][3])} against {E(credit[1][3])}), but {E(ratio_assets,0)} times the assets and {E(ratio_turn,1)} times the annual income; per member this is {E(credit[0][7],0)} against {E(credit[1][7],0)} Thaler of assets."),
    ],
    "caveats": [
        bi("Die Aufzählungen nennen Gründungsjahre, aber weder Mitglieder noch Kassenstände der Sterbe- und Krankenkassen; die Zahl der Einrichtungen sagt daher nichts über ihre Größe oder ihren Bestand 1868. Teils nennt Brückner mehrere Orte oder Berufsgruppen in einer Einrichtung, die hier als eine Einheit zählt.",
           "The lists give founding years but neither members nor funds of the burial and sickness societies; the number of institutions therefore says nothing about their size or existence in 1868. Brückner sometimes names several places or occupational groups in one institution, which counts as one unit here."),
        bi("Die Silbergroschen und Pfennige bei den Vorschussvereinen sind weggelassen (Gera Aktiva 291.196 Thlr. 2 Sgr. 10 Pf., Schleiz 24.526 Thlr. 27 Sgr. 6 Pf.); Aktiva und Passiva sind gleich groß (Bilanzsumme). Beim Gewinn des geraer Vereins (3717 Thlr.) steht ein eigenes Vermögen von 41.503 Thlr. neben fremdem Kapital von 249.110 Thlr. (Verhältnis 1 : 6); für Schleiz fehlt eine solche Angabe.",
           "The Silbergroschen and Pfennige of the credit associations are omitted (Gera assets 291,196 Thlr. 2 Sgr. 10 Pf., Schleiz 24,526 Thlr. 27 Sgr. 6 Pf.); assets and liabilities are equal (balance-sheet total). Against the profit of the Gera association (3,717 Thlr.) stands its own capital of 41,503 Thlr. beside outside capital of 249,110 Thlr. (ratio 1 : 6); for Schleiz no such figure is given."),
    ],
    "datasets": [
        {"name": "societies", "title": bi("Selbsthilfeeinrichtungen mit Gründungsjahr", "Self-help institutions with founding year"),
         "columns": [
             col("key", "Kürzel", "Key", "string"),
             col("type_key", "Kürzel Art", "Type key", "string"),
             col("type_de", "Art", "Type", "string"), col("type_en", "Art (englisch)", "Type (English)", "string"),
             col("place_de", "Ort / Mitglieder", "Place / members", "string"), col("place_en", "Ort / Mitglieder (englisch)", "Place / members (English)", "string"),
             col("year", "Gründungsjahr", "Founding year", "integer"),
             col("region_key", "Kürzel Region", "Region key", "string"),
             col("region_de", "Region", "Region", "string", note="editorische Zuordnung nach Ortsnamen"), col("region_en", "Region (englisch)", "Region (English)", "string"),
         ],
         "rows": assoc, "source_refs": [{"page": "302", "block": "b4"}, {"page": "302", "block": "b5"}, {"page": "302", "block": "b6"}, {"page": "303", "block": "b1"}, {"page": "303", "block": "b3"}, {"page": "303", "block": "b4"}]},
        {"name": "per_year", "title": bi("Neugründungen je Jahr und Art", "New foundings per year and type"),
         "columns": [col("year", "Jahr", "Year", "integer"), col("type_key", "Kürzel Art", "Type key", "string"),
                     col("type_de", "Art", "Type", "string"), col("type_en", "Art (englisch)", "Type (English)", "string"),
                     col("count", "Gründungen", "Foundings", "integer", "Einrichtungen", derived=True)],
         "rows": peryear, "source_refs": [{"page": "302", "block": "b4"}, {"page": "302", "block": "b5"}, {"page": "302", "block": "b6"}, {"page": "303", "block": "b1"}, {"page": "303", "block": "b3"}, {"page": "303", "block": "b4"}]},
        {"name": "cumulative", "title": bi("Zahl der Einrichtungen im Zeitverlauf", "Number of institutions over time"),
         "columns": [col("year", "Jahr", "Year", "integer"), col("cumulative", "Einrichtungen insgesamt (kumuliert)", "Institutions in total (cumulative)", "integer", "Einrichtungen", derived=True),
                     col("new", "Neugründungen im Jahr", "New foundings in the year", "integer", "Einrichtungen", derived=True)],
         "rows": cum, "source_refs": [{"page": "302", "block": "b4"}, {"page": "302", "block": "b5"}, {"page": "302", "block": "b6"}, {"page": "303", "block": "b1"}, {"page": "303", "block": "b3"}, {"page": "303", "block": "b4"}]},
        {"name": "credit", "title": bi("Vorschussvereine in Gera und Schleiz, Ende 1867", "Credit associations in Gera and Schleiz, end of 1867"),
         "columns": [col("town", "Ort", "Town", "string"),
                     col("name_de", "Verein", "Association", "string"), col("name_en", "Verein (englisch)", "Association (English)", "string"),
                     col("members", "Mitglieder", "Members", "integer", "Personen"),
                     col("assets", "Aktiva (= Passiva)", "Assets (= liabilities)", "integer", "Thaler"),
                     col("income", "Jahreseinnahme", "Annual income", "integer", "Thaler"),
                     col("profit", "Gewinn", "Profit", "integer", "Thaler"),
                     col("assets_per_member", "Aktiva je Mitglied", "Assets per member", "number", "Thaler", derived=True),
                     col("income_per_member", "Jahreseinnahme je Mitglied", "Annual income per member", "number", "Thaler", derived=True)],
         "rows": credit, "source_refs": [{"page": "303", "block": "b3"}, {"page": "303", "block": "b4"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "per_year",
         "title": bi("Neugründungen von Selbsthilfeeinrichtungen je Jahr", "New self-help institutions per year"),
         "caption": bi("1848–1869 nach Art; die vier Sterbekassen von 1777–1806 sind nicht dargestellt.", "1848–1869 by type; the four death-benefit societies of 1777–1806 are not shown."),
         "vegalite": {
             "height": 280,
             "mark": "bar",
             "encoding": {
                 "x": {"field": "year", "type": "ordinal", "title": bi("Jahr", "Year"), "axis": {"labelAngle": -45}, "scale": {"domain": list(range(1848, 1870))}},
                 "y": {"field": "count", "type": "quantitative", "title": bi("Neugründungen", "New foundings"), "stack": "zero", "axis": {"tickMinStep": 1, "format": "d"}},
                 "color": {"field": F("type"), "type": "nominal", "title": None, "sort": {"field": "type_key", "op": "min"}, "legend": {"labelLimit": 300, "columns": 2}},
                 "order": {"field": "type_key", "type": "nominal", "sort": "ascending"},
                 "tooltip": [tt("year", "Jahr", "Year"), ttf("type", "Art", "Type"), tt("count", "Gründungen", "Foundings")]}}},
        {"id": "c2", "dataset": "cumulative",
         "title": bi("Zahl der Einrichtungen im Zeitverlauf", "Number of institutions over time"),
         "caption": bi("Kumulierte Zahl der von Brückner genannten Einrichtungen nach Gründungsjahr.", "Cumulative number of the institutions named by Brückner by year of founding."),
         "vegalite": {
             "height": 260,
             "mark": {"type": "line", "interpolate": "step-after", "point": True},
             "encoding": {
                 "x": {"field": "year", "type": "quantitative", "title": bi("Jahr", "Year"), "axis": {"format": "d"}, "scale": {"domain": [1770, 1872]}},
                 "y": {"field": "cumulative", "type": "quantitative", "title": bi("Einrichtungen (kumuliert)", "Institutions (cumulative)")},
                 "tooltip": [tt("year", "Jahr", "Year"), tt("new", "Neugründungen", "New foundings"), tt("cumulative", "kumuliert", "cumulative")]}}},
        {"id": "c3", "dataset": "credit",
         "title": bi("Vorschussvereine: Aktiva je Mitglied, Ende 1867", "Credit associations: assets per member, end of 1867"),
         "caption": bi("Thaler je Mitglied. Der geraer Verein (846 Mitglieder) ist ein Vielfaches größer als der schleizer (720 Mitglieder).", "Thaler per member. The Gera association (846 members) is many times larger than the Schleiz one (720 members)."),
         "vegalite": {
             "height": 150,
             "mark": "bar",
             "encoding": {
                 "y": {"field": "town", "type": "nominal", "title": None, "sort": "-x"},
                 "x": {"field": "assets_per_member", "type": "quantitative", "title": bi("Aktiva je Mitglied (Thaler)", "Assets per member (Thaler)")},
                 "tooltip": [tt("town", "Ort", "Town"), tt("members", "Mitglieder", "Members"), {"field": "assets", "title": bi("Aktiva (Thaler)", "Assets (Thaler)"), "format": ","}, {"field": "assets_per_member", "title": bi("je Mitglied", "per member"), "format": ".1f"}]}}},
    ],
    "keywords": {"de": ["Selbsthilfe", "Sterbekassen", "Krankenkassen", "Begräbniskassen", "Leichencommune", "Vorschussverein", "Gewerbebank", "Armenwesen", "Gera"],
                 "en": ["self-help", "burial societies", "sickness funds", "friendly societies", "credit association", "trade bank", "poor relief", "Gera"]},
}
write(ana)
