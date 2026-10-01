# -*- coding: utf-8 -*-
import json, re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from search_pages_a import A
from search_pages_b import B
ROOT = r"C:\Users\totom\Projects\reuss-edition"
P = {}
P.update(A)
P.update(B)
labels = [str(i) for i in range(633, 706)]
missing = [l for l in labels if l not in P]
extra = [k for k in P if k not in labels]
print("missing", missing, "extra", extra)


def page_text(p):
    return open(os.path.join(ROOT, "data", "text", "pages", f"{p}.txt"), encoding="utf-8").read()


TXT = {l: page_text(l) for l in labels}


def pages_for(rx):
    return [l for l in labels if re.search(rx, TXT[l])]


G = []


def g(term, kind, de, en, rx, variants=None, pages=None):
    pg = pages if pages is not None else pages_for(rx)
    if not pg:
        print("NO PAGES for", term, rx)
        return
    o = {"term": term}
    if variants:
        o["variants"] = variants
    o.update({"kind": kind, "de": de, "en": en, "pages": pg})
    G.append(o)


# ---- units
g("Morgen", "unit",
  "Flächenmaß; 1 preuß. Morgen = 180 Quadratruthen = 0,255322 ha (Brückner, S. 832). In den Ortsartikeln sind die Fluren in Morgen angegeben.",
  "Unit of area; 1 Prussian Morgen = 180 square rods = 0.255322 ha (Brückner, p. 832). The municipal areas in the place articles are given in Morgen.",
  r"Morgen", ["Mrg."])
g("Quadratruthe", "unit",
  "Flächenmaß; 1 preuß. Quadratruthe = 14,184579 m², 180 Quadratruthen = 1 Morgen (S. 832); in der Flurtabelle von Hohenleuben als □-Ruthen.",
  "Unit of area; 1 Prussian square rod = 14.184579 m², 180 square rods = 1 Morgen (p. 832); shown as □-Ruthen in the Hohenleuben land-use table.",
  r"□-Ruthen", ["□-Ruthe", "Ruthen"])
g("Fuß", "unit",
  "Längenmaß; 1 preuß. Fuß = 0,313853 m (S. 831). Höhenangaben der Orte als Fuß über dem Meere.",
  "Unit of length; 1 Prussian foot = 0.313853 m (p. 831). Elevations of the places are given as feet above sea level.",
  r"\d Fuß")
g("Elle", "unit",
  "Längenmaß; in Schleiz, Tanna und Hohenleuben 1 Elle = 0,565311 m, in Saalburg 0,606531 m (S. 831).",
  "Unit of length; in Schleiz, Tanna and Hohenleuben 1 ell = 0.565311 m, in Saalburg 0.606531 m (p. 831).",
  r"\d Ellen?\b|\bEllen\b")
g("Klafter", "unit",
  "Holzmaß; im Landestheil Schleiz z. B. 6 1/4 Fuß weit, 6 1/4 Fuß hoch, 3 1/2 Fuß Scheitlänge = 3,0874 m³ (S. 832).",
  "Unit of firewood volume; in the Landestheil Schleiz e.g. 6 1/4 ft wide, 6 1/4 ft high, 3 1/2 ft log length = 3.0874 m³ (p. 832).",
  r"Klaftern?")
g("Scheffel", "unit",
  "Getreidemaß; in Schleiz und Tanna 1 Scheffel = 4 Viertel = 224 Kannen = 1,4237 hl (S. 832). Im Text für Decem, Pfarrbesoldung und Aussaat.",
  "Unit of grain volume; in Schleiz and Tanna 1 Scheffel = 4 Viertel = 224 Kannen = 1.4237 hl (p. 832). Used in the text for tithes, pastors' pay and seed quantities.",
  r"Scheffel")
g("Fuder", "unit",
  "Ladungsmaß (Fuhre) für Heu, Stroh und Erbsen; Brückner gibt keine Umrechnung an.",
  "Load measure (cartload) for hay, straw and peas; Brückner gives no conversion.",
  r"\bFuder\b")
g("Schock", "unit",
  "Zählmaß (60 Stück); alte Schock auch als Geldsumme in Klosterverzeichnissen des 16. Jahrhunderts.",
  "Counting unit (60 items); old Schock is also used as a sum of money in 16th-century convent inventories.",
  r"\bSchock\b")
g("Thaler", "currency",
  "Rechnungsmünze (Thlr.) der Gemeinde- und Pachtangaben des Textes; eine Umrechnungstabelle gibt Brückner hier nicht.",
  "Money of account (Thlr.) used for the municipal finances and rents in the text; Brückner gives no conversion table here.",
  r"Thlr", ["Thlr."])
g("Mark", "currency",
  "Ältere Rechnungseinheit (Mk.) für Kauf-, Taxe- und Lösesummen früherer Jahrhunderte (z. B. Rittergüter 1503 bis 1703); ihr Wert wird nicht erklärt.",
  "Older unit of account (Mk.) for purchase, assessment and ransom sums in earlier centuries (e.g. manors 1503 to 1703); its value is not explained.",
  r"\bMk\.", ["Mk."])
g("Gulden", "currency",
  "Rechnungs- und Münzeinheit des 15. bis 17. Jahrhunderts in Kauf- und Zinsangaben; Wert nicht erklärt.",
  "Unit of account and coin of the 15th to 17th centuries in purchase and rent entries; value not explained.",
  r"Gulden|Gülden")
g("Aßo", "currency",
  "Geldsumme in Kosten- und Zinsangaben (z. B. Schulbau Schilbach, Kirchenbau Zollgrün); Brückner erklärt die Einheit nicht.",
  "Sum of money in cost and rent entries (e.g. school building at Schilbach, church work at Zollgrün); Brückner does not explain the unit.",
  r"Aßo")
# ---- church terms
g("Decem", "term",
  "Zehnt: jährliche Abgabe (meist Getreide) der Bauern an die Pfarrei oder ein Stift; die Pfarreinkünfte werden oft nach Decem verzeichnet.",
  "Tithe: annual levy (mostly grain) owed by farmers to the parish or a foundation; parish incomes are often listed by tithes.",
  r"Decem", ["Zehnt"])
g("Collatur", "term",
  "Recht zur Besetzung einer Pfarr- oder Lehrerstelle (Patronat); bei Hohenleuben zeitweise zwischen Landesherren, Kloster Cronswitz und Gutsbesitzern wechselnd.",
  "Right of appointment to a parish or teaching post (patronage); at Hohenleuben it passed between territorial lords, Cronswitz convent and manor owners.",
  r"Collatur|Collator|Patronat", ["Patronat", "Besetzungsrecht"])
g("Filial", "term",
  "Kirche oder Ort ohne eigenen Pfarrer, der von einer Mutterkirche mitversorgt wird.",
  "Church or village without its own pastor, served by a mother church.",
  r"Filial", ["Filiale"])
g("Parochie", "term",
  "Pfarrbezirk; Parochialverband oder -nexus bezeichnet die Zusammengehörigkeit der eingepfarrten Orte.",
  "Parish district; the parochial union or nexus denotes the link between the villages attached to a parish.",
  r"Parochie|Parochial", ["Parochialverband", "Parochialnexus"])
g("Kirchenvisitation", "term",
  "Kirchliche Bestandsaufnahme durch landesherrliche Kommissare, vor allem 1533/34 bei der Einführung der Reformation; Quelle für Pfarrer, Einkünfte und Besitz.",
  "Church visitation: survey by commissioners of the territorial lord, above all in 1533/34 when the Reformation was introduced; a source for pastors, incomes and holdings.",
  r"Kirchenvisitat|Visitat")
g("Ephorie", "institution",
  "Aufsichtsbezirk eines Superintendenten (Ephorus); Hohenleuben gehörte bis 1647 zur Ephorie Gera, danach Schleiz.",
  "Supervisory district of a superintendent (ephor); Hohenleuben belonged to the Ephorie of Gera until 1647 and then to Schleiz.",
  r"Ephorie|Ephoral")
g("Superintendent", "office",
  "Leitender Geistlicher einer Ephorie; in Saalburg zeitweise als Inspector oder Superintendent (1653) bezeichnet.",
  "Senior clergyman of an ephorie; at Saalburg styled inspector and, from 1653, superintendent.",
  r"Superintendent|Inspector", ["Inspector"])
g("Archidiaconus", "office",
  "Zweiter Geistlicher an einer Stadtkirche (nach dem Oberpfarrer); in Saalburg zugleich Pfarrer für Kulm und Gräfenwarth.",
  "Second clergyman at a town church (after the chief pastor); at Saalburg also pastor of Kulm and Gräfenwarth.",
  r"Archidiaconus|Archidiaconat")
g("Diaconus", "office",
  "Hilfsgeistlicher neben dem Pfarrer; in Tanna zugleich Pfarrer der Filiale Schilbach und Zollgrün.",
  "Assistant clergyman beside the pastor; at Tanna also pastor of the filials Schilbach and Zollgrün.",
  r"Diaconus|Diaconat", ["Diaconat", "Caplan"])
g("Frühmesser", "office",
  "Geistlicher für die Frühmesse (eigene Pfründe) an einer vorreformatorischen Kirche; in Saalburg und Unterkoskau genannt.",
  "Priest for the early mass (own benefice) at a pre-Reformation church; named at Saalburg and Unterkoskau.",
  r"Frühmess")
# ---- land / lordship
g("Pflege", "institution",
  "Mittelalterlicher Verwaltungsbezirk einer Burg (Pflege Reichenfels, Pflege Saalburg), später Amtsbezirk.",
  "Medieval administrative district of a castle (Pflege Reichenfels, Pflege Saalburg), later an official district.",
  r"\bPflege\b", pages=["634", "635", "639", "647", "651", "661", "662", "663", "665", "666", "667", "671"])
g("Paragiatherrschaft", "term",
  "Herrschaft einer nachgeborenen Linie des Fürstenhauses (Paragium); hier das Haus Reuß-Köstritz, dem Reichenfels und Hohenleuben gehören.",
  "Lordship held by a cadet line of the princely house (paragium); here the house of Reuss-Köstritz, which owned Reichenfels and Hohenleuben.",
  r"Paragiat", ["Paragium"])
g("Rittergut", "term",
  "Adliges Gut mit Gerichts- und Lehnsrechten (Erbgerichte, Lehen) über Dorfbewohner.",
  "Noble manor with jurisdiction and feudal rights over villagers.",
  r"Rittergut")
g("Kammergut", "term",
  "Landesherrliches Domänengut, das früher oft ein Rittergut war und von Pächtern bewirtschaftet wurde.",
  "Domain estate of the territorial lord, often a former manor, run by tenants.",
  r"Kammergut|Kammergüt")
g("Freigut", "term",
  "Von bäuerlichen Lasten freies Gut, oft Rest eines geteilten Ritterguts.",
  "Estate free of peasant burdens, often a remnant of a divided manor.",
  r"Freigut|Freigüt")
g("Vorwerk", "term",
  "Außen- oder Wirtschaftshof eines Guts; z. B. das dobeneckische Vorwerk in Saalburg und das Vorwerk der v. Magwitz in Gräfenwarth.",
  "Outlying or home farm of an estate; e.g. the Dobeneck farm in Saalburg and the v. Magwitz farm at Gräfenwarth.",
  r"Vorwerk")
g("Burggut", "term",
  "Lehen, das an Burgmannen zur Bewachung einer Burg vergeben war (Saalburg, Reichenfels).",
  "Fief granted to castle guards (Burgmannen) for guarding a castle (Saalburg, Reichenfels).",
  r"Burggut|Burggüt|Burgmann", ["Burgmannen"])
g("Kemnate", "term",
  "Steinernes, heizbares Wohngebäude eines Rittersitzes; in Tanna die Mauer der v. Rußwurm.",
  "Stone, heated residence of a knightly seat; at Tanna the Mauer of the v. Rußwurm.",
  r"Kemnate")
g("Erbgerichte", "term",
  "Niedere Gerichtsbarkeit der Grund- oder Gutsherren über ihre Untertanen, im Gegensatz zu den landesherrlichen Obergerichten.",
  "Lower jurisdiction of the landlords over their tenants, as opposed to the high jurisdiction of the territorial lord.",
  r"Erbgericht|Obergericht|Niedergericht", ["Obergerichte", "Niedergerichte"])
g("Lehngeld", "term",
  "Gebühr bei Belehnung; Brückner nennt das große Lehngeld (10 Prozent) und das kleine bei Erbfällen und Verkauf (S. 668, 674).",
  "Fee on enfeoffment; Brückner mentions the great fief fee (10 percent) and the small one on inheritance and sale (pp. 668, 674).",
  r"Lehngeld")
g("Frohn", "term",
  "Dienst- und Fuhrleistungen der Bauern für ihren Grundherrn; auch als Spann- und Handfrohn.",
  "Labour and carting duties of peasants for their landlord; also draught and hand labour.",
  r"Frohn", ["Frohnden"])
g("Hutung", "term",
  "Weide- bzw. Triftland (Hut, Trift), oft Gemeindebesitz.",
  "Grazing or drove land (Hut, Trift), often communal property.",
  r"Hutung|Hut und|Triftrecht|Trift\b", ["Hut", "Trift"])
g("Landrathsamt", "institution",
  "Seit 1849 eingerichtete Verwaltungsbehörde; Orte des Amtes Saalburg kamen 1849 unter das Landrathsamt Schleiz.",
  "Administrative authority set up from 1849; the places of the Saalburg district came under the Landrathsamt Schleiz in 1849.",
  r"Landrathsamt|Landrathshämter|Landrathshamt")
g("Justizamt", "office",
  "Gerichts- und Verwaltungsamt der Rechtspflege; Hohenleuben, Saalburg (bis 1861) und Schleiz hatten Justizämter.",
  "Court and administrative office for the administration of justice; Hohenleuben, Saalburg (until 1861) and Schleiz had court offices.",
  r"Justizamt")
g("Steuerreceptur", "office",
  "Örtliche Steuereinnahmestelle; in Hohenleuben vorhanden, in Saalburg 1869 aufgehoben.",
  "Local tax collection office; present at Hohenleuben, abolished at Saalburg in 1869.",
  r"Steuerreceptur")
g("Amtsverwalter", "office",
  "Verwalter des Amtes Saalburg; nach Brückners Fußnote zugleich Stadt- und Landrichter, Schösser, Steuereinnehmer und Mitinspector bei Kirchen und Schulen.",
  "Administrator of the Saalburg district; according to Brückner's footnote also town and district judge, bailiff, tax collector and co-inspector of churches and schools.",
  r"Amtsverwalter")
g("Gensd'arm", "office",
  "Landpolizist (Gendarm), in den größeren Orten stationiert.",
  "Rural policeman (gendarme), stationed in the larger villages.",
  r"Gensd'arm")
# ---- social classes
g("Häusler", "term",
  "Kleinstellenbesitzer mit Haus und wenig Land, gegliedert in Feld-, Klein- und Kühhäusler; die große Gruppe der Weber- und Taglöhnerfamilien.",
  "Cottager with a house and little land, subdivided into field, small and cow cottagers; the large group of weaver and day-laborer families.",
  r"Häusler", ["Feldhäusler", "Kleinhäusler"])
g("Hintersiedler", "term",
  "Einwohner ohne eigenes Gut, der bei einem Hausbesitzer wohnt; auch Hausgenosse.",
  "Inhabitant without own property who lives with a house owner; also called Hausgenosse (lodger).",
  r"Hintersiedler|Hausgenossen", ["Hausgenosse"])
g("Kühbauer", "term",
  "Kleinbauer, der sich von der Haltung weniger Kühe ernährt (zwischen Bauer und Häusler).",
  "Smallholder who lives from keeping a few cows (between farmer and cottager).",
  r"Kühbauer")
g("Grundstücksverband", "term",
  "Kategorie der Besitzstatistik neben Bauerngütern, Pertinenzen und ledigen Grundstücken; Brückner erläutert die Abgrenzung nicht.",
  "Category in the landholding statistics beside farms, appurtenances and single plots; Brückner does not explain the exact demarcation.",
  r"Grundstücksverband", ["Pertinenz", "ledige Grundstücke"])
g("Jahresbrod bauen", "term",
  "Brückners Maßstab der Selbstversorgung: Familien, die ihren Jahresbedarf an Brotgetreide selbst anbauen.",
  "Brückner's measure of self-sufficiency: families that grow their annual bread-grain needs themselves.",
  r"Jahresbrod|Brod bauen", ["sein Brod bauen"])
g("Almosener", "term",
  "Empfänger von Almosen, Ortsarme einer Gemeinde (in der Statistik der Vermögensverhältnisse neben den Kapitalisten).",
  "Recipient of alms, a municipality's poor (in the wealth statistics alongside the Kapitalisten).",
  r"Almosener|Almosenarm|Ortsarm", ["Ortsarme"])
g("Kapitalist", "term",
  "Person, die von Kapitalvermögen lebt (Rentier); in Brückners Wohlstandsangaben gezählt.",
  "Person living on capital (rentier); counted in Brückner's wealth statistics.",
  r"Kapitalist")
g("Kommunikationsweg", "term",
  "Verbindungsweg zwischen Orten, den die Gemeinde zu unterhalten hat; Vicinalweg = Nachbarschaftsweg.",
  "Connecting road between places that the municipality must maintain; Vicinalweg = neighborhood road.",
  r"Communications|Vicinalweg", ["Communicationsweg", "Vicinalweg"])
# ---- trades
g("Zeugmacher", "term",
  "Weber leichter Woll- oder Halbwollstoffe (Zeug); in Tanna zusammen mit den Webern ein Drittel der Bevölkerung.",
  "Weaver of light woollen or half-woollen cloth (Zeug); at Tanna together with the weavers a third of the population.",
  r"Zeugmacher")
g("Strumpfwirker", "term",
  "Handwerker, der Strümpfe am Wirkstuhl herstellt; im Oberland oft Arbeit für Zeulenroda.",
  "Craftsman who makes stockings on a stocking frame; in the Oberland often working for Zeulenroda.",
  r"Strumpfwirker")
g("Posamentirer", "term",
  "Hersteller von Borten, Schnüren und Quasten (Posamenten).",
  "Maker of braids, cords and tassels (passementerie).",
  r"Posamentirer")
g("Factor", "term",
  "Zwischenhändler, der den Webern Rohstoffe gibt und die Ware abnimmt (Verleger).",
  "Intermediary who supplies weavers with raw material and takes their goods (putting-out merchant).",
  r"Factoren|Factor")
g("Webermeister", "term",
  "Selbständiger Webermeister mit eigenen Stühlen und oft Gesellen; Hauptgewerbe vieler Dörfer des Oberlandes.",
  "Independent master weaver with his own looms and often journeymen; the main trade in many villages of the Oberland.",
  r"Webermeister")
g("Rettungshaus", "institution",
  "Anstalt zur Erziehung verwahrloster Kinder; in Hohenleuben 1855 durch ein Legat der Fürstin Chlotilde gegründet.",
  "Institution for the upbringing of neglected children; at Hohenleuben founded in 1855 from a legacy of Princess Chlotilde.",
  r"Rettungshaus")
g("Reihenschule", "term",
  "Schule ohne Schulhaus, in der der Lehrer reihum in den Häusern unterrichtet; auch Wanderschule.",
  "School without a school building in which the teacher teaches in turn in private houses; also itinerant school.",
  r"Reihenschule|Reiheschule|Reiheshule|Wanderschule", ["Wanderschule"])
g("Reihenschank", "term",
  "Reihum ausgeübtes Schankrecht der Berechtigten (z. B. der Vollbürger).",
  "Right to sell drink exercised in rotation by those entitled (e.g. full citizens).",
  r"Reihenschank|Reihenschenk")
g("Schrotbau", "term",
  "Blockbauweise aus waagerecht aufeinandergelegten Balken; neben Fachwerk (Fachbau) bei alten Dorfhäusern.",
  "Log construction of horizontally stacked timbers; beside half-timbering in old village houses.",
  r"Schrotbau|Schrothütten|Schrot-", ["Schrothütte"])
g("Zainhammer", "term",
  "Hammerwerk, in dem Schmiedeeisen zu Stäben (Zainen) ausgereckt wird (so beim Werk Christianenthal erklärt); Stahlhammer: Frischeisen aus Roheisen (S. 677).",
  "Hammer works where wrought iron is drawn into bars (explained for Christianenthal); steel hammer: fresh iron made from pig iron (p. 677).",
  r"Zainhammer|Stahlhammer|Eisenhammer", ["Stahlhammer", "Eisenhammer"])
g("Gewerkschaft", "institution",
  "Gesellschaft von Anteilseignern (hier sieben Personen 1693) zum Betrieb eines Berg- oder Hüttenwerks.",
  "Partnership of shareholders (here seven persons in 1693) running a mine or ironworks.",
  r"Gewerkschaft")
g("Kirchweih", "term",
  "Jährliches Fest zur Weihe der Dorfkirche (Kirmes), z. B. am Montag nach Martin Bischof (Gräfenwarth, Kulm) oder nach Gallus (Künsdorf).",
  "Annual feast of the dedication of the village church (kermis), e.g. on the Monday after St Martin (Gräfenwarth, Kulm) or after St Gall (Künsdorf).",
  r"Kirchweih|Kirmes", ["Kirmes"])
g("Stättegeld", "term",
  "Standgebühr der Händler auf Jahrmärkten; Fürst Heinrich LXII. wies 2/3 der Einnahme der Kirche Langenwolschendorf zu.",
  "Stall fee paid by traders at annual fairs; Prince Heinrich LXII. assigned two thirds of it to the church at Langenwolschendorf.",
  r"Stättegeld")
g("Brandschatzung", "term",
  "Erpressung von Geld oder Lieferungen unter Androhung von Brandstiftung (Bayern in Künsdorf, 1806).",
  "Extortion of money or supplies under threat of arson (Bavarians at Künsdorf, 1806).",
  r"[Bb]randschatz")
g("Mutz", "dialect",
  "Mundartwort für Quark, Käse; die Mutzgasse in Hohenleuben heißt so nach den aus weimarischen Orten eingeführten Waren (S. 634).",
  "Dialect word for curd cheese; the Mutzgasse in Hohenleuben is named after the goods imported from Weimar-ruled villages (p. 634).",
  r"Mutz", pages=["634"])
g("Leichenfiscus", "institution",
  "Begräbniskasse; in Tanna mit 400 Mitgliedern eingerichtet.",
  "Burial fund; at Tanna set up with 400 members.",
  r"Leichenfiscus")
g("Deutscher Orden", "institution",
  "Ritterorden; das deutsche Haus in Schleiz und Plauen war Patron vieler Kirchen (Seubtendorf, Tanna, Mielesdorf) und Lehnsherr.",
  "Knightly order; the German house at Schleiz and Plauen was patron of many churches (Seubtendorf, Tanna, Mielesdorf) and a feudal lord.",
  r"deutsche[nrs]? Orden|deutsche[nrs]? Haus|Deutsche[nrs]? Orden|Ordenshaus|deutschen Ritterorden", ["deutsches Haus"])
g("Voigt", "office",
  "Ursprünglich Reichsvogt; im Text Titel der Landesherren (Voigte von Gera, Reichsvoigt Heinrich zu Gera) bis zum Aussterben der altgeraischen Dynastie 1550.",
  "Originally an imperial advocate; in the text the title of the territorial lords (Voigts of Gera, Imperial Voigt Heinrich of Gera) until the old Gera dynasty died out in 1550.",
  r"Voigt", ["Vogt", "Reichsvoigt"])
g("Ablassbrief", "term",
  "Urkunde über einen Ablass, die einer Kirche oder Kapelle verliehen wurde (Aegidienkapelle Saalburg 1320, 1479).",
  "Charter granting an indulgence to a church or chapel (Aegidien chapel at Saalburg 1320, 1479).",
  r"Ablaß|Ablass|Indulgenz", ["Indulgenzbrief"])
g("Luftziegelei", "term",
  "Ziegelei für an der Luft getrocknete (ungebrannte) Ziegel, so die Deutung des Wortes (Stelzen).",
  "Brickworks for air-dried (unfired) bricks, as the word suggests (Stelzen).",
  r"Luftziegelei")

pages = []
for l in labels:
    de, en, kd, ke, sj = P[l]
    pages.append({"page": l, "summary_de": de, "summary_en": en, "keywords_de": kd, "keywords_en": ke, "subjects": sj})
out = {"package": "G4", "pages": pages, "glossary": G}
dst = os.path.join(ROOT, "data", "search", "pages", "G4.json")
os.makedirs(os.path.dirname(dst), exist_ok=True)
json.dump(out, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(pages), "pages;", len(G), "glossary terms ->", dst)
