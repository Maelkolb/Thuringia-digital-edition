"""A11-16: Stipendien und Schulstiftungen: Jahresbeträge, Stifter und Gründungszeit (pp. 304-308)."""
from common import *

T = lambda thlr, sgr=0.0: round(thlr + sgr / 30, 2)

# key, name_de, name_en, level_key, level_de, level_en, founder_key, founder_de, founder_en, place, year, recipients, per_recipient, annual_total, capital
S = [
    ("a01", "Jugelsches Stipendium", "Jugel stipend", "a", "Universität", "University", "b", "Bürger, Beamte, Adel", "Citizens, officials, nobility", "Gera", 1615, 1, 10.5, 10.5, None),
    ("a02", "Reißkesches Stipendium", "Reißke stipend", "a", "Universität", "University", "b", "Bürger, Beamte, Adel", "Citizens, officials, nobility", "Gera", 1622, 2, None, 21.0, None),
    ("a03", "Stockelmannisches Stipendium", "Stockelmann stipend", "a", "Universität", "University", "b", "Bürger, Beamte, Adel", "Citizens, officials, nobility", "Gera", 1650, 2, 17.5, 35.0, None),
    ("a04", "Bragersches Stipendium", "Brager stipend", "a", "Universität", "University", "b", "Bürger, Beamte, Adel", "Citizens, officials, nobility", "Gera", 1696, 2, 17.5, 35.0, None),
    ("a05", "Langenberg (Bergner, Buschendorf)", "Langenberg (Bergner, Buschendorf)", "a", "Universität", "University", "b", "Bürger, Beamte, Adel", "Citizens, officials, nobility", "Langenberg", 1714, None, None, T(8, 6 + 8 / 12), None),
    ("a06", "Straußisches Stipendium", "Strauß stipend", "a", "Universität", "University", "b", "Bürger, Beamte, Adel", "Citizens, officials, nobility", "Gera", 1730, 1, T(3, 8), T(3, 8), None),
    ("a07", "Richtersches Stipendium", "Richter stipend", "a", "Universität", "University", "b", "Bürger, Beamte, Adel", "Citizens, officials, nobility", "Gera", 1783, 2, T(20, 16.75), 2 * T(20, 16.75), None),
    ("a08", "Stipendium Heinrichs LXII.", "Stipend of Heinrich LXII", "a", "Universität", "University", "a", "Landesherr", "Sovereign", "Land", 1850, None, None, 40.0, None),
    ("a09", "Saalburger Stipendien (zwei)", "Saalburg stipends (two)", "a", "Universität", "University", "a", "Landesherr", "Sovereign", "Saalburg", 1866, 2, 30.0, 60.0, None),
    ("a10", "Schleizer Landesstipendium", "Schleiz provincial stipend", "a", "Universität", "University", "a", "Landesherr", "Sovereign", "Schleiz", None, 2, 21.0, 42.0, None),
    ("a11", "Lobenstein-Ebersdorfer Stipendium", "Lobenstein-Ebersdorf stipend", "a", "Universität", "University", "a", "Landesherr", "Sovereign", "Lobenstein-Ebersdorf", None, 1, 27.0, 27.0, None),
    ("b01", "Naundorfisches Stipendium", "Naundorf stipend", "b", "Gymnasium, Seminar", "Gymnasium, college", "b", "Bürger, Beamte, Adel", "Citizens, officials, nobility", "Gera", 1667, None, None, 7.0, None),
    ("b02", "Strauch-Lenzsches Stipendium", "Strauch-Lenz stipend", "b", "Gymnasium, Seminar", "Gymnasium, college", "b", "Bürger, Beamte, Adel", "Citizens, officials, nobility", "Gera", 1739, 6, None, 10.0, None),
    ("b03", "Freitischstipendium Gera (sechs Stellen)", "Free-table stipend Gera (six places)", "b", "Gymnasium, Seminar", "Gymnasium, college", "a", "Landesherr", "Sovereign", "Gera", 1763, 6, 28.0, 168.0, None),
    ("b04", "Fürstlicher Freitisch Schleiz", "Princely free table, Schleiz", "b", "Gymnasium, Seminar", "Gymnasium, college", "a", "Landesherr", "Sovereign", "Schleiz", None, 12, 6.5, 78.0, None),
    ("b05", "Stipendium Heinrichs LXVII. (Seminaristen)", "Stipend of Heinrich LXVII (trainee teachers)", "b", "Gymnasium, Seminar", "Gymnasium, college", "a", "Landesherr", "Sovereign", "Schleiz", None, None, None, 40.0, None),
    ("c01", "Heinrichs LXVII., Landlehrer", "Heinrich LXVII, village teachers", "c", "Landschulen", "Village schools", "a", "Landesherr", "Sovereign", "Land", None, None, None, 45.0, 1000),
    ("c02", "Wiesesche Stiftung (Landschulen)", "Wiese foundation (village schools)", "c", "Landschulen", "Village schools", "b", "Bürger, Beamte, Adel", "Citizens, officials, nobility", "Gera", None, None, None, 200.0, None),
]
rows = [list(r) for r in S]
# capital-only foundations (annual amount not stated)
CAPONLY = [
    ("k1", "Grimmsches Stipendium", "Grimm stipend", "a", "Universität", "University", "b", "Bürger, Beamte, Adel", "Citizens, officials, nobility", "Untermhaus/Gera", 1864, None, None, None, 1500),
    ("k2", "Webersches Stipendium", "Weber stipend", "a", "Universität", "University", "b", "Bürger, Beamte, Adel", "Citizens, officials, nobility", "Gera", 1864, None, None, None, 2000),
    ("k3", "Friedericische Freitischstellen Leipzig", "Friederici free places, Leipzig", "a", "Universität", "University", "b", "Bürger, Beamte, Adel", "Citizens, officials, nobility", "Leipzig/Gera", 1835, 2, None, None, 1500),
    ("k4", "Friedericische Stiftung (Seminar)", "Friederici foundation (college)", "b", "Gymnasium, Seminar", "Gymnasium, college", "b", "Bürger, Beamte, Adel", "Citizens, officials, nobility", "Gera", 1860, None, None, None, 500),
    ("k5", "Herzogische Stiftung", "Herzog foundation", "b", "Gymnasium, Seminar", "Gymnasium, college", "b", "Bürger, Beamte, Adel", "Citizens, officials, nobility", "Gera", 1863, 1, None, None, 650),
]
rows_all = rows + [list(r) for r in CAPONLY]
with_total = [r for r in rows_all if r[13] is not None]
cap_rows = [r for r in rows_all if r[14] is not None]
print(len(rows_all), len(with_total), len(cap_rows))
tot_annual = sum(r[13] for r in with_total)
stud_total = sum(r[13] for r in with_total if r[3] in ("a", "b"))
per_rec = [r for r in rows_all if r[12] is not None and r[3] in ("a", "b")]
yr = [r for r in rows_all if r[10] is not None and r[13] is not None]
yr_b_pre1800 = [r for r in yr if r[6] == "b" and r[10] < 1800]
cap_total = sum(r[14] for r in cap_rows if r[0].startswith('k'))
yr_pre = [r for r in yr if r[10] < 1800]
yr_pre_b = [r for r in yr_pre if r[6] == 'b']
yr_post = [r for r in yr if r[10] >= 1850]
yr_post_a = [r for r in yr_post if r[6] == 'a']
per_vals = sorted(r[12] for r in per_rec)
print(tot_annual, stud_total, per_vals, len(yr), len(yr_b_pre1800), cap_total)
med = per_vals[len(per_vals) // 2] if len(per_vals) % 2 else (per_vals[len(per_vals) // 2 - 1] + per_vals[len(per_vals) // 2]) / 2
teacher_min = 180
oldest = min(yr, key=lambda r: r[10])
bigger = max([r for r in with_total if r[3] in ("a", "b")], key=lambda r: r[13])
fuerst_n = len([r for r in with_total if r[6] == "a"])
fuerst_sum = sum(r[13] for r in with_total if r[6] == "a")
print(med, oldest[1], bigger[1], fuerst_n, fuerst_sum)


def D(x, nd=0):
    return fmt_de(x, nd)


def E(x, nd=0):
    return fmt_en(x, nd)


ana = {
    "id": "schule-stipendien-stiftungen-betraege-gruendung",
    "title": bi("Stipendien und Schulstiftungen: Jahresbeträge, Stifter und Gründungszeit", "Stipends and school foundations: annual amounts, donors and time of founding"),
    "category": "education",
    "section": "t1-4-8",
    "sources": [{"page": "304", "block": "b6", "rows": "i1-i5"}, {"page": "305", "block": "b1"}, {"page": "305", "block": "b3"}, {"page": "305", "block": "b4"}, {"page": "305", "block": "b5"},
                {"page": "305", "block": "b6"}, {"page": "305", "block": "b7"}, {"page": "305", "block": "b8"}, {"page": "305", "block": "b9"}, {"page": "305", "block": "b11"}, {"page": "305", "block": "b12"},
                {"page": "306", "block": "b3"}, {"page": "306", "block": "b4"}, {"page": "306", "block": "b6"}, {"page": "306", "block": "b7"}, {"page": "306", "block": "b9"},
                {"page": "307", "block": "b1"}, {"page": "307", "block": "b6", "rows": "i1"}, {"page": "308", "block": "b6"}, {"page": "308", "block": "b9"}, {"page": "308", "block": "b10"}, {"page": "297", "block": "b3", "note": "Mindestbesoldung eines Landlehrers (Vergleichswert)"}],
    "summary": bi(
        f"Brückner verzeichnet zahlreiche Stipendien und Freitische für Studenten, Gymnasiasten, Seminaristen und Landschullehrer, die meist von Bürgern, Beamten und Fürsten gestiftet wurden. Für {len(with_total)} von ihnen nennt er einen Jahresbetrag, für {len(cap_rows)} ein Kapital, für {len(yr)} Stiftungen mit Jahresbetrag ein Gründungsjahr (1615–1866). Die Auswertung ordnet Beträge, Stifter und Gründungszeit.",
        f"Brückner lists numerous stipends and free tables for university students, Gymnasium pupils, trainee teachers and village teachers, mostly founded by citizens, officials and princes. For {len(with_total)} of them he gives an annual amount, for {len(cap_rows)} a capital, and for {len(yr)} foundations with an annual amount a founding year (1615–1866). The analysis arranges amounts, donors and time of founding.",
    ),
    "method": bi(
        "Die Stipendien stammen aus den Aufzählungen S. 304–308 (»Universitätsstipendien«, »Gymnasial- und Seminarstipendien«, »Landschulen«). Angaben in Thalern, Silbergroschen und Pfennigen wurden mit 1 Thaler = 30 Silbergroschen = 360 Pfennige in Dezimal-Thaler umgerechnet (z. B. 20 Thlr. 16¾ Sgr. = 20,56 Thaler); der Betrag der langenbergischen Stipendien (10 Mark = 8 Thaler 6 Sgr. 8 Pfg.) wurde wie gedruckt umgerechnet. Der Gesamtbetrag je Stiftung = Betrag je Stipendiat × Zahl der Stipendiaten, wo beide genannt sind. Stiftungen, die nur ein Kapital nennen (Grimm, Weber, Friederici, Herzog), sind gesondert aufgeführt. Nicht aufgenommen sind Legate in den älteren Währungen »Mark« und »Aßo« sowie die Bücherstipendien.",
        "The stipends come from the lists on pp. 304–308 (“university stipends”, “Gymnasium and college stipends”, “village schools”). Amounts in Thaler, Silbergroschen and Pfennige were converted into decimal Thaler with 1 Thaler = 30 Silbergroschen = 360 Pfennige (e.g. 20 Thlr. 16¾ Sgr. = 20.56 Thaler); the amount of the Langenberg stipends (10 Mark = 8 Thaler 6 Sgr. 8 Pfg.) was converted as printed. The total per foundation = amount per recipient × number of recipients where both are given. Foundations that give only a capital (Grimm, Weber, Friederici, Herzog) are listed separately. Legacies in the older currencies “Mark” and “Aßo” and the book stipends are not included.",
    ),
    "findings": [
        bi(f"Die {len(with_total)} Stiftungen mit Jahresbetrag zahlen zusammen {D(tot_annual)} Thaler jährlich, davon {D(stud_total)} Thaler an Studenten, Gymnasiasten und Seminaristen; der größte Posten für Schüler und Studenten ist das geraer Freitischstipendium von 1763 ({D(bigger[13])} Thaler für sechs Stellen).",
           f"The {len(with_total)} foundations with an annual amount pay {E(tot_annual)} Thaler a year in total, {E(stud_total)} Thaler of it to university students, Gymnasium pupils and trainee teachers; the largest item for pupils and students is the Gera free-table stipend of 1763 ({E(bigger[13])} Thaler for six places)."),
        bi(f"Je Stipendiat zahlen die Stiftungen meist 10 bis 30 Thaler im Jahr (Median {D(med,1)}); das sind etwa {D(100*10/teacher_min,0)} bis {D(100*30/teacher_min,0)} % der gesetzlichen Mindestbesoldung eines Landlehrers von 180 Thalern (S. 297).",
           f"Per recipient the foundations mostly pay 10 to 30 Thaler a year (median {E(med,1)}); this is about {E(100*10/teacher_min,0)} to {E(100*30/teacher_min,0)} % of the legal minimum pay of a village teacher of 180 Thaler (p. 297)."),
        bi(f"Von den {len(yr)} Stiftungen mit Jahresbetrag und Jahreszahl entstanden {len(yr_pre)} vor 1800, davon {len(yr_pre_b)} durch Bürger, Beamte und Adlige (überwiegend in Gera); die älteste ist das jugelsche Stipendium von {oldest[10]}. Die {len(yr_post)} Stiftungen ab 1850 sind {'alle' if len(yr_post)==len(yr_post_a) else 'zum Teil'} landesherrlich.",
           f"Of the {len(yr)} foundations with an annual amount and a year, {len(yr_pre)} arose before 1800, {len(yr_pre_b)} of them from citizens, officials and nobles (mostly in Gera); the oldest is the Jugel stipend of {oldest[10]}. The {len(yr_post)} foundations from 1850 onwards are {'all' if len(yr_post)==len(yr_post_a) else 'partly'} sovereign."),
        bi(f"Die fünf Stiftungen, die nur ein Kapital nennen (Grimm, Weber, zweimal Friederici, Herzog), umfassen zusammen {D(cap_total)} Thaler (ohne die Friederici-Stiftung von 1857 über 1000 Gulden); alle sind zwischen 1835 und 1864 entstanden.",
           f"The five foundations that give only a capital (Grimm, Weber, Friederici twice, Herzog) amount to {E(cap_total)} Thaler together (without the Friederici foundation of 1857 of 1,000 gulden); all arose between 1835 and 1864."),
    ],
    "caveats": [
        bi("Die Zahl der Stipendiaten ist nicht immer genannt (dann ohne Betrag je Stipendiat); Brückner gibt Beträge teils je Person, teils insgesamt an. Bei mehreren Stiftungen entscheidet die Auswahl der Stiftungen mit Betrag über die Summen; die Stipendien in Mark und Aßo (Schleiz) sind nicht in Thaler umrechenbar und fehlen. Alle Beträge sind nominale Thaler ohne Berücksichtigung der Kaufkraft.",
           "The number of recipients is not always given (then no amount per recipient); Brückner gives amounts partly per person, partly in total. The sums depend on which foundations state an amount; the stipends in Mark and Aßo (Schleiz) cannot be converted into Thaler and are missing. All amounts are nominal Thaler without regard to purchasing power."),
        bi("Das Gründungsjahr ist dort angegeben, wo Brückner es nennt (Urkunde oder Testament); beim langenbergischen Stipendium sind zwei Stiftungen (1714 und 1731) zusammengefasst, bei den saalburger Stipendien datiert 1866 nur das zweite. Die Spalte »Stifter« ordnet nach Landesherr (Fürst, höchste Urkunde) und Bürgern, Beamten und Adel.",
           "The founding year is given where Brückner states it (deed or will); for the Langenberg stipend two foundations (1714 and 1731) are combined, for the Saalburg stipends only the second is dated 1866. The column “donor” sorts into sovereign (prince, supreme deed) and citizens, officials and nobility."),
    ],
    "datasets": [
        {"name": "stipends", "title": bi("Stipendien und Schulstiftungen mit Jahresbetrag", "Stipends and school foundations with an annual amount"),
         "columns": [
             col("key", "Kürzel", "Key", "string"),
             col("name_de", "Stiftung", "Foundation", "string"), col("name_en", "Stiftung (englisch)", "Foundation (English)", "string"),
             col("level_key", "Kürzel Stufe", "Level key", "string"),
             col("level_de", "Stufe", "Level", "string"), col("level_en", "Stufe (englisch)", "Level (English)", "string"),
             col("founder_key", "Kürzel Stifter", "Donor key", "string"),
             col("founder_de", "Stifter", "Donor", "string"), col("founder_en", "Stifter (englisch)", "Donor (English)", "string"),
             col("place", "Ort", "Place", "string"),
             col("year", "Gründungsjahr", "Founding year", "integer"),
             col("recipients", "Zahl der Stipendiaten", "Number of recipients", "integer", "Personen", derived=True, note="aus den ausgeschriebenen Zahlwörtern übertragen"),
             col("per_recipient", "Betrag je Stipendiat", "Amount per recipient", "number", "Thaler", derived=True, note="in Dezimal-Thaler umgerechnet"),
             col("annual_total", "Jahresbetrag insgesamt", "Annual total", "number", "Thaler", derived=True),
             col("capital", "Kapital", "Capital", "integer", "Thaler"),
         ],
         "rows": with_total, "source_refs": [{"page": "304", "block": "b6", "rows": "i1-i5"}, {"page": "305", "block": "b1"}, {"page": "305", "block": "b3"}, {"page": "305", "block": "b4"}, {"page": "305", "block": "b5"},
                                            {"page": "305", "block": "b6"}, {"page": "305", "block": "b7"}, {"page": "305", "block": "b8"}, {"page": "306", "block": "b3"}, {"page": "306", "block": "b4"}, {"page": "306", "block": "b6"},
                                            {"page": "307", "block": "b6", "rows": "i1"}, {"page": "308", "block": "b6"}, {"page": "308", "block": "b9"}, {"page": "308", "block": "b10"}]},
        {"name": "capital_only", "title": bi("Stiftungen mit genanntem Kapital", "Foundations with a stated capital"),
         "columns": [
             col("key", "Kürzel", "Key", "string"),
             col("name_de", "Stiftung", "Foundation", "string"), col("name_en", "Stiftung (englisch)", "Foundation (English)", "string"),
             col("level_key", "Kürzel Stufe", "Level key", "string"),
             col("level_de", "Stufe", "Level", "string"), col("level_en", "Stufe (englisch)", "Level (English)", "string"),
             col("year", "Gründungsjahr", "Founding year", "integer"),
             col("capital", "Kapital", "Capital", "integer", "Thaler"),
         ],
         "rows": [[r[0], r[1], r[2], r[3], r[4], r[5], r[10], r[14]] for r in cap_rows if r[0].startswith("k")],
         "source_refs": [{"page": "305", "block": "b9"}, {"page": "305", "block": "b11"}, {"page": "305", "block": "b12"}, {"page": "306", "block": "b7"}, {"page": "306", "block": "b9"}, {"page": "307", "block": "b1"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "stipends",
         "title": bi("Jahresbeträge der Stipendien und Schulstiftungen", "Annual amounts of the stipends and school foundations"),
         "caption": bi("Thaler jährlich insgesamt je Stiftung; Farbe = Schulstufe.", "Thaler per year in total per foundation; colour = school level."),
         "vegalite": {
             "height": 440,
             "mark": "bar",
             "encoding": {
                 "y": {"field": F("name"), "type": "nominal", "sort": "-x", "title": None, "axis": {"labelLimit": 380}},
                 "x": {"field": "annual_total", "type": "quantitative", "title": bi("Thaler im Jahr", "Thaler per year")},
                 "color": {"field": F("level"), "type": "nominal", "title": None, "sort": {"field": "level_key", "op": "min"}, "legend": {"labelLimit": 300, "columns": 2}},
                 "tooltip": [ttf("name", "Stiftung", "Foundation"), ttf("level", "Stufe", "Level"), ttf("founder", "Stifter", "Donor"), {"field": "annual_total", "title": bi("Thaler im Jahr", "Thaler per year"), "format": ".1f"}, tt("recipients", "Stipendiaten", "Recipients"), tt("year", "Gründungsjahr", "Founding year")]}}},
        {"id": "c2", "dataset": "stipends",
         "title": bi("Gründungsjahr und Jahresbetrag", "Founding year and annual amount"),
         "caption": bi("Nur Stiftungen mit Jahresbetrag und Jahreszahl (1615–1866). Bis 1783 stiften überwiegend Bürger, Beamte und Adlige; die Stiftungen ab 1850 sind landesherrlich.", "Only foundations with an annual amount and a year (1615–1866). Until 1783 mostly citizens, officials and nobles are the donors; the foundations from 1850 onwards are sovereign."),
         "vegalite": {
             "height": 300,
             "transform": [{"filter": "datum.year != null"}],
             "mark": {"type": "point", "filled": True, "size": 120},
             "encoding": {
                 "x": {"field": "year", "type": "quantitative", "title": bi("Gründungsjahr", "Founding year"), "axis": {"format": "d"}, "scale": {"domain": [1600, 1880]}},
                 "y": {"field": "annual_total", "type": "quantitative", "title": bi("Thaler im Jahr", "Thaler per year"), "scale": {"zero": True}},
                 "color": {"field": F("founder"), "type": "nominal", "title": None, "sort": {"field": "founder_key", "op": "min"}, "legend": {"labelLimit": 300}},
                 "tooltip": [ttf("name", "Stiftung", "Foundation"), tt("year", "Gründungsjahr", "Founding year"), {"field": "annual_total", "title": bi("Thaler im Jahr", "Thaler per year"), "format": ".1f"}]}}},
        {"id": "c3", "dataset": "capital_only",
         "title": bi("Stiftungen mit Kapitalangabe", "Foundations with a stated capital"),
         "caption": bi("Kapital in Thalern; die Friederici-Stiftung von 1857 (1000 Gulden) fehlt.", "Capital in Thaler; the Friederici foundation of 1857 (1,000 gulden) is missing."),
         "vegalite": {
             "height": 200,
             "mark": "bar",
             "encoding": {
                 "y": {"field": F("name"), "type": "nominal", "sort": "-x", "title": None, "axis": {"labelLimit": 360}},
                 "x": {"field": "capital", "type": "quantitative", "title": bi("Kapital (Thaler)", "Capital (Thaler)"), "axis": {"format": ",d"}},
                 "color": {"field": F("level"), "type": "nominal", "title": None, "sort": {"field": "level_key", "op": "min"}},
                 "tooltip": [ttf("name", "Stiftung", "Foundation"), tt("year", "Gründungsjahr", "Founding year"), {"field": "capital", "title": bi("Kapital (Thaler)", "Capital (Thaler)"), "format": ","}]}}},
    ],
    "keywords": {"de": ["Stipendien", "Stiftungen", "Freitische", "Gymnasium Gera", "Studenten", "Landesschule", "Lehrerseminar", "Schulstiftungen"],
                 "en": ["stipends", "foundations", "free tables", "Gymnasium Gera", "students", "teacher training", "school foundations"]},
}
write(ana)
