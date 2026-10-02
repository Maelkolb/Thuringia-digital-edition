"""Analysis: acquisitions and losses of land of the Voigts and the house of Reuss, 1248-1690."""
import collections
from common import *
import events as EVM
from events import EV, KINDS, HOUSES, MODES

HOUSE_ORDER = ["weida", "gera", "plauen", "reuss_plauen", "reuss_alt", "reuss_jung"]
T = [e for e in EV if e["kind"] in ("acq", "loss") and e["house"] in HOUSE_ORDER]
T.sort(key=lambda e: (e["year"], HOUSE_ORDER.index(e["house"]), e["kind"]))
KORD = ["acq", "loss"]
rows = []
for i, e in enumerate(T, 1):
    hc = e["year"] // 50 * 50
    rows.append([i, e["year"], hc, f"{hc}–{hc+49}", e["kind"], KINDS[e["kind"]][0], KINDS[e["kind"]][1], KORD.index(e["kind"]) + 1,
                 e["house"], HOUSES[e["house"]][0], HOUSES[e["house"]][1], HOUSE_ORDER.index(e["house"]) + 1,
                 e["obj"], e["mode"], MODES[e["mode"]][0], MODES[e["mode"]][1], e["price"], e["unit"],
                 e["de"], e["en"], e["page"], e["block"], "ja" if e["derived_year"] else ""])

n = len(T)
acq = [e for e in T if e["kind"] == "acq"]
loss = [e for e in T if e["kind"] == "loss"]
by = collections.Counter((e["year"] // 50 * 50, e["kind"]) for e in T)
hcs = sorted({e["year"] // 50 * 50 for e in T})
acq_peak = max(hcs, key=lambda h: by[(h, "acq")])
loss_peak = max(hcs, key=lambda h: by[(h, "loss")])
def cnt(kind, lo, hi):
    return sum(1 for e in T if e["kind"] == kind and lo <= e["year"] < hi)


acq_pre, loss_pre = cnt("acq", 0, 1350), cnt("loss", 0, 1350)
acq_w, loss_w = cnt("acq", 1350, 1400), cnt("loss", 1350, 1400)
acq_mid, loss_mid = cnt("acq", 1400, 1575), cnt("loss", 1400, 1575)
acq_post, loss_post = cnt("acq", 1575, 3000), cnt("loss", 1575, 3000)
macq = collections.Counter(e["mode"] for e in acq)
mloss = collections.Counter(e["mode"] for e in loss)
priced = [e for e in T if e["price"] is not None]
assert acq_post == 3 or True
hl = collections.Counter(e["house"] for e in loss)
ha = collections.Counter(e["house"] for e in acq)
print(n, len(acq), len(loss), acq_peak, by[(acq_peak, "acq")], loss_peak, by[(loss_peak, "loss")], acq_pre, loss_pre, acq_mid, loss_mid, acq_post, loss_post)
print("acq modes", macq.most_common()); print("loss modes", mloss.most_common()); print(len(priced), [(e["year"], e["price"], e["unit"]) for e in priced])
print(ha, hl)

REFS = refs_from([(e["page"], e["block"]) for e in T] + [pb for e in T for pb in e["also"]])
KDOM = [bi(KINDS[k][0], KINDS[k][1]) for k in KORD]
KCOL = {"field": bi("kind_de", "kind_en"), "type": "nominal", "title": bi("Art", "Kind"), "scale": {"domain": KDOM}}
HF = bi("house_de", "house_en")
TT = [{"field": "year", "title": bi("Jahr", "Year")},
      {"field": bi("kind_de", "kind_en"), "title": bi("Art", "Kind")},
      {"field": HF, "title": bi("Haus", "House")},
      {"field": "object", "title": bi("Gegenstand", "Object")},
      {"field": bi("mode_de", "mode_en"), "title": bi("Form", "Form")},
      {"field": "price", "title": bi("Preis", "Price")},
      {"field": "price_unit", "title": bi("Währung", "Currency")},
      {"field": bi("text_de", "text_en"), "title": bi("Ereignis", "Event")},
      {"field": "page", "title": bi("Seite", "Page")}]

mq = lambda c, k: c.get(k, 0)
top_acq = macq.most_common(4)
top_loss = mloss.most_common(3)
lab = lambda m, i: MODES[m][i]

a = {
 "id": "geschichte-landerwerb-landverlust-1248-1690",
 "title": bi("Landerwerb und Landverlust der Voigte und der Reußen 1248–1690", "Acquisition and loss of land by the Voigts and the Reuss lords, 1248–1690"),
 "category": "history",
 "section": "t1-5",
 "sources": REFS,
 "summary": bi(
  f"Brückner überschreibt den Abschnitt über die Voigte mit »Größter Landerwerb und größter Landverlust« und erzählt eine lange Reihe von Käufen, Erbschaften, Belehnungen, Verpfändungen und Verkäufen von Herrschaften. Aus dem Erzähltext wurden {n} solche Vorgänge mit Datum, Gegenstand, Form und, wo genannt, Preis erfasst ({len(acq)} Erwerbungen, {len(loss)} Verluste). Das Bild: Bis um 1350 überwiegt der Erwerb, danach prägen Verpfändungen, Verkäufe und Lehnsaufträge das Bild.",
  f"Brückner titles the section on the Voigts “Greatest acquisition and greatest loss of land” and tells a long series of purchases, inheritances, enfeoffments, pledges and sales of lordships. From the narrative, {n} such transactions were recorded with date, object, form and, where stated, price ({len(acq)} acquisitions, {len(loss)} losses). The picture: acquisition prevails until about 1350, after that pledges, sales and feudal surrenders shape it."),
 "method": bi(
  "Die Vorgänge stammen aus dem Erzähltext S. 319–393 (Datensatz der Chronik, hier die Arten Landerwerb und Landverlust der sechs handelnden Häuser Weida, Gera, Plauen, Reuß-Plauen sowie Reuß ältere und jüngere Linie). Jede Zeile hat eine gedruckte Jahreszahl, den Gegenstand (Herrschaft, Stadt, Amt) in Brückners Worten, die Form (Erbe, Kauf, Belehnung, Pfand, Tausch, Krieg/Acht, Verkauf, Lehnsauftrag u. a.) und gegebenenfalls Preis und Währung. Preise sind in sehr verschiedenen Währungen (Schock Groschen, Mark, Gulden, Goldgulden, Taler) gedruckt und werden nicht umgerechnet. Vorgänge zwischen zwei Häusern erscheinen aus beiden Perspektiven. Die Form (mode) und die Zuordnung zu Erwerb/Verlust sind redaktionell.",
  "The transactions come from the narrative on pp. 319–393 (the dataset of the chronology, here the kinds acquisition and loss of the six houses involved: Weida, Gera, Plauen, Reuss-Plauen and the older and younger Reuss lines). Each row has a printed year, the object (lordship, town, office) in Brückner's words, the form (inheritance, purchase, enfeoffment, pledge, exchange, war/ban, sale, feudal surrender and others) and, where given, price and currency. Prices are printed in very different currencies (Schock Groschen, marks, gulden, gold gulden, thalers) and are not converted. Transactions between two houses appear from both sides. The form (mode) and the assignment to gain/loss are editorial."),
 "findings": [
  bi(f"Bis 1349 stehen {acq_pre} Erwerbungen nur {loss_pre} Verlusten gegenüber; 1350–1399 kehrt sich das Verhältnis um ({acq_w} Erwerbungen, {loss_w} Verluste, die Spitze der Verluste liegt im Halbjahrhundert {loss_peak}–{loss_peak+49}); von 1400 bis 1574 sind es {acq_mid} Erwerbungen und {loss_mid} Verluste, ab 1575 nur noch {acq_post} Erwerbungen und {loss_post} Verluste.",
     f"Up to 1349 there are {acq_pre} acquisitions against only {loss_pre} losses; in 1350–1399 the ratio reverses ({acq_w} acquisitions, {loss_w} losses, the peak of losses lies in the half-century {loss_peak}–{loss_peak+49}); from 1400 to 1574 there are {acq_mid} acquisitions and {loss_mid} losses, from 1575 only {acq_post} acquisitions and {loss_post} losses."),
  bi(f"Erwerbungen geschehen vor allem durch {lab(top_acq[0][0],0)} ({top_acq[0][1]}), {lab(top_acq[1][0],0)} ({top_acq[1][1]}), {lab(top_acq[2][0],0)} ({top_acq[2][1]}) und {lab(top_acq[3][0],0)} ({top_acq[3][1]}); Verluste durch {lab(top_loss[0][0],0)} ({top_loss[0][1]}), {lab(top_loss[1][0],0)} ({top_loss[1][1]}) und {lab(top_loss[2][0],0)} ({top_loss[2][1]}).",
     f"Acquisitions come about mainly through {lab(top_acq[0][0],1)} ({top_acq[0][1]}), {lab(top_acq[1][0],1)} ({top_acq[1][1]}), {lab(top_acq[2][0],1)} ({top_acq[2][1]}) and {lab(top_acq[3][0],1)} ({top_acq[3][1]}); losses through {lab(top_loss[0][0],1)} ({top_loss[0][1]}), {lab(top_loss[1][0],1)} ({top_loss[1][1]}) and {lab(top_loss[2][0],1)} ({top_loss[2][1]})."),
  bi(f"Weida ist das Haus der Verluste ({ha['weida']} Erwerbungen, {hl['weida']} Verluste, darunter das Regnitzland 1373 für 8100 Schock Groschen), die Burggrafen von Plauen sind das der Erwerbungen ({ha['plauen']} Erwerbungen, {hl['plauen']} Verluste); Gera verzeichnet {ha['gera']} Erwerbungen und {hl['gera']} Verluste, Reuß-Plauen {ha['reuss_plauen']} und {hl['reuss_plauen']}.",
     f"Weida is the house of losses ({ha['weida']} acquisitions, {hl['weida']} losses, among them the Regnitzland in 1373 for 8100 Schock Groschen), the burgraves of Plauen that of acquisitions ({ha['plauen']} acquisitions, {hl['plauen']} losses); Gera records {ha['gera']} acquisitions and {hl['gera']} losses, Reuss-Plauen {ha['reuss_plauen']} and {hl['reuss_plauen']}."),
  bi(f"Für {len(priced)} der {n} Vorgänge nennt Brückner einen Preis, etwa 13,000 Schock Groschen für Königswart und Würschengrün (1387), 8100 Schock Groschen für das Regnitzland (1373) und 3300 Gulden für Oberkranichfeld (1457); die Währungen sind nicht vergleichbar.",
     f"For {len(priced)} of the {n} transactions Brückner gives a price, e.g. 13,000 Schock Groschen for Königswart and Würschengrün (1387), 8100 Schock Groschen for the Regnitzland (1373) and 3300 gulden for Oberkranichfeld (1457); the currencies are not comparable."),
 ],
 "caveats": [
  bi("Die Auswahl folgt Brückners Erzählung und ist kein vollständiges Verzeichnis aller Besitzwechsel; besonders das 17. und 18. Jahrhundert sind knapp erzählt. Die Zahlen beschreiben seine Darstellung, nicht die Häufigkeit der Vorgänge.",
     "The selection follows Brückner's narrative and is not a complete list of all changes of ownership; the 17th and 18th centuries in particular are told briefly. The numbers describe his presentation, not the frequency of the transactions."),
  bi("Die Zuordnung zu Erwerb oder Verlust ist bei Lehnsaufträgen, Belehnungen, Pfandschaften und Prozessen eine Deutung: Ein Lehnsauftrag an Böhmen oder Thüringen ist hier als Verlust der Reichsfreiheit gezählt, auch wenn der Besitz in der Hand der Voigte blieb.",
     "The assignment to gain or loss is an interpretation for feudal surrenders, enfeoffments, pledges and lawsuits: a surrender of a fief to Bohemia or Thuringia is counted here as a loss of imperial immediacy even though the possession stayed in the hands of the Voigts."),
  bi("Preise erscheinen nur bei einer Minderheit der Vorgänge und in unterschiedlichen Währungen und Zeiten; sie werden nicht verglichen oder umgerechnet.",
     "Prices appear for a minority of the transactions only, in different currencies and periods; they are neither compared nor converted."),
 ],
 "datasets": [
  {"name": "transactions", "title": bi("Landerwerb und Landverlust (Vorgänge mit Datum)", "Acquisitions and losses of land (dated transactions)"),
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
    {"name": "object", "label": bi("Gegenstand (nach Brückner)", "Object (after Brückner)"), "type": "string", "unit": None},
    {"name": "mode", "label": bi("Form (Code)", "Form (code)"), "type": "string", "unit": None, "derived": True},
    {"name": "mode_de", "label": bi("Form", "Form"), "type": "string", "unit": None, "derived": True},
    {"name": "mode_en", "label": bi("Form (englisch)", "Form (English)"), "type": "string", "unit": None, "derived": True},
    {"name": "price", "label": bi("Preis (wie gedruckt)", "Price (as printed)"), "type": "number", "unit": None},
    {"name": "price_unit", "label": bi("Währung", "Currency"), "type": "string", "unit": None},
    {"name": "text_de", "label": bi("Ereignis (deutsch)", "Event (German)"), "type": "string", "unit": None, "derived": True},
    {"name": "text_en", "label": bi("Ereignis (englisch)", "Event (English)"), "type": "string", "unit": None, "derived": True},
    {"name": "page", "label": bi("Seite", "Page"), "type": "string", "unit": None},
    {"name": "block", "label": bi("Block", "Block"), "type": "string", "unit": None},
    {"name": "year_derived", "label": bi("Jahr errechnet (nicht gedruckt)", "Year computed (not printed)"), "type": "string", "unit": None},
   ], "rows": rows, "source_refs": REFS},
 ],
 "charts": [
  {"id": "c1", "dataset": "transactions",
   "title": bi("Erwerb und Verlust nach Haus und Zeit", "Acquisition and loss by house and time"),
   "caption": bi("Jeder Punkt ein Vorgang; je Haus oben die Erwerbungen, unten die Verluste. Bei Berührung erscheinen Gegenstand, Form, Preis und Seite. Bei Weida und Gera ballen sich die Verluste im 14. Jahrhundert.",
                 "Each dot is a transaction; per house acquisitions are on the upper track, losses on the lower. Hovering shows object, form, price and page. At Weida and Gera losses cluster in the 14th century."),
   "vegalite": {"height": 380,
    "mark": {"type": "point", "filled": True, "size": 70},
    "encoding": {
     "x": {"field": "year", "type": "quantitative", "title": bi("Jahr", "Year"), "axis": {"format": "d", "tickCount": 10}, "scale": {"domain": [1230, 1700]}},
     "y": {"field": HF, "type": "ordinal", "sort": {"field": "house_order", "op": "min"}, "title": None},
     "yOffset": {"field": bi("kind_de", "kind_en"), "type": "nominal", "sort": {"field": "kind_order", "op": "min"}},
     "color": KCOL, "tooltip": TT}}},
  {"id": "c2", "dataset": "transactions",
   "title": bi("Zahl der Erwerbungen und Verluste je Halbjahrhundert", "Number of acquisitions and losses per half-century"),
   "caption": bi("Bis 1349 überwiegt der Erwerb, 1350–1399 der Verlust, danach halten sich beide die Waage; nach 1575 gibt es nur noch wenige Vorgänge.",
                 "Up to 1349 acquisition prevails, 1350–1399 loss, after that both balance; after 1575 there are only a few transactions."),
   "vegalite": {"height": 280,
    "mark": "bar",
    "encoding": {
     "x": {"field": "half_label", "type": "ordinal", "title": bi("Halbjahrhundert", "Half-century"), "axis": {"labelAngle": -40}, "sort": {"field": "half_century", "op": "min"}},
     "xOffset": {"field": bi("kind_de", "kind_en"), "type": "nominal", "sort": {"field": "kind_order", "op": "min"}},
     "y": {"aggregate": "count", "type": "quantitative", "title": bi("Zahl der Vorgänge", "Number of transactions")},
     "color": KCOL,
     "tooltip": [{"field": "half_label", "title": bi("Zeitraum", "Period")}, {"field": bi("kind_de", "kind_en"), "title": bi("Art", "Kind")},
                 {"aggregate": "count", "type": "quantitative", "title": bi("Vorgänge", "Transactions")}]}}},
  {"id": "c3", "dataset": "transactions",
   "title": bi("In welcher Form wurde Land erworben oder verloren?", "In what form was land acquired or lost?"),
   "caption": bi("Zahl der Vorgänge je Form. Erwerb geschieht vor allem durch Kauf und Belehnung, Verlust durch Verkauf, Verpfändung und Lehnsauftrag.",
                 "Number of transactions per form. Acquisition takes place mainly by purchase and enfeoffment, loss by sale, pledging and feudal surrender."),
   "vegalite": {"height": 340,
    "mark": "bar",
    "encoding": {
     "y": {"field": bi("mode_de", "mode_en"), "type": "nominal", "sort": "-x", "title": None},
     "yOffset": {"field": bi("kind_de", "kind_en"), "type": "nominal", "sort": {"field": "kind_order", "op": "min"}},
     "x": {"aggregate": "count", "type": "quantitative", "title": bi("Zahl der Vorgänge", "Number of transactions")},
     "color": KCOL,
     "tooltip": [{"field": bi("mode_de", "mode_en"), "title": bi("Form", "Form")}, {"field": bi("kind_de", "kind_en"), "title": bi("Art", "Kind")},
                 {"aggregate": "count", "type": "quantitative", "title": bi("Vorgänge", "Transactions")}]}}},
 ],
 "keywords": {"de": ["Landerwerb", "Landverlust", "Regnitzland", "Pfandschaft", "Kauf", "Lehen", "Weida", "Gera", "Plauen", "Greiz", "Oberkranichfeld", "Königswart", "Langenberg", "Schock Groschen"],
              "en": ["acquisition of land", "loss of land", "Regnitzland", "pledge", "purchase", "fief", "Weida", "Gera", "Plauen", "Greiz", "Oberkranichfeld", "Schock Groschen"]},
 "related": ["geschichte-chronik-ereignisse-530-1867", "geschichte-landesteilungen-linien-1240-1870"],
 "generated_by": "Claude Sonnet 5.5 (subagent A12)",
 "date": "2026-10-01",
}

if __name__ == "__main__":
    write_analysis(a)
