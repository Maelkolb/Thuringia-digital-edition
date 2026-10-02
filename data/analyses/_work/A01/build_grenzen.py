"""Build analysis grenzen-umfang-nachbarlaender (A01): boundary lengths by neighbour, p. 5."""
import re
from fractions import Fraction
from common import *

T = lambda de, en: {"de": de, "en": en}

b1 = text("5", "b1")
b2 = text("5", "b2")

# ---- parse the printed boundary lengths ("auf Reuß ä. L. 22, auf Sachsen 8, auf Bayern 7 1/5, ...") ----
def parse_len(s):
    s = s.strip()
    m = re.match(r"^(\d+)(?:\s+(\d+)/(\d+))?$", s)
    return float(Fraction(int(m.group(1))) + (Fraction(int(m.group(2)), int(m.group(3))) if m.group(2) else 0))

ob = re.findall(r"auf (Reuß ä\. L\.|Sachsen|Bayern|Preußen|Schwarzburg|Meiningen) (\d+(?: \d/\d)?)", b1.split("kommen")[1])
ob = [(n, t) for n, t in ob]
un = re.findall(r"auf (Altenburg|Weimar|Preußen|Sachsen) (\d+)", b2.split("18 stündigen")[1])
print(ob, un)
assert len(ob) == 6 and len(un) == 4
rows = []
for n, t in ob:
    rows.append(["Oberland", n, t, parse_len(t)])
for n, t in un:
    rows.append(["Unterland", n, t, parse_len(t)])
tot = {"Oberland": 48.0, "Unterland": 18.0}
assert "zu 48 Stunden" in b1 and "18 stündigen Umfange" in b2
for lt in tot:
    s = sum(r[3] for r in rows if r[0] == lt)
    assert abs(s - tot[lt]) < 1e-9, (lt, s)
for r in rows:
    r.append(round(100 * r[3] / tot[r[0]], 1))

# neighbour totals
from collections import defaultdict
nb_tot = defaultdict(float)
for r in rows:
    nb_tot[r[1]] += r[3]
total = sum(nb_tot.values())
print(dict(nb_tot), total)
order = sorted(nb_tot, key=lambda k: -nb_tot[k])
print(order)

DOMAIN = ["Reuß ä. L.", "Sachsen", "Bayern", "Preußen", "Schwarzburg", "Meiningen", "Altenburg", "Weimar"]
assert set(DOMAIN) == set(nb_tot)
rows = [[r[0], r[1], DOMAIN.index(r[1]) + 1, r[2], r[3], r[4]] for r in rows]
share_aeL_ob = 100 * 22 / 48
share_aeL_all = 100 * nb_tot["Reuß ä. L."] / total
share_alt_un = 100 * 9 / 18
num = lambda x: fmt(x, 1)
numen = lambda x: fmt(x, 1, "en")
LB = T("Landesteil", "Part of the country")
NB = T("Angrenzender Staat", "Neighbouring state")

ana = {
    "id": "grenzen-umfang-nachbarlaender",
    "title": T("Grenzen: Umfang von Ober- und Unterland nach Nachbarstaaten", "Boundaries: perimeter of Oberland and Unterland by neighbouring state"),
    "category": "geography",
    "section": "t1-1-1",
    "sources": [{"page": "5", "block": "b1"}, {"page": "5", "block": "b2"}],
    "summary": T(
        "Brückner gibt für beide Landesteile die Länge der Grenze in Stunden an und verteilt sie auf die angrenzenden Staaten: das Oberland (48 Stunden) grenzt an sechs, das Unterland (18 Stunden) an vier Nachbarn. Die Auswertung zeigt, welche Staaten den größten Anteil haben und dass die Teilwerte genau die Gesamtumfänge ergeben.",
        "Brückner gives the length of the boundary of both parts in hours (Stunden) and distributes it among the neighbouring states: the Oberland (48 Stunden) borders six, the Unterland (18 Stunden) four neighbours. The analysis shows which states have the largest share and that the partial values add up exactly to the total perimeters."),
    "method": T(
        "Die Zahlen stehen im Fließtext auf S. 5 (Oberland: »Den Umfang … zu 48 Stunden angenommen, kommen auf Reuß ä. L. 22, auf Sachsen 8 …«; Unterland: »Von seinem 18 stündigen Umfange kommen auf Altenburg 9 …«). Gemischte Brüche (7 1/5, 3 3/5, 1 1/5) wurden in Dezimalzahlen umgesetzt (7,2; 3,6; 1,2). Der Umfang wird nach Brückner »in seinen Krümmungen und mit Einschlusse seiner Ex- und Enclaven« gemessen. Eine Umrechnung der Stunden in Kilometer ist nicht möglich: Brückners Maßtabelle (S. 831–832) enthält keine Wegstunde.",
        "The figures are in the running text on p. 5 (Oberland: “Den Umfang … zu 48 Stunden angenommen, kommen auf Reuß ä. L. 22, auf Sachsen 8 …”; Unterland: “Von seinem 18 stündigen Umfange kommen auf Altenburg 9 …”). Mixed fractions (7 1/5, 3 3/5, 1 1/5) were converted to decimals (7.2, 3.6, 1.2). Brückner measures the perimeter “in its windings and including its exclaves and enclaves”. A conversion of the hours into kilometres is not possible: Brückner's table of units (pp. 831–832) contains no walking hour."),
    "findings": [
        T(f"Die Teilwerte ergeben genau die genannten Umfänge: 22 + 8 + 7 1/5 + 6 + 3 3/5 + 1 1/5 = 48 Stunden (Oberland) und 9 + 5 + 3 + 1 = 18 Stunden (Unterland), zusammen {fmt(total, 0)} Stunden.",
          f"The partial values add up exactly to the stated perimeters: 22 + 8 + 7 1/5 + 6 + 3 3/5 + 1 1/5 = 48 Stunden (Oberland) and 9 + 5 + 3 + 1 = 18 Stunden (Unterland), {fmt(total, 0, 'en')} Stunden together."),
        T(f"Die längste gemeinsame Grenze hat das Oberland mit Reuß ä. L.: 22 Stunden, das sind {num(share_aeL_ob)} % seines Umfangs und {num(share_aeL_all)} % der gesamten Grenzlänge beider Landesteile.",
          f"The longest common boundary is that of the Oberland with Reuss (elder line): 22 Stunden, i.e. {numen(share_aeL_ob)} % of its perimeter and {numen(share_aeL_all)} % of the total boundary length of both parts."),
        T(f"Das Unterland grenzt zur Hälfte ({num(share_alt_un)} %) an Altenburg (9 von 18 Stunden); Weimar, Preußen und Sachsen teilen sich die andere Hälfte (5, 3 und 1 Stunde).",
          f"Half of the Unterland's boundary ({numen(share_alt_un)} %) borders Altenburg (9 of 18 Stunden); Weimar, Prussia and Saxony share the other half (5, 3 and 1 Stunde)."),
        T(f"Preußen (6 + 3) und Sachsen (8 + 1) grenzen an beide Landesteile und kommen je auf 9 Stunden, ebenso Altenburg (nur Unterland); Bayern ({num(nb_tot['Bayern'])} Stunden) grenzt nur an das Oberland, Meiningen ({num(nb_tot['Meiningen'])}) hat die kürzeste Grenze.",
          f"Prussia (6 + 3) and Saxony (8 + 1) border both parts and each reach 9 Stunden, as does Altenburg (Unterland only); Bavaria ({numen(nb_tot['Bayern'])} Stunden) borders only the Oberland, Meiningen ({numen(nb_tot['Meiningen'])}) has the shortest boundary."),
    ],
    "caveats": [
        T("Die »Stunde« ist hier ein Wegmaß; Brückner erklärt sie nicht. Die Längen sind daher nur untereinander vergleichbar.",
          "The “Stunde” is a walking-time measure here, which Brückner does not explain. The lengths are therefore comparable with each other only."),
        T("Brückner nennt die Nachbarn nur mit Kurzbezeichnungen; gemeint sind vermutlich das Königreich Sachsen, das Herzogtum Sachsen-Altenburg, das Großherzogtum Sachsen-Weimar und das Herzogtum Sachsen-Meiningen. Die Zuordnung der Nachbarn zu den Landesteilen folgt dem Text von S. 5.",
          "Brückner names the neighbours only by short names; presumably the Kingdom of Saxony, the Duchy of Saxe-Altenburg, the Grand Duchy of Saxe-Weimar and the Duchy of Saxe-Meiningen are meant. The assignment of the neighbours to the parts follows the text of p. 5."),
    ],
    "conversions": [],
    "datasets": [
        {"name": "grenzen", "title": T("Grenzlängen nach Nachbarstaaten", "Boundary lengths by neighbouring state"),
         "columns": [
             {"name": "landesteil", "label": LB, "type": "string", "unit": None},
             {"name": "nachbar", "label": NB, "type": "string", "unit": None},
             {"name": "nachbar_nr", "label": T("Reihenfolge der Nachbarn", "Order of neighbours"), "type": "integer", "unit": None, "derived": True, "note": "redaktionell, für Farben und Stapelung"},
             {"name": "laenge_text", "label": T("Länge wie gedruckt", "Length as printed"), "type": "string", "unit": "Stunden"},
             {"name": "laenge_stunden", "label": T("Länge", "Length"), "type": "number", "unit": "Stunden", "derived": True, "note": "gemischte Brüche in Dezimalzahlen"},
             {"name": "anteil", "label": T("Anteil am Umfang des Landesteils", "Share of the part's perimeter"), "type": "number", "unit": "%", "derived": True},
         ],
         "rows": rows, "source_refs": [{"page": "5", "block": "b1"}, {"page": "5", "block": "b2"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "grenzen",
         "title": T("Wer grenzt wie lang an Ober- und Unterland?", "Who borders the Oberland and Unterland, and for how long?"),
         "caption": T("Grenzlänge in Stunden, aufgeteilt nach Nachbarstaaten. Das Oberland hat 48, das Unterland 18 Stunden Umfang.",
                      "Boundary length in hours (Stunden), divided by neighbouring state. The Oberland has a perimeter of 48, the Unterland of 18 Stunden."),
         "vegalite": {
             "height": 150,
             "transform": [{"stack": "laenge_stunden", "groupby": ["landesteil"], "sort": [{"field": "nachbar_nr", "order": "ascending"}], "as": ["start", "end"]},
                           {"calculate": "(datum.start + datum.end) / 2", "as": "mitte"}],
             "layer": [
                 {"mark": "bar",
                  "encoding": {
                      "y": {"field": "landesteil", "type": "nominal", "title": None, "sort": ["Oberland", "Unterland"]},
                      "x": {"field": "start", "type": "quantitative", "title": "Stunden"},
                      "x2": {"field": "end"},
                      "color": {"field": "nachbar", "type": "nominal", "title": NB, "scale": {"domain": DOMAIN}, "legend": {"columns": 4}},
                      "tooltip": [{"field": "landesteil", "title": LB},
                                  {"field": "nachbar", "title": NB},
                                  {"field": "laenge_text", "title": T("Länge (Stunden, wie gedruckt)", "Length (hours, as printed)")},
                                  {"field": "anteil", "title": T("Anteil am Umfang (%)", "Share of perimeter (%)")}]}},
             ]}},
        {"id": "c2", "dataset": "grenzen",
         "title": T("Grenzlänge je Nachbarstaat, beide Landesteile zusammen", "Boundary length by neighbouring state, both parts together"),
         "caption": T("Summe der Grenzlängen von Ober- und Unterland in Stunden. Preußen, Sachsen und Altenburg haben jeweils 9 Stunden.",
                      "Sum of the boundary lengths of Oberland and Unterland in Stunden. Prussia, Saxony and Altenburg each have 9 Stunden."),
         "vegalite": {
             "height": 260,
             "layer": [
                 {"mark": "bar",
                  "encoding": {
                      "y": {"field": "nachbar", "type": "nominal", "title": None, "sort": "-x"},
                      "x": {"aggregate": "sum", "field": "laenge_stunden", "type": "quantitative", "title": "Stunden"},
                      "color": {"field": "nachbar", "type": "nominal", "legend": None, "scale": {"domain": DOMAIN}},
                      "tooltip": [{"field": "nachbar", "title": NB},
                                  {"aggregate": "sum", "field": "laenge_stunden", "title": T("Länge (Stunden)", "Length (Stunden)")}]}},
                 {"mark": {"type": "text", "align": "left", "dx": 5, "baseline": "middle"},
                  "encoding": {
                      "y": {"field": "nachbar", "type": "nominal", "sort": "-x"},
                      "x": {"aggregate": "sum", "field": "laenge_stunden", "type": "quantitative"},
                      "text": {"aggregate": "sum", "field": "laenge_stunden", "type": "quantitative", "format": ".1~f"}}},
             ]}},
    ],
    "keywords": T(["Grenzen", "Umfang", "Nachbarstaaten", "Reuß ältere Linie", "Sachsen", "Bayern", "Preußen", "Altenburg", "Weimar", "Meiningen", "Schwarzburg", "Stunde"],
                  ["boundaries", "perimeter", "neighbouring states", "Reuss elder line", "Saxony", "Bavaria", "Prussia", "Altenburg", "Weimar", "Meiningen", "Schwarzburg"]),
    "related": ["lage-vermessene-punkte-laenge-breite", "flaeche-fuerstenthum-vermessung-nachbarn"],
    "generated_by": "Claude Sonnet 5.5 (subagent A01)",
    "date": "2026-10-01",
}
write_analysis(ana)
