"""Analysis: fish species of the principality by water body (pp. 87-88)."""
import re
from collections import Counter
from common import *

g1, g2 = grid("87", "b2"), grid("88", "b1")
rows_raw = [(("87", "b2"), i, r) for i, r in enumerate(g1[1:], start=2)] + [(("88", "b1"), i, r) for i, r in enumerate(g2[1:], start=2)]
assert len(rows_raw) == 34

WATER = [("saale", "Saale", "Saale"), ("elster", "Elster", "Elster"), ("wiesenthal", "Wiesenthal", "Wiesenthal stream"), ("teiche", "Teiche", "Ponds")]
ST = {  # key: (order, de, en)
    "present": (1, "vorhanden", "present"),
    "rare": (2, "selten", "rare"),
    "introduced": (3, "eingesetzt", "stocked"),
    "former": (4, "früher", "formerly"),
    "uncertain": (5, "fraglich", "uncertain"),
    "absent": (6, "nicht angegeben", "not given"),
}


def status(txt, prev_status):
    t = txt.strip()
    if t in ("—", "-", ""):
        return "absent"
    if t == "?":
        return "uncertain"
    if t.startswith("desgl"):
        return prev_status
    low = t.lower()
    if "eingesetzt" in low and "?" in low:
        return "uncertain"
    if "eingetreten" in low or "eingesetzt" in low:
        return "introduced"
    if low == "früher" or low.startswith("früher in") or "sonst hie und da" in low:
        return "former"
    if "selten" in low:  # selten, jetzt selten, jetzt sehr selten, seltener, sonst häufig jetzt selten
        return "rare"
    return "present"


# Modern names where the identification is certain (otherwise None); Brückner's names are 19th-century.
MOD = {
    1: ("Schlammpeitzger", "Weatherfish", "Misgurnus fossilis"), 2: ("Schmerle (Bartgrundel)", "Stone loach", "Barbatula barbatula"),
    3: ("Steinbeißer", "Spined loach", "Cobitis taenia"), 4: ("Karpfen", "Common carp", "Cyprinus carpio"),
    5: (None, None, None), 6: ("Karausche", "Crucian carp", "Carassius carassius"), 7: ("Schleie", "Tench", "Tinca tinca"),
    8: ("Barbe", "Barbel", "Barbus barbus"), 9: ("Gründling", "Gudgeon", "Gobio gobio"), 10: ("Bitterling", "Bitterling", "Rhodeus amarus"),
    11: ("Elritze", "Minnow", "Phoxinus phoxinus"), 12: ("Plötze (Rotauge)", "Roach", "Rutilus rutilus"),
    13: ("Rotfeder", "Rudd", "Scardinius erythrophthalmus"), 14: ("Döbel (Aitel)", "Chub", "Squalius cephalus"),
    15: ("Hasel", "Dace", "Leuciscus leuciscus"), 16: ("Aland (Nerfling)", "Ide", "Leuciscus idus"), 17: ("Rapfen", "Asp", "Aspius aspius"),
    18: ("Ukelei (Laube)", "Bleak", "Alburnus alburnus"), 19: ("Schneider", "Schneider", "Alburnoides bipunctatus"),
    20: ("Brachse (Blei)", "Common bream", "Abramis brama"), 21: (None, None, None), 22: ("Güster", "Silver bream", "Blicca bjoerkna"),
    23: ("Quappe (Aalquappe)", "Burbot", "Lota lota"), 24: ("Groppe (Mühlkoppe)", "European bullhead", "Cottus gobio"),
    25: ("Kaulbarsch", "Ruffe", "Gymnocephalus cernua"), 26: ("Flussbarsch", "European perch", "Perca fluviatilis"),
    27: ("Äsche", "Grayling", "Thymallus thymallus"), 28: ("Lachs", "Atlantic salmon", "Salmo salar"),
    29: ("Meerforelle (Lachsforelle)", "Sea trout", "Salmo trutta"), 30: ("Bachforelle", "Brown trout", "Salmo trutta"),
    31: ("Hecht", "Northern pike", "Esox lucius"), 32: ("Aal", "European eel", "Anguilla anguilla"),
    33: ("Flussneunauge", "River lamprey", "Lampetra fluviatilis"), 34: ("Bachneunauge", "Brook lamprey", "Lampetra planeri"),
}

cells, species = [], []
for (pg, bk), ri, r in rows_raw:
    m = re.match(r"(\d+)\.\s+(.*)$", r[0])
    no, name = int(m.group(1)), m.group(2).strip()
    pref = name.endswith("*")
    label = f"{no}. {name}"
    prev = None
    sts = []
    for wi, (wk, wde, wen) in enumerate(WATER):
        txt = r[wi + 1]
        s = status(txt, prev)
        prev = s
        sts.append(s)
        corr = "Bandschmerle statt Brandschmerle (S. 831)" if "Brandschmerle" in txt else None
        cells.append([no, label, "ja" if pref else None, wk, wde, wen, txt, s, ST[s][0], ST[s][1], ST[s][2], corr, pg, bk, ri])
    n_pres = sum(1 for s in sts if s != "absent")
    md = MOD[no]
    species.append([no, name.rstrip("*"), "ja" if pref else None, md[0], md[1], md[2], n_pres])
assert [s[0] for s in species] == list(range(1, 35))


cnt_all = {wk: Counter(c[7] for c in cells if c[3] == wk) for wk, _, _ in WATER}
n_water = {wk: sum(v for st_, v in cnt_all[wk].items() if st_ != "absent") for wk, _, _ in WATER}
n_pref = sum(1 for sp in species if sp[2])
RIV = ("saale", "elster", "wiesenthal")
all3 = [sp for sp in species if all(c[7] != "absent" for c in cells if c[0] == sp[0] and c[3] in RIV)]
pond = [sp for sp in species if any(c[0] == sp[0] and c[3] == "teiche" and c[7] != "absent" for c in cells)]
only_pond = [sp for sp in pond if sp[6] == 1]
n_unc = sum(1 for c in cells if c[7] == "uncertain")
decl = [c for c in cells if c[7] in ("rare", "former")]
pc = lambda a, b: 100 * a / b
print(n_water, n_pref, len(all3), len(pond), [p[1] for p in only_pond], n_unc, len(decl))

REFS = [{"page": "87", "block": "b2", "rows": "r2-r27"}, {"page": "88", "block": "b1", "rows": "r2-r9"}]
ana = {
    "id": "fauna-fische-gewaesser",
    "title": bi("Fische des Fürstenthums nach Gewässern", "Fish of the principality by water body"),
    "category": "fauna",
    "section": "t1-1-9",
    "sources": REFS + [{"page": "88", "block": "b2"}, {"page": "87", "block": "b1"}, {"page": "831", "block": "b3"}],
    "summary": bi(
        f"Brückner führt 34 Fischarten mit zoologischem Namen und Volksnamen für die Saale, die Elster, die Wiesenthal und die Teiche auf. Die Tabelle wurde in eine Matrix Art × Gewässer überführt: Die Saale ({n_water['saale']} Arten) und die Elster ({n_water['elster']}) sind artenreich, die Wiesenthal ({n_water['wiesenthal']}) und besonders die Teiche ({n_water['teiche']}) deutlich ärmer; bei Lachs, Äsche und Forelle verzeichnet Brückner Rückgänge.",
        f"Brückner lists 34 fish species with their zoological names and folk names for the Saale, the Elster, the Wiesenthal and the ponds. The table was turned into a species × water-body matrix: the Saale ({n_water['saale']} species) and the Elster ({n_water['elster']}) are rich in species, the Wiesenthal ({n_water['wiesenthal']}) and especially the ponds ({n_water['teiche']}) clearly poorer; for salmon, grayling and trout Brückner records declines."),
    "method": bi(
        "Die zweiteilige Tabelle (S. 87 Nr. 1–26, S. 88 Nr. 27–34) wurde vollständig übernommen, 34 Arten × 4 Gewässer = 136 Zellen. Jede Zelle wurde nach Brückners Wortlaut einer von fünf Stufen zugeordnet (abgeleitet): vorhanden (Volksname oder »häufig«), selten (selten, jetzt selten, seltener), eingesetzt (eingesetzt oder aus den Teichen eingetreten), früher (früher, sonst hie und da) und fraglich (?). Ein Strich (—) heißt, dass Brückner für das Gewässer nichts angibt. »desgl.« wurde zur Angabe der Zelle links aufgelöst. Das Sternchen (*) bezeichnet nach Brückner besonders bevorzugte Arten. Die Korrektur »Bandschmerle statt Brandschmerle« (S. 831) ist vermerkt. Heutige Namen und wissenschaftliche Namen stehen nur dort, wo die Zuordnung sicher ist; bei Nr. 5 und Nr. 21 fehlen sie.",
        "The two-part table (p. 87 nos. 1–26, p. 88 nos. 27–34) was taken over in full, 34 species × 4 water bodies = 136 cells. Each cell was assigned to one of five levels following Brückner's wording (derived): present (folk name or “häufig”), rare (selten, jetzt selten, seltener), stocked (stocked or strayed in from ponds), formerly (früher, sonst hie und da) and uncertain (?). A dash (—) means that Brückner gives nothing for the water body. “desgl.” (“ditto”) was resolved to the cell on the left. The asterisk (*) marks, according to Brückner, especially preferred species. The correction “Bandschmerle statt Brandschmerle” (p. 831) is noted. Modern and scientific names are given only where the identification is certain; for nos. 5 and 21 they are missing."),
    "findings": [
        bi(f"Die Saale hat {n_water['saale']} der 34 Arten, die Elster {n_water['elster']}, die Wiesenthal {n_water['wiesenthal']} (davon {n_unc} mit Fragezeichen) und die Teiche {n_water['teiche']}. {len(all3)} Arten stehen in allen drei Flussgebieten.",
           f"The Saale has {n_water['saale']} of the 34 species, the Elster {n_water['elster']}, the Wiesenthal {n_water['wiesenthal']} ({n_unc} of them with a question mark) and the ponds {n_water['teiche']}. {len(all3)} species are named in all three river systems."),
        bi(f"{n_pref} der 34 Arten ({de(pc(n_pref, 34), 0)} %) sind als besonders bevorzugt gekennzeichnet. In den Teichen werden nur {len(pond)} Arten genannt; die Karausche (Nr. 6) kommt ausschließlich dort vor. Karpfen und Schleie stehen in Saale, Elster und Wiesenthal ausdrücklich als aus den Teichen eingetreten.",
           f"{n_pref} of the 34 species ({en(pc(n_pref, 34), 0)} %) are marked as especially preferred. Only {len(pond)} species are named for the ponds; the crucian carp (no. 6) occurs only there. Carp and tench are explicitly given as strayed in from ponds in the Saale, Elster and Wiesenthal."),
        bi(f"Rückgänge vermerkt Brückner in {len(decl)} Zellen: der Lachs ist in Saale und Elster »jetzt sehr selten«, die Äsche in der Wiesenthal nur noch »früher«, die Steinforelle in der Elster »früher in Bächen, jetzt gezüchtet«, die Quappe in der Elster »sonst häufig, jetzt selten«. Im Text führt er das auf rücksichtslosen, räuberischen Fischfang und eine nach »altem Schlendrian« betriebene Fischzucht zurück (S. 87).",
           f"Brückner notes declines or rarity in {len(decl)} cells: the salmon is “jetzt sehr selten” in the Saale and Elster, the grayling in the Wiesenthal only “früher”, the brown trout in the Elster “früher in Bächen, jetzt gezüchtet”, the burbot in the Elster “sonst häufig, jetzt selten”. In the text he attributes the decline to reckless, predatory fishing and to fish-breeding carried on in the “old rut” (p. 87)."),
    ],
    "caveats": [
        bi("Brückners Namenliste ist nach heutiger Kenntnis nicht frei von Dubletten und überholten Namen (z. B. Nr. 5 Cyprinus dobula neben Nr. 14 Squalius cephalus; Nr. 12 und 13 mit gleichen Volksnamen). Die Zahl 34 ist daher die Zahl der Tabellenzeilen, nicht gesicherter Arten.",
           "By current knowledge Brückner's list of names is not free of duplicates and obsolete names (e.g. no. 5 Cyprinus dobula next to no. 14 Squalius cephalus; nos. 12 and 13 with the same folk names). The figure 34 is therefore the number of table rows, not of established species."),
        bi("Die Stufenzuordnung ist eine redaktionelle Vereinfachung; ein Strich heißt nicht, dass die Art im Gewässer fehlt. Bei Nr. 4 Karpfen und Nr. 7 Schleie steht »desgl.«, wodurch die Angabe »aus den Teichen eingetreten« für Elster und Wiesenthal übernommen wurde. Bachforelle (Nr. 30) und Lachsforelle (Nr. 29) werden heute zur selben Art (Salmo trutta) gerechnet.",
           "The level assignment is an editorial simplification; a dash does not mean that the species is absent from the water body. For no. 4 carp and no. 7 tench the entry is “desgl.”, so the statement “aus den Teichen eingetreten” was carried over to the Elster and Wiesenthal. Brown trout (no. 30) and sea trout (no. 29) are today counted as the same species (Salmo trutta)."),
        bi("Die Tabelle gibt Volksnamen je Gewässer an; mehrere Arten tragen denselben Namen (z. B. »Weissfisch« für Nr. 12, 16, 18, 19, 22), so dass die Volksnamen allein keine Art bestimmen.",
           "The table gives folk names per water body; several species bear the same name (e.g. “Weissfisch” for nos. 12, 16, 18, 19, 22), so folk names alone do not identify a species."),
    ],
    "datasets": [
        {"name": "fish_cells",
         "title": bi("Fischarten × Gewässer (S. 87–88)", "Fish species × water body (pp. 87–88)"),
         "columns": [
             col("species_no", "Nr.", "No.", "integer", None),
             col("species_label", "Zoologischer Name (Druck)", "Zoological name (print)", "string", None),
             col("preferred", "Besonders bevorzugt (*)", "Especially preferred (*)", "string", None),
             col("water_key", "Gewässer (Schlüssel)", "Water body (key)", "string", None, True),
             col("water_de", "Gewässer", "Water body", "string", None, True),
             col("water_en", "Gewässer (EN)", "Water body (EN)", "string", None, True),
             col("cell_text", "Angabe im Druck", "Entry in print", "string", None),
             col("status_key", "Stufe (Schlüssel)", "Level (key)", "string", None, True),
             col("status_order", "Stufe (Reihenfolge)", "Level (order)", "integer", None, True),
             col("status_de", "Stufe", "Level", "string", None, True),
             col("status_en", "Stufe (EN)", "Level (EN)", "string", None, True),
             col("correction", "Berichtigung (S. 831)", "Correction (p. 831)", "string", None),
             col("page", "Seite", "Page", "string", None),
             col("block", "Block", "Block", "string", None),
             col("table_row", "Tabellenzeile", "Table row", "integer", None, True),
         ],
         "rows": cells, "source_refs": REFS},
        {"name": "fish_species",
         "title": bi("Fischarten mit heutigen Namen (soweit sicher)", "Fish species with current names (where certain)"),
         "columns": [
             col("species_no", "Nr.", "No.", "integer", None),
             col("name_printed", "Zoologischer Name (Druck)", "Zoological name (print)", "string", None),
             col("preferred", "Besonders bevorzugt (*)", "Especially preferred (*)", "string", None),
             col("name_de", "Deutscher Name (heute)", "German name (current)", "string", None, True),
             col("name_en", "Englischer Name", "English name", "string", None, True),
             col("name_sci", "Wissenschaftlicher Name (heute)", "Scientific name (current)", "string", None, True),
             col("n_waters", "Zahl der Gewässer mit Angabe", "Number of water bodies with an entry", "integer", None, True),
         ],
         "rows": species, "source_refs": REFS},
    ],
    "charts": [],
    "keywords": {"de": ["Fische", "Fischerei", "Saale", "Elster", "Wiesenthal", "Teiche", "Forelle", "Lachs", "Karpfen", "Äsche", "Volksnamen"],
                 "en": ["fish", "fishing", "Saale", "Elster", "Wiesenthal", "ponds", "trout", "salmon", "carp", "grayling", "folk names"]},
    "related": ["fauna-artenzahlen-tiergruppen"],
    "generated_by": GEN,
    "date": DATE,
}
STAT = {"field": {"de": "status_de", "en": "status_en"}, "type": "nominal", "title": bi("Angabe", "Entry"), "legend": {"columns": 3},
        "scale": {"domain": [{"de": ST[k][1], "en": ST[k][2]} for k in ("present", "rare", "introduced", "former", "uncertain")]}}
WAT = {"field": {"de": "water_de", "en": "water_en"}, "type": "nominal", "title": None,
       "sort": [{"de": w[1], "en": w[2]} for w in WATER]}
ana["charts"] = [
    {"id": "c1", "dataset": "fish_cells",
     "title": bi("Welche Fische in welchem Gewässer? 34 Arten × 4 Gewässer", "Which fish in which water body? 34 species × 4 water bodies"),
     "caption": bi("Brückners Tabelle S. 87–88 als Matrix, Zellen nach seinem Wortlaut in fünf Stufen eingeteilt. Leere Zellen: keine Angabe (—). »eingesetzt«: eingesetzt oder aus den Teichen eingetreten. Ein Sternchen kennzeichnet besonders bevorzugte Arten.",
                   "Brückner's table pp. 87–88 as a matrix, cells classed in five levels following his wording. Empty cells: no entry (—). An asterisk marks especially preferred species."),
     "vegalite": {"height": 420, "transform": [{"filter": "datum.status_key != 'absent'"}], "mark": "rect",
                  "encoding": {
                      "y": {"field": "species_label", "type": "nominal", "sort": {"field": "species_no", "op": "min"}, "title": None, "axis": {"labelFontSize": 10, "labelLimit": 215}},
                      "x": {**WAT, "axis": {"labelAngle": 0, "orient": "top"}},
                      "color": STAT,
                      "tooltip": [{"field": "species_label", "title": bi("Art", "Species")},
                                  {"field": {"de": "water_de", "en": "water_en"}, "title": bi("Gewässer", "Water body")},
                                  {"field": "cell_text", "title": bi("Angabe im Druck", "Entry in print")},
                                  {"field": {"de": "status_de", "en": "status_en"}, "title": bi("Stufe", "Level")}]}}},
    {"id": "c2", "dataset": "fish_cells",
     "title": bi("Artenzahl je Gewässer", "Number of species per water body"),
     "caption": bi("Zahl der Arten mit Angabe, nach Stufe. Die Saale ist am artenreichsten, die Teiche sind mit nur sechs Arten am ärmsten.",
                   "Number of species with an entry, by level. The Saale is richest in species, the ponds are poorest with only six species."),
     "vegalite": {"height": 260, "transform": [{"filter": "datum.status_key != 'absent'"}], "mark": "bar",
                  "encoding": {
                      "x": {**WAT, "axis": {"labelAngle": 0}},
                      "y": {"aggregate": "count", "type": "quantitative", "title": bi("Arten", "Species")},
                      "color": STAT,
                      "order": {"field": "status_order", "type": "quantitative", "sort": "descending"},
                      "tooltip": [{"field": {"de": "water_de", "en": "water_en"}, "title": bi("Gewässer", "Water body")},
                                  {"field": {"de": "status_de", "en": "status_en"}, "title": bi("Stufe", "Level")},
                                  {"aggregate": "count", "title": bi("Arten", "Species")}]}}},
]
assert n_water["teiche"] == 6
write(ana)
