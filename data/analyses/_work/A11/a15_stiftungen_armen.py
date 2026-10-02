"""A11-15: Stiftungen für Arme, Waisen und Bedürftige mit genanntem Kapital (pp. 308-310)."""
from common import *

# key, name_de, name_en, group_key, group_de, group_en, purpose_de, purpose_en, capital (Thaler), year (or None), year_de, year_en, annual_interest (or None), source page/block
F_ = [
    ("a", "Christiane Louise Reuß", "Christiane Louise Reuss", "a", "Fürstenhaus", "Princely house", "verschiedene Zwecke in Gera und Saalburg", "various purposes in Gera and Saalburg", 30000, 1828, "Testament 1828", "will of 1828", None, "309", "b1"),
    ("b", "Heinrich LXII., verschämte Arme", "Heinrich LXII, needy poor", "a", "Fürstenhaus", "Princely house", "verschämte Arme", "needy poor", 3000, None, "", "", 120, "308", "b14"),
    ("c", "Heinrich LXII., Dienstboten", "Heinrich LXII, servants", "a", "Fürstenhaus", "Princely house", "Dienstboten", "servants", 200, None, "", "", 8, "308", "b13"),
    ("d", "Heinrich LXVII., Waisen", "Heinrich LXVII, orphans", "a", "Fürstenhaus", "Princely house", "Waisenkinder", "orphans", 3750, 1862, "1862 (1000 Thlr, erhöht auf 3750)", "1862 (1,000 Thaler, raised to 3,750)", None, "308", "b15"),
    ("e", "Rettungshaus Hohenleuben", "Rescue house Hohenleuben", "a", "Fürstenhaus", "Princely house", "verwahrloste Kinder", "neglected children", 2300, 1853, "1853", "1853", None, "310", "b3"),
    ("f", "Ebeling (Gera)", "Ebeling (Gera)", "b", "Private", "Private donors", "bedürftige Bürger", "needy citizens", 6000, 1833, "1833", "1833", None, "309", "b4"),
    ("g", "Friederici (Armenfreischule)", "Friederici (free school)", "b", "Private", "Private donors", "Weihnachtsbescherung der Armenfreischule", "Christmas gifts for the free school", 500, 1856, "1856", "1856", None, "309", "b6"),
    ("h", "Münch (Gera)", "Münch (Gera)", "b", "Private", "Private donors", "verschämte arme Frauen", "needy women", 1000, 1854, "1854 (Tod des Stifters)", "1854 (founder's death)", None, "309", "b8"),
    ("i", "Zenker (Schleiz)", "Zenker (Schleiz)", "b", "Private", "Private donors", "Hospitaliten in Schleiz", "hospital inmates in Schleiz", 100, 1858, "1858 (Tod des Stifters)", "1858 (founder's death)", None, "309", "b9"),
    ("j", "Gräfin Therese (Köstritz)", "Countess Therese (Köstritz)", "b", "Private", "Private donors", "Witwen und Waisen in Köstritz", "widows and orphans in Köstritz", 260, 1858, "1858 (Tod der Stifterin)", "1858 (founder's death)", None, "309", "b10"),
    ("k", "Bauer (Gera)", "Bauer (Gera)", "b", "Private", "Private donors", "Witwen und Waisen geraer Kaufleute", "widows and orphans of Gera merchants", 1000, None, "", "", None, "309", "b11"),
    ("l", "Dinger (Gera)", "Dinger (Gera)", "b", "Private", "Private donors", "Wäscherinnen und Waisenanstalt", "washerwomen and an orphanage", 700, 1860, "1860", "1860", None, "309", "b12"),
    ("m", "Ungenannter (Gera)", "Anonymous (Gera)", "b", "Private", "Private donors", "bedürftige Kranke in Gera", "needy sick in Gera", 200, 1854, "1854", "1854", 8, "309", "b13"),
]
rows = []
for k, nde, nen, gk, gde, gen, pde, pen, cap, yr, yde, yen, intr, pg, blk in F_:
    yld = round(100 * intr / cap, 1) if intr else None
    rows.append([k, nde, nen, gk, gde, gen, pde, pen, cap, yr, yde, yen, intr, yld])
total = sum(r[8] for r in rows)
fh = sum(r[8] for r in rows if r[3] == "a")
cl = rows[0][8]
yrs = [r for r in rows if r[9]]
print(total, fh, cl, len(yrs), [r[13] for r in rows if r[13]])
yields = [(r[1], r[13]) for r in rows if r[13]]
ymin, ymax = min(y for _, y in yields), max(y for _, y in yields)
pct = lambda a, b: 100 * a / b
n_with_year = len(yrs)
yrmin, yrmax = min(r[9] for r in yrs), max(r[9] for r in yrs)
n_mid = len([r for r in yrs if 1833 <= r[9] <= 1862])
small50 = [r for r in yrs if r[3] == 'b' and 100 <= r[8] <= 1000]
print(n_mid, [(r[1], r[9]) for r in small50], len(yrs))
# annual distribution of the 1867 foundation (p. 308 b16)
DIST = [("Gera", 20), ("Schleiz", 12), ("Ebersdorf", 11), ("Saalburg", 11), ("Lobenstein", 15), ("Hirschberg", 10.5), ("Tanna", 10.5)]
dist_rows = [[t, a] for t, a in DIST]
dist_total = sum(a for _, a in DIST)
print(dist_total)


def D(x, nd=0):
    return fmt_de(x, nd)


def E(x, nd=0):
    return fmt_en(x, nd)


ana = {
    "id": "armenwesen-stiftungen-kapital-1828-1866",
    "title": bi("Stiftungen für Arme, Waisen und Bedürftige: Kapital und Gründung", "Foundations for the poor, orphans and the needy: capital and founding"),
    "category": "welfare",
    "section": "t1-4-8",
    "sources": [{"page": "308", "block": "b13"}, {"page": "308", "block": "b14"}, {"page": "308", "block": "b15"}, {"page": "308", "block": "b16"},
                {"page": "309", "block": "b1"}, {"page": "309", "block": "b4"}, {"page": "309", "block": "b6"}, {"page": "309", "block": "b8"}, {"page": "309", "block": "b9"},
                {"page": "309", "block": "b10"}, {"page": "309", "block": "b11"}, {"page": "309", "block": "b12"}, {"page": "309", "block": "b13"}, {"page": "310", "block": "b3"}],
    "summary": bi(
        f"Brückner führt für das Armenwesen landesherrliche und private Stiftungen auf; bei dreizehn nennt er das Kapital in Thalern. Zusammen sind es {D(total)} Thaler, davon {D(pct(cl,total),0)} % aus der Stiftung der Fürstin Christiane Louise von 1828. Die Auswertung stellt Kapital, Gründungszeit und, wo genannt, die Verzinsung dar; außerdem die Verteilung einer Stiftung von 1867 auf sieben Städte.",
        f"For poor relief Brückner lists princely and private foundations; for thirteen of them he gives the capital in Thaler. Together they amount to {E(total)} Thaler, {E(pct(cl,total),0)} % of it from the foundation of Princess Christiane Louise of 1828. The analysis presents capital, time of founding and, where given, the yield; it also shows the distribution of a foundation of 1867 among seven towns.",
    ),
    "method": bi(
        "Aus den Aufzählungen S. 308–310 (»Landesherrliche Stiftungen«, »Stiftungen von Privaten«, Rettungshaus) wurden alle Stiftungen mit genanntem Kapital in Thalern ausgewählt. Nicht aufgenommen sind Stiftungen ohne Kapitalangabe (z. B. Kirschkauer Waisenhaus: Kammergut, jährlich ca. 1420 Thaler Unterstützung; Wiesesches Bürgerrettungsinstitut; Schülersches Stift) und das Kapital von Stipendien (siehe die Auswertung zu den Stipendien). Bei der Dinger-Stiftung sind 200 und 500 Thaler zusammengezählt (700). Die Verzinsung = Jahresertrag : Kapital (abgeleitet). Währung: 1 Thaler = 30 Silbergroschen.",
        "From the lists on pp. 308–310 (“princely foundations”, “foundations of private persons”, rescue house) all foundations with a capital stated in Thaler were selected. Not included are foundations without a capital figure (e.g. the Kirschkau orphanage: a crown estate, about 1,420 Thaler of support a year; the Wiese citizens' rescue institute; the Schüler foundation) and the capital of stipends (see the analysis of the stipends). For the Dinger foundation 200 and 500 Thaler are added (700). Yield = annual income : capital (derived). Currency: 1 Thaler = 30 Silbergroschen.",
    ),
    "findings": [
        bi(f"Die dreizehn Stiftungen verfügen zusammen über {D(total)} Thaler; auf das Fürstenhaus entfallen {D(fh)} Thaler ({D(pct(fh,total),0)} %), auf private Stifter {D(total-fh)} Thaler.",
           f"The thirteen foundations together hold {E(total)} Thaler; the princely house accounts for {E(fh)} Thaler ({E(pct(fh,total),0)} %), private donors for {E(total-fh)} Thaler."),
        bi(f"Die Stiftung der Fürstin Christiane Louise (30.000 Thaler, 1828) ist fünfmal so groß wie die nächstgrößere (Ebeling 1833: 6.000) und größer als alle übrigen zwölf zusammen ({D(total-cl)}).",
           f"The foundation of Princess Christiane Louise (30,000 Thaler, 1828) is five times as large as the next (Ebeling 1833: 6,000) and larger than all other twelve together ({E(total-cl)})."),
        bi(f"Von den {D(n_with_year)} Stiftungen mit Zeitangabe entstanden alle zwischen {yrmin} und {yrmax}; {D(n_mid)} davon zwischen 1833 und 1862. Die kleinen privaten Stiftungen (100–1.000 Thaler) mit Jahresangabe stammen bis auf eine aus den 1850er Jahren.",
           f"All {E(n_with_year)} foundations with a date arose between {yrmin} and {yrmax}; {E(n_mid)} of them between 1833 and 1862. The small private foundations (100–1,000 Thaler) with a year date, with one exception, from the 1850s."),
        bi(f"Wo Brückner Kapital und Jahresertrag nennt (drei Stiftungen), beträgt die Verzinsung jeweils {D(ymin,1)} %; das entspricht dem Zinssatz der Staatsschuldscheine von 4 % (S. 277).",
           f"Where Brückner gives both capital and annual income (three foundations), the yield is {E(ymin,1)} % in each case; this matches the 4 % interest of the state bonds (p. 277)."),
        bi(f"Die Stiftung vom 20. Oktober 1867 verteilt jährlich {D(dist_total,0)} Thaler an verschämte Arme in sieben Städten; Gera erhält 20, Lobenstein 15, Schleiz 12 Thaler.",
           f"The foundation of 20 October 1867 distributes {E(dist_total,0)} Thaler a year to the needy poor in seven towns; Gera receives 20, Lobenstein 15, Schleiz 12 Thaler."),
    ],
    "caveats": [
        bi("Die Jahreszahlen bezeichnen teils die Errichtung, teils das Testament oder den Tod des Stifters (siehe Spalte »Zeitpunkt«); für sechs Stiftungen nennt Brückner kein Jahr. Nur drei Stiftungen geben sowohl Kapital als auch Jahresertrag an; die Verzinsungen sind daher eine schmale Basis.",
           "The years denote partly the establishment, partly the will or the founder's death (see column “point in time”); for six foundations Brückner gives no year. Only three foundations state both capital and annual income; the yields are therefore a narrow basis."),
        bi("Die Summen vergleichen Kapital in Thalern ohne Rücksicht auf unterschiedliche Entstehungsjahre und Kaufkraft. Das Kapital der Fürstenhaus-Stiftungen kann bei Christiane Louise nur als »ursprüngliches Kapital« gelten; ob es 1868 noch bestand, sagt Brückner nicht. Zahlreiche kleinere Stiftungen (Gera allein »an 100 kleine Legate«) sind nicht erfasst.",
           "The sums compare capital in Thaler regardless of differing founding years and purchasing power. For Christiane Louise the capital is only the “original capital”; Brückner does not say whether it still existed in 1868. Numerous smaller foundations (Gera alone has “about 100 small legacies”) are not covered."),
    ],
    "datasets": [
        {"name": "foundations", "title": bi("Stiftungen mit genanntem Kapital", "Foundations with a stated capital"),
         "columns": [
             col("key", "Kürzel", "Key", "string"),
             col("name_de", "Stiftung", "Foundation", "string"), col("name_en", "Stiftung (englisch)", "Foundation (English)", "string"),
             col("group_key", "Kürzel Stifter", "Donor key", "string"),
             col("group_de", "Stifter", "Donor", "string"), col("group_en", "Stifter (englisch)", "Donor (English)", "string"),
             col("purpose_de", "Zweck", "Purpose", "string"), col("purpose_en", "Zweck (englisch)", "Purpose (English)", "string"),
             col("capital", "Kapital", "Capital", "integer", "Thaler", note="Dinger: 200 + 500 Thaler addiert (700)."),
             col("year", "Jahr", "Year", "integer", None),
             col("year_de", "Zeitpunkt", "Point in time", "string"), col("year_en", "Zeitpunkt (englisch)", "Point in time (English)", "string"),
             col("income", "Jahresertrag", "Annual income", "integer", "Thaler"),
             col("yield", "Verzinsung", "Yield", "number", "%", derived=True, note="Jahresertrag : Kapital"),
         ],
         "rows": rows, "source_refs": [{"page": "308", "block": "b13"}, {"page": "308", "block": "b14"}, {"page": "308", "block": "b15"}, {"page": "309", "block": "b1"}, {"page": "309", "block": "b4"},
                                      {"page": "309", "block": "b6"}, {"page": "309", "block": "b8"}, {"page": "309", "block": "b9"}, {"page": "309", "block": "b10"}, {"page": "309", "block": "b11"},
                                      {"page": "309", "block": "b12"}, {"page": "309", "block": "b13"}, {"page": "310", "block": "b3"}]},
        {"name": "distribution", "title": bi("Verteilung der Stiftung vom 20. Oktober 1867", "Distribution of the foundation of 20 October 1867"),
         "columns": [col("town", "Stadt", "Town", "string"), col("thaler", "Jahresbetrag", "Annual amount", "number", "Thaler", derived=True, note="Alle Beträge stehen im Text; 10 1/2 gelesen als 10,5 (Bruch wird vom Zahlenabgleich nicht erkannt).")],
         "rows": dist_rows, "source_refs": [{"page": "308", "block": "b16"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "foundations",
         "title": bi("Kapital der Stiftungen", "Capital of the foundations"),
         "caption": bi("Thaler. Die Stiftung der Fürstin Christiane Louise (1828) überragt alle anderen.", "Thaler. The foundation of Princess Christiane Louise (1828) dwarfs all others."),
         "vegalite": {
             "height": 380,
             "mark": "bar",
             "encoding": {
                 "y": {"field": F("name"), "type": "nominal", "sort": "-x", "title": None, "axis": {"labelLimit": 360}},
                 "x": {"field": "capital", "type": "quantitative", "title": bi("Kapital (Thaler)", "Capital (Thaler)"), "axis": {"format": ",d"}},
                 "color": {"field": F("group"), "type": "nominal", "title": None, "sort": {"field": "group_key", "op": "min"}},
                 "tooltip": [ttf("name", "Stiftung", "Foundation"), ttf("purpose", "Zweck", "Purpose"), {"field": "capital", "title": bi("Kapital (Thaler)", "Capital (Thaler)"), "format": ","}, ttf("year", "Zeitpunkt", "Point in time")]}}},
        {"id": "c2", "dataset": "foundations",
         "title": bi("Gründungszeit und Kapital", "Time of founding and capital"),
         "caption": bi("Nur Stiftungen mit Jahresangabe; logarithmische Kapitalachse. Fast alle Stiftungen stammen aus den 1830er bis 1860er Jahren.", "Only foundations with a year; logarithmic capital axis. Almost all foundations date from the 1830s to the 1860s."),
         "vegalite": {
             "height": 280,
             "transform": [{"filter": "datum.year != null"}],
             "mark": {"type": "point", "filled": True, "size": 110},
             "encoding": {
                 "x": {"field": "year", "type": "quantitative", "title": bi("Jahr", "Year"), "axis": {"format": "d"}, "scale": {"domain": [1825, 1868]}},
                 "y": {"field": "capital", "type": "quantitative", "title": bi("Kapital (Thaler, logarithmisch)", "Capital (Thaler, logarithmic)"), "scale": {"type": "log", "domain": [50, 50000]}, "axis": {"format": ",d", "values": [100, 300, 1000, 3000, 10000, 30000]}},
                 "color": {"field": F("group"), "type": "nominal", "title": None, "sort": {"field": "group_key", "op": "min"}},
                 "tooltip": [ttf("name", "Stiftung", "Foundation"), ttf("year", "Zeitpunkt", "Point in time"), {"field": "capital", "title": bi("Kapital (Thaler)", "Capital (Thaler)"), "format": ","}]}}},
        {"id": "c3", "dataset": "distribution",
         "title": bi("Jährliche Spende der Stiftung von 1867 nach Stadt", "Annual gift of the 1867 foundation by town"),
         "caption": bi("Thaler, jährlich am 20. Oktober an verschämte Arme.", "Thaler, distributed to the needy poor each year on 20 October."),
         "vegalite": {
             "height": 240,
             "mark": "bar",
             "encoding": {
                 "y": {"field": "town", "type": "nominal", "sort": "-x", "title": None},
                 "x": {"field": "thaler", "type": "quantitative", "title": bi("Thaler", "Thaler")},
                 "tooltip": [tt("town", "Stadt", "Town"), tt("thaler", "Thaler", "Thaler")]}}},
    ],
    "keywords": {"de": ["Stiftungen", "Armenwesen", "Armenpflege", "Waisen", "Christiane Louise", "Kapital", "Wohltätigkeit", "Verschämte Arme"],
                 "en": ["foundations", "poor relief", "orphans", "Christiane Louise", "capital", "charity", "needy poor"]},
}
write(ana)
