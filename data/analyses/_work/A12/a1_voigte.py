"""Analysis: the Heinrichs of the Voigt lines Weida, Gera, Plauen and Reuss-Plauen (Tab. I-V, pp. 331-372)."""
import re, statistics
from common import *

LINES = {
    "weida": ("Weida", "Weida"),
    "gera": ("Gera", "Gera"),
    "plauen": ("Plauen", "Plauen"),
    "reuss": ("Reuß-Plauen", "Reuss-Plauen"),
}
ROLES = {"ruler": ("Landesherr", "ruler"), "cleric": ("Geistlicher/Ordensritter", "cleric/knight of the Order"), "other": ("ohne Herrschaft", "no lordship")}

# (line, tab, (page, block, row, col) | (page, block) for paragraphs, name, first, last, end_qual, date_text, note, role, kind, from_facsimile)
# kind: att = dates as printed for the period of attestation/reign; life = geb.-+ ; end_qual: x exact, c circa, n nach, v vor
E = []
def add(line, tab, src, name, first, last, qual, dtext, note, role, kind="att", fac=False):
    E.append(dict(line=line, tab=tab, src=src, name=name, first=first, last=last, qual=qual, dtext=dtext, note=note, role=role, kind=kind, fac=fac))

# --- Tab. I (p. 331): the undivided house Weida
add("weida","I",("331","b5",1,2),"Heinrich v. Weida der Fromme (nach den Chronisten)",None,1100,"c","† c. 1100","nur nach den Chronisten","ruler")
add("weida","I",("331","b5",2,2),"Heinrich v. Weida, erster Beurkundeter",1143,1143,"x","1143","","ruler")
add("weida","I",("331","b5",3,1),"Heinrich v. Weida der Reiche",1188,1209,"v","1188 — † vor 1209","Gem. Berchta","ruler")
add("weida","I",("331","b5",4,1),"Heinrich d. ä., Voigt von Weida",1209,1224,"n","1209 — † nach 1224","vor 1219 verheiratet, dann Ordensritter","ruler")
add("weida","I",("331","b5",4,2),"Heinrich d. m., von Gottes Gnaden, Voigt von Weida",1209,1249,"x","1209—1249","seit 1224 d. ä.; 1238 Ordensritter (Landmeister und Stellvertreter)","ruler")
add("weida","I",("331","b5",4,3),"Heinrich d. j., Voigt von Weida",1209,1240,"n","1209 — † nach 1240","von 1240 an Voigt v. Greiz","ruler")
add("weida","I",("331","b5",5,1),"Heinrich von Weida",1236,1246,"x","1236. 1237. 1246.","","ruler")
add("weida","I",("331","b6",1,4),"Heinrich, Mönch, dann Domherr zu Magdeburg",1248,1267,"x","1248. 1267.","","cleric")
add("weida","I",("331","b6",1,5),"Heinrich, Prior z. Erfurt",1256,1259,"x","1256. 1259.","","cleric")
# --- Tab. II (p. 341): line Weida
add("weida","II",("341","b2"),"Heinrich, Voigt von Weida",1236,1275,"c","1236 — c. 1275","Reichslandrichter in Eger 1256; Gründer der Linie","ruler")
add("weida","II",("341","b3",1,1),"Heinrich d. ä.",1276,1316,"c","1276 — c. 1316","Gem. Hedwig","ruler")
add("weida","II",("341","b3",1,3),"Heinrich",1294,1294,"x","1294 Probst zu Jagow","Probst zu Jagow","cleric")
add("weida","II",("341","b3",1,4),"Heinrich d. j.",1277,1293,"v","1277 — † vor Mitte 1293","","ruler")
add("weida","II",("341","b3",2,1),"Heinrich d. ä.",1295,1364,"c","1295 — c. 1364","seit 1323 Landvoigt zu Eger","ruler")
add("weida","II",("341","b3",2,2),"Heinrich d. j.",1295,1348,"c","1295 — † um 1348","","ruler")
add("weida","II",("341","b3",2,3),"Heinrich",1298,1333,"n","1298 Mönch, † nach 1333","Mönch","cleric")
add("weida","II",("341","b3",2,5),"Heinrich der Graf",1293,1335,"n","1293 — † nach 1335","Gem. Hedwig (v. Lobdaburg-Arnshaugk)","ruler")
add("weida","II",("341","b3",3,1),"Heinrich",None,1349,"n","† nach 10. Aug. 1349","Mönch","cleric")
add("weida","II",("341","b3",3,2),"Heinrich der Ritter",1337,1377,"n","1337 — nach 1377","","ruler")
add("weida","II",("341","b3",3,3),"Heinrich der Rothe",1377,1388,"c","1377 — c. 1388","Gem. Ilse von Gera","ruler")
add("weida","II",("341","b3",3,6),"Heinrich d. j.",1341,1354,"v","1341 Landvogt zu Eger. † vor Decbr. 1354","Landvogt zu Eger","ruler")
add("weida","II",("341","b3",4,1),"Heinrich",1389,1400,"v","1389. † vor 17. Decbr. 1400","","ruler")
add("weida","II",("341","b3",5,1),"Heinrich d. ä.",1402,1435,"n","1402 — † nach 1435","","ruler")
add("weida","II",("341","b3",5,2),"Heinrich d. m.",1402,1411,"n","1402 — † nach 1411","Gem. Anna v. Schönburg","ruler")
add("weida","II",("341","b3",5,3),"Heinrich d. j.",1402,1435,"n","1402 — † nach 1435","","ruler")
add("weida","II",("341","b3",6,1),"Heinrich",1438,1454,"x","1438 Herr von Weida zu Hauenstein, 1454 zu Wildenfels","Herr zu Hauenstein, dann zu Wildenfels","ruler")
add("weida","II",("341","b3",6,2),"Heinrich",1447,1447,"x","1447 Herr von Weida zu Hauenstein","Herr zu Hauenstein","ruler")
add("weida","II",("341","b3",7,1),"Heinrich d. ä.",1485,1519,"n","1485 — † nach 1519","Herr v. Weida und Wildenfels, brandenburger Rath","ruler")
add("weida","II",("341","b3",7,2),"Heinrich d. m.",1504,1510,"v","1504. † vor 1510","Herr v. Weida und Wildenfels","ruler")
add("weida","II",("341","b3",7,3),"Heinrich d. j.",None,1510,"x","† 1510","Herr v. Weida und Wildenfels","ruler")
add("weida","II",("341","b3",8,1),"Heinrich",None,1535,"c","† c. 1535","Herr von Weida und Wildenfels; letzter männlicher Erbe","ruler")
# --- Tab. III (p. 352): line Gera
add("gera","III",("352","b2"),"Heinrich der Mehrer",1244,1279,"v","1244 — † vor Ende August 1279","Voigt von Gera; Gem. Lukard von Lobdaburg-Arnshaugk (Transkription: »der Ältere«)","ruler")
add("gera","III",("352","b3",1,1),"Heinrich d. ä., der Hochberühmte",1275,1306,"x","1275 — Ende 1306","Gem. Irmgard v. Weida","ruler")
add("gera","III",("352","b3",1,2),"Heinrich, Deutschherr",1275,1326,"n","1275 — † nach Aug. 1326","Deutschherr","cleric")
add("gera","III",("352","b3",1,4),"Heinrich, Mönch zu Plauen",None,1333,"n","† nach 1333","Mönch zu Plauen","cleric")
add("gera","III",("352","b3",1,5),"Heinrich d. j.",1275,1310,"v","1275 — † zwischen 1303 und 1310","Voigt v. Weißenfels","ruler")
add("gera","III",("352","b3",2,1),"Heinrich d. ä., der Große",1307,1345,"c","1307 — c. 1345 († nach dem Mai 1344)","Gem. Sophie v. Lobdaburg-Bergau","ruler")
add("gera","III",("352","b3",2,5),"Heinrich d. j., der Worthalter",1310,1376,"x","1310 — 1376 (8. Decbr.)","Gem. Mechtild v. Käfernburg (Transkription: »der Wohlbedachte«)","ruler")
add("gera","III",("352","b3",2,6),"Heinrich",1348,1348,"x","1348 Domherr zu Magdeburg","Domherr zu Magdeburg","cleric")
add("gera","III",("352","b3",3,7),"Heinrich d. Dispensirte",1351,1419,"x","1351 — 1419 Ende od. 1520 Anfang","Druck: »1520« für 1420 (S. 346)","ruler")
add("gera","III",("352","b3",3,8),"Heinrich",1363,1363,"x","1363. † kurz darauf","","other")
add("gera","III",("352","b3",4,2),"Heinrich",None,1414,"x","† Ende 1414","ältester Sohn des Dispensirten, Gem. Margarethe v. Wertheim","other")
add("gera","III",("352","b3",4,1),"Heinrich",1415,1422,"x","1415—1422","Enkel des Dispensirten","other")
add("gera","III",("352","b3",4,2),"Heinrich",1415,1422,"x","1415—1422","Enkel des Dispensirten","other")
add("gera","III",("352","b3",4,2),"Heinrich d. ä.",1404,1439,"v","geb. 1404, † vor April 1439","Herr v. Burgk 1426","ruler","life")
add("gera","III",("352","b3",4,3),"Heinrich d. m.",1406,1481,"c","geb. 1406, † c. 1481","Herr von Lobenstein 1426","ruler","life")
add("gera","III",("352","b3",4,4),"Heinrich d. j.",1415,1456,"v","geb. 1415, † vor 1456","Herr zu Gera u. Lobenstein 1441 (der Unglückliche)","ruler","life")
add("gera","III",("352","b3",4,3),"Heinrich",1446,1446,"x","1446 Domherr zu Köln","Domherr zu Köln (Zelle fehlt in der Transkription)","cleric","att",True)
add("gera","III",("352","b3",4,3),"Heinrich d. ä.",1474,1488,"c","1474 — † c. 1488","Herr v. Gera u. Rochsburg (Zelle fehlt in der Transkription)","ruler","att",True)
add("gera","III",("352","b3",4,2),"Heinrich d. m.",1478,1500,"x","1478 — † 1500","Herr von Schleiz und Reichenfels; Gem. Hedwig v. Mansfeld-Heldrungen","ruler")
add("gera","III",("352","b3",4,3),"Heinrich d. j., der Hinkende",1476,1498,"c","1476 — † c. 1498","Herr zu Lobenstein, Saalburg und Burgk (Transkription: »der Fintende« bei d. m.)","ruler","att",True)
add("gera","III",("352","b3",4,4),"Heinrich",1495,1508,"x","1495. 1508.","Druck ohne »†«; Transkription: »† vor 1508«","other","att",True)
add("gera","III",("352","b3",4,1),"Heinrich d. ä.",1502,1538,"x","1502 — † 1538","Gem. 1) Margarethe von Mynicz, 2) Anna von Beichlingen","ruler")
add("gera","III",("352","b3",4,2),"Heinrich d. j., der Beharrliche",1502,1550,"x","1502 — † 7. Aug. 1550","Gem. 1) Ludmilla von Lobkowiz, 2) Margaretha v. Schwarzburg-Leutenberg","ruler")
# --- Tab. IV (p. 364): line Plauen (older line) and Reuss-Plauen
add("plauen","IV",("364","b2"),"Heinrich der Ruthene (Ruzze, Reuß)",1244,1303,"x","1244 — † 1303","von Gottes Vollmacht; Gem. Kunigunde v. Eberstein","ruler")
add("plauen","IV",("364","b3",1,1),"Heinrich der Böhme oder der Lange",1275,1302,"x","1275—1302","Gem. Katharina v. Riesenburg","ruler")
add("plauen","IV",("364","b3",1,2),"Heinrich",1265,1300,"v","1265 Prior und Comthur des deutschen Ordens in Plauen, † vor 1300","Prior und Comthur in Plauen","cleric")
add("reuss","IV",("364","b3",1,5),"Heinrich der Ruzze",1276,1296,"v","1276 — † vor 20. März 1296","Gem. unbekannt","ruler")
add("plauen","IV",("364","b3",2,1),"Heinrich der Lange",1290,1346,"c","1290 — c. 1346","Herr zu Plauen; Gründer der älteren Linie","ruler")
add("plauen","IV",("364","b3",2,2),"Heinrich",1332,1332,"x","1332 Mönch im Kl. Buch","Mönch im Kloster Buch","cleric")
add("reuss","IV",("364","b3",2,3),"Heinrich Reuß gen. Erik",1290,1349,"x","1290—1349","Herr zu Greiz; Gründer der jüngeren Linie","ruler")
add("plauen","IV",("364","b3",3,1),"Heinrich d. ä., der Lange",1306,1373,"x","1306—1373","Gem. Sophie v. Weida","ruler")
add("plauen","IV",("364","b3",3,2),"Heinrich",1333,1333,"x","1333 Domherr zu Magdeburg","Domherr zu Magdeburg","cleric")
add("plauen","IV",("364","b3",3,3),"Heinrich",1336,1336,"x","1336 Ordensritter","Ordensritter, Comthur zu Reichenbach","cleric")
add("plauen","IV",("364","b3",3,4),"Heinrich d. j., der Lange",1306,1352,"x","1306—1352","Herr zu Mühltroff","ruler")
add("plauen","IV",("364","b3",4,1),"Heinrich d. ä.",1373,1389,"x","1373 — Ende 1389","Herr zu Urbach (Auerbach)","ruler")
add("plauen","IV",("364","b3",4,2),"Heinrich",None,1363,"n","† nach August 1363","Mönch zu Pegau","cleric")
add("plauen","IV",("364","b3",5,1),"Heinrich I.",1389,1429,"x","1389—1429","als Burggraf seit 1426","ruler")
add("plauen","IV",("364","b3",5,2),"Heinrich",1389,1429,"x","1389—1429","Hochmeister in Preußen 1410","cleric")
add("plauen","IV",("364","b3",5,3),"Heinrich",1410,1413,"x","1410—1413","Comthur zu Danzig","cleric")
add("plauen","IV",("364","b3",6,1),"Heinrich II.",1429,1446,"x","1429—1446","Burggraf","ruler")
add("plauen","IV",("364","b3",7,1),"Heinrich III.",1446,1482,"n","1446 — † nach 1482","Burggraf","ruler")
add("plauen","IV",("364","b3",8,1),"Heinrich IV.",1482,1520,"x","1482—1520","Burggraf; Gem. Barbara v. Anhalt","ruler")
add("plauen","IV",("364","b3",9,1),"Heinrich V.",1508,1554,"x","geb. 1508, † 1554","Burggraf","ruler","life")
add("plauen","IV",("364","b3",10,1),"Heinrich VI.",1533,1568,"x","geb. 1533, † 1568","Burggraf","ruler","life")
add("plauen","IV",("364","b3",10,2),"Heinrich VII.",1536,1572,"x","geb. 1536, † 1572","Burggraf; letzter seines Hauses","ruler","life")
add("plauen","IV",("364","b3",11,1),"Heinrich",1557,1557,"x","geb. und † 16. März 1557","","other","life")
# --- Tab. V (p. 372): Reuss-Plauen (younger line) down to 1578
add("reuss","V",("372","b2",1,1),"Heinrich der Strenge",1327,1359,"x","1327-1359","Gem. Anna v. Weida","ruler")
add("reuss","V",("372","b2",1,2),"Heinrich",1326,1338,"x","1326-1338","Ordensritter, Großcomthur","cleric")
add("reuss","V",("372","b2",2,1),"Heinrich d. ä.",1359,1394,"v","1359 - † vor 1394","Herr zu Greiz","ruler")
add("reuss","V",("372","b2",2,2),"Heinrich d. m.",1359,1372,"x","1359-1372","Herr zu Ronneburg","ruler")
add("reuss","V",("372","b2",2,3),"Heinrich d. j.",1364,1407,"n","1364 - † nach 1407","Herr zu Ronneburg","ruler")
add("reuss","V",("372","b2",3,1),"Heinrich d. ä.",1384,1413,"n","1384 - † nach 1413","Gem. Gaudencia v. Lobdaburg-Elsterberg","ruler")
add("reuss","V",("372","b2",3,2),"Heinrich d. j.",1384,1429,"x","1384 - † 1429","","ruler")
add("reuss","V",("372","b2",4,1),"Heinrich d. j. (der Alte von Greiz)",1413,1449,"n","1413 - † nach 1449","Der Alte von Greiz","ruler")
add("reuss","V",("372","b2",4,2),"Heinrich",1430,1445,"x","1430-1445","Deutschherr, Großcomthur, oberster Spittler","cleric")
add("reuss","V",("372","b2",4,4),"Heinrich d. ä.",1429,1475,"c","1429 - † c. 1475","Gem. Magdalena v. Schwarzenberg","ruler")
add("reuss","V",("372","b2",4,7),"Heinrich",1415,1470,"x","geb. 1415, † 1470","Deutschherr, zuletzt Hochmeister","cleric","life")
add("reuss","V",("372","b2",4,8),"Heinrich d. j.",1429,1462,"x","1429-1462","kursächs. Rath","ruler")
add("reuss","V",("372","b2",5,1),"Heinrich d. ä.",1476,1502,"x","1476-1502","Herr zu Greiz","ruler")
add("reuss","V",("372","b2",5,2),"Heinrich",1462,1530,"x","geb. 1462, † 1530","Domherr zu Mainz","cleric","life")
add("reuss","V",("372","b2",5,3),"Heinrich d. m.",1476,1539,"x","1476-1539","Herr zu Kranichfeld","ruler")
add("reuss","V",("372","b2",5,4),"Heinrich",None,1526,"n","† nach 1526","Deutschherr","cleric")
add("reuss","V",("372","b2",5,8),"Heinrich d. j. (der Friedsame)",1476,1535,"x","1476-1535","Herr zu Greiz u. seit 1529 auch Herr zu Kranichfeld","ruler")
add("reuss","V",("372","b2",5,10),"Heinrich",1506,1506,"x","Domherr zu Köln 1506","Domherr zu Köln","cleric")
add("reuss","V",("372","b2",7,1),"Heinrich d. ä.",1506,1572,"x","geb. 1506, † 1572","Herr zu Untergreiz; Stifter der älteren Linie Reuß","ruler","life")
add("reuss","V",("372","b2",7,8),"Heinrich d. m.",1525,1578,"x","geb. 1525, † 1578","Herr zu Obergreiz; Stifter der mittleren Linie","ruler","life")
add("reuss","V",("372","b2",7,9),"Heinrich d. j.",1530,1572,"x","geb. 1530, † 1572","Herr v. Gera; Stifter der jüngeren Linie","ruler","life")


def norm(s):
    return re.sub(r"\s+", "", re.sub(r"[—–]", "-", s.replace("*", ""))).lower()


def src_text(src):
    pg, b = src[0], src[1]
    if len(src) == 2:
        return block_text(pg, b)
    return cell(pg, b, src[2], src[3])


# verification against the transcription
bad = []
for e in E:
    if e["fac"]:
        continue
    t = norm(src_text(e["src"]))
    if norm(e["dtext"]) not in t:
        bad.append((e["tab"], e["src"], e["dtext"]))
    for y in (e["first"], e["last"]):
        if y is not None and str(y) not in t:
            bad.append((e["tab"], e["src"], "year", y))
if bad:
    for b_ in bad:
        print("MISSING", b_)
    raise SystemExit(1)


def short_dates(e):
    f, l = e["first"], e["last"]
    if f is None:
        return f"† {l}"
    if f == l:
        return f"{f}"
    return f"{f}–{l}"


SHORT = [(" (nach den Chronisten)", ""), ("Heinrich v. Weida, erster Beurkundeter", "Heinrich v. Weida (Beurkundeter)"),
         (", Voigt von Weida", ", Voigt"), ("von Gottes Gnaden, Voigt", "v. Gottes Gnaden"), (" (Ruzze, Reuß)", ""),
         ("Heinrich der Böhme oder der Lange", "Heinrich der Böhme"), (" (der Alte von Greiz)", ", Alte von Greiz"), (" (der Friedsame)", ", Friedsame")]
rows = []
for i, e in enumerate(E, 1):
    f, l = e["first"], e["last"]
    bs = f if f is not None else l
    be = l if l is not None else f
    e["bar_start"], e["bar_end"] = bs, be
    e["sortkey"] = bs * 100 + (i % 100)
    nm = e["name"]
    for a_, b_ in SHORT:
        nm = nm.replace(a_, b_)
    nm = nm.replace(", der ", ", ")
    lab = f"{nm} ({short_dates(e)})"
    # make labels unique within the dataset
    e["label"] = lab
labels = [e["label"] for e in E]
seen = {}
for e in E:
    n = seen.get((e["line"], e["label"]), 0)
    seen[(e["line"], e["label"])] = n + 1
    if n:
        e["label"] += " " + "′" * n
    # a name occurring in two lines with equal label stays distinct by line in the chart filters

assert len({(e["line"], e["label"]) for e in E}) == len(E)

for i, e in enumerate(E, 1):
    rows.append([i, e["line"], LINES[e["line"]][0], LINES[e["line"]][1], e["tab"], e["name"], e["note"] or "", e["role"],
                 ROLES[e["role"]][0], ROLES[e["role"]][1], e["kind"], e["first"], e["last"], e["qual"], e["dtext"],
                 e["bar_start"], e["bar_end"], e["sortkey"], e["label"], e["src"][0], e["src"][1], "ja" if e["fac"] else ""])

# --- statistics for the findings
rulers = [e for e in E if e["role"] == "ruler"]
byline = {k: [e for e in E if e["line"] == k] for k in LINES}
rcount = {k: sum(1 for e in v if e["role"] == "ruler") for k, v in byline.items()}
ccount = {k: sum(1 for e in v if e["role"] == "cleric") for k, v in byline.items()}
ocount = {k: sum(1 for e in v if e["role"] == "other") for k, v in byline.items()}
nE = len(E)
spans = [(e["bar_end"] - e["bar_start"], e) for e in rulers if e["kind"] == "att" and e["first"] is not None and e["last"] is not None and e["first"] != e["last"] and e["qual"] in ("x", "c")]
spans.sort(key=lambda t: -t[0])
top3 = spans[:3]
med_span = statistics.median([s for s, _ in spans])
# presence of rulers per half-century
def overlap(e, b):
    return e["bar_start"] <= b + 49 and e["bar_end"] >= b
presence = []
bins = list(range(1100, 1600, 50))
for k in LINES:
    for b in bins:
        n = sum(1 for e in rulers if e["line"] == k and overlap(e, b))
        presence.append([k, LINES[k][0], LINES[k][1], b, n])
tot_by_bin = {b: sum(r[4] for r in presence if r[3] == b) for b in bins}
peak_bin = max(tot_by_bin, key=lambda b: tot_by_bin[b])
peak_n = tot_by_bin[peak_bin]
peak_split = {r[0]: r[4] for r in presence if r[3] == peak_bin}
print(nE, rcount, ccount, ocount, top3[0][1]["name"], top3[0][0], med_span, peak_bin, peak_n, peak_split)

LCOL = {"field": bi("line_de", "line_en"), "type": "nominal", "title": bi("Linie", "Line"),
        "scale": {"domain": [bi(LINES[k][0], LINES[k][1]) for k in LINES]}}
YEAR = bi("Jahr", "Year")
Y_LABEL = {"field": "label", "type": "ordinal", "sort": {"field": "sortkey", "op": "min"}, "title": None, "axis": {"labelLimit": 400}}
TT = [{"field": "name", "title": bi("Name (wie gedruckt)", "Name (as printed)")},
      {"field": "date_text", "title": bi("Datum (wie gedruckt)", "Date (as printed)")},
      {"field": "note", "title": bi("Zusatz (wie gedruckt)", "Note (as printed)")},
      {"field": "tab", "title": bi("Tafel", "Table")},
      {"field": bi("line_de", "line_en"), "title": bi("Linie", "Line")}]


def gantt(flt, dom):
    LC = dict(LCOL, legend={"columns": 2})
    return {"height": 420,
            "transform": [{"filter": flt}],
            "layer": [
                {"transform": [{"filter": "datum.bar_start < datum.bar_end"}],
                 "mark": {"type": "bar", "height": 9},
                 "encoding": {"y": Y_LABEL,
                              "x": {"field": "bar_start", "type": "quantitative", "title": YEAR, "axis": {"format": "d", "tickCount": 8}, "scale": {"zero": False, "domain": dom}},
                              "x2": {"field": "bar_end"}, "color": LC, "tooltip": TT}},
                {"transform": [{"filter": "datum.bar_start == datum.bar_end"}],
                 "mark": {"type": "point", "size": 70, "filled": True},
                 "encoding": {"y": Y_LABEL,
                              "x": {"field": "bar_start", "type": "quantitative"}, "color": LC, "tooltip": TT}},
            ]}


