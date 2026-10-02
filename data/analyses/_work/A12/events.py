"""Master list of dated events of chapter V (pp. 311-404), with page/block references.

kind: war | treaty | acq | loss | dyn | found | disaster
house: land | weida | gera | plauen | reuss_plauen | reuss_alt | reuss_jung | gesamt
mode (acq/loss only): see MODES
"""
from common import *

KINDS = {
    "war": ("Krieg, Aufstand", "War, uprising"),
    "treaty": ("Vertrag, Bündnis", "Treaty, alliance"),
    "acq": ("Landerwerb", "Acquisition"),
    "loss": ("Landverlust", "Loss of land"),
    "dyn": ("Teilung, Erbfolge", "Partition, succession"),
    "found": ("Stiftung, Reform", "Foundation, reform"),
    "disaster": ("Brand, Not", "Fire, hardship"),
}
HOUSES = {
    "land": ("Land (Voigtland)", "Land (Voigtland)"),
    "gesamt": ("Gesamthaus", "House as a whole"),
    "weida": ("Weida", "Weida"),
    "gera": ("Gera", "Gera"),
    "plauen": ("Plauen (Burggrafen)", "Plauen (burgraves)"),
    "reuss_plauen": ("Reuß-Plauen", "Reuss-Plauen"),
    "reuss_alt": ("Reuß ä. L.", "Reuss older line"),
    "reuss_jung": ("Reuß j. L.", "Reuss younger line"),
}
MODES = {
    "erbe": ("Erbe", "inheritance"),
    "kauf": ("Kauf", "purchase"),
    "lehen": ("Belehnung", "enfeoffment"),
    "pfand": ("Pfand", "pledge"),
    "tausch": ("Tausch", "exchange"),
    "krieg": ("Krieg, Acht", "war, ban"),
    "gabe": ("Schenkung", "grant"),
    "mitgift": ("Heiratsgut", "dowry"),
    "lehnsauftrag": ("Lehnsauftrag", "feudal surrender"),
    "verkauf": ("Verkauf", "sale"),
    "loesung": ("Rückgewinnung", "recovery"),
    "vorkauf": ("Vorkaufsrecht", "right of pre-emption"),
    "prozess": ("Prozess", "lawsuit"),
    "unbekannt": ("Art nicht genannt", "mode not stated"),
}
EV = []


def ev(year, kind, house, de, en, page, block, obj=None, mode=None, price=None, unit=None, derived_year=False, also=()):
    assert kind in KINDS and house in HOUSES, (year, kind, house)
    if kind in ("acq", "loss"):
        assert obj and mode in MODES, (year, de)
    EV.append(dict(year=year, kind=kind, house=house, de=de, en=en, page=str(page), block=block, obj=obj, mode=mode,
                   price=price, unit=unit, derived_year=derived_year, also=[(str(p), b) for p, b in also]))


# ---------------------------------------------------------------- Sorbian period and the Voigtland before the Voigte
ev(530, "war", "land", "Die Franken unterwerfen das Königreich Thüringen, zu dem das Voigtland gehört", "The Franks conquer the kingdom of Thuringia, which included the Voigtland", 313, "b4")
ev(630, "war", "land", "König Dagobert zieht gegen die Slaven und erleidet an der oberen Saale oder Eger eine Niederlage", "King Dagobert campaigns against the Slavs and is defeated on the upper Saale or Eger", 314, "b2")
ev(782, "war", "land", "Räuberischer Einfall der Sorben nach Thüringen und Sachsen", "Raid of the Sorbs into Thuringia and Saxony", 314, "b2")
ev(805, "war", "land", "Aufstand der Sorben; Karls Sohn unterwirft sie (Feldzüge 805/806)", "Sorbian uprising; Charlemagne's son subdues them (campaigns 805/806)", 314, "b2")
ev(815, "war", "land", "Die Sorben folgen der Ladung nach Paderborn nicht; im Jahr darauf erobert ein Heer Teile des Sorbenlandes an der Saale", "The Sorbs ignore the summons to Paderborn; the following year an army conquers parts of the Sorbian land on the Saale", 314, "b2")
ev(849, "dyn", "land", "Die sorbische Grenzmark (limes sorabicus) steht unter einem Herzog (Tachulf)", "The Sorbian border march (limes sorabicus) is placed under a duke (Tachulf)", 315, "b1")
ev(874, "war", "land", "Aufstand der Sorben nach Tachulfs Tod; Herzog Ratolf und der Erzbischof von Mainz unterwerfen sie", "Sorbian uprising after Tachulf's death; Duke Ratolf and the archbishop of Mainz subdue them", 315, "b1")
ev(877, "war", "land", "Erneute Niederlage der Sorben", "Another defeat of the Sorbs", 315, "b1")
ev(880, "war", "land", "Die an der Saale wohnenden treuen Sorben werden von ihren Stammesgenossen mit Brand und Plünderung heimgesucht", "The loyal Sorbs on the Saale are attacked with fire and plunder by their kinsmen", 315, "b1")
ev(892, "war", "land", "Zug Herzog Poppos gegen die hinteren Sorben endet unglücklich, Bischof Arn von Würzburg fällt", "Duke Poppo's campaign against the far Sorbs ends in disaster, Bishop Arn of Würzburg is killed", 315, "b1")
ev(908, "war", "land", "Herzog Burchard fällt im Kampf gegen die Ungarn; Thüringen mit der Ostmark geht an Heinrich über", "Duke Burchard falls fighting the Hungarians; Thuringia with the eastern march passes to Heinrich", 315, "b1")
ev(968, "found", "land", "Kaiser Otto I. errichtet das Bistum Zeitz für die Bekehrung der Sorben", "Emperor Otto I founds the bishopric of Zeitz for the conversion of the Sorbs", 321, "b3")
ev(999, "dyn", "land", "König Otto III. schenkt den Distrikt Gera dem Stift Quedlinburg", "King Otto III grants the district of Gera to the abbey of Quedlinburg", 320, "b2")
ev(1011, "dyn", "land", "König Heinrich II. gibt einen großen Teil des orla-saalfelder Gebiets an Pfalzgraf Ehrenfried", "King Heinrich II gives a large part of the Orla-Saalfeld region to Count Palatine Ehrenfried", 320, "b2")
ev(1029, "found", "land", "Das Bistum Zeitz muss wegen der Feindseligkeit der Sorben seinen Sitz nach Naumburg verlegen", "The bishopric of Zeitz has to move its seat to Naumburg because of Sorbian hostility", 322, "b1")
ev(1060, "dyn", "land", "Kaiser Heinrich IV. übergibt die Burgwarte Langenberg dem Hochstift Naumburg", "Emperor Heinrich IV gives the burgward of Langenberg to the cathedral chapter of Naumburg", 320, "b2")
# ---------------------------------------------------------------- the Voigte of Weida: origin to the division
ev(1143, "dyn", "weida", "Heinrich von Weida tritt erstmals urkundlich im Gefolge Kaiser Konrads auf", "Heinrich of Weida first appears in a charter, in the retinue of Emperor Conrad", 329, "b2")
ev(1185, "war", "land", "Die Reichsministerialen an der Elster bekämpfen und schädigen einander", "The imperial ministeriales on the Elster fight and harm each other", 329, "b2")
ev(1193, "found", "weida", "Heinrich der Reiche gründet das Prämonstratenserkloster Mildenfurt, das älteste im Voigtland", "Heinrich the Rich founds the Premonstratensian monastery Mildenfurt, the oldest in the Voigtland", 329, "b2")
ev(1209, "dyn", "weida", "Die drei Söhne Heinrichs des Reichen erscheinen erstmals gemeinsam; mit ihnen kommt der Titel Voigt (advocatus) auf", "The three sons of Heinrich the Rich first appear together; with them the title Voigt (advocatus) begins", 330, "b3")
ev(1224, "dyn", "weida", "Heinrich d. ä. von Weida ist vor 1224 in den Deutschen Orden eingetreten", "Heinrich the elder of Weida has joined the Teutonic Order by 1224", 330, "b3")
ev(1228, "war", "weida", "Der jüngste Bruder beteiligt sich am Kreuzzug Kaiser Friedrichs II.", "The youngest brother takes part in Emperor Friedrich II's crusade", 330, "b3")
ev(1237, "treaty", "weida", "Heinrich d. m. schließt mit der Äbtissin von Quedlinburg den Vertrag über die Stiftsvoigtei Gera", "Heinrich the middle brother concludes the treaty with the abbess of Quedlinburg on the abbey's advocacy of Gera", 330, "b3")
ev(1238, "found", "weida", "Heinrich d. m. tritt in den Deutschen Orden; seine Gattin stiftet das Kloster Cronswitz", "Heinrich the middle brother joins the Teutonic Order; his wife founds the convent of Cronswitz", 330, "b3")
ev(1241, "war", "plauen", "Schlacht bei Wahlstedt gegen die Mongolen (Ursprung des Namens Reuß nach Brückner)", "Battle of Wahlstedt against the Mongols (origin of the name Reuss according to Brückner)", 353, "b1")
ev(1244, "dyn", "gesamt", "Erste folgenreiche Landesteilung (zwischen 1239 und 1244): die Linien Weida, Plauen und Gera entstehen", "First momentous division of the land (between 1239 and 1244): the lines of Weida, Plauen and Gera arise", 332, "b1")
ev(1246, "war", "weida", "Heinrich d. m. zieht mit Rittern an die Weichsel (Preußenfahrt des Deutschen Ordens)", "Heinrich the middle brother leads knights to the Vistula (Prussian campaign of the Teutonic Order)", 334, "b1")
# ---------------------------------------------------------------- line Weida
ev(1248, "acq", "weida", "Nach dem Aussterben der Meraner wird Heinrich d. ä. von Weida Miterbe: das Regnitzland fällt an Weida", "After the Meran family dies out Heinrich the elder of Weida becomes co-heir: the Regnitzland falls to Weida", 334, "b1", obj="Regnitzland", mode="erbe")
ev(1254, "treaty", "gesamt", "Grimmaischer Vertrag: Schutzbündnis der Voigte von Weida, Plauen und Gera mit Markgraf Heinrich dem Erlauchten", "Treaty of Grimma: defensive alliance of the Voigts of Weida, Plauen and Gera with Margrave Heinrich the Illustrious", 334, "b2")
ev(1258, "found", "weida", "Heinrich d. ä. begabt das Kloster Laußnitz und mit seiner Gattin das Kloster Pforte", "Heinrich the elder endows the monastery of Laußnitz and, with his wife, the monastery of Pforta", 334, "b2")
ev(1260, "treaty", "weida", "Heinrich d. ä. schlichtet den Streit um die meranische Erbschaft zwischen Orlamünde und Bamberg", "Heinrich the elder settles the dispute over the Meran inheritance between Orlamünde and Bamberg", 335, "b1")
ev(1264, "found", "weida", "Heinrich d. ä. stiftet ein Hospital zu Hof", "Heinrich the elder founds a hospital in Hof", 334, "b2")
ev(1267, "found", "weida", "Heinrich d. ä. stiftet ein Kloster zu Weida", "Heinrich the elder founds a monastery in Weida", 334, "b2")
ev(1288, "treaty", "weida", "Vertrag der Voigte von Weida und Plauen beschränkt das willkürliche Entfernen bäuerlicher Pächter", "Treaty of the Voigts of Weida and Plauen limits the arbitrary removal of tenant farmers", 335, "b2")
ev(1292, "dyn", "weida", "Heinrich d. j. von Weida stirbt; sein Bruder übernimmt die Vormundschaft über dessen Kinder", "Heinrich the younger of Weida dies; his brother becomes guardian of his children", 335, "b3")
ev(1295, "acq", "weida", "Landgraf Albrecht belehnt Heinrich d. ä. und seine Söhne mit dem Reichsgut Caaschwitz", "Landgrave Albrecht enfeoffs Heinrich the elder and his sons with the imperial estate of Caaschwitz", 336, "b1", obj="Caaschwitz", mode="lehen")
ev(1307, "war", "weida", "Heinrich d. ä. kämpft in der Schlacht bei Lucka an der Seite Markgraf Friedrichs", "Heinrich the elder fights at the battle of Lucka at Margrave Friedrich's side", 336, "b1")
ev(1309, "treaty", "weida", "Markgraf Friedrich schlichtet den Streit um die Wechselbank zu Gera: sie bleibt beim Haus Weida", "Margrave Friedrich settles the dispute over the exchange bank at Gera: it stays with the house of Weida", 336, "b1")
ev(1312, "treaty", "gesamt", "Die Voigte von Weida, Gera und Plauen sagen König Johann von Böhmen Beistand gegen Landgraf Friedrich zu", "The Voigts of Weida, Gera and Plauen promise King Johann of Bohemia support against Landgrave Friedrich", 336, "b1")
ev(1318, "loss", "weida", "Burggraf Friedrich von Nürnberg belehnt Heinrich von Weida nur noch mit dem Regnitzland: es gilt als Afterlehen", "Burgrave Friedrich of Nuremberg enfeoffs Heinrich of Weida with the Regnitzland only: it is now a sub-fief", 336, "b1", obj="Regnitzland (Lehnshoheit)", mode="lehnsauftrag")
ev(1319, "loss", "weida", "Die jungen Voigte von Weida verkaufen das Vorwerk Tinz und die Münze zu Gera an Gera", "The young Voigts of Weida sell the manor of Tinz and the mint at Gera to Gera", 337, "b1", obj="Tinz und Münze zu Gera", mode="verkauf")
ev(1323, "loss", "weida", "Kaiser Ludwig überträgt die Lehnshoheit über das Regnitzland dem Burggrafen von Nürnberg", "Emperor Ludwig gives the feudal overlordship of the Regnitzland to the burgrave of Nuremberg", 321, "b1", obj="Regnitzland (Lehnshoheit)", mode="lehnsauftrag")
ev(1327, "treaty", "gesamt", "Ronneburger Bündnis: alle Voigte verpflichten sich zu gegenseitigem Schutz", "Alliance of Ronneburg: all Voigts pledge mutual protection", 365, "b1")
ev(1329, "treaty", "gesamt", "Goldene Bulle Kaiser Ludwigs für alle Zweige des Hauses: ihre Regalien werden bestätigt", "Golden Bull of Emperor Ludwig for all branches of the house: their regalia are confirmed", 366, "b1")
ev(1331, "war", "gesamt", "Die Voigte stellen dem Kaiser Hilfstruppen für den Zug in die Mark Brandenburg", "The Voigts supply the emperor with auxiliary troops for the campaign in the March of Brandenburg", 337, "b2")
ev(1337, "treaty", "gesamt", "Der Streit mit Landgraf Friedrich um das Bergwerk Hohenforst wird beigelegt", "The dispute with Landgrave Friedrich over the mine of Hohenforst is settled", 337, "b2")
ev(1351, "found", "weida", "Die Weidaer Voigte begaben das Stift Bibra mit Gütern im Eckartsbergischen", "The Voigts of Weida endow the abbey of Bibra with estates near Eckartsberga", 337, "b2")
ev(1354, "loss", "weida", "Heinrich d. ä. muss den Landgrafen geloben, ihnen mit Schloss und Stadt Weida zu dienen", "Heinrich the elder has to promise the landgraves the service of castle and town of Weida", 337, "b3", obj="Schloss und Stadt Weida (Dienstpflicht)", mode="lehnsauftrag")
ev(1356, "loss", "weida", "Weida veräußert Eprechtstein an die Nürnberger Burggrafen", "Weida sells Eprechtstein to the burgraves of Nuremberg", 338, "b1", obj="Eprechtstein", mode="verkauf")
ev(1360, "loss", "weida", "Weida verspricht den Burggrafen, Hof nicht ohne ihr Wissen zu verkaufen; Weida kommt unter Thüringen", "Weida promises the burgraves not to sell Hof without their knowledge; Weida comes under Thuringia", 338, "b1", obj="Hof, Weida (Bindung)", mode="lehnsauftrag")
ev(1362, "loss", "weida", "Weida verpfändet das halbe höfer Land an die Burggrafen", "Weida pledges half of the Hof land to the burgraves", 338, "b1", obj="halbes höfer Land", mode="pfand")
ev(1366, "dyn", "weida", "Heinrich der Ritter verkauft seinen Anteil am Regnitzland an seinen Bruder Heinrich den Rothen", "Heinrich the Knight sells his share of the Regnitzland to his brother Heinrich the Red", 338, "b2")
ev(1373, "loss", "weida", "Heinrich der Rothe verkauft das Regnitzland an Burggraf Friedrich von Nürnberg um 8100 Schock Groschen", "Heinrich the Red sells the Regnitzland to Burgrave Friedrich of Nuremberg for 8100 Schock Groschen", 338, "b2", obj="Regnitzland", mode="verkauf", price=8100, unit="Schock Groschen")
ev(1406, "loss", "weida", "Heinrich d. ä. verpfändet sein Drittel an Weida an die Wettiner (1410 verkauft er es mit Schmölln)", "Heinrich the elder pledges his third of Weida to the Wettins (in 1410 he sells it with Schmölln)", 339, "b2", obj="Drittel an Weida", mode="pfand")
ev(1410, "loss", "weida", "Heinrich d. ä. verkauft sein Drittel an Weida samt Schmölln an die Wettiner", "Heinrich the elder sells his third of Weida together with Schmölln to the Wettins", 339, "b2", obj="Drittel an Weida und Schmölln", mode="verkauf")
ev(1411, "loss", "weida", "Heinrich d. m. verkauft seinen Anteil an Weida an die Wettiner", "Heinrich the middle brother sells his share of Weida to the Wettins", 339, "b2", obj="Anteil an Weida", mode="verkauf")
ev(1427, "found", "weida", "Heinrich d. j. verleiht Berga Stadtrechte", "Heinrich the younger grants Berga town rights", 339, "b2")
ev(1447, "treaty", "weida", "Vergleich mit Markgraf Johann von Baireuth über das Regnitzland: der ältere Bruder erhält 200 Gulden", "Settlement with Margrave Johann of Bayreuth over the Regnitzland: the elder brother receives 200 Gulden", 339, "b2")
ev(1454, "loss", "weida", "Das Schloss Hauenstein wird verkauft; nur Wildenfels bleibt dem Haus Weida", "Hauenstein castle is sold; only Wildenfels remains to the house of Weida", 340, "b1", obj="Schloss Hauenstein", mode="verkauf")
ev(1535, "dyn", "weida", "Heinrich von Weida zu Wildenfels stirbt als letzter männlicher Erbe: das Haus Weida erlischt", "Heinrich of Weida at Wildenfels dies as the last male heir: the house of Weida becomes extinct", 340, "b1")
# ---------------------------------------------------------------- line Gera
ev(1302, "loss", "gera", "Heinrich d. j. von Gera verkauft Sparnberg an Ulrich Sack", "Heinrich the younger of Gera sells Sparnberg to Ulrich Sack", 342, "b1", obj="Sparnberg", mode="verkauf")
ev(1306, "acq", "gera", "Heinrich d. ä. kauft vom Hochstift Quedlinburg das Schultheißenamt zu Gera samt Zubehör um 750 Mark", "Heinrich the elder buys the office of Schultheiß at Gera with its appurtenances from the abbey of Quedlinburg for 750 marks", 342, "b1", obj="Schultheißenamt zu Gera", mode="kauf", price=750, unit="Mark")
ev(1310, "found", "gera", "Die Brüder von Gera gründen das Kloster zum heiligen Kreuz bei Saalburg", "The brothers of Gera found the monastery of the Holy Cross near Saalburg", 343, "b2")
ev(1314, "war", "gera", "Burggraf von Nürnberg und Landgraf von Thüringen ziehen gegen das Haus Gera; Burgk und Schleiz werden verwüstet", "The burgrave of Nuremberg and the landgrave of Thuringia attack the house of Gera; Burgk and Schleiz are devastated", 365, "b1")
ev(1317, "treaty", "gera", "Friede zu Weißenfels: Landgraf Friedrich gibt seine Ansprüche gegen Gera auf", "Peace of Weißenfels: Landgrave Friedrich gives up his claims against Gera", 344, "b1")
ev(1319, "acq", "gera", "Heinrich d. ä. von Gera kauft das Vorwerk Tinz und die Münze zu Gera vom Haus Weida", "Heinrich the elder of Gera buys the manor of Tinz and the mint at Gera from the house of Weida", 344, "b1", obj="Tinz und Münze zu Gera", mode="kauf")
ev(1320, "treaty", "gera", "Die Lobdaburger geben ihre Forderungen auf Schleiz und Burgk auf", "The Lobdaburgs give up their claims to Schleiz and Burgk", 344, "b1")
ev(1333, "acq", "gera", "Heinrich d. ä. kauft die halbe Pflege Langenberg von Friedrich von Schönburg", "Heinrich the elder buys half of the Langenberg district from Friedrich of Schönburg", 344, "b1", obj="halbe Pflege Langenberg", mode="kauf")
ev(1335, "acq", "gera", "Der Landgraf überlässt Gera die Stadt Zwickau, bis seine Schuld beglichen ist", "The landgrave leaves the town of Zwickau to Gera until his debt is settled", 344, "b1", obj="Stadt Zwickau", mode="pfand")
ev(1348, "disaster", "land", "Der Schwarze Tod durchzieht das Voigtland; die Juden werden aus Schleiz und Gera vertrieben", "The Black Death sweeps through the Voigtland; the Jews are expelled from Schleiz and Gera", 344, "b2")
ev(1358, "loss", "gera", "Heinrich der Worthalter trägt Reitzenstein und Sparnberg der Krone Böhmen zu Lehen auf", "Heinrich the Wordkeeper surrenders Reitzenstein and Sparnberg to the crown of Bohemia as fiefs", 344, "b2", obj="Reitzenstein und Sparnberg", mode="lehnsauftrag")
ev(1359, "found", "gera", "Heinrich der Worthalter gibt der Stadt Schleiz Statuten", "Heinrich the Wordkeeper grants the town of Schleiz statutes", 344, "b2")
ev(1364, "acq", "gera", "Heinrich der Worthalter kauft die vom Haus Plauen erworbene Hälfte von Langenberg", "Heinrich the Wordkeeper buys the half of Langenberg that the house of Plauen had acquired", 344, "b2", obj="halb Langenberg", mode="kauf")
ev(1365, "loss", "gera", "Gera verpfändet Burgk an das Ordenshaus zu Schleiz", "Gera pledges Burgk to the Order's house at Schleiz", 345, "b1", obj="Burgk", mode="pfand")
ev(1369, "loss", "gera", "Gera verpfändet Lobenstein mit Nordhalben und den höfer Lehen an die Wettiner", "Gera pledges Lobenstein with Nordhalben and the Hof fiefs to the Wettins", 345, "b1", obj="Lobenstein, Nordhalben, höfer Lehen", mode="pfand")
ev(1370, "loss", "gera", "Gera verpfändet Reichenfels an die Herren von Tannrode", "Gera pledges Reichenfels to the lords of Tannrode", 345, "b1", obj="Reichenfels", mode="pfand")
ev(1371, "acq", "gera", "Gera löst Lobenstein mit böhmischem Geld wieder ein und trägt es der Krone Böhmen zu Lehen auf", "Gera redeems Lobenstein with Bohemian money and surrenders it as a fief to the crown of Bohemia", 345, "b1", obj="Herrschaft Lobenstein", mode="loesung")
ev(1374, "loss", "gera", "Gera muss Burgk, Schleiz, Saalburg und Reichenfels den thüringischen Landgrafen zu Lehen reichen; keine Herrschaft ist mehr reichsfrei", "Gera has to hold Burgk, Schleiz, Saalburg and Reichenfels as fiefs of the landgraves of Thuringia; no lordship is imperial any more", 345, "b1", obj="Burgk, Schleiz, Saalburg, Reichenfels", mode="lehnsauftrag")
ev(1380, "acq", "gera", "Gera erhält das Vorkaufsrecht auf die halbe Herrschaft Weida", "Gera obtains the right of pre-emption on half of the lordship of Weida", 345, "b2", obj="halbe Herrschaft Weida", mode="vorkauf")
ev(1385, "treaty", "gera", "Vertrag mit dem Hochstift Naumburg trennt weltliche und geistliche Gerichtsbarkeit", "Treaty with the cathedral chapter of Naumburg separates secular and ecclesiastical jurisdiction", 345, "b2")
ev(1387, "loss", "gera", "Gera verkauft mit Oswald von Truhendingen Schesslitz und Gügel an das Bistum Bamberg", "Gera, with Oswald of Truhendingen, sells Schesslitz and Gügel to the bishopric of Bamberg", 345, "b2", obj="Schesslitz und Gügel", mode="verkauf")
ev(1403, "acq", "gera", "Heinrich der Dispensirte erwirbt von der Familie Marschalk deren nordhalbensche Güter", "Heinrich the Dispensed acquires the Nordhalben estates of the Marschalk family", 345, "b2", obj="Güter in Nordhalben", mode="unbekannt")
ev(1405, "found", "gera", "Pfaffenbrief: Verzicht auf das Regentenrecht am Nachlass der Pfarrer", "Pfaffenbrief: renunciation of the ruler's right to the estates of parish priests", 345, "b2")
ev(1415, "acq", "gera", "Landgraf Friedrich belehnt die Söhne des Dispensirten mit Gera, Schleiz, Reichenfels, Langenberg und einem Teil von Heringen", "Landgrave Friedrich enfeoffs the sons of the Dispensed with Gera, Schleiz, Reichenfels, Langenberg and part of Heringen", 346, "b2", obj="Gera, Schleiz, Reichenfels, Langenberg, Teil von Heringen", mode="lehen")
ev(1420, "acq", "gera", "König Sigismund belehnt die drei Brüder mit Lobenstein und den höfer Lehen", "King Sigismund enfeoffs the three brothers with Lobenstein and the Hof fiefs", 346, "b2", obj="Lobenstein, höfer Lehen", mode="lehen")
ev(1426, "dyn", "gera", "Teilung der Lande unter den drei Söhnen des Dispensirten: Burgk/Schleiz, Lobenstein, Gera", "Division of the lands among the three sons of the Dispensed: Burgk/Schleiz, Lobenstein, Gera", 346, "b2")
ev(1426, "war", "land", "Schlacht bei Aussig gegen die Hussiten (Juni 1426)", "Battle of Aussig against the Hussites (June 1426)", 347, "b1")
ev(1438, "found", "gera", "Heinrich d. ä. von Gera erhebt Zeulenroda zur Stadt", "Heinrich the elder of Gera raises Zeulenroda to a town", 347, "b1")
ev(1443, "acq", "gera", "Kaiser Friedrich belehnt die Brüder mit der Beste Ehrenstein, dem Leibgeding ihrer Frauen", "Emperor Friedrich enfeoffs the brothers with Ehrenstein, their wives' dower", 347, "b1", obj="Beste Ehrenstein", mode="lehen")
ev(1446, "war", "gera", "Sächsischer Bruderkrieg (1446–1450) zwischen Kurfürst Friedrich und Herzog Wilhelm; Gera wird hineingezogen", "Saxon war between the brothers Elector Friedrich and Duke Wilhelm (1446–1450); Gera is drawn in", 347, "b1")
ev(1447, "dyn", "gera", "Teilung der Brüder von Gera in Gera-Lobenstein und Gera-Schleiz", "The brothers of Gera divide into Gera-Lobenstein and Gera-Schleiz", 347, "b1")
ev(1448, "acq", "gera", "Heinrich d. ä. kauft Schloss und Stadt Rochsburg und gewinnt schlüsselburgische Güter in Franken", "Heinrich the elder buys castle and town of Rochsburg and gains Schlüsselburg estates in Franconia", 347, "b1", obj="Rochsburg, schlüsselburgische Güter", mode="kauf")
ev(1450, "war", "gera", "Herzog Wilhelm erstürmt Gera (15. Oktober), brennt die Stadt nieder, angeblich etwa 5000 Einwohner kommen um, der Landesherr wird gefangen", "Duke Wilhelm storms Gera (15 October), burns the town down, allegedly about 5000 inhabitants are killed, the lord is taken prisoner", 348, "b2")
ev(1451, "treaty", "gera", "Frieden: Landgraf Ludwig von Hessen vergleicht die Fürsten und die Herren von Gera mit Graf Heinrich von Schwarzburg (27. Januar)", "Peace: Landgrave Ludwig of Hesse reconciles the princes and the lords of Gera with Count Heinrich of Schwarzburg (27 January)", 348, "b2")
ev(1474, "disaster", "gera", "Brand von Schleiz", "Fire of Schleiz", 349, "b1", derived_year=True)
ev(1478, "acq", "gera", "Heinrich d. ä. gewinnt Burgk zurück", "Heinrich the elder regains Burgk", 349, "b2", obj="Burgk", mode="loesung")
ev(1482, "dyn", "gera", "Die drei weltlichen Brüder teilen ihr Erbland: Gera, Schleiz, Lobenstein", "The three lay brothers divide their inheritance: Gera, Schleiz, Lobenstein", 349, "b2")
ev(1494, "found", "gera", "Heinrich d. m. erhebt Tanna zur Stadt", "Heinrich the middle brother raises Tanna to a town", 350, "b1")
ev(1496, "loss", "gera", "Zeulenroda wird der Tochter Katharina als Heiratsgut an das Haus Reuß-Greiz mitgegeben", "Zeulenroda is given to the daughter Katharina as dowry to the house of Reuss-Greiz", 349, "b2", obj="Zeulenroda", mode="mitgift")
ev(1497, "acq", "gera", "Heinrich d. m. kauft von seinem jüngeren Bruder die Herrschaft Lobenstein", "Heinrich the middle brother buys the lordship of Lobenstein from his younger brother", 350, "b1", obj="Herrschaft Lobenstein", mode="kauf")
ev(1501, "acq", "gera", "Heinrich d. ä. kauft von seinem jüngeren Bruder die Pflege Langenberg", "Heinrich the elder buys the Langenberg district from his younger brother", 350, "b3", obj="Pflege Langenberg", mode="kauf")
ev(1509, "dyn", "gera", "Lobenstein, Saalburg und Burgk werden schiedsrichterlich geteilt", "Lobenstein, Saalburg and Burgk are divided by arbitration", 350, "b1")
ev(1517, "found", "land", "Luthers Auftreten (1517) löst die Reformation aus; die Herren von Gera widerstreben zunächst", "Luther's appearance (1517) triggers the Reformation; the lords of Gera resist at first", 350, "b2")
ev(1525, "war", "gera", "Die Stadt Gera beteiligt sich am Bauernkrieg", "The town of Gera takes part in the Peasants' War", 350, "b3")
ev(1533, "found", "gera", "Einführung der Reformation in Gera und Schleiz (Lobenstein 1543)", "Introduction of the Reformation in Gera and Schleiz (Lobenstein 1543)", 350, "b2")
ev(1547, "loss", "gera", "Nach der Schlacht bei Mühlberg wird über Heinrich d. j. die Reichsacht gesprochen; er verzichtet auf Gera", "After the battle of Mühlberg the imperial ban is pronounced on Heinrich the younger; he renounces Gera", 351, "b2", obj="Gera", mode="krieg")
ev(1550, "dyn", "gera", "Heinrich d. j. von Gera stirbt ohne Erben: das Haus Gera erlischt, der Burggraf von Plauen nimmt die Herrschaften in Besitz", "Heinrich the younger of Gera dies without heirs: the house of Gera becomes extinct, the burgrave of Plauen takes possession of its lordships", 351, "b2")
# ---------------------------------------------------------------- line Plauen (burgraves) and Reuss-Plauen
ev(1261, "treaty", "plauen", "Heinrich der Ruthene vergleicht sich mit dem Pfalzgrafen zu Rhein wegen des Banners", "Heinrich the Ruthenian settles with the count palatine of the Rhine about the banner", 354, "b2")
ev(1272, "acq", "plauen", "Heinrich der Ruthene erhält von König Ottokar von Böhmen das Schloss Gräslitz", "Heinrich the Ruthenian receives the castle of Gräslitz from King Ottokar of Bohemia", 354, "b2", obj="Schloss Gräslitz", mode="gabe")
ev(1278, "acq", "plauen", "Heinrich der Ruthene erhält vom Grafen Conrad von Eberstein dessen Lehen im Gau Dobene", "Heinrich the Ruthenian receives from Count Conrad of Eberstein his fiefs in the Dobene district", 354, "b2", obj="ebersteinische Lehen im Gau Dobene", mode="lehen")
ev(1281, "acq", "plauen", "Heinrich der Ruthene erhält von Kaiser Rudolf die Märkte Asch und Selb als Pfand", "Heinrich the Ruthenian receives the markets of Asch and Selb as a pledge from Emperor Rudolf", 354, "b2", obj="Asch und Selb", mode="pfand")
ev(1288, "acq", "plauen", "Heinrich der Ruthene erwirbt die Güter des Albert von Neiperg", "Heinrich the Ruthenian acquires the estates of Albert of Neiperg", 354, "b2", obj="Güter des Albert von Neiperg", mode="unbekannt")
ev(1290, "acq", "plauen", "Heinrich der Ruthene erhält vom Landgrafen das Gut Tinz als Pfand", "Heinrich the Ruthenian receives the estate of Tinz from the landgrave as a pledge", 354, "b2", obj="Gut Tinz", mode="pfand")
ev(1296, "acq", "plauen", "Heinrich der Ruthene erhält von König Adolf das Schloss Hirschberg", "Heinrich the Ruthenian receives the castle of Hirschberg from King Adolf", 354, "b2", obj="Schloss Hirschberg", mode="gabe")
ev(1305, "dyn", "plauen", "Die Enkel des Ruthenen teilen: Plauen (ältere Linie) und Greiz mit Ronneburg, Werdau, Reichenbach, Mylau (jüngere Linie Reuß)", "The grandsons of the Ruthenian divide: Plauen (older line) and Greiz with Ronneburg, Werdau, Reichenbach, Mylau (younger, Reuss line)", 355, "b1")
ev(1323, "acq", "reuss_plauen", "Kaiser Ludwig belehnt Heinrich Reuß mit den altväterlichen Reichslehen und dem Bergwerk", "Emperor Ludwig enfeoffs Heinrich Reuss with the ancestral imperial fiefs and the mine", 365, "b1", obj="altväterliche Reichslehen, Bergwerk", mode="lehen")
ev(1327, "acq", "reuss_plauen", "Heinrich Reuß kauft Spilmannsdorf und mit Heinrich von Gera die Pflege Langenberg", "Heinrich Reuss buys Spilmannsdorf and, with Heinrich of Gera, the Langenberg district", 365, "b1", obj="Spilmannsdorf, Pflege Langenberg", mode="kauf")
ev(1327, "acq", "plauen", "Heinrich der Lange von Plauen trägt seine ebersteinischen Lehen der Krone Böhmen auf und erhält Voigtsberg", "Heinrich the Long of Plauen surrenders his Eberstein fiefs to the crown of Bohemia and receives Voigtsberg", 355, "b2", obj="Voigtsberg", mode="lehen")
ev(1331, "treaty", "reuss_plauen", "Kaiserliche Entscheidung im Streit mit Landgraf Friedrich: Rückgabe der Reichspfandschaften, 3000 Schock Groschen Entschädigung", "Imperial decision in the dispute with Landgrave Friedrich: return of the imperial pledges, 3000 Schock Groschen compensation", 366, "b2")
ev(1334, "treaty", "plauen", "Heinrich der Lange verbindet sich auf fünf Jahre mit thüringischen Grafen und Städten gegen den Landgrafen", "Heinrich the Long allies for five years with Thuringian counts and towns against the landgrave", 356, "b1")
ev(1337, "acq", "plauen", "Heinrich der Lange kauft mit Bewilligung des Kaisers Eprechtstein", "Heinrich the Long buys Eprechtstein with the emperor's permission", 356, "b1", obj="Eprechtstein", mode="kauf")
ev(1349, "dyn", "reuss_plauen", "Tod Landgraf Friedrichs des Ernsthaften und Heinrich Reuß' des Kleinen", "Death of Landgrave Friedrich the Serious and of Heinrich Reuss the Small", 367, "b2")
ev(1354, "war", "gesamt", "Voigtländischer Krieg: die Thüringer Landgrafen bewältigen das Land der Verbündeten, Elsterberg wird verwüstet", "Voigtland War: the Thuringian landgraves overcome the land of the allies, Elsterberg is devastated", 367, "b2")
ev(1354, "loss", "reuss_plauen", "Thüringen nimmt die drei Streitämter und die pleißener Güter; Greiz mit Ronneburg und Werdau wird thüringisches Lehen", "Thuringia takes the three disputed districts and the Pleißen estates; Greiz with Ronneburg and Werdau becomes a Thuringian fief", 367, "b2", obj="Streitämter, pleißener Güter, Greiz (Lehnshoheit)", mode="krieg")
ev(1357, "loss", "plauen", "Plauen tauscht Hirschberg, Adorf, Mühltroff und Pausa an Meißen gegen Borna, Kohren und Geithain und nimmt sie zu Lehen", "Plauen exchanges Hirschberg, Adorf, Mühltroff and Pausa to Meißen for Borna, Kohren and Geithain and holds them as fiefs", 356, "b1", obj="Hirschberg, Adorf, Mühltroff, Pausa", mode="tausch")
ev(1359, "dyn", "reuss_plauen", "Die drei Söhne Heinrichs des Strengen teilen das Erbe: Greiz; Ronneburg, Werdau, Posterstein u. a.", "The three sons of Heinrich the Severe divide the inheritance: Greiz; Ronneburg, Werdau, Posterstein and others", 367, "b3")
ev(1364, "loss", "reuss_plauen", "Die jüngeren Brüder verkaufen die Hälfte von Langenberg um 800 Schock Groschen an Gera", "The younger brothers sell half of Langenberg to Gera for 800 Schock Groschen", 367, "b3", obj="halb Langenberg", mode="verkauf", price=800, unit="Schock Groschen", also=[(368, "b1")])
ev(1367, "loss", "reuss_plauen", "Greiz verpfändet Mylau mit Reichenbach, später Treuen, an die Krone Böhmen", "Greiz pledges Mylau with Reichenbach, later Treuen, to the crown of Bohemia", 368, "b1", obj="Mylau, Reichenbach, Treuen", mode="pfand")
ev(1368, "found", "plauen", "Heinrich der Lange gibt der Stadt Plauen Statuten", "Heinrich the Long gives the town of Plauen statutes", 356, "b1")
ev(1387, "acq", "plauen", "Heinrich d. ä. kauft Königswart und Würschengrün um 13,000 Schock Groschen", "Heinrich the elder buys Königswart and Würschengrün for 13,000 Schock Groschen", 357, "b1", obj="Königswart, Würschengrün", mode="kauf", price=13000, unit="Schock Groschen")
ev(1393, "acq", "plauen", "Burggraf Heinrich I. löst von den Landgrafen Pausa wieder ein", "Burgrave Heinrich I redeems Pausa from the landgraves", 357, "b2", obj="Pausa", mode="loesung")
ev(1399, "war", "reuss_plauen", "Heinrich Reuß d. j. führt Krieg mit König Wenzel, wird in Reichenbach belagert und gefangen, bald befreit", "Heinrich Reuss the younger wages war on King Wenzel, is besieged and captured at Reichenbach, soon freed", 368, "b1")
ev(1410, "war", "plauen", "Heinrich von Plauen rettet als Ordensritter die Marienburg gegen die Polen", "Heinrich of Plauen saves the Marienburg against the Poles as a knight of the Order", 358, "b2")
ev(1411, "loss", "reuss_plauen", "Heinrich d. ä. von Greiz verpfändet die Halsgerichte seines Gebiets auf drei Jahre für 150 Goldgulden", "Heinrich the elder of Greiz pledges the high jurisdiction of his territory for three years for 150 gold gulden", 368, "b1", obj="Halsgerichte (Gerichtsrechte)", mode="pfand", price=150, unit="Goldgulden")
ev(1418, "loss", "plauen", "Burggraf Heinrich I. verpfändet Plauen an die Burggrafen von Nürnberg", "Burgrave Heinrich I pledges Plauen to the burgraves of Nuremberg", 357, "b2", obj="Plauen", mode="pfand")
ev(1420, "war", "plauen", "Heinrich I. verteidigt das Schloss zu Prag gegen die Hussiten", "Heinrich I defends the castle of Prague against the Hussites", 357, "b2")
ev(1422, "war", "plauen", "Heinrich I. leitet die Belagerung von Saatz", "Heinrich I directs the siege of Saaz", 357, "b2")
ev(1426, "acq", "plauen", "König Sigismund belehnt Heinrich I. mit dem Burggrafthum Meißen", "King Sigismund enfeoffs Heinrich I with the burgraviate of Meißen", 357, "b2", obj="Burggrafthum Meißen", mode="lehen")
ev(1428, "treaty", "plauen", "Vertrag zu Arnshaugk mit Kursachsen (7. September): Anerkennung des Lehnbriefs, Zugeständnis von Schloss Meißen und Frauenstein", "Treaty of Arnshaugk with Electoral Saxony (7 September): recognition of the enfeoffment, concession of Meißen castle and Frauenstein", 357, "b2")
ev(1430, "war", "plauen", "Die Hussiten verwüsten das Voigtland, vor allem Plauen", "The Hussites devastate the Voigtland, above all Plauen", 358, "b3")
ev(1440, "loss", "plauen", "Burggraf Heinrich II. verzichtet gegen 9000 Gulden auf die Burggrafschaft Meißen und die Lehnsherrlichkeit von Wildenfels", "Burgrave Heinrich II renounces the burgraviate of Meißen and the overlordship of Wildenfels for 9000 gulden", 358, "b3", obj="Burggrafschaft Meißen, Lehnsherrlichkeit Wildenfels", mode="lehnsauftrag", price=9000, unit="Gulden")
ev(1449, "dyn", "reuss_plauen", "Neue Teilung der Herrschaft Greiz unter den Brüdern Reuß (23. Mai)", "New division of the lordship of Greiz between the Reuss brothers (23 May)", 369, "b2")
ev(1457, "acq", "reuss_plauen", "Heinrich Reuß d. j. kauft Schloss Oberkranichfeld um 3300 Gulden; der Kranich kommt ins Wappen", "Heinrich Reuss the younger buys Oberkranichfeld castle for 3300 gulden; the crane enters the coat of arms", 369, "b2", obj="Oberkranichfeld", mode="kauf", price=3300, unit="Gulden")
ev(1462, "acq", "reuss_plauen", "Nach dem Tod des Bruders erbt Heinrich d. ä. ganz Greiz und Oberkranichfeld", "After his brother's death Heinrich the elder inherits all of Greiz and Oberkranichfeld", 369, "b2", obj="Herrschaft Greiz (ganz), Oberkranichfeld", mode="erbe")
ev(1463, "acq", "reuss_plauen", "Bischof Peter von Naumburg belehnt Heinrich d. ä. mit dem naumburger Lehnskomplex (mehr als 40 Güter)", "Bishop Peter of Naumburg enfeoffs Heinrich the elder with the Naumburg fief complex (more than 40 estates)", 370, "b1", obj="naumburger Lehnskomplex (über 40 Güter)", mode="lehen")
ev(1466, "loss", "plauen", "Burggraf Heinrich III. wird geächtet; Sachsen erobert seine voigtländischen Besitzungen", "Burgrave Heinrich III is outlawed; Saxony conquers his Voigtland possessions", 359, "b2", obj="voigtländische Besitzungen (u. a. Plauen)", mode="krieg")
ev(1482, "loss", "plauen", "Vertrag zu Brüx: Burggraf Heinrich IV. entsagt seinen Ansprüchen auf Plauen", "Treaty of Brüx: Burgrave Heinrich IV renounces his claims to Plauen", 360, "b1", obj="Plauen (Ansprüche)", mode="lehnsauftrag")
ev(1482, "acq", "plauen", "Sachsen gibt Heinrich IV. die Herrschaften Königswart, Neuhartenstein und Petschau heraus", "Saxony hands over the lordships of Königswart, Neuhartenstein and Petschau to Heinrich IV", 360, "b1", obj="Königswart, Neuhartenstein, Petschau", mode="loesung")
ev(1485, "dyn", "reuss_plauen", "Teilung der drei Brüder von Greiz: Greiz gemeinsam, Oberkranichfeld an Heinrich d. m.", "Division by the three brothers of Greiz: Greiz jointly, Oberkranichfeld to Heinrich the middle brother", 370, "b2")
ev(1490, "acq", "plauen", "Burggraf Heinrich IV. wird mit der Herrschaft Breitenstein belehnt und kauft Schönfeld und Schlackenwalde", "Burgrave Heinrich IV is enfeoffed with the lordship of Breitenstein and buys Schönfeld and Schlackenwalde", 360, "b1", obj="Breitenstein, Schönfeld, Schlackenwalde", mode="lehen")
ev(1495, "acq", "plauen", "Burggraf Heinrich IV. kauft Waldmünchen und Schwarzenberg", "Burgrave Heinrich IV buys Waldmünchen and Schwarzenberg", 360, "b1", obj="Waldmünchen, Schwarzenberg", mode="kauf")
ev(1496, "acq", "reuss_plauen", "Greiz erhält durch die Heirat mit Katharina von Gera den Markt Zeulenroda als Heiratsgut", "Greiz receives the market town of Zeulenroda as dowry through the marriage with Katharina of Gera", 349, "b2", obj="Zeulenroda", mode="mitgift", also=[(370, "b2")])
ev(1502, "treaty", "reuss_plauen", "Vertrag vom 7. Juli: Heinrich d. j. behält ganz Greiz, Heinrich d. m. erhält Kranichfeld", "Treaty of 7 July: Heinrich the younger keeps all of Greiz, Heinrich the middle brother receives Kranichfeld", 370, "b2")
ev(1502, "acq", "plauen", "Burggraf Heinrich IV. wird unter die Mitbelehnten von Lobenstein aufgenommen", "Burgrave Heinrich IV is admitted among the co-enfeoffed of Lobenstein", 360, "b1", obj="Lobenstein (Mitbelehnung)", mode="lehen")
ev(1529, "dyn", "reuss_plauen", "Heinrich d. m. tritt Kranichfeld an seinen Bruder Heinrich den Friedsamen ab", "Heinrich the middle brother cedes Kranichfeld to his brother Heinrich the Peaceful", 370, "b2")
ev(1529, "found", "reuss_plauen", "Heinrich der Friedsame führt die Reformation in Kranichfeld und darauf in Greiz ein", "Heinrich the Peaceful introduces the Reformation in Kranichfeld and then in Greiz", 371, "b1")
ev(1537, "treaty", "gesamt", "Vertrag vom 4. Juli: die Herren Reuß und der Burggraf teilen künftig die geraischen Lehen (Eventualbelehnung)", "Treaty of 4 July: the lords Reuss and the burgrave are to share the Gera fiefs (contingent enfeoffment)", 373, "b2")
ev(1547, "war", "reuss_plauen", "Schlacht bei Mühlberg (24. April); über die drei Brüder Reuß wird die Reichsacht gesprochen", "Battle of Mühlberg (24 April); the imperial ban is pronounced on the three Reuss brothers", 373, "b3")
ev(1547, "loss", "reuss_plauen", "Ihr Land (außer Kranichfeld) fällt infolge der Acht an Burggraf Heinrich V.", "Their land (except Kranichfeld) falls to Burgrave Heinrich V as a result of the ban", 373, "b3", obj="Greiz, Posterstein u. a. (außer Kranichfeld)", mode="krieg", also=[(374, "b1")])
ev(1547, "acq", "plauen", "Der Kaiser überträgt Burggraf Heinrich V. Gera und die Lehngüter der Herren von Greiz als böhmisches Lehen", "The emperor gives Burgrave Heinrich V Gera and the fief estates of the lords of Greiz as a Bohemian fief", 361, "b1", obj="Gera, Lehngüter von Greiz", mode="lehen")
ev(1548, "acq", "plauen", "Heinrich V. wird mit den um 32,000 Thaler angekauften anhaltinischen Landen belehnt", "Heinrich V is enfeoffed with the Anhalt lands bought for 32,000 thalers", 361, "fn1", obj="anhaltinische Lande", mode="lehen", price=32000, unit="Thaler")
ev(1549, "acq", "plauen", "Heinrich V. erhält die Herrschaft Hirschberg von Böhmen geschenkt", "Heinrich V is given the lordship of Hirschberg by Bohemia", 361, "b1", obj="Herrschaft Hirschberg", mode="gabe")
ev(1549, "acq", "reuss_plauen", "Die Herren von Greiz erhalten Greiz und Stein zurück, bleiben aber von der Nachfolge in Gera ausgeschlossen", "The lords of Greiz get Greiz and Stein back, but are excluded from the succession in Gera", 361, "b1", obj="Greiz, Stein", mode="loesung")
ev(1550, "acq", "plauen", "Nach dem Erlöschen des Hauses Gera nimmt der Burggraf Schleiz, Lobenstein, Saalburg, Burgk und Reichenfels als böhmische Lehen in Besitz", "After the house of Gera dies out the burgrave takes possession of Schleiz, Lobenstein, Saalburg, Burgk and Reichenfels as Bohemian fiefs", 361, "b1", obj="Schleiz, Lobenstein, Saalburg, Burgk, Reichenfels", mode="erbe")
ev(1552, "found", "plauen", "Burggräfliche Kirchenordnung, verfasst von Korbinian Hendel, Grundlage aller späteren reußischen Kirchenordnungen", "Burgraves' church order, written by Korbinian Hendel, basis of all later Reuss church orders", 361, "b1")
ev(1553, "war", "plauen", "Heinrich V. zieht gegen Markgraf Albrecht von Brandenburg, erobert Hof und belagert die Plassenburg", "Heinrich V marches against Margrave Albrecht of Brandenburg, takes Hof and besieges the Plassenburg", 361, "b1")
ev(1554, "dyn", "plauen", "Burggraf Heinrich V. stirbt plötzlich vor der Plassenburg; sein Hausbau stürzt rasch zusammen", "Burgrave Heinrich V dies suddenly before the Plassenburg; the edifice of his house quickly collapses", 361, "b1")
ev(1556, "loss", "plauen", "Die Burggrafen verpfänden Pausa an Georg von Schönburg", "The burgraves pledge Pausa to Georg of Schönburg", 362, "b1", obj="Pausa", mode="pfand")
ev(1559, "loss", "plauen", "Heinrich VI. versetzt das ganze plauensche Land an Sachsen (Pfandschaft um 60,000 Gulden)", "Heinrich VI pledges the whole Plauen land to Saxony (pledge for 60,000 gulden)", 362, "b1", obj="ganzes plauensches Land", mode="pfand", price=60000, unit="Gulden")
ev(1560, "dyn", "plauen", "Die Burggrafen Heinrich VI. und VII. teilen ihr Erbe", "The burgraves Heinrich VI and VII divide their inheritance", 362, "b1")
ev(1562, "loss", "plauen", "Der Prozess mit den Reußen zwingt die Burggrafen, Greiz, Gera und Posterstein zurückzugeben und 40,000 Gulden zu zahlen", "The lawsuit with the Reuss lords forces the burgraves to return Greiz, Gera and Posterstein and pay 40,000 gulden", 362, "b1", obj="Greiz, Gera, Posterstein", mode="prozess", price=40000, unit="Gulden")
ev(1562, "acq", "reuss_plauen", "Die Reuß erhalten im Prozess Greiz, Posterstein und Gera zurück und Erbrechte auf Schleiz, Lobenstein u. a.", "In the lawsuit the Reuss get Greiz, Posterstein and Gera back and inheritance rights to Schleiz, Lobenstein and others", 362, "b1", obj="Greiz, Posterstein, Gera", mode="prozess")
ev(1563, "dyn", "plauen", "Neuer Erbvergleich der Burggrafen über Lande und Schulden", "New inheritance settlement of the burgraves over lands and debts", 362, "b1")
ev(1564, "dyn", "reuss_plauen", "Die drei Brüder Reuß teilen ihr Gebiet: Gera, Untergreiz, Obergreiz (Ausgangspunkt der beiden Linien)", "The three Reuss brothers divide their territory: Gera, Untergreiz, Obergreiz (origin of the two lines)", 374, "b2")
ev(1567, "found", "reuss_plauen", "Die Brüder erlassen die reussische (geraische) Kirchenordnung", "The brothers issue the Reuss (Gera) church order", 374, "b2")
ev(1569, "loss", "plauen", "Burggraf Heinrich VII. verkauft das hoch verpfändete Plauen an Sachsen", "Burgrave Heinrich VII sells the heavily pledged Plauen to Saxony", 363, "b1", obj="Plauen", mode="verkauf")
ev(1572, "dyn", "plauen", "Burggraf Heinrich VII. stirbt als letzter seines Hauses: die burggräfliche Linie erlischt", "Burgrave Heinrich VII dies as the last of his house: the burgraves' line becomes extinct", 363, "b1")
ev(1572, "acq", "reuss_jung", "Heinrich d. j. von Gera, Gründer der jüngeren Linie, erhält ein Drittel der angefallenen Lande des Burggrafen Heinrich VII.", "Heinrich the younger of Gera, founder of the younger line, receives a third of the lands that fell in from Burgrave Heinrich VII", 375, "b3", obj="Drittel der burggräflichen Lande (Schleiz, Lobenstein)", mode="erbe")
ev(1572, "acq", "reuss_alt", "Heinrich der Ältere erhält ein Drittel von Lobenstein und Schleiz aus dem burggräflichen Erbe", "Heinrich the elder receives a third of Lobenstein and Schleiz from the burgraves' inheritance", 389, "b4", obj="Drittel von Lobenstein und Schleiz", mode="erbe")
# ---------------------------------------------------------------- Reuss older line
ev(1583, "dyn", "reuss_alt", "Heinrich II. und Heinrich V. teilen Untergreiz: Untergreiz und Dölau", "Heinrich II and Heinrich V divide Untergreiz: Untergreiz and Dölau", 389, "b4")
ev(1585, "loss", "reuss_alt", "Die Brüder verkaufen ihre Anteile an Lobenstein und Kranichfeld an die jüngere Linie (1585/86)", "The brothers sell their shares of Lobenstein and Kranichfeld to the younger line (1585/86)", 389, "b4", obj="Anteile an Lobenstein und Kranichfeld", mode="verkauf")
ev(1596, "dyn", "reuss_alt", "Teilung der Herrschaft Schleiz; es entstehen die Zweige Burgk und Untergreiz", "Division of the lordship of Schleiz; the branches of Burgk and Untergreiz arise", 389, "b4")
ev(1616, "dyn", "reuss_alt", "Die mittlere Linie (Obergreiz) erlischt; ihr Land fällt an die beiden anderen Linien", "The middle line (Obergreiz) becomes extinct; its land falls to the two other lines", 375, "b1")
ev(1625, "dyn", "reuss_alt", "Teilung der Herrschaft Greiz in Obergreiz und Untergreiz mitten im Dreißigjährigen Krieg", "Division of the lordship of Greiz into Obergreiz and Untergreiz in the middle of the Thirty Years' War", 390, "b3")
ev(1668, "dyn", "reuss_alt", "Die drei Söhne Heinrichs V. teilen: Burgk, Untergreiz, Rothenthal", "The three sons of Heinrich V divide: Burgk, Untergreiz, Rothenthal", 390, "b5")
ev(1694, "dyn", "reuss_alt", "Die Brüder in Obergreiz teilen das Land in Obergreiz und Dölau (nur vier Jahre)", "The brothers in Obergreiz divide the land into Obergreiz and Dölau (for four years only)", 391, "b2")
ev(1768, "dyn", "reuss_alt", "Das Haus Untergreiz erlischt; Obergreiz vereint alle Teile in einer Hand", "The house of Untergreiz becomes extinct; Obergreiz unites all parts in one hand", 391, "b1")
ev(1778, "found", "reuss_alt", "Heinrich XI. von Greiz wird von Kaiser Joseph II. in den Reichsfürstenstand erhoben", "Heinrich XI of Greiz is raised to the rank of imperial prince by Emperor Joseph II", 391, "b4")
ev(1802, "disaster", "reuss_alt", "Residenzschloss und der größte Teil der Stadt Greiz gehen in Flammen auf", "The residence castle and most of the town of Greiz go up in flames", 392, "b1")
ev(1807, "treaty", "gesamt", "Beitritt der Reußen zum Rheinbund", "The Reuss lines join the Confederation of the Rhine", 384, "b1")
ev(1815, "treaty", "gesamt", "Beitritt zum Deutschen Bund", "Accession to the German Confederation", 392, "b1")
ev(1866, "treaty", "reuss_alt", "Friedensschluss Greiz–Preußen (26. September) und Eintritt in den Norddeutschen Bund; 100,000 Taler an den preußischen Invalidenfonds", "Peace between Greiz and Prussia (26 September) and entry into the North German Confederation; 100,000 thalers to the Prussian invalids' fund", 392, "b1")
ev(1867, "dyn", "reuss_alt", "Fürst Heinrich XXII. übernimmt am 28. März die Regierung in Greiz", "Prince Heinrich XXII takes over the government in Greiz on 28 March", 392, "b1")
# ---------------------------------------------------------------- Reuss younger line
ev(1595, "found", "reuss_jung", "Heinrich Posthumus beginnt selbständig zu regieren und begründet in Gera die Wollenzeugfabrikation", "Heinrich Posthumus begins to rule on his own and founds the woollen-cloth manufacture in Gera", 375, "b3")
ev(1600, "found", "reuss_jung", "Kirchen- und Schulvisitationen im Land angeordnet", "Church and school visitations ordered in the land", 375, "b3")
ev(1604, "found", "reuss_jung", "Hofregiment (Kanzlei) und Konsistorium gestiftet", "Court government (chancery) and consistory founded", 375, "b3")
ev(1608, "found", "reuss_jung", "Gründung des Gymnasium illustre (Rutheneum) zu Gera", "Foundation of the Gymnasium illustre (Rutheneum) at Gera", 375, "b3")
ev(1613, "found", "reuss_jung", "Reußisches Appellationsgericht errichtet", "Reuss court of appeal established", 375, "b3")
ev(1615, "loss", "reuss_jung", "Heinrich Posthumus verkauft die verpfändete, entlegene Herrschaft Kranichfeld an Sachsen-Weimar", "Heinrich Posthumus sells the pledged, remote lordship of Kranichfeld to Saxe-Weimar", 376, "b1", obj="Herrschaft Kranichfeld", mode="verkauf")
ev(1632, "disaster", "reuss_jung", "Brandschatzung, Plünderung und Pest treffen das Land im Dreißigjährigen Krieg", "Extortion, plunder and plague hit the land in the Thirty Years' War", 376, "b1")
ev(1635, "dyn", "reuss_jung", "Heinrich Posthumus stirbt im Dezember; vier Söhne regieren gemeinsam vom Osterstein aus", "Heinrich Posthumus dies in December; four sons rule jointly from the Osterstein", 376, "b1")
ev(1646, "found", "reuss_jung", "Die Landesschulden werden getilgt, obwohl der Krieg die Bevölkerung um zwei Drittel vernichtet hat", "The land's debts are paid off, although the war has destroyed two thirds of the population", 376, "b1")
ev(1647, "dyn", "reuss_jung", "Teilung der Lande: Heinrich II. erhält Gera, IX. Schleiz, X. Lobenstein, I. Saalburg", "Division of the lands: Heinrich II receives Gera, IX Schleiz, X Lobenstein, I Saalburg", 376, "b2", also=[(376, "b1")])
ev(1664, "treaty", "gesamt", "Familienkongress zu Gera beschließt die Zählung der Regentennamen in beiden Linien", "Family congress at Gera decides on the numbering of the rulers' names in both lines", 377, "b1")
ev(1664, "acq", "reuss_jung", "Heinrich X. kauft von den Herren von Beulwitz die Herrschaft Hirschberg", "Heinrich X buys the lordship of Hirschberg from the lords of Beulwitz", 380, "b2", obj="Herrschaft Hirschberg", mode="kauf")
ev(1666, "dyn", "reuss_jung", "Heinrich IX. stirbt unvermählt; Schleiz fällt an Heinrich I., Saalburg wird zerteilt", "Heinrich IX dies unmarried; Schleiz falls to Heinrich I, Saalburg is divided up", 376, "b1")
ev(1668, "found", "gesamt", "Beide Linien einigen sich auf das Primogeniturrecht", "Both lines agree on the right of primogeniture", 377, "b1")
ev(1673, "found", "gesamt", "Kaiser Leopold I. erhebt die Reußen in den Reichsgrafenstand (26. April)", "Emperor Leopold I raises the Reuss lords to the rank of imperial counts (26 April)", 377, "b1")
ev(1678, "dyn", "reuss_jung", "Die Söhne Heinrichs X. teilen: Lobenstein, Hirschberg, Ebersdorf", "The sons of Heinrich X divide: Lobenstein, Hirschberg, Ebersdorf", 403, "b6")
ev(1681, "found", "gesamt", "Untheilbarkeit der Lande beschlossen", "Indivisibility of the lands decided", 377, "b1")
ev(1686, "disaster", "reuss_jung", "Brand zerstört zwei Drittel der Stadt Gera, sieben Tage nach dem Tod Heinrichs IV.", "A fire destroys two thirds of the town of Gera, seven days after the death of Heinrich IV", 379, "b2")
ev(1689, "disaster", "reuss_jung", "Schleiz brennt im Juli samt dem Residenzschloss nieder", "Schleiz burns down in July together with the residence castle", 383, "b3")
ev(1690, "found", "gesamt", "Die Primogenitur wird zum sanktionierten Landesgesetz erhoben", "Primogeniture is enacted as an approved law of the land", 377, "b1")
ev(1690, "acq", "reuss_jung", "Heinrich X. kauft Ebersdorf und macht es zum Mittelpunkt seiner Besitzungen", "Heinrich X buys Ebersdorf and makes it the centre of his possessions", 380, "b2", obj="Ebersdorf", mode="kauf")
ev(1711, "dyn", "reuss_jung", "Der Zweig Hirschberg erlischt; sein Land fällt an Lobenstein und Ebersdorf", "The Hirschberg branch becomes extinct; its land falls to Lobenstein and Ebersdorf", 380, "b2")
ev(1714, "disaster", "reuss_jung", "Feuer verheert die Stadt Lobenstein und ihr Schloss (zweite Verheerung der Stadt 1732)", "Fire devastates the town of Lobenstein and its castle (a second devastation of the town in 1732)", 381, "b1")
ev(1721, "treaty", "reuss_jung", "Heinrich XXIX. legt die Rechte der Stadt Hirschberg durch Vertrag fest", "Heinrich XXIX fixes the rights of the town of Hirschberg by treaty", 381, "b2")
ev(1732, "disaster", "reuss_jung", "Zweiter Brand der Stadt Lobenstein", "Second fire of the town of Lobenstein", 381, "b1")
ev(1733, "found", "reuss_jung", "Heinrich XXIX. gründet in Ebersdorf eine Herrnhuter-Kolonie", "Heinrich XXIX founds a Moravian colony at Ebersdorf", 381, "b2")
ev(1750, "disaster", "reuss_jung", "Brand von Hirschberg", "Fire of Hirschberg", 382, "b1")
ev(1771, "disaster", "reuss_jung", "Hungersnot und Teuerung der Jahre 1771/72", "Famine and dearth of 1771/72", 380, "b1")
ev(1780, "disaster", "reuss_jung", "Großer Brand von Gera", "Great fire of Gera", 380, "b1")
ev(1790, "found", "reuss_jung", "Heinrich XXXV. von Lobenstein wird bei der Krönung Leopolds II. zum Reichsfürsten erhoben", "Heinrich XXXV of Lobenstein is raised to imperial prince at the coronation of Leopold II", 381, "b1")
ev(1802, "dyn", "reuss_jung", "Heinrich XXX. stirbt als letzter Graf von Gera; sein Land fällt an Schleiz und Lobenstein", "Heinrich XXX dies as the last count of Gera; his land falls to Schleiz and Lobenstein", 380, "b1")
ev(1806, "found", "reuss_jung", "Heinrich XLII. von Schleiz und Heinrich LI. von Ebersdorf werden Reichsfürsten", "Heinrich XLII of Schleiz and Heinrich LI of Ebersdorf become imperial princes", 382, "b1")
ev(1817, "found", "gesamt", "Beide Linien nehmen das Oberappellationsgericht zu Jena als obersten Gerichtshof an", "Both lines accept the supreme court of appeal at Jena as their highest court", 378, "b3")
ev(1824, "dyn", "reuss_jung", "Der Zweig Lobenstein erlischt; Lobenstein fällt an Ebersdorf", "The Lobenstein branch becomes extinct; Lobenstein falls to Ebersdorf", 381, "b1")
ev(1826, "war", "reuss_jung", "Aufstand im Dorf Harra gegen die Feuerversicherung; 20 Bauern fallen in der »harraer Schlacht«", "Uprising in the village of Harra against compulsory fire insurance; 20 peasants die in the “battle of Harra”", 379, "b1")
ev(1830, "war", "reuss_jung", "Unruhen im Geraischen (1830) und in Gera und Greiz (1831), unblutig", "Unrest in the Gera region (1830) and in Gera and Greiz (1831), without bloodshed", 379, "b1")
ev(1833, "treaty", "gesamt", "Beitritt zum Zollverein", "Accession to the German Customs Union", 378, "b3")
ev(1836, "found", "reuss_jung", "Das Fürstentum Schleiz ist schuldenfrei, die halben Steuern werden erlassen; Kriminalgerichtsordnung", "The principality of Schleiz is free of debt, half of the taxes are remitted; criminal procedure code", 384, "b1")
ev(1837, "disaster", "reuss_jung", "Ein großer Teil der Stadt Schleiz samt Residenzschloss brennt ab", "A large part of the town of Schleiz together with the residence castle burns down", 384, "b1")
ev(1842, "disaster", "reuss_jung", "Im Theater zu Schleiz werden durch ein falsches Gerücht 22 Menschen erdrückt", "In the theatre at Schleiz 22 people are crushed after a false rumour", 384, "b1")
ev(1848, "war", "gesamt", "Revolutionäre Bewegung im Reußenland; Militär der Nachbarstaaten wird zur Ordnung eingesetzt", "Revolutionary movement in the Reuss lands; troops of neighbouring states restore order", 379, "b1")
ev(1848, "dyn", "reuss_jung", "Heinrich LXXII. entsagt am 1. Oktober; Schleiz erbt Ebersdorf-Lobenstein und vereint Reuß j. L. nach 223 Jahren Zerstückung", "Heinrich LXXII renounces on 1 October; Schleiz inherits Ebersdorf-Lobenstein and reunites Reuss y. l. after 223 years of fragmentation", 385, "b1")
ev(1849, "found", "reuss_jung", "Das vom Landtag beschlossene demokratische Staatsgrundgesetz wird sanktioniert (30. November)", "The democratic fundamental law passed by the Landtag is sanctioned (30 November)", 385, "b1")
ev(1850, "found", "reuss_jung", "Gemeindeordnung gewährt freie Selbstverwaltung (13. Februar)", "Municipal ordinance grants free self-government (13 February)", 385, "b1")
ev(1853, "found", "reuss_jung", "Gesetz über die Aufhebung des Lehnsverbandes (28. Juli)", "Law abolishing the feudal bond (28 July)", 385, "b1")
ev(1856, "found", "reuss_jung", "Das Staatsgrundgesetz wird wesentlich revidiert und abgeschwächt", "The fundamental law is substantially revised and weakened", 386, "b1")
ev(1863, "found", "reuss_jung", "Neue Justizgesetze (28. April): Organisation der Justiz, öffentlicher Strafprozess, Friedensgerichte", "New judicial laws (28 April): court organisation, public criminal procedure, justices of the peace", 387, "b2")
ev(1866, "treaty", "reuss_jung", "Freiwilliger Beitritt zum Norddeutschen Bund (26. Juni)", "Voluntary accession to the North German Confederation (26 June)", 388, "b2")
ev(1867, "treaty", "reuss_jung", "Militärhoheit, Post und Telegraphie gehen an das Bundespräsidium über", "Military sovereignty, post and telegraph pass to the presidency of the Confederation", 388, "b2")
ev(1867, "dyn", "reuss_jung", "Fürst Heinrich LXVII. stirbt am 11. Juli; sein Sohn Heinrich XIV. folgt", "Prince Heinrich LXVII dies on 11 July; his son Heinrich XIV succeeds", 388, "b2")

# ---------------------------------------------------------------- verification
bad = []
for e in EV:
    ys = years_in(e["page"], e["block"])
    if e["year"] not in ys and not e["derived_year"]:
        bad.append((e["year"], e["page"], e["block"], e["de"][:50]))
if bad:
    for b_ in bad:
        print("YEAR NOT IN BLOCK", b_)
    raise SystemExit(1)
EV.sort(key=lambda e: (e["year"]))
if __name__ == "__main__":
    import collections
    print(len(EV), collections.Counter(e["kind"] for e in EV))
    print(collections.Counter(e["house"] for e in EV))
