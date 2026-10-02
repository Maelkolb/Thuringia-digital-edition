"""A11-14: Höhere und besondere Schulen 1868/69: Schüler, Lehrer, Klassen (pp. 299-300)."""
from common import *

# values printed in the running text of pp. 299-300 and in the table p. 300 b6
INST = [
    # key, name_de, name_en, place, type_key, type_de, type_en, pupils, teachers, classes, approx_de, approx_en
    ("a", "Realschule Gera", "Realschule, Gera", "Gera", "a", "Realschule", "Realschule", 432, 19, 10, "", ""),
    ("b", "Höhere Töchterschule Gera", "Higher girls' school, Gera", "Gera", "d", "Mädchenschule", "Girls' school", 240, None, 8, "ca.", "approx."),
    ("c", "Gymnasium Gera", "Gymnasium, Gera", "Gera", "b", "Gymnasium", "Gymnasium", 190, 15, 7, "", ""),
    ("d", "Gymnasium Schleiz", "Gymnasium, Schleiz", "Schleiz", "b", "Gymnasium", "Gymnasium", 114, 11, 6, "", ""),
    ("e", "Handelsschule Amthor, Gera", "Commercial school (Amthor), Gera", "Gera", "c", "Handelsschule", "Commercial school", 75, None, None, "ca.", "approx."),
    ("f", "Seminar Schleiz", "Teacher training college, Schleiz", "Schleiz", "e", "Lehrerbildung", "Teacher training", 49, None, 3, "", ""),
    ("g", "Taubstummenanstalt Schleiz", "School for the deaf-mute, Schleiz", "Schleiz", "f", "Sonderschule", "Special school", 8, None, None, "", ""),
]
rows = []
for k, nde, nen, place, tk, tde, ten, pup, teach, cls, ade, aen in INST:
    ppt = round(pup / teach, 1) if teach else None
    ppc = round(pup / cls, 1) if cls else None
    rows.append([k, nde, nen, place, tk, tde, ten, pup, ade, aen, teach, cls, ppt, ppc])
print(rows)

# comparison series for chart 2: three schools with teacher and class numbers
cmp_rows = []
for r in rows:
    if r[0] in ("a", "c", "d"):
        cmp_rows.append([r[0], r[1], r[2], "a", "Schüler je Lehrer", "Pupils per teacher", r[12]])
        cmp_rows.append([r[0], r[1], r[2], "b", "Schüler je Klasse", "Pupils per class", r[13]])

pupils = {r[0]: r[7] for r in rows}
gym = pupils["c"] + pupils["d"]
total_listed = sum(r[7] for r in rows)
vs = 14239
print(gym, total_listed, 100 * total_listed / vs)
R = {r[0]: r for r in rows}


def D(x, nd=0):
    return fmt_de(x, nd)


def E(x, nd=0):
    return fmt_en(x, nd)


ana = {
    "id": "schule-hoehere-anstalten-schueler-lehrer-1868",
    "title": bi("Höhere und besondere Schulen 1868/69: Schüler, Lehrer und Klassen", "Secondary and special schools in 1868/69: pupils, teachers and classes"),
    "category": "education",
    "section": "t1-4-6",
    "sources": [{"page": "299", "block": "b5"}, {"page": "300", "block": "b1"}, {"page": "300", "block": "b2"}, {"page": "300", "block": "b4"}, {"page": "300", "block": "b6"}, {"page": "300", "block": "b7"}],
    "summary": bi(
        f"Neben den Volksschulen nennt Brückner die höheren und besonderen Anstalten des Fürstentums mit Schülerzahlen: die Realschule in Gera ({D(pupils['a'])} Schüler), die höhere Töchterschule in Gera (ca. {D(pupils['b'])}), die Gymnasien in Gera ({D(pupils['c'])}) und Schleiz ({D(pupils['d'])}), eine Handelsschule, das Seminar in Schleiz und eine Taubstummenanstalt. Die Auswertung vergleicht die Größe der Anstalten und die Besetzung mit Lehrern.",
        f"Besides the elementary schools Brückner lists the secondary and special institutions of the principality with pupil numbers: the Realschule in Gera ({E(pupils['a'])} pupils), the higher girls' school in Gera (approx. {E(pupils['b'])}), the Gymnasien in Gera ({E(pupils['c'])}) and Schleiz ({E(pupils['d'])}), a commercial school, the teacher training college in Schleiz and a school for the deaf-mute. The analysis compares the size of the institutions and their staffing.",
    ),
    "method": bi(
        "Die Schülerzahlen stehen im Text S. 299–300 (Realschule: 320 in sieben Real-, 112 in drei Vorklassen; Töchterschule ca. 240; Handelsschule ca. 75; Seminar Schleiz drei Seminarklassen mit 49 Schülern; Taubstummenanstalt acht Zöglinge) und in der Tabelle der Gymnasien (S. 300, b6). Lehrer- und Klassenzahlen sind aus den gedruckten Teilzahlen addiert (Gymnasien: Haupt- + Hilfslehrer; Realschule: 17 + 2 = 19 eigene Lehrer, die vier hilfsweise herangezogenen Lehrer der Realschule sind nicht eingerechnet; Realschule 7 + 3 Klassen). Schüler je Lehrer und je Klasse sind abgeleitet. Die Anstalt von Dr. Mauke in Schleiz (30–40 Schülerinnen) ist wegen der Spannenangabe nicht aufgenommen.",
        "The pupil numbers are in the text of pp. 299–300 (Realschule: 320 in seven real classes, 112 in three preparatory classes; girls' school approx. 240; commercial school approx. 75; Schleiz college three seminar classes with 49 pupils; school for the deaf-mute eight inmates) and in the table of the Gymnasien (p. 300, b6). Teacher and class numbers are added from the printed partial figures (Gymnasien: main + assistant teachers; Realschule: 17 + 2 = 19 own teachers, the four additional teachers drawn from elsewhere are not counted; Realschule 7 + 3 classes). Pupils per teacher and per class are derived. Dr Mauke's institution in Schleiz (30–40 girls) is not included because only a range is given.",
    ),
    "findings": [
        bi(f"Die Realschule in Gera hat mit {D(pupils['a'])} Schülern (davon 112 in den Vorklassen) mehr Schüler als beide Gymnasien zusammen ({D(gym)}); allein ihre Realklassen (320) übertreffen die Gymnasien.",
           f"The Realschule in Gera, with {E(pupils['a'])} pupils (112 of them in the preparatory classes), has more pupils than both Gymnasien together ({E(gym)}); its real classes alone (320) exceed the Gymnasien."),
        bi(f"Die Realschule hat {D(R['a'][12],1)} Schüler je Lehrer, die Gymnasien nur {D(R['c'][12],1)} (Gera) und {D(R['d'][12],1)} (Schleiz); je Klasse sind es {D(R['a'][13],1)} gegenüber {D(R['c'][13],1)} und {D(R['d'][13],1)}.",
           f"The Realschule has {E(R['a'][12],1)} pupils per teacher, the Gymnasien only {E(R['c'][12],1)} (Gera) and {E(R['d'][12],1)} (Schleiz); per class the figures are {E(R['a'][13],1)} against {E(R['c'][13],1)} and {E(R['d'][13],1)}."),
        bi(f"Die aufgeführten höheren und besonderen Anstalten zählen zusammen rund {D(total_listed)} Schüler, das sind {D(100*total_listed/vs,1)} % der Zahl der Volksschüler (14.239, S. 299).",
           f"The institutions listed together count about {E(total_listed)} pupils, i.e. {E(100*total_listed/vs,1)} % of the number of elementary pupils (14,239, p. 299)."),
        bi("Von den beiden früheren Lehrerseminaren hatte Gera durchschnittlich 9, Schleiz 51 Schüler; 1869 wurde Gera aufgehoben und Schleiz zum Landesseminar gemacht (49 Seminaristen).",
           "Of the two former teacher training colleges Gera had on average 9 pupils and Schleiz 51; in 1869 Gera was closed and Schleiz became the college for the whole country (49 trainee teachers)."),
    ],
    "caveats": [
        bi("Mehrere Zahlen sind Näherungen (»ca. 240«, »ca. 75«). Die Zahlen gelten für 1868/69, ohne genaues Stichdatum. Lehrer und Klassen sind nur für die Realschule, die Gymnasien und das Seminar angegeben. Die Zahl der Hilfslehrer an den Gymnasien (7 und 5) ist in den Lehrern mitgerechnet; Hilfslehrer können Teilzeit-Kräfte sein.",
           "Several numbers are approximations (“approx. 240”, “approx. 75”). The figures apply to 1868/69 without an exact reference date. Teachers and classes are given only for the Realschule, the Gymnasien and the college. The number of assistant teachers at the Gymnasien (7 and 5) is included in the teachers; assistant teachers may be part-time staff."),
        bi("Brückner nennt für die Gymnasien »auf eine Klasse 23« Schüler (304 : 13 = 23,4) und »auf einen Hauptlehrer 21,7« (304 : 14). Die Klassenzahl von Schleiz (6) enthält die zusätzliche Real-Parallelklasse nicht (Fußnote).",
           "For the Gymnasien Brückner gives “23 per class” (304 : 13 = 23.4) and “21.7 per main teacher” (304 : 14). The class number of Schleiz (6) does not include the additional parallel real class (footnote)."),
    ],
    "datasets": [
        {"name": "institutions", "title": bi("Höhere und besondere Anstalten", "Secondary and special institutions"),
         "columns": [
             col("inst_key", "Kürzel", "Key", "string"),
             col("inst_de", "Anstalt", "Institution", "string"), col("inst_en", "Anstalt (englisch)", "Institution (English)", "string"),
             col("place", "Ort", "Place", "string"),
             col("type_key", "Kürzel Art", "Type key", "string"),
             col("type_de", "Art", "Type", "string"), col("type_en", "Art (englisch)", "Type (English)", "string"),
             col("pupils", "Schüler", "Pupils", "integer", "Schüler"),
             col("approx_de", "Angabe", "Remark", "string"), col("approx_en", "Angabe (englisch)", "Remark (English)", "string"),
             col("teachers", "Lehrer", "Teachers", "integer", "Lehrer", derived=True, note="Summe der gedruckten Teilzahlen"),
             col("classes", "Klassen", "Classes", "integer", "Klassen", derived=True, note="Summe der gedruckten Teilzahlen; Töchterschule 5 + 3"),
             col("ppt", "Schüler je Lehrer", "Pupils per teacher", "number", "Schüler", derived=True),
             col("ppc", "Schüler je Klasse", "Pupils per class", "number", "Schüler", derived=True),
         ],
         "rows": rows, "source_refs": [{"page": "299", "block": "b5"}, {"page": "300", "block": "b1"}, {"page": "300", "block": "b2"}, {"page": "300", "block": "b4"}, {"page": "300", "block": "b6"}]},
        {"name": "staffing", "title": bi("Besetzung der Realschule und der Gymnasien", "Staffing of the Realschule and the Gymnasien"),
         "columns": [
             col("inst_key", "Kürzel", "Key", "string"),
             col("inst_de", "Anstalt", "Institution", "string"), col("inst_en", "Anstalt (englisch)", "Institution (English)", "string"),
             col("measure_key", "Kürzel Messgröße", "Measure key", "string"),
             col("measure_de", "Messgröße", "Measure", "string"), col("measure_en", "Messgröße (englisch)", "Measure (English)", "string"),
             col("value", "Wert", "Value", "number", "Schüler", derived=True),
         ],
         "rows": cmp_rows, "source_refs": [{"page": "300", "block": "b4"}, {"page": "300", "block": "b6"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "institutions",
         "title": bi("Schüler der höheren und besonderen Anstalten", "Pupils of the secondary and special institutions"),
         "caption": bi("Schülerzahlen 1868/69; bei Töchterschule und Handelsschule »ca.«. Die Farbe zeigt die Schulart.", "Pupil numbers 1868/69; approximate for the girls' school and the commercial school. Colour shows the type of school."),
         "vegalite": {
             "height": 300,
             "mark": "bar",
             "encoding": {
                 "y": {"field": F("inst"), "type": "nominal", "sort": "-x", "title": None, "axis": {"labelLimit": 320}},
                 "x": {"field": "pupils", "type": "quantitative", "title": bi("Schüler", "Pupils")},
                 "color": {"field": F("type"), "type": "nominal", "title": None, "sort": {"field": "type_key", "op": "min"}, "legend": {"labelLimit": 300, "columns": 3}},
                 "tooltip": [ttf("inst", "Anstalt", "Institution"), tt("pupils", "Schüler", "Pupils"), ttf("approx", "Angabe", "Remark")]}}},
        {"id": "c2", "dataset": "staffing",
         "title": bi("Schüler je Lehrer und je Klasse", "Pupils per teacher and per class"),
         "caption": bi("Realschule Gera und die beiden Gymnasien; Lehrer einschließlich Hilfslehrer, Klassen einschließlich Vorklassen der Realschule.", "Realschule Gera and the two Gymnasien; teachers including assistant teachers, classes including the preparatory classes of the Realschule."),
         "vegalite": {
             "height": 280,
             "mark": "bar",
             "encoding": {
                 "x": {"field": F("inst"), "type": "nominal", "sort": {"field": "inst_key", "op": "min"}, "title": None, "axis": {"labelAngle": 0, "labelLimit": 220}},
                 "xOffset": {"field": F("measure"), "sort": {"field": "measure_key", "op": "min"}},
                 "y": {"field": "value", "type": "quantitative", "title": bi("Schüler je Lehrer bzw. Klasse", "Pupils per teacher or class")},
                 "color": {"field": F("measure"), "type": "nominal", "title": None, "sort": {"field": "measure_key", "op": "min"}},
                 "tooltip": [ttf("inst", "Anstalt", "Institution"), ttf("measure", "Messgröße", "Measure"), {"field": "value", "title": bi("Wert", "Value"), "format": ".1f"}]}}},
    ],
    "keywords": {"de": ["Gymnasium", "Realschule", "Seminar", "Töchterschule", "Handelsschule", "Taubstummenanstalt", "Schulwesen", "Gera", "Schleiz"],
                 "en": ["Gymnasium", "Realschule", "teacher training", "girls' school", "commercial school", "school for the deaf-mute", "schools", "Gera", "Schleiz"]},
}
write(ana)
