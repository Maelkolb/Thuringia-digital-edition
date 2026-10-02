"""Analysis: heights of springs, mouths, entries and exits of the streams (pp. 45-53)."""
from common import *

# (stream, region, point type, printed height, page, block, note)
# region: M = Main/Rhein basin, O = Oberland (Saale, Weida), U = Unterland (Elster)
PTS = [
    ("Rodach", "M", "source", "1772", "45", "b7", "Rodacherbrunn auf dem Frankenwald"),
    ("Grumbach (zum Kettelbach)", "M", "source", "1850", "45", "b13", ""),
    ("Großer Rosenbaumbach", "M", "source", "1825", "45", "b13", ""),
    ("Saale", "O", "entry", "1190", "46", "b2", "Einmündung des Kegelbachs"),
    ("Saale", "O", "exit", "923", "46", "b2", "Mündung des Molbitzbachs"),
    ("Tannenbach", "O", "source", "1600", "46", "b4", "oberhalb Gebersreuth"),
    ("Töpenbach (Kupferbach)", "O", "source", "1625", "46", "b4", ""),
    ("Erlichsbach", "O", "source", "1580", "46", "b5", "oberhalb Gefell"),
    ("Ziezelbach", "O", "source", "1475", "46", "b16", ""),
    ("Wettera", "O", "source", "1646", "47", "b4", ""),
    ("Wettera", "O", "mouth", "945", "47", "b4", "in die Saale"),
    ("Wioschwitz (zur Selbitz)", "O", "source", "1647", "48", "b4", "Südwestfuß des Kulm"),
    ("Wiesenthal", "O", "mouth", "862", "48", "b1", "in die Saale unterhalb Dörflas"),
    ("Lemnitz", "O", "source", "1537", "48", "b6", ""),
    ("Lemnitz", "O", "mouth", "1061", "48", "b6", "beim Lemnitzhammer"),
    ("Sieglitzbach", "O", "source", "1650", "48", "b6", ""),
    ("Sieglitzbach", "O", "mouth", "1098", "48", "b6", "in die Lemnitz"),
    ("Langwasser (Sormitz)", "O", "source", "1721,7", "49", "b5", "am Kulm im Frankenwald"),
    ("Weida", "O", "source", "1300", "49", "b6", "Quellflächen bei Pausa (außerhalb des Landes)"),
    ("Weida", "O", "entry", "1055", "49", "b6", "südlich von Leitlitz"),
    ("Weida", "O", "exit", "840", "49", "b6", ""),
    ("Triebes (zur Weida)", "O", "source", "1225", "50", "b15", "Pöllwitzwald"),
    ("Triebes (zur Weida)", "O", "entry", "960", "50", "b15", ""),
    ("Triebes (zur Weida)", "O", "exit", "776", "50", "b15", ""),
    ("Leuba", "O", "entry", "975", "50", "b16", ""),
    ("Leuba", "O", "exit", "774", "50", "b16", ""),
    ("Elster", "U", "entry", "525", "51", "b1", ""),
    ("Elster", "U", "exit", "459", "51", "b1", ""),
    ("Erlbach", "U", "entry", "824", "52", "b1", ""),
    ("Erlbach", "U", "mouth", "487,3", "51", "b8", "unterhalb Thieschitz"),
    ("Saarbach (zum Erlbach)", "U", "entry", "745", "52", "b1", ""),
    ("Saarbach (zum Erlbach)", "U", "mouth", "540", "52", "b1", "Einmündung in den Erlbach"),
    ("Schafgrund", "U", "inflow", "700", "52", "b2", "Einfluss der Treibe"),
    ("Schafgrund", "U", "mouth", "480", "52", "b2", ""),
    ("Goldthalwasser", "U", "mouth", "468", "52", "b3", "unterhalb Köstritz"),
    ("Pfortenbach", "U", "mouth", "505", "52", "b11", "bei Pforten"),
    ("Zaufensgraben", "U", "source", "822", "52", "b12", "Südosthöhe von Leumnitz"),
    ("Leumnitzbach", "U", "source", "798", "52", "b13", ""),
    ("Leumnitzbach", "U", "entry", "575", "52", "b13", "Eintritt in Gera"),
    ("Krautgrund", "U", "source", "797", "52", "b14", "südöstlich von Trebnitz"),
    ("Krautgrund", "U", "mouth", "495", "52", "b14", "unterhalb Cuba"),
    ("Brambach", "U", "source", "760", "52", "b15", "Quellfäden bei Bethenhausen und Caasen"),
    ("Brambach", "U", "mouth", "490", "53", "b1", "unterhalb Tinz"),
    ("Aga (Reichenbach)", "U", "source", "830", "53", "b6", "Reichenbach bei Kleinaga"),
]
REGION = {"M": ("Main (Rhein)", 1), "O": ("Oberland", 2), "U": ("Unterland", 3)}
# printed value strings use a decimal comma in the source; verify each against the block text
rows_pts = []
for s, reg, typ, val, pg, bl, note in PTS:
    ft = num_in_text(val, pg, bl)
    rows_pts.append([s, REGION[reg][0], REGION[reg][1], typ, ft, round(ft * FT_M, 1), pg, bl, note])

# reaches: streams with an upper and a lower height
by = {}
for r in rows_pts:
    by.setdefault(r[0], []).append(r)
reach_rows = []
RCODE = {"A": "Quelle → Mündung", "B": "Landeseintritt → Landesaustritt", "C": "Teilstrecke"}
for s, rs in by.items():
    types = {r[3]: r for r in rs}
    if len(rs) < 2:
        continue
    if "source" in types and "mouth" in types:
        up, lo, code = types["source"], types["mouth"], "A"
    elif "entry" in types and "exit" in types:
        up, lo, code = types["entry"], types["exit"], "B"
    else:
        up = max(rs, key=lambda r: r[4])
        lo = min(rs, key=lambda r: r[4])
        code = "C"
    if up[4] == lo[4]:
        continue
    reach_rows.append([s, up[1], up[2], code, up[4], lo[4], round(up[4] * FT_M, 1), round(lo[4] * FT_M, 1),
                       round(up[4] - lo[4], 1), round((up[4] - lo[4]) * FT_M, 1)])
reach_rows.sort(key=lambda r: -r[4])
for r in reach_rows:
    print(r)
print(len(rows_pts), "points;", len(reach_rows), "reaches")

src = sorted([r for r in rows_pts if r[3] == "source"], key=lambda r: -r[4])
print([(r[0], r[4]) for r in src])
import statistics
def rng(reg, typ="source"):
    v = [r[4] for r in rows_pts if r[2] == reg and r[3] == typ]
    return min(v), max(v), len(v)
print("M", rng(1), "O", rng(2), "U", rng(3))
