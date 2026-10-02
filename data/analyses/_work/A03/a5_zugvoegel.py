"""Analysis 5: arrival and departure of migratory birds at Gera 1859-1864 (p. 61, block b5)."""
import re
import statistics as st
from common import *

SPECIES = {  # printed name -> (German, English, label side, label dy)
    "Lerche": ("Lerche", "Skylark", "left", 0),
    "Bachstelze": ("Bachstelze", "Wagtail (unspecified)", "left", 13),
    "Hausschwalbe": ("Hausschwalbe", "House swallow (uncertain)", "right", 0),
    "Schwarzk. Grasmücke": ("Mönchsgrasmücke", "Blackcap", "left", 0),
    "Turmschwalbe": ("Turmschwalbe", "Common swift", "right", 0),
    "Pirol": ("Pirol", "Golden oriole", "right", 0),
    "Kukuk": ("Kuckuck", "Common cuckoo", "left", 0),
    "Mehlschwalbe": ("Mehlschwalbe", "House martin", "right", 0),
    "Ringeltaube": ("Ringeltaube", "Wood pigeon", "left", 0),
    "Rauchschwalbe": ("Rauchschwalbe", "Barn swallow", "left", 0),
    "Hausrothschwanz": ("Hausrotschwanz", "Black redstart", "right", 3),
    "Staar": ("Star", "Starling", "left", 0),
    "Waldschnepfe": ("Waldschnepfe", "Woodcock", "right", -3),
    "Weiße Bachstelze": ("Weiße Bachstelze", "White wagtail", "left", -3),
}
YEARS = [1859, 1860, 1861, 1862, 1863, 1864]


def pdate(s):
    s = s.strip()
    if s in ("—", ""):
        return None
    m = re.match(r"^(\d+)\.(?:-(\d+)\.)?\s*/(\d+)\.?$", s)
    assert m, repr(s)
    d1 = int(m.group(1))
    d2 = int(m.group(2)) if m.group(2) else d1
    return int(m.group(3)), d1, d2


def iso(y, mo, d):
    return f"{y}-{mo:02d}-{d:02d}"


g = grid("61", "b5")
assert g[0][1] == "1859." and g[1][1] == "Ank." and g[1][2] == "Abz."
obs = []
for r in g[2:]:
    sp = r[0]
    de, en, _, _ = SPECIES[sp]
    for i, y in enumerate(YEARS):
        ca, cd = r[1 + 2 * i], r[2 + 2 * i]
        a, d = pdate(ca), pdate(cd)
        if not a and not d:
            continue
        a_s = a_e = d_s = d_e = None
        a_doy = d_doy = stay = None
        if a:
            a_s, a_e = iso(y, a[0], a[1]), iso(y, a[0], a[2])
            a_doy = (doy(a[0], a[1]) + doy(a[0], a[2])) / 2
        if d:
            d_s, d_e = iso(y, d[0], d[1]), iso(y, d[0], d[2])
            d_doy = (doy(d[0], d[1]) + doy(d[0], d[2])) / 2
        if a and d:
            stay = d_doy - a_doy
        obs.append([sp, de, en, y, a_s, a_e, d_s, d_e, ca.strip() if a else None, cd.strip() if d else None, a_doy, d_doy, stay])
print(len(obs), "species-year rows")

# ---- species table ----------------------------------------------------------------------------
spec_rows = []
for sp, (de, en, align, dy) in SPECIES.items():
    o = [x for x in obs if x[0] == sp]
    a = [x[10] for x in o if x[10] is not None]
    d = [x[11] for x in o if x[11] is not None]
    pr = [x[12] for x in o if x[12] is not None]
    spec_rows.append([sp, de, en, len(a), len(d), len(pr), round(st.mean(a), 1), round(st.mean(d), 1), (round(st.mean(pr), 1) if pr else None), align, dy])
xs = [r[6] for r in spec_rows]
ys = [r[7] for r in spec_rows]
slope, icpt = st.linear_regression(xs, ys)
r_sp = st.correlation(xs, ys)
pairs = [x for x in obs if x[12] is not None]
r_pairs = st.correlation([p[10] for p in pairs], [p[11] for p in pairs])
x0, x1 = 25.0, 140.0
trend_rows = [[x0, round(slope * x0 + icpt, 1), x1, round(slope * x1 + icpt, 1)]]
print("r species", r_sp, "r pairs", r_pairs, len(pairs), "slope", slope)

MON_DE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
MON_EN = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def md(d):
    d = int(round(d))
    m = max(i for i in range(12) if CUM[i] < d)
    return m, d - CUM[m]


def dde(d):
    m, k = md(d)
    return f"{k}. {MON_DE[m]}"


def den(d):
    m, k = md(d)
    return f"{MON_EN[m]} {k}"


arr = [x for x in obs if x[10] is not None]
dep = [x for x in obs if x[11] is not None]
a_min = min(arr, key=lambda x: x[10]); a_max = max(arr, key=lambda x: x[10])
d_min = min(dep, key=lambda x: x[11]); d_max = max(dep, key=lambda x: x[11])
print(len(arr), len(dep), a_min[:4], a_max[:4], d_min[:4], d_max[:4])
by_arr = sorted(spec_rows, key=lambda r: r[6])
early, late = by_arr[:2], by_arr[-2:]
with_pairs = [r for r in spec_rows if r[8] is not None]
short = min(with_pairs, key=lambda r: r[8])
long_ = max(with_pairs, key=lambda r: r[8])
# year-to-year spread of arrival for species with >= 4 arrival records
spr = {}
for sp in SPECIES:
    a = [x[10] for x in obs if x[0] == sp and x[10] is not None]
    if len(a) >= 4:
        spr[sp] = max(a) - min(a)
sp_big = max(spr, key=spr.get)
within = {}
for sp in SPECIES:
    pr = [x for x in obs if x[0] == sp and x[12] is not None]
    if len(pr) >= 3:
        within[sp] = st.correlation([x[10] for x in pr], [x[11] for x in pr])
w_lo, w_hi = min(within.values()), max(within.values())
print(spr, within)
assert len(within) == 7 and len(pairs) == 32 and len(SPECIES) * len(YEARS) == 84

F, E = fde, fen
LINE = lambda s: s
ana = {
    "id": "phaenologie-zugvoegel-gera-1859-1864",
    "title": bi("Ankunft und Abzug der Zugvögel in Gera 1859–1864", "Arrival and departure of migratory birds at Gera, 1859–1864"),
    "category": "phenology",
    "section": "t1-1-7",
    "sources": [
        {"page": "61", "block": "b4"},
        {"page": "61", "block": "b5", "rows": "r1-r16"},
    ],
    "summary": bi(
        f"Ludwig Müller beobachtete in Gera von 1859 bis 1864 Ankunft und Abzug von 14 Zugvogelarten; Brückner druckt die Termine der Arten, für die Ankunft und Abzug angegeben sind. Es liegen {len(arr)} Ankunfts- und {len(dep)} Abzugsdaten vor, davon {len(pairs)} vollständige Paare. Die Ankunft reicht vom {dde(a_min[10])} bis zum {dde(a_max[10])}, der Abzug vom {dde(d_min[11])} bis zum {dde(d_max[11])}; je später die Art ankommt, desto früher zieht sie ab.",
        f"Ludwig Müller observed the arrival and departure of 14 migratory bird species at Gera from 1859 to 1864; Brückner prints the dates of the species for which arrival and departure are given. There are {len(arr)} arrival and {len(dep)} departure dates, {len(pairs)} of them complete pairs. Arrival ranges from {den(a_min[10])} to {den(a_max[10])}, departure from {den(d_min[11])} to {den(d_max[11])}; the later a species arrives, the earlier it leaves."),
    "method": bi(
        "Die Brüche der Tabelle (»15./2.« = Tag/Monat) wurden in ISO-Daten umgesetzt; Tagesspannen (»21.–26./4.«, in drei Fällen für die Ankunft, einmal »2.–9./5.«) werden als Anfang und Ende geführt und in den Diagrammen mit ihrer Mitte (Tag im Jahr, normiertes Jahr ohne Schalttag) gezeichnet. Die Aufenthaltsdauer ist Abzug minus Ankunft im selben Jahr, nur bei vollständigem Paar. Die Artmittel in Abb. 3 sind Mittel aller vorhandenen Ankunfts- bzw. Abzugsdaten der Art (unterschiedliche Jahre). Deutsche Namen sind modernisiert, englische Namen und Arten editorisch zugeordnet; wo die Zuordnung unsicher ist (Hausschwalbe, Bachstelze), steht das im Namen (Turmschwalbe = Mauersegler, Schwarzköpfige Grasmücke = Mönchsgrasmücke). Die Trendgerade ist die lineare Regression der mittleren Abzugs- auf die mittleren Ankunftstermine der 14 Arten.",
        "The fractions of the table (“15./2.” = day/month) were converted to ISO dates; day ranges (“21.–26./4.”, three arrival cases, plus one “2.–9./5.”) are kept as start and end and are drawn at their midpoint in the charts (day of year in a normalised year without a leap day). The length of stay is departure minus arrival in the same year, for complete pairs only. The species means in chart 3 are means of all available arrival and departure dates of the species (from different years). German names are modernised, English names and species assigned editorially; where the assignment is uncertain (house swallow, wagtail) this is stated in the name (Turmschwalbe = common swift, Schwarzköpfige Grasmücke = blackcap). The trend line is the linear regression of the mean departure on the mean arrival dates of the 14 species."),
    "findings": [
        bi(f"Die Ankunftstermine liegen zwischen dem {dde(a_min[10])} ({SPECIES[a_min[0]][0]} {a_min[3]}) und dem {dde(a_max[10])} ({SPECIES[a_max[0]][0]} {a_max[3]}), die Abzugstermine zwischen dem {dde(d_min[11])} ({SPECIES[d_min[0]][0]} {d_min[3]}) und dem {dde(d_max[11])} ({SPECIES[d_max[0]][0]} {d_max[3]}) – übereinstimmend mit Brückners Angabe »letztes Drittel des Januar« bis »Beginn des August« bis »Mitte November«.",
           f"Arrival dates lie between {den(a_min[10])} ({SPECIES[a_min[0]][1]} {a_min[3]}) and {den(a_max[10])} ({a_max[2]} {a_max[3]}), departure dates between {den(d_min[11])} ({d_min[2]} {d_min[3]}) and {den(d_max[11])} ({d_max[2]} {d_max[3]}) – in line with Brückner’s statement of “last third of January” and “beginning of August” to “mid-November”."),
        bi(f"Am frühesten kommen im Mittel {early[0][1]} ({dde(early[0][6])}) und {early[1][1]} ({dde(early[1][6])}), am spätesten {late[1][1]} ({dde(late[1][6])}) und {late[0][1]} ({dde(late[0][6])}).",
           f"On average the earliest arrivals are {early[0][2]} ({den(early[0][6])}) and {early[1][2]} ({den(early[1][6])}), the latest {late[1][2]} ({den(late[1][6])}) and {late[0][2]} ({den(late[0][6])})."),
        bi(f"Brückners Satz »je später die Ankunft, desto früher der Wegzug« gilt zwischen den Arten: Die mittleren Termine der 14 Arten korrelieren mit r = {F(r_sp,2)}, die {len(pairs)} Paare mit r = {F(r_pairs,2)}. Die Aufenthaltsdauer reicht im Mittel von {F(short[8],0)} Tagen ({short[1]}) bis {F(long_[8],0)} Tagen ({long_[1]}).",
           f"Brückner’s statement “the later the arrival, the earlier the departure” holds between species: the mean dates of the 14 species correlate with r = {E(r_sp,2)}, the {len(pairs)} pairs with r = {E(r_pairs,2)}. The mean length of stay ranges from {E(short[8],0)} days ({short[2]}) to {E(long_[8],0)} days ({long_[2]})."),
        bi(f"Von Jahr zu Jahr innerhalb einer Art zeigt sich dagegen kein einheitliches Muster: bei den sieben Arten mit mindestens drei vollständigen Paaren liegt die Korrelation zwischen Ankunft und Abzug zwischen {F(w_lo,2)} und {F(w_hi,2)}. Die Ankunft derselben Art streut stark (größte Spanne: {SPECIES[sp_big][0]}, {F(spr[sp_big],0)} Tage).",
           f"Within a species from year to year, by contrast, no uniform pattern appears: for the seven species with at least three complete pairs the correlation between arrival and departure lies between {E(w_lo,2)} and {E(w_hi,2)}. The arrival of one species scatters widely (largest span: {SPECIES[sp_big][1]}, {E(spr[sp_big],0)} days)."),
    ],
    "caveats": [
        bi("Ein Beobachter, sechs Jahre; die Tabelle enthält nur Arten, bei denen laut Brückner Ankunft und Abzug angegeben sind, in den Einzeljahren aber oft nur eines von beiden (Lücken »—«). Nur 32 von 84 möglichen Art-Jahr-Kombinationen haben ein vollständiges Paar. Die Zahlen sind deshalb kein Mittel gleicher Jahre.",
           "One observer, six years; the table contains only species for which, according to Brückner, arrival and departure are given, but in single years often only one of the two (gaps “—”). Only 32 of 84 possible species-year combinations have a complete pair. The figures are therefore no mean over equal years."),
        bi("Brückner nennt als Ende der Ankunftsperiode »Mitte Juni«; die späteste Ankunft in der gedruckten Tabelle ist der 1. Juni (Pirol 1859). Der Text bezieht sich offenbar auch auf nicht abgedruckte Arten.",
           "Brückner gives “mid-June” as the end of the arrival period; the latest arrival in the printed table is 1 June (golden oriole 1859). The text evidently also refers to species not printed."),
        bi("Die Artbestimmung der alten Namen ist unsicher: »Hausschwalbe« (neben Rauch- und Mehlschwalbe aufgeführt) kann Rauch- oder Mehlschwalbe meinen, »Bachstelze« neben der Weißen Bachstelze eine andere Bachstelzenart; »Lerche« wird als Feldlerche gelesen. Die Namen wurden nicht zusammengelegt.",
           "The identification of the old names is uncertain: “Hausschwalbe” (listed besides barn and house martin) may mean either, “Bachstelze” besides the white wagtail another wagtail species; “Lerche” is read as skylark. The names were not merged."),
        bi("Terminangaben sind Tagesdaten ohne Angabe, ob sie das erste Tier, den Hauptzug oder den letzten Nachzügler meinen; Überwinterer (Lerche, Star, Bachstelze) sind in milden Wintern kaum von Zugvögeln zu trennen.",
           "The dates are day dates without saying whether they refer to the first bird, the main passage or the last straggler; partial migrants (lark, starling, wagtail) are hard to separate from migrants in mild winters."),
    ],
    "conversions": [
        {"from": "Datumsbruch (Tag./Monat.)", "to": "ISO-Datum und Tag im Jahr", "factor_or_formula": "Tag im Jahr = Tage vor Monatsbeginn (Nicht-Schaltjahr) + Tag; bei Tagesspannen Mitte der Spanne", "reference": "Brückner S. 60: Monat als Nenner, Tag als Zähler eines Bruches"},
    ],
    "datasets": [
        {"name": "observations", "title": bi("Ankunft und Abzug je Art und Jahr", "Arrival and departure by species and year"),
         "columns": [
             {"name": "species_printed", "label": bi("Name im Druck", "Name as printed"), "type": "string", "unit": None},
             {"name": "species_de", "label": bi("Deutscher Name", "German name"), "type": "string", "unit": None},
             {"name": "species_en", "label": bi("Englischer Name", "English name"), "type": "string", "unit": None},
             {"name": "year", "label": YEAR, "type": "integer", "unit": None},
             {"name": "arrival_start", "label": bi("Ankunft (frühester Tag)", "Arrival (first day)"), "type": "date", "unit": None, "derived": True},
             {"name": "arrival_end", "label": bi("Ankunft (letzter Tag)", "Arrival (last day)"), "type": "date", "unit": None, "derived": True},
             {"name": "departure_start", "label": bi("Abzug (frühester Tag)", "Departure (first day)"), "type": "date", "unit": None, "derived": True},
             {"name": "departure_end", "label": bi("Abzug (letzter Tag)", "Departure (last day)"), "type": "date", "unit": None, "derived": True},
             {"name": "arrival_printed", "label": bi("Ankunft gedruckt", "Arrival as printed"), "type": "string", "unit": None},
             {"name": "departure_printed", "label": bi("Abzug gedruckt", "Departure as printed"), "type": "string", "unit": None},
             {"name": "arrival_doy", "label": bi("Ankunft (Tag im Jahr)", "Arrival (day of year)"), "type": "number", "unit": "d", "derived": True, "note": "Mitte der Spanne, normiertes Jahr ohne Schalttag"},
             {"name": "departure_doy", "label": bi("Abzug (Tag im Jahr)", "Departure (day of year)"), "type": "number", "unit": "d", "derived": True, "note": "Mitte der Spanne, normiertes Jahr ohne Schalttag"},
             {"name": "stay_days", "label": bi("Aufenthaltsdauer", "Length of stay"), "type": "number", "unit": "d", "derived": True},
         ],
         "rows": obs, "source_refs": [{"page": "61", "block": "b5", "rows": "r3-r16"}]},
        {"name": "species", "title": bi("Mittlere Termine je Art", "Mean dates by species"),
         "columns": [
             {"name": "species_printed", "label": bi("Name im Druck", "Name as printed"), "type": "string", "unit": None},
             {"name": "species_de", "label": bi("Deutscher Name", "German name"), "type": "string", "unit": None},
             {"name": "species_en", "label": bi("Englischer Name", "English name"), "type": "string", "unit": None},
             {"name": "n_arrival", "label": bi("Zahl der Ankunftsdaten", "Number of arrival dates"), "type": "integer", "unit": None, "derived": True},
             {"name": "n_departure", "label": bi("Zahl der Abzugsdaten", "Number of departure dates"), "type": "integer", "unit": None, "derived": True},
             {"name": "n_pairs", "label": bi("Zahl vollständiger Paare", "Number of complete pairs"), "type": "integer", "unit": None, "derived": True},
             {"name": "mean_arrival_doy", "label": bi("Mittlere Ankunft (Tag im Jahr)", "Mean arrival (day of year)"), "type": "number", "unit": "d", "derived": True},
             {"name": "mean_departure_doy", "label": bi("Mittlerer Abzug (Tag im Jahr)", "Mean departure (day of year)"), "type": "number", "unit": "d", "derived": True},
             {"name": "mean_stay_days", "label": bi("Mittlere Aufenthaltsdauer", "Mean length of stay"), "type": "number", "unit": "d", "derived": True},
             {"name": "label_align", "label": bi("Beschriftung (Seite)", "Label side"), "type": "string", "unit": None, "note": "nur für das Diagramm"},
             {"name": "label_dy", "label": bi("Beschriftung (Versatz)", "Label offset"), "type": "integer", "unit": None, "derived": True, "note": "nur für das Diagramm"},
         ],
         "rows": spec_rows, "source_refs": [{"page": "61", "block": "b5", "rows": "r3-r16"}]},
        {"name": "trend", "title": bi("Trendgerade Ankunft–Abzug", "Arrival–departure trend line"),
         "columns": [
             {"name": "x0", "label": bi("Ankunft Anfang", "Arrival start"), "type": "number", "unit": "d", "derived": True},
             {"name": "y0", "label": bi("Abzug Anfang", "Departure start"), "type": "number", "unit": "d", "derived": True},
             {"name": "x1", "label": bi("Ankunft Ende", "Arrival end"), "type": "number", "unit": "d", "derived": True},
             {"name": "y1", "label": bi("Abzug Ende", "Departure end"), "type": "number", "unit": "d", "derived": True},
         ],
         "rows": trend_rows, "source_refs": [{"page": "61", "block": "b5", "rows": "r3-r16"}]},
    ],
}

# ---- charts -------------------------------------------------------------------------------------------------
sp_name = bi("datum.species_de", "datum.species_en")
order = [bi(SPECIES[r[0]][0], SPECIES[r[0]][1]) for r in by_arr]
order_pairs = [bi(SPECIES[r[0]][0], SPECIES[r[0]][1]) for r in by_arr if r[5] > 0]
y_sp = lambda srt=None: {"field": "sp", "type": "nominal", "title": None, "sort": srt or order}
x_date = lambda title: {"type": "quantitative", "title": title, "axis": doy_axis(1, 11), "scale": {"domain": [10, 330], "nice": False}}
YR_DOM = YEARS
col_year = {"field": "year", "type": "nominal", "title": YEAR, "scale": {"domain": YEARS}}

c1 = {"id": "c1", "dataset": "observations",
      "title": bi("Aufenthalt von der Ankunft bis zum Abzug", "Stay from arrival to departure"),
      "caption": bi("Je Balken ein Jahr, von der Ankunft bis zum Abzug (nur Arten und Jahre mit beiden Terminen), nach mittlerer Ankunft geordnet. Frühankömmlinge wie die Lerche bleiben bis in den November, Spätankömmlinge wie Turmschwalbe und Pirol ziehen schon im August ab.",
                    "One bar per year, from arrival to departure (only species and years with both dates), ordered by mean arrival. Early arrivals such as the lark stay until November, late arrivals such as swift and oriole leave as early as August."),
      "vegalite": {
          "height": 520,
          "transform": [{"filter": "isValid(datum.stay_days)"}, {"calculate": sp_name, "as": "sp"}],
          "mark": {"type": "bar", "cornerRadiusEnd": 2},
          "encoding": {
              "x": {"field": "arrival_doy", "type": "quantitative", "title": bi("Tag des Jahres (Ankunft → Abzug)", "Day of the year (arrival → departure)"), "axis": doy_axis(1, 11), "scale": {"domain": [10, 330], "nice": False}},
              "x2": {"field": "departure_doy"},
              "y": y_sp(order_pairs), "yOffset": {"field": "year"}, "color": col_year,
              "tooltip": [tip("species_de", "Art", "Species"), tip("species_en", "Englisch", "English"), tip("year", "Jahr", "Year"),
                          tip("arrival_printed", "Ankunft (gedruckt)", "Arrival (printed)"), tip("departure_printed", "Abzug (gedruckt)", "Departure (printed)"), tip("stay_days", "Aufenthalt (Tage)", "Stay (days)", ".0f")]}}}

EVT = {"arrival_doy": bi("Ankunft", "Arrival"), "departure_doy": bi("Abzug", "Departure")}
ev_expr = bi("datum.key == 'arrival_doy' ? 'Ankunft' : 'Abzug'", "datum.key == 'arrival_doy' ? 'Arrival' : 'Departure'")
c2 = {"id": "c2", "dataset": "observations",
      "title": bi("Alle Ankunfts- und Abzugstermine nach Art", "All arrival and departure dates by species"),
      "caption": bi("Jeder Punkt ist ein beobachtetes Jahr (bei Tagesspannen die Mitte); der Strich verbindet früheste und späteste Beobachtung der Art. Arten nach mittlerer Ankunft geordnet.",
                    "Each dot is an observed year (midpoint for day ranges); the line joins the earliest and latest observation of the species. Species ordered by mean arrival."),
      "vegalite": {
          "height": 440,
          "transform": [{"calculate": sp_name, "as": "sp"}, {"fold": ["arrival_doy", "departure_doy"], "as": ["key", "value"]}, {"filter": "isValid(datum.value)"}, {"calculate": ev_expr, "as": "event"}],
          "layer": [
              {"transform": [{"aggregate": [{"op": "min", "field": "value", "as": "lo"}, {"op": "max", "field": "value", "as": "hi"}], "groupby": ["sp", "event"]}],
               "mark": {"type": "rule", "strokeWidth": 2, "opacity": 0.5},
               "encoding": {"x": {"field": "lo", "type": "quantitative", "title": bi("Tag des Jahres", "Day of the year"), "axis": doy_axis(1, 11), "scale": {"domain": [10, 330], "nice": False}}, "x2": {"field": "hi"}, "y": y_sp(),
                            "color": {"field": "event", "type": "nominal", "title": None, "scale": {"domain": [EVT["arrival_doy"], EVT["departure_doy"]]}}}},
              {"mark": {"type": "circle", "size": 70, "opacity": 0.9},
               "encoding": {"x": {"field": "value", "type": "quantitative", "title": bi("Tag des Jahres", "Day of the year"), "axis": doy_axis(1, 11), "scale": {"domain": [10, 330], "nice": False}},
                            "y": y_sp(), "color": {"field": "event", "type": "nominal", "title": None, "scale": {"domain": [EVT["arrival_doy"], EVT["departure_doy"]]}},
                            "tooltip": [tip("species_de", "Art", "Species"), tip("species_en", "Englisch", "English"), tip("year", "Jahr", "Year"), tip("event", "Ereignis", "Event"),
                                        tip("arrival_printed", "Ankunft (gedruckt)", "Arrival (printed)"), tip("departure_printed", "Abzug (gedruckt)", "Departure (printed)")]}},
          ]}}

def lab(align, dy):
    return {"transform": [{"filter": f"datum.label_align == '{align}' && datum.label_dy == {dy}"}, {"calculate": sp_name, "as": "sp"}],
            "mark": {"type": "text", "align": "left" if align == "right" else "right", "dx": 9 if align == "right" else -9, "dy": dy, "fontSize": 10},
            "encoding": {"x": {"field": "mean_arrival_doy", "type": "quantitative"}, "y": {"field": "mean_departure_doy", "type": "quantitative"},
                         "text": {"field": "sp", "type": "nominal"}}}


c3 = {"id": "c3", "dataset": "species", "extra_datasets": ["trend"],
      "title": bi("Mittlere Ankunft und mittlerer Abzug der Arten", "Mean arrival and mean departure of the species"),
      "caption": bi(f"Je Punkt eine Art (Mittel aller Beobachtungsjahre). Je später die Art im Mittel ankommt, desto früher zieht sie ab (r = {F(r_sp,2)}); die Gerade ist die Regression.",
                    f"One dot per species (mean over all observed years). The later a species arrives on average, the earlier it leaves (r = {E(r_sp,2)}); the line is the regression."),
      "vegalite": {
          "height": 380,
          "layer": [
              {"data": {"name": "trend"}, "mark": {"type": "rule", "strokeDash": [5, 4]},
               "encoding": {"x": {"field": "x0", "type": "quantitative", "scale": {"domain": [20, 150], "nice": False}}, "x2": {"field": "x1"},
                            "y": {"field": "y0", "type": "quantitative", "scale": {"domain": [200, 330], "nice": False}}, "y2": {"field": "y1"}}},
              {"transform": [{"calculate": sp_name, "as": "sp"}],
               "mark": {"type": "circle", "size": 100, "opacity": 1},
               "encoding": {"x": {"field": "mean_arrival_doy", "type": "quantitative", "title": bi("Mittlere Ankunft", "Mean arrival"), "axis": doy_axis(1, 6), "scale": {"domain": [20, 150], "nice": False}},
                            "y": {"field": "mean_departure_doy", "type": "quantitative", "title": bi("Mittlerer Abzug", "Mean departure"), "axis": {k: v for k, v in doy_axis(8, 11).items()}, "scale": {"domain": [200, 330], "nice": False}},
                            "tooltip": [tip("species_de", "Art", "Species"), tip("species_en", "Englisch", "English"), tip("n_arrival", "Ankunftsdaten", "Arrival dates"), tip("n_departure", "Abzugsdaten", "Departure dates"),
                                        tip("mean_arrival_doy", "Mittlere Ankunft (Tag im Jahr)", "Mean arrival (day of year)", ".0f"), tip("mean_departure_doy", "Mittlerer Abzug (Tag im Jahr)", "Mean departure (day of year)", ".0f")]}},
              *[lab(al, dy) for al, dy in sorted({(r[9], r[10]) for r in spec_rows})],
          ]}}

ana["charts"] = [c1, c2, c3]
ana["keywords"] = bi(["Zugvögel", "Vogelzug", "Ankunft", "Abzug", "Gera", "Lerche", "Schwalben", "Kuckuck", "Pirol", "Star", "Phänologie", "Ludwig Müller"],
                     ["migratory birds", "bird migration", "arrival", "departure", "Gera", "skylark", "swallows", "cuckoo", "golden oriole", "starling", "phenology", "Ludwig Müller"])
ana["related"] = ["phaenologie-bluetezeiten-gera-hohenleuben-1851-1861", "klima-gera-temperatur-1856-1867", "fauna-voegel-zugzeiten-und-seltene-gaeste"]
ana["supersedes_legacy"] = "p. 61 'Vogelzug in Gera (1859–1864) – Phänologische Analyse' (interaktives HTML, p61_birdviz)"
ana["generated_by"] = "Claude Sonnet 5.5 (subagent A03)"
ana["date"] = "2026-10-01"
write(ana)
