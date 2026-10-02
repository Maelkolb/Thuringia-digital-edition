"""Analysis: chronology of dated events in chapter V (kinds per half-century, by house)."""
import collections
from common import *
import events as EVM
from events import EV, KINDS, HOUSES

KORDER = list(KINDS)
HORDER = ["land", "gesamt", "weida", "gera", "plauen", "reuss_plauen", "reuss_alt", "reuss_jung"]
rows = []
for i, e in enumerate(EV, 1):
    hc = e["year"] // 50 * 50
    rows.append([i, e["year"], hc, f"{hc}–{hc+49}", e["kind"], KINDS[e["kind"]][0], KINDS[e["kind"]][1], KORDER.index(e["kind"]) + 1,
                 e["house"], HOUSES[e["house"]][0], HOUSES[e["house"]][1], HORDER.index(e["house"]) + 1,
                 e["de"], e["en"], e["page"], e["block"], "ja" if e["derived_year"] else ""])

n = len(EV)
cnt = collections.Counter(e["kind"] for e in EV)
by_hc = collections.Counter(e["year"] // 50 * 50 for e in EV)
peak_hc, peak_n = max(by_hc.items(), key=lambda kv: kv[1])
second = sorted(by_hc.items(), key=lambda kv: (-kv[1], kv[0]))[:3]
assert second[0][1] == second[1][1]
acq_pre = sum(1 for e in EV if e["kind"] == "acq" and e["year"] < 1350)
loss_pre = sum(1 for e in EV if e["kind"] == "loss" and e["year"] < 1350)
acq_mid = sum(1 for e in EV if e["kind"] == "acq" and 1350 <= e["year"] < 1575)
loss_mid = sum(1 for e in EV if e["kind"] == "loss" and 1350 <= e["year"] < 1575)
fires = [e for e in EV if e["kind"] == "disaster" and "Brand" in e["de"] or e["kind"] == "disaster" and "brennt" in e["de"] or e["kind"] == "disaster" and "Flammen" in e["de"]]
n_dis = cnt["disaster"]
found_pos = [e for e in EV if e["kind"] == "found" and (1595 <= e["year"] <= 1613)]
found_19 = [e for e in EV if e["kind"] == "found" and 1836 <= e["year"] <= 1867]
n_before_1200 = sum(1 for e in EV if e["year"] < 1200)
print(n, cnt, peak_hc, peak_n, second, acq_pre, loss_pre, acq_mid, loss_mid, len(fires), n_dis, len(found_pos), len(found_19), n_before_1200)

REFS = refs_from([(e["page"], e["block"]) for e in EV] + [pb for e in EV for pb in e["also"]])
KDOM = [bi(KINDS[k][0], KINDS[k][1]) for k in KORDER]
KCOL = {"field": bi("kind_de", "kind_en"), "type": "nominal", "title": bi("Art des Ereignisses", "Kind of event"), "scale": {"domain": KDOM}, "legend": {"columns": 4}}
HOUSEFIELD = bi("house_de", "house_en")

a = {
 "id": "geschichte-chronik-ereignisse-530-1867",
 "title": bi("Chronik der datierten Ereignisse in Brückners Landesgeschichte (530–1867)", "Chronology of the dated events in Brückner's history of the land (530–1867)"),
 "category": "history",
 "section": "t1-5",
 "sources": REFS,
 "summary": bi(
  f"Aus dem Erzähltext des Kapitels V (S. 311–393) wurden {n} datierte Ereignisse mit Seiten- und Blockverweis erfasst und nach Art (Krieg, Vertrag, Landerwerb, Landverlust, Teilung, Stiftung/Reform, Brand/Not) und handelndem Haus geordnet. Der Datensatz ist als Verzeichnis der erzählten Geschichte nutzbar; die Diagramme zeigen, wann Brückner Erwerb, Verlust, Teilungen und Verträge berichtet.",
  f"From the narrative of chapter V (pp. 311–393), {n} dated events were recorded with page and block references and sorted by kind (war, treaty, acquisition, loss, partition, foundation/reform, fire/hardship) and by the house involved. The dataset serves as an index of the narrated history; the charts show when Brückner reports acquisition, loss, partitions and treaties."),
 "method": bi(
  "Die Ereignisse wurden beim vollständigen Lesen der Erzähltexte von S. 313–393 gesammelt: jedes Ereignis mit einer gedruckten Jahreszahl, das einen Gebietswechsel, eine Teilung oder ein Aussterben, einen Krieg, einen Vertrag, eine Stiftung oder Reform oder ein Unglück betrifft. Die Beschreibungen sind knappe Paraphrasen, keine Zitate; der Jahreswert ist die im Block gedruckte Jahreszahl (bei mehrjährigen Vorgängen das erste Jahr). Wo ein Jahr nicht gedruckt, sondern aus Brückners Angabe errechnet ist (Brand von Schleiz 1474 = zwei Jahre vor 1476), steht »ja« in der Spalte year_derived. Die Zuordnung zu Art und Haus ist eine redaktionelle Entscheidung. Die Stammtafeln (S. 331–403) liefern keine Ereignisse. Die Zahl je Halbjahrhundert (Spalte half_century) ist abgeleitet.",
  "The events were collected while reading the narrative on pp. 313–393 in full: every event with a printed year that concerns a change of territory, a partition or extinction, a war, a treaty, a foundation or reform, or a calamity. The descriptions are brief paraphrases, not quotations; the year is the one printed in the block (the first year for multi-year episodes). Where a year is not printed but computed from Brückner's statement (fire of Schleiz 1474 = two years before 1476), the column year_derived says “ja”. The assignment to kind and house is an editorial decision. The genealogical tables (pp. 331–403) do not supply events. The count per half-century (column half_century) is derived."),
 "findings": [
  bi(f"Der Datensatz enthält {n} Ereignisse: {cnt['acq']} Landerwerbungen, {cnt['loss']} Landverluste, {cnt['dyn']} Teilungen, Erbfälle und Erlöschen von Linien, {cnt['found']} Stiftungen, Reformen und Gesetze, {cnt['war']} Kriege und Aufstände, {cnt['treaty']} Verträge und {cnt['disaster']} Unglücksfälle. Nur {n_before_1200} liegen vor 1200.",
     f"The dataset contains {n} events: {cnt['acq']} acquisitions of land, {cnt['loss']} losses of land, {cnt['dyn']} partitions, successions and extinctions of lines, {cnt['found']} foundations, reforms and laws, {cnt['war']} wars and uprisings, {cnt['treaty']} treaties and {cnt['disaster']} calamities. Only {n_before_1200} fall before 1200."),
  bi(f"Am dichtesten erzählt Brückner die Halbjahrhunderte {second[0][0]}–{second[0][0]+49} und {second[1][0]}–{second[1][0]+49} (je {second[0][1]} Ereignisse), danach {second[2][0]}–{second[2][0]+49} ({second[2][1]}).",
     f"Brückner narrates most densely the half-centuries {second[0][0]}–{second[0][0]+49} and {second[1][0]}–{second[1][0]+49} ({second[0][1]} events each), followed by {second[2][0]}–{second[2][0]+49} ({second[2][1]})."),
  bi(f"Das Verhältnis von Erwerb zu Verlust kehrt sich um: Vor 1350 stehen {acq_pre} Erwerbungen {loss_pre} Verlusten gegenüber, von 1350 bis 1574 {acq_mid} Erwerbungen und {loss_mid} Verluste; nach 1574 überwiegen Teilungen und Reformen statt Gebietsverlusten.",
     f"The ratio of gain to loss reverses: before 1350 {acq_pre} acquisitions face {loss_pre} losses, from 1350 to 1574 there are {acq_mid} acquisitions and {loss_mid} losses; after 1574 partitions and reforms take the place of territorial losses."),
  bi(f"Von den {n_dis} Unglücksfällen sind {len(fires)} Brände (Schleiz 1474, 1689, 1837; Gera 1686, 1780; Lobenstein 1714, 1732; Hirschberg 1750; Greiz 1802); Stiftungen, Reformen und Gesetze häufen sich um 1595–1613 ({len(found_pos)}, Heinrich Posthumus) und 1836–1867 ({len(found_19)}, Verfassungs- und Rechtsreformen).",
     f"Of the {n_dis} calamities, {len(fires)} are fires (Schleiz 1474, 1689, 1837; Gera 1686, 1780; Lobenstein 1714, 1732; Hirschberg 1750; Greiz 1802); foundations, reforms and laws cluster around 1595–1613 ({len(found_pos)}, Heinrich Posthumus) and 1836–1867 ({len(found_19)}, constitutional and legal reforms)."),
 ],
 "caveats": [
  bi("Die Auswahl folgt Brückners Erzählung: Die Zahlen sagen etwas über seine Gewichtung, nicht über die tatsächliche Häufigkeit von Ereignissen. Die Linien Weida, Gera und Plauen sind in der Erzählung ausführlicher als das Haus Reuß im 17. und 18. Jahrhundert.",
     "The selection follows Brückner's narrative: the numbers say something about his emphasis, not about the true frequency of events. The lines of Weida, Gera and Plauen are treated at greater length than the house of Reuss in the 17th and 18th centuries."),
  bi("Manche Vorgänge erscheinen doppelt, weil sie zwei Häuser betreffen (z. B. 1319 Verkauf durch Weida und Kauf durch Gera). Die Zuordnung zu einer Art ist nicht immer eindeutig (Vergleiche, Lehnsaufträge, Prozesse).",
     "Some transactions appear twice because they affect two houses (e.g. 1319 sale by Weida and purchase by Gera). The assignment to a kind is not always clear-cut (settlements, feudal surrenders, lawsuits)."),
  bi("Brückner nennt Jahre oft nur ungefähr (»um«, »ca.«) oder als Spanne; hier steht die gedruckte Jahreszahl. Das Brandjahr 1474 ist aus der Angabe »zwei Jahre vor 1476« errechnet.",
     "Brückner often gives years only approximately (“um”, “ca.”) or as a span; the printed year is used here. The year of the fire, 1474, is computed from the statement “two years before 1476”."),
 ],
 "datasets": [
  {"name": "events", "title": bi("Datierte Ereignisse der Kapitel-V-Erzählung", "Dated events of the narrative of chapter V"),
   "columns": [
    {"name": "ord", "label": bi("Nr.", "No."), "type": "integer", "unit": None, "derived": True},
    {"name": "year", "label": bi("Jahr", "Year"), "type": "integer", "unit": None},
    {"name": "half_century", "label": bi("Halbjahrhundert ab", "Half-century from"), "type": "integer", "unit": None, "derived": True},
    {"name": "half_label", "label": bi("Halbjahrhundert", "Half-century"), "type": "string", "unit": None, "derived": True},
    {"name": "kind", "label": bi("Art (Code)", "Kind (code)"), "type": "string", "unit": None, "derived": True},
    {"name": "kind_de", "label": bi("Art", "Kind"), "type": "string", "unit": None, "derived": True},
    {"name": "kind_en", "label": bi("Art (englisch)", "Kind (English)"), "type": "string", "unit": None, "derived": True},
    {"name": "kind_order", "label": bi("Reihenfolge der Art", "Order of kind"), "type": "integer", "unit": None, "derived": True},
    {"name": "house", "label": bi("Haus (Code)", "House (code)"), "type": "string", "unit": None, "derived": True},
    {"name": "house_de", "label": bi("Haus", "House"), "type": "string", "unit": None, "derived": True},
    {"name": "house_en", "label": bi("Haus (englisch)", "House (English)"), "type": "string", "unit": None, "derived": True},
    {"name": "house_order", "label": bi("Reihenfolge des Hauses", "Order of house"), "type": "integer", "unit": None, "derived": True},
    {"name": "text_de", "label": bi("Ereignis (deutsch)", "Event (German)"), "type": "string", "unit": None, "derived": True},
    {"name": "text_en", "label": bi("Ereignis (englisch)", "Event (English)"), "type": "string", "unit": None, "derived": True},
    {"name": "page", "label": bi("Seite", "Page"), "type": "string", "unit": None},
    {"name": "block", "label": bi("Block", "Block"), "type": "string", "unit": None},
    {"name": "year_derived", "label": bi("Jahr errechnet (nicht gedruckt)", "Year computed (not printed)"), "type": "string", "unit": None},
   ], "rows": rows, "source_refs": REFS},
 ],
 "charts": [
  {"id": "c1", "dataset": "events",
   "title": bi("Ereignisse je Halbjahrhundert nach Art", "Events per half-century by kind"),
   "caption": bi("Zahl der datierten Ereignisse in 50-Jahres-Abschnitten, gestapelt nach Art. Das Maximum liegt im 14. Jahrhundert, in dem Erwerb, Verlust und Verträge der Voigte zusammenfallen.",
                 "Number of dated events in 50-year periods, stacked by kind. The maximum lies in the 14th century, where acquisitions, losses and treaties of the Voigts coincide."),
   "vegalite": {"height": 320,
    "mark": "bar",
    "encoding": {
     "x": {"field": "year", "type": "quantitative", "bin": {"step": 50, "extent": [500, 1900]}, "title": bi("Jahr (50-Jahres-Abschnitte)", "Year (50-year periods)"), "axis": {"format": "d", "tickCount": 14}},
     "y": {"aggregate": "count", "type": "quantitative", "title": bi("Zahl der Ereignisse", "Number of events")},
     "color": KCOL,
     "order": {"field": "kind_order", "type": "quantitative"},
     "tooltip": [{"field": "year", "bin": {"step": 50, "extent": [500, 1900]}, "title": bi("Jahre", "Years")},
                 {"field": bi("kind_de", "kind_en"), "title": bi("Art", "Kind")},
                 {"aggregate": "count", "type": "quantitative", "title": bi("Ereignisse", "Events")}]}}},
  {"id": "c2", "dataset": "events",
   "title": bi("Ereignisse nach Haus und Zeit", "Events by house and time"),
   "caption": bi("Jeder Punkt ein Ereignis; die Zeilen sind die handelnden Häuser, innerhalb einer Zeile je Art eine eigene Spur (Farbe wie oben). Bei Berührung erscheint die Beschreibung mit Seite und Block.",
                 "Each dot is an event; rows are the houses involved, and within a row each kind has its own track (colours as above). The description with page and block appears on hover."),
   "vegalite": {"height": 420,
    "mark": {"type": "point", "filled": True, "size": 34},
    "encoding": {
     "x": {"field": "year", "type": "quantitative", "title": bi("Jahr", "Year"), "axis": {"format": "d", "tickCount": 12}, "scale": {"domain": [500, 1880]}},
     "y": {"field": HOUSEFIELD, "type": "ordinal", "sort": {"field": "house_order", "op": "min"}, "title": None},
     "yOffset": {"field": bi("kind_de", "kind_en"), "type": "nominal", "sort": {"field": "kind_order", "op": "min"}},
     "color": KCOL,
     "tooltip": [{"field": "year", "title": bi("Jahr", "Year")},
                 {"field": bi("kind_de", "kind_en"), "title": bi("Art", "Kind")},
                 {"field": HOUSEFIELD, "title": bi("Haus", "House")},
                 {"field": bi("text_de", "text_en"), "title": bi("Ereignis", "Event")},
                 {"field": "page", "title": bi("Seite", "Page")},
                 {"field": "block", "title": bi("Block", "Block")}]}}},
  {"id": "c3", "dataset": "events",
   "title": bi("Welche Art von Ereignis betrifft welches Haus?", "Which kind of event concerns which house?"),
   "caption": bi("Zahl der Ereignisse je Haus, gestapelt nach Art. Die Voigtlinien Weida, Gera und Plauen tragen den Landerwerb und -verlust, das Haus Reuß die Teilungen, Stiftungen und Reformen.",
                 "Number of events per house, stacked by kind. The Voigt lines of Weida, Gera and Plauen carry acquisition and loss, the house of Reuss the partitions, foundations and reforms."),
   "vegalite": {"height": 300,
    "mark": "bar",
    "encoding": {
     "y": {"field": HOUSEFIELD, "type": "ordinal", "sort": {"field": "house_order", "op": "min"}, "title": None},
     "x": {"aggregate": "count", "type": "quantitative", "title": bi("Zahl der Ereignisse", "Number of events")},
     "color": dict(KCOL, legend={"columns": 4}),
     "order": {"field": "kind_order", "type": "quantitative"},
     "tooltip": [{"field": HOUSEFIELD, "title": bi("Haus", "House")}, {"field": bi("kind_de", "kind_en"), "title": bi("Art", "Kind")},
                 {"aggregate": "count", "type": "quantitative", "title": bi("Ereignisse", "Events")}]}}},
 ],
 "keywords": {"de": ["Chronik", "Ereignisse", "Geschichte", "Voigte", "Reuß", "Brand", "Krieg", "Vertrag", "Landerwerb", "Landverlust", "Reformation", "Hussitenkrieg", "Dreißigjähriger Krieg", "Revolution 1848"],
              "en": ["chronology", "events", "history", "Voigts", "Reuss", "fire", "war", "treaty", "acquisition", "loss of land", "Reformation", "Hussite wars", "Thirty Years' War", "revolution of 1848"]},
 "related": ["geschichte-landerwerb-landverlust-1248-1572", "geschichte-landesteilungen-linien-1240-1870"],
 "generated_by": "Claude Sonnet 5.5 (subagent A12)",
 "date": "2026-10-01",
}

if __name__ == "__main__":
    write_analysis(a)
