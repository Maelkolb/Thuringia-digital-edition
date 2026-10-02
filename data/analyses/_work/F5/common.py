import json
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:\Users\totom\Projects\reuss-edition")
ARCHIVE = ROOT / "data" / "analyses" / "_archive"
SHARED = ROOT / "data" / "analyses" / "_shared"
OUT = ROOT / "data" / "analyses"

DISTRICTS = ["Gera", "Schleiz", "Lobenstein-Ebersdorf"]
DISTRICT_COLORS = ["@accent", "@accent2", "@accent3"]


def load(archive_id):
    return json.loads((ARCHIVE / f"{archive_id}.json").read_text(encoding="utf-8"))


def dataset(archive_id, name):
    d = load(archive_id)
    return next(x for x in d["datasets"] if x["name"] == name)


def rows_as_dicts(ds):
    cols = [c["name"] for c in ds["columns"]]
    return [dict(zip(cols, r)) for r in ds["rows"]]


def col(name, de, en, typ, unit=None, derived=False, note=None):
    c = {"name": name, "label": {"de": de, "en": en}, "type": typ, "unit": unit}
    if derived:
        c["derived"] = True
    if note:
        c["note"] = note
    return c


def num_de(x, nd=0):
    s = f"{x:,.{nd}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def num_en(x, nd=0):
    return f"{x:,.{nd}f}"


def bi(de, en):
    return {"de": de, "en": en}


def pct_de(x, nd=1):
    return num_de(x, nd) + " Prozent"


def pct_en(x, nd=1):
    return num_en(x, nd) + " percent"


def words(s):
    return len(s.split())


def write_feature(feature, path=None):
    path = path or OUT / f"{feature['id']}.json"
    Path(path).write_text(json.dumps(feature, ensure_ascii=False, indent=1), encoding="utf-8")
    return path


def validate(feature_id):
    r = subprocess.run(
        ["node", "tools/validate_analysis.mjs", f"data/analyses/{feature_id}.json"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
    )
    print(r.stdout)
    if r.stderr:
        print(r.stderr[:3000])
    return r.returncode


def tooltip(field, de, en, fmt=None):
    t = {"field": field, "title": bi(de, en)}
    if fmt:
        t["format"] = fmt
    return t


def refs_of(ds):
    return ds["source_refs"]


def sources_from(datasets, extra=None):
    seen = []
    out = []
    for ds in datasets:
        for r in ds["source_refs"]:
            key = (r["page"], r["block"])
            if key not in seen:
                seen.append(key)
                out.append({"page": r["page"], "block": r["block"]})
    for r in extra or []:
        key = (r["page"], r["block"])
        if key not in seen:
            seen.append(key)
            out.append(r)
    return out


def shared_dataset(name):
    f = {"orte_basis": "base_places.json", "fluesse_basis": "base_rivers.json"}[name]
    return json.loads((SHARED / f).read_text(encoding="utf-8"))
