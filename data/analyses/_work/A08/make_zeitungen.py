"""Analysis: Zeitungsbezug durch die Post (p. 168 table + text, corrigendum p. 831)."""
import re
from _common import *

g = block("168", "b2")["grid"]
LT = ["Gera", "Schleiz", "Lobenstein-Ebersdorf"]
cur = None
rows_po, rows_lt = [], []
for r in g[1:]:
    name = r[0].replace(" . . .", "").replace(" .", "").replace(".", "").strip()
    if r[0].startswith("Gera") and r[1] == "Gera":
        cur = "Gera"
    elif r[0].startswith("Schleiz") and r[1] == "Schleiz":
        cur = "Schleiz"
    elif r[0].startswith("Lobenstein-Ebersdorf"):
        cur = "Lobenstein-Ebersdorf"
    if r[0] == "Summe":
        rows_lt.append([cur, int(num(r[2])), int(num(r[3])), int(num(r[4])), int(num(r[5]))])
    elif r[0] == "Gesammtsumme":
        rows_lt.append(["Gesamt", int(num(r[2])), int(num(r[3])), int(num(r[4])), int(num(r[5]))])
    else:
        rows_po.append([cur, r[1], int(num(r[2])), int(num(r[4]))])
print(rows_po)
print(rows_lt)
# sums check
for lt in LT:
    assert sum(r[2] for r in rows_po if r[0] == lt) == next(r[1] for r in rows_lt if r[0] == lt)
    assert sum(r[3] for r in rows_po if r[0] == lt) == next(r[3] for r in rows_lt if r[0] == lt)
tot = next(r for r in rows_lt if r[0] == "Gesamt")
assert sum(r[2] for r in rows_po) == tot[1] and sum(r[3] for r in rows_po) == tot[3]

rows_pc = []
for lt, cop, per_cop, tit, per_tit in rows_lt:
    rows_pc.append([lt, cop, per_cop, round(1000 / per_cop, 1), tit, per_tit, round(cop / tit, 1)])
pc = {r[0]: r for r in rows_pc}
print(rows_pc)

# local papers
t = text("168", "b3")
corr = text("831", "b5")
assert "S. 168. Z. 13 v. u. lies: eine statt zwei" in corr
assert "10996" in t and "acht" in t
local = [["Gera", 4], ["Schleiz", 2], ["Hohenleuben", 1], ["Lobenstein", 1]]
assert sum(r[1] for r in local) == 8
share_gera = round(100 * 739 / tot[1], 1)
def back(lt):
    r = pc[lt]
    return r[1] * r[2], r[4] * r[5]
bk = {lt: back(lt) for lt in LT}
print(bk)
def r100(x):
    return int(round(x, -2))
def de_t(x):
    return f"{r100(x):,}".replace(",", ".")
def en_t(x):
    return f"{r100(x):,}"

print("Gera post office share", share_gera)
top3 = sorted(rows_po, key=lambda r: -r[2])[:3]
print(top3)

ana = {
    "id": "kultur-zeitungsbezug-durch-die-post",
    "title": bi("Zeitungsbezug durch die Post", "Newspapers delivered by the post"),
    "category": "culture",
    "section": "t1-2-5",
    "sources": [
        {"page": "168", "block": "b2", "rows": "r2-r16"},
        {"page": "168", "block": "b3"},
        {"page": "831", "block": "b5", "note": "Berichtigung zu S. 168: in Lobenstein eine (statt zwei) Zeitung"},
    ],
    "summary": bi(
        "Als Maßstab für die geistige Regsamkeit der Bevölkerung zählt Brückner (S. 168), wie viele Zeitungsexemplare und wie viele verschiedene Zeitungen durch die elf Postämter und Poststellen des Landes bezogen werden. Insgesamt sind es 2229 Exemplare, die sich sehr ungleich auf die Postorte und die drei Landestheile verteilen: Am dichtesten ist der Bezug im Landestheil Schleiz, am dünnsten in Lobenstein-Ebersdorf.",
        "As a measure of the people’s mental alertness Brückner counts (p. 168) how many newspaper copies and how many different newspapers are taken through the eleven post offices and postal agencies of the country. In all there are 2229 copies, very unevenly distributed over the post towns and the three districts: the density of subscription is highest in the district of Schleiz and lowest in Lobenstein-Ebersdorf.",
    ),
    "method": bi(
        "Die Tabelle (S. 168, b2, r2–r16) wurde vollständig übernommen und die gedruckten Summen gegen die Einzelwerte geprüft (alle stimmen). Aus der gedruckten Kennzahl »1 Exemplar auf … Einw.« wurde der Bezug je 1000 Einwohner berechnet (1000 ÷ Einwohner je Exemplar). Die Zahl der Exemplare je Titel ist der Quotient der beiden gedruckten Spalten. Die Zahl der inländischen Zeitungen (acht) folgt Brückners Text mit der Berichtigung von S. 831 (Lobenstein: eine statt zwei). Einwohnerzahlen der Postbezirke sind nicht angegeben.",
        "The table (p. 168, b2, r2–r16) was taken over in full and the printed totals were checked against the individual values (all agree). From the printed ratio “1 copy per … inhabitants” the subscription per 1000 inhabitants was computed (1000 ÷ inhabitants per copy). Copies per title is the quotient of the two printed columns. The number of domestic newspapers (eight) follows Brückner’s text with the corrigendum on p. 831 (Lobenstein: one instead of two). The populations of the postal districts are not given.",
    ),
    "findings": [
        bi(
            f"Das Postamt Gera allein liefert 739 von 2229 Exemplaren ({dz(share_gera)} %); es folgen Schleiz (451) und Tanna (334). Tanna übertrifft mit 334 Exemplaren Lobenstein (160) und Hohenleuben (73) deutlich.",
            f"The Gera post office alone delivers 739 of 2229 copies ({ez(share_gera)} %); Schleiz (451) and Tanna (334) follow. With 334 copies Tanna clearly exceeds Lobenstein (160) and Hohenleuben (73).",
        ),
        bi(
            f"Je 1000 Einwohner ergeben sich im Landestheil Schleiz {dz(pc['Schleiz'][3])} Exemplare (1 auf 29), im Landestheil Gera {dz(pc['Gera'][3])} (1 auf 43) und in Lobenstein-Ebersdorf {dz(pc['Lobenstein-Ebersdorf'][3])} (1 auf 53); im ganzen Land {dz(pc['Gesamt'][3])} (1 auf 39).",
            f"Per 1000 inhabitants the district of Schleiz receives {ez(pc['Schleiz'][3])} copies (1 per 29), the district of Gera {ez(pc['Gera'][3])} (1 per 43) and Lobenstein-Ebersdorf {ez(pc['Lobenstein-Ebersdorf'][3])} (1 per 53); for the whole country {ez(pc['Gesamt'][3])} (1 per 39).",
        ),
        bi(
            f"Im Durchschnitt werden je Titel {dz(pc['Gesamt'][6])} Exemplare bezogen; in Schleiz sind es {dz(pc['Schleiz'][6])}, in Gera {dz(pc['Gera'][6])}, in Lobenstein-Ebersdorf nur {dz(pc['Lobenstein-Ebersdorf'][6])}.",
            f"On average {ez(pc['Gesamt'][6])} copies are taken per title; in Schleiz {ez(pc['Schleiz'][6])}, in Gera {ez(pc['Gera'][6])} and in Lobenstein-Ebersdorf only {ez(pc['Lobenstein-Ebersdorf'][6])}.",
        ),
        bi(
            "Im Land selbst erscheinen acht Zeitungen (Gera vier, Schleiz zwei, Hohenleuben und – nach der Berichtigung S. 831 – Lobenstein je eine), also eine auf 10996 Einwohner.",
            "Eight newspapers are published in the country itself (Gera four, Schleiz two, Hohenleuben and, according to the correction on p. 831, Lobenstein one each), i.e. one per 10,996 inhabitants.",
        ),
    ],
    "caveats": [
        bi(
            "Erfasst ist nur der Bezug durch die Post; Zeitungen aus dem Buchhandel, aus Lesezirkeln oder Gasthäusern fehlen. Das Jahr der Erhebung nennt Brückner nicht (um 1868).",
            "Only subscription through the post is covered; newspapers from booksellers, reading circles or inns are missing. Brückner does not state the year of the survey (about 1868).",
        ),
        bi(
            f"Die Spalte »Zeitungen« wird hier als Zahl der bezogenen verschiedenen Titel gelesen; Brückner erläutert sie nicht. Die Kennzahlen »auf … Einw.« sind aus Einwohnerzahlen der Postbezirke berechnet, die nicht gedruckt sind (die Rückrechnung aus beiden Kennzahlen ergibt für Gera {de_t(bk['Gera'][0])} bzw. {de_t(bk['Gera'][1])} Einwohner, für Schleiz {de_t(bk['Schleiz'][0])} bzw. {de_t(bk['Schleiz'][1])}, für Lobenstein-Ebersdorf {de_t(bk['Lobenstein-Ebersdorf'][0])} bzw. {de_t(bk['Lobenstein-Ebersdorf'][1])}).",
            f"The column “Zeitungen” is read here as the number of different titles taken; Brückner does not explain it. The ratios “per … inhabitants” are based on populations of the postal districts that are not printed (back-calculation from the two ratios gives {en_t(bk['Gera'][0])} and {en_t(bk['Gera'][1])} inhabitants for Gera, {en_t(bk['Schleiz'][0])} and {en_t(bk['Schleiz'][1])} for Schleiz, and {en_t(bk['Lobenstein-Ebersdorf'][0])} and {en_t(bk['Lobenstein-Ebersdorf'][1])} for Lobenstein-Ebersdorf).",
        ),
        bi(
            "Der Text auf S. 168 nennt für Lobenstein zwei Zeitungen, aber nur einen Titel; die Berichtigung auf S. 831 (»eine statt zwei«) stellt die Summe von acht Zeitungen her. Die Transkription stimmt mit dem Druck überein.",
            "The text on p. 168 names two newspapers for Lobenstein but only one title; the correction on p. 831 (“eine statt zwei”) restores the total of eight newspapers. The transcription agrees with the print.",
        ),
    ],
    "conversions": [
        {"from": "Einwohner je Exemplar", "to": "Exemplare je 1000 Einwohner", "factor_or_formula": "1000 ÷ Einwohner je Exemplar"}
    ],
    "datasets": [
        {
            "name": "post_offices",
            "title": bi("Bezogene Zeitungen nach Postämtern und Poststellen", "Newspapers taken by post offices and postal agencies"),
            "columns": [
                {"name": "district", "label": bi("Landestheil", "District"), "type": "string", "unit": None},
                {"name": "post_office", "label": bi("Postamt / Post-Expedition", "Post office / agency"), "type": "string", "unit": None},
                {"name": "copies", "label": bi("Zahl der Zeitungsexemplare", "Number of newspaper copies"), "type": "integer", "unit": "Exemplare"},
                {"name": "titles", "label": bi("Zeitungen (verschiedene Titel)", "Newspapers (different titles)"), "type": "integer", "unit": "Titel"},
            ],
            "rows": rows_po,
            "source_refs": [{"page": "168", "block": "b2", "rows": "r2-r15"}],
        },
        {
            "name": "districts",
            "title": bi("Summen und Kennzahlen nach Landestheilen", "Totals and ratios by district"),
            "columns": [
                {"name": "district", "label": bi("Landestheil", "District"), "type": "string", "unit": None},
                {"name": "copies", "label": bi("Zahl der Zeitungsexemplare", "Number of newspaper copies"), "type": "integer", "unit": "Exemplare"},
                {"name": "inh_per_copy", "label": bi("Einwohner je Exemplar", "Inhabitants per copy"), "type": "integer", "unit": "Einwohner"},
                {"name": "copies_per_1000", "label": bi("Exemplare je 1000 Einwohner", "Copies per 1000 inhabitants"), "type": "number", "unit": "Exemplare", "derived": True},
                {"name": "titles", "label": bi("Zeitungen (verschiedene Titel)", "Newspapers (different titles)"), "type": "integer", "unit": "Titel"},
                {"name": "inh_per_title", "label": bi("Einwohner je Zeitung", "Inhabitants per newspaper"), "type": "integer", "unit": "Einwohner"},
                {"name": "copies_per_title", "label": bi("Exemplare je Titel", "Copies per title"), "type": "number", "unit": "Exemplare", "derived": True},
            ],
            "rows": rows_pc,
            "source_refs": [{"page": "168", "block": "b2", "rows": "r5,r10,r15,r16"}],
        },
        {
            "name": "local_papers",
            "title": bi("Im Lande erscheinende Zeitungen", "Newspapers published in the country"),
            "columns": [
                {"name": "place", "label": bi("Ort", "Place"), "type": "string", "unit": None},
                {"name": "papers", "label": bi("Zahl der Zeitungen", "Number of newspapers"), "type": "integer", "unit": "Titel", "derived": True, "note": "im Text in Worten gedruckt (vier, zwei, eine, zwei); Lobenstein nach der Berichtigung S. 831: eine"},
            ],
            "rows": local,
            "source_refs": [{"page": "168", "block": "b3"}, {"page": "831", "block": "b5"}],
        },
    ],
    "charts": [
        {
            "id": "c1",
            "dataset": "post_offices",
            "title": bi("Zeitungsexemplare nach Postämtern", "Newspaper copies by post office"),
            "caption": bi(
                "Zahl der durch die Post bezogenen Exemplare, farbig nach Landestheil. Gera und Schleiz überragen die übrigen Postorte; Tanna steht mit 334 Exemplaren an dritter Stelle.",
                "Number of copies taken through the post, coloured by district. Gera and Schleiz tower over the other post towns; Tanna ranks third with 334 copies.",
            ),
            "vegalite": {
                "height": 340,
                "mark": "bar",
                "encoding": {
                    "y": {"field": "post_office", "type": "nominal", "sort": {"field": "copies", "order": "descending"}, "title": None},
                    "x": {"field": "copies", "type": "quantitative", "title": bi("Zeitungsexemplare", "Newspaper copies")},
                    "color": {"field": "district", "type": "nominal", "title": bi("Landestheil", "District"), "scale": {"domain": LT}, "legend": {"labelLimit": 400}},
                    "tooltip": [
                        {"field": "post_office", "title": bi("Postamt", "Post office")},
                        {"field": "district", "title": bi("Landestheil", "District")},
                        {"field": "copies", "title": bi("Exemplare", "Copies")},
                        {"field": "titles", "title": bi("Titel", "Titles")},
                    ],
                },
            },
        },
        {
            "id": "c2",
            "dataset": "districts",
            "title": bi("Zeitungsbezug je 1000 Einwohner", "Newspaper subscriptions per 1000 inhabitants"),
            "caption": bi(
                "Aus Brückners Kennzahl »1 Exemplar auf … Einwohner« umgerechnet. Im Landestheil Schleiz wird am meisten gelesen, in Lobenstein-Ebersdorf am wenigsten; die gestrichelte Linie ist der Landesdurchschnitt.",
                "Converted from Brückner’s ratio “1 copy per … inhabitants”. Reading is most common in the district of Schleiz and least in Lobenstein-Ebersdorf; the dashed line is the national average.",
            ),
            "vegalite": {
                "height": 240,
                "layer": [
                    {
                        "transform": [{"filter": "datum.district != 'Gesamt'"}],
                        "mark": "bar",
                        "encoding": {
                            "x": {"field": "district", "type": "nominal", "sort": ["Gera", "Schleiz", "Lobenstein-Ebersdorf"], "title": None, "axis": {"labelAngle": 0}},
                            "y": {"field": "copies_per_1000", "type": "quantitative", "title": bi("Exemplare je 1000 Einwohner", "Copies per 1000 inhabitants")},
                            "color": {"field": "district", "type": "nominal", "legend": None, "scale": {"domain": LT}},
                            "tooltip": [
                                {"field": "district", "title": bi("Landestheil", "District")},
                                {"field": "inh_per_copy", "title": bi("Einwohner je Exemplar", "Inhabitants per copy")},
                                {"field": "copies_per_1000", "title": bi("Exemplare je 1000 Einwohner", "Copies per 1000 inhabitants")},
                            ],
                        },
                    },
                    {
                        "transform": [{"filter": "datum.district == 'Gesamt'"}],
                        "mark": {"type": "rule", "strokeDash": [4, 3]},
                        "encoding": {"y": {"field": "copies_per_1000", "type": "quantitative"}},
                    },
                ],
            },
        },
    ],
    "transcription_issues": [],
    "keywords": {
        "de": ["Zeitungen", "Postämter", "Lesen", "Bildung", "Gera", "Schleiz", "Tanna", "Lobenstein"],
        "en": ["newspapers", "post offices", "reading", "literacy", "Gera", "Schleiz", "Tanna", "Lobenstein"],
    },
    "related": [],
    "generated_by": GEN,
    "date": DATE,
}
write(ana)
