"""Analysis: find-spots of rare plants around Gera (pp. 76-77) and in the Lobenstein district (p. 81)."""
import re
from collections import Counter, defaultdict
from common import *
from flora_lists import unterland, oberland, corrected_sets

G = {"P": ("Blütenpflanzen", "Flowering plants"), "M": ("Moose", "Mosses and liverworts"),
     "F": ("Flechten", "Lichens"), "A": ("Algen", "Algae")}

# --- list 1: Gera district, p.76 b2 + p.77 b1 (name, group, printed locality phrase, [normalised localities])
GERA = [
    ("Bergwolverlei", "P", "bei Frankenthal", ["Frankenthal"]),
    ("Geranium sylvaticum", "P", "bei Tinz", ["Tinz"]),
    ("Matricaria discoidea", "P", "bei Köstritz", ["Köstritz"]),
    ("Ranunculus Lingua", "P", "bei Zwötzen", ["Zwötzen"]),
    ("Aconitum Lycoctonum", "P", "an der Cosse", ["Cosse"]),
    ("Teesdalia nudicaulis", "P", "bei Debschwitz", ["Debschwitz"]),
    ("Trifolium spadiceum", "P", "bei Dürrenebersdorf", ["Dürrenebersdorf"]),
    ("Coronilla varia", "P", "bei Langenberg", ["Langenberg"]),
    ("Vicia dumetorum", "P", "in der Kerbe", ["Kerbe"]),
    ("Vicia angustifolia", "P", "in der Kerbe", ["Kerbe"]),
    ("Peplis Portula", "P", "bei Ernsee", ["Ernsee"]),
    ("Scrophularia vernalis", "P", "im Park zu Köstritz", ["Köstritz"]),
    ("Teucrium Scordium", "P", "bei Dürrenebersdorf", ["Dürrenebersdorf"]),
    ("Anagallis coerulea", "P", "bei Gera", ["Gera"]),
    ("Amarantus Blitum", "P", "auf dem alten Markte", ["Alter Markt"]),
    ("Parietaria erecta", "P", "bei Pforten", ["Pforten"]),
    ("Orchis coriophora", "P", "bei Gera und Mühlsdorf", ["Gera", "Mühlsdorf"]),
    ("Ophrys muscifera", "P", "bei Osterstein", ["Osterstein"]),
    ("Cypripedium Calceolus", "P", "am Hainberg, bei Langenberg und Hartmannsdorf", ["Hainberg", "Langenberg", "Hartmannsdorf"]),
    ("Iris sibirica", "P", "bei Pforten", ["Pforten"]),
    ("Bruchia palustris", "M", "im Martinsgrund", ["Martinsgrund"]),
    ("Ephemerella pachycarpa", "M", "bei Frankenthal", ["Frankenthal"]),
    ("Orthotrichum pallens", "M", "bei Kaimberg", ["Kaimberg"]),
    ("Neckera pennata", "M", "bei Ernsee", ["Ernsee"]),
    ("Lecidea sanguinaria", "F", "hinter Pöppeln", ["Pöppeln"]),
    ("Fissidens incurvus", "M", "bei Windischenbernsdorf", ["Windischenbernsdorf"]),
    ("Hypnum sylvaticum", "M", "bei Ernsee", ["Ernsee"]),
    ("Hypnum ruscifolium", "M", "zwischen Saara und Hundhaupten", ["Saara/Hundhaupten"]),
    ("Hypnum populeum", "M", "am Hainberg", ["Hainberg"]),
    ("Hookeria lucens", "M", "in der Kerbe", ["Kerbe"]),
    ("Leskea", "M", "im Köstritzer Park", ["Köstritz"]),
    ("Mnium rostratum", "M", "bei Windischenbernsdorf", ["Windischenbernsdorf"]),
    ("Weisia crispula", "M", "bei Frankenthal", ["Frankenthal"]),
    ("Ephemerum patens", "M", "bei Zwötzen", ["Zwötzen"]),
    ("Phascum crispum", "M", "auf dem Zoitsberg", ["Zoitsberg"]),
    ("Ptilidium ciliare", "M", "bei Pöppeln", ["Pöppeln"]),
    ("Madotheca platyphylla", "M", "am Hainberg", ["Hainberg"]),
    ("Pellia epiphylla", "M", "in der Mooßschlucht", ["Mooßschlucht"]),
    ("Riccia fluitans", "M", "bei Zwötzen", ["Zwötzen"]),
    ("Cetraria glauca", "F", "hinter dem Martinsgrund", ["Martinsgrund"]),
    ("Lecidea parasema", "F", "in der Mooßschlucht", ["Mooßschlucht"]),
    ("Lecidea candida", "F", "bei Pforten", ["Pforten"]),
    ("Calycium disseminatum", "F", "bei Kraftsdorf", ["Kraftsdorf"]),
    ("Peltigera malacea", "F", "in der Mooßschlucht", ["Mooßschlucht"]),
    ("Sticta scrobiculata", "F", "in der Kerbe", ["Kerbe"]),
    ("Parmelia tiliacea", "F", "bei Pforten", ["Pforten"]),
    ("Collema teretiusculum", "F", "bei Pforten", ["Pforten"]),
    ("Urceolaria calcarea", "F", "am pfortner Berg", ["Pforten"]),
    ("Cliostomum corrugatum", "F", "bei Ernsee", ["Ernsee"]),
    ("Opegrapha herp. subocellata", "F", "bei Weißig", ["Weißig"]),
    ("Spiloma viridens", "F", "bei Ernsee", ["Ernsee"]),
    ("Lepra nigra", "F", "auf dem Hainberg", ["Hainberg"]),
    ("Conferva tenerrima", "A", "bei Bieblach", ["Bieblach"]),
    ("Myxonema tenue", "A", "im Martinsgrund", ["Martinsgrund"]),
    ("Myxonema dissiliens", "A", "bei Frankenthal", ["Frankenthal"]),
    ("Allogonium converfaceum", "A", "zwischen Köstritz und Caaschwitz", ["Köstritz/Caaschwitz"]),
    ("Chaetophora tuberculosa", "A", "bei Debschwitz", ["Debschwitz"]),
    ("Rivularia dura", "A", "bei Milbitz", ["Milbitz"]),
    ("Microcoleus leptodermus", "A", "bei Bieblach", ["Bieblach"]),
    ("Micrasterias angulosa", "A", "bei Dorna", ["Dorna"]),
    ("Micrasterias Napoleonis", "A", "bei Kraftsdorf", ["Kraftsdorf"]),
    ("Diatoma tenue", "A", "bei Windischenbernsdorf", ["Windischenbernsdorf"]),
    ("Fragilaria acuta", "A", "bei Bieblach", ["Bieblach"]),
    ("Eunotia Vergatus", "A", "bei Windischenbernsdorf", ["Windischenbernsdorf"]),
]
GERA_BLOCKS = {}
for nm, g, ph, locs in GERA:
    blk = None
    for lab, bid in (("76", "b2"), ("77", "b1")):
        t = re.sub(r"\s+", " ", text(lab, bid))
        i = t.find(nm)
        if i >= 0 and ph.split(",")[0] in t[i:i + 160]:
            blk = (lab, bid)
            break
    if nm == "Myxonema dissiliens":  # name at the end of p.76 b2, locality at the start of p.77 b1
        assert "Myxonema dissiliens bei" in re.sub(r"\s+", " ", text("76", "b2")) and text("77", "b1").startswith("Frankenthal")
        blk = ("77", "b1")
    assert blk, nm
    GERA_BLOCKS[nm] = blk

# --- list 2: Dürr, p.81 b1
t81 = text("81", "b1")
body = t81.split("an: ", 1)[1]
ents = re.findall(r"(?:^|, )((?:[A-Z][^()]*?)) \(([^()]*?)\)", body)
assert len(ents) == 46
LOCMAP = {
    "Heinrichstein": ["Heinrichstein"], "ebenda": None, "daselbst": None, "Ebersdorf": ["Ebersdorf"], "Saalthal": ["Saalthal"],
    "auf Wiesen bei Röttersdorf": ["Röttersdorf"], "Wurzbach": ["Wurzbach"],
    "Sormitzgrund und bei Heinrichstein": ["Sormitzgrund", "Heinrichstein"],
    "verbreitet, aber nur stellenweise": [], "auf Äckern bei Röttersdorf": ["Röttersdorf"],
    "zwischen Lobenstein und Ebersdorf": ["Lobenstein/Ebersdorf"], "Lobenstein": ["Lobenstein"],
    "Röttersdorf, Helmsgrün": ["Röttersdorf", "Helmsgrün"], "Wurzbach, Heinrichshütte": ["Wurzbach", "Heinrichshütte"],
    "Lobenstein im Raps *": ["Lobenstein"], "Heinersdorf, Oßla, Wurzbach": ["Heinersdorf", "Oßla", "Wurzbach"],
    "an Bächen bei Röttersdorf": ["Röttersdorf"], "Oßla, Heinersdorf": ["Oßla", "Heinersdorf"], "Unterlemnitz": ["Unterlemnitz"],
    "Weitisberga am Hainberg und bei Wurzbach": ["Weitisberga", "Wurzbach"], "Heinersdorf": ["Heinersdorf"],
    "Röttersdorf auf Wiesen": ["Röttersdorf"], "Tännich bei Lobenstein.": ["Tännich"],
}
LOB = []
prev = None
for raw, loc in ents:
    names = [raw]
    if raw.startswith("Rubus"):
        names = ["Rubus candicans", "Rubus sylvatica", "Rubus fuscoater", "Rubus vestitus"]
    else:
        w = raw.replace(",", " ").split()
        names = [w[0] + " " + w[1]]
    locs = LOCMAP[loc]
    if locs is None:
        locs = prev
    else:
        prev = locs
    for n in names:
        LOB.append((n, "P", loc, locs))
assert len(LOB) == 49, len(LOB)
for n, g, loc, locs in LOB:
    need(loc.rstrip("."), "81", "b1")

# --- cross-check against the exclusive lists
def norm(s):
    s = s.lower()
    s = re.sub(r"[^a-z ]", "", s)
    s = s.replace("y", "i").replace("ae", "e").replace("oe", "e").replace("th", "t").replace("rrh", "rh").replace("ll", "l").replace("ph", "f")
    return " ".join(s.split())


_ul, _ol = corrected_sets()  # lists after Brückner's own corrections (p. 830)
UL = {norm(n): n for n in _ul}
OL = {norm(n): n for n in _ol}
def where(name):
    k = norm(name)
    if k in UL:
        return "UL"
    if k in OL:
        return "OL"
    return None


rows = []
for lst, data, src in (("gera", GERA, None), ("lob", LOB, None)):
    for rec in data:
        nm, g, phrase, locs = rec
        if lst == "gera":
            pg, bk = GERA_BLOCKS[nm]
        else:
            pg, bk = "81", "b1"
        w = where(nm)
        if not locs:
            rows.append([lst, nm, G[g][0], G[g][1], None, phrase, w, pg, bk])
        for loc in locs or []:
            rows.append([lst, nm, G[g][0], G[g][1], loc, phrase, w, pg, bk])

gera_rows = [r for r in rows if r[0] == "gera"]
lob_rows = [r for r in rows if r[0] == "lob"]

LISTS = {"gera": ("Gera und Umgebung (S. 76–77)", "Gera and surroundings (pp. 76–77)"),
         "lob": ("Landschaft Lobenstein nach Dr. Dürr (S. 81)", "Lobenstein district after Dr Dürr (p. 81)")}
EXCL = {"UL": ("In der Liste »nur Unterland«", "In the “Unterland only” list"), "OL": ("In der Liste »nur Oberland«", "In the “Oberland only” list")}
tot = Counter((r[0], r[4]) for r in rows if r[4])
out_rows = []
for lst, nm, gde, gen, loc, phrase, w, pg, bk in rows:
    out_rows.append([lst, LISTS[lst][0], LISTS[lst][1], nm, gde, gen, loc, tot[(lst, loc)] if loc else None, phrase,
                     EXCL[w][0] if w else None, EXCL[w][1] if w else None, pg, bk])

gera_rows = [r for r in rows if r[0] == "gera"]
lob_rows = [r for r in rows if r[0] == "lob"]
n_g_rec, n_g_sp, n_g_loc = len(gera_rows), len({r[1] for r in gera_rows}), len({r[4] for r in gera_rows})
n_l_rec, n_l_sp, n_l_loc = len(lob_rows), len({r[1] for r in lob_rows}), len({r[4] for r in lob_rows if r[4]})
g_sp = {r[1]: r for r in gera_rows}
l_sp = {r[1]: r for r in lob_rows}
g_phan = [n for n, r in g_sp.items() if r[2] == "Blütenpflanzen"]
g_ul = [n for n in g_phan if g_sp[n][6] == "UL"]
l_ol = [n for n in l_sp if l_sp[n][6] == "OL"]
cg = Counter(r[4] for r in gera_rows)
cl = Counter(r[4] for r in lob_rows if r[4])
top5 = sum(v for _, v in cg.most_common(6))
hein = cl["Heinrichstein"]
THR_G, THR_L = 3, 2
n_g_top = len([k for k, v in cg.items() if v >= THR_G])
n_l_top = len([k for k, v in cl.items() if v >= THR_L])
print(n_g_rec, n_g_sp, n_g_loc, n_l_rec, n_l_sp, n_l_loc, top5, hein, len(g_phan), len(g_ul), len(l_ol), n_g_top, n_l_top)
pc = lambda a, b: 100 * a / b
top_g = ", ".join(f"{k} ({v})" for k, v in cg.most_common(6))
ngrp = lambda g: len([1 for r in g_sp.values() if r[2] == g])
cl2 = cl.most_common(3)

REFS = [{"page": "76", "block": "b2"}, {"page": "77", "block": "b1"}, {"page": "81", "block": "b1"}]
ana = {
    "id": "flora-seltene-pflanzen-fundorte",
    "title": bi("Fundorte seltener Pflanzen: Gera und Lobenstein", "Find-spots of rare plants: Gera and Lobenstein"),
    "category": "flora",
    "section": "t1-1-8",
    "sources": REFS + [{"page": "71", "block": "fn2"}, {"page": "81", "block": "fn1"}, {"page": "72", "block": "b5"}, {"page": "73", "block": "b1"}, {"page": "73", "block": "b3"}, {"page": "74", "block": "b1"}, {"page": "830", "block": "b8"}, {"page": "830", "block": "b9"}],
    "summary": bi(
        f"Brückner nennt für die Umgebung von Gera {n_g_sp} seltene Pflanzen (Blütenpflanzen, Moose, Flechten, Algen) mit ihren Fundorten und gibt für die Landschaft Lobenstein ein Verzeichnis von Dr. Dürr mit {n_l_sp} Arten wieder. Die Fundortangaben wurden zu {n_g_rec + n_l_rec} Einzelnachweisen aufgelöst und nach Orten ausgezählt; zugleich wurde geprüft, ob die Arten in den Listen der nur im Unter- oder nur im Oberland vorkommenden Pflanzen stehen.",
        f"For the surroundings of Gera Brückner names {n_g_sp} rare plants (flowering plants, mosses, lichens, algae) with their find-spots, and for the Lobenstein district he reproduces a list by Dr Dürr with {n_l_sp} species. The find-spot statements were resolved into {n_g_rec + n_l_rec} individual records and counted by place; it was also checked whether the species appear in the lists of plants occurring only in the Unterland or only in the Oberland."),
    "method": bi(
        "Aus dem Fließtext auf S. 76–77 (Gera) und S. 81 (Lobenstein) wurde jede Angabe »Art – Fundort« als eigener Datensatz erfasst; Angaben mit mehreren Orten (»bei Gera und Mühlsdorf«) ergeben mehrere Datensätze, »ebenda« und »daselbst« wurden zum vorher genannten Ort aufgelöst. Die Fundorte wurden vereinheitlicht (»hinter dem Martinsgrund« und »im Martinsgrund« = Martinsgrund; »am pfortner Berg« = Pforten); Ortsnamen sind nicht georeferenziert. Die Gruppen (Blütenpflanzen, Moose einschließlich Lebermoose, Flechten, Algen) beruhen auf der Gattung und sind redaktionell. Der Abgleich mit den Exklusivlisten (S. 72–74) verwendet die Listen nach Brückners Berichtigungen (S. 830) und vergleicht die Namen nach vereinheitlichter Schreibweise (z. B. sylvaticum/silvaticum, Amarantus/Amaranthus). Die Rubus-Sammelangabe (vier Arten) ist in vier Arten aufgelöst; die Angabe zu Digitalis grandiflora (»verbreitet, aber nur stellenweise«) hat keinen Ort und fehlt in den Ortszählungen.",
        "Every statement “species – find-spot” in the running text on pp. 76–77 (Gera) and p. 81 (Lobenstein) was captured as a separate record; statements with several places (“near Gera and Mühlsdorf”) give several records, and “ebenda”/“daselbst” (“the same place”) were resolved to the place named before. The find-spots were standardised (“hinter dem Martinsgrund” and “im Martinsgrund” = Martinsgrund; “am pfortner Berg” = Pforten); place names are not georeferenced. The groups (flowering plants, mosses including liverworts, lichens, algae) rest on the genus and are editorial. The comparison with the exclusive lists (pp. 72–74) uses the lists after Brückner's corrections (p. 830) and matches names after standardising the spelling (e.g. sylvaticum/silvaticum, Amarantus/Amaranthus). The collective Rubus entry (four species) was resolved into four species; the entry for Digitalis grandiflora (“widespread, but only locally”) has no place and is missing from the place counts."),
    "findings": [
        bi(f"Um Gera nennt Brückner {n_g_sp} Arten an {n_g_loc} Fundorten: {len(g_phan)} Blütenpflanzen, {ngrp('Moose')} Moose, {ngrp('Flechten')} Flechten und {ngrp('Algen')} Algen. Die meisten Nachweise haben {top_g}; auf diese sechs Orte entfallen {top5} von {n_g_rec} Datensätzen ({de(pc(top5, n_g_rec), 0)} %).",
           f"Around Gera Brückner names {n_g_sp} species at {n_g_loc} find-spots: {len(g_phan)} flowering plants, {ngrp('Moose')} mosses, {ngrp('Flechten')} lichens and {ngrp('Algen')} algae. The most records come from {top_g}; these six places account for {top5} of {n_g_rec} records ({en(pc(top5, n_g_rec), 0)} %)."),
        bi(f"In Dr. Dürrs Verzeichnis für die Landschaft Lobenstein entfallen {hein} von {n_l_rec} Datensätzen ({de(pc(hein, n_l_rec), 0)} %) auf den Heinrichstein; danach folgen {cl2[1][0]} ({cl2[1][1]}) und {cl2[2][0]} ({cl2[2][1]}).",
           f"In Dr Dürr's list for the Lobenstein district {hein} of {n_l_rec} records ({en(pc(hein, n_l_rec), 0)} %) fall on the Heinrichstein, followed by {cl2[1][0]} ({cl2[1][1]}) and {cl2[2][0]} ({cl2[2][1]})."),
        bi(f"Die Fundortangaben stützen die Exklusivlisten weitgehend: {len(g_ul)} der {len(g_phan)} Blütenpflanzen aus dem Gebiet um Gera stehen in der Liste der nur im Unterland vorkommenden Arten, {len(l_ol)} der {n_l_sp} Lobensteiner Arten in der Oberlandliste; keine Art aus dem einen Gebiet steht in der Liste des anderen, mit einer Ausnahme: Geranium sylvaticum steht in der Oberlandliste, wird aber auch »bei Tinz« genannt.",
           f"The find-spots largely support the exclusive lists: {len(g_ul)} of the {len(g_phan)} flowering plants from the Gera area are in the list of species found only in the Unterland, {len(l_ol)} of the {n_l_sp} Lobenstein species in the Oberland list; no species from one area is in the other's list, with one exception: Geranium sylvaticum is in the Oberland list but is also named “near Tinz”."),
    ],
    "caveats": [
        bi("Die Häufung von Nachweisen an einzelnen Orten spiegelt wohl auch wider, wo gesammelt wurde: Brückner nennt für den geraer Strich Dr. Robert Schmidt, Otto Müller und Chr. Seydel (S. 71), das Lobensteiner Verzeichnis stammt von einem einzelnen Gewährsmann. Die Zahlen sind kein Maß der Artenvielfalt der Orte.",
           "The accumulation of records at single places probably also reflects where botanists collected: for the Gera area Brückner names Dr Robert Schmidt, Otto Müller and Chr. Seydel (p. 71), and the Lobenstein list comes from a single informant. The figures are not a measure of the species richness of the places."),
        bi("Dass Tinz im Unterland liegt, ergibt sich nur aus dem Zusammenhang (S. 76 und S. 85 in der Beschreibung des Unterlandes); der Widerspruch bei Geranium sylvaticum bleibt ungeklärt. Möglich ist ein Versehen in Liste oder Fundmeldung. Die Schreibung bei Brückner ist uneinheitlich (Geranium silvaticum S. 74, sylvaticum S. 76 und 81).",
           "That Tinz lies in the Unterland follows only from the context (pp. 76 and 85, in the description of the Unterland); the contradiction for Geranium sylvaticum remains unresolved. A slip in the list or in the record is possible. Brückner's spelling is inconsistent (Geranium silvaticum p. 74, sylvaticum pp. 76 and 81)."),
        bi("Malva moschata (Lobenstein) trägt in Brückners Anmerkung den Zusatz »wohl verwildert«.", "Malva moschata (Lobenstein) carries Brückner's note “probably escaped from cultivation”."),
    ],
    "datasets": [
        {"name": "records",
         "title": bi("Einzelnachweise seltener Pflanzen (S. 76–77, 81)", "Individual records of rare plants (pp. 76–77, 81)"),
         "columns": [
             col("list_key", "Liste", "List", "string", None, True),
             col("list_de", "Liste (DE)", "List (DE)", "string", None, True),
             col("list_en", "Liste (EN)", "List (EN)", "string", None, True),
             col("name", "Art bei Brückner", "Species in Brückner", "string", None),
             col("group_de", "Gruppe", "Group", "string", None, True, "redaktionell nach der Gattung"),
             col("group_en", "Gruppe (EN)", "Group (EN)", "string", None, True),
             col("locality", "Fundort (vereinheitlicht)", "Find-spot (standardised)", "string", None, True),
             col("locality_total", "Nachweise am Ort in dieser Liste", "Records at the place in this list", "integer", "Nachweise", True),
             col("locality_printed", "Fundortangabe im Druck", "Find-spot as printed", "string", None),
             col("exclusive_de", "In den Exklusivlisten (S. 72–74)", "In the exclusive lists (pp. 72–74)", "string", None, True),
             col("exclusive_en", "In den Exklusivlisten (EN)", "In the exclusive lists (EN)", "string", None, True),
             col("page", "Seite", "Page", "string", None),
             col("block", "Block", "Block", "string", None),
         ],
         "rows": out_rows, "source_refs": REFS},
    ],
    "charts": [],
    "keywords": {"de": ["Flora", "Seltenheiten", "Fundorte", "Gera", "Lobenstein", "Heinrichstein", "Moose", "Flechten", "Orchideen", "Botanik"],
                 "en": ["flora", "rarities", "find-spots", "Gera", "Lobenstein", "Heinrichstein", "mosses", "lichens", "orchids", "botany"]},
    "related": ["flora-exklusivarten-unterland-oberland", "flora-artenzahlen-phanerogamen-kryptogamen"],
    "generated_by": GEN,
    "date": DATE,
}
GRP = {"field": {"de": "group_de", "en": "group_en"}, "type": "nominal", "title": bi("Gruppe", "Group"),
       "scale": {"domain": [{"de": G[k][0], "en": G[k][1]} for k in ("P", "M", "F", "A")]}}


def chart(cid, lst, thr, title, caption, h):
    return {"id": cid, "dataset": "records", "title": title, "caption": caption,
            "vegalite": {"height": h, "transform": [{"filter": f"datum.list_key == '{lst}' && datum.locality_total >= {thr}"}],
                         "mark": "bar",
                         "encoding": {
                             "y": {"field": "locality", "type": "nominal", "sort": "-x", "title": None},
                             "x": {"aggregate": "count", "type": "quantitative", "title": bi("Nachweise seltener Arten", "Records of rare species"), "axis": {"tickMinStep": 1}},
                             "color": GRP,
                             "tooltip": [{"field": "locality", "title": bi("Fundort", "Find-spot")},
                                         {"field": {"de": "group_de", "en": "group_en"}, "title": bi("Gruppe", "Group")},
                                         {"aggregate": "count", "title": bi("Nachweise", "Records")}]}}}


ana["charts"] = [
    chart("c1", "gera", THR_G, bi("Seltene Pflanzen bei Gera: Fundorte mit mindestens drei Nachweisen", "Rare plants near Gera: find-spots with at least three records"),
          bi(f"{n_g_top} von {n_g_loc} Fundorten; Nachweise nach Pflanzengruppe (S. 76–77).", f"{n_g_top} of {n_g_loc} find-spots; records by plant group (pp. 76–77)."), 330),
    chart("c2", "lob", THR_L, bi("Seltene Pflanzen in der Landschaft Lobenstein: Fundorte mit mindestens zwei Nachweisen", "Rare plants in the Lobenstein district: find-spots with at least two records"),
          bi(f"{n_l_top} von {n_l_loc} Fundorten; nach dem Verzeichnis von Dr. Dürr (S. 81), alle Blütenpflanzen.", f"{n_l_top} of {n_l_loc} find-spots; after the list by Dr Dürr (p. 81), all flowering plants."), 280),
]
write(ana)
