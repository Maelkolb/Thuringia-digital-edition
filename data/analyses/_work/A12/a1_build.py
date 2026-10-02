import re
from common import *
import a1_voigte as m
from a1_voigte import E, rows, LINES, ROLES, presence, rcount, ccount, ocount, nE, top3, med_span, peak_bin, peak_n, peak_split, LCOL, YEAR, gantt

nr = sum(rcount.values())
nc = sum(ccount.values())
no = sum(ocount.values())
spans_n = len(m.spans)
epi = sum(1 for e in E if re.search(r"\bd\. (ä|m|j)\.", e["name"]))
rom = [e for e in E if re.fullmatch(r"Heinrich [IVX]+\.", e["name"])]
assert len(rom) == 7 and nE == 98 and nr == 70

REFS = refs_from([(e["src"][0], e["src"][1]) for e in E])
SRC = REFS + refs_from([("346", "b1"), ("331", "b3"), ("342", "b1"), ("353", "b1")])

a = {
 "id": "genealogie-voigte-heinriche-1143-1572",
 "title": bi("Die Heinriche der Voigte von Weida, Gera und Plauen 1143–1572", "The Heinrichs of the Voigts of Weida, Gera and Plauen, 1143–1572"),
 "category": "genealogy",
 "section": "t1-5-2",
 "sources": SRC,
 "summary": bi(
  f"Brückners Stammtafeln I–V (S. 331–372) führen die Männer des Hauses Weida mit Jahreszahlen auf; mit einer Ausnahme (dem nach den Chronisten jung gestorbenen Bernhard) heißen sie alle Heinrich und werden durch »d. ä., d. m., d. j.« und Beinamen unterschieden. Der Datensatz erfasst {nE} Heinriche der Linien Weida, Gera, Plauen und der jüngeren Linie Reuß-Plauen, davon {nr} als Landesherren. Die Diagramme ordnen sie nach den gedruckten Jahren zeitlich und zeigen, wie viele Herren gleichzeitig bezeugt sind.",
  f"Brückner's genealogical tables I–V (pp. 331–372) list the men of the house of Weida with years; with one exception (Bernhard, who died young according to the chroniclers) they are all called Heinrich and are told apart by “d. ä., d. m., d. j.” (elder, middle, younger) and by epithets. The dataset records {nE} Heinrichs of the lines of Weida, Gera, Plauen and the younger line Reuss-Plauen, {nr} of them as lords. The charts arrange them in time by the printed years and show how many lords are attested at the same time."),
 "method": bi(
  "Aus Tab. I–V wurden alle männlichen Personen mit gedruckten Jahreszahlen übernommen (Namen und Datumsangaben wie gedruckt, auch die Heinrich-Zählung). Bis ins 15. Jahrhundert geben die Tafeln die Jahre der urkundlichen Bezeugung bzw. der Regierung (»1307 — c. 1345«), später Geburts- und Todesjahr (»geb. 1508, † 1554«; Spalte »kind«). Die Balken laufen vom ersten zum letzten gedruckten Jahr; Zusätze wie »c.«, »nach«, »vor« stehen in der Spalte »end_qual« (c = circa, n = nach, v = vor, x = genau); Personen mit nur einer Jahreszahl erscheinen als Punkt. Als »Landesherr« zählt, wer als Voigt, Herr oder Burggraf auftritt; Mönche, Domherren und Ordensritter sind als Geistliche, Kinder und Erben ohne Herrschaft getrennt aufgeführt. Die Tafeln III und V sind auf dem Seitenspiegel quergedruckt; wo die Transkription Zellen verwechselte oder ausließ, wurden die Angaben am Faksimile geprüft (siehe transcription_issues). Gleichzeitigkeit (Diagramm 4) ist abgeleitet: Ein Landesherr zählt für jedes Halbjahrhundert, das sein Zeitraum berührt.",
  "All men with printed years were taken from Tab. I–V (names and dates as printed, including the Heinrich numbering). Up to the 15th century the tables give the years of documentary attestation or of rule (“1307 — c. 1345”), later birth and death years (“geb. 1508, † 1554”; column “kind”). The bars run from the first to the last printed year; qualifiers such as “c.”, “nach” (after), “vor” (before) are in column “end_qual” (c = circa, n = after, v = before, x = exact); persons with only one year appear as a dot. A “lord” is anyone who acts as Voigt, Herr or burgrave; monks, canons and knights of the Order are listed separately as clerics, children and heirs without a lordship as a third group. Tables III and V are printed sideways on the page; where the transcription confused or omitted cells, the entries were checked against the facsimile (see transcription_issues). Simultaneity (chart 4) is derived: a lord counts in every half-century that his period touches."),
 "findings": [
  bi(f"Die Tafeln I–V nennen {nE} Heinriche mit Jahreszahlen, {nr} davon als Landesherren (Weida {rcount['weida']}, Gera {rcount['gera']}, Plauen ältere Linie {rcount['plauen']}, Reuß-Plauen {rcount['reuss']}), dazu {nc} Geistliche und Ordensritter und {no} Erben ohne Herrschaft. Der Name unterscheidet die Personen nicht; in {epi} Einträgen helfen »d. ä., d. m., d. j.«, römische Ziffern gibt es nur bei den Burggrafen Heinrich I.–VII. von Plauen (1389–1572).",
     f"Tables I–V name {nE} Heinrichs with years, {nr} of them as lords (Weida {rcount['weida']}, Gera {rcount['gera']}, Plauen older line {rcount['plauen']}, Reuss-Plauen {rcount['reuss']}), plus {nc} clerics and knights of the Order and {no} heirs without a lordship. The name does not tell the persons apart; in {epi} entries “d. ä., d. m., d. j.” (elder, middle, younger) help, Roman numerals occur only for the burgraves Heinrich I–VII of Plauen (1389–1572)."),
  bi(f"Am dichtesten ist die Überlieferung im Halbjahrhundert {peak_bin}–{peak_bin+49}: {peak_n} Landesherren namens Heinrich sind gleichzeitig bezeugt ({peak_split['weida']} Weida, {peak_split['gera']} Gera, {peak_split['plauen']} Plauen, {peak_split['reuss']} Reuß-Plauen).",
     f"The record is densest in the half-century {peak_bin}–{peak_bin+49}: {peak_n} lords named Heinrich are attested at the same time ({peak_split['weida']} Weida, {peak_split['gera']} Gera, {peak_split['plauen']} Plauen, {peak_split['reuss']} Reuss-Plauen)."),
  bi(f"Bei den {spans_n} Landesherren mit gedrucktem Zeitraum beträgt die Spanne vom ersten bis zum letzten Jahr im Median {int(med_span)} Jahre; am längsten bezeugt sind Heinrich d. ä. von Weida (1295–c. 1364, {top3[0][0]} Jahre), Heinrich der Dispensirte von Gera (1351–1419, {top3[1][0]}) und Heinrich d. ä., der Lange, von Plauen (1306–1373, {top3[2][0]}).",
     f"For the {spans_n} lords with a printed period, the span from first to last year has a median of {int(med_span)} years; the longest attested are Heinrich the elder of Weida (1295–c. 1364, {top3[0][0]} years), Heinrich the Dispensed of Gera (1351–1419, {top3[1][0]}) and Heinrich the elder, the Long, of Plauen (1306–1373, {top3[2][0]})."),
  bi("Die drei älteren Linien enden nacheinander: Weida mit einem Heinrich »† c. 1535«, Gera mit Heinrich d. j., dem Beharrlichen († 1550), der ältere Zweig von Plauen mit Burggraf Heinrich VII. († 1572). Fortgeführt wird nur Reuß-Plauen.",
     "The three older lines end one after the other: Weida with a Heinrich “† c. 1535”, Gera with Heinrich the younger, the Persistent († 1550), the older branch of Plauen with Burgrave Heinrich VII († 1572). Only Reuss-Plauen continues."),
 ],
 "caveats": [
  bi("Die gedruckten Zeiträume sind nicht einheitlich: Bis ins 15. Jahrhundert sind es Jahre der Bezeugung oder Regierung, später Lebensdaten; »nach«/»vor« bezeichnen nur Untergrenzen bzw. Obergrenzen. Balken sind daher keine genauen Regierungszeiten.",
     "The printed periods are not uniform: up to the 15th century they are years of attestation or rule, later life dates; “nach”/“vor” give only lower or upper bounds. The bars are therefore not exact reigns."),
  bi("Die Tafeln widersprechen sich teilweise: Tab. I gibt Heinrich von Plauen mit 1244—c. 1296 und Heinrich von Gera mit 1244—c. 1274, Tab. IV und III dagegen mit † 1303 bzw. † vor Ende August 1279 (auch der Text S. 354 und 342). Hier gelten die Daten der Einzeltafeln.",
     "The tables partly contradict each other: Tab. I gives Heinrich of Plauen as 1244—c. 1296 and Heinrich of Gera as 1244—c. 1274, whereas Tab. IV and III give † 1303 and † before the end of August 1279 (as do the text on pp. 354 and 342). The dates of the individual tables are used here."),
  bi("Für Heinrich den Dispensirten druckt Tab. III »1419 Ende od. 1520 Anfang«; gemeint ist 1420 (S. 346: »Ende 1419 oder zu Anfang 1420«). Hier gilt 1419 als letztes sicheres Jahr.",
     "For Heinrich the Dispensed, Tab. III prints “1419 Ende od. 1520 Anfang” (end of 1419 or beginning of 1520); 1420 is meant (p. 346: “end of 1419 or beginning of 1420”). 1419 is used here as the last certain year."),
  bi("Die Gliederung in »Landesherr«, »Geistlicher« und »ohne Herrschaft« ist eine redaktionelle Zuordnung nach den Angaben der Tafeln (Titel, Aufenthalt); Frauen und andere Namen sind nicht erfasst.",
     "The grouping into “lord”, “cleric” and “no lordship” is an editorial assignment based on the details of the tables (title, residence); women and persons with other names are not recorded."),
 ],
 "datasets": [
  {"name": "heinriche", "title": bi("Die Heinriche der Tafeln I–V", "The Heinrichs of Tables I–V"),
   "columns": [
    {"name": "ord", "label": bi("Nr.", "No."), "type": "integer", "unit": None, "derived": True},
    {"name": "line", "label": bi("Linie (Code)", "Line (code)"), "type": "string", "unit": None, "derived": True},
    {"name": "line_de", "label": bi("Linie", "Line"), "type": "string", "unit": None, "derived": True},
    {"name": "line_en", "label": bi("Linie (englisch)", "Line (English)"), "type": "string", "unit": None, "derived": True},
    {"name": "tab", "label": bi("Tafel", "Table"), "type": "string", "unit": None},
    {"name": "name", "label": bi("Name (wie gedruckt)", "Name (as printed)"), "type": "string", "unit": None},
    {"name": "note", "label": bi("Zusatz (wie gedruckt)", "Note (as printed)"), "type": "string", "unit": None},
    {"name": "role", "label": bi("Stellung (Code)", "Role (code)"), "type": "string", "unit": None, "derived": True},
    {"name": "role_de", "label": bi("Stellung", "Role"), "type": "string", "unit": None, "derived": True},
    {"name": "role_en", "label": bi("Stellung (englisch)", "Role (English)"), "type": "string", "unit": None, "derived": True},
    {"name": "kind", "label": bi("Art der Daten (att = Bezeugung/Regierung, life = Lebensdaten)", "Kind of dates (att = attestation/rule, life = life dates)"), "type": "string", "unit": None, "derived": True},
    {"name": "first_year", "label": bi("erstes gedrucktes Jahr", "first printed year"), "type": "integer", "unit": None},
    {"name": "last_year", "label": bi("letztes gedrucktes Jahr", "last printed year"), "type": "integer", "unit": None},
    {"name": "end_qual", "label": bi("Zusatz zum Endjahr (x genau, c circa, n nach, v vor)", "Qualifier of the end year (x exact, c circa, n after, v before)"), "type": "string", "unit": None, "derived": True},
    {"name": "date_text", "label": bi("Datum (wie gedruckt)", "Date (as printed)"), "type": "string", "unit": None},
    {"name": "bar_start", "label": bi("Beginn des Balkens", "Start of bar"), "type": "integer", "unit": None, "derived": True},
    {"name": "bar_end", "label": bi("Ende des Balkens", "End of bar"), "type": "integer", "unit": None, "derived": True},
    {"name": "sortkey", "label": bi("Sortierschlüssel", "Sort key"), "type": "integer", "unit": None, "derived": True},
    {"name": "label", "label": bi("Beschriftung", "Label"), "type": "string", "unit": None, "derived": True},
    {"name": "page", "label": bi("Seite", "Page"), "type": "string", "unit": None},
    {"name": "block", "label": bi("Block", "Block"), "type": "string", "unit": None},
    {"name": "read_from_scan", "label": bi("am Faksimile gelesen, nicht in der Transkription", "read from the facsimile, not in the transcription"), "type": "string", "unit": None},
   ], "rows": rows, "source_refs": REFS},
  {"name": "presence", "title": bi("Landesherren namens Heinrich je Halbjahrhundert", "Lords named Heinrich per half-century"),
   "columns": [
    {"name": "line", "label": bi("Linie (Code)", "Line (code)"), "type": "string", "unit": None, "derived": True},
    {"name": "line_de", "label": bi("Linie", "Line"), "type": "string", "unit": None, "derived": True},
    {"name": "line_en", "label": bi("Linie (englisch)", "Line (English)"), "type": "string", "unit": None, "derived": True},
    {"name": "half_century", "label": bi("Halbjahrhundert ab", "Half-century from"), "type": "integer", "unit": None, "derived": True},
    {"name": "n_lords", "label": bi("bezeugte Landesherren", "attested lords"), "type": "integer", "unit": None, "derived": True},
   ], "rows": presence, "source_refs": REFS},
 ],
 "charts": [
  {"id": "c1", "dataset": "heinriche",
   "title": bi("Die Herren von Weida (Tab. I–II)", "The lords of Weida (Tab. I–II)"),
   "caption": bi("Balken: erstes bis letztes gedrucktes Jahr; Punkte: nur ein Jahr gedruckt. Beschriftung wie gedruckt, mit der Zählung d. ä./d. m./d. j. Geistliche und Ordensritter siehe Datensatz.",
                 "Bars: first to last printed year; dots: only one year printed. Names as printed, with the d. ä./d. m./d. j. numbering. Clerics and knights of the Order: see dataset."),
   "vegalite": gantt("datum.role == 'ruler' && datum.line == 'weida'", [1080, 1560])},
  {"id": "c2", "dataset": "heinriche",
   "title": bi("Die Herren von Gera und Plauen (Tab. III–IV)", "The lords of Gera and Plauen (Tab. III–IV)"),
   "caption": bi("Gera und die ältere Linie von Plauen mit den Burggrafen Heinrich I.–VII. Ab dem 16. Jahrhundert stehen Lebensdaten (geb.–†).",
                 "Gera and the older line of Plauen with the burgraves Heinrich I–VII. From the 16th century life dates (born–died) are given."),
   "vegalite": gantt("datum.role == 'ruler' && (datum.line == 'gera' || datum.line == 'plauen')", [1230, 1590])},
  {"id": "c3", "dataset": "heinriche",
   "title": bi("Die Herren von Reuß-Plauen (Tab. IV–V)", "The lords of Reuss-Plauen (Tab. IV–V)"),
   "caption": bi("Jüngere Linie Plauen bis zur Teilung von 1564. Ab 1506 Lebensdaten.",
                 "Younger line of Plauen up to the division of 1564. From 1506 life dates."),
   "vegalite": dict(gantt("datum.role == 'ruler' && datum.line == 'reuss'", [1270, 1590]), height=340)},
  {"id": "c4", "dataset": "presence",
   "title": bi("Gleichzeitig bezeugte Landesherren je Halbjahrhundert", "Lords attested at the same time per half-century"),
   "caption": bi("Ein Herr zählt für jedes Halbjahrhundert, das sein gedruckter Zeitraum berührt. Weida und Gera sind früh besetzt, Reuß-Plauen bleibt über 1550 hinaus.",
                 "A lord counts for each half-century that his printed period touches. Weida and Gera are densely recorded early, Reuss-Plauen continues beyond 1550."),
   "vegalite": {"height": 260,
    "mark": {"type": "line", "point": True},
    "encoding": {
      "x": {"field": "half_century", "type": "ordinal", "title": bi("Halbjahrhundert ab", "Half-century from"), "axis": {"labelAngle": 0}},
      "y": {"field": "n_lords", "type": "quantitative", "title": bi("bezeugte Landesherren", "attested lords")},
      "color": LCOL,
      "tooltip": [{"field": "half_century", "title": bi("ab Jahr", "from year")},
                  {"field": bi("line_de", "line_en"), "title": bi("Linie", "Line")},
                  {"field": "n_lords", "title": bi("Landesherren", "Lords")}]}}},
 ],
 "transcription_issues": [
  {"page": "352", "block": "b2", "transcribed": "Heinrich der Ältere", "facsimile": "Heinrich der Mehrer (Voigt von Gera, 1244 — † vor Ende August 1279)", "checked_facsimile": True, "note": "Der Text (S. 342) nennt ihn den »Mehrer seines Landes«."},
  {"page": "352", "block": "b3", "cell": "r1c1", "transcribed": "Irmgard v. Weimar", "facsimile": "Irmgard v. Weida, † nach 1317", "checked_facsimile": True},
  {"page": "352", "block": "b3", "cell": "r2c5", "transcribed": "Heinrich d. j., der Wohlbedachte", "facsimile": "Heinrich d. j., der Worthalter", "checked_facsimile": True, "note": "Auch der Text (S. 344) nennt ihn »der Worthalter«."},
  {"page": "352", "block": "b3", "cell": "r4c2", "transcribed": "Heinrich d. m., der Fintende, 1478 — † 1500", "facsimile": "Heinrich d. m., 1478 — † 1500. Herr von Schleiz und Reichenfels; der Beiname »der Hinkende« gehört zu Heinrich d. j. (1476 — † c. 1498)", "checked_facsimile": True},
  {"page": "352", "block": "b3", "cell": "r4c3", "transcribed": "(fehlt)", "facsimile": "Heinrich d. ä., 1474 — † c. 1488. Herr v. Gera u. Rochsburg; Heinrich, 1446 Domherr zu Köln", "checked_facsimile": True, "note": "Zwei Personen fehlen in der Transkription."},
  {"page": "352", "block": "b3", "cell": "r4c4", "transcribed": "Heinrich, 1495. † vor 1508.", "facsimile": "Heinrich, 1495. 1508.", "checked_facsimile": True, "note": "Im Druck steht kein »†«."},
  {"page": "352", "block": "b3", "cell": "r3c7", "transcribed": "1351 — 1419 Ende od. 1520 Anfang", "facsimile": "1351 — 1419 Ende od. 1520 Anfang", "checked_facsimile": True, "note": "Druckfehler im Original für 1420 (vgl. S. 346); Transkription entspricht dem Druck."},
 ],
 "keywords": {"de": ["Heinrich", "Voigte", "Weida", "Gera", "Plauen", "Reuß", "Genealogie", "Stammtafel", "Burggrafen von Plauen", "Heinrich der Dispensirte"],
              "en": ["Heinrich", "Voigts", "Weida", "Gera", "Plauen", "Reuss", "genealogy", "family tree", "burgraves of Plauen"]},
 "related": ["geschichte-landesteilungen-linien-1240-1870"],
 "generated_by": "Claude Sonnet 5.5 (subagent A12)",
 "date": "2026-10-01",
}

if __name__ == "__main__":
    write_analysis(a)
