"""Build analysis gewaesser-quellen-muendungen-hoehen (data from a1_heights.py)."""
import io
import contextlib
from common import *

with contextlib.redirect_stdout(io.StringIO()):
    from a1_heights import rows_pts, reach_rows, by, src, rng, REGION

M = lambda de_, en_: {"de": de_, "en": en_}
mm = lambda ft: ft * FT_M
byname = {r[0]: r for r in reach_rows}
fall = lambda name: byname[name][8]
oth_max = max((r for r in src if r[2] != 1), key=lambda r: r[4])
o_min, o_max, o_n = rng(2)
u_min, u_max, u_n = rng(3)

findings = [
    M(f"Die drei höchsten der {len(src)} genannten Quellhöhen liegen im Maingebiet: Grumbach (1850'), Großer Rosenbaumbach (1825') und Rodach (1772', {de(mm(1772),0)} m). Die höchste Quelle des Elbgebiets ist das Langwasser der Sormitz mit {de(oth_max[4])}' ({de(oth_max[5],0)} m) – das passt zu Brückners Satz, im Main- oder Rheingebiet lägen »die höchsten Quellen des Landes«.",
      f"The three highest of the {len(src)} stated spring heights lie in the Main basin: Grumbach (1850'), Großer Rosenbaumbach (1825') and Rodach (1772', {en(mm(1772),0)} m). The highest spring in the Elbe system is the Langwasser, a headstream of the Sormitz, at {en(oth_max[4])}' ({en(oth_max[5],0)} m) – in line with Brückner's remark that the Main (Rhine) basin holds “the highest springs of the country”."),
    M(f"Die Quellen des Oberlandes liegen zwischen {de(o_min,0)}' und {de(o_max)}' ({de(mm(o_min),0)}–{de(mm(o_max),0)} m, {o_n} Angaben), die des Unterlandes nur zwischen {de(u_min,0)}' und {de(u_max,0)}' ({de(mm(u_min),0)}–{de(mm(u_max),0)} m, {u_n} Angaben): Die Elster-Zuflüsse entspringen mindestens {de(o_min-u_max,0)}' (rund {de(mm(o_min-u_max),0)} m) tiefer als die Oberländer Quellen.",
      f"Springs in the Oberland lie between {en(o_min,0)}' and {en(o_max)}' ({en(mm(o_min),0)}–{en(mm(o_max),0)} m, {o_n} values), those in the Unterland only between {en(u_min,0)}' and {en(u_max,0)}' ({en(mm(u_min),0)}–{en(mm(u_max),0)} m, {u_n} values): the Elster tributaries rise at least {en(o_min-u_max,0)}' (about {en(mm(o_min-u_max),0)} m) lower than the Oberland springs."),
    M(f"Am stärksten fallen die kurzen Oberländer Nebenbäche der Saale: Die Wettera stürzt von 1646' auf 945' ({de(fall('Wettera'),0)}' = {de(fall('Wettera')*FT_M,0)} m), der Sieglitzbach von 1650' auf 1098' ({de(fall('Sieglitzbach'),0)}' = {de(fall('Sieglitzbach')*FT_M,0)} m). Die Saale selbst fällt im ganzen Land nur um {de(fall('Saale'),0)}' ({de(fall('Saale')*FT_M,0)} m).",
      f"The short Oberland tributaries of the Saale fall most steeply: the Wettera drops from 1646' to 945' ({en(fall('Wettera'),0)}' = {en(fall('Wettera')*FT_M,0)} m), the Sieglitzbach from 1650' to 1098' ({en(fall('Sieglitzbach'),0)}' = {en(fall('Sieglitzbach')*FT_M,0)} m). The Saale itself falls only {en(fall('Saale'),0)}' ({en(fall('Saale')*FT_M,0)} m) across the whole country."),
    M(f"Die Weiße Elster verliert zwischen Ein- und Austritt nur {de(fall('Elster'),0)}' ({de(fall('Elster')*FT_M,0)} m) – deutlich weniger als Weida ({de(fall('Weida'),0)}'), Triebes ({de(fall('Triebes (zur Weida)'),0)}') oder Leuba ({de(fall('Leuba'),0)}'). Das flache Gefälle passt zu Brückners Lob des Elstertals als »anmuthig«.",
      f"Between entry and exit the White Elster loses only {en(fall('Elster'),0)}' ({en(fall('Elster')*FT_M,0)} m) – far less than the Weida ({en(fall('Weida'),0)}'), Triebes ({en(fall('Triebes (zur Weida)'),0)}') or Leuba ({en(fall('Leuba'),0)}'). The gentle gradient fits Brückner's praise of the Elster valley as “graceful” (anmuthig)."),
]
for f in findings:
    print(f["de"])

PT_COLS = [
    {"name": "stream", "label": M("Gewässer", "Watercourse"), "type": "string", "unit": None},
    {"name": "region", "label": M("Gebiet", "Region"), "type": "string", "unit": None, "note": "Gliederung nach Brückners Überschriften (S. 45): I. Main-/Rheingebiet, II.A Oberland, II.B Unterland; Saale und Weida stehen bei ihm im Oberland."},
    {"name": "region_order", "label": M("Gebiet (Ordnung)", "Region (order)"), "type": "integer", "unit": None, "derived": True, "note": "Sortierschlüssel 1–3, editorisch"},
    {"name": "point_type", "label": M("Messpunkt", "Point"), "type": "string", "unit": None, "note": "source = Quelle, mouth = Mündung, entry = Eintritt ins Land, exit = Austritt aus dem Land, inflow = Einfluss eines Nebenbachs (Codes editorisch)"},
    {"name": "height_ft", "label": M("Höhe", "Height"), "type": "number", "unit": "preuß. Dezimalfuß"},
    {"name": "height_m", "label": M("Höhe", "Height"), "type": "number", "unit": "m", "derived": True},
    {"name": "page", "label": M("Seite", "Page"), "type": "string", "unit": None},
    {"name": "block", "label": M("Block", "Block"), "type": "string", "unit": None},
    {"name": "note", "label": M("Ort/Bemerkung", "Place/remark"), "type": "string", "unit": None},
]
RC_COLS = [
    {"name": "stream", "label": M("Gewässer", "Watercourse"), "type": "string", "unit": None},
    {"name": "region", "label": M("Gebiet", "Region"), "type": "string", "unit": None},
    {"name": "region_order", "label": M("Gebiet (Ordnung)", "Region (order)"), "type": "integer", "unit": None, "derived": True},
    {"name": "reach", "label": M("Strecke", "Reach"), "type": "string", "unit": None, "note": "A = Quelle bis Mündung, B = Landeseintritt bis Landesaustritt, C = Teilstrecke (z. B. Landeseintritt bis Mündung, Quelle bis Eintritt in Gera); Codes editorisch"},
    {"name": "upper_ft", "label": M("Obere Höhe", "Upper height"), "type": "number", "unit": "preuß. Dezimalfuß"},
    {"name": "lower_ft", "label": M("Untere Höhe", "Lower height"), "type": "number", "unit": "preuß. Dezimalfuß"},
    {"name": "upper_m", "label": M("Obere Höhe", "Upper height"), "type": "number", "unit": "m", "derived": True},
    {"name": "lower_m", "label": M("Untere Höhe", "Lower height"), "type": "number", "unit": "m", "derived": True},
    {"name": "fall_ft", "label": M("Gefälle", "Fall"), "type": "number", "unit": "preuß. Dezimalfuß", "derived": True, "note": "Differenz; für die Saale druckt Brückner 267' (S. 46), das stimmt mit 1190' − 923' überein."},
    {"name": "fall_m", "label": M("Gefälle", "Fall"), "type": "number", "unit": "m", "derived": True},
]
refs = sorted({(r[6], r[7]) for r in rows_pts}, key=lambda t: (int(t[0]), int(t[1][1:])))
SRC = [{"page": p, "block": b} for p, b in refs]


def TT(f, de_, en_):
    return {"field": f, "title": M(de_, en_)}


YAX = {"field": "stream", "type": "nominal", "title": None, "axis": {"labelLimit": 230},
       "sort": {"field": "upper_m", "op": "max", "order": "descending"}}
REACH_L = {"calculate": {"de": "datum.reach == 'A' ? 'Quelle–Mündung' : datum.reach == 'B' ? 'Eintritt–Austritt' : 'Teilstrecke'",
                         "en": "datum.reach == 'A' ? 'Spring–mouth' : datum.reach == 'B' ? 'Entry–exit' : 'Partial reach'"}, "as": "reach_l"}
c1 = {
    "height": 400,
    "transform": [REACH_L],
    "encoding": {
        "y": YAX,
        "color": {"field": "reach_l", "type": "nominal", "title": None, "sort": {"field": "reach", "op": "min"}, "legend": {"columnPadding": 4}},
    },
    "layer": [
        {"mark": {"type": "rule", "strokeWidth": 3},
         "encoding": {"x": {"field": "lower_m", "type": "quantitative", "title": M("Höhe in m (aus Dezimalfuß umgerechnet)", "Height in m (converted from decimal feet)"), "scale": {"zero": False}},
                      "x2": {"field": "upper_m"},
                      "tooltip": [TT("stream", "Gewässer", "Watercourse"), TT("reach_l", "Strecke", "Reach"),
                                  TT("upper_ft", "Obere Höhe (Fuß)", "Upper height (ft)"), TT("lower_ft", "Untere Höhe (Fuß)", "Lower height (ft)"),
                                  TT("upper_m", "Obere Höhe (m)", "Upper height (m)"), TT("lower_m", "Untere Höhe (m)", "Lower height (m)"),
                                  TT("fall_ft", "Gefälle (Fuß)", "Fall (ft)"), TT("fall_m", "Gefälle (m)", "Fall (m)")]}},
        {"mark": {"type": "circle", "size": 70},
         "encoding": {"x": {"field": "upper_m", "type": "quantitative"}}},
        {"mark": {"type": "circle", "size": 70},
         "encoding": {"x": {"field": "lower_m", "type": "quantitative"}}},
    ],
}
c2 = {
    "height": 400,
    "transform": [{"filter": "datum.point_type == 'source'"}],
    "mark": "bar",
    "encoding": {
        "y": {"field": "stream", "type": "nominal", "title": None, "axis": {"labelLimit": 230},
              "sort": {"field": "height_m", "op": "max", "order": "descending"}},
        "x": {"field": "height_m", "type": "quantitative", "title": M("Quellhöhe in m (aus Dezimalfuß umgerechnet)", "Spring height in m (converted from decimal feet)")},
        "color": {"field": "region", "type": "nominal", "title": None, "sort": {"field": "region_order", "op": "min"}},
        "tooltip": [TT("stream", "Gewässer", "Watercourse"), TT("region", "Gebiet", "Region"),
                    TT("height_ft", "Höhe (Dezimalfuß)", "Height (decimal feet)"), TT("height_m", "Höhe (m)", "Height (m)"),
                    TT("note", "Bemerkung", "Remark")],
    },
}

ana = {
    "id": "gewaesser-quellen-muendungen-hoehen",
    "title": M("Höhenlage von Quellen, Mündungen und Landesgrenzen der Gewässer", "Heights of springs, mouths and border crossings of the watercourses"),
    "category": "hydrology",
    "section": "t1-1-6",
    "sources": SRC,
    "summary": M(
        f"In seinem Verzeichnis des Gewässernetzes nennt Brückner für {len(by)} Bäche und Flüsse Höhenangaben in preußischen Dezimalfuß: Quellen, Mündungen sowie die Höhe beim Eintritt in und Austritt aus dem Land. Die Auswertung stellt sie nach Gebiet (Main, Oberland, Unterland) zusammen und rechnet in Meter um. Sie zeigt, wie viel höher das Oberland als das Unterland liegt und wo die Gewässer am stärksten fallen.",
        f"In his survey of the drainage network Brückner gives heights in Prussian decimal feet for {len(by)} streams and rivers: springs, mouths and the elevation where a river enters or leaves the country. The analysis groups them by region (Main, Oberland, Unterland) and converts them to meters. It shows how much higher the Oberland lies than the Unterland and where the watercourses fall most steeply."),
    "method": M(
        "Alle Höhenangaben (Zahl mit Apostroph, z. B. 1772') stammen aus dem Gewässerverzeichnis S. 45–53; jede Zahl wurde im Quellblock geprüft. Aufgenommen sind nur Angaben, die sich eindeutig einem Punkt eines Gewässers zuordnen lassen; Spannenangaben (Sieglitzbach und Hackenbach »1650 bis 1660'«, S. 45–46) und Höhen nicht benannter Zuflüsse wurden weggelassen. Einheit: Nach Brückners Fußnote S. 11 sind sämtliche Höhenangaben des Buchs »preuß. Decimalfuß, auf den Pegel bei Swinemünde bezogen«; das gilt auch für die Gewässerhöhen. Umrechnung: 1 Dezimalfuß = 1/10 preuß. Ruthe = 0,3766242 m (1 Ruthe = 3,766242 m, S. 831). Das Gefälle ist die Differenz zwischen oberer und unterer Höhe einer Strecke; für Flüsse, die das Land durchqueren, ist es das Gefälle zwischen Eintritt und Austritt, nicht zwischen Quelle und Mündung. Das Gebiet folgt Brückners Gliederung (I. Main, II.A Oberland, II.B Unterland).",
        "All heights (a number with an apostrophe, e.g. 1772') come from the drainage survey on pp. 45–53; every number was checked in its source block. Only values that can be assigned unambiguously to one point of a watercourse are included; range statements (Sieglitzbach and Hackenbach, “1650 to 1660'”, pp. 45–46) and heights of unnamed tributaries were left out. Unit: according to Brückner's footnote on p. 11 all height figures in the book are “Prussian decimal feet, referred to the Swinemünde tide gauge”; this includes the watercourse heights. Conversion: 1 decimal foot = 1/10 Prussian Ruthe = 0.3766242 m (1 Ruthe = 3.766242 m, p. 831). Fall is the difference between the upper and lower height of a reach; for rivers crossing the country it is the fall between entry and exit, not between spring and mouth. The region follows Brückner's divisions (I. Main, II.A Oberland, II.B Unterland)."),
    "findings": findings,
    "caveats": [
        M("Bezugsfläche der Höhen ist nach Brückners Fußnote (S. 11) der Pegel bei Swinemünde; die Fußangaben sind großenteils auf ganze Fuß gerundet. Die Höhen der Elster bei Gera (503') und Köstritz (468') liegen nahe bei den Bahnhofshöhen von S. 11 (Gera 502', Köstritz 474'), was für dieselbe Höhenvermessung spricht.",
          "According to Brückner's footnote (p. 11) the reference level is the Swinemünde tide gauge; most foot values are rounded to whole feet. The Elster heights at Gera (503') and Köstritz (468') lie close to the station heights on p. 11 (Gera 502', Köstritz 474'), which indicates the same height survey."),
        M(f"Höhen sind nur für {len(by)} von rund 300 Gewässern des Landes angegeben und ungleich verteilt (viele Oberländer Bäche, wenige Unterländer); »Teilstrecken« beginnen und enden nicht an Quelle und Mündung.",
          f"Heights are given for only {len(by)} of the roughly 300 watercourses of the country and are unevenly distributed (many Oberland streams, few in the Unterland); “partial reaches” do not start and end at spring and mouth."),
        M("Die Weida führt Brückner unter dem Oberland, obwohl sie bei Voigtsberg in die Elster mündet (S. 50); die Auswertung folgt seiner Gliederung.",
          "Brückner lists the Weida under the Oberland, although it joins the Elster at Voigtsberg (p. 50); the analysis follows his grouping."),
    ],
    "conversions": [
        {"from": "preuß. Dezimalfuß (Höhen)", "to": "m", "factor_or_formula": "m = Dezimalfuß × 0.3766242 (1 Dezimalfuß = 1/10 preuß. Ruthe)", "reference": "Brückner S. 11 Fußnote (Dezimalfuß, Pegel Swinemünde); S. 831: 1 preuß. Ruthe = 3,766242 m"},
    ],
    "datasets": [
        {"name": "points", "title": M("Höhenpunkte der Gewässer", "Height points of the watercourses"), "columns": PT_COLS,
         "rows": rows_pts, "source_refs": SRC},
        {"name": "reaches", "title": M("Strecken mit oberer und unterer Höhe", "Reaches with upper and lower height"), "columns": RC_COLS,
         "rows": reach_rows, "source_refs": SRC},
    ],
    "charts": [
        {"id": "c1", "dataset": "reaches",
         "title": M("Obere und untere Höhe der Gewässerstrecken", "Upper and lower height of watercourse reaches"),
         "caption": M("Jede Linie verbindet die obere und die untere Höhe einer Strecke (Meter, aus Dezimalfuß umgerechnet); Farbe = Art der Strecke. Sortiert nach der oberen Höhe.",
                      "Each line joins the upper and lower height of a reach (meters, converted from decimal feet); colour = type of reach. Sorted by upper height."),
         "vegalite": c1},
        {"id": "c2", "dataset": "points",
         "title": M("Quellhöhen nach Gebiet", "Spring heights by region"),
         "caption": M(f"Die {len(src)} von Brückner genannten Quellhöhen (Meter, aus Dezimalfuß). Die Weida entspringt auf Hochflächen außerhalb des Landes; Langwasser und Rodach entspringen am Frankenwald.",
                      f"The {len(src)} spring heights Brückner gives (meters, converted from decimal feet). The Weida rises on uplands outside the country; Langwasser and Rodach rise on the Frankenwald."),
         "vegalite": c2},
    ],
    "keywords": {"de": ["Quellen", "Flüsse", "Gewässer", "Höhen", "Saale", "Weiße Elster", "Weida", "Rodach", "Gefälle", "Dezimalfuß"],
                 "en": ["springs", "rivers", "watercourses", "heights", "Saale", "White Elster", "Weida", "Rodach", "gradient", "decimal foot"]},
    "generated_by": "Claude Sonnet 5.5 (subagent A02)",
    "date": "2026-10-01",
}
write_analysis(ana)
