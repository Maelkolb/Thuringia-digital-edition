"""A01 analysis 1: trigonometrically determined points (pp. 6-7), extents of Unter-/Oberland (pp. 4-6)."""
import json, math, re, statistics
from common import *

FERRO = 17 + 40 / 60       # Ferro meridian = 17 deg 40' west of Greenwich (editorial constant, caller's rule)

def parse_dms(s):
    """'29° 7' 42" L.' -> (29, 7, 42.0); decimals use comma."""
    s = s.replace("''", '"').replace("„", "").replace("″", '"')
    m = re.match(r"^\s*(\d+)°\s*(\d+)'\s*(\d+(?:,\d+)?)\"", s)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2)), num(m.group(3))

# corrections confirmed on the facsimile (spurious '1' after the decimal comma in the transcription)
FIX = {("Lobenstein", "lon"): 27.54, ("Bellevue", "lon"): 28.05, ("(St. Gangloff", "lon"): 6.27}

rows_src = []
for page, bid in (("6", "b3"), ("7", "b1")):
    for ri, r in enumerate(grid(page, bid)):
        rows_src.append((page, bid, ri + 1, r))

OBJ_CLASS = [
    (r"(?i)^Kirche\.?$", "Kirche"),
    (r"(?i)(Thurmknopf|Kirchthurmknopf)", "Turmknopf"),
    (r"(?i)^Signal", "Signalpunkt/-stein"),
    (r"(?i)(Thurm|Schloß)", "Turm, Schloss, Ruine"),
    (r"(?i)Mühle", "Mühle"),
    (r"(?i)(Kohlhäuser|Forsthaus|Haus|Schornstein|Giebel)", "Haus, Schornstein"),
    (r"(?i)Dorf[s]?mitte", "Dorfmitte"),
]

def obj_class(o):
    if not o:
        return "ohne Angabe"
    for pat, c in OBJ_CLASS:
        if re.search(pat, o):
            return c
    return "Sonstiges"

LABELLED = {"Gera", "Köstritz", "Hohenleuben", "Schleiz", "Lobenstein", "Tanna", "Hirschberg", "Geissen"}
# Geissen is listed in the Unterland heights (p. 13) although its printed latitude lies south of the Unterland's printed limit
UNTERLAND_OVERRIDE = {"Geissen"}
UL_MIN_LAT = 50 + 47/60 + 48/3600

points = []
issues = []
for page, bid, rno, r in rows_src:
    name_raw = r[0]
    br = 1 if name_raw.startswith("(") else 0
    name = name_raw.lstrip("(").strip()
    lon = parse_dms(r[1])
    lat = parse_dms(r[2]) if r[2].strip() else None
    obj = r[3].strip().rstrip(")").rstrip(".").strip() if r[3].strip() else None
    if obj:
        obj = obj.replace("Straßen= kreuzungspunkt", "Straßenkreuzungspunkt")
    key = (name_raw, "lon")
    if key in FIX:
        issues.append(dict(page=page, block=bid, cell=f"r{rno}c2", transcribed=r[1], printed=FIX[key], name=name))
        lon = (lon[0], lon[1], FIX[key])
    lon_dec = lon[0] + lon[1] / 60 + lon[2] / 3600
    lat_dec = (lat[0] + lat[1] / 60 + lat[2] / 3600) if lat else None
    lon_gw = lon_dec - FERRO
    if lat_dec is None:
        lt = None
    elif name in UNTERLAND_OVERRIDE:
        lt = "Unterland"
    else:
        lt = "Unterland" if lat_dec >= UL_MIN_LAT else "Oberland"
    points.append(dict(page=page, block=bid, rno=rno, name=name, bracket=br, lon=lon, lat=lat, obj=obj,
                       lon_dec=lon_dec, lat_dec=lat_dec, lon_gw=lon_gw, landesteil=lt if lt else "Oberland",
                       cls=obj_class(obj), lab=1 if name in LABELLED and not br else 0))

# Kleinfriesa has no latitude -> excluded from the map (kept in the table)
for p in points:
    print(p["page"], p["rno"], p["name"], p["lon"], p["lat"], p["obj"], p["cls"], p["landesteil"], round(p["lon_gw"], 4), None if p["lat_dec"] is None else round(p["lat_dec"], 4))
print(len(points), "points")
json.dump(dict(points=points, issues=issues), open("lage_points.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
