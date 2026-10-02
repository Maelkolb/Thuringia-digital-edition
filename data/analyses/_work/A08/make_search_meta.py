# -*- coding: utf-8 -*-
"""Builds data/search/pages/A08.json (pages 119-207). Page entries live in search_pages_1/2.py."""
import json
from pathlib import Path
from search_pages_2 import P

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "data" / "search" / "pages" / "A08.json"

G = []


def g(term, kind, de, en, pages, variants=None):
    G.append({"term": term, "variants": variants or [], "kind": kind, "de": de, "en": en, "pages": pages})


# --- terms and institutions (Wohnliche Einrichtung)
g("Sorben", "term", "Slawischer Volksstamm (Wenden), der das Land vor der deutschen Kolonisation bewohnte; Brückner rechnet ihn nach Schleicher zu den elbslawischen (polabischen) Stämmen.", "Slavic people (Wends) who inhabited the land before German colonisation; Brückner, following Schleicher, counts them among the Elbe-Slavic (Polabian) tribes.", ["119", "120", "123", "162", "196"], ["Sorbe", "sorbisch", "Wenden"])
g("Rundling", "term", "Geschlossene sorbische Dorfform: die Höfe stehen hufeisenförmig um einen Anger mit Teich, mit nur einem Ausgang (Sackgasse).", "Closed Sorbian village form: the farms stand in a horseshoe around a green with a pond, with a single exit (dead-end lane).", ["123"])
g("Hofraithe", "term", "Gehöft eines Bauern (Hofreite) mit Wohnhaus, Stallungen, Scheune und Hof.", "A farmer’s farmstead (Hofreite) with dwelling, stables, barn and yard.", ["123", "127", "130", "131"], ["Hofraithen"])
g("Schrotbau", "term", "Blockbau aus horizontal aufeinandergelegten Balken, die älteste Bauweise des Bauernhauses; später durch Fachbau (Fachwerk) und Massivbau abgelöst.", "Log construction of horizontally stacked timbers, the oldest form of the farmhouse; later replaced by half-timbering (Fachbau) and masonry.", ["128", "129"], ["Fachbau"])
g("Hintersiedler", "term", "Besitzloser Dörfler mit kleinem Haus ohne Hof, Stall und Scheune, lebt von Taglohn und Handwerk (auch Kleinhäusler, Häusler).", "Landless villager with a small house without yard, stable or barn, living from day labour and crafts (also Kleinhäusler, Häusler).", ["126", "128", "165"], ["Kleinhäusler", "Häusler"])
g("Stammgemeinde", "institution", "Engere Ortsgemeinde der alten Hofbesitzer (auch Brau- oder alte Gemeinde), allein am Gemeindegrundbesitz beteiligt.", "The narrower village commune of the old farm owners (also brewing or old commune), alone entitled to the communal land.", ["126"], ["alte Gemeinde", "Brau-Gemeinde"])
g("Patrimonialgericht", "institution", "Gutsherrliche Gerichtsbarkeit: der Rittergutsbesitzer übte Ortspolizei sowie niedere (oft auch höhere) Gerichtsbarkeit aus.", "Manorial jurisdiction: the lord of the manor exercised local policing and low (often also high) justice.", ["126"], ["Patrimonialgerichtsorte"])
g("Schulze", "office", "Dorfvorsteher (Bauermeister) der bäuerlichen Gemeinden; auch der Ortsrichter im Patrimonialgericht.", "Village head (Bauermeister) of the peasant communes; also the local judge in a patrimonial court.", ["126"], ["Bauermeister"])
g("Vierleute", "office", "Kontrollorgan neben der dörflichen Gemeindeverwaltung (in Städten die Stadtverordneten mit Viertelsmeistern), im späten Mittelalter eingeführt.", "Supervisory body alongside the village administration (in towns the councillors with district masters), introduced in the late Middle Ages.", ["127"])
g("Kammergut", "term", "Landesherrliches Gut (Domäne); an der Stelle alter Vasallenburgen liegen Kammergutsgebäude.", "Princely estate (domain); the buildings of Kammergüter stand on the sites of old vassal castles.", ["137"], ["Kammergutsgebäude"])
g("Rittergut", "term", "Adliges Gut mit Gerichts- und Polizeirechten; seine Besitzer saßen auf Burgen und Herrenhäusern, bis später der Boden zerschlagen wurde.", "Noble estate with rights of jurisdiction and policing; its owners lived in castles and manor houses until the land was later broken up.", ["126", "137"], ["Rittergüter"])
g("Latzschürze", "term", "Schürze mit Brustlatz, von Männern und Frauen getragen; im Oberland vorwiegend blau, Grundform der voigtländischen Tracht.", "Bib apron worn by men and women; in the Oberland mostly blue, a basic form of Voigtland costume.", ["155", "156"], ["Latzschürzen"])
g("Nesthaube", "term", "Kunstvoll gearbeitete Frauenhaube mit langen Bändern der älteren Tracht.", "Elaborately made woman’s cap with long ribbons of the older costume.", ["155"], ["Nesthauben"])
g("Eimer", "unit", "Hohlmaß, besonders für Bier; in Gera 72 Kannen = 0,6870 hl, in Schleiz und Tanna 0,6183 hl, in Lobenstein 0,6435 hl (S. 832). Brückner: im reußischen Unterland noch nicht zwei Eimer Bier je Person und Jahr.", "Measure of capacity, especially for beer; at Gera 72 Kannen = 0.6870 hl, at Schleiz and Tanna 0.6183 hl, at Lobenstein 0.6435 hl (p. 832). Brückner: in the Reuss Unterland not yet two Eimer of beer per person and year.", ["160"])
g("Elle", "unit", "Längenmaß, örtlich verschieden: in Gera 0,572394 m, in Schleiz, Tanna und Hohenleuben 0,565311 m, in Saalburg 0,606531 m (S. 831).", "Unit of length, varying locally: at Gera 0.572394 m, at Schleiz, Tanna and Hohenleuben 0.565311 m, at Saalburg 0.606531 m (p. 831).", ["137"], ["Ellen"])
g("Fuß", "unit", "Längenmaß; Brückners Baufuß (leipziger Werkmaß) = 0,282655 m, 12 Zoll; die Körpergröße der Rekruten ist in sächsischem Fuß und Zoll angegeben (5′ 7″ ≈ 158 cm).", "Unit of length; Brückner’s building foot (Leipzig work measure) = 0.282655 m, 12 inches; recruits’ body height is given in Saxon feet and inches (5′ 7″ ≈ 158 cm).", ["137", "162", "173"], ["Zoll", "sächsisches Maß"])
g("Thlr.", "currency", "Thaler, Münzeinheit; in Tanna werden jährlich mindestens 150 Thlr. an Gerichtskosten und Advokatengebühren für Injurienklagen ausgegeben.", "Thaler, monetary unit; at Tanna at least 150 Thlr. a year are spent on court costs and lawyers’ fees for libel suits.", ["166"], ["Thaler", "Thlr"])
g("Güll'n", "currency", "Dialektform für Gulden (in der Erzählung von Waltersdorf: »en pör'n Güll'n«, ein paar Gulden).", "Dialect form of Gulden (in the Waltersdorf story: “en pör’n Güll’n”, a few guilders).", ["146"], ["Gulden"])
g("Ersatzreserve", "institution", "Reserve, in die zeitweilig Untaugliche eingestellt werden; Ende 1867 betraf das 193 von 1778 Militärpflichtigen.", "Reserve into which the temporarily unfit are placed; at the end of 1867 this concerned 193 of 1778 conscripts.", ["173"])
g("Friedensrichter", "office", "Richter für die Schlichtung von Streitigkeiten; Brückner: 1864 im Justizamt Schleiz nur 60 Sachen vor Friedensrichtern gegenüber über 800 Zivil- und Injurienklagen.", "Justice of the peace for settling disputes; Brückner: in 1864 only 60 cases before justices of the peace in the judicial office of Schleiz against over 800 civil and libel suits.", ["166"], ["Friedensgerichte"])
g("Erbkürrecht", "term", "Wahlrecht des Vaters, einen Erben zu bestimmen; üblich ist der jüngste Sohn als Kürerbe (Bauernminorat), der die Geschwister abfindet.", "The father’s right to choose an heir; usually the youngest son is the chosen heir (peasant minorat) and pays off his siblings.", ["193", "194"], ["Kürerbe", "Bauernminorat"])
g("Schröpfen", "term", "Volksheilverfahren: Blutentzug mit Schröpfköpfen, zusammen mit dem Aderlass noch ein- bis zweimal im Jahr üblich.", "Folk therapy: drawing blood with cupping glasses, together with bloodletting still customary once or twice a year.", ["174"], ["Aderlass"])
g("Johannisblume", "term", "Arnika (Arnica montana); das am meisten verehrte Hausmittel, im Oberland korbweise gesammelt und trocken oder in Spiritus aufbewahrt.", "Arnica (Arnica montana); the most revered household remedy, gathered by the basket in the Oberland and kept dry or in spirits.", ["174", "190"])
g("Pröpelweib", "term", "Kluge Frau, die mit Murmeln und sympathetischen Mitteln heilt (zu dialektal pröpeln = murmeln, Sympathie treiben).", "Wise woman who heals with muttering and sympathetic means (from dialect pröpeln = to mutter, practise sympathetic magic).", ["153", "174"], ["Pröpelweiber", "Pröpeln"])
g("Platzbursche", "term", "Zum Kirchweihfest gehörender, mit Sträußen geschmückter ehrbarer Bursche, der mit seinem Platzmädle die ersten Reihen tanzt; an der Spitze der Platzmeister.", "Respectable young man belonging to the church-fair festivities, decorated with posies, who dances the first rounds with his Platzmädle; headed by the Platzmeister.", ["188"], ["Platzmädle", "Platzmeister"])
g("Kirchweih", "term", "Kirchweihfest (Kirmes, Kirmst, Kirwe, Kerwä), Krone der ländlichen Haus- und Dorffeste, im September/Oktober nach der Ernte.", "Church-dedication fair (Kirmes, Kirmst, Kirwe, Kerwä), crown of the rural house and village festivals, held in September/October after the harvest.", ["187", "188"], ["Kirmes", "Kerwe"])
g("Sichelhahn", "term", "Schmaus und Tanz, den der Grundherr den Schnittern nach beendeter Ernte gibt.", "Feast and dance given by the landlord to the reapers when the harvest is finished.", ["187"])
g("Rockenstube", "term", "Spinnstube: abendliche Zusammenkunft der jungen Leute zum Spinnen im Winterhalbjahr (von Burkhard bis Fastnacht), Ort von Liedern, Rätseln und Freien.", "Spinning room: evening gathering of young people for spinning in the winter half year (from Burkhard to Shrovetide), a place of songs, riddles and courting.", ["166", "181", "189"], ["Spinnstube", "Rockenstuben"])
g("Hochzeitbitter", "office", "Festordner der großen Hochzeit: lädt eine Woche vorher mit Gruß und Rede die Gäste (seidenes Tuch, rotbebänderter Stock) und leitet Zug und Mahl.", "Master of ceremonies of the large wedding: invites the guests a week earlier with greeting and speech (silk cloth, red-ribboned stick) and directs procession and meal.", ["182", "183"])
g("Kammerwagen", "term", "Wagen, der die Ausstattung und die Braut in das Haus des Bräutigams holt.", "Wagon that fetches the trousseau and the bride to the bridegroom’s house.", ["183"])
g("Todaustragen", "term", "Frühlingsbrauch (1. März oder Lätare): eine Strohpuppe wird umhergetragen und ins Wasser geworfen, um den Winter und den Tod auszutreiben.", "Spring custom (1 March or Laetare): a straw puppet is carried around and thrown into the water to drive out winter and death.", ["184", "189"], ["Todaustreiben", "Todausbringen"])
g("Werre", "term", "Weibliche Gestalt der Volksmythe (Berchta, Holle), die in den Zwölf Nächten Häuser und Spinnerinnen prüft; am Werre- oder Holla-Abend (Dreikönigsabend) isst man Polse.", "Female figure of folk myth (Berchta, Holle) who inspects houses and spinners in the Twelve Nights; on Werre or Holla evening (Epiphany eve) Polse is eaten.", ["161", "185", "206"], ["Berchta", "Holla", "Holle"])
g("Bilmesschneider", "term", "Feldgeist oder zaubernder Bauer, der um Johanni mit dreieckigem Hütchen und Sichelscheren an den Füßen durch das Getreide schreitet und halbe Erträge an sich zieht.", "Field spirit or sorcerer-farmer who strides through the grain around St John’s Day with a three-cornered hat and sickle-shears on his feet and draws off half the yield.", ["187", "206"], ["Bilsenschneider", "Bilwitz"])
g("Wiedenheer", "term", "Wütendes Heer; Wotans Nachtjagd mit Hunden, Raben, Hexen und verdammten Seelen in den Zwölf Nächten.", "The raging host; Wotan’s night hunt with dogs, ravens, witches and damned souls during the Twelve Nights.", ["202"], ["wütendes Heer", "wilde Jagd"])
g("Hausotter", "term", "Sanfter, milchfressender Hausgeist unter der Türschwelle, glückbringend; man weiht ihm Milchgeschirre.", "Gentle, milk-drinking house spirit under the threshold, bringing luck; milk vessels are dedicated to it.", ["178"])
g("Hebeschmaus", "term", "Festmahl des Bauherrn für die Bauleute nach dem Aufrichten (Heben) eines neuen Hauses.", "Feast given by the builder to the workmen after the raising of a new house.", ["152", "178"])
g("Kühtanz", "term", "Flurname und Sagenplatz, an dem die Hexen nach dem Gelage ihren Kuhtanz halten; viele Kuhtanzplätze gelten als verrufen.", "Field name and legend site where the witches hold their cow dance after their carousal; many Kuhtanz places have a bad name.", ["203", "204"], ["Kuhtanz"])
g("Hankermann", "term", "Feuriger Irrlichtgeist, der auf einer Sumpfwiese zwischen Otticha, Wüstfalke und Loitsch zur Riesengestalt anwächst und Menschen begleitet.", "Fiery will-o’-the-wisp spirit that grows into a giant figure on a marshy meadow between Otticha, Wüstfalke and Loitsch and accompanies people.", ["203"])
# --- dialect words
g("Druid", "dialect", "Alp, ein böses Wesen, das die Menschen im Schlafe quält (zu Druden).", "Nightmare spirit, an evil being that torments people in their sleep (see Druden).", ["152", "197", "204"], ["Druden", "Drude"])
g("Büßen", "dialect", "Übel durch magische Mittel entfernen (ähnlich Söhnen, Sühnen).", "To remove ills by magical means (similar to Söhnen, Sühnen).", ["152", "154"], ["Söhnen", "sühnen"])
g("Eignen sich", "dialect", "Gespenstiges Vorzeichen eines Todesfalles.", "Spectral omen of a death.", ["152"])
g("Gutermuth", "dialect", "Kindtaufe (auch das Taufmahl).", "Christening.", ["152"])
g("Pimpelmutter", "dialect", "Hebamme.", "Midwife.", ["153"])
g("Polse", "dialect", "Pfannengebäck aus gekochten oder grün geriebenen Kartoffeln bzw. Mehl; Fastengericht des Werre-Abends (auch Pampus, Pfannenpolse, Bröckelpols, Gießklos).", "Pan-baked dish of boiled or raw grated potatoes or flour; the Werre-evening dish (also Pampus, Pfannenpolse, Bröckelpols, Gießklos).", ["152", "153", "154", "158", "161", "187"], ["Pfannenpolse", "Pampus", "Bröckelpols", "Gießklos", "Zotelklos"])
g("Käsehitsche", "dialect", "Kinderschlitten.", "Child’s sledge.", ["153"])
g("Lih", "dialect", "Kienlichtpfanne; in der alten Stube brannten Holzspäne in einer Pfanne (Lihe) unter einem Tonhut (Lihhut).", "Pan for pine-wood light; in the old living room wood splints burned in a pan (Lihe) under a clay hood (Lihhut).", ["128", "153"], ["Lihe", "Lihhut"])
g("Höhlerbier", "dialect", "Lagerbier (aus dem Höhler, dem Felsenkeller).", "Lager beer (from the Höhler, the rock cellar).", ["153", "160"], ["Höhler"])
g("Huzen gehn", "dialect", "Besuche ohne Arbeit machen (im Gegensatz zu ze Rocken gehn, Besuche mit Arbeit); Beginn der Winterabende nach Simon Judä.", "To pay visits without work (as opposed to ze Rocken gehn, visits with work); begins in winter evenings after Simon and Jude.", ["153", "188", "191"], ["Hutzengehn", "ze Rocken gehn"])
g("Unternächte", "dialect", "Die heiligen zwölf Nächte.", "The holy twelve nights.", ["154", "192"], ["Zwölf Nächte", "zwölf Nächte"])
g("Trauerbrod", "dialect", "Leichenschmaus (zu Leichenessen, Mahlzeit bei Beerdigungen).", "Funeral feast (see Leichenessen, meal at burials).", ["153", "154", "195"], ["Leichenessen"])
g("Bornkinnel", "dialect", "Christkind; auch Name der wundertätigen Marienpuppe von Untermhaus.", "The Christ child; also the name of the miracle-working Mary doll of Untermhaus.", ["152", "201"], ["Bornkindel"])
g("Koller", "dialect", "Jacke oder Weste der Bauerntracht (Goller).", "Jacket or waistcoat of peasant costume (Goller).", ["153", "155", "156"], ["Goller"])
g("Kopfsättel", "dialect", "Kopftuch der Weiber.", "Women’s headscarf.", ["153"])
g("Präßläber", "dialect", "Wurst (Preßleberwurst).", "Sausage (pressed liver sausage).", ["149", "153"])
g("Mutz", "dialect", "Quark, Käse (auch Steifmatz).", "Curd cheese, cheese (also Steifmatz).", ["153", "154"], ["Steifmatz"])
g("Starken", "dialect", "Die Kalben (junge Kühe).", "Heifers (young cows).", ["154"])
g("Zenst", "dialect", "Längs; Zenstweck: stets (so in der Sprachprobe von Tanna).", "Along; Zenstweck: always (as in the Tanna dialect sample).", ["150", "154"], ["Zenstweck"])
g("Nauthem", "dialect", "Athem (Atem); in Tanna: »m'r sicht 'n Náuthem« (man sieht den Atem).", "Breath; at Tanna: “m’r sicht ’n Náuthem” (one sees one’s breath).", ["150", "153"])
g("Weißpfiferet", "dialect", "Blaß, bleich.", "Pale.", ["150", "154"])
g("Gälle", "dialect", "Nicht wahr? (Frageanhängsel).", "Isn’t it? (tag question).", ["148", "152"], ["gelt"])
g("Hadgeh", "dialect", "Gruß beim Abschied (aus Adieu, mit Aspiration).", "Parting greeting (from adieu, with aspiration).", ["142", "148"], ["Hadgeh", "Hadgeh!"])
g("Schwinden", "dialect", "Volkskrankheitsname für trockene Hautausschläge (Flechten); bei Brückner auch Auszehrung für Schwindsucht.", "Folk disease name for dry skin eruptions (lichens); in Brückner also consumption (Auszehrung) for pulmonary tuberculosis.", ["154", "173"], ["Auszehrung"])
g("Brand", "dialect", "Volksname für tödliche Entzündungskrankheiten (tödlicher Ausgang akuter Krankheiten).", "Folk name for fatal inflammatory diseases (fatal outcome of acute diseases).", ["152", "173"])
g("Friesel", "dialect", "Volksname für Scharlach, Masern und alle durch Röthe oder Flecken der Haut gekennzeichneten Krankheiten.", "Folk name for scarlet fever, measles and all diseases marked by redness or spots on the skin.", ["172", "173"])
g("Zehrwurm", "dialect", "Mitesser; eingebildeter Krankheitswurm der Volksmedizin (neben Herzwurm und Fingerwurm).", "Blackhead; imagined disease worm of folk medicine (alongside heart worm and finger worm).", ["152", "154", "173"], ["Herzwurm", "Fingerwurm"])
g("Unkraut", "dialect", "In der Mundart: Epilepsie (auch »böses Wesen«); sonst Gleichnisunkraut.", "In dialect: epilepsy (also “böses Wesen”); otherwise the weeds of the parable.", ["154", "173"], ["böses Wesen"])

pages = sorted(P, key=lambda p: int(p["page"]))
doc = {"package": "A08", "pages": pages, "glossary": G}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
print(OUT, len(pages), "pages", len(G), "glossary terms")
