"""A09: Taubstumme und Blinde 1864 / 1867 (pp. 117-118)."""
import re
from common import *

D4 = ["Gera", "Schleiz", "Lobenstein-Ebersdorf", "Reuß j. L."]
gd = grid("117", "b4")
gb = grid("118", "b2")


def z(s):
    """'—' = none -> 0.0, else number"""
    return 0.0 if str(s).strip() in ("—", "–") else num(s)


rows = []
AREAS3 = [("Städte", 0), ("Landorte", 6), ("Überhaupt", 12)]
for i in range(8):
    k = D4[i // 2]
    rd = gd[3 + i]
    year = int(rd[1])
    # deaf-mute: [label, year, then 18 values]
    vals = rd[2:]
    for area, off in AREAS3:
        cm, cw, ct = [int(z(v)) for v in vals[off:off + 3]]
        rm, rw, rt = [z(v) for v in vals[off + 3:off + 6]]
        rows.append(["Taubstumme", k, year, area, cm, cw, ct, rm, rw, rt])
    rb = gb[3 + i]
    year_b = int(re.search(r"(\d{4})", rb[0]).group(1))
    assert year_b == year, (year_b, year)
    vals = rb[1:]
    for area, off in AREAS3:
        cm, cw, ct = [int(z(v)) for v in vals[off:off + 3]]
        rm, rw, rt = [z(v) for v in vals[off + 3:off + 6]]
        rows.append(["Blinde", k, year_b, area, cm, cw, ct, rm, rw, rt])
print(len(rows))

R = {(r[0], r[1], r[2], r[3]): r for r in rows}
def tot(c, k, y): return R[(c, k, y, "Überhaupt")][6]
def rate(c, k, y, a="Überhaupt"): return R[(c, k, y, a)][9]
def ratem(c, k, y, a="Überhaupt"): return R[(c, k, y, a)][7]
def ratew(c, k, y, a="Überhaupt"): return R[(c, k, y, a)][8]

# ---- checks of the claims
for c in ("Taubstumme", "Blinde"):
    for y in (1864, 1867):
        assert max(D4[:3], key=lambda k: rate(c, k, y)) == "Schleiz", (c, y)
        assert min(D4[:3], key=lambda k: rate(c, k, y)) == "Gera", (c, y)
for y in (1864, 1867):
    assert ratew("Blinde", "Reuß j. L.", y) > ratem("Blinde", "Reuß j. L.", y)
    assert ratem("Taubstumme", "Reuß j. L.", y) > ratew("Taubstumme", "Reuß j. L.", y)
    assert rate("Blinde", "Reuß j. L.", y, "Landorte") > rate("Blinde", "Reuß j. L.", y, "Städte")
print({(c, y): (tot(c, "Reuß j. L.", y), rate(c, "Reuß j. L.", y)) for c in ("Taubstumme", "Blinde") for y in (1864, 1867)})

F = "Reuß j. L."
T = "Taubstumme"
B = "Blinde"

ana = {
    "id": "gesundheit-taubstumme-blinde-1864-1867",
    "title": bi("Taubstumme und Blinde 1864 und 1867", "Deaf-mute and blind people, 1864 and 1867"),
    "category": "health",
    "section": "t1-2-1",
    "sources": [ref("117", "b3"), ref("117", "b4", "r4-r11"), ref("118", "b1"), ref("118", "b2", "r4-r11"), ref("118", "b3")],
    "summary": bi(
        f"Brückner zählt für 1864 und 1867 die Taubstummen und die Blinden je Landrathsbezirk, getrennt nach Städten, Landorten und Geschlecht, und gibt die Zahl auf 10 000 Einwohner an. 1864 gab es im Fürstenthum {tot(T, F, 1864)} Taubstumme ({fde(rate(T, F, 1864))} auf 10 000 Einwohner) und {tot(B, F, 1864)} Blinde ({fde(rate(B, F, 1864))}); 1867 waren es {tot(T, F, 1867)} ({fde(rate(T, F, 1867))}) und {tot(B, F, 1867)} ({fde(rate(B, F, 1867))}). Schleiz hat bei beiden Gebrechen die höchsten, Gera die niedrigsten Werte.",
        f"For 1864 and 1867 Brückner counts the deaf-mute and the blind per district, split into towns, rural places and sex, and gives the number per 10,000 inhabitants. In 1864 the principality had {tot(T, F, 1864)} deaf-mute people ({fen(rate(T, F, 1864))} per 10,000 inhabitants) and {tot(B, F, 1864)} blind people ({fen(rate(B, F, 1864))}); in 1867 the figures were {tot(T, F, 1867)} ({fen(rate(T, F, 1867))}) and {tot(B, F, 1867)} ({fen(rate(B, F, 1867))}). Schleiz has the highest values for both conditions, Gera the lowest."),
    "method": bi(
        "Die beiden Tabellen auf S. 117 (Taubstumme) und S. 118 (Blinde) nennen je Landrathsbezirk und Jahr (1864, 1867) die Zahl der Betroffenen (männlich, weiblich, zusammen) und die Zahl auf 10 000 Einwohner für Städte, Landorte und überhaupt. Die Werte stehen wie gedruckt im Datensatz (langes Format, eine Zeile je Gebrechen, Landrathsbezirk, Jahr und Gebiet); ein Strich „—“ der Vorlage ist als 0 eingetragen. Die Zeilen des Fürstenthums sind Brückners Summen.",
        "The two tables on p. 117 (deaf-mute) and p. 118 (blind) give for each district and year (1864, 1867) the number of persons affected (male, female, total) and the number per 10,000 inhabitants for towns, rural places and overall. The values are in the dataset as printed (long format, one row per condition, district, year and area); a dash “—” in the source is entered as 0. The rows for the principality are Brückner's totals."),
    "findings": [
        bi(f"Die Zahl der Taubstummen sank im Fürstenthum von {tot(T, F, 1864)} (1864) auf {tot(T, F, 1867)} (1867), die der Blinden blieb mit {tot(B, F, 1864)} und {tot(B, F, 1867)} fast gleich. Auf 10 000 Einwohner kommen 1867 {fde(rate(T, F, 1867))} Taubstumme und {fde(rate(B, F, 1867))} Blinde.",
           f"The number of deaf-mute people in the principality fell from {tot(T, F, 1864)} (1864) to {tot(T, F, 1867)} (1867), while the number of blind people stayed almost the same at {tot(B, F, 1864)} and {tot(B, F, 1867)}. Per 10,000 inhabitants there are {fen(rate(T, F, 1867))} deaf-mute and {fen(rate(B, F, 1867))} blind people in 1867."),
        bi(f"In beiden Jahren hat Schleiz bei Taubstummen ({fde(rate(T, 'Schleiz', 1864))} und {fde(rate(T, 'Schleiz', 1867))}) und Blinden ({fde(rate(B, 'Schleiz', 1864))} und {fde(rate(B, 'Schleiz', 1867))} auf 10 000) die höchsten Werte, Gera die niedrigsten (Taubstumme {fde(rate(T, 'Gera', 1864))} und {fde(rate(T, 'Gera', 1867))}, Blinde {fde(rate(B, 'Gera', 1864))} und {fde(rate(B, 'Gera', 1867))}). Brückner hält Schlüsse auf die Ursache wegen der kurzen Beobachtungszeit für unreif (S. 118).",
           f"In both years Schleiz has the highest values for the deaf-mute ({fen(rate(T, 'Schleiz', 1864))} and {fen(rate(T, 'Schleiz', 1867))}) and the blind ({fen(rate(B, 'Schleiz', 1864))} and {fen(rate(B, 'Schleiz', 1867))} per 10,000), Gera the lowest (deaf-mute {fen(rate(T, 'Gera', 1864))} and {fen(rate(T, 'Gera', 1867))}, blind {fen(rate(B, 'Gera', 1864))} and {fen(rate(B, 'Gera', 1867))}). Brückner considers conclusions about the cause premature because of the short period of observation (p. 118)."),
        bi(f"Unter den Blinden überwiegen die Frauen ({fde(ratem(B, F, 1864))} Männer gegenüber {fde(ratew(B, F, 1864))} Frauen auf 10 000 im Jahr 1864, {fde(ratem(B, F, 1867))} gegenüber {fde(ratew(B, F, 1867))} 1867), unter den Taubstummen die Männer ({fde(ratem(T, F, 1864))} gegenüber {fde(ratew(T, F, 1864))}, 1867 {fde(ratem(T, F, 1867))} gegenüber {fde(ratew(T, F, 1867))}).",
           f"Women predominate among the blind ({fen(ratem(B, F, 1864))} men against {fen(ratew(B, F, 1864))} women per 10,000 in 1864, {fen(ratem(B, F, 1867))} against {fen(ratew(B, F, 1867))} in 1867), men among the deaf-mute ({fen(ratem(T, F, 1864))} against {fen(ratew(T, F, 1864))}, 1867 {fen(ratem(T, F, 1867))} against {fen(ratew(T, F, 1867))})."),
        bi(f"Blinde sind auf dem Land häufiger als in den Städten ({fde(rate(B, F, 1864, 'Landorte'))} gegenüber {fde(rate(B, F, 1864, 'Städte'))} auf 10 000 im Jahr 1864, {fde(rate(B, F, 1867, 'Landorte'))} gegenüber {fde(rate(B, F, 1867, 'Städte'))} 1867); bei den Taubstummen ist das Bild uneinheitlich (1864 {fde(rate(T, F, 1864, 'Landorte'))} gegenüber {fde(rate(T, F, 1864, 'Städte'))}, 1867 {fde(rate(T, F, 1867, 'Landorte'))} gegenüber {fde(rate(T, F, 1867, 'Städte'))}). Den höchsten Einzelwert hat die Stadtbevölkerung von Schleiz mit {fde(rate(T, 'Schleiz', 1864, 'Städte'))} Taubstummen auf 10 000 (1864).",
           f"Blindness is more frequent in the countryside than in the towns ({fen(rate(B, F, 1864, 'Landorte'))} against {fen(rate(B, F, 1864, 'Städte'))} per 10,000 in 1864, {fen(rate(B, F, 1867, 'Landorte'))} against {fen(rate(B, F, 1867, 'Städte'))} in 1867); for the deaf-mute the picture is mixed (1864 {fen(rate(T, F, 1864, 'Landorte'))} against {fen(rate(T, F, 1864, 'Städte'))}, 1867 {fen(rate(T, F, 1867, 'Landorte'))} against {fen(rate(T, F, 1867, 'Städte'))}). The highest single value is for the urban population of Schleiz with {fen(rate(T, 'Schleiz', 1864, 'Städte'))} deaf-mute per 10,000 (1864)."),
    ],
    "caveats": [
        bi("Die Zahlen sind klein (in den Städten Geras 5 bzw. 6 Taubstumme, in denen Lobenstein-Ebersdorfs 4 bzw. 5; je Geschlecht oft nur 1 bis 5 Personen), die Raten daher sehr unsicher. Der Rückgang der Taubstummen in Schleiz (42 auf 31) und Lobenstein-Ebersdorf (21 auf 14) kann auf unterschiedlicher Erfassung beruhen; die Quelle nennt Zählweise und Definition nicht.",
           "The numbers are small (5 and 6 deaf-mute people in the towns of Gera, 4 and 5 in those of Lobenstein-Ebersdorf; often only 1 to 5 persons per sex), so the rates are very uncertain. The decline of the deaf-mute in Schleiz (42 to 31) and Lobenstein-Ebersdorf (21 to 14) may be due to differing enumeration; the source does not state counting method or definition."),
        bi("Zwei gedruckte Raten sind nicht mit den Zahlen vereinbar: Blinde, Gera 1867, Frauen überhaupt, 12,48 auf 10 000 (die Zahlen ergeben etwa 11,96); Blinde, Fürstenthum 1867, Städte zusammen, 10,06 (die Zahlen ergeben etwa 11,06). Die Werte stehen wie gedruckt im Datensatz.",
           "Two printed rates are not compatible with the counts: blind, Gera 1867, women overall, 12.48 per 10,000 (the counts give about 11.96); blind, principality 1867, towns combined, 10.06 (the counts give about 11.06). The values are in the dataset as printed."),
    ],
    "datasets": [
        {"name": "disability", "title": bi("Taubstumme und Blinde nach Landrathsbezirk, Jahr, Gebiet und Geschlecht", "Deaf-mute and blind people by district, year, area and sex"),
         "columns": [col("condition", "Gebrechen", "Condition", "string", note="Taubstumme / Blinde"),
                     col("district", "Landrathsbezirk", "District", "string", note="„Reuß j. L.“ = Fürstenthum insgesamt"),
                     col("year", "Jahr", "Year", "integer"),
                     col("area", "Gebiet", "Area", "string", note="Städte / Landorte / Überhaupt"),
                     col("count_m", "Zahl männlich", "Number, male", "integer", "Personen"),
                     col("count_w", "Zahl weiblich", "Number, female", "integer", "Personen"),
                     col("count_total", "Zahl zusammen", "Number, total", "integer", "Personen"),
                     col("per10k_m", "Auf 10 000 männliche Einwohner", "Per 10,000 male inhabitants", "number", "je 10 000"),
                     col("per10k_w", "Auf 10 000 weibliche Einwohner", "Per 10,000 female inhabitants", "number", "je 10 000"),
                     col("per10k_total", "Auf 10 000 Einwohner", "Per 10,000 inhabitants", "number", "je 10 000")],
         "rows": rows, "source_refs": [ref("117", "b4", "r4-r11"), ref("118", "b2", "r4-r11")]},
    ],
    "charts": [
        {"id": "c1", "dataset": "disability",
         "title": bi("Taubstumme auf 10 000 Einwohner", "Deaf-mute people per 10,000 inhabitants"),
         "caption": bi("Je Landrathsbezirk und für das Fürstenthum (Reuß j. L.), Städte und Landorte zusammen, 1864 und 1867.",
                       "By district and for the principality (Reuß j. L.), towns and rural places combined, 1864 and 1867."),
         "vegalite": {"height": 280, "transform": [{"filter": "datum.condition == 'Taubstumme' && datum.area == 'Überhaupt'"}], "mark": "bar",
                      "encoding": {
                          "x": {"field": "district", "type": "nominal", "sort": DISTRICTS, "title": DIST_TITLE, "axis": {"labelAngle": 0}},
                          "xOffset": {"field": "year", "type": "nominal"},
                          "y": {"field": "per10k_total", "type": "quantitative", "title": bi("auf 10 000 Einwohner", "per 10,000 inhabitants")},
                          "color": {"field": "year", "type": "nominal", "title": None, "scale": {"domain": [1864, 1867]}},
                          "tooltip": [tip("district", "Landrathsbezirk", "District"), tip("year", "Jahr", "Year"), tip("count_total", "Zahl der Taubstummen", "Number of deaf-mute people"),
                                      tip("per10k_total", "auf 10 000 Einwohner", "per 10,000 inhabitants", ".2f")]}}},
        {"id": "c2", "dataset": "disability",
         "title": bi("Blinde auf 10 000 Einwohner", "Blind people per 10,000 inhabitants"),
         "caption": bi("Je Landrathsbezirk und für das Fürstenthum (Reuß j. L.), Städte und Landorte zusammen, 1864 und 1867.",
                       "By district and for the principality (Reuß j. L.), towns and rural places combined, 1864 and 1867."),
         "vegalite": {"height": 280, "transform": [{"filter": "datum.condition == 'Blinde' && datum.area == 'Überhaupt'"}], "mark": "bar",
                      "encoding": {
                          "x": {"field": "district", "type": "nominal", "sort": DISTRICTS, "title": DIST_TITLE, "axis": {"labelAngle": 0}},
                          "xOffset": {"field": "year", "type": "nominal"},
                          "y": {"field": "per10k_total", "type": "quantitative", "title": bi("auf 10 000 Einwohner", "per 10,000 inhabitants")},
                          "color": {"field": "year", "type": "nominal", "title": None, "scale": {"domain": [1864, 1867]}},
                          "tooltip": [tip("district", "Landrathsbezirk", "District"), tip("year", "Jahr", "Year"), tip("count_total", "Zahl der Blinden", "Number of blind people"),
                                      tip("per10k_total", "auf 10 000 Einwohner", "per 10,000 inhabitants", ".2f")]}}},
        {"id": "c3", "dataset": "disability",
         "title": bi("Männer und Frauen im Fürstenthum", "Men and women in the principality"),
         "caption": bi("Taubstumme und Blinde auf 10 000 männliche bzw. weibliche Einwohner, Fürstenthum insgesamt. Unter den Blinden überwiegen die Frauen, unter den Taubstummen die Männer.",
                       "Deaf-mute and blind people per 10,000 male or female inhabitants, principality as a whole. Women predominate among the blind, men among the deaf-mute."),
         "vegalite": {"height": 280,
                      "transform": [{"filter": "datum.district == 'Reuß j. L.' && datum.area == 'Überhaupt'"},
                                    {"calculate": {"de": "datum.condition + ' ' + datum.year",
                                                   "en": "(datum.condition == 'Taubstumme' ? 'Deaf-mute' : 'Blind') + ' ' + datum.year"}, "as": "group"},
                                    {"calculate": "(datum.condition == 'Taubstumme' ? 0 : 1) * 10000 + datum.year", "as": "ord"},
                                    {"fold": ["per10k_m", "per10k_w"], "as": ["sex", "per10k"]}],
                      "mark": "bar",
                      "encoding": {
                          "x": {"field": "group", "type": "nominal", "sort": {"field": "ord", "op": "min"}, "title": None, "axis": {"labelAngle": 0}},
                          "xOffset": {"field": "sex", "type": "nominal", "sort": ["per10k_m", "per10k_w"]},
                          "y": {"field": "per10k", "type": "quantitative", "title": bi("auf 10 000 Einwohner des Geschlechts", "per 10,000 inhabitants of that sex")},
                          "color": {"field": "sex", "type": "nominal", "title": None, "scale": {"domain": ["per10k_m", "per10k_w"]},
                                    "legend": {"labelExpr": lab_expr2({"per10k_m": "Männer", "per10k_w": "Frauen"}, {"per10k_m": "Men", "per10k_w": "Women"})}},
                          "tooltip": [tip("group", "Gebrechen und Jahr", "Condition and year"), tip("per10k", "auf 10 000", "per 10,000", ".2f")]}}},
        {"id": "c4", "dataset": "disability",
         "title": bi("Städte und Landorte im Fürstenthum", "Towns and rural places in the principality"),
         "caption": bi("Taubstumme und Blinde auf 10 000 Einwohner in den Städten und auf dem Land des Fürstenthums. Bei den Blinden liegt das Land in beiden Jahren über den Städten; Werte je Landrathsbezirk stehen im Datensatz.",
                       "Deaf-mute and blind people per 10,000 inhabitants in the towns and in the countryside of the principality. For the blind the countryside is above the towns in both years; values per district are in the dataset."),
         "vegalite": {"height": 280,
                      "transform": [{"filter": "datum.district == 'Reuß j. L.' && datum.area != 'Überhaupt'"},
                                    {"calculate": {"de": "datum.condition + ' ' + datum.year",
                                                   "en": "(datum.condition == 'Taubstumme' ? 'Deaf-mute' : 'Blind') + ' ' + datum.year"}, "as": "group"},
                                    {"calculate": "(datum.condition == 'Taubstumme' ? 0 : 1) * 10000 + datum.year", "as": "ord"}],
                      "mark": "bar",
                      "encoding": {
                          "x": {"field": "group", "type": "nominal", "sort": {"field": "ord", "op": "min"}, "title": None, "axis": {"labelAngle": 0}},
                          "xOffset": {"field": "area", "type": "nominal", "sort": ["Städte", "Landorte"]},
                          "y": {"field": "per10k_total", "type": "quantitative", "title": bi("auf 10 000 Einwohner", "per 10,000 inhabitants")},
                          "color": {"field": "area", "type": "nominal", "title": None, "scale": {"domain": AREAS}, "legend": {"labelExpr": lab_expr(AREA_EN)}},
                          "tooltip": [tip("group", "Gebrechen und Jahr", "Condition and year"), tip("area", "Gebiet", "Area"), tip("count_total", "Zahl", "Number"),
                                      tip("per10k_total", "auf 10 000 Einwohner", "per 10,000 inhabitants", ".2f")]}}},
    ],
    "transcription_issues": [
        {"page": "118", "block": "b2", "cell": "r5c18", "transcribed": "12,48", "facsimile": "12,48", "checked_facsimile": True,
         "note": "Gera 1867, blind women overall: 23 women among about 19,230 gives 11,96 per 10,000 (urban 11 / 13,72 and rural 12 / 10,70 imply that population); printed so."},
        {"page": "118", "block": "b2", "cell": "r11c7", "transcribed": "10,06", "facsimile": "10,06", "checked_facsimile": True,
         "note": "Fürstenthum 1867, blind in towns, total: 32 persons among about 28,930 inhabitants gives 11,06; printed 10,06."},
    ],
    "keywords": {"de": ["Taubstumme", "Blinde", "Behinderung", "Gebrechen", "Blindheit", "Taubheit", "Stadt und Land", "Geschlecht"],
                 "en": ["deaf-mute", "blind", "disability", "blindness", "deafness", "town and country", "sex"]},
    "related": ["bevoelkerung-sterblichkeit-1858-1867", "gesundheit-selbstmord-unglueck-1858-1867"],
    "generated_by": GEN,
    "date": DATE,
}
write(ana)
