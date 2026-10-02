"""Analysis: Volkskalender (pp. 161, 181, 185-193): dated customs, weather lore, work and dishes through the year.

The entries are hand-coded paraphrases of Brückner's running text (the source is prose, not a table). Each entry is
tied to a page/block that is located by a key phrase, so that the citation is checked by the script.
"""
from collections import Counter, defaultdict
from _common import *

KINDS = {
    "brauch": bi("Brauch und Fest", "Customs and feasts"),
    "regel": bi("Wetter- und Ernteregel", "Weather and harvest lore"),
    "arbeit": bi("Landarbeit und Gesinde", "Farm work and servants"),
    "speise": bi("Festspeise", "Feast dishes"),
    "orakel": bi("Orakel, Zauber, Schutz", "Oracles, magic, protection"),
}
MONTH_DE = ["Jan.", "Febr.", "März", "April", "Mai", "Juni", "Juli", "Aug.", "Sept.", "Okt.", "Nov.", "Dez."]
MONTH_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
G, K, B, M = "gedruckt", "Kalenderfest", "beweglich", "Monat"

# (month, day, basis, kind, name_de, name_en, note_de, note_en, page, phrase)
E = [
    # --- January
    (1, 1, K, "brauch", "Neujahr", "New Year", "Anschießen und Einläuten des Jahres, gegenseitiges Glückwünschen, Beschenken der Pathen, Umsingen der Schüler.", "The year is shot and rung in; mutual good wishes, godparents give presents, schoolchildren sing from house to house.", "188", "Am Neujahr, das angeschossen"),
    (1, 1, K, "speise", "Neujahrstag: Speise", "New Year’s Day: dish", "Hirsenbrei, damit das Geld im Jahr nicht ausgeht.", "Millet porridge, so that the money does not run out in the course of the year.", "161", "am Neujahrstage Hirsenbrei"),
    (1, 1, K, "arbeit", "Neujahrstag: Stall und Mist", "New Year’s Day: stable and dung", "Ausmisten am Neujahrstag gibt den besten Mist; das Vieh erhält Häringsmilch oder drei Häringsköpfe (auch am Dreikönigsabend).", "Mucking out on New Year’s Day yields the best manure; the cattle get herring milt or three herring heads (also on Epiphany eve).", "186", "den besten Mist aber giebt es"),
    (1, 5, K, "speise", "Werre- oder Holla-Abend: Speise", "Werre or Holla evening: dish", "Polse (Mehl- oder Kartoffelgericht in Butter), um nicht von der Werre bestraft zu werden.", "Polse (a flour or potato dish fried in butter), so as not to be punished by the Werre.", "161", "am Werre- oder Holla-Abend Polse"),
    (1, 6, K, "brauch", "Heilige Drei Könige (»Oberster«)", "Epiphany (the “Oberste”)", "Früher Umzüge der Knaben mit den Puppen des Herodes und der drei Weisen; der Tag ist um einen Hahnenschrei länger.", "Formerly boys’ processions with puppets of Herod and the three Magi; the day has grown by a cock’s crow.", "188", "Am h. Dreikönigstage"),
    (1, 20, G, "regel", "Fabian Sebastian (20. Januar)", "St Fabian and St Sebastian (20 January)", "»Läßt den Saft in die Bäume gahn.«", "“Lets the sap rise into the trees.”", "188", "Fabian Sebastian (20. Januar)"),
    (1, 22, K, "regel", "Vincenttag", "St Vincent’s day", "Ein schöner Vincenttag gilt als Zeichen eines guten Erntejahres.", "A fine St Vincent’s day is a sign of a good harvest year.", "186", "ein schöner Vincenttag"),
    (1, 25, G, "regel", "Pauli Bekehrung (25. Januar)", "Conversion of St Paul (25 January)", "Helles Wetter bedeutet ein gutes Jahr, Nebel Sterben, Regen und Schnee teure Zeit, Wind Krieg oder Aufruhr; die Kinder erhielten Wurmlatwerge.", "Clear weather foretells a good year, fog deaths, rain and snow dear times, wind war or riot; children were given worm electuary.", "188", "Pauli Bekehrung (25. Januar)"),
    # --- February
    (2, 2, K, "arbeit", "Lichtmeß: Gesindewechsel", "Candlemas: change of servants", "Das abziehende Gesinde räumt das Haus vor dem neuen, das anziehende schaut ins Ofenloch und isst Klöße auf der Ofenbank.", "The departing servants leave before the new ones arrive; these look into the stove hole and eat dumplings on the stove bench.", "188", "Zu Lichtmeß besteht seit uralter Zeit Gesindewechsel"),
    (2, 2, K, "regel", "Lichtmeß: Witterung", "Candlemas: weather lore", "»Lichtmeß hell, schindet dem Bauer das Fell; Lichtmeß dunkel, macht den Bauer zum Junker; Lichtmeß klar, giebt ein gutes Flachsjahr.«", "“Bright Candlemas flays the farmer; dark Candlemas makes him a squire; clear Candlemas gives a good flax year.”", "188", "Lichtmeß hell"),
    (2, 2, K, "speise", "Lichtmeß: Speise", "Candlemas: dish", "Die große Wurst (Säusack).", "The large sausage (“Säusack”).", "161", "zu Lichtmeß hat man die große Wurst"),
    (2, None, B, "brauch", "Fastnacht", "Shrovetide", "Spinnen und landwirtschaftliche Arbeit sind verboten; Pfannkuchen, Brezeln, Mummereien, Aufzüge, Schmaus und Tanz, der »Fastnachtsnarr«.", "Spinning and farm work are forbidden; pancakes, pretzels, mummeries, processions, feasting and dancing, the “Fastnacht fool”.", "188", "Fastnacht, die Zeit, wo der Germane"),
    (2, None, B, "speise", "Fastnacht: Speise", "Shrovetide: dish", "Sauerkraut mit Wurst, Pfannkuchen oder Kräpfel, sonst geht das Geld im Jahr aus.", "Sauerkraut with sausage, pancakes or Kräpfel, otherwise the money runs out during the year.", "161", "zur Fastnacht Sauerkraut mit Wurst"),
    (2, None, B, "arbeit", "Fastnacht: Ochsen und Lein", "Shrovetide: oxen and flax", "Zu Fastnacht erstmals angespannte Ochsen werden gute Zugochsen; hohe Sprünge der Frauen sollen langen Flachs bringen.", "Oxen yoked for the first time at Shrovetide become good draught oxen; women’s high leaps are to bring long flax.", "186", "Ochsen, zum ersten Male zu Fastnacht"),
    (2, None, B, "brauch", "Aschermittwoch", "Ash Wednesday", "Die Männer gehen ins Bierhaus, um »die Gerste zu netzen«, die Frauen äschern das Garn und erzählen die »Garnlüge«.", "The men go to the alehouse to “wet the barley”, the women bleach the yarn and tell the “yarn lie”.", "189", "Am Aschermittwoch ist es hie und da Sitte"),
    (2, None, B, "brauch", "Mitfasten", "Mid-Lent", "Die Rockenstuben (Spinnstuben) werden geschlossen.", "The spinning rooms (Rockenstuben) are closed.", "189", "Zu Mitfasten werden die Rockenstuben geschlossen"),
    # --- March
    (3, 1, G, "brauch", "Todaustragen (1. März oder Lätare)", "Carrying out Death (1 March or Laetare)", "Eine Strohpuppe wird durch die Häuser getragen, aus dem Dorf getragen und in die Elster geworfen; die Kinder sammeln Eier.", "A straw puppet is carried through the houses, out of the village and thrown into the Elster; the children collect eggs.", "189", "Am ersten März (oder auch zu Lätare)"),
    (3, None, M, "regel", "Märzennebel", "March fog", "Nebel im März bedeuten Gewitter 100 Tage später.", "March fogs mean thunderstorms 100 days later.", "186", "Märzennebel mit ihren 100 Tage"),
    # --- April
    (4, 1, G, "brauch", "Erster April", "First of April", "Kinder werden mit seltsamen Aufträgen geneckt, Erwachsene gefoppt.", "Children are teased with odd errands, adults are fooled.", "189", "Am ersten April hänselt man Kinder"),
    (4, 10, "berechnet", "arbeit", "Gerstensaat am 100. Tag", "Barley sowing on the 100th day", "Gerste soll man am 100. Tage des Jahres säen.", "Barley is to be sown on the 100th day of the year.", "186", "Gerste soll man am 100. Tage"),
    (4, None, B, "brauch", "Vorabend des Palmsonntags", "Eve of Palm Sunday", "Die Konfirmanden besuchen ihre Pathen, um »abzudanken«, und stellen Pfarrer und Lehrer Tannbäumchen vor die Tür.", "Confirmands visit their godparents to “say thanks” and put fir saplings at the doors of pastor and teacher.", "189", "Am Vorabende des Palmsonntags"),
    (4, None, B, "regel", "Palmsonntag", "Palm Sunday", "Ist der Palmsonntag schön, kommt ein fruchtbares Jahr.", "If Palm Sunday is fine, a fruitful year follows.", "189", "Ist der Palmsonntag schön"),
    (4, None, B, "brauch", "Gründonnerstag", "Maundy Thursday", "Grüne Gemüse, Abgewöhnen der Kinder, Aussaat von Kohlpflanzensamen beim Glockenläuten.", "Green vegetables, weaning of children, sowing of cabbage seed during the ringing of the bells.", "189", "Der Gründonnerstag, wo man gern grüne"),
    (4, None, B, "speise", "Gründonnerstag: Speise", "Maundy Thursday: dish", "Grünes, insbesondere Kohl oder Spinat mit Eiern.", "Greens, in particular cabbage or spinach with eggs.", "161", "am grünen Donnerstage hat man Grünes"),
    (4, None, B, "brauch", "Karfreitag", "Good Friday", "Arbeitsruhe (sonst kommen Gewitter); Zahnschmerzen werden in der Nacht »verthan«; Schütteln der Obstbäume gegen Raupen.", "Rest from work (otherwise storms come); toothache is charmed away at night; shaking the fruit trees against caterpillars.", "189", "Der Charfreitag selbst, sowie Himmelfahrt"),
    (4, None, B, "speise", "Karfreitag: Speise", "Good Friday: dish", "Stockfisch.", "Stockfish.", "161", "am Charfreitage Stockfisch"),
    (4, None, B, "regel", "Karfreitags- und Osterregen", "Good Friday and Easter rain", "»Charfreitag- und Osterregen bringt wenig Segen.«", "“Good Friday and Easter rain bring little blessing.”", "186", "Charfreitag- und Osterregen bringt"),
    (4, None, B, "brauch", "Ostern", "Easter", "Osterwasser in der Osternacht, Sonnenspringen beobachten, gefärbte Eier, Eier-»Dutzen« der Knaben.", "Easter water fetched on Easter night, watching the sun “jump”, coloured eggs, the boys’ egg-tapping contest.", "189", "In der Osternacht von 11 bis 12 Uhr"),
    (4, None, B, "speise", "Ostern: Speise", "Easter: dish", "Der Osterfladen (Quarkkuchen).", "The Osterfladen (curd cake).", "161", "zu Ostern den Osterfladen"),
    # --- May
    (5, 1, G, "orakel", "Walpurgisnacht", "Walpurgis Night", "Die Hexen werden »ausgeklatscht« (Peitschenknall, Schießen), alte Besen auf Höhen angebrannt, drei Kreuze an Türen, dem Vieh wird Neunerlei gefüttert.", "The witches are “clapped out” (cracking whips, shooting), old brooms burned on hills, three crosses on doors, the cattle fed nine kinds of fodder.", "189", "In der ersten Mai- oder in der Walpurgisnacht"),
    (5, 1, K, "regel", "Walpurgi: Ernteregel", "Walpurgis: harvest lore", "»Reiche Walpurge, arme Johanne«; gute Kornernte, wenn sich zu Walpurgi eine Krähe, zu Pfingsten ein Schaf, zu Johanni eine Kuh in der Saat verstecken kann.", "“Rich Walpurga, poor John”; a good grain harvest if a crow can hide in the crop at Walpurgis, a sheep at Whitsun, a cow at St John’s.", "186", "Reiche Walpurge, arme Johanne"),
    (5, 12, K, "regel", "Pankratius und Servatius", "Pancras and Servatius", "Gelten als die letzten Frosttage.", "Regarded as the last frost days.", "190", "Pankratius und Servatius gelten"),
    (5, None, B, "brauch", "Christi Himmelfahrt", "Ascension Day", "Arbeitsruhe und Schonung von Tieren und Blumen (sonst »ziehen die Gewitter nach«); Berg- und Höhenzüge der Jugend.", "Rest from work and care for animals and flowers (otherwise storms “follow”); youths’ processions to hills and heights.", "190", "Am Himmelfahrtstage, dem Tage der Gewitter"),
    (5, None, B, "speise", "Himmelfahrt: Speise", "Ascension: dish", "Semmelmilch.", "Semmelmilch (bread roll in milk).", "161", "zu Himmelfahrt Semmelmilch"),
    (5, None, B, "regel", "Himmelfahrtsregen", "Ascension rain", "Regen an Himmelfahrt deutet auf eine schlechte Heuernte.", "Rain on Ascension Day points to a poor hay harvest.", "190", "Himmelfahrtsregen deutet auf eine schlechte"),
    (5, None, B, "brauch", "Pfingsten", "Whitsun", "Die Burschen setzen ihren Mädchen Birken (»Maien«) vor die Tür, zur Beschimpfung Vogelbeerbaum und Wacholder; Birken schmücken Stuben, Kirchen, Brunnen; Pfingstlümmel, Hammelauskegeln, Maitänze.", "Lads set birches (“Maien”) at their girls’ doors, rowan and juniper as an insult; birches decorate rooms, churches and wells; “Pfingstlümmel”, ram bowling, May dances.", "190", "Zu Pfingsten setzen die Burschen"),
    (5, None, B, "speise", "Pfingsten: Speise", "Whitsun: dish", "Der große Schinken (am ersten Pfingsttag).", "The large ham (on Whit Sunday).", "161", "am ersten Pfingsttage den großen Schinken"),
    # --- June
    (6, None, B, "arbeit", "Trinitatis", "Trinity Sunday", "Arbeitsruhe in Haus und Feld, sonst schlägt der Blitz ein.", "Rest from work in house and field, otherwise lightning strikes.", "190", "Zu Trinitat herrscht Arbeitsruhe"),
    (6, 15, G, "regel", "St. Veit (15. Juni)", "St Vitus (15 June)", "Veitsregen deutet auf eine geringe Gerstenernte.", "Rain on St Vitus’s day points to a small barley harvest.", "190", "St. Veitsregen (15. Juni)"),
    (6, 23, K, "brauch", "Johannisvorabend", "St John’s Eve", "Johannesfeuer auf den Höhen, von der Jugend mit zusammengebetteltem Holz geschürt und mit angebrannten Besen umtanzt.", "John’s fires on the hills, lit by the youth with begged wood and danced around with burning brooms.", "190", "Johannesfeuer"),
    (6, 24, K, "orakel", "Johannistag: Kräuter und Kranz", "St John’s Day: herbs and wreath", "Heilkräuter (Johannisblume) vor Sonnenaufgang oder zur Mittagsstunde; Mädchen werfen einen Kranz aus neunerlei Blumen rücklings an einen Baum, jeder Fall ohne Hängenbleiben bedeutet ein Jahr ledig.", "Medicinal herbs (arnica) gathered before sunrise or at noon; girls throw a wreath of nine flowers backwards at a tree, each fall without catching means a year unmarried.", "190", "Auch holen sich Mädchen in der Mittagsstunde"),
    (6, 24, K, "regel", "Johanni: Regen", "St John: rain", "»Vor Johanni bet um Regen, nach Johanni kommt er ungelegen.«", "“Before St John pray for rain, after St John it comes unwelcome.”", "190", "Vor Johanni bet um Regen"),
    (6, 27, G, "regel", "Siebenschläfer (27. Juni)", "Seven Sleepers (27 June)", "Der Regen am Siebenschläfer dauert sieben Wochen.", "Rain on the Seven Sleepers’ day lasts seven weeks.", "190", "Siebenschläfer (27. Juni)"),
    # --- July
    (7, 2, G, "regel", "Mariä Heimsuchung (2. Juli)", "Visitation of Mary (2 July)", "Regen: »geht Marie über's Gebirg, läßt sie das Wasser fallen«; er dauert 40 Tage.", "Rain: “when Mary crosses the mountains she lets the water fall”; it lasts 40 days.", "190", "Mariä Heimsuchung (2. Juli)"),
    (7, 13, G, "regel", "Margarethentag (13. Juli)", "St Margaret’s day (13 July)", "Bei Regen fallen die Nüsse ab.", "If it rains, the nuts fall off.", "190", "Am Margarethentag (13. Juli)"),
    (7, 25, G, "regel", "Jacobi (25. Juli)", "St James (25 July)", "»Der Schnee blüht«: viel oder wenig Wolken, viel oder wenig Schnee im nächsten Winter.", "“The snow blooms”: many or few clouds, much or little snow next winter.", "190", "Zu Jacobi (25. Juli)"),
    (7, 25, K, "arbeit", "Jacobi: Kraut und Kartoffeln", "St James: cabbage and potatoes", "»Jöf wirft sie, Barthel drückt sie, Michel nimmt sie« (Krautköpfe); Kartoffeln: zu Jacobi gegriffen, zu Laurentii probiert, zu Bartholomäi nimmt man die Hacke.", "“Jacobi sets them, Bartholomew presses them, Michael takes them” (cabbage heads); potatoes: felt at Jacobi, tested at Laurence, hoe at Bartholomew.", "187", "Jöf (Jacobi) wirft sie"),
    # --- August
    (8, None, M, "brauch", "Vogel- und Scheibenschießen", "Bird and target shooting", "In allen Städten und Marktflecken; in Hirschberg seit 1848 statt dessen ein dreitägiges Wiesenfest mit Tanz und Turnbelustigungen.", "In all towns and market villages; at Hirschberg since 1848 a three-day meadow festival with dancing and gymnastics instead.", "190", "Im August „vom Bauer"),
    (8, 10, G, "regel", "Laurentii (10. August)", "St Lawrence (10 August)", "Regen bringt Mäuse in Menge.", "Rain brings mice in numbers.", "191", "(10. August) bringt Mäuse in Menge"),
    (8, 24, G, "regel", "Bartholomäi (24. August)", "St Bartholomew (24 August)", "Er »wirft Häder ins Kraut«; am Bartholomäustag darf niemand ein Krautfeld betreten.", "He “sets the heads in the cabbage”; nobody may enter a cabbage field on St Bartholomew’s day.", "191", "Bartholomäi (24. August)"),
    (8, 24, K, "arbeit", "Bartholomäi: Beginn der Herbstarbeiten", "St Bartholomew: start of autumn work", "»Bartholomä, Bauer, sä und mäh; Simon Jude, Bauer, schließ die Bude.«", "“Bartholomew, farmer, sow and mow; Simon and Jude, farmer, shut the booth.”", "187", "Bartholomä, Bauer, sä und mäh"),
    # --- September
    (9, 1, G, "regel", "Aegidi (1. September)", "St Giles (1 September)", "»Wie der Hirsch zu Aegidi in die Brunst tritt, so tritt er heraus«: Maßstab für die Witterung bis dahin.", "“As the stag enters the rut at St Giles, so he comes out”: a guide to the weather in between.", "191", "zu Aegidi (1. September) in die Brunst"),
    (9, None, M, "arbeit", "September: Aussaat und Weide", "September: sowing and pasture", "Die neue Aussaat beginnt, die Weide ist offen (Hutjungen).", "The new sowing begins, the pasture is open (herd boys).", "191", "Im September beginnt die neue Aussaat"),
    (9, None, B, "brauch", "Erntefest", "Harvest festival", "Predigt, Erntekränze, Gegenleistung von Speise und Trank, Tanz in der Schenke; an einem der letzten zwei Sonntage vor Michaeli.", "Sermon, harvest wreaths, food and drink in return, dancing in the inn; on one of the last two Sundays before Michaelmas.", "187", "Erndtefest, das vordem beliebig"),
    (10, None, B, "brauch", "Kirchweih (Kirmes)", "Church fair (Kirmes)", "Krone der ländlichen Haus- und Dorffeste: Musik und Tanz mit Platzburschen und Platzmädeln, Sonntag und Montag (da und dort Dienstag), »kleine Kerwe« am nächsten Sonntag; Speisen: Reissuppe, Kraut mit Wurst, Braten mit Rosinbrühe.", "Crown of the rural house and village festivals: music and dancing with Platzburschen and Platzmädel, Sunday and Monday (here and there Tuesday), “small Kerwe” the following Sunday; dishes: rice soup, cabbage with sausage, roast with raisin sauce.", "188", "man der ganzen Concentration der Freudigkeit"),
    # --- October
    (10, 14, K, "brauch", "Burkhard: Beginn der Spinnstuben", "Burkhard: start of the spinning rooms", "Die Spinnstuben (Rockenstuben) beginnen, wenn der Flachs gebreckt ist, und dauern bis zum Tag vor Fastnacht; früher mit der Burkhardsgans.", "The spinning rooms begin when the flax has been broken and last until the day before Shrovetide; formerly with the Burkhard goose.", "181", "im Spätherbste um Burkhard"),
    (10, 16, G, "regel", "Gallus (16. Oktober)", "St Gall (16 October)", "»St. Gall läßt den Schnee fall«; im Wald werden Vogelherde und Geschneide hergerichtet.", "“St Gall lets the snow fall”; bird-traps and forest cuttings are set up.", "191", "St. Gall (Gallus, 16. October)"),
    (10, 18, G, "brauch", "18. Oktober (Völkerschlacht bei Leipzig)", "18 October (Battle of Leipzig)", "Gedenken an den Sieg bei Leipzig; nur die (meist städtische) Jugend feiert, teils mit Freudenfeuern.", "Commemoration of the victory at Leipzig; only the (mostly urban) youth celebrate it, in part with bonfires.", "191", "Die Feier des 18. Octobers"),
    (10, 28, K, "arbeit", "Simon Judä", "St Simon and Jude", "Der Bauer weicht vom Felde und beginnt das Huzengehn (Abendbesuche).", "The farmer leaves the field and begins the “Huzengehn” (evening visits).", "191", "Mit Simon Judä weicht der Bauer"),
    # --- November
    (11, 11, G, "brauch", "Martinstag (11. November)", "St Martin’s day (11 November)", "Martinsgans und Martinshörner, ursprünglich zu Ehren Wotans; Kinder bringen dem Lehrer eine Gans.", "Martin’s goose and Martin’s horns, originally in honour of Wotan; children bring their teacher a goose.", "191", "Am Martinstage (11. November)"),
    (11, 11, K, "speise", "Martini: Speise", "Martinmas: dish", "Eine Gans wird auf den Tisch gebracht und »geopfert«.", "A goose is brought to the table and “sacrificed”.", "161", "Martini eine Gans auf den Tisch"),
    (11, 11, G, "regel", "Martini: Witterung", "Martinmas: weather lore", "»Geht die Gans Martini auf dem Eis, so geht sie Weihnachten auf dem Dreck.«", "“If the goose walks on ice at Martinmas it walks in the muck at Christmas.”", "191", "Geht die Gans Martini auf dem Eis"),
    (11, 30, G, "orakel", "Andreastag (30. November)", "St Andrew’s day (30 November)", "Wichtigster Orakeltag der Mädchen: Bleigießen, Gänserich, Streuäste, Erbzaun, Hering mit Spruch; Eberesche (Thors Baum) in Wassertöpfen.", "The girls’ most important oracle day: lead-pouring, gander, brushwood twigs, pea fence, herring with a spell; rowan (Thor’s tree) in water pots.", "191", "Der 30. November, der Andreastag"),
    # --- December
    (12, 6, G, "brauch", "Nikolaus und Knecht Rupprecht (6. Dezember)", "St Nicholas and Knecht Rupprecht (6 December)", "Knecht Rupprecht prüft die Kinder; die gesitteten bekommen Äpfel und Nüsse, die ungesitteten die Drohung des Sacksteckens.", "Knecht Rupprecht tests the children; the well-behaved get apples and nuts, the naughty the threat of the sack.", "191", "am Niclastage (6. December)"),
    (12, None, M, "brauch", "Hausschlachten und Schlachtfest", "House slaughtering and slaughter feast", "Mit der Mitte des Dezembers beginnt das Hausschlachten; das Schlachtfest (»Krummbâ«) erinnert an das Juelopfer, Verwandte werden eingeladen.", "House slaughtering begins in mid-December; the slaughter feast (“Krummbâ”) recalls the Yule sacrifice, relatives are invited.", "192", "Mit der Mitte des Decembers hebt das Hausschlachten an"),
    (12, 21, G, "orakel", "Thomasnacht (21. Dezember) und die zwölf Nächte", "Thomas night (21 December) and the twelve nights", "Beginn der heiligen zwölf Nächte bis zum Dreikönigstag: Geisterwelt, Horchen auf Zeichen, Bleigießen, Zwiebelschalen-Wetter; Dreschen, Spinnen und Flachsbrechen ruhen.", "Start of the holy twelve nights up to Epiphany: spirit world, listening for signs, lead-pouring, onion-shell weather oracle; threshing, spinning and flax-breaking rest.", "192", "Die Thomasnacht (21. December)"),
    (12, 24, K, "speise", "Weihnachtsabend: Speise", "Christmas Eve: dish", "Rogener Hering mit Apfelsalat oder Hirsenmuß; zu Weihnachten Stollen und Pfefferkuchen.", "Herring with roe and apple salad or millet mush; stollen and gingerbread at Christmas.", "161", "muß Häring, und zwar rogener"),
    (12, 24, K, "brauch", "Christabend und Weihnachten", "Christmas Eve and Christmas", "Christmetten, Christbescheerung (Tannenbäumchen oder Kunstpyramide), in der Weihnachtswoche das Tängeln der Kinder und Burschen.", "Midnight services, giving of presents (fir tree or artificial pyramid), in Christmas week the “Tängeln” of children and lads.", "193", "Die am Weihnachtsabende oder am Morgen des Christtages"),
    (12, 24, K, "arbeit", "Christabend: Vieh", "Christmas Eve: livestock", "Das Vieh erhält »Leckig« (Salz und Körner); auch am Sylvester- und Walpurgisabend Körner oder Halmenasche gegen Verhexung.", "The cattle get “Leckig” (salt and grain); also on New Year’s Eve and Walpurgis eve grain or straw ash against bewitching.", "185", "Am Christabende erhält das Vieh"),
    (12, 25, K, "regel", "Weihnachten: Ernteregel", "Christmas: harvest lore", "»Helle Weihe, finstre Scheuer« (helle Weihnachten, volle Scheunen) gilt als Zeichen eines guten Erntejahres.", "“Bright Christmas, dark barn” (bright Christmas, full barns) is a sign of a good harvest year.", "186", "Helle Weihe, finstre Scheuer"),
    (12, 31, K, "orakel", "Silvesterabend", "New Year’s Eve", "Horchen auf Kreuzwegen, Bleigießen, Zwiebelschalen-Orakel; Anschießen des neuen Jahres, »Prost Neujahr!« nach dem Zwölfuhrschlag.", "Listening at crossroads, lead-pouring, onion-shell oracle; shooting in the new year, “Prost Neujahr!” after the stroke of twelve.", "193", "Der Sylvesterabend"),
]


def locate(page_label, phrase):
    p = page(page_label)
    hits = []
    for b in p["blocks"] + p["footnotes"]:
        t = text(page_label, b["id"])
        if phrase in t:
            hits.append(b["id"])
    assert hits, (page_label, phrase)
    assert len(hits) == 1, (page_label, phrase, hits)
    return hits[0]


rows = []
for i, (month, day, basis, kind, nd, ne, td, te, pg, ph) in enumerate(E, start=1):
    blk = locate(pg, ph)
    rows.append([i, month, MONTH_DE[month - 1], MONTH_EN[month - 1], day, basis, KINDS[kind]["de"], KINDS[kind]["en"], nd, ne, td, te, pg, blk])

# printed day check for entries with basis 'gedruckt'
import re
for r in rows:
    if r[5] == G and r[4] is not None:
        t = text(r[12], r[13])
        assert re.search(rf"\b{r[4]}\. ?(Jan|Febr|März|April|Mai|Juni|Juli|Aug|Sept|Oct|Nov|Dec)", t) or re.search(rf"ersten (März|April|Mai)", t) or "(" + str(r[4]) + ". " in t or f"{r[4]}. " in t, (r[8], r[4])

# same month/day/kind collisions
cnt = Counter((r[1], r[4], r[6]) for r in rows if r[4] is not None)
print("collisions:", [k for k, v in cnt.items() if v > 1])
print(len(rows), "entries")

kind_n = Counter(r[6] for r in rows)
print(kind_n)
month_n = Counter(r[1] for r in rows)
print(sorted(month_n.items()))
fixed = [r for r in rows if r[4] is not None]
movable = [r for r in rows if r[5] == B]
print(len(fixed), len(movable))
# winter-solstice cluster 21 Dec - 6 Jan
cluster = [r for r in fixed if (r[1] == 12 and r[4] >= 21) or (r[1] == 1 and r[4] <= 6)]
print("cluster", len(cluster), [(r[1], r[4]) for r in cluster])
# weather rules from 15 Jun to 24 Aug with printed day
sw = [r for r in rows if r[6] == KINDS["regel"]["de"] and r[4] is not None and ((r[1] == 6 and r[4] >= 15) or r[1] in (7,) or (r[1] == 8 and r[4] <= 24))]
print("summer saints' day rules", len(sw), [(r[1], r[4]) for r in sw])
regel_total = kind_n[KINDS["regel"]["de"]]
printed_days = [r for r in rows if r[5] == G]
print("printed days", len(printed_days))
top_months = month_n.most_common(4)
assert {k for k, v in month_n.items() if v == month_n[1]} == {1, 2, 5, 12} and month_n[4] == max(month_n.values())
print(top_months)
# month with printed day vs by name
nameday = [r for r in rows if r[5] in (G, K) and r[4] is not None]

refs = sorted({(r[12], r[13]) for r in rows}, key=lambda x: (int(x[0]), x[1]))
src_refs = [{"page": p, "block": b} for p, b in refs]
corr = {"page": "831", "block": "b5", "note": "Berichtigung zu S. 192: zwölf Nächte ab 21. oder 25. Dezember bis 6. Januar"}
assert "S. 192. Z. 15 v. u." in text("831", "b5")

dec = month_n[12]
n_regel_jul_aug = sum(1 for r in rows if r[6] == KINDS["regel"]["de"] and r[1] in (6, 7, 8))
print("regel jun-aug", n_regel_jul_aug)
n_speise = kind_n[KINDS["speise"]["de"]]

ana = {
    "id": "kultur-volkskalender-bauernjahr",
    "title": bi("Volkskalender: Bräuche, Regeln und Speisen im Jahreslauf", "Folk calendar: customs, lore and dishes through the year"),
    "category": "culture",
    "section": "t1-2-7",
    "sources": src_refs + [corr],
    "summary": bi(
        f"Brückner ordnet das Brauchtum des Landvolks im Abschnitt »Sitte und Brauch« nach dem Jahreslauf (»Volkskalender«, S. 188–193); dazu kommen Festspeisen (S. 161) und Arbeitsregeln (S. 185–187). Der Text wurde in {len(rows)} Einträge gegliedert: Bräuche, Wetter- und Ernteregeln, Landarbeit, Festspeisen sowie Orakel und Schutzzauber. Die Grafiken zeigen, in welchen Monaten sich diese Einträge häufen und auf welche Tage des Jahres sie fallen.",
        f"Brückner arranges the customs of the country people in the section “Sitte und Brauch” according to the course of the year (“Volkskalender”, pp. 188–193); added to this are feast-day dishes (p. 161) and rules of farm work (pp. 185–187). The text was broken down into {len(rows)} entries: customs, weather and harvest lore, farm work, feast dishes, and oracles and protective magic. The charts show in which months these entries cluster and on which days of the year they fall.",
    ),
    "method": bi(
        f"Der Fließtext wurde von Hand in Einträge gegliedert (je ein Brauch, eine Regel, eine Speise oder Arbeit an einem Tag oder Fest); Wortlaut und Absatz sind über Seite und Block belegt (die Zuordnung wurde per Skript an Schlüsselwörtern des Blocks geprüft). Der Tag ist nur bei {len(printed_days)} Einträgen gedruckt (Basis »gedruckt«); sonst steht der Kalendertag des genannten Festes (»Kalenderfest«, ergänzt nach dem kirchlichen Kalender), bei beweglichen Festen (Fastnacht, Ostern, Pfingsten u. a.) kein Tag, sondern der Monat, in dem Brückner sie behandelt. Die Einteilung in fünf Sorten ist eine Zuordnung des Bearbeiters.",
        f"The running text was broken down by hand into entries (one custom, rule, dish or task on one day or feast); wording and paragraph are documented by page and block (the assignment was checked by script against key phrases of the block). The day is printed for only {len(printed_days)} entries (basis “gedruckt”); otherwise the calendar day of the named feast is given (“Kalenderfest”, added from the church calendar), and for movable feasts (Shrovetide, Easter, Whitsun and others) no day but the month in which Brückner treats them. The division into five kinds is the analyst’s assignment.",
    ),
    "findings": [
        bi(
            f"April ist mit {month_n[4]} Einträgen der dichteste Monat (Gründonnerstag, Karfreitag und Ostern samt Speisen und Regeln); je {month_n[1]} Einträge entfallen auf Januar, Februar, Mai und Dezember, dagegen nur {month_n[3]} auf den März und {month_n[9]} auf den September. Zwischen 21. Dezember und 6. Januar liegen {len(cluster)} Einträge (Zwölf Nächte, Weihnachten, Neujahr, Dreikönig).",
            f"April is the densest month with {month_n[4]} entries (Maundy Thursday, Good Friday and Easter with dishes and lore); {month_n[1]} entries each fall on January, February, May and December, but only {month_n[3]} on March and {month_n[9]} on September. {len(cluster)} entries lie between 21 December and 6 January (Twelve Nights, Christmas, New Year, Epiphany).",
        ),
        bi(
            f"Von {kind_n[KINDS['regel']['de']]} Wetter- und Ernteregeln hängen {n_regel_jul_aug} an Tagen zwischen Juni und August (Veit, Johanni, Siebenschläfer, Mariä Heimsuchung, Margarethe, Jacobi, Laurentii, Bartholomäi): die Zeit, in der die Ernte entschieden wird.",
            f"Of {kind_n[KINDS['regel']['de']]} weather and harvest rules, {n_regel_jul_aug} are tied to days between June and August (Vitus, John, Seven Sleepers, Visitation, Margaret, James, Lawrence, Bartholomew): the time when the harvest is decided.",
        ),
        bi(
            f"{n_speise} Einträge betreffen Festspeisen mit festem Tag (Neujahr: Hirsenbrei, Fastnacht: Sauerkraut und Wurst, Karfreitag: Stockfisch, Ostern: Osterfladen, Pfingsten: Schinken, Martini: Gans, Weihnachtsabend: Hering); Brückner spricht von einer »Speiseordnung mit gebundenen und ungebundenen Tagen«.",
            f"{n_speise} entries concern feast-day dishes tied to a fixed day (New Year: millet porridge, Shrovetide: sauerkraut and sausage, Good Friday: stockfish, Easter: Osterfladen, Whitsun: ham, Martinmas: goose, Christmas Eve: herring); Brückner speaks of a “food order with bound and unbound days”.",
        ),
        bi(
            "Brückner deutet viele dieser Bräuche als Nachklänge germanischer und sorbischer Feiern (Sonnenwenden, Wotan, Thor, Hertha/Berchta); das ist seine Interpretation und wird hier nur wiedergegeben, nicht belegt.",
            "Brückner interprets many of these customs as echoes of Germanic and Sorbian festivals (solstices, Wotan, Thor, Hertha/Berchta); this is his interpretation and is reported here, not proved.",
        ),
    ],
    "caveats": [
        bi(
            "Die Einträge sind eine redaktionelle Gliederung von Prosa, keine Zählung von Bräuchen: Brückner nennt weit mehr Einzelheiten, mehrere Bräuche an einem Tag sind zu einem Eintrag zusammengefasst, und die Häufigkeit eines Monats hängt auch von der Ausführlichkeit seiner Darstellung ab.",
            "The entries are an editorial arrangement of prose, not a count of customs: Brückner names many more details, several customs on one day are merged into one entry, and the density of a month also depends on how fully he describes it.",
        ),
        bi(
            "Bewegliche Feste sind dem Monat zugeordnet, unter dem Brückner sie bespricht (z. B. Mitfasten unter Februar, Kirchweih unter Oktober); der tatsächliche Termin schwankt von Jahr zu Jahr. Der Tag des Todaustragens (1. März oder Lätare) und die Walpurgisnacht (Nacht zum 1. Mai) sind nach dem Text angesetzt. Für die Zwölf Nächte nennt die Berichtigung S. 831 als Beginn zuerst den 21., später den 25. Dezember; hier gilt der 21. Dezember (Thomasnacht).",
            "Movable feasts are assigned to the month under which Brückner discusses them (e.g. mid-Lent under February, Kirchweih under October); the actual date varies from year to year. The day of the carrying-out of Death (1 March or Laetare) and Walpurgis Night (eve of 1 May) are set according to the text. For the Twelve Nights the correction on p. 831 gives first 21 and later 25 December as the start; 21 December (Thomas night) is used here.",
        ),
        bi(
            "Tage ohne Druckangabe (Kalenderfest) sind ergänzt: Vincenttag 22. Januar, Pankratius 12. Mai, Burkhard 14. Oktober, Simon Judä 28. Oktober; die 100. Tage des Jahres (Gerstensaat) fällt auf den 10. April (Nichtschaltjahr). Alle diese Spalten sind als berechnet gekennzeichnet.",
            "Days without a printed date (Kalenderfest) are supplied: St Vincent 22 January, Pancras 12 May, Burkhard 14 October, Simon and Jude 28 October; the 100th day of the year (barley sowing) falls on 10 April (non-leap year). The day column is flagged as derived throughout.",
        ),
    ],
    "datasets": [
        {
            "name": "calendar",
            "title": bi("Volkskalender: Einträge", "Folk calendar: entries"),
            "columns": [
                {"name": "id", "label": bi("Nr.", "No."), "type": "integer", "unit": None, "derived": True},
                {"name": "month", "label": bi("Monat (Nummer)", "Month (number)"), "type": "integer", "unit": None, "derived": True, "note": "Monatsnummer 1–12; bei beweglichen Festen der Monat, unter dem Brückner sie behandelt"},
                {"name": "month_de", "label": bi("Monat (de)", "Month (de)"), "type": "string", "unit": None, "derived": True},
                {"name": "month_en", "label": bi("Monat (en)", "Month (en)"), "type": "string", "unit": None, "derived": True},
                {"name": "day", "label": bi("Tag im Monat", "Day of the month"), "type": "integer", "unit": None, "derived": True, "note": "nur bei 'gedruckt' im Text genannt, sonst Kalendertag des Festes (ergänzt); leer bei beweglichen Festen und Monatsregeln"},
                {"name": "date_basis", "label": bi("Datierung", "Dating basis"), "type": "string", "unit": None, "derived": True, "note": "gedruckt | Kalenderfest | berechnet | beweglich | Monat"},
                {"name": "kind_de", "label": bi("Sorte (de)", "Kind (de)"), "type": "string", "unit": None, "derived": True},
                {"name": "kind_en", "label": bi("Sorte (en)", "Kind (en)"), "type": "string", "unit": None, "derived": True},
                {"name": "name_de", "label": bi("Tag / Anlass (de)", "Day / occasion (de)"), "type": "string", "unit": None},
                {"name": "name_en", "label": bi("Tag / Anlass (en)", "Day / occasion (en)"), "type": "string", "unit": None},
                {"name": "note_de", "label": bi("Brauch (de)", "Custom (de)"), "type": "string", "unit": None},
                {"name": "note_en", "label": bi("Brauch (en)", "Custom (en)"), "type": "string", "unit": None},
                {"name": "page", "label": bi("Seite", "Page"), "type": "string", "unit": None},
                {"name": "block", "label": bi("Block", "Block"), "type": "string", "unit": None},
            ],
            "rows": rows,
            "source_refs": src_refs,
        }
    ],
    "charts": [
        {
            "id": "c1",
            "dataset": "calendar",
            "title": bi("Einträge des Volkskalenders je Monat", "Entries of the folk calendar per month"),
            "caption": bi(
                "Zahl der Einträge je Monat, nach Sorte (bewegliche Feste im Monat, unter dem Brückner sie behandelt). Die Winterfeste um Weihnachten und Neujahr, die Ostertage und der Hochsommer sind am dichtesten besetzt.",
                "Number of entries per month, by kind (movable feasts in the month under which Brückner treats them). The winter feasts around Christmas and New Year, Easter week and high summer are the most densely occupied.",
            ),
            "vegalite": {
                "height": 300,
                "mark": "bar",
                "encoding": {
                    "x": {"field": {"de": "month_de", "en": "month_en"}, "type": "ordinal", "sort": {"field": "month", "op": "min"}, "title": None, "axis": {"labelAngle": 0}},
                    "y": {"aggregate": "count", "type": "quantitative", "title": bi("Einträge", "Entries"), "axis": {"tickMinStep": 1}},
                    "color": {"field": {"de": "kind_de", "en": "kind_en"}, "type": "nominal", "title": None, "scale": {"domain": [KINDS[k] for k in KINDS]}, "legend": {"labelLimit": 400, "columns": 3}},
                    "tooltip": [
                        {"field": {"de": "month_de", "en": "month_en"}, "title": bi("Monat", "Month")},
                        {"field": {"de": "kind_de", "en": "kind_en"}, "title": bi("Sorte", "Kind")},
                        {"aggregate": "count", "title": bi("Einträge", "Entries")},
                    ],
                },
            },
        },
        {
            "id": "c2",
            "dataset": "calendar",
            "title": bi("Der Festkalender im Jahreslauf", "The calendar of feasts through the year"),
            "caption": bi(
                "Jeder Punkt ist ein Eintrag mit festem Kalendertag; die Zeile gibt den Monat an, die Lage den Tag, die Farbe die Sorte. Bewegliche Feste sind nicht eingetragen. Gebündelte Punkte (24./25. Dezember, 11. November, 2. Februar) zeigen Tage, an denen sich mehrere Bräuche überlagern.",
                "Each dot is an entry with a fixed calendar day; the row gives the month, the position the day, the colour the kind. Movable feasts are not shown. Clustered dots (24/25 December, 11 November, 2 February) show days on which several customs overlap.",
            ),
            "vegalite": {
                "height": 420,
                "transform": [{"filter": "datum.day != null"}],
                "mark": {"type": "point", "filled": True, "size": 45, "opacity": 0.95},
                "encoding": {
                    "y": {"field": {"de": "month_de", "en": "month_en"}, "type": "ordinal", "sort": {"field": "month", "op": "min"}, "title": None},
                    "yOffset": {"field": "kind_de", "sort": [KINDS[k]["de"] for k in KINDS]},
                    "x": {"field": "day", "type": "quantitative", "title": bi("Tag im Monat", "Day of the month"), "scale": {"domain": [0, 32]}, "axis": {"values": [1, 5, 10, 15, 20, 25, 30], "format": "d"}},
                    "color": {"field": {"de": "kind_de", "en": "kind_en"}, "type": "nominal", "title": None, "scale": {"domain": [KINDS[k] for k in KINDS]}, "legend": {"labelLimit": 400, "columns": 3}},
                    "tooltip": [
                        {"field": {"de": "name_de", "en": "name_en"}, "title": bi("Anlass", "Occasion")},
                        {"field": {"de": "note_de", "en": "note_en"}, "title": bi("Brauch", "Custom")},
                        {"field": "day", "title": bi("Tag", "Day")},
                        {"field": {"de": "month_de", "en": "month_en"}, "title": bi("Monat", "Month")},
                        {"field": "page", "title": bi("Seite", "Page")},
                    ],
                },
            },
        },
    ],
    "transcription_issues": [],
    "keywords": {
        "de": ["Volkskalender", "Brauchtum", "Feste", "Bauernregeln", "Wetterregeln", "Festspeisen", "Johannisfeuer", "Walpurgisnacht", "Zwölf Nächte", "Kirchweih"],
        "en": ["folk calendar", "customs", "festivals", "weather lore", "peasant rules", "feast dishes", "St John’s fires", "Walpurgis Night", "twelve nights", "church fair"],
    },
    "related": [],
    "generated_by": GEN,
    "date": DATE,
}
write(ana)
