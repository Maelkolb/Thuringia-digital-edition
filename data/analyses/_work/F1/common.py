"""Shared helpers for agent F1 (features land-lage-grenzen, relief-hoehen, geologie-boden, gewaesser)."""
import json
import math
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:\Users\totom\Projects\reuss-edition")
ARCHIVE = ROOT / "data" / "analyses" / "_archive"
SHARED = ROOT / "data" / "analyses" / "_shared"
OUT = ROOT / "data" / "analyses"

DFUSS_M = 0.3766242          # 1 preuss. Dezimalfuss in m (Brueckner p. 11 fn., p. 831)
QM_KM2 = 55.06               # 1 geographische Quadratmeile in km2 (p. 832)


def load(aid):
    return json.loads((ARCHIVE / f"{aid}.json").read_text(encoding="utf-8"))


def ds_of(a, name):
    return next(d for d in a["datasets"] if d["name"] == name)


def rows_as_dicts(ds):
    cols = [c["name"] for c in ds["columns"]]
    return [dict(zip(cols, r)) for r in ds["rows"]]


def shared(name):
    return json.loads((SHARED / f"{name}.json").read_text(encoding="utf-8"))


def T(de, en):
    return {"de": de, "en": en}


def de(x, nd=1, thousands=True):
    """German number format: decimal comma, thousands point."""
    s = f"{x:,.{nd}f}"
    return s.replace(",", "\u0000").replace(".", ",").replace("\u0000", ".") if thousands else f"{x:.{nd}f}".replace(".", ",")


def en(x, nd=1):
    return f"{x:,.{nd}f}"


def km(lon1, lat1, lon2, lat2):
    kx = 111.32 * math.cos(math.radians((lat1 + lat2) / 2))
    return math.hypot((lon1 - lon2) * kx, (lat1 - lat2) * 111.2)


def words(s):
    return len(s.split())


def dump(feature):
    path = OUT / f"{feature['id']}.json"
    path.write_text(json.dumps(feature, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", path)


def validate(fid):
    r = subprocess.run(["node", "tools/validate_analysis.mjs", f"data/analyses/{fid}.json"], cwd=ROOT,
                       capture_output=True, text=True, encoding="utf-8")
    print(r.stdout)
    print(r.stderr[-2000:])
    return r.returncode == 0


def col(name, de_, en_, typ, unit=None, derived=False, note=None):
    c = {"name": name, "label": T(de_, en_), "type": typ, "unit": unit}
    if derived:
        c["derived"] = True
    if note:
        c["note"] = note
    return c


def tooltip(*fields):
    """fields: (field, de, en, fmt or None)"""
    out = []
    for f in fields:
        t = {"field": f[0], "title": T(f[1], f[2]) if f[1] else f[0]}
        if len(f) > 3 and f[3]:
            t["format"] = f[3]
        out.append(t)
    return out
