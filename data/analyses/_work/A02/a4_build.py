"""Analysis gewaesser-heilquellen-lobenstein-analyse: Reichardt's analysis of the Neue Quelle and the Agnesquelle
at Lobenstein (p. 44, table = block b4).

The table was missing from the first text transcription and has since been restored as block b4 of page 44.
The values are therefore printed values (derived: false); the 14 values of each column add up exactly to the printed
'Summa der festen Bestandtheile' (2,5232 and 1,0082) - checked below."""
from common import *

M = lambda de_, en_: {"de": de_, "en": en_}

# order, German name as printed (ditto marks resolved), English, group, Neue Quelle, Agnesquelle  (None = printed dash)
TABLE = [
    (1, "Chlornatrium", "sodium chloride", "alkali", 0.1897, 0.0311),
    (2, "Schwefelsaures Natron", "sodium sulfate", "alkali", 0.1618, 0.0619),
    (3, "Schwefelsaures Kali", "potassium sulfate", "alkali", None, 0.0521),
    (4, "Natron, an organische Säuren gebunden", "sodium bound to organic acids", "alkali", 0.0297, None),
    (5, "Kali, an organische Säuren gebunden", "potassium bound to organic acids", "alkali", 0.1253, None),
    (6, "Zweifach kohlensaurer Kalk", "calcium bicarbonate", "earth", 0.8061, 0.1244),
    (7, "Zweifach kohlensaure Magnesia", "magnesium bicarbonate", "earth", 0.2807, 0.1307),
    (8, "Zweifach kohlensaures Maganoxydul", "manganese(II) bicarbonate", "iron", 0.1377, 0.0780),
    (9, "Zweifach kohlensaures Eisenoxydul", "iron(II) bicarbonate", "iron", 0.5698, 0.4148),
    (10, "Schwefelsaurer Kalk", "calcium sulfate", "earth", 0.0039, 0.0422),
    (11, "Thonerde", "alumina", "other", 0.0397, 0.0122),
    (12, "Lösliche Kieselsäure", "soluble silica", "other", 0.1259, 0.0061),
    (13, "Unlösliche organische Substanz", "insoluble organic matter", "other", 0.0331, 0.0243),
    (14, "Unlösliche aufgeschwemmte Theile", "insoluble suspended matter", "other", 0.0198, 0.0304),
]
SUM_PRINTED = {"Neue Quelle": 2.5232, "Agnesquelle": 1.0082}
for i, name in ((4, "Neue Quelle"), (5, "Agnesquelle")):
    s = round(sum(r[i] for r in TABLE if r[i] is not None), 4)
    assert abs(s - SUM_PRINTED[name]) < 1e-9, (name, s)
print("column sums match the printed totals:", SUM_PRINTED)

rows = []
for order, dename, enname, grp, nq, ag in TABLE:
    for spring, v in (("Neue Quelle", nq), ("Agnesquelle", ag)):
        if v is None:
            continue
        rows.append([order, dename, enname, grp, spring, v, round(v / SUM_PRINTED[spring] * 100, 1)])

tot = SUM_PRINTED
ratio = tot["Neue Quelle"] / tot["Agnesquelle"]
fe_n, fe_a = 0.5698, 0.4148
ca_n = 0.8061
alk = {s: round(sum(r[5] for r in rows if r[4] == s and r[3] == "alkali"), 4) for s in tot}
grp_sum = {(s, g): round(sum(r[5] for r in rows if r[4] == s and r[3] == g), 4) for s in tot for g in ("alkali", "earth", "iron", "other")}
print(alk, grp_sum)
iron_group_n = grp_sum[("Neue Quelle", "iron")]
iron_group_a = grp_sum[("Agnesquelle", "iron")]
top_a = max((r for r in rows if r[4] == "Agnesquelle"), key=lambda r: r[5])
assert top_a[1] == "Zweifach kohlensaures Eisenoxydul"
assert sorted((r[5] for r in rows if r[4] == "Neue Quelle"), reverse=True)[:2] == [ca_n, fe_n]
top_n = max((r for r in rows if r[4] == "Neue Quelle"), key=lambda r: r[5])
print(top_n, top_a)
pc = lambda x, t: x / t * 100

findings = [
    M(f"Die Neue Quelle enthält {de(tot['Neue Quelle'],4)} Teile feste Bestandteile in 10 000 Teilen Wasser, die Agnesquelle {de(tot['Agnesquelle'],4)}, also nur etwa {de(1/ratio*100,0)} % davon; die Neue Quelle ist {de(ratio,1)}-mal so stark mineralisiert. In Prozent sind das {de(tot['Neue Quelle']/100,3)} % bzw. {de(tot['Agnesquelle']/100,3)} % feste Stoffe – beide Wässer sind in absoluten Zahlen schwach mineralisiert.",
      f"The Neue Quelle contains {en(tot['Neue Quelle'],4)} parts of solids in 10,000 parts of water, the Agnesquelle {en(tot['Agnesquelle'],4)}, i.e. only about {en(1/ratio*100,0)} % of that; the Neue Quelle is {en(ratio,1)} times as strongly mineralized. In percent that is {en(tot['Neue Quelle']/100,3)} % and {en(tot['Agnesquelle']/100,3)} % solids – both waters are weakly mineralized in absolute terms."),
    M(f"Der Eisengehalt (zweifach kohlensaures Eisenoxydul) beträgt {de(fe_n,4)} bzw. {de(fe_a,4)} Teile. In der Agnesquelle ist Eisen der größte Einzelbestandteil ({de(pc(fe_a,tot['Agnesquelle']),0)} % der festen Stoffe), in der Neuen Quelle der zweitgrößte hinter dem Kalk ({de(ca_n,4)}; Eisen: {de(pc(fe_n,tot['Neue Quelle']),0)} %). Brückner nennt die neue Trinkquelle »eine der stärksten Eisenquellen Deutschlands«; ein Vergleich mit anderen Quellen ist aus seinem Text nicht möglich.",
      f"The iron content (iron(II) bicarbonate) is {en(fe_n,4)} and {en(fe_a,4)} parts respectively. In the Agnesquelle iron is the largest single constituent ({en(pc(fe_a,tot['Agnesquelle']),0)} % of the solids), in the Neue Quelle the second largest after lime ({en(ca_n,4)}; iron: {en(pc(fe_n,tot['Neue Quelle']),0)} %). Brückner calls the new drinking spring “one of the strongest iron springs in Germany”; a comparison with other springs is not possible from his text."),
    M(f"Alkalisalze (Natrium- und Kaliumverbindungen) machen in der Neuen Quelle {de(pc(alk['Neue Quelle'],tot['Neue Quelle']),0)} % der festen Stoffe aus ({de(alk['Neue Quelle'],4)}), in der Agnesquelle {de(pc(alk['Agnesquelle'],tot['Agnesquelle']),0)} % ({de(alk['Agnesquelle'],4)}).",
      f"Alkali salts (sodium and potassium compounds) make up {en(pc(alk['Neue Quelle'],tot['Neue Quelle']),0)} % of the solids in the Neue Quelle ({en(alk['Neue Quelle'],4)}) and {en(pc(alk['Agnesquelle'],tot['Agnesquelle']),0)} % in the Agnesquelle ({en(alk['Agnesquelle'],4)})."),
    M("Die gedruckten Summen (2,5232 und 1,0082) stimmen exakt mit der Summe der Einzelwerte überein; die Tabelle ist damit in sich schlüssig und die Übertragung bestätigt.",
      "The printed totals (2.5232 and 1.0082) agree exactly with the sum of the individual values; the table is thus internally consistent and the transcription confirmed."),
]
for f in findings:
    print(f["de"])

COLS = [
    {"name": "order", "label": M("Zeile in Brückners Tabelle", "Row in Brückner's table"), "type": "integer", "unit": None, "derived": True},
    {"name": "constituent", "label": M("Bestandteil (wie gedruckt)", "Constituent (as printed)"), "type": "string", "unit": None, "note": "Anführungszeichen der Tabelle (=) sind zu »Zweifach« bzw. »Unlösliche« aufgelöst; »Maganoxydul« steht so im Druck."},
    {"name": "constituent_en", "label": M("Bestandteil (englisch, modern)", "Constituent (English, modern)"), "type": "string", "unit": None, "derived": True},
    {"name": "group", "label": M("Stoffgruppe", "Group"), "type": "string", "unit": None, "derived": True, "note": "alkali = Natrium-/Kaliumverbindungen, earth = Kalk- und Magnesiumverbindungen, iron = Eisen und Mangan, other = übrige; editorisch"},
    {"name": "spring", "label": M("Quelle", "Spring"), "type": "string", "unit": None},
    {"name": "parts_per_10000", "label": M("Gehalt", "Content"), "type": "number", "unit": "Teile in 10 000 Teilen Wasser"},
    {"name": "share_pct", "label": M("Anteil an den festen Bestandteilen", "Share of the solids"), "type": "number", "unit": "%", "derived": True, "note": "Wert / gedruckte Summe der festen Bestandteile"},
]
PROP_ROWS = [
    ["Neue Quelle", 2.5232, 336.93, 9.5, 11.9, 1.00033],
    ["Agnesquelle", 1.0082, 235.0, 9.0, 11.25, 1.0002],
]
PROP_COLS = [
    {"name": "spring", "label": M("Quelle", "Spring"), "type": "string", "unit": None},
    {"name": "solids_total", "label": M("Summa der festen Bestandteile", "Total of solids"), "type": "number", "unit": "Teile in 10 000 Teilen Wasser"},
    {"name": "free_co2_cc", "label": M("Menge der freien Kohlensäure", "Amount of free carbonic acid"), "type": "number", "unit": "C. C.", "note": "Bezugsmenge im Druck nicht angegeben (vermutlich Kubikzentimeter je Liter)."},
    {"name": "temperature_r", "label": M("Temperatur", "Temperature"), "type": "number", "unit": "°R", "derived": True, "note": "Gedruckt »9 1/2° R.« bzw. »9° R.«; der Bruch ist hier als Dezimalzahl 9,5 geschrieben, daher als umgeschrieben markiert."},
    {"name": "temperature_c", "label": M("Temperatur", "Temperature"), "type": "number", "unit": "°C", "note": "Von Brückner/Reichardt selbst in °C angegeben (»9 1/2° R. = 11,9° C.«, »9° R. = 11,25° C.«); 9,5 × 1,25 = 11,875 ≈ 11,9."},
    {"name": "specific_gravity", "label": M("Spezifisches Gewicht", "Specific gravity"), "type": "number", "unit": None},
]
assert abs(9.5 * 1.25 - 11.9) < 0.03 and abs(9.0 * 1.25 - 11.25) < 1e-9

TT = lambda f, d, e: {"field": f, "title": M(d, e)}
CL = {"calculate": {"de": "datum.constituent", "en": "datum.constituent_en"}, "as": "constituent_l"}
c1 = {
    "height": 420,
    "transform": [CL],
    "mark": "bar",
    "encoding": {
        "y": {"field": "constituent_l", "type": "nominal", "title": None, "sort": {"field": "order", "op": "min"}, "axis": {"labelLimit": 340}},
        "yOffset": {"field": "spring", "type": "nominal", "sort": ["Neue Quelle", "Agnesquelle"]},
        "x": {"field": "parts_per_10000", "type": "quantitative", "title": M("Teile in 10 000 Teilen Wasser", "Parts in 10,000 parts of water")},
        "color": {"field": "spring", "type": "nominal", "title": None, "sort": ["Neue Quelle", "Agnesquelle"]},
        "tooltip": [TT("constituent", "Bestandteil (gedruckt)", "Constituent (as printed)"), TT("constituent_en", "Modern", "Modern"), TT("spring", "Quelle", "Spring"),
                    TT("parts_per_10000", "Teile in 10 000", "Parts in 10,000"), TT("share_pct", "Anteil an festen Stoffen (%)", "Share of solids (%)")],
    },
}
GL = {"calculate": {"de": "datum.group == 'alkali' ? 'Natrium/Kalium' : datum.group == 'earth' ? 'Kalk/Magnesia' : datum.group == 'iron' ? 'Eisen/Mangan' : 'übrige'",
                    "en": "datum.group == 'alkali' ? 'Sodium/potassium' : datum.group == 'earth' ? 'Lime/magnesia' : datum.group == 'iron' ? 'Iron/manganese' : 'other'"}, "as": "group_l"}
GO = {"calculate": "indexof(['alkali','earth','iron','other'], datum.group)", "as": "group_order"}
c2 = {
    "height": 170,
    "transform": [GL, GO],
    "mark": "bar",
    "encoding": {
        "y": {"field": "spring", "type": "nominal", "title": None, "sort": ["Neue Quelle", "Agnesquelle"]},
        "x": {"field": "parts_per_10000", "aggregate": "sum", "type": "quantitative", "title": M("Feste Bestandteile in Teilen je 10 000 Teile Wasser", "Solids in parts per 10,000 parts of water")},
        "color": {"field": "group_l", "type": "nominal", "title": None, "sort": {"field": "group_order", "op": "min"}},
        "order": {"field": "group_order", "type": "quantitative"},
        "tooltip": [TT("spring", "Quelle", "Spring"), TT("group_l", "Stoffgruppe", "Group"),
                    {"field": "parts_per_10000", "aggregate": "sum", "type": "quantitative", "title": M("Teile in 10 000", "Parts in 10,000")}],
    },
}

SRC_MAIN = [{"page": "44", "block": "b4", "rows": "r2-r19", "note": "Tabelle der Analyse (Neue Quelle, Agnesquelle)"},
            {"page": "44", "block": "b1", "note": "Einleitungssatz: Analyse von Prof. Dr. Reichardt, Jena"}]
ana = {
    "id": "gewaesser-heilquellen-lobenstein-analyse",
    "title": M("Chemische Analyse der Eisenquellen von Lobenstein (1868)", "Chemical analysis of the iron springs at Lobenstein (1868)"),
    "category": "hydrology",
    "section": "t1-1-6",
    "sources": SRC_MAIN,
    "summary": M(
        "Für die 1868 eröffnete Badeanstalt in Lobenstein druckt Brückner die Analyse des Jenaer Professors Reichardt für die »Neue Quelle« (wohl die neue Trinkquelle am Siechenberg) und die »Agnesquelle«: 14 Bestandteile in 10 000 Teilen Wasser, dazu Kohlensäure, Temperatur und spezifisches Gewicht. Die Auswertung stellt beide Quellen gegenüber und zeigt, aus welchen Stoffen sich die Mineralisierung zusammensetzt.",
        "For the spa opened at Lobenstein in 1868 Brückner prints the analysis by Professor Reichardt of Jena for the “Neue Quelle” (probably the new drinking spring at the Siechenberg) and the “Agnesquelle”: 14 constituents in 10,000 parts of water, plus carbonic acid, temperature and specific gravity. The analysis compares the two springs and shows what the mineralization consists of."),
    "method": M(
        "Die Tabelle auf S. 44 (Block b4) wurde Zeile für Zeile übernommen; die 14 Einzelwerte jeder Spalte ergeben genau die gedruckten Summen 2,5232 bzw. 1,0082. Die Bestandteile stehen so da, wie Reichardt sie nennt (hypothetische Salze, z. B. »zweifach kohlensaurer Kalk« = Calciumhydrogencarbonat); die Anführungszeichen der Tabelle (»„«) sind zu »Zweifach« bzw. »Unlösliche« aufgelöst. Die Gruppierung (Natrium/Kalium, Kalk/Magnesia, Eisen/Mangan, übrige), die englischen Namen und die Anteile an der Summe sind editorisch bzw. berechnet. Striche (—) im Druck bedeuten »nicht gefunden« und erscheinen im Datensatz nicht als Zeile. Die Temperatur gibt Brückner selbst in °R und °C an (9 1/2° R. = 11,9° C.); eine eigene Umrechnung war nicht nötig.",
        "The table on p. 44 (block b4) was taken over row by row; the 14 individual values of each column add up exactly to the printed totals 2.5232 and 1.0082. The constituents are given as Reichardt names them (hypothetical salts, e.g. “zweifach kohlensaurer Kalk” = calcium bicarbonate); the ditto marks of the table (“„”) are resolved to “Zweifach” and “Unlösliche”. The grouping (sodium/potassium, lime/magnesia, iron/manganese, other), the English names and the shares of the total are editorial or computed. Dashes (—) in the print mean “not found” and do not appear as rows in the dataset. Brückner himself gives the temperature in both °R and °C (9 1/2° R. = 11.9° C.), so no conversion of our own was needed."),
    "findings": findings,
    "caveats": [
        M("Die Bezugsmenge der freien Kohlensäure (»C. C.«, vermutlich Kubikzentimeter) ist im Druck nicht angegeben; die Zeile wird nur im Datensatz geführt, nicht gezeichnet.",
          "The reference quantity of the free carbonic acid (“C. C.”, presumably cubic centimeters) is not stated in the print; the row is given in the dataset only and not plotted."),
        M("Die Salze sind rechnerische Kombinationen der damals nachgewiesenen Ionen, keine tatsächlich gelösten Verbindungen; ein Vergleich mit heutigen Mineralwasseranalysen erfordert eine Umrechnung, die hier nicht vorgenommen wird.",
          "The salts are computed combinations of the ions detected at the time, not compounds actually in solution; comparison with modern mineral-water analyses requires a conversion that is not attempted here."),
    ],
    "datasets": [
        {"name": "composition", "title": M("Bestandteile der beiden Quellen", "Constituents of the two springs"), "columns": COLS, "rows": rows,
         "source_refs": SRC_MAIN},
        {"name": "properties", "title": M("Summe, Kohlensäure, Temperatur und spezifisches Gewicht", "Total, carbonic acid, temperature and specific gravity"),
         "columns": PROP_COLS, "rows": PROP_ROWS, "source_refs": SRC_MAIN},
    ],
    "charts": [
        {"id": "c1", "dataset": "composition",
         "title": M("Bestandteile der Neuen Quelle und der Agnesquelle", "Constituents of the Neue Quelle and the Agnesquelle"),
         "caption": M("Analyse von Prof. Dr. Reichardt, Jena, in Teilen auf 10 000 Teile Wasser; Reihenfolge wie in Brückners Tabelle. Fehlende Balken: im Druck »—« (nicht gefunden).",
                      "Analysis by Prof. Dr. Reichardt, Jena, in parts per 10,000 parts of water; order as in Brückner's table. Missing bars: printed “—” (not found)."),
         "vegalite": c1},
        {"id": "c2", "dataset": "composition",
         "title": M("Zusammensetzung der festen Bestandteile nach Stoffgruppe", "Composition of the solids by group of substances"),
         "caption": M("Summe der Einzelwerte je Quelle, nach Stoffgruppen gestapelt. Die Gesamtlängen entsprechen den gedruckten Summen 2,5232 und 1,0082.",
                      "Sum of the individual values per spring, stacked by group. The total lengths correspond to the printed totals 2.5232 and 1.0082."),
         "vegalite": c2},
    ],
    "keywords": {"de": ["Lobenstein", "Eisenquelle", "Mineralquelle", "Heilquelle", "Quellanalyse", "Reichardt", "Agnesquelle", "Badeanstalt", "Kohlensäure"],
                 "en": ["Lobenstein", "iron spring", "mineral spring", "spa", "water analysis", "Reichardt", "Agnesquelle", "bathing establishment", "carbonic acid"]},
    "generated_by": "Claude Sonnet 5.5 (subagent A02)",
    "date": "2026-10-01",
}
write_analysis(ana)
