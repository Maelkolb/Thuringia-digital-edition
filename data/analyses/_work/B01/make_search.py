"""B01: search metadata for pp. 826-840 (back matter) -> data/search/pages/B01.json"""
import json
import sys
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
from common import ROOT
from subs_classify import build as build_subs
from units_calc import build as build_units, LIN_PER_M

reg = json.loads((ROOT / "data/registers/ortsregister.json").read_text(encoding="utf-8"))
reg_n = Counter(e["register_page"] for e in reg["entries"])
reg_see = Counter(e["register_page"] for e in reg["entries"] if e.get("see"))
S = build_subs()
sub_n, sub_c = Counter(r["page"] for r in S), Counter()
for r in S:
    sub_c[r["page"]] += r["copies"]
first = {p: next(r for r in S if r["page"] == p) for p in ("835", "836", "837", "838", "839", "840")}
last = {p: [r for r in S if r["page"] == p][-1] for p in first}
U = build_units()
u = lambda unit, dist=None: [r for r in U if r["unit"] == unit and (dist is None or r["district"] == dist)]
dec = lambda x, nd=4: f"{x:.{nd}f}".replace(".", ",")
dot = lambda x, nd=4: f"{x:.{nd}f}"

pages = []


def add(page, sde, sen, kde, ken, subj):
    pages.append({"page": page, "summary_de": sde, "summary_en": sen, "keywords_de": kde, "keywords_en": ken, "subjects": subj})


# ---------------------------------------------------------------------------------- Ortsregister
add("826",
    f"Beginn des Ortsregisters (Abfang bis Fuchsmühle, {reg_n['826']} Einträge) mit der Bemerkung zu den Siglen: W. = Wüstung, a. G. = außer Gemeindeverband; Orte ohne Klammer sind Gemeinden, Orte in Klammer gehören zu der genannten Gemeinde. Verweisungen wie »Aergerniß s. Birkenhain«.",
    f"Start of the index of places (Abfang to Fuchsmühle, {reg_n['826']} entries) with the note on the sigla: W. = deserted settlement, a. G. = outside the municipal union; places without brackets are municipalities, places in brackets belong to the municipality named. Cross-references such as “Aergerniß s. Birkenhain”.",
    ["Ortsregister", "Ortsverzeichnis", "Gemeinden", "Wüstungen", "Mühlen", "Blankenstein", "Ebersdorf", "Bieblach", "Cuba"],
    ["index of places", "gazetteer", "municipalities", "deserted settlements", "mills", "Blankenstein", "Ebersdorf", "Bieblach", "Cuba"],
    ["Register", "Gemeinden", "Wüstung"])
add("827",
    f"Fortsetzung des Ortsregisters (Fundhäuser bis Lerchenhügel, {reg_n['827']} Einträge) mit Seitenzahlen des Haupttextes, u. a. Gera 428, Hirschberg 809, Hohenleuben 633, Köstritz 494, Langenwetzendorf 642; viele Mühlen, Hammerwerke und Einzelhöfe mit der Gemeinde in Klammern.",
    f"Continuation of the index of places (Fundhäuser to Lerchenhügel, {reg_n['827']} entries) with page numbers of the main text, e.g. Gera 428, Hirschberg 809, Hohenleuben 633, Köstritz 494, Langenwetzendorf 642; many mills, hammer works and single farms with the municipality in brackets.",
    ["Ortsregister", "Ortsverzeichnis", "Gera", "Hirschberg", "Hohenleuben", "Köstritz", "Langenwetzendorf", "Mühlen", "Hammerwerke", "Gemeinden"],
    ["index of places", "gazetteer", "Gera", "Hirschberg", "Hohenleuben", "Köstritz", "Langenwetzendorf", "mills", "hammer works", "municipalities"],
    ["Register", "Gemeinden"])
add("828",
    f"Fortsetzung des Ortsregisters (Lessen bis Schleiz, {reg_n['828']} Einträge), u. a. Lobenstein 713, Pirk 799, Pottiga 800, Reichenbach 527, Saalburg 661, Saaldorf 723 und 725, Schleiz 579; Mühlen, Hämmer und Wüstungen mit Verweisen auf die Gemeinde.",
    f"Continuation of the index of places (Lessen to Schleiz, {reg_n['828']} entries), e.g. Lobenstein 713, Pirk 799, Pottiga 800, Reichenbach 527, Saalburg 661, Saaldorf 723 and 725, Schleiz 579; mills, hammers and deserted settlements with references to the municipality.",
    ["Ortsregister", "Ortsverzeichnis", "Lobenstein", "Schleiz", "Saalburg", "Saaldorf", "Reichenbach", "Pirk", "Pottiga", "Wüstungen"],
    ["index of places", "gazetteer", "Lobenstein", "Schleiz", "Saalburg", "Saaldorf", "Reichenbach", "Pirk", "Pottiga", "deserted settlements"],
    ["Register", "Gemeinden", "Wüstung"])
add("829",
    f"Schluss des Ortsregisters (Schliffstein bis Zwötzen, {reg_n['829']} Einträge), u. a. Tanna 684, Triebes 650, Weißendorf 654, Wurzbach 766, Zschippach 547, Zwötzen 451; Wüstungen und Verweisungen (»s. …«).",
    f"End of the index of places (Schliffstein to Zwötzen, {reg_n['829']} entries), e.g. Tanna 684, Triebes 650, Weißendorf 654, Wurzbach 766, Zschippach 547, Zwötzen 451; deserted settlements and cross-references (“s. …”).",
    ["Ortsregister", "Ortsverzeichnis", "Tanna", "Triebes", "Wurzbach", "Zwötzen", "Weißendorf", "Wüstungen"],
    ["index of places", "gazetteer", "Tanna", "Triebes", "Wurzbach", "Zwötzen", "Weißendorf", "deserted settlements"],
    ["Register", "Wüstung", "Gemeinden"])

# ---------------------------------------------------------------------------------- Berichtigungen
add("830",
    "Zusätze und Berichtigungen zu S. 61–80: Zahlen der Gera-Tabellen zum Klima (S. 66, 67, 69), Beobachter Dr. Rob. Schmidt in Gera, Pflanzennamen (Pulicaria, Schlechtendal), Streichung und Ergänzung von Pflanzen des Ober- und Unterlandes, Einzelfichte vom Sturm 1868 gebrochen.",
    "Addenda and corrigenda to pp. 61–80: figures in the Gera climate tables (pp. 66, 67, 69), observer Dr. Rob. Schmidt in Gera, plant names (Pulicaria, Schlechtendal), deletion and addition of plants of the upland and lowland, a solitary spruce broken by a storm in 1868.",
    ["Berichtigungen", "Zusätze", "Druckfehler", "Klima", "Gera", "Tabelle", "Robert Schmidt", "Pflanzen", "Oberland", "Unterland", "Sturm 1868"],
    ["corrigenda", "addenda", "misprints", "climate", "Gera", "table", "Robert Schmidt", "plants", "upland", "lowland", "storm 1868"],
    ["Berichtigungen", "Klima", "Pflanzen"])
add("831",
    "Berichtigungen zu S. 84–277 (Vögel, Fische, Maikäfer, Zwölfnächte, Steuerwerth, Salzhandel seit 1868, Steuerreceptur) und Beginn von Brückners Umrechnungstabelle der Maße und Gewichte nach der Ministerial-Bekanntmachung vom 20. März 1869: Längenmaße (Baufuß, preußischer Fuß, Ruthe, Ellen in Gera, Schleiz, Saalburg, Lobenstein, Hirschberg).",
    "Corrigenda to pp. 84–277 (birds, fish, cockchafers, the Twelve Nights, tax value, salt trade from 1868, tax receiving office) and start of Brückner's table converting weights and measures under the ministerial notice of 20 March 1869: measures of length (Baufuß, Prussian foot, Ruthe, ells in Gera, Schleiz, Saalburg, Lobenstein, Hirschberg).",
    ["Berichtigungen", "Maße und Gewichte", "Längenmaße", "Elle", "Umrechnung", "Meter", "Vögel", "Maikäfer", "Salzhandel", "Zwölfnächte"],
    ["corrigenda", "weights and measures", "length measures", "ell", "conversion", "metre", "birds", "cockchafer", "salt trade", "Twelve Nights"],
    ["Berichtigungen", "Maße und Gewichte", "Vögel", "Insekten"])
add("832",
    "Fortsetzung der Umrechnungstabelle: Flächenmaße (preußischer Morgen), Körpermaße (Kanne, Eimer, Scheffel, Viertel, Achtel in Gera, Schleiz und Tanna, Lobenstein, Hirschberg), Pfund, Holzmaße (Klafter), Bruchsteinmaße (Ruthe, Schachtruthe) und Entfernungsmaße (Meile) mit metrischen Werten.",
    "Continuation of the conversion table: measures of area (Prussian Morgen), capacity (Kanne, Eimer, Scheffel, Viertel, Achtel in Gera, Schleiz and Tanna, Lobenstein, Hirschberg), pound, firewood (Klafter), quarry stone (Ruthe, Schachtruthe) and distance (Meile) with metric values.",
    ["Maße und Gewichte", "Umrechnung", "Kanne", "Eimer", "Scheffel", "Klafter", "Morgen", "Meile", "Pfund", "Liter", "Hektoliter"],
    ["weights and measures", "conversion", "Kanne", "Eimer", "Scheffel", "Klafter", "Morgen", "mile", "pound", "litre", "hectolitre"],
    ["Maße und Gewichte", "Holz", "Berichtigungen"])
add("833",
    "Zusätze und Berichtigungen zu S. 281–503: Gesamthaus Reuß und Oberappellationsgericht Jena, Kirchenvorstandsordnung 1866, Stiftungen Ferber (1869, 10 000 Thlr.) und Bruhm in Gera, Jahreszahlen und Todesjahre (c. 1279, 1420, † 1748), Hoheitsausgleichungsvertrag mit Sachsen-Altenburg 1868, Hospitäler in Gera, Glocken zu Caaschwitz.",
    "Addenda and corrigenda to pp. 281–503: the common house of Reuss and the court of appeal at Jena, church council ordinance of 1866, the Ferber (1869, 10,000 Thlr.) and Bruhm foundations in Gera, dates and years of death (c. 1279, 1420, † 1748), sovereignty treaty with Saxe-Altenburg 1868, hospitals in Gera, bells at Caaschwitz.",
    ["Berichtigungen", "Stiftungen", "Hoheitsvertrag", "Sachsen-Altenburg", "Ferber", "Bruhm", "Gera", "Hospitäler", "Heinrich von Weida", "Reuß"],
    ["corrigenda", "foundations", "sovereignty treaty", "Saxe-Altenburg", "Ferber", "Bruhm", "Gera", "hospitals", "Heinrich of Weida", "Reuss"],
    ["Berichtigungen", "Stiftungen", "Territorialgeschichte", "Fürstenhaus"])
add("834",
    "Letzte Berichtigungen zu S. 517–819 (Schreibungen, 40 statt 400, Zusatz zu Adam Heinrich Meisner aus Schleiz, Spinnfabrik Rosenthal bei Blankenstein, Juchhöh oder Dornbusch und die Quarkschenke); der Rest der Seite ist leer.",
    "Last corrigenda to pp. 517–819 (spellings, 40 instead of 400, addition on Adam Heinrich Meisner of Schleiz, the Rosenthal spinning mill at Blankenstein, Juchhöh or Dornbusch and the Quarkschenke); the rest of the page is blank.",
    ["Berichtigungen", "Zusätze", "Blankenstein", "Spinnfabrik", "Rosenthal", "Juchhöh", "Dornbusch", "Meisner", "Schleiz"],
    ["corrigenda", "addenda", "Blankenstein", "spinning mill", "Rosenthal", "Juchhöh", "Dornbusch", "Meisner", "Schleiz"],
    ["Berichtigungen", "Ortsname", "Textilgewerbe"])

# ---------------------------------------------------------------------------------- Subscriptionsliste
nm = lambda r: r["name"]
add("835",
    f"Titel der Subscriptionsliste (Georg Brückner, Hof- und Archivrath in Meiningen) und Beginn der Liste mit Exemplarzahl, Name, Stand und Ort ({sub_n['835']} Einträge, {sub_c['835']} Exemplare): Fürst Heinrich XIV. (12 Exemplare), Fürstin Agnes (8), Fürstin Adelheid (4), Heinrich XXII. Reuß ä. L. in Greiz, das fürstliche Ministerium und die Subskribenten Adler bis Behr.",
    f"Title of the subscription list (Georg Brückner, Hof- und Archivrath in Meiningen) and start of the list with number of copies, name, rank and place ({sub_n['835']} entries, {sub_c['835']} copies): Prince Heinrich XIV (12 copies), Princess Agnes (8), Princess Adelheid (4), Heinrich XXII of Reuss (older line) at Greiz, the princely ministry and the subscribers Adler to Behr.",
    ["Subskribenten", "Subscriptionsliste", "Fürst Heinrich XIV.", "Fürstin Agnes", "Schloss Osterstein", "Ministerium", "Gera", "Lobenstein", "Schleiz"],
    ["subscribers", "subscription list", "Prince Heinrich XIV", "Princess Agnes", "Osterstein castle", "ministry", "Gera", "Lobenstein", "Schleiz"],
    ["Subskribenten", "Fürstenhaus", "Berufe"])
add("836",
    f"Subscriptionsliste, Bergner bis Grimm ({sub_n['836']} Einträge, {sub_c['836']} Exemplare): Pastoren, Lehrer und Cantoren, Buchhandlungen (Sondershausen, Greifswald, Greiz, Dresden, Karlsruhe, Meiningen), Kaufleute in Gera, Schleiz und Greiz, Revierförster, die großherzogliche Bibliothek in Weimar und die Magdeburger Landfeuer-Societät in Altenhausen.",
    f"Subscription list, Bergner to Grimm ({sub_n['836']} entries, {sub_c['836']} copies): pastors, teachers and cantors, booksellers (Sondershausen, Greifswald, Greiz, Dresden, Karlsruhe, Meiningen), merchants in Gera, Schleiz and Greiz, foresters, the grand-ducal library at Weimar and the Magdeburg fire-insurance society at Altenhausen.",
    ["Subskribenten", "Subscriptionsliste", "Pastoren", "Lehrer", "Buchhandlungen", "Kaufleute", "Revierförster", "Bibliothek Weimar", "Gera", "Greiz"],
    ["subscribers", "subscription list", "pastors", "teachers", "booksellers", "merchants", "foresters", "Weimar library", "Gera", "Greiz"],
    ["Subskribenten", "Berufe"])
add("837",
    f"Subscriptionsliste, Grimm bis Luboldt ({sub_n['837']} Einträge, {sub_c['837']} Exemplare): Gymnasialbibliothek und Hauptsteueramt Gera, Justizämter, Kreisgerichte, Landrathsämter und Kammer, Hof- und Staatsbibliothek München, Buchhandlungen, Hofbeamte, Berg- und Forstbeamte, Kaufleute in Gera und Untermhaus.",
    f"Subscription list, Grimm to Luboldt ({sub_n['837']} entries, {sub_c['837']} copies): the Gymnasium library and main tax office in Gera, justice offices, district courts, district administrations and the princely chamber, the court and state library in Munich, booksellers, court officials, mining and forestry officials, merchants in Gera and Untermhaus.",
    ["Subskribenten", "Subscriptionsliste", "Justizämter", "Kreisgericht", "Landratsamt", "Staatsbibliothek München", "Hofbeamte", "Bergbeamte", "Gera", "Untermhaus"],
    ["subscribers", "subscription list", "justice offices", "district court", "district administration", "Munich state library", "court officials", "mining officials", "Gera", "Untermhaus"],
    ["Subskribenten", "Ämter und Behörden", "Berufe"])
add("838",
    f"Subscriptionsliste, Ludwig bis Schnicke ({sub_n['838']} Einträge, {sub_c['838']} Exemplare): Lehrer, Bürgermeister und Justizbeamte in Lobenstein, Schleiz, Gera und Hohenleuben, Pastoren, Buchhandlungen in Berlin, Rudolstadt und Leipzig, das fürstliche Rentamt Köstritz, Forstgehilfen und Gutsbesitzer.",
    f"Subscription list, Ludwig to Schnicke ({sub_n['838']} entries, {sub_c['838']} copies): teachers, mayors and judicial officials in Lobenstein, Schleiz, Gera and Hohenleuben, pastors, booksellers in Berlin, Rudolstadt and Leipzig, the princely revenue office at Köstritz, forestry assistants and landowners.",
    ["Subskribenten", "Subscriptionsliste", "Lehrer", "Bürgermeister", "Justizbeamte", "Buchhandlungen", "Rentamt Köstritz", "Lobenstein", "Schleiz", "Hohenleuben"],
    ["subscribers", "subscription list", "teachers", "mayors", "judicial officials", "booksellers", "Köstritz revenue office", "Lobenstein", "Schleiz", "Hohenleuben"],
    ["Subskribenten", "Berufe"])
add("839",
    f"Subscriptionsliste, Schönfeld'sche Buchhandlung bis Zenker ({sub_n['839']} Einträge, {sub_c['839']} Exemplare): die Buchhandlung Christian Teich in Lobenstein mit 50 Exemplaren, Stadträthe von Gera und Lobenstein, Vereine in Hohenleuben, Gera und Schleiz (altertumsforschend, landwirtschaftlich, naturwissenschaftlich), Kaufleute, Advokaten, Forstbeamte, Superintendent Stiehler.",
    f"Subscription list, Schönfeld'sche Buchhandlung to Zenker ({sub_n['839']} entries, {sub_c['839']} copies): the bookshop of Christian Teich in Lobenstein with 50 copies, town councils of Gera and Lobenstein, societies in Hohenleuben, Gera and Schleiz (antiquarian, agricultural, natural history), merchants, lawyers, forestry officials, Superintendent Stiehler.",
    ["Subskribenten", "Subscriptionsliste", "Teich", "Buchhandlung Lobenstein", "Stadtrat", "Vereine", "Altertumsforschender Verein Hohenleuben", "Kaufleute", "Advokaten", "Forstbeamte"],
    ["subscribers", "subscription list", "Teich", "Lobenstein bookshop", "town council", "societies", "antiquarian society Hohenleuben", "merchants", "lawyers", "forestry officials"],
    ["Subskribenten", "Berufe", "Sammlungen"])
add("840",
    f"Schluss der Subscriptionsliste, Zeigermann bis Zippel ({sub_n['840']} Einträge, {sub_c['840']} Exemplare; u. a. Pastor Ziegler in Göschitz mit 4 Exemplaren), darunter der Druckvermerk »Druck von Hermann Rudolph in Gera«.",
    f"End of the subscription list, Zeigermann to Zippel ({sub_n['840']} entries, {sub_c['840']} copies; among them Pastor Ziegler at Göschitz with 4 copies), followed by the imprint “Druck von Hermann Rudolph in Gera”.",
    ["Subskribenten", "Subscriptionsliste", "Ziegler", "Göschitz", "Druckvermerk", "Hermann Rudolph", "Gera"],
    ["subscribers", "subscription list", "Ziegler", "Göschitz", "imprint", "Hermann Rudolph", "Gera"],
    ["Subskribenten", "Titelei"])

# ---------------------------------------------------------------------------------- glossary
K, E = {r["district"]: r for r in u("Kanne")}, {r["district"]: r for r in u("Eimer")}
L = {r["district"]: r for r in u("Elle")}
gl = []


def g(term, kind, de, en, pages, variants=None):
    d = {"term": term, "kind": kind, "de": de, "en": en, "pages": pages}
    if variants:
        d["variants"] = variants
    gl.append(d)


g("Kanne", "unit",
  f"Hohlmaß; je nach Bezirk {dec(K['Gera']['base'])} l (Gera), {dec(K['Schleiz']['base'])} l (Schleiz, Tanna), {dec(K['Lobenstein']['base'])} l (Lobenstein), {dec(K['Hirschberg']['base'])} l (Hirschberg), jeweils ein Bruchteil des preuß. Quarts (S. 832).",
  f"Measure of capacity; depending on the district {dot(K['Gera']['base'])} l (Gera), {dot(K['Schleiz']['base'])} l (Schleiz, Tanna), {dot(K['Lobenstein']['base'])} l (Lobenstein), {dot(K['Hirschberg']['base'])} l (Hirschberg), each a fraction of the Prussian Quart (p. 832).",
  ["832"], ["K."])
g("Eimer", "unit",
  f"Hohlmaß zu 72 Kannen (Hirschberg 64): {dec(E['Gera']['base'], 2)} l (Gera), {dec(E['Schleiz']['base'], 2)} l (Schleiz, Tanna), {dec(E['Lobenstein']['base'], 2)} l (Lobenstein), {dec(E['Hirschberg']['base'], 2)} l (Hirschberg) (S. 832).",
  f"Measure of capacity of 72 Kannen (Hirschberg 64): {dot(E['Gera']['base'], 2)} l (Gera), {dot(E['Schleiz']['base'], 2)} l (Schleiz, Tanna), {dot(E['Lobenstein']['base'], 2)} l (Lobenstein), {dot(E['Hirschberg']['base'], 2)} l (Hirschberg) (p. 832).",
  ["832"])
sc, ds = u("Scheffel", "Schleiz")[0], u("dresdner Scheffel")[0]
g("Scheffel", "unit",
  f"Getreidemaß: dresdner Scheffel in Gera {dec(ds['base'], 2)} l; Scheffel in Schleiz und Tanna = 4 Viertel = 224 Kannen, gedruckt 1,4237 hl, nach der Kannenzahl {dec(sc['recomp'], 1)} l (S. 832; vermutlich Druckfehler).",
  f"Grain measure: Dresden Scheffel in Gera {dot(ds['base'], 2)} l; Scheffel in Schleiz and Tanna = 4 Viertel = 224 Kannen, printed 1.4237 hl, from the number of Kannen {dot(sc['recomp'], 1)} l (p. 832; probably a misprint).",
  ["832"])
vi, ak, ah, ag = u("Viertel Getreidemaß")[0], u("Achtel Kornmaß")[0], u("Achtel Hafermaß")[0], u("Achtel Getreidemaß")[0]
g("Viertel, Achtel", "unit",
  f"Getreidemaße nach Kannen: Viertel in Schleiz = 56 Kannen ({dec(vi['base'], 2)} l); Achtel Kornmaß in Lobenstein = 28 Kannen ({dec(ak['base'], 2)} l), Achtel Hafermaß = 34 Kannen ({dec(ah['base'], 2)} l); Achtel in Hirschberg = 24 Kannen ({dec(ag['base'], 2)} l) (S. 832).",
  f"Grain measures counted in Kannen: Viertel in Schleiz = 56 Kannen ({dot(vi['base'], 2)} l); Achtel of grain in Lobenstein = 28 Kannen ({dot(ak['base'], 2)} l), Achtel of oats = 34 Kannen ({dot(ah['base'], 2)} l); Achtel in Hirschberg = 24 Kannen ({dot(ag['base'], 2)} l) (p. 832).",
  ["832"])
g("Elle", "unit",
  f"Längenmaß mit fünf Werten: Gera {dec(L['Gera']['base'])} m, Schleiz/Tanna/Hohenleuben (leipziger Elle) {dec(L['Schleiz']['base'])} m, Saalburg {dec(L['Saalburg']['base'])} m, Lobenstein {dec(L['Lobenstein']['base'])} m, Hirschberg (alte hofer Elle) {dec(L['Hirschberg']['base'])} m (S. 831).",
  f"Measure of length with five values: Gera {dot(L['Gera']['base'])} m, Schleiz/Tanna/Hohenleuben (Leipzig ell) {dot(L['Schleiz']['base'])} m, Saalburg {dot(L['Saalburg']['base'])} m, Lobenstein {dot(L['Lobenstein']['base'])} m, Hirschberg (old Hof ell) {dot(L['Hirschberg']['base'])} m (p. 831).",
  ["831"])
g("Baufuß", "unit",
  f"Fuß des leipziger Werkmaßes = {dec(u('Baufuß')[0]['base'], 6)} m; landesweit gültig (S. 831). Der preuß. Fuß misst {dec(u('preuß. Fuß')[0]['base'], 6)} m, die preuß. Ruthe zu 12 Fuß {dec(u('preuß. Ruthe')[0]['base'], 6)} m.",
  f"Foot of the Leipzig works measure = {dot(u('Baufuß')[0]['base'], 6)} m; valid throughout the principality (p. 831). The Prussian foot measures {dot(u('preuß. Fuß')[0]['base'], 6)} m, the Prussian Ruthe of 12 feet {dot(u('preuß. Ruthe')[0]['base'], 6)} m.",
  ["831"], ["preuß. Fuß", "Ruthe"])
mo = u("preuß. Morgen")[0]
g("Morgen", "unit",
  f"Flächenmaß; 1 preuß. Morgen = 180 Quadratruthen = {dec(mo['value'], 6)} ha = {dec(mo['base'], 2)} m²; 1 preuß. Quadratruthe = {dec(u('preuß. Quadratruthe')[0]['base'], 6)} m² (S. 832).",
  f"Measure of area; 1 Prussian Morgen = 180 square Ruthen = {dot(mo['value'], 6)} ha = {dot(mo['base'], 2)} m²; 1 Prussian square Ruthe = {dot(u('preuß. Quadratruthe')[0]['base'], 6)} m² (p. 832).",
  ["832"], ["Mrg.", "Quadratruthe"])
kg_, ks_, kl_ = [r for r in u("Klafter") if r["district"] == "Gera"], [r for r in u("Klafter") if r["district"] == "Schleiz"], [r for r in u("Klafter") if r["district"] == "Lobenstein"]
g("Klafter", "unit",
  f"Holzmaß (Scheitholz), je nach Landestheil verschieden: Gera 6 × 6 Fuß mit 3 1/2 Fuß Scheitlänge = {dec(kg_[0]['base'])} m³ (leipziger Maß), Schleiz 3 1/2 Fuß Scheitlänge ab {dec(ks_[0]['base'])} m³, Lobenstein-Ebersdorf (nürnberger Maß) {dec(kl_[0]['base'])} m³ (S. 832).",
  f"Firewood measure (split logs), different in each district: Gera 6 × 6 feet with 3 1/2 feet log length = {dot(kg_[0]['base'])} m³ (Leipzig measure), Schleiz with 3 1/2 feet log length from {dot(ks_[0]['base'])} m³, Lobenstein-Ebersdorf (Nuremberg measure) {dot(kl_[0]['base'])} m³ (p. 832).",
  ["832"], ["Kubikfuß"])
rg, rs = u("Ruthe", "Gera")[0], u("Schachtruthe")[0]
g("Schachtruthe", "unit",
  f"Bruchsteinmaß: Ruthe in Gera (8 × 8 Ellen, 1 1/2 Elle hoch) = {dec(rg['base'])} m³, Schachtruthe in Schleiz (6 × 3 Ellen, 1 1/2 Elle hoch) = {dec(rs['base'])} m³; im Landestheil Lobenstein-Ebersdorf gilt die geraische Ruthe im Chausseebau, die schleizer Schachtruthe im Privatverkehr (S. 832).",
  f"Quarry-stone measure: Ruthe in Gera (8 × 8 ells, 1 1/2 ells high) = {dot(rg['base'])} m³, Schachtruthe in Schleiz (6 × 3 ells, 1 1/2 ells high) = {dot(rs['base'])} m³; in the district of Lobenstein-Ebersdorf the Gera Ruthe applies in road building, the Schleiz Schachtruthe in private trade (p. 832).",
  ["832"])
g("Pfund (Zollpfund)", "unit", "Gewichtseinheit; 1 Pfund (Zollpfund) = 0,5 kg (S. 832).", "Unit of weight; 1 Pfund (Zollpfund) = 0.5 kg (p. 832).", ["832"])
g("Meile", "unit",
  f"Entfernungsmaß; 1 preuß. Meile (2000 preuß. Ruthen) = 1,0043 künftige Meile, 1 geographische Meile = 0,9894 künftige Meile; die künftige Meile zählt 7500 m (S. 832).",
  f"Measure of distance; 1 Prussian mile (2000 Prussian Ruthen) = 1.0043 future mile, 1 geographical mile = 0.9894 future mile; the future mile is 7500 m (p. 832).",
  ["832"], ["künftige Meile"])
g("Pariser Linie", "unit",
  f"Längenmaß; 443,296 pariser Linien = 1 Meter, also 1 Linie = {dec(1000 / LIN_PER_M, 4)} mm (S. 831).",
  f"Unit of length; 443.296 Paris lines = 1 metre, i.e. 1 line = {dot(1000 / LIN_PER_M, 4)} mm (p. 831).",
  ["831"], ["par. Lin.", "par. L."])
g("Thaler", "currency",
  "Geldeinheit des Buchs (Thlr.); in den Berichtigungen für Stiftungskapitale (z. B. 10 000 Thlr. Stiftung Ferber 1869) und eine Prämie von 1829 (»1 Thlr. Current«) (S. 831, 833).",
  "Monetary unit of the book (Thlr.); in the corrigenda for foundation capital (e.g. 10,000 Thlr. Ferber foundation 1869) and a bounty of 1829 (“1 Thlr. Current”) (pp. 831, 833).",
  ["831", "833"], ["Thlr."])
g("Wüstung", "term", "Abgegangene (verlassene) Siedlung; im Ortsregister mit W. gekennzeichnet (S. 826).", "Deserted settlement; marked W. in the index of places (p. 826).", ["826", "827", "828", "829"], ["W."])
g("a. G. (außer Gemeindeverband)", "term", "Ort oder Gut außerhalb des Gemeindeverbands; im Ortsregister mit a. G. bezeichnet (S. 826).", "Place or estate outside the municipal union; marked a. G. in the index of places (p. 826).", ["826", "827", "828", "829"], ["a. G."])
g("Oberland, Unterland", "term",
  "Brückners Bezeichnung der beiden Landestheile: das Unterland (Gera, Elsterthal, tiefer gelegen) und das Oberland (Schleiz, Lobenstein-Ebersdorf, Saalthal, höher gelegen); in den Berichtigungen bei Pflanzenlisten (S. 830).",
  "Brückner's names for the two parts of the land: the Unterland (Gera, Elster valley, lower) and the Oberland (Schleiz, Lobenstein-Ebersdorf, Saale valley, higher); in the corrigenda concerning plant lists (p. 830).",
  ["830", "831"], ["Oberlande", "Unterlande"])
g("Reuß ä. L. / j. L.", "term", "Ältere bzw. jüngere Linie des Hauses Reuß; die Subscriptionsliste nennt den Fürsten Reuß ä. L. in Greiz (S. 835).", "Older or younger line of the house of Reuss; the subscription list names the prince of Reuss (older line) at Greiz (p. 835).", ["835"], ["Reuß j. L.", "Reuß ä. L."])
g("Gesamthaus Reuß", "institution", "Die gemeinsame Vertretung beider reußischer Linien; sie hat eine gemeinsame Stimme beim Oberappellationsgericht Jena, bis 1868 auch die gemeinsamen Militärangelegenheiten (S. 833).", "The joint representation of both Reuss lines; it holds a common vote at the court of appeal in Jena and, until 1868, the joint military affairs (p. 833).", ["833"], ["Gesammthaus"])
g("Subscriptionsliste", "term", "Verzeichnis der Vorbesteller des Buchs mit Zahl der bestellten Exemplare (Expl.), Stand und Wohnort (S. 835–840).", "List of advance subscribers of the book with the number of copies ordered (Expl.), rank and place of residence (pp. 835–840).", ["835", "836", "837", "838", "839", "840"], ["Expl.", "Subskription"])
g("Debitstelle", "term", "Verkaufsstelle, hier für Salz; nach dem Bundesgesetz vom 12. Oktober 1867 entfielen die früheren Debitstellen mit der Freigabe des Salzhandels 1868 (S. 831).", "Retail outlet, here for salt; under the federal law of 12 October 1867 the former outlets lapsed when the salt trade was freed in 1868 (p. 831).", ["831"], ["Debit"])
g("Zwölfen (Zwölf Nächte)", "term", "Die Nächte zwischen Weihnachten und dem Großen Neujahr (6. Januar); nach Brückners Zusatz begannen sie ursprünglich am 21. Dezember, später (urkundlich 1321) am 25. Dezember (S. 831).", "The nights between Christmas and Epiphany (6 January); according to Brückner's addition they began originally on 21 December, later (documented 1321) on 25 December (p. 831).", ["831"], ["12 Nächte", "Zwölfe"])
g("Steuerreceptur", "office", "Steuereinnahmestelle; laut Zusatz zu S. 277 aufgehoben (S. 831).", "Tax receiving office; abolished according to the addendum to p. 277 (p. 831).", ["831"])
g("Hoheitsausgleichungsvertrag", "term", "Vertrag vom 30. Mai 1868 (ratifiziert 5. August 1868) zwischen Reuß j. L. und Sachsen-Altenburg über strittige Grenzgrundstücke, u. a. in Roschitz, Bethenhausen, Hirschfeld, Dorna, Pörsdorf und Rüdersdorf (S. 833).", "Treaty of 30 May 1868 (ratified 5 August 1868) between Reuss (younger line) and Saxe-Altenburg on disputed border plots, among others in Roschitz, Bethenhausen, Hirschfeld, Dorna, Pörsdorf and Rüdersdorf (p. 833).", ["833"])
g("Kammergut", "term", "Landesherrliches Gut, das verpachtet wurde; in der Liste z. B. der Kammergutspächter in Oettersdorf (gedruckt Dettersdorf) und der Pächter auf dem Kammergut Harra (S. 836, 837).", "Estate of the sovereign, leased out; in the list e.g. the Kammergut tenant at Oettersdorf (printed Dettersdorf) and the tenant of the Kammergut at Harra (pp. 836, 837).", ["836", "837"], ["Kammergutspachter"])
g("Catechet", "office", "Religionslehrer und Gehilfe des Pfarrers an einer Stadtkirche (Katechet); in der Subscriptionsliste in Gera, Lobenstein und Hirschberg (S. 835, 836, 838).", "Religious instructor and assistant to the parish priest at a town church (Katechet); in the subscription list in Gera, Lobenstein and Hirschberg (pp. 835, 836, 838).", ["835", "836", "838"], ["Katechet"])
g("Diaconus", "office", "Zweiter Geistlicher an einer Stadtkirche (Diakonus); in der Liste in Schleiz, Tanna und Lobenstein (S. 835, 838, 839).", "Second clergyman at a town church (deacon); in the list at Schleiz, Tanna and Lobenstein (pp. 835, 838, 839).", ["835", "838", "839"], ["Diakonus"])
g("Superintendent", "office", "Leitender Geistlicher eines Kirchenkreises (Ephorie); in der Liste in Lobenstein (S. 839).", "Senior clergyman of a church district; in the list at Lobenstein (p. 839).", ["839"])
g("Kirchenrath", "office", "Titel und Amt eines Mitglieds der Kirchenbehörde; in der Liste in Gera und Schleiz (S. 836, 839).", "Title and office of a member of the church authority; in the list at Gera and Schleiz (pp. 836, 839).", ["836", "839"])
g("Cantor", "office", "Kantor: Lehrer, der zugleich den Kirchengesang und die Orgel versah (Schul- und Kirchendienst); in der Liste u. a. in Ebersdorf, Saalburg und Wurzbach (S. 836, 837).", "Cantor: teacher who also led church singing and played the organ (school and church service); in the list e.g. at Ebersdorf, Saalburg and Wurzbach (pp. 836, 837).", ["836", "837"], ["Kantor"])
g("Revierförster", "office", "Forstbeamter, der ein Forstrevier verwaltet; daneben in der Liste Oberförster, Forstmeister, Oberforstmeister und Forstgehilfen (S. 835–839).", "Forestry official in charge of a forest district; the list also names senior foresters (Oberförster), Forstmeister, Oberforstmeister and forestry assistants (pp. 835–839).", ["835", "836", "837", "838", "839"], ["Oberförster", "Forstmeister"])
g("Justizamt", "institution", "Fürstliche Behörde der Rechtspflege erster Instanz mit einem Justizamtmann an der Spitze; die Liste nennt Justizämter in Gera, Hohenleuben und Schleiz (S. 837).", "Princely authority for first-instance justice headed by a Justizamtmann; the list names justice offices at Gera, Hohenleuben and Schleiz (p. 837).", ["837", "836", "838"], ["Justizamtmann"])
g("Landrathsamt", "institution", "Verwaltungsbehörde eines Landestheils (Landrathsamtsbezirk); die Liste nennt die fürstlichen Landrathsämter in Gera und Ebersdorf (S. 837).", "Administrative authority of a district (Landrathsamtsbezirk); the list names the princely Landrathsämter at Gera and Ebersdorf (p. 837).", ["837"])
g("Rendant", "office", "Rechnungs- und Kassenführer einer Behörde oder Anstalt; in der Liste in Neuhammer und Hirschberg sowie als Steuerrendant in Lobenstein (S. 837–839).", "Accountant or cashier of an authority or institution; in the list at Neuhammer and Hirschberg and as tax cashier at Lobenstein (pp. 837–839).", ["837", "838", "839"], ["Steuerrendant"])
g("Commerzienrath", "office", "Ehrentitel für verdiente Kaufleute und Fabrikanten; in der Liste Rud. Ferber in Gera (S. 836).", "Honorary title for distinguished merchants and manufacturers; in the list Rud. Ferber at Gera (p. 836).", ["836"], ["Kommerzienrat"])
g("Steiger", "office", "Bergmann mit Aufsichtsfunktion unter Tage (Grubenaufseher); in der Liste auf dem Zechenhaus bei Lobenstein, daneben Bergmeister und Bergverwalter (S. 836, 837).", "Miner with supervisory duties underground (mine overseer); in the list at the Zechenhaus near Lobenstein, alongside Bergmeister and Bergverwalter (pp. 836, 837).", ["836", "837"], ["Bergmeister", "Bergverwalter"])
g("Aktuar", "office", "Gerichts- oder Amtsschreiber, der Protokolle führt; in der Liste in Gera (S. 839).", "Court or office clerk who keeps records; in the list at Gera (p. 839).", ["839"])
g("Assessor", "office", "Beamter im Vorbereitungsdienst der Justiz oder Verwaltung mit Stimmrecht in Kollegialbehörden; in der Liste in Gera und Schleiz (S. 838, 839).", "Official in the preparatory service of the judiciary or administration with a vote in collegiate authorities; in the list at Gera and Schleiz (pp. 838, 839).", ["838", "839"])
g("Oeconom", "office", "Landwirt oder Gutsverwalter (Ökonom); in der Liste in Rusitz (S. 835).", "Farmer or estate manager (Ökonom); in the list at Rusitz (p. 835).", ["835"], ["Ökonom"])

doc = {"package": "B01", "pages": pages, "glossary": gl}
out = ROOT / "data/search/pages/B01.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
print(out, len(pages), len(gl))
