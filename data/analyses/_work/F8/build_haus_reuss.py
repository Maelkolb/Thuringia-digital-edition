from f8common import *
import re
import statistics
from collections import Counter

g1 = arch("genealogie-voigte-heinriche-1143-1572")
g2 = arch("genealogie-reuss-lebensdauer-kindersterblichkeit-1550-1850")

heinriche = dataset(g1, "heinriche")
persons = dataset(g2, "persons")
cohorts = dataset(g2, "cohorts")

H = rows(heinriche)
P = rows(persons)
C = rows(cohorts)

# ------------------------------------------------------------ derived columns on heinriche
LINES = ["weida", "gera", "plauen", "reuss"]
order = []
pos = 0.0
group_rows = {}
for ln in LINES:
    grp = sorted([r for r in H if r["line"] == ln], key=lambda r: (r["bar_start"], r["bar_end"], r["ord"]))
    group_rows[ln] = grp
    for i, r in enumerate(grp):
        order.append((r["ord"], pos))
        pos += 1
    pos += 3
row_pos = dict(order)
add_column(heinriche, "row_pos", "Zeile im Diagramm", "Row in the chart", [row_pos[r["ord"]] for r in H], typ="number",
           note="nach Linie und erstem Jahr geordnet, mit Lücken zwischen den Linien")
add_column(heinriche, "end_plot", "Ende für die Zeichnung", "End for plotting",
           [r["bar_end"] if r["bar_end"] > r["bar_start"] else r["bar_start"] + 2 for r in H], typ="integer", unit=None,
           note="Personen mit nur einer Jahreszahl erhalten zwei Jahre Breite")
H = rows(heinriche)

rulers = [r for r in H if r["role"] == "ruler"]
others = [r for r in H if r["role"] != "ruler"]
n_all, n_rul, n_oth = len(H), len(rulers), len(others)
n_cleric = sum(1 for r in H if r["role"] == "cleric")
n_noreign = sum(1 for r in H if r["role"] == "other")
sim = lambda y: sum(1 for r in rulers if r["bar_start"] <= y <= r["bar_end"])
peak_year = max(range(1100, 1600), key=lambda y: (sim(y), -y))
peak_n = sim(peak_year)
print("peak", peak_year, peak_n, "first years with peak", [y for y in range(1100, 1600) if sim(y) == peak_n][:6])
n_dm = sum(1 for r in H if re.search(r"\bd\. ?(ä|m|j)\.", r["name"]))
win = lambda a, b: sum(1 for r in rulers if r["bar_start"] <= b and r["bar_end"] >= a)
n_1400 = win(1400, 1449)
print("98?", n_all, n_rul, n_oth, n_cleric, n_noreign, "d.a/m/j", n_dm, "1400-49", n_1400)
by_line_rul = Counter(r["line"] for r in rulers)
print(by_line_rul)

# last row of each house that ends (erlischt)
end_rows = {}
for ln, lab in (("weida", 1535), ("gera", 1550), ("plauen", 1572)):
    last = max(group_rows[ln], key=lambda r: (r["bar_end"], r["bar_start"]))
    end_rows[ln] = (last["ord"], last["bar_end"], last["name"])
    print(ln, end_rows[ln])

# group label places: free spot at the top right of each group
label_ord = {}
label_x = {}
for ln in LINES:
    grp = group_rows[ln]
    k = 2
    x = max(r["bar_end"] for r in grp[: k + 3]) + 30
    while any(r["bar_start"] < x + 70 and r["bar_end"] > x - 10 for r in grp[max(k - 1, 0): k + 2]):
        x += 10
    if x - 5 < peak_year < x + 55:
        x = peak_year + 12
    label_ord[ln] = grp[k]["ord"]
    label_x[ln] = x
print("labels", label_ord, label_x)

# ------------------------------------------------------------ numbers for child mortality
u = [r for r in P if 1550 <= r["birth_year"] <= 1799]
n_u = len(u)
n_u15 = sum(1 for r in u if r["age"] < 15)
n_u0 = sum(1 for r in u if r["age"] == 0)
n_65 = sum(1 for r in u if r["age"] >= 65)
share_u15 = {c["cohort"]: c["share_under15"] for c in C}
print("u", n_u, n_u15, n_u0, n_65, share_u15)
med = {}
for coh in (1550, 1600, 1650, 1700, 1750):
    sl = [r["age"] for r in u if r["cohort"] == coh and r["age"] >= 15]
    med[coh] = statistics.median(sl)
print("median 15+", med)
sh = {coh: 100 * sum(1 for r in u if r["cohort"] == coh and r["age"] < 15) / sum(1 for r in u if r["cohort"] == coh) for coh in (1550, 1600, 1650, 1700, 1750)}
print({k: round(v, 1) for k, v in sh.items()})
sh65 = {coh: 100 * sum(1 for r in u if r["cohort"] == coh and r["age"] >= 65) / sum(1 for r in u if r["cohort"] == coh) for coh in (1550, 1600, 1650, 1700, 1750)}
print({k: round(v, 1) for k, v in sh65.items()})
lo, hi = min(sh.values()), max(sh.values())
lo_c = min(sh, key=sh.get)
hi_c = max(sh, key=sh.get)

# ------------------------------------------------------------ chart 1
X_DOM = [1090, 1610]
xs = {"type": "quantitative", "scale": {"domain": X_DOM, "nice": False}}


def lookup(d, de_en):
    return "{" + ",".join(f"'{k}':'{v[de_en]}'" for k, v in d.items()) + "}[toString(datum.ord)]"


end_text = {}
for ln in ("weida", "gera", "plauen"):
    o, y, nm = end_rows[ln]
    qual = [r for r in H if r["ord"] == o][0]["end_qual"]
    yr = ("c. " if qual == "c" else "") + str(y)
    pre_de = "ältere Linie erlischt" if ln == "plauen" else "Linie erlischt"
    pre_en = "older line dies out" if ln == "plauen" else "line dies out"
    end_text[str(o)] = {"de": f"{pre_de} {yr}", "en": f"{pre_en} {yr}"}
print(end_text)

c1 = {
    "id": "c1",
    "dataset": "heinriche",
    "title": bi(
        f"{n_all} Heinriche in vier Linien: {peak_year} sind bis zu {peak_n} Landesherren zugleich bezeugt",
        f"{n_all} men named Heinrich in four lines: up to {peak_n} lords attested at once in {peak_year}",
    ),
    "caption": bi(
        "Jeder Balken ist ein Heinrich der Stammtafeln I bis V, vom ersten bis zum letzten gedruckten Jahr (später Lebensjahre), nach Linie und Beginn geordnet. Kurze Striche: nur ein Jahr genannt. Quelle: S. 331–372.",
        "Each bar is one Heinrich of genealogical tables I to V, from the first to the last printed year (later life dates), ordered by line and start. Short ticks: only one year given. Source: pp. 331–372.",
    ),
    "vegalite": {
        "height": 560,
        "encoding": {
            "y": {"field": "row_pos", "type": "quantitative", "scale": {"domain": [-4, 107], "reverse": True, "nice": False}, "axis": None},
        },
        "layer": [
            {
                "mark": {"type": "rule", "strokeDash": [3, 3], "color": "@muted"},
                "encoding": {"x": {"datum": peak_year, **xs}, "y": None},
            },
            {
                "transform": [{"calculate": "datum.row_pos + 0.78", "as": "row_end"}],
                "mark": {"type": "bar", "cornerRadius": 1.5, "stroke": None},
                "encoding": {
                    "x": {"field": "bar_start", **xs,
                          "axis": {"values": [1100, 1200, 1300, 1400, 1500, 1600], "format": "d", "title": None, "grid": True, "domain": False}},
                    "x2": {"field": "end_plot"},
                    "y2": {"field": "row_end"},
                    "color": {"condition": {"test": "datum.role == 'ruler'", "value": "@accent"}, "value": "@context"},
                    "tooltip": [
                        {"field": "label", "title": bi("Heinrich", "Heinrich")},
                        {"field": "note", "title": bi("Anmerkung", "Note")},
                        {"field": {"de": "line_de", "en": "line_en"}, "title": bi("Linie", "Line")},
                        {"field": {"de": "role_de", "en": "role_en"}, "title": bi("Stellung", "Role")},
                        {"field": "date_text", "title": bi("Gedruckt", "As printed")},
                    ],
                },
            },
            {
                "transform": [{"filter": f"indexof([{', '.join(str(label_ord[l]) for l in LINES)}], datum.ord) >= 0"},
                              {"calculate": "{" + ",".join(f"'{label_ord[l]}':{label_x[l]}" for l in LINES) + "}[toString(datum.ord)]", "as": "lx"}],
                "mark": {"type": "text", "align": "left", "baseline": "middle", "style": "label", "fontSize": 12, "color": "@ink"},
                "encoding": {"x": {"field": "lx", **xs}, "y": {"field": "row_pos", "type": "quantitative"}, "text": {"field": {"de": "line_de", "en": "line_en"}}},
            },
            {
                "transform": [{"filter": f"indexof([{', '.join(k for k in end_text)}], datum.ord) >= 0"},
                              {"calculate": {"de": lookup(end_text, "de"), "en": lookup(end_text, "en")}, "as": "end_note"}],
                "mark": {"type": "text", "align": "left", "baseline": "middle", "dx": 6, "style": "label-muted"},
                "encoding": {"x": {"field": "end_plot", **xs}, "y": {"field": "row_pos", "type": "quantitative"}, "text": {"field": "end_note"}},
            },
            {
                "transform": [{"filter": "datum.ord == 2"}],
                "mark": {"type": "text", "align": "left", "baseline": "middle", "dx": 6, "style": "annotation"},
                "encoding": {"x": {"datum": peak_year, **xs}, "y": {"datum": -2.2, "type": "quantitative"},
                             "text": {"value": bi(f"{peak_year}: {peak_n} Landesherren zugleich", f"{peak_year}: {peak_n} lords at once")}},
            },
            {
                "transform": [{"filter": "datum.ord == 2"}],
                "mark": {"type": "text", "align": "left", "baseline": "middle", "style": "label", "color": "@accent"},
                "encoding": {"x": {"datum": 1100, **xs}, "y": {"datum": 44, "type": "quantitative"},
                             "text": {"value": bi(f"{n_rul} Landesherren", f"{n_rul} lords")}},
            },
            {
                "transform": [{"filter": "datum.ord == 2"}],
                "mark": {"type": "text", "align": "left", "baseline": "middle", "style": "label-muted"},
                "encoding": {"x": {"datum": 1100, **xs}, "y": {"datum": 47.5, "type": "quantitative"},
                             "text": {"value": bi(f"{n_oth} Geistliche, Ritter, Erben", f"{n_oth} clerics, knights, heirs")}},
            },
        ],
    },
}

# ------------------------------------------------------------ chart 2: age classes by birth cohort
cohort_expr = "datum.cohort >= 1550 && datum.cohort <= 1750"
c2 = {
    "id": "c2",
    "dataset": "persons",
    "title": bi(
        "Jedes dritte Kind starb vor dem 15. Lebensjahr, wer es überlebte, wurde nach 1700 deutlich älter",
        "One child in three died before 15; those who survived lived much longer after 1700",
    ),
    "caption": bi(
        f"Anteil der Altersklassen beim Tod, je 50-Jahres-Jahrgang der {n_u} zwischen 1550 und 1799 Geborenen mit gedrucktem Sterbejahr (n links). Nachkommen der Stammväter Heinrich von Gera und Heinrich von Untergreiz. Quelle: S. 394–402.",
        f"Share of age classes at death by 50-year birth cohort of the {n_u} persons born 1550 to 1799 with a printed year of death (n at left). Descendants of the ancestors Heinrich of Gera and Heinrich of Untergreiz. Source: pp. 394–402.",
    ),
    "vegalite": {
        "height": {"step": 44},
        "padding": {"top": 4, "bottom": 26, "left": 4, "right": 8},
        "transform": [
            {"filter": cohort_expr},
            {"calculate": "datum.age < 15 ? 0 : datum.class_code", "as": "grp"},
            {"calculate": "datum.cohort_label", "as": "cl"},
            {"aggregate": [{"op": "count", "as": "n"}], "groupby": ["cl", "grp"]},
            {"joinaggregate": [{"op": "sum", "field": "n", "as": "total"}], "groupby": ["cl"]},
            {"window": [{"op": "sum", "field": "n", "as": "cum"}], "groupby": ["cl"], "sort": [{"field": "grp"}], "frame": [None, 0]},
            {"calculate": "(datum.cum - datum.n) / datum.total", "as": "x0"},
            {"calculate": "datum.cum / datum.total", "as": "x1"},
            {"calculate": "(datum.x0 + datum.x1) / 2", "as": "xm"},
            {"calculate": "datum.cl + ' (n = ' + datum.total + ')'", "as": "ylab"},
            {"calculate": "format(100 * datum.n / datum.total, '.0f') + ' %'", "as": "pct"},
        ],
        "encoding": {
            "y": {"field": "ylab", "type": "ordinal", "sort": "ascending", "axis": {"title": None, "ticks": False, "domain": False, "labelLimit": 300}},
        },
        "layer": [
            {
                "mark": {"type": "bar", "stroke": "@paper", "strokeWidth": 2, "cornerRadius": 0, "size": 30},
                "encoding": {
                    "x": {"field": "x0", "type": "quantitative", "scale": {"domain": [0, 1]}, "axis": None},
                    "x2": {"field": "x1"},
                    "color": {"field": "grp", "type": "ordinal", "legend": None,
                              "scale": {"domain": [0, 2, 3, 4], "range": ["@accent2", "@context", "@ink2", "@accent"]}},
                    "tooltip": [
                        {"field": "cl", "title": bi("Jahrgang", "Birth cohort")},
                        {"field": "grp", "title": bi("Altersklasse (0 = unter 15)", "Age class (0 = under 15)")},
                        {"field": "n", "title": bi("Personen", "Persons")},
                        {"field": "total", "title": bi("von", "of")},
                    ],
                },
            },
            {
                "mark": {"type": "text", "style": "label"},
                "encoding": {
                    "x": {"field": "xm", "type": "quantitative", "scale": {"domain": [0, 1]}},
                    "text": {"field": "pct"},
                    "color": {"condition": {"test": "datum.grp == 0 || datum.grp == 3 || datum.grp == 4", "value": "@paper"}, "value": "@ink"},
                },
            },
            {
                "transform": [
                    {"filter": "datum.cl == '1750–1799'"},
                    {"calculate": {"de": "datum.grp == 0 ? 'unter 15' : datum.grp == 2 ? '15–44' : datum.grp == 3 ? '45–64' : '65 und älter'",
                                   "en": "datum.grp == 0 ? 'under 15' : datum.grp == 2 ? '15–44' : datum.grp == 3 ? '45–64' : '65 and older'"}, "as": "gl"},
                ],
                "mark": {"type": "text", "style": "annotation", "dy": 31},
                "encoding": {
                    "x": {"field": "xm", "type": "quantitative", "scale": {"domain": [0, 1]}},
                    "text": {"field": "gl"},
                },
            },
        ],
    },
}


# ------------------------------------------------------------ text
sources_seen = []
for src in (g1["sources"], g2["sources"]):
    for s in src:
        key = (s["page"], s["block"])
        if key not in sources_seen:
            sources_seen.append(key)
sources = [{"page": p, "block": b} for p, b in sources_seen]

pc = lambda x: fmt_de(x, 1)
pc_en = lambda x: f"{x:.1f}"
summary = bi(
    f"Brückners Stammtafeln führen die Männer der Voigte von Weida, Gera und Plauen mit Jahreszahlen auf: {n_all} Heinriche, {n_rul} davon als Landesherren. "
    f"Für {n_u} zwischen 1550 und 1799 geborene Nachkommen der Reußen ist auch das Sterbealter gedruckt. "
    f"Davon starben {n_u15} ({pc(100 * n_u15 / n_u)} Prozent) vor dem 15. Lebensjahr, {n_u0} schon im Geburtsjahr.",
    f"Brückner’s genealogical tables list the men of the Voigts of Weida, Gera and Plauen with years: {n_all} men named Heinrich, {n_rul} of them as lords. "
    f"For {n_u} descendants of the Reuss lords born between 1550 and 1799 the age at death can be computed as well. "
    f"{n_u15} of them ({pc_en(100 * n_u15 / n_u)} percent) died before the age of 15, {n_u0} in the year of birth.",
)
findings = [
    bi(
        f"In den Tafeln I bis V unterscheidet der Name die Männer kaum: {n_dm} Einträge tragen »d. ä., d. m., d. j.«, Ziffern nur die Burggrafen Heinrich I. bis VII. von Plauen (1389–1572).",
        f"In tables I to V the name hardly tells the men apart: {n_dm} entries carry “d. ä., d. m., d. j.”, numerals only the burgraves Heinrich I to VII of Plauen (1389–1572).",
    ),
    bi(
        f"Für 1400 bis 1449 nennen die Tafeln {n_1400} verschiedene Landesherren namens Heinrich, davon {by_line_rul['weida'] and sum(1 for r in rulers if r['line']=='weida' and r['bar_start']<=1449 and r['bar_end']>=1400)} in Weida und {sum(1 for r in rulers if r['line']=='reuss' and r['bar_start']<=1449 and r['bar_end']>=1400)} in Reuß-Plauen.",
        f"For 1400 to 1449 the tables name {n_1400} different lords called Heinrich, {sum(1 for r in rulers if r['line']=='weida' and r['bar_start']<=1449 and r['bar_end']>=1400)} of them in Weida and {sum(1 for r in rulers if r['line']=='reuss' and r['bar_start']<=1449 and r['bar_end']>=1400)} in Reuss-Plauen.",
    ),
    bi(
        f"Der Anteil der vor dem 15. Jahr Gestorbenen liegt je Jahrgang zwischen {round(lo)} und {round(hi)} Prozent, ohne Rückgang. Wer 15 erreichte, starb im Median mit {med[1550]:.0f} (Jahrgang 1550–1599) bis {med[1750]:.0f} Jahren (1750–1799).",
        f"The share of children dying before 15 lies between {round(lo)} and {round(hi)} percent per cohort, with no decline. Survivors of 15 died at a median age of {med[1550]:.0f} (cohort 1550–1599) to {med[1750]:.0f} years (1750–1799).",
    ),
]
print(findings)

method = bi(
    "Aus den Stammtafeln I bis V (S. 331–372) wurden alle männlichen Personen mit gedruckten Jahreszahlen übernommen, Namen und Daten wie gedruckt. Bis ins 15. Jahrhundert geben die Tafeln die Jahre der Bezeugung oder Regierung, später Geburts- und Todesjahr. "
    "Die Balken laufen vom ersten zum letzten gedruckten Jahr; Zusätze wie »c.«, »nach«, »vor« stehen im Datensatz. Als Landesherr zählt, wer als Voigt, Herr oder Burggraf auftritt; Mönche, Domherren und Ordensritter sind Geistliche, Kinder und Erben ohne Herrschaft stehen getrennt. "
    "Die querformatigen Tafeln III und V wurden an Stellen, wo die Transkription Zellen verwechselte, am Faksimile geprüft. "
    "Für die Sterbealter wurden aus den Tafeln VI bis XIV alle Personen mit gedrucktem Geburtsjahr gesammelt (Ehepartner nicht), 342 davon mit Sterbejahr; doppelt vorkommende wurden zusammengeführt. Das Sterbealter ist die Differenz der Jahreszahlen, »im Geburtsjahr gestorben« steht für gleiche Jahre oder »g. u. †«. "
    "Die Anteile beschränken sich auf die Jahrgänge 1550 bis 1799; spätere sind unvollständig, weil Lebende ohne Sterbejahr fehlen.",
    "From genealogical tables I to V (pp. 331–372) all male persons with printed years were taken, names and dates as printed. Up to the 15th century the tables give the years of attestation or rule, later birth and death years. "
    "The bars run from the first to the last printed year; qualifiers such as “c.”, “nach” (after), “vor” (before) are in the dataset. A lord is anyone who acts as Voigt, Herr or burgrave; monks, canons and knights of the Order are clerics, children and heirs without a lordship are listed separately. "
    "Where the transcription confused cells in the sideways-printed tables III and V, the entries were checked against the facsimile. "
    "For the ages at death, all persons with a printed year of birth were collected from tables VI to XIV (spouses excluded), 342 of them with a year of death; persons occurring twice were merged. Age at death is the difference of the two years; “in the year of birth” stands for equal years or “g. u. †”. "
    "The shares are restricted to the birth cohorts 1550 to 1799; later cohorts are incomplete because living persons without a year of death are missing.",
)
caveats = [
    bi(
        "Die gedruckten Zeiträume sind nicht einheitlich: Bis ins 15. Jahrhundert sind es Jahre der Bezeugung oder Regierung, später Lebensdaten; »nach« und »vor« nennen nur Grenzen. Die Balken sind keine genauen Regierungszeiten.",
        "The printed periods are not uniform: up to the 15th century they are years of attestation or rule, later life dates; “nach” and “vor” give bounds only. The bars are not exact reigns.",
    ),
    bi(
        "Die Tafeln widersprechen sich teilweise: Tafel I gibt Heinrich von Plauen mit 1244 bis c. 1296 und Heinrich von Gera mit 1244 bis c. 1274, Tafel IV und III dagegen † 1303 und † vor Ende August 1279. Hier gelten die Daten der Einzeltafeln.",
        "The tables partly contradict each other: Table I gives Heinrich of Plauen as 1244 to c. 1296 and Heinrich of Gera as 1244 to c. 1274, whereas Tables IV and III give † 1303 and † before the end of August 1279. The dates of the individual tables are used.",
    ),
    bi(
        "Die Sterbealter beschreiben das Fürstenhaus, nicht die Bevölkerung: Es sind nur die Nachkommen zweier Stammväter, und Personen ohne gedrucktes Sterbejahr fehlen, vermutlich auch manche früh verstorbene Kinder.",
        "The ages at death describe the princely house, not the population: only the descendants of two ancestors are included, and persons without a printed year of death are missing, probably including some children who died early.",
    ),
    bi(
        "Das Sterbealter ist die Differenz der Jahreszahlen und auf ein Jahr genau. »Im Geburtsjahr« umfasst Totgeburten und Neugeborene; wer im Folgejahr starb, kann noch keinen Geburtstag erlebt haben und steht bei »1–14 Jahre«.",
        "The age at death is the difference of the years and accurate to one year. “In the year of birth” includes stillbirths and newborns; someone who died in the following year may not have reached a birthday and is counted under “1–14 years”.",
    ),
]

issues = copy.deepcopy(g1.get("transcription_issues", [])) + copy.deepcopy(g2.get("transcription_issues", []))

a = {
    "id": "haus-reuss",
    "title": bi("Die Voigte und das Haus Reuß", "The Voigts and the house of Reuss"),
    "category": "genealogy",
    "section": "t1-5-3",
    "merges": ["genealogie-voigte-heinriche-1143-1572", "genealogie-reuss-lebensdauer-kindersterblichkeit-1550-1850"],
    "sources": sources,
    "summary": summary,
    "findings": findings,
    "method": method,
    "caveats": caveats,
    "transcription_issues": issues,
    "datasets": [heinriche, persons],
    "charts": [c1, c2],
    "keywords": {
        "de": ["Voigte", "Heinrich", "Weida", "Gera", "Plauen", "Reuß", "Stammtafeln", "Lebensdauer", "Kindersterblichkeit", "Genealogie"],
        "en": ["Voigts", "Heinrich", "Weida", "Gera", "Plauen", "Reuss", "genealogical tables", "life span", "child mortality", "genealogy"],
    },
    "related": ["landesgeschichte", "geburten-sterbefaelle", "alter-familie"],
    "generated_by": "Claude Sonnet 5.5 (Agent F8), aus 2 Einzelauswertungen zusammengeführt",
    "date": "2026-10-02",
}

if __name__ == "__main__":
    write_feature(a, "haus-reuss")
