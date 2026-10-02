"""Analysis: Militärpflichtige 1864-1866 (p. 173, footnote p. 162)."""
import re
from _common import *

g = block("173", "b1")["grid"]
years = [1864, 1865, 1866]
# row index in grid -> bilingual labels
CATS = {
    3: ("Vorläufig zurückgestellt", "Provisionally deferred", "zurueck"),
    4: ("Hautkrankheiten", "Skin diseases", "haut"),
    5: ("Augen-, Ohren-, Brustleiden", "Eye, ear, chest ailments", "augen"),
    6: ("Körper-/Nervenschwäche", "Bodily/nervous weakness", "koerper"),
    7: ("Krampfadern", "Varicose veins", "krampf"),
    8: ("Verkrüppelung", "Crippling / deformity", "verkr"),
    9: ("Plattfüße", "Flat feet", "platt"),
    10: ("Dicker Hals u. a. Gebrechen", "Goitre, other infirmities", "hals"),
    11: ("Unterwüchsig (unter 5′ 7″)", "Undersized (under 5′ 7″)", "unter"),
    13: ("Brauchbar", "Fit for service", "brauchbar"),
}
STATUS_FIT = bi("Tauglich", "Fit for service")
STATUS_NOT = bi("Zurückgestellt/untauglich", "Deferred/unfit")

total = {y: int(num(g[1][1 + i])) for i, y in enumerate(years)}
printed_sum = {y: int(num(g[11][1 + i])) for i, y in enumerate(years)}

rows_year = []
rows_mean = []
order = []
for r, (de, en, key) in CATS.items():
    cells = g[r - 1]
    counts = [int(num(c)) for c in cells[1:4]]
    avg = int(num(cells[4]))
    pct = num(cells[5])
    status = STATUS_FIT if key == "brauchbar" else STATUS_NOT
    order.append((pct, key))
    rows_mean.append([de, en, status["de"], status["en"], avg, pct])
    for y, c in zip(years, counts):
        rows_year.append([y, de, en, status["de"], status["en"], 1 if key == "brauchbar" else 0, c, round(100 * c / total[y], 1)])

# sort rows_mean by printed percent descending (stable)
rows_mean.sort(key=lambda r: -r[5])

# sums computed from the printed rows, to document the 1866 gap
col_sum = {y: sum(r[6] for r in rows_year if r[0] == y and r[5] == 0) for y in years}
gap = {y: printed_sum[y] - col_sum[y] for y in years}
print("printed sums", printed_sum, "column sums", col_sum, "gap", gap)
assert gap[1864] == 0 and gap[1865] == 0 and gap[1866] == 60

totals_rows = []
for y in years:
    fit = next(r[6] for r in rows_year if r[0] == y and r[5] == 1)
    totals_rows.append([y, total[y], printed_sum[y], col_sum[y], gap[y], fit, round(100 * fit / total[y], 1)])

# footnote p. 162: undersized per year
fn = text("162", "fn1")
m = re.findall(r"(\d{4})(?: waren)? unter (\d+) Rekruten (\d+,\d+)", fn)
print(m)
undersized_chk = [(int(y), int(n), num(p)) for y, n, p in m]
for y, n, p in undersized_chk:
    c = next(r[6] for r in rows_year if r[0] == y and r[1].startswith("Unterwüchsig"))
    assert n == total[y] and abs(100 * c / n - p) < 0.006, (y, c, n, p)

# final balance of the Ersatzgeschäft, end of 1867 (p. 173 b2)
b2 = text("173", "b2")
ersatz = [
    ["Militärpflichtige insgesamt", "Conscripts in total", 1778, None],
    ["dauernd unbrauchbar", "permanently unfit", 189, 10.63],
    ["zeitig unbrauchbar, zur Ersatzreserve gestellt", "temporarily unfit, placed in the replacement reserve", 193, 11.64],
]
for v in ("1778", "189", "10,63", "193", "11,64"):
    assert v in b2

# derived for text
share = {(r[0], r[2]): r[7] for r in rows_year}
fit_share = {y: next(r[6] for r in totals_rows if r[0] == y) for y in years}
print("fit share", fit_share)
und = {y: share[(y, "Undersized (under 5′ 7″)")] for y in years}
haut = {y: share[(y, "Skin diseases")] for y in years}
hals = {y: share[(y, "Goitre, other infirmities")] for y in years}
verk = {y: share[(y, "Crippling / deformity")] for y in years}
print(und, haut, hals, verk)
top = rows_mean[:5]
print(top)
mean_unfit = round(sum(r[5] for r in rows_mean if r[2] == STATUS_NOT["de"]), 2)
print("sum printed pct non-fit", mean_unfit)

CM_PER_ZOLL = 28.2655 / 12
thr_cm = round(67 * CM_PER_ZOLL, 1)
print("5'7'' =", thr_cm, "cm")

CAT = {"de": "Befund", "en": "Finding"}
ana = {
    "id": "gesundheit-militaer-tauglichkeit-1864-1866",
    "title": bi("Tauglichkeit der Militärpflichtigen 1864–1866", "Fitness of military conscripts, 1864–1866"),
    "category": "health",
    "section": "t1-2-6",
    "sources": [
        {"page": "173", "block": "b1", "rows": "r2-r13"},
        {"page": "173", "block": "b2"},
        {"page": "162", "block": "fn1"},
        {"page": "172", "block": "b6"},
    ],
    "summary": bi(
        f"Als »sicheren Maßstab« für die Gesundheit der männlichen Jugend wertet Brückner die jährlichen militärischen Musterungen. Die Tabelle auf S. 173 schlüsselt für 1864, 1865 und 1866 (zusammen {sum(total.values())} Militärpflichtige) auf, aus welchem Grund Pflichtige zurückgestellt oder ausgemustert wurden und wie viele »brauchbar« waren. Nur rund drei von zehn galten als tauglich; häufigste Einzelgründe waren zu geringe Körpergröße, »Dicker Hals und sonstige Gebrechen« sowie Körper- und Nervenschwäche.",
        f"Brückner treats the annual military examinations as a reliable measure of the health of the young men. The table on p. 173 breaks down, for 1864, 1865 and 1866 ({sum(total.values())} conscripts in all), why conscripts were deferred or rejected and how many were found fit (“brauchbar”). Only about three in ten were found fit; the most frequent single reasons were insufficient height, “goitre and other infirmities” and bodily and nervous weakness.",
    ),
    "method": bi(
        "Die Zählwerte (Jahre 1864–1866), die Durchschnitte und die Prozentspalte »In Proc.« stammen unverändert aus der Tabelle S. 173 (Block b1, Zeilen r2–r13); die Prozentwerte der Spalte sind auf den gedruckten Durchschnitt von 799 Pflichtigen bezogen. Zusätzlich wurden die Jahresanteile (Fälle ÷ Zahl der Militärpflichtigen des Jahres × 100) berechnet. Die Summenzeilen wurden gegen die Zeilen geprüft; die Unterwüchsigen (128/795, 67/771, 88/833) stimmen mit den Prozentangaben der Fußnote S. 162 überein (16,10; 8,69; 10,56). Die Maßangabe »5′ 7″ sächs. Maß« wurde über Brückners Baufuß (leipziger Werkmaß, S. 831) in Zentimeter umgerechnet, 12 Zoll je Fuß vorausgesetzt.",
        "Counts for 1864–1866, the averages and the percentage column “In Proc.” are taken unchanged from the table on p. 173 (block b1, rows r2–r13); the percentages refer to the printed average of 799 conscripts. In addition, annual shares (cases ÷ conscripts of the year × 100) were computed. The totals were checked against the rows; the undersized counts (128/795, 67/771, 88/833) agree with the percentages of the footnote on p. 162 (16.10, 8.69, 10.56). The height “5′ 7″ Saxon measure” was converted to centimetres via Brückner’s building foot (Leipzig work measure, p. 831), assuming 12 inches to the foot.",
    ),
    "findings": [
        bi(
            f"Im Durchschnitt der drei Jahre galten nur 242 von 799 Pflichtigen (30,29 %) als brauchbar; nach der gedruckten Summe wurden 69,71 % zurückgestellt oder aus gesundheitlichen Gründen ausgemustert. Der Anteil der Tauglichen stieg von {dz(fit_share[1864])} % (1864) auf {dz(fit_share[1865])} % (1865) und {dz(fit_share[1866])} % (1866).",
            f"On average over the three years only 242 of 799 conscripts (30.29 %) were found fit; according to the printed total 69.71 % were deferred or rejected. The share found fit rose from {fit_share[1864]:.1f} % (1864) to {fit_share[1865]:.1f} % (1865) and {fit_share[1866]:.1f} % (1866).",
        ),
        bi(
            "Größter Einzelgrund ist zu geringe Körpergröße (unter 5′ 7″, nach der Umrechnung rund 158 cm) mit 11,76 %, gefolgt von »Dickem Hals und sonstigen Gebrechen« (10,1 %), Körper- und Nervenschwäche (9,38 %) sowie Augen-, Ohren- und Brustleiden (8,76 %).",
            f"The largest single reason is insufficient height (under 5′ 7″, about {thr_cm:.0f} cm after conversion) with 11.76 %, followed by “goitre and other infirmities” (10.1 %), bodily and nervous weakness (9.38 %) and eye, ear and chest ailments (8.76 %).",
        ),
        bi(
            f"Die Einzelgründe schwanken von Jahr zu Jahr stark: Der Anteil der Unterwüchsigen fiel von {dz(und[1864])} % (1864) auf {dz(und[1865])} % (1865), »Dicker Hals und sonstige Gebrechen« von {dz(hals[1864])} % auf {dz(hals[1866])} % (1866), während Hautkrankheiten von {dz(haut[1864])} % auf {dz(haut[1865])} % (1865) und Verkrüppelung von {dz(verk[1864])} % auf {dz(verk[1866])} % (1866) zunahmen.",
            f"The individual reasons vary strongly from year to year: the share of undersized men fell from {und[1864]:.1f} % (1864) to {und[1865]:.1f} % (1865) and “goitre and other infirmities” from {hals[1864]:.1f} % to {hals[1866]:.1f} % (1866), whereas skin diseases rose from {haut[1864]:.1f} % to {haut[1865]:.1f} % (1865) and crippling from {verk[1864]:.1f} % to {verk[1866]:.1f} % (1866).",
        ),
        bi(
            "Nach der Übersicht über das Ersatzgeschäft Ende 1867 waren von 1778 Militärpflichtigen 189 (10,63 %) dauernd unbrauchbar und 193 (11,64 %) wegen zeitiger Unbrauchbarkeit zur Ersatzreserve gestellt.",
            "According to the overview of the recruitment procedure at the end of 1867, of 1778 conscripts 189 (10.63 %) were permanently unfit and 193 (11.64 %) were placed in the replacement reserve because of temporary unfitness.",
        ),
    ],
    "caveats": [
        bi(
            "Die gedruckte Summe für 1866 (575) stimmt nicht mit der Addition der Einzelzeilen überein (515); die Differenz von 60 Pflichtigen ist im Druck nicht aufgeschlüsselt. Die Summe 575 passt zu 833 − 258 (brauchbar), die Einzelwerte passen zu den gedruckten Durchschnitten; entsprechend ergeben die gedruckten Prozentwerte der neun Einzelgründe zusammen 67,02 % und nicht die gedruckten 69,71 %. Am Faksimile geprüft: Die Transkription gibt den Druck richtig wieder.",
            "The printed total for 1866 (575) does not agree with the sum of the individual rows (515); the difference of 60 conscripts is not accounted for in the print. The total 575 fits 833 − 258 (fit), while the row values fit the printed averages; accordingly the printed percentages of the nine individual reasons add up to 67.02 %, not to the printed 69.71 %. Checked against the facsimile: the transcription reproduces the print correctly.",
        ),
        bi(
            "Die Prozentspalte bezieht sich auf den Durchschnitt von 799 Pflichtigen und ist deshalb nicht der Mittelwert der Jahresanteile; für »Dicker Hals und sonstige Gebrechen« druckt Brückner 10,1 (80/799 = 10,01).",
            "The percentage column refers to the average of 799 conscripts and is therefore not the mean of the annual shares; for “goitre and other infirmities” Brückner prints 10.1 (80/799 = 10.01).",
        ),
        bi(
            "Die Umrechnung der Körpergröße ist eine Näherung: Brückner gibt nur das »sächsische Maß« an; angenommen wurde der leipziger Baufuß (0,282655 m) mit 12 Zoll je Fuß. Die Zahl 1778 der Schlussübersicht ist nicht mit der Summe der drei Jahrgänge (2399) vereinbar und bezieht sich offenbar auf einen anderen Zeitraum.",
            "The height conversion is an approximation: Brückner gives only “Saxon measure”; the Leipzig building foot (0.282655 m) with 12 inches to the foot was assumed. The figure of 1778 in the closing overview cannot be reconciled with the sum of the three cohorts (2399) and evidently refers to a different period.",
        ),
    ],
    "conversions": [
        {
            "from": "5′ 7″ sächsisches Maß (Mindestgröße)",
            "to": "cm",
            "factor_or_formula": "67 Zoll × 28.2655 cm / 12 ≈ " + f"{thr_cm}" + " cm",
            "reference": "1 Baufuß (leipziger Werkmaß) = 0,282655 m (Brückner S. 831); 12 Zoll = 1 Fuß (Annahme)",
        }
    ],
    "datasets": [
        {
            "name": "by_year",
            "title": bi("Befund der Militärpflichtigen nach Jahr", "Findings for conscripts by year"),
            "columns": [
                {"name": "year", "label": bi("Jahr", "Year"), "type": "integer", "unit": None},
                {"name": "category_de", "label": bi("Befund (de)", "Finding (de)"), "type": "string", "unit": None},
                {"name": "category_en", "label": bi("Befund (en)", "Finding (en)"), "type": "string", "unit": None},
                {"name": "status_de", "label": bi("Gruppe (de)", "Group (de)"), "type": "string", "unit": None, "derived": True},
                {"name": "status_en", "label": bi("Gruppe (en)", "Group (en)"), "type": "string", "unit": None, "derived": True},
                {"name": "is_fit", "label": bi("Brauchbar (1) / nicht brauchbar (0)", "Fit (1) / not fit (0)"), "type": "integer", "unit": None, "derived": True},
                {"name": "count", "label": bi("Anzahl", "Number"), "type": "integer", "unit": "Personen"},
                {"name": "share_pct", "label": bi("Anteil an den Militärpflichtigen des Jahres", "Share of the year’s conscripts"), "type": "number", "unit": "%", "derived": True},
            ],
            "rows": rows_year,
            "source_refs": [{"page": "173", "block": "b1", "rows": "r2-r13"}],
        },
        {
            "name": "mean",
            "title": bi("Durchschnitt 1864–1866 (gedruckt)", "Average 1864–1866 (as printed)"),
            "columns": [
                {"name": "category_de", "label": bi("Befund (de)", "Finding (de)"), "type": "string", "unit": None},
                {"name": "category_en", "label": bi("Befund (en)", "Finding (en)"), "type": "string", "unit": None},
                {"name": "status_de", "label": bi("Gruppe (de)", "Group (de)"), "type": "string", "unit": None, "derived": True},
                {"name": "status_en", "label": bi("Gruppe (en)", "Group (en)"), "type": "string", "unit": None, "derived": True},
                {"name": "avg_count", "label": bi("Durchschnitt pro Jahr", "Average per year"), "type": "integer", "unit": "Personen"},
                {"name": "pct_mean", "label": bi("In Prozent (Brückner)", "In per cent (Brückner)"), "type": "number", "unit": "%"},
            ],
            "rows": rows_mean,
            "source_refs": [{"page": "173", "block": "b1", "rows": "r2-r13"}],
        },
        {
            "name": "totals",
            "title": bi("Gesamtzahlen und Summenprüfung", "Totals and sum check"),
            "columns": [
                {"name": "year", "label": bi("Jahr", "Year"), "type": "integer", "unit": None},
                {"name": "conscripts", "label": bi("Militärpflichtige", "Conscripts"), "type": "integer", "unit": "Personen"},
                {"name": "printed_sum", "label": bi("Gedruckte Summe der Befunde", "Printed sum of findings"), "type": "integer", "unit": "Personen"},
                {"name": "row_sum", "label": bi("Summe der gedruckten Einzelzeilen", "Sum of the printed rows"), "type": "integer", "unit": "Personen", "derived": True},
                {"name": "gap", "label": bi("Differenz", "Difference"), "type": "integer", "unit": "Personen", "derived": True},
                {"name": "fit", "label": bi("Brauchbar", "Fit"), "type": "integer", "unit": "Personen"},
                {"name": "fit_pct", "label": bi("Anteil Brauchbare", "Share fit"), "type": "number", "unit": "%", "derived": True},
            ],
            "rows": totals_rows,
            "source_refs": [{"page": "173", "block": "b1", "rows": "r2-r13"}],
        },
        {
            "name": "ersatz_1867",
            "title": bi("Ersatzgeschäft, Stand Ende 1867", "Recruitment procedure, status at the end of 1867"),
            "columns": [
                {"name": "item_de", "label": bi("Gruppe (de)", "Group (de)"), "type": "string", "unit": None},
                {"name": "item_en", "label": bi("Gruppe (en)", "Group (en)"), "type": "string", "unit": None},
                {"name": "count", "label": bi("Anzahl", "Number"), "type": "integer", "unit": "Personen"},
                {"name": "pct", "label": bi("Prozent (Brückner)", "Per cent (Brückner)"), "type": "number", "unit": "%"},
            ],
            "rows": ersatz,
            "source_refs": [{"page": "173", "block": "b2"}],
        },
    ],
    "charts": [
        {
            "id": "c1",
            "dataset": "mean",
            "title": bi("Warum Militärpflichtige nicht eingestellt wurden", "Why conscripts were not taken"),
            "caption": bi(
                "Anteil an den Militärpflichtigen, Durchschnitt 1864–1866 (Spalte »In Proc.« bei Brückner). Der größte Teil entfällt auf Zurückstellung und gesundheitliche Gründe; tauglich waren rund 30 %.",
                "Share of conscripts, average 1864–1866 (column “In Proc.” in Brückner). Most fall under deferral and health reasons; about 30 % were fit.",
            ),
            "vegalite": {
                "height": 320,
                "mark": "bar",
                "encoding": {
                    "y": {
                        "field": {"de": "category_de", "en": "category_en"},
                        "type": "nominal",
                        "sort": {"field": "pct_mean", "order": "descending"},
                        "title": None,
                        "axis": {"labelLimit": 400},
                    },
                    "x": {"field": "pct_mean", "type": "quantitative", "title": {"de": "Prozent der Militärpflichtigen", "en": "Per cent of conscripts"}},
                    "color": {
                        "field": {"de": "status_de", "en": "status_en"},
                        "type": "nominal",
                        "title": None,
                        "scale": {"domain": [STATUS_FIT, STATUS_NOT]},
                        "legend": {"labelLimit": 400},
                    },
                    "tooltip": [
                        {"field": {"de": "category_de", "en": "category_en"}, "title": bi("Befund", "Finding")},
                        {"field": "avg_count", "title": bi("Durchschnitt pro Jahr", "Average per year")},
                        {"field": "pct_mean", "title": bi("Prozent", "Per cent")},
                    ],
                },
            },
        },
        {
            "id": "c2",
            "dataset": "by_year",
            "title": bi("Die drei Jahrgänge im Vergleich", "The three cohorts compared"),
            "caption": bi(
                "Anteil an den Militärpflichtigen des jeweiligen Jahres (berechnet), nur Gründe für Zurückstellung oder Untauglichkeit. Jede Zelle ist ein Befund in einem Jahr; auffällig sind die Unterwüchsigen (1864) und die Zunahme der Hautkrankheiten 1865/66.",
                "Share of the conscripts of each year (computed), reasons for deferral or unfitness only. Each cell is one finding in one year; notable are the undersized men (1864) and the rise of skin diseases in 1865/66.",
            ),
            "vegalite": {
                "height": 300,
                "transform": [{"filter": "datum.is_fit == 0"}],
                "mark": "rect",
                "encoding": {
                    "x": {"field": "year", "type": "ordinal", "title": bi("Jahr", "Year"), "axis": {"labelAngle": 0}},
                    "y": {
                        "field": {"de": "category_de", "en": "category_en"},
                        "type": "nominal",
                        "sort": {"field": "share_pct", "op": "mean", "order": "descending"},
                        "title": None,
                        "axis": {"labelLimit": 400},
                    },
                    "color": {"field": "share_pct", "type": "quantitative", "title": bi("Prozent", "Per cent")},
                    "tooltip": [
                        {"field": "year", "title": bi("Jahr", "Year")},
                        {"field": {"de": "category_de", "en": "category_en"}, "title": bi("Befund", "Finding")},
                        {"field": "count", "title": bi("Anzahl", "Number")},
                        {"field": "share_pct", "title": bi("Prozent des Jahrgangs", "Per cent of cohort")},
                    ],
                },
            },
        },
    ],
    "transcription_issues": [],
    "keywords": {
        "de": ["Militärpflichtige", "Musterung", "Tauglichkeit", "Körpergröße", "Gesundheit", "Plattfüße", "Krampfadern", "Reuß j. L."],
        "en": ["conscripts", "military examination", "fitness for service", "body height", "health", "flat feet", "varicose veins"],
    },
    "related": [],
    "generated_by": GEN,
    "date": DATE,
}
write(ana)
