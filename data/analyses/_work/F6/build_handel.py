from common import *
import handel_charts as C
from datetime import date

IDS = ["handel-verkehr-begleitscheine-1858-1867", "verkehr-eisenbahn-geldinstitute-zeitleiste",
       "handel-jahrmaerkte-marktorte-landesteile", "staat-chausseen-laenge-kosten-1868",
       "kultur-zeitungsbezug-durch-die-post"]
A = {i: archive(i) for i in IDS}
a_beg, a_bahn, a_mark, a_chaus, a_zeit = (A[k] for k in IDS)

# ---------------------------------------------------------------- datasets
P, R = base_layers()
places = {r[0]: r for r in P["rows"]}
ALIAS = {"Grossaga": "Großaga", "Weissendorf": "Weißendorf", "Ossla": "Oßla"}   # Brückner's spelling in the market list
LON = col("lon", "Länge", "Longitude", "number", "° O", True, "GeoNames (Kartengrundlage orte_basis), nicht im Druck")
LAT = col("lat", "Breite", "Latitude", "number", "° N", True, "GeoNames (Kartengrundlage orte_basis), nicht im Druck")


def coord(r, i):
    return places[ALIAS.get(r["place"], r["place"])][i]


ds_beg = dataset(a_beg, "begleitscheine")
ds_mark = dataset(a_mark, "maerkte", add_cols=[(LON, lambda r: coord(r, 1)), (LAT, lambda r: coord(r, 2))])
ds_ereig = dataset(a_bahn, "ereignisse")
ds_kosten = dataset(a_chaus, "costs", new_name="chausseekosten")
ds_zeit = dataset(a_zeit, "districts", new_name="zeitungen_landesteile")
ds_orte = copy.deepcopy(P)
ds_fluesse = copy.deepcopy(R)

beg, mark, ereig, kosten, zeit = rows(ds_beg), rows(ds_mark), rows(ds_ereig), rows(ds_kosten), rows(ds_zeit)

# ---------------------------------------------------------------- numbers
def year_sum(region, year):
    return sum(r["count"] or 0 for r in beg if r["region"] == region and r["year"] == year)

gera58, gera67 = year_sum("Unterland", 1858), year_sum("Unterland", 1867)
ober58, ober67 = year_sum("Oberland", 1858), year_sum("Oberland", 1867)
gera_chg = (gera67 / gera58 - 1) * 100
ober_chg = (ober67 / ober58 - 1) * 100
share58 = gera58 / (gera58 + ober58) * 100
share67 = gera67 / (gera67 + ober67) * 100
schleiz58 = next(r["count"] for r in beg if r["office"] == "Schleiz" and r["year"] == 1858)
schleiz67 = next(r["count"] for r in beg if r["office"] == "Schleiz" and r["year"] == 1867)

n_markets = sum(r["count"] for r in mark)
by_district = {}
for r in mark:
    by_district[r["district"]] = by_district.get(r["district"], 0) + r["count"]
le = by_district["Lobenstein-Ebersdorf"]
by_place = {}
for r in mark:
    by_place[r["place"]] = by_place.get(r["place"], 0) + r["count"]
top_place, top_n = max(by_place.items(), key=lambda kv: kv[1])
n_places = len(by_place)
assert (n_markets, le, top_place, top_n) == (110, 66, "Wurzbach", 14)

bahn = {r["name_de"]: r for r in ereig if r["kind"] == "Eisenbahn"}
d1 = bahn["Eisenbahn Weißenfels–Gera"]
d2 = bahn["Eisenbahn Gößnitz–Gera"]
def days(r):
    a = date.fromisoformat(r["date_start"]); b = date.fromisoformat(r["date_end"])
    return (b - a).days
yrs1, yrs2 = days(d1) / 365.25, days(d2) / 365.25
first_bank = min(int(r["date_start"][:4]) for r in ereig if r["kind"] == "Geldinstitut")

ertrag = next(r["thaler"] for r in kosten if r["item_key"] == "a")
aufwand = next(r["thaler"] for r in kosten if r["item_key"] == "b")
cover = ertrag / aufwand * 100

z = {r["district"]: r for r in zeit}
copies_total = z["Gesamt"]["copies"]
best = max((r for r in zeit if r["district"] != "Gesamt"), key=lambda r: r["copies_per_1000"])
worst = min((r for r in zeit if r["district"] != "Gesamt"), key=lambda r: r["copies_per_1000"])

print(dict(gera58=gera58, gera67=gera67, ober58=ober58, ober67=ober67, gera_chg=round(gera_chg, 1), ober_chg=round(ober_chg, 1),
           share58=round(share58, 1), share67=round(share67, 1), schleiz=(schleiz58, schleiz67), n_markets=n_markets, le=le,
           yrs=(round(yrs1, 2), round(yrs2, 2), days(d1), days(d2)), first_bank=first_bank, cover=round(cover, 1),
           copies_total=copies_total, best=(best["district"], best["copies_per_1000"]), worst=(worst["district"], worst["copies_per_1000"])))

# ---------------------------------------------------------------- texts
title = {"de": "Handel, Märkte und Verkehr", "en": "Trade, markets and transport"}

summary = {
    "de": (f"Als Maß für den Handel druckt Brückner die Zahl der erledigten Begleitscheine: In Gera stieg sie von {gera58} (1858) auf {gera67} (1867), "
           f"im Oberland sank sie von {ober58} auf {ober67}. Von {n_markets} Jahrmärkten fanden {le} in Lobenstein-Ebersdorf statt. "
           f"1859 und 1865 wurden zwei Eisenbahnen nach Gera eröffnet. Brückner erklärt den Gegensatz mit der Lage zu den großen Verkehrsströmen."),
    "en": (f"As a measure of trade Brückner prints the number of customs transit documents processed: in Gera it rose from {gera58} (1858) to {gera67} (1867), "
           f"in the Oberland it fell from {ober58} to {ober67}. Of {n_markets} annual markets, {le} took place in Lobenstein-Ebersdorf. "
           f"Two railways to Gera opened in 1859 and 1865. Brückner explains the contrast by the position relative to the great traffic flows."),
}

findings = [
    {"de": (f"Gera erledigte 1867 {de(share67, 1)} Prozent aller Begleitscheine des Landes, 1858 waren es {de(share58, 1)} Prozent. "
            f"Beim Amt Schleiz sank die Zahl von {schleiz58} auf {schleiz67}."),
     "en": (f"In 1867 Gera processed {en(share67, 1)} percent of all transit documents in the principality, in 1858 it was {en(share58, 1)} percent. "
            f"At the Schleiz office the number fell from {schleiz58} to {schleiz67}.")},
    {"de": (f"Der jährliche Reinertrag der Chausseegelder, {de(ertrag)} Taler, deckte {de(cover, 1)} Prozent des Unterhaltungsaufwands von {de(aufwand)} Talern. "
            f"Alle Chausseen unterhielt der Staat."),
     "en": (f"The annual net revenue from road tolls, {en(ertrag)} thalers, covered {en(cover, 1)} percent of the maintenance cost of {en(aufwand)} thalers. "
            f"The state maintained all the highways.")},
    {"de": (f"Die Postämter lieferten {de(copies_total)} Zeitungsexemplare. Je 1.000 Einwohner waren es im Landesteil {best['district']} {de(best['copies_per_1000'], 1)}, "
            f"in {worst['district']} {de(worst['copies_per_1000'], 1)}."),
     "en": (f"The post offices delivered {en(copies_total)} newspaper copies. Per 1,000 inhabitants that was {en(best['copies_per_1000'], 1)} in the district of {best['district']} "
            f"and {en(worst['copies_per_1000'], 1)} in {worst['district']}.")},
]

charts = [
    {"id": "c1", "dataset": "begleitscheine", "extra_datasets": ["ereignisse"],
     "title": {"de": f"Die Begleitscheine stiegen in Gera um {de(gera_chg)} Prozent und sanken im Oberland um {de(-ober_chg)} Prozent",
               "en": f"Transit documents rose {en(gera_chg)} percent in Gera and fell {en(-ober_chg)} percent in the Oberland"},
     "caption": {"de": "Bei den Erledigungsämtern erledigte Begleitscheine (Zollpapiere für Warentransporte) 1858 bis 1867, bezogen auf 1858. Unterland: Amt Gera; Oberland: Ämter Schleiz, Lobenstein und Hirschberg. Gestrichelt: Eröffnung der Bahnen. Quelle: S. 261–262.",
                 "en": "Transit documents (customs papers for goods in transit) processed by the clearing offices, 1858 to 1867, relative to 1858. Unterland: Gera office; Oberland: Schleiz, Lobenstein and Hirschberg offices. Dashed: opening of the railways. Source: pp. 261–262."},
     "vegalite": C.c1},
    {"id": "c2", "dataset": "maerkte", "extra_datasets": ["orte_basis", "fluesse_basis"],
     "title": {"de": f"Im Landesteil Lobenstein-Ebersdorf fanden {le} von {n_markets} Märkten statt, allein {top_n} in {top_place}",
               "en": f"The district of Lobenstein-Ebersdorf had {le} of {n_markets} markets, {top_n} of them in {top_place} alone"},
     "caption": {"de": f"Märkte im Jahr (Jahr-, Kram-, Vieh-, Ross-, Woll- und Kornmärkte, ohne Wochenmärkte) an den {n_places} Marktorten. Graue Punkte: übrige Orte. Quelle: S. 262.",
                 "en": f"Markets per year (fairs, general, cattle, horse, wool and grain markets, without weekly markets) in the {n_places} market towns. Grey dots: other places. Source: p. 262."},
     "vegalite": C.c2},
    {"id": "c3", "dataset": "ereignisse",
     "title": {"de": f"Sparkassen gab es ab {first_bank}, die erste Eisenbahn erreichte Gera 1859, die zweite 1865",
               "en": f"Savings banks existed from {first_bank}, the first railway reached Gera in 1859, the second in 1865"},
     "caption": {"de": "Datierte Einrichtungen von Handel und Verkehr. Dicke Balken: Vertrag bis Eröffnung der Bahn; Punkte: Gründung; dünne Linien: besteht bis 1868. Quelle: S. 258, 261–262.",
                 "en": "Dated institutions of trade and transport. Thick bars: treaty to opening of the railway; dots: foundation; thin lines: in existence until 1868. Source: pp. 258, 261–262."},
     "vegalite": C.c3},
]

method = {
    "de": ("Die Begleitscheine stehen in der Tabelle S. 261 (vier Erledigungsämter, zehn Jahre); ein Strich im Druck ist als fehlender Wert kodiert. "
           "Für den Vergleich der Landesteile bildet Gera das Unterland, Schleiz, Lobenstein und Hirschberg zusammen das Oberland; beide Reihen sind auf 1858 = 100 bezogen. "
           "Die Märkte nennt die Aufzählung S. 262 in Zahlwörtern (»sieben Kram- und Viehmärkte«); jede genannte Art wurde als eine Zeile mit der Anzahl erfasst, ein kombinierter Markt zählt als ein Markt. "
           "Die Koordinaten der Marktorte stammen aus den Ortsdaten der Edition (GeoNames), nicht aus dem Druck. "
           "Die Zeitleiste enthält die Daten, die Brückner für Bahnen, Geldinstitute und Gesetze nennt; bei den Bahnen reicht der Balken vom Vertrag zur Eröffnung. "
           "Die Zeitungszahlen stammen aus der Tabelle S. 168; je 1.000 Einwohner ergibt sich aus Brückners Kennzahl »1 Exemplar auf … Einwohner«. "
           "Alle Beträge in Talern (1 Taler = 30 Silbergroschen)."),
    "en": ("The transit documents are in the table on p. 261 (four clearing offices, ten years); a dash in the print is coded as a missing value. "
           "To compare the districts, Gera stands for the Unterland and Schleiz, Lobenstein and Hirschberg together for the Oberland; both series are set to 1858 = 100. "
           "The markets are given in number words in the list on p. 262 (“seven general and cattle markets”); each kind named was recorded as one row with its number, a combined market counts as one market. "
           "The coordinates of the market towns come from the edition’s place data (GeoNames), not from the print. "
           "The timeline contains the dates that Brückner gives for railways, financial institutions and laws; for the railways the bar runs from the treaty to the opening. "
           "The newspaper figures come from the table on p. 168; per 1,000 inhabitants follows from Brückner’s ratio “1 copy per … inhabitants”. "
           "All amounts are in thalers (1 thaler = 30 silver groschen)."),
}

caveats = [
    {"de": ("Die Begleitscheine erfassen nach Brückner nur einen Teil der Aus- und Einfuhr; er hält sie für kennzeichnend für den übrigen Verkehr. Die Zahl der Scheine sagt nichts über Wert oder Menge der Waren "
            "und hängt auch von Lage und Zuständigkeit der Ämter ab (Hirschberg erscheint nur 1864 bis 1866 mit je einem Schein)."),
     "en": ("According to Brückner the documents cover only part of exports and imports; he takes them to be characteristic of the rest of the traffic. The number of documents says nothing about the value or quantity of goods "
            "and also depends on the location and competence of the offices (Hirschberg appears only in 1864 to 1866, with one document each).")},
    {"de": ("Brückner nennt die Zahl der Märkte pro Jahr, nicht ihre Dauer oder Bedeutung. Die Gruppierung der Marktarten ist eine Vereinfachung; Titschendorf ist laut Fußnote angeblich zur Zeit eingestellt, aber mitgezählt. "
            "Einzelne Formulierungen (»sechs Kram-, drei Viehmärkte«) sind mehrdeutig und in der Methode gelesen."),
     "en": ("Brückner gives the number of markets per year, not their duration or importance. The grouping of market kinds is a simplification; according to a footnote Titschendorf is said to be suspended at present, but it is counted. "
            "Some phrasings (“six general, three cattle markets”) are ambiguous and are read as described in the method.")},
    {"de": ("Die Zeitleiste verzeichnet nur, was Brückner mit Jahr oder Tag nennt. Die Gewerbebank in Gera, der Vorschussverein in Schleiz und die Handelskammer bleiben ohne Datum. "
            "»Vertrag« bezeichnet bei den Bahnen den Staatsvertrag, nicht den Baubeginn."),
     "en": ("The timeline lists only what Brückner dates by year or day. The trade bank in Gera, the advance association in Schleiz and the chamber of commerce remain undated. "
            "For the railways “treaty” means the state treaty, not the start of construction.")},
    {"de": ("Das Jahr der Zeitungserhebung nennt Brückner nicht (um 1868); erfasst ist nur der Bezug durch die Post. Der Unterhaltungsaufwand der Chausseen ist als jährlicher Betrag gelesen; Strecken, die Preußen und Sachsen unterhalten, fehlen."),
     "en": ("Brückner does not give the year of the newspaper survey (around 1868); only subscriptions through the post are counted. The cost of maintaining the highways is read as an annual amount; stretches maintained by Prussia and Saxony are not included.")},
]

a = {
    "id": "handel-verkehr",
    "title": title,
    "category": "trade-transport",
    "section": "t1-3-7",
    "merges": IDS,
    "sources": uniq_sources(*[A[i]["sources"] for i in IDS]),
    "summary": summary,
    "findings": findings,
    "method": method,
    "conversions": [{"from": "Taler", "to": "Silbergroschen", "factor_or_formula": "1 Taler = 30 Silbergroschen", "reference": "Brückner S. 278"}],
    "caveats": caveats,
    "datasets": [ds_beg, ds_mark, ds_ereig, ds_orte, ds_fluesse, ds_kosten, ds_zeit],
    "charts": charts,
    "transcription_issues": [],
    "keywords": {
        "de": ["Handel", "Verkehr", "Märkte", "Jahrmärkte", "Begleitscheine", "Eisenbahn", "Sparkasse", "Geraer Bank", "Chaussee", "Zeitungen", "Gera", "Oberland"],
        "en": ["trade", "transport", "markets", "fairs", "transit documents", "railway", "savings bank", "Bank of Gera", "highway", "newspapers", "Gera", "Oberland"]},
    "related": ["berufe-gewerbe", "viehzucht", "bergbau", "staatsfinanzen"],
    "generated_by": GENERATED_BY.format(n=len(IDS)),
    "date": DATE,
}
for i in IDS:
    a["transcription_issues"] += A[i].get("transcription_issues", [])
if not a.get("transcription_issues"):
    a.pop("transcription_issues", None)
check_limits(a)
write_analysis(a)
