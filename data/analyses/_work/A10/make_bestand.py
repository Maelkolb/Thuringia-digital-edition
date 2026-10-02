"""A10: Gruben und Huettenwerke des Oberlandes vor dem Dreissigjaehrigen Krieg (pp. 242-244)."""
import sys
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\A10")
from common import *

# verify the numbers directly against the canonical grid -------------------------------------------
g = grid("243", "b4")
assert [r[0] for r in g[1:]] == ["Schleiz:", "Saalburg:", "Lobenstein:"]
assert g[1][1].startswith("2 Silbergruben") and g[1][2].startswith("4 Antimongruben") and g[1][4].startswith("126 Eisen")
assert g[2][1].startswith("1 Goldgrube") and g[2][4].startswith("10 Kupfer") and g[2][5].startswith("60 Eisen")
assert g[3][1].startswith("3 Silbergr") and g[3][2].startswith("3 Kupfergr") and g[3][3].startswith("2 Blei") and g[3][4].startswith("3 Alaun") and g[3][5].startswith("133 Eisen")
h = grid("244", "b1")
assert h[1][0].startswith("Schleiz") and h[1][1].startswith("2 Schmelz") and h[1][2].startswith("3 Hammer") and h[1][3].startswith("1 Alaunh") and h[1][4].startswith("1 Pulver")
assert h[2][1].startswith("3 Kupfer") and h[2][2].startswith("3 Alaun") and h[2][3].startswith("über 10 Hammer")

SCH, SAAL, LOB = "Schleiz", "Saalburg", "Lobenstein"
EI, KU, AGB, SB, GZ, AL = "Eisen", "Kupfer", "Silber, Blei", "Antimon", "Gold, Zinn", "Alaun"
GROUP_ORDER = [EI, KU, AGB, SB, GZ, AL]
GROUP_EN = {EI: "Iron", KU: "Copper", AGB: "Silver, lead", SB: "Antimony", GZ: "Gold, tin", AL: "Alum"}
# district, printed ore, group, kind, count, names, row
G = [
    (SCH, "Silbergruben", AGB, "Grube", 2, "St. Katharina am Schloßberg bei Schleiz; Gotthilf bei Löhma", "r2"),
    (SCH, "Antimongruben", SB, "Grube", 4, "bei Oberböhmsdorf; bei Weckersdorf; Trau auf Gott am Lössauer Wege; am Wolfsgalgen", "r2"),
    (SCH, "Eisengruben", EI, "Grube", 126, "", "r2"),
    (SAAL, "Goldgrube", GZ, "Grube", 1, "bei Zollgrün (nach der Volkssage weitere Goldgruben)", "r3"),
    (SAAL, "Gold- und Zinnseife", GZ, "Seife", 1, "an der Wettera bei Gräfenwarth", "r3"),
    (SAAL, "Silber- und Kupfergrube", AGB, "Grube", 1, "zu Thramitz zwischen Raila und Glücksthalhammer", "r3"),
    (SAAL, "Kupfergruben", KU, "Grube", 10, "", "r3"),
    (SAAL, "Eisengruben", EI, "Grube", 60, "", "r3"),
    (LOB, "Silbergruben", AGB, "Grube", 3, "Fortuna bei der Zschachenmühle; Heinrichs- und Luisenglück bei Gahma; Silberschlössel bei Weitisberga", "r4"),
    (LOB, "Kupfergruben", KU, "Grube", 3, "Kaiser Siegmund im Saalwald; Kupferplatte bei Harra; Schütz bei Pottiga", "r4"),
    (LOB, "Blei- und Silbergruben", AGB, "Grube", 2, "Kluft bei Harra; Bleistollen am Muckenberg", "r4"),
    (LOB, "Alaunerzgruben", AL, "Grube", 3, "bei Haueisen; Zoppothen an der Saale; bei der Pempelsmühle; schon 1550 erwähnt", "r4"),
    (LOB, "Eisengruben", EI, "Grube", 133, "darunter fünf Gruben mit Wasser- und Roßkünsten", "r4"),
]
gruben = [[d, ore, grp, kind, n, names, "S. 243 b4 " + row] for d, ore, grp, kind, n, names, row in G]
tot = sum(r[4] for r in gruben)
by_d = {d: sum(r[4] for r in gruben if r[0] == d) for d in (SCH, SAAL, LOB)}
eisen = sum(r[4] for r in gruben if r[2] == EI)
eisen_d = {d: sum(r[4] for r in gruben if r[0] == d and r[2] == EI) for d in (SCH, SAAL, LOB)}
non = {d: by_d[d] - eisen_d[d] for d in by_d}
non_tot = sum(non.values())
print(tot, by_d, eisen, eisen_d, non, non_tot)
eisen_share = eisen / tot * 100

# works ---------------------------------------------------------------------------------------
HW = [("Schleiz mit Saalburg", "Schmelzhütten", 2, "r2"), ("Schleiz mit Saalburg", "Hammerwerke", 3, "r2"), ("Schleiz mit Saalburg", "Alaun-/Vitriolwerke", 1, "r2"),
      ("Schleiz mit Saalburg", "Pulvermühlen", 1, "r2"), ("Lobenstein", "Schmelzhütten", 3, "r3"), ("Lobenstein", "Hammerwerke", 10, "r3"), ("Lobenstein", "Alaun-/Vitriolwerke", 3, "r3")]
huetten = [[d, t, n, "S. 244 b1 " + r] for d, t, n, r in HW]
n_s = sum(n for d, t, n, r in HW if d.startswith("Schleiz"))
n_l = sum(n for d, t, n, r in HW if d == "Lobenstein")
print(n_s, n_l)

# chronicle --------------------------------------------------------------------------------------
URK, VO, FO, GW = "Urkunde, Privileg", "Verordnung", "Vertrag, Förderung", "Gewerkschaften"
KIND_EN = {URK: "Record, privilege", VO: "Decree", FO: "Contract, promotion", GW: "Mining companies"}
CH = [
    (1318, None, URK, "Silbergruben bei Schleiz erwähnt", "Silver mines near Schleiz mentioned", "S. 242 b4"),
    (1323, None, URK, "Reichsvoigte von Kaiser Ludwig mit dem Bergbauregal begnadigt", "Imperial bailiffs granted the mining regalia by Emperor Louis", "S. 242 b4"),
    (1327, None, URK, "Reichsvoigte erneut mit dem Bergbauregal begnadigt", "Imperial bailiffs again granted the mining regalia", "S. 242 b4"),
    (1329, None, URK, "Reichsvoigte erneut mit dem Bergbauregal begnadigt", "Imperial bailiffs again granted the mining regalia", "S. 242 b4"),
    (1371, None, URK, "Eisengruben und Hammerwerk bei Blankenberg bestehen", "Iron mines and a hammer works exist near Blankenberg", "S. 242 b4"),
    (1502, None, FO, "Vertrag mit Nürnberger Handelsherren: 500 Ctr. Garkupfer zu 19 Gulden", "Contract with Nuremberg merchants: 500 Ctr. of refined copper at 19 gulden", "S. 243 b1"),
    (1530, None, VO, "Verordnung zur Förderung des Bergbaus", "Decree promoting mining", "S. 242 b5, S. 243 b1"),
    (1551, None, VO, "Verordnung zur Förderung des Bergbaus", "Decree promoting mining", "S. 242 b5, S. 243 b1"),
    (1563, None, FO, "Burggraf Heinrich VII. fördert die Stahlhütten an der Saale mit 20.000 Thalern", "Burgrave Heinrich VII promotes the steelworks on the Saale with 20,000 thalers", "S. 243 b1"),
    (1566, None, VO, "Verordnung zur Förderung des Bergbaus", "Decree promoting mining", "S. 242 b5, S. 243 b1"),
    (1601, 1605, GW, "Elf neue Gewerkschaften in den Distrikten Lobenstein, Schleiz und Burgk", "Eleven new mining companies in the districts of Lobenstein, Schleiz and Burgk", "S. 243 b1"),
    (1604, None, VO, "Verordnung zur Förderung des Bergbaus", "Decree promoting mining", "S. 242 b5, S. 243 b1"),
    (1605, None, FO, "Landesregenten drängen darauf, den Eisenstein-Bau nicht den übrigen Metallen nachzustellen", "The rulers insist that iron-ore mining not be put behind the other metals", "S. 243 b1"),
    (1614, None, VO, "Verordnung zur Förderung des Bergbaus", "Decree promoting mining", "S. 242 b5, S. 243 b1"),
    (1649, None, VO, "Verordnung zur Förderung des Bergbaus", "Decree promoting mining", "S. 242 b5, S. 243 b1"),
]
chron = [[s, e, k, de_, en_, src] for s, e, k, de_, en_, src in CH]
n_vo = sum(1 for c in CH if c[2] == VO)
vo_years = [c[0] for c in CH if c[2] == VO]
print(n_vo, vo_years)

GRP_CALC = {"de": "datum.ore_group", "en": "{" + ",".join(f"'{k}':'{v}'" for k, v in GROUP_EN.items()) + "}[datum.ore_group]"}
GRP_LEGEND = {"de": "datum.label", "en": "{" + ",".join(f"'{k}':'{v}'" for k, v in GROUP_EN.items()) + "}[datum.label]"}
GCOLOR = {"field": "ore_group", "type": "nominal", "scale": {"domain": GROUP_ORDER}, "title": {"de": "Erz", "en": "Ore"}, "legend": {"labelExpr": GRP_LEGEND, "columns": 3, "labelLimit": 300}}
GCOLOR_NOFE = {**GCOLOR, "legend": {**GCOLOR["legend"], "values": [g for g in GROUP_ORDER if g != EI]}}
DIST = {"de": "Bergwerksdistrikt", "en": "Mining district"}
KIND_LEGEND = {"de": "datum.label", "en": "{" + ",".join(f"'{k}':'{v}'" for k, v in KIND_EN.items()) + "}[datum.label]"}
KIND_CALC = {"de": "datum.kind", "en": "{" + ",".join(f"'{k}':'{v}'" for k, v in KIND_EN.items()) + "}[datum.kind]"}

ana = {
    "id": "bergbau-bestand-oberland-vor-1648",
    "title": {"de": "Bergbau im Oberland vor dem Dreißigjährigen Krieg: Gruben, Hütten und Verordnungen", "en": "Mining in the Oberland before the Thirty Years' War: mines, smelters and decrees"},
    "category": "mining",
    "section": "t1-3-5",
    "sources": [
        {"page": "242", "block": "b4"},
        {"page": "242", "block": "b5"},
        {"page": "243", "block": "b1"},
        {"page": "243", "block": "b2"},
        {"page": "243", "block": "b4", "rows": "h1-r4"},
        {"page": "243", "block": "fn1"},
        {"page": "243", "block": "fn2"},
        {"page": "243", "block": "fn3"},
        {"page": "244", "block": "b1", "rows": "h1-r4"},
        {"page": "244", "block": "b2"},
        {"page": "244", "block": "b3"},
    ],
    "summary": {
        "de": f"Um zu zeigen, wie ausgedehnt der oberländische Bergbau vor dem Dreißigjährigen Krieg war, vergleicht Brückner die Gruben der drei Bergamtsdistrikte Schleiz, Saalburg und Lobenstein (S. 243) und die Hüttenwerke der Bezirke Schleiz mit Saalburg und Lobenstein (S. 244). Es sind {tot} Gruben und Seifen, davon {eisen} auf Eisen; dazu kommen Silber-, Kupfer-, Antimon-, Alaun- und Goldbetriebe. Eine Zeittafel ordnet die im Text genannten Daten von 1318 bis 1649.",
        "en": f"To show how extensive Oberland mining was before the Thirty Years' War, Brückner compares the mines of the three mining districts Schleiz, Saalburg and Lobenstein (p. 243) and the smelting works of the districts Schleiz with Saalburg and Lobenstein (p. 244). There are {tot} mines and placers, {eisen} of them for iron; silver, copper, antimony, alum and gold operations come in addition. A chronology arranges the dates named in the text from 1318 to 1649.",
    },
    "method": {
        "de": "Die Tabelle S. 243 (b4) wurde Zeile für Zeile übernommen: je Distrikt und Erzart die gedruckte Zahl der Gruben mit den in Klammern genannten Namen (Spalte names). Die Erzarten sind sechs Gruppen zugeordnet (ore_group): Eisen; Kupfer; Silber und Blei (einschließlich der »Silber- und Kupfergrube« bei Thramitz und der »Blei- und Silbergruben«); Antimon; Gold und Zinn (Goldgrube und Gold- und Zinnseife); Alaun. Die Hüttenwerke stammen aus der Tabelle S. 244 (b1), die für Schleiz und Saalburg zusammengefasst ist; »über 10 Hammerwerke« im Bezirk Lobenstein ist als Untergrenze 10 kodiert. Die Zeittafel enthält die Jahreszahlen aus S. 242 (b4, b5) und S. 243 (b1); die sechs Verordnungsjahre (1530 bis 1649) setzen den abgebrochenen Satz auf S. 242 (»durch Verordnungen, namentlich durch …«) auf S. 243 (»die von 1530, 1551, …«) fort.",
        "en": "The table on p. 243 (b4) was transferred row by row: for each district and ore, the printed number of mines with the names given in brackets (column names). The ores are assigned to six groups (ore_group): iron; copper; silver and lead (including the “silver and copper mine” at Thramitz and the “lead and silver mines”); antimony; gold and tin (gold mine and gold and tin placer); alum. The smelting works come from the table on p. 244 (b1), which combines Schleiz and Saalburg; “über 10 Hammerwerke” in the district of Lobenstein is coded as the lower bound 10. The chronology contains the years from p. 242 (b4, b5) and p. 243 (b1); the six years of decrees (1530 to 1649) continue the interrupted sentence on p. 242 (“through decrees, especially through …”) on p. 243 (“those of 1530, 1551, …”).",
    },
    "findings": [
        {"de": f"Von den {tot} Gruben des Oberlandes sind {eisen} Eisengruben ({de(eisen_share, 1)} %): Lobenstein {eisen_d[LOB]}, Schleiz {eisen_d[SCH]}, Saalburg {eisen_d[SAAL]}. Brückner betont entsprechend, dass die Landesregenten dem Eisenstein-Bau den Vorrang gaben, weil das Oberland hier an Güte und Reichtum in erster Reihe stehe (1605).",
         "en": f"Of the {tot} mines of the Oberland, {eisen} are iron mines ({en(eisen_share, 1)} %): Lobenstein {eisen_d[LOB]}, Schleiz {eisen_d[SCH]}, Saalburg {eisen_d[SAAL]}. Brückner accordingly stresses that the rulers gave priority to iron-ore mining because the Oberland ranked first in quality and richness (1605)."},
        {"de": f"Die {non_tot} übrigen Gruben verteilen sich nach Distrikt unterschiedlich: Saalburg {non[SAAL]} (zehn Kupfergruben, dazu Gold, Zinn und eine Silber-/Kupfergrube), Lobenstein {non[LOB]} (Silber, Kupfer, Blei, drei Alaunerzgruben), Schleiz {non[SCH]} (zwei Silber-, vier Antimongruben). Antimon kommt nur im Distrikt Schleiz, Alaun nur im Distrikt Lobenstein vor.",
         "en": f"The remaining {non_tot} mines are distributed differently among the districts: Saalburg {non[SAAL]} (ten copper mines, plus gold, tin and one silver/copper mine), Lobenstein {non[LOB]} (silver, copper, lead, three alum-ore mines), Schleiz {non[SCH]} (two silver, four antimony mines). Antimony occurs only in the district of Schleiz, alum only in the district of Lobenstein."},
        {"de": f"Bei den Hüttenwerken steht der Bezirk Lobenstein mit mindestens {n_l} Werken (über 10 Hammerwerke, 3 Kupferschmelzhütten, 3 Alaun- und Vitriolwerke) gegen {n_s} im Bezirk Schleiz mit Saalburg (2 Schmelzhütten, 3 Hammerwerke, 1 Alaunhütte, 1 Pulvermühle), obwohl Schleiz und Saalburg zusammen mehr Gruben haben ({by_d[SCH] + by_d[SAAL]} gegen {by_d[LOB]}).",
         "en": f"For smelting works the district of Lobenstein has at least {n_l} (over 10 hammer works, 3 copper smelters, 3 alum and vitriol works) against {n_s} in the district of Schleiz with Saalburg (2 smelters, 3 hammer works, 1 alum works, 1 powder mill), although Schleiz and Saalburg together have more mines ({by_d[SCH] + by_d[SAAL]} against {by_d[LOB]})."},
        {"de": f"Die Zeittafel zeigt eine Folge von Maßnahmen: Bergbauregal 1323–1329, ein Kupferliefervertrag 1502, {n_vo} Verordnungen zwischen {vo_years[0]} und {vo_years[-1]} und 1601–1605 die Gründung von elf Gewerkschaften in den Distrikten Lobenstein, Schleiz und Burgk.",
         "en": f"The chronology shows a sequence of measures: mining regalia 1323–1329, a copper supply contract in 1502, {n_vo} decrees between {vo_years[0]} and {vo_years[-1]}, and in 1601–1605 the founding of eleven mining companies in the districts of Lobenstein, Schleiz and Burgk."},
    ],
    "caveats": [
        {"de": "Die Zahlen beschreiben nach Brückner den Zustand vor dem Dreißigjährigen Krieg, ohne ein Stichjahr zu nennen; Hüttenwerke tragen Jahreszahlen zwischen 1472 und 1650 (S. 244). Zahl und Art der Gruben sind Brückners Zusammenstellung aus den Akten; ob alle Gruben gleichzeitig in Betrieb waren, sagt er nicht.",
         "en": "According to Brückner the figures describe the situation before the Thirty Years' War without giving a reference year; smelting works carry years between 1472 and 1650 (p. 244). Number and kind of mines are Brückner's compilation from the records; he does not say whether all mines were in operation at the same time."},
        {"de": "Die Distrikte der Gruben (Schleiz, Saalburg, Lobenstein) und der Hüttenwerke (Schleiz mit Saalburg, Lobenstein) sind verschieden gegliedert; der Vergleich fasst Schleiz und Saalburg zusammen. Die Angabe »über 10« ist eine Untergrenze.",
         "en": "The districts of the mines (Schleiz, Saalburg, Lobenstein) and of the smelting works (Schleiz with Saalburg, Lobenstein) are divided differently; the comparison combines Schleiz and Saalburg. “über 10” is a lower bound."},
        {"de": "Die Verordnungen von 1530 bis 1649 sind nur als Jahreszahlen überliefert; der Text nennt Inhalt und Urheber nicht. Die Zuordnung zu Verordnungen »zur Förderung des Bergbaus« folgt dem Satz auf S. 242, wonach die Landesregenten die Bergbauindustrie durch Befreiungen und Verordnungen unterstützten.",
         "en": "The decrees from 1530 to 1649 are given only as years; the text names neither content nor issuer. Their description as decrees “promoting mining” follows the sentence on p. 242 stating that the rulers supported the mining industry by exemptions and decrees."},
    ],
    "conversions": [],
    "datasets": [
        {"name": "gruben", "title": {"de": "Gruben nach Bergwerksdistrikt und Erz (vor 1648)", "en": "Mines by mining district and ore (before 1648)"},
         "columns": [
             {"name": "district", "label": DIST, "type": "string", "unit": None},
             {"name": "ore", "label": {"de": "Erz (Wortlaut)", "en": "Ore (printed)"}, "type": "string", "unit": None},
             {"name": "ore_group", "label": {"de": "Erzgruppe", "en": "Ore group"}, "type": "string", "unit": None, "derived": True},
             {"name": "kind", "label": {"de": "Art", "en": "Kind"}, "type": "string", "unit": None},
             {"name": "count", "label": {"de": "Anzahl", "en": "Number"}, "type": "integer", "unit": "Gruben"},
             {"name": "names", "label": {"de": "Namen und Lage", "en": "Names and location"}, "type": "string", "unit": None},
             {"name": "source", "label": {"de": "Quelle", "en": "Source"}, "type": "string", "unit": None},
         ],
         "rows": gruben, "source_refs": [{"page": "243", "block": "b4", "rows": "r2-r4"}]},
        {"name": "huetten", "title": {"de": "Hüttenwerke nach Bezirk und Art (vor 1648)", "en": "Smelting works by district and type (before 1648)"},
         "columns": [
             {"name": "district", "label": {"de": "Bezirk", "en": "District"}, "type": "string", "unit": None},
             {"name": "type", "label": {"de": "Art des Werks", "en": "Type of works"}, "type": "string", "unit": None},
             {"name": "count", "label": {"de": "Anzahl", "en": "Number"}, "type": "integer", "unit": "Werke", "note": "Hammerwerke Lobenstein: »über 10« = Untergrenze"},
             {"name": "source", "label": {"de": "Quelle", "en": "Source"}, "type": "string", "unit": None},
         ],
         "rows": huetten, "source_refs": [{"page": "244", "block": "b1", "rows": "r2-r3"}]},
        {"name": "chronik", "title": {"de": "Zeittafel zum Bergbau im Oberland 1318–1649", "en": "Chronology of Oberland mining, 1318–1649"},
         "columns": [
             {"name": "year", "label": {"de": "Jahr bzw. Beginn", "en": "Year or start"}, "type": "integer", "unit": "Jahr"},
             {"name": "year_end", "label": {"de": "Ende", "en": "End"}, "type": "integer", "unit": "Jahr"},
             {"name": "kind", "label": {"de": "Art", "en": "Type"}, "type": "string", "unit": None, "derived": True},
             {"name": "event_de", "label": {"de": "Ereignis (de)", "en": "Event (German)"}, "type": "string", "unit": None},
             {"name": "event_en", "label": {"de": "Ereignis (en)", "en": "Event (English)"}, "type": "string", "unit": None},
             {"name": "source", "label": {"de": "Quelle", "en": "Source"}, "type": "string", "unit": None},
         ],
         "rows": chron, "source_refs": [{"page": "242", "block": "b4"}, {"page": "242", "block": "b5"}, {"page": "243", "block": "b1"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "gruben",
         "title": {"de": "Gruben je Bergwerksdistrikt nach Erz", "en": "Mines per mining district by ore"},
         "caption": {"de": f"Gesamtzahl der Gruben und Seifen (Tabelle S. 243). Die Eisengruben überwiegen mit {eisen} von {tot} deutlich; Lobenstein und Schleiz haben je über 125, Saalburg 60.",
                     "en": f"Total number of mines and placers (table p. 243). Iron mines clearly dominate with {eisen} of {tot}; Lobenstein and Schleiz have over 125 each, Saalburg 60."},
         "vegalite": {
             "height": 240,
             "transform": [{"calculate": GRP_CALC, "as": "group_label"}],
             "mark": "bar",
             "encoding": {
                 "y": {"field": "district", "type": "nominal", "sort": [LOB, SCH, SAAL], "title": None},
                 "x": {"field": "count", "type": "quantitative", "title": {"de": "Anzahl Gruben", "en": "Number of mines"}},
                 "color": GCOLOR,
                 "tooltip": [{"field": "district", "title": DIST}, {"field": "ore", "title": {"de": "Erz (Wortlaut)", "en": "Ore (printed)"}}, {"field": "group_label", "title": {"de": "Erzgruppe", "en": "Ore group"}},
                             {"field": "count", "title": {"de": "Anzahl", "en": "Number"}}, {"field": "names", "title": {"de": "Namen und Lage", "en": "Names and location"}}]}}},
        {"id": "c2", "dataset": "gruben",
         "title": {"de": "Gruben ohne Eisen: Erzvielfalt je Distrikt", "en": "Mines other than iron: ore variety by district"},
         "caption": {"de": "Die Eisengruben sind ausgeblendet. Jeder Distrikt hat sein eigenes Profil: Antimon im Distrikt Schleiz, Gold, Zinn und viel Kupfer bei Saalburg, Silber, Blei, Kupfer und Alaun bei Lobenstein.",
                     "en": "The iron mines are hidden. Each district has its own profile: antimony in the district of Schleiz, gold, tin and much copper at Saalburg, silver, lead, copper and alum at Lobenstein."},
         "vegalite": {
             "height": 240,
             "transform": [{"filter": "datum.ore_group != 'Eisen'"}, {"calculate": GRP_CALC, "as": "group_label"}],
             "mark": "bar",
             "encoding": {
                 "y": {"field": "district", "type": "nominal", "sort": [SAAL, LOB, SCH], "title": None},
                 "x": {"field": "count", "type": "quantitative", "title": {"de": "Anzahl Gruben", "en": "Number of mines"}, "axis": {"tickMinStep": 1}},
                 "color": GCOLOR_NOFE,
                 "tooltip": [{"field": "district", "title": DIST}, {"field": "ore", "title": {"de": "Erz (Wortlaut)", "en": "Ore (printed)"}}, {"field": "group_label", "title": {"de": "Erzgruppe", "en": "Ore group"}},
                             {"field": "count", "title": {"de": "Anzahl", "en": "Number"}}, {"field": "names", "title": {"de": "Namen und Lage", "en": "Names and location"}}]}}},
        {"id": "c3", "dataset": "huetten",
         "title": {"de": "Hüttenwerke nach Bezirk und Art", "en": "Smelting works by district and type"},
         "caption": {"de": "Bestand nach der Tabelle auf S. 244. Für Lobenstein steht bei den Hammerwerken »über 10«; gezeichnet ist die Untergrenze 10.",
                     "en": "Stock according to the table on p. 244. For Lobenstein the hammer works are given as “over 10”; the lower bound 10 is drawn."},
         "vegalite": {
             "height": 260,
             "mark": "bar",
             "encoding": {
                 "x": {"field": "type", "type": "nominal", "sort": ["Hammerwerke", "Schmelzhütten", "Alaun-/Vitriolwerke", "Pulvermühlen"], "title": None, "axis": {"labelAngle": 0, "labelLimit": 180}},
                 "xOffset": {"field": "district", "type": "nominal"},
                 "y": {"field": "count", "type": "quantitative", "title": {"de": "Anzahl", "en": "Number"}, "axis": {"tickMinStep": 1}},
                 "color": {"field": "district", "type": "nominal", "title": {"de": "Bezirk", "en": "District"}, "legend": {"labelLimit": 300}},
                 "tooltip": [{"field": "district", "title": {"de": "Bezirk", "en": "District"}}, {"field": "type", "title": {"de": "Art", "en": "Type"}}, {"field": "count", "title": {"de": "Anzahl", "en": "Number"}}]}}},
        {"id": "c4", "dataset": "chronik",
         "title": {"de": "Zeittafel: Bergbau im Oberland 1318–1649", "en": "Chronology: Oberland mining, 1318–1649"},
         "caption": {"de": "Urkundliche Erwähnungen und Privilegien, Verordnungen, Verträge und Fördermaßnahmen sowie die Gründung von elf Gewerkschaften 1601–1605 (Balken). Die Verordnungen setzen mit 1530 ein.",
                     "en": "Documentary mentions and privileges, decrees, contracts and promotion measures, and the founding of eleven mining companies in 1601–1605 (bar). The decrees begin in 1530."},
         "vegalite": {
             "height": 240,
             "transform": [{"calculate": KIND_CALC, "as": "kind_label"}, {"calculate": "datum.year_end != null ? datum.year_end : datum.year", "as": "end_plot"}],
             "layer": [
                 {"transform": [{"filter": "datum.year_end != null"}],
                  "mark": {"type": "bar", "height": {"band": 0.5}},
                  "encoding": {
                      "y": {"field": "kind", "type": "nominal", "sort": [URK, FO, VO, GW], "title": None, "axis": {"labelExpr": KIND_LEGEND}},
                      "x": {"field": "year", "type": "quantitative", "scale": {"domain": [1300, 1670]}, "axis": {"format": "d", "values": list(range(1300, 1651, 50)), "title": {"de": "Jahr", "en": "Year"}}},
                      "x2": {"field": "end_plot"},
                      "color": {"field": "kind", "type": "nominal", "scale": {"domain": [URK, FO, VO, GW]}, "legend": None},
                      "tooltip": [{"field": "kind_label", "title": {"de": "Art", "en": "Type"}}, {"field": "year", "title": {"de": "Jahr", "en": "Year"}}, {"field": "year_end", "title": {"de": "bis", "en": "to"}}, {"field": "event_de", "title": {"de": "Ereignis", "en": "Event (German)"}}]}},
                 {"transform": [{"filter": "datum.year_end == null"}],
                  "mark": {"type": "point", "filled": True, "size": 90, "opacity": 1},
                  "encoding": {
                      "y": {"field": "kind", "type": "nominal", "sort": [URK, FO, VO, GW]},
                      "x": {"field": "year", "type": "quantitative", "scale": {"domain": [1300, 1670]}},
                      "color": {"field": "kind", "type": "nominal", "scale": {"domain": [URK, FO, VO, GW]}, "legend": None},
                      "tooltip": [{"field": "kind_label", "title": {"de": "Art", "en": "Type"}}, {"field": "year", "title": {"de": "Jahr", "en": "Year"}}, {"field": "event_de", "title": {"de": "Ereignis", "en": "Event (German)"}}]}},
             ]}},
    ],
    "keywords": {"de": ["Bergbau", "Eisengruben", "Silbergruben", "Kupfergruben", "Antimon", "Alaun", "Hüttenwerke", "Hammerwerke", "Schleiz", "Saalburg", "Lobenstein", "Bergordnung", "Gewerkschaften", "Oberland"],
                 "en": ["mining", "iron mines", "silver mines", "copper mines", "antimony", "alum", "smelting works", "hammer works", "Schleiz", "Saalburg", "Lobenstein", "mining decrees", "mining companies", "Oberland"]},
    "related": ["bergbau-huettenwerke-oberland-betriebszeiten", "bergbau-erzbergbau-zeitleiste-ober-unterland"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(ana)
