"""B01 analysis 1: Brückner's conversion table of historical units (pp. 831-832) as a reference dataset."""
import sys
from fractions import Fraction
sys.stdout.reconfigure(encoding="utf-8")
from common import write_analysis
from units_calc import build, LIN_PER_M, TOL_PCT

recs = build()
fmt = lambda x, nd=4: f"{x:.{nd}f}"
de = lambda x, nd=4: fmt(x, nd).replace(".", ",")

# ------------------------------------------------------------------ dataset rows
rows = []
for i, r in enumerate(recs, start=1):
    label = f"{r['unit']} ({r['district']})" if r["district"] not in ("ohne Angabe", "ganzes Fürstenthum") else r["unit"]
    rows.append([
        f"U{i:02d}", r["section"], r["quantity"], r["district"], r["district_printed"], r["unit"], r["definition"],
        r["n_kannen"], r["quart"], r["ref_len"], r["value"], r["unit_printed"],
        r["base"], r["unit_base"], r["recomp"], r["dev"], r["check"], r["rule"], label, r["note"],
        r["page"], r["block"], r["ref"],
    ])
cols = [
    ("unit_id", "Nr.", "No.", "string", None, False, "laufende Nummer in Brückners Reihenfolge (editorisch)"),
    ("section", "Abschnitt", "Section", "string", None, False, "römische Abschnittsnummer I–VII wie gedruckt"),
    ("quantity", "Größe", "Quantity", "string", None, False, "length | area | capacity | weight | firewood | stone | distance (editorisch)"),
    ("district", "Bezirk", "District", "string", None, False, "normalisiert: Schleiz = Schleiz, Tanna (und Hohenleuben) bzw. Landestheil Schleiz; Lobenstein = Lobenstein(-Ebersdorf)"),
    ("district_printed", "Bezirk (gedruckt)", "District (as printed)", "string", None, False, None),
    ("unit", "Einheit", "Unit", "string", None, False, "Kurzname der Einheit aus der gedruckten Definition"),
    ("definition_printed", "Definition (gedruckt)", "Definition (as printed)", "string", None, False, "linke Seite der Gleichung, wörtlich"),
    ("n_kannen", "Anzahl Kannen", "Number of Kannen", "integer", "Kannen", False, "nur wo Brückner die Kannenzahl nennt"),
    ("kanne_in_quart", "Kanne in preuß. Quart", "Kanne in Prussian Quart", "string", None, False, "Bruch wie gedruckt"),
    ("ref_length_par_lin", "Bezugslänge", "Reference length", "number", "par. Linien", False, "Länge der Elle bzw. des Fußes in Pariser Linien, wie gedruckt (Lobenstein-Klafter: 134,75 nach Faksimile)"),
    ("value_printed", "Metrischer Wert (gedruckt)", "Metric value (as printed)", "number", None, False, "Zahl der rechten Seite der Gleichung"),
    ("unit_printed", "Einheit (gedruckt)", "Unit (as printed)", "string", None, False, None),
    ("value_base", "Metrischer Wert in Basiseinheit", "Metric value in base unit", "number", None, True, "m, m², L, kg, m³; Hectoliter ×100, Hectar ×10 000, künftige Meile ×7500"),
    ("unit_base", "Basiseinheit", "Base unit", "string", None, True, None),
    ("recomputed_base", "Neu berechnet (Probe)", "Recomputed (check)", "number", None, True, "aus anderen gedruckten Werten der Tabelle, siehe recompute_rule"),
    ("deviation_pct", "Abweichung gedruckt/berechnet", "Deviation printed/recomputed", "number", "%", True, None),
    ("check", "Probe", "Check", "string", None, True, f"ok = Abweichung höchstens {str(TOL_PCT).replace('.', ',')} %"),
    ("recompute_rule", "Rechenweg der Probe", "Recomputation rule", "string", None, True, None),
    ("label", "Bezeichnung", "Label", "string", None, True, "Einheit + Bezirk für Diagramme (editorisch)"),
    ("note", "Anmerkung", "Note", "string", None, True, None),
    ("page", "Seite", "Page", "string", None, False, None),
    ("block", "Block", "Block", "string", None, False, None),
    ("ref", "Zeile", "Row/line", "string", None, False, "Tabellenzeile rN (S. 831) bzw. Textzeile lN im Block (S. 832)"),
]
columns = []
for n, lde, len_, t, u, der, note in cols:
    c = {"name": n, "label": {"de": lde, "en": len_}, "type": t, "unit": u}
    if der:
        c["derived"] = True
    if note:
        c["note"] = note
    columns.append(c)

# ------------------------------------------------------------------ statistics for the text
by = lambda unit: {r["district"]: r for r in recs if r["unit"] == unit}
K, E, L = by("Kanne"), by("Eimer"), by("Elle")
kmin = min(K.values(), key=lambda r: r["base"]); kmax = max(K.values(), key=lambda r: r["base"])
emin = min(E.values(), key=lambda r: r["base"]); emax = max(E.values(), key=lambda r: r["base"])
lmin = min(L.values(), key=lambda r: r["base"]); lmax = max(L.values(), key=lambda r: r["base"])
k_pct = (kmax["base"] / kmin["base"] - 1) * 100
e_pct = (emax["base"] / emin["base"] - 1) * 100
l_pct = (lmax["base"] / lmin["base"] - 1) * 100
checked = [r for r in recs if r["check"]]
ok = [r for r in checked if r["check"] == "ok"]
bad = [r for r in checked if r["check"] != "ok"]
assert {r["unit"] for r in bad} == {"Elle", "Scheffel"}, [(r["unit"], r["district"]) for r in bad]
sch = next(r for r in recs if r["unit"] == "Scheffel")
elle_g = L["Gera"]
implied_lin = elle_g["base"] * LIN_PER_M            # par. Linien implied by the printed metric value
max_ok = max(abs(r["dev"]) for r in ok)
klaf_l = next(r for r in recs if r["unit"] == "Klafter" and r["district"] == "Lobenstein")
dev_134775 = ((klaf_l["base"] / (126 * (134.775 / LIN_PER_M) ** 3)) - 1) * 100
eimer_kannen = {d: r["n_kannen"] for d, r in E.items()}
quart_vals = {d: r["base"] / float(Fraction(r["quart"])) for d, r in K.items()}
quart_mean = sum(quart_vals.values()) / len(quart_vals)
print("kanne", k_pct, "eimer", e_pct, "elle", l_pct, "checked", len(checked), "ok", len(ok), "max_ok", max_ok)
print("implied lin", implied_lin, "scheffel", sch["base"], sch["recomp"], "dev134775", dev_134775, "quart", quart_vals)

# ------------------------------------------------------------------ texts
title = {"de": "Maße und Gewichte: Brückners Umrechnungstabelle (1869)",
         "en": "Weights and measures: Brückner's conversion table (1869)"}
summary = {
    "de": (f"Brückner druckt als Nachtrag die amtliche Umrechnung der bisherigen Maße und Gewichte in das metrische System "
           f"(Ministerial-Bekanntmachung vom 20. März 1869): Längen-, Flächen-, Hohl-, Holz-, Bruchstein- und Entfernungsmaße, "
           f"getrennt nach den Landestheilen Gera, Schleiz, Lobenstein-Ebersdorf sowie Saalburg und Hirschberg. Die Tabelle wird hier "
           f"als Referenzdatensatz mit {len(recs)} Einheitendefinitionen erfasst; die Diagramme vergleichen Kanne, Eimer, Getreidemaße "
           f"und Elle der Bezirke in metrischen Einheiten."),
    "en": (f"As an addendum Brückner prints the official conversion of the former weights and measures into the metric system "
           f"(ministerial notice of 20 March 1869): measures of length, area, capacity, firewood, quarry stone and distance, given "
           f"separately for the districts of Gera, Schleiz, Lobenstein-Ebersdorf, and for Saalburg and Hirschberg. The table is captured "
           f"here as a reference dataset of {len(recs)} unit definitions; the charts compare the Kanne, Eimer, grain measures and Elle "
           f"of the districts in metric units."),
}
method = {
    "de": (f"Quelle sind S. 831 (Block b7 mit dem Faktor »443,296 pariser Linien = 1 Meter«, Block b8 mit den Längenmaßen) und S. 832 "
           f"(Blöcke b2–b12). Jede Gleichung der Tabelle ergibt eine Zeile; die Zahl rechts vom Gleichheitszeichen ist als »Metrischer Wert "
           f"(gedruckt)« mit der gedruckten Einheit übernommen, die Definition links wörtlich. Bezirksangaben sind auf Gera, Schleiz (mit Tanna, "
           f"Hohenleuben), Saalburg, Lobenstein (Lobenstein-Ebersdorf) und Hirschberg normalisiert, die gedruckte Fassung steht daneben. "
           f"Abgeleitet sind die Basiswerte (Hectoliter ×100 = Liter; Hectar ×10 000 = m²; künftige Meile ×7500 = m) und eine Probe: Wo die "
           f"Tabelle aus anderen gedruckten Werten nachrechenbar ist (Eimer = n Kannen, Klafter = n Kubikfuß, Elle aus Pariser Linien usw.), "
           f"steht der neu berechnete Wert samt Abweichung daneben; {len(ok)} von {len(checked)} Proben stimmen auf höchstens {de(max_ok, 3)} % "
           f"(Toleranz {str(TOL_PCT).replace('.', ',')} %). Alle Zahlen wurden am Faksimile (S. 831–832) geprüft."),
    "en": (f"The sources are p. 831 (block b7 with the factor “443,296 Paris lines = 1 metre”, block b8 with the length measures) and p. 832 "
           f"(blocks b2–b12). Each equation of the table yields one row; the number to the right of the equals sign is taken as “metric value "
           f"(as printed)” with the printed unit, the definition on the left verbatim. District names are normalised to Gera, Schleiz (with Tanna, "
           f"Hohenleuben), Saalburg, Lobenstein (Lobenstein-Ebersdorf) and Hirschberg, with the printed form alongside. Derived are the base values "
           f"(hectolitre ×100 = litres; hectare ×10,000 = m²; future mile ×7500 = m) and a check: where the table can be recomputed from other "
           f"printed values (Eimer = n Kannen, Klafter = n cubic feet, Elle from Paris lines, etc.) the recomputed value is given with its "
           f"deviation; {len(ok)} of {len(checked)} checks agree to within {max_ok:.3f} % (tolerance {TOL_PCT} %). All numbers were checked "
           f"against the facsimile (pp. 831–832)."),
}
findings = [
    {"de": (f"Die Kanne ist von Bezirk zu Bezirk verschieden: {de(kmin['base'])} L in {kmin['district']} gegenüber {de(kmax['base'])} L in "
            f"{kmax['district']} (dort 1 preuß. Quart), ein Unterschied von {de(k_pct, 1)} %. Alle vier Kannen sind Bruchteile desselben "
            f"preußischen Quarts (5/6, 3/4, 32/41, 1; Quart ≈ {de(quart_mean, 3)} L)."),
     "en": (f"The Kanne differs from district to district: {fmt(kmin['base'])} L in {kmin['district']} against {fmt(kmax['base'])} L in "
            f"{kmax['district']} (there 1 Prussian Quart), a difference of {k_pct:.1f} %. All four Kannen are fractions of the same "
            f"Prussian Quart (5/6, 3/4, 32/41, 1; Quart ≈ {fmt(quart_mean, 3)} L).")},
    {"de": (f"Der Eimer zählt in Gera, Schleiz und Lobenstein 72 Kannen, in Hirschberg nur {eimer_kannen['Hirschberg']}; wegen der größeren Kanne "
            f"ist er dort mit {de(emax['base'], 2)} L trotzdem der größte (Schleiz: {de(emin['base'], 2)} L, Unterschied {de(e_pct, 1)} %)."),
     "en": (f"The Eimer holds 72 Kannen in Gera, Schleiz and Lobenstein but only {eimer_kannen['Hirschberg']} in Hirschberg; because of the larger "
            f"Kanne it is nevertheless the largest there at {fmt(emax['base'], 2)} L (Schleiz: {fmt(emin['base'], 2)} L, a difference of {e_pct:.1f} %).")},
    {"de": (f"Für die Elle nennt Brückner fünf verschiedene Werte, von {de(lmin['base'])} m ({lmin['district']}, leipziger Elle) bis "
            f"{de(lmax['base'])} m ({lmax['district']}, alte hofer Elle); die längste ist {de(l_pct, 1)} % länger als die kürzeste. Landesweit gelten "
            f"dagegen der Baufuß (0,282655 m) und der preußische Fuß (0,313853 m)."),
     "en": (f"For the Elle Brückner gives five different values, from {fmt(lmin['base'])} m ({lmin['district']}, Leipzig ell) to "
            f"{fmt(lmax['base'])} m ({lmax['district']}, old Hof ell); the longest is {l_pct:.1f} % longer than the shortest. Valid throughout "
            f"the principality, by contrast, are the Baufuß (0.282655 m) and the Prussian foot (0.313853 m).")},
    {"de": (f"Die Probe bestätigt die Tabelle weitgehend: {len(ok)} von {len(checked)} nachrechenbaren Werten stimmen auf höchstens {de(max_ok, 3)} % mit den "
            f"aus anderen Angaben berechneten überein. Zwei Werte weichen im Druck ab: der Scheffel von Schleiz (gedruckt {de(sch['value'])} hl, aus "
            f"224 Kannen {de(sch['recomp'] / 100)} hl; vermutlich Druckfehler 4 statt 9) und die Elle von Gera (253,47 Pariser Linien, der metrische "
            f"Wert entspricht {de(implied_lin, 2)}; vermutlich Zahlendreher)."),
     "en": (f"The check largely confirms the table: {len(ok)} of {len(checked)} recomputable values agree with those derived from other entries to within "
            f"{max_ok:.3f} %. Two values deviate in the print itself: the Schleiz Scheffel (printed {fmt(sch['value'])} hl, from 224 Kannen "
            f"{fmt(sch['recomp'] / 100)} hl; presumably a misprint of 4 for 9) and the Gera Elle (253.47 Paris lines, whereas the metric value "
            f"corresponds to {fmt(implied_lin, 2)}; presumably transposed digits).")},
]
caveats = [
    {"de": ("Die Tabelle ist die amtliche Umrechnung von 1869 (Ministerial-Bekanntmachung v. 20. März 1869 und Nachtrag v. 14. August, nach Art. 21 der "
            "Maß- und Gewichtsordnung für den norddeutschen Bund vom 17. August 1868). Sie legt fest, was die Einheiten des Buchs metrisch bedeuten; "
            "sie sagt nicht, wie genau die älteren lokalen Maße im Gebrauch eingehalten wurden."),
     "en": ("The table is the official conversion of 1869 (ministerial notice of 20 March 1869 with a supplement of 14 August, under Art. 21 of the "
            "weights-and-measures ordinance for the North German Confederation of 17 August 1868). It fixes what the book's units mean in metric "
            "terms; it does not say how precisely the older local measures were observed in practice.")},
    {"de": (f"Die beiden gedruckten Unstimmigkeiten (Scheffel Schleiz, Elle Gera) stehen so im Original; der Datensatz gibt sie wie gedruckt wieder "
            f"und nennt daneben den berechneten Wert. Für Rechnungen mit dem Schleizer Scheffel ist {de(sch['recomp'] / 100)} hl wahrscheinlicher "
            f"als {de(sch['value'])} hl."),
     "en": (f"The two printed inconsistencies (Scheffel of Schleiz, Elle of Gera) are in the original; the dataset reproduces them as printed and "
            f"gives the recomputed value alongside. For calculations with the Schleiz Scheffel, {fmt(sch['recomp'] / 100)} hl is more likely than "
            f"{fmt(sch['value'])} hl.")},
    {"de": ("Die Tabelle erfasst nicht alle im Buch verwendeten Einheiten: Pariser Fuß und Pariser Linie (Höhen, Barometer), Réaumur-Grade und Währungen "
            "fehlen; für Brückners Faktor 443,296 pariser Linien = 1 Meter siehe »conversions«. Für Lobenstein-Ebersdorf gibt Brückner beim "
            "Bruchsteinmaß keinen Wert an (es gelten die geraische Ruthe im Chausseebau und die schleizer Schachtruthe im Privatverkehr)."),
     "en": ("The table does not cover all units used in the book: the Paris foot and Paris line (heights, barometer), Réaumur degrees and currencies "
            "are missing; for Brückner's factor 443,296 Paris lines = 1 metre see “conversions”. For Lobenstein-Ebersdorf Brückner gives no value "
            "for the quarry-stone measure (the Gera Ruthe applies in road building and the Schleiz Schachtruthe in private trade).")},
    {"de": "Die Diagramme verwenden die gedruckten Werte; die Rauten im Diagramm der Getreidemaße zeigen die aus der Kannenzahl berechneten Werte.",
     "en": "The charts use the printed values; the diamonds in the grain-measure chart show the values computed from the number of Kannen."},
]
conversions = [
    {"from": "1 Meter", "to": "pariser Linien", "factor_or_formula": "1 m = 443.296 par. Linien (1 par. Linie = 2.2558 mm)", "reference": "Brückner S. 831, Block b7"},
    {"from": "1 Pariser Fuß (144 Linien)", "to": "m", "factor_or_formula": f"1 Fuß = 144 / 443.296 m = {144 / LIN_PER_M:.6f} m",
     "reference": "aus Brückners Faktor (S. 831); 1 Fuß = 144 Linien editorisch"},
    {"from": "1 Hectoliter", "to": "Liter", "factor_or_formula": "1 hl = 100 L", "reference": "metrisch"},
    {"from": "1 Hectar", "to": "m²", "factor_or_formula": "1 ha = 10 000 m²", "reference": "metrisch; preuß. Morgen = 0,255322 ha (S. 832)"},
    {"from": "1 künftige Meile", "to": "m", "factor_or_formula": "1 künftige Meile = 7500 m", "reference": "Brückner S. 832, Block b12"},
    {"from": "1 preuß. Meile", "to": "m", "factor_or_formula": f"1.0043 künftige Meile × 7500 = {1.0043 * 7500:.2f} m", "reference": "Brückner S. 832, Block b12"},
    {"from": "1 Pfund (Zollpfund)", "to": "kg", "factor_or_formula": "1 Pfund = 0.5 kg", "reference": "Brückner S. 832, Block b6"},
]

# ------------------------------------------------------------------ charts
DOM = ["Gera", "Schleiz", "Lobenstein", "Hirschberg", "Saalburg"]
DIST = {"de": "Bezirk", "en": "District"}
LITRES = {"de": "Liter", "en": "Litres"}
SORT_Y = {"field": "value_base", "op": "max", "order": "descending"}
def color_for(values):
    return {"field": "district", "type": "nominal", "scale": {"domain": DOM}, "title": DIST, "legend": {"values": values}}


COLOR4 = color_for(["Gera", "Schleiz", "Lobenstein", "Hirschberg"])
COLOR5 = color_for(DOM)


def tip(extra=()):
    return [{"field": "label", "title": {"de": "Einheit", "en": "Unit"}},
            {"field": "definition_printed", "title": {"de": "Definition (gedruckt)", "en": "Definition (as printed)"}},
            {"field": "value_printed", "title": {"de": "Gedruckt", "en": "Printed"}},
            {"field": "unit_printed", "title": {"de": "Einheit (gedruckt)", "en": "Printed unit"}},
            {"field": "value_base", "title": {"de": "Basiseinheit", "en": "Base unit"}},
            {"field": "unit_base", "title": {"de": "Einheit", "en": "Unit"}}, *extra]


def bars(unit, ytitle, fmtstr, color, height=230):
    return {
        "height": height,
        "transform": [{"filter": f"datum.unit == '{unit}'"}],
        "layer": [
            {"mark": "bar",
             "encoding": {"x": {"field": "district", "type": "nominal", "sort": SORT_Y, "title": DIST, "axis": {"labelAngle": 0}},
                          "y": {"field": "value_base", "type": "quantitative", "title": ytitle},
                          "color": color, "tooltip": tip()}},
            {"mark": {"type": "text", "dy": -7},
             "encoding": {"x": {"field": "district", "type": "nominal", "sort": SORT_Y},
                          "y": {"field": "value_base", "type": "quantitative"},
                          "text": {"field": "value_base", "type": "quantitative", "format": fmtstr}}},
        ],
    }


GRAIN = ["dresdner Scheffel", "Viertel Getreidemaß", "Scheffel", "Achtel Kornmaß", "Achtel Hafermaß", "Achtel Getreidemaß"]
grain = {
    "height": 260,
    "transform": [{"filter": "indexof(" + str(GRAIN) + ", datum.unit) >= 0"}],
    "layer": [
        {"mark": "bar",
         "encoding": {"y": {"field": "label", "type": "nominal", "sort": SORT_Y, "title": None, "axis": {"labelLimit": 320}},
                      "x": {"field": "value_base", "type": "quantitative", "title": LITRES},
                      "color": COLOR4,
                      "tooltip": tip([{"field": "recomputed_base", "title": {"de": "aus Kannenzahl berechnet (L)", "en": "computed from Kannen (L)"}},
                                      {"field": "check", "title": {"de": "Probe", "en": "Check"}}])}},
        {"transform": [{"filter": "datum.recomputed_base != null"}],
         "mark": {"type": "text", "text": "◆", "fontSize": 14},
         "encoding": {"y": {"field": "label", "type": "nominal", "sort": SORT_Y},
                      "x": {"field": "recomputed_base", "type": "quantitative"}}},
    ],
}
charts = [
    {"id": "c1", "dataset": "units",
     "title": {"de": "Die Kanne in den Bezirken", "en": "The Kanne in the districts"},
     "caption": {"de": "Inhalt einer Kanne in Litern (Brückner S. 832). Die Hirschberger Kanne entspricht 1 preußischen Quart.",
                 "en": "Capacity of one Kanne in litres (Brückner p. 832). The Hirschberg Kanne equals 1 Prussian Quart."},
     "vegalite": bars("Kanne", LITRES, ".4f", COLOR4)},
    {"id": "c2", "dataset": "units",
     "title": {"de": "Der Eimer in den Bezirken", "en": "The Eimer in the districts"},
     "caption": {"de": "Inhalt eines Eimers in Litern: 72 Kannen in Gera, Schleiz und Lobenstein, 64 Kannen in Hirschberg.",
                 "en": "Capacity of one Eimer in litres: 72 Kannen in Gera, Schleiz and Lobenstein, 64 Kannen in Hirschberg."},
     "vegalite": bars("Eimer", LITRES, ".2f", COLOR4)},
    {"id": "c3", "dataset": "units",
     "title": {"de": "Getreidemaße in Litern", "en": "Grain measures in litres"},
     "caption": {"de": "Balken: gedruckter Wert. Raute: aus der Kannenzahl berechneter Wert. Nur beim Schleizer Scheffel (224 Kannen) liegen beide weit auseinander.",
                 "en": "Bars: printed value. Diamond: value computed from the number of Kannen. Only for the Schleiz Scheffel (224 Kannen) do the two differ widely."},
     "vegalite": grain},
    {"id": "c4", "dataset": "units",
     "title": {"de": "Die Elle in den Bezirken", "en": "The Elle in the districts"},
     "caption": {"de": "Länge einer Elle in Metern (Brückner S. 831): fünf verschiedene Ellen im Fürstenthum.",
                 "en": "Length of one Elle in metres (Brückner p. 831): five different ells in the principality."},
     "vegalite": bars("Elle", {"de": "Meter", "en": "Metres"}, ".4f", COLOR5)},
]

blocks832 = ("b2", "b4", "b6", "b8", "b10", "b12")
sources = ([{"page": "831", "block": "b6"}, {"page": "831", "block": "b7"}, {"page": "831", "block": "b8", "rows": "r2-r14"}]
           + [{"page": "832", "block": b} for b in blocks832])
ana = {
    "id": "masse-gewichte-umrechnung-1869",
    "title": title, "category": "economy", "section": "berichtigungen",
    "sources": sources, "summary": summary, "method": method, "findings": findings, "caveats": caveats,
    "conversions": conversions,
    "datasets": [{"name": "units", "title": {"de": "Einheitendefinitionen (Brückner S. 831–832)", "en": "Unit definitions (Brückner pp. 831–832)"},
                  "columns": columns, "rows": rows,
                  "source_refs": [{"page": "831", "block": "b8", "rows": "r2-r14"}] + [{"page": "832", "block": b} for b in blocks832]}],
    "charts": charts,
    "transcription_issues": [
        {"page": "832", "block": "b8", "transcribed": "den Fuß zu 134,775 par. Linien", "facsimile": "den Fuß zu 134,75 par. Linien",
         "checked_facsimile": True,
         "note": (f"Nürnberger Fuß im Abschnitt V c; mit 134,75 ergibt die Probe für 126 Kubikfuß 3,5390 m³ (Abweichung {klaf_l['dev']:+.4f} %), "
                  f"mit 134,775 wären es {dev_134775:+.3f} %.")},
    ],
    "keywords": {"de": ["Maße und Gewichte", "Umrechnung", "metrisches System", "Kanne", "Eimer", "Scheffel", "Elle", "Klafter", "Morgen", "Ruthe",
                        "Pariser Linie", "Entfernungsmaße", "Holzmaße"],
                 "en": ["weights and measures", "conversion", "metric system", "Kanne", "Eimer", "Scheffel", "ell", "Klafter", "Morgen", "Ruthe",
                        "Paris line", "distance measures", "firewood measures"]},
    "generated_by": "Claude Sonnet 5.5 (subagent B01)", "date": "2026-10-01",
}
print(write_analysis(ana))
