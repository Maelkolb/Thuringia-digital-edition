import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\totom\Projects\reuss-edition")
ANALYSES = ROOT / "data" / "analyses"
WORK = ANALYSES / "_work" / "F7"
ARCHIVE = ANALYSES / "_archive"
SHARED = ANALYSES / "_shared"

sys.stdout.reconfigure(encoding="utf-8")


def bi(de, en):
    return {"de": de, "en": en}


def col(name, de, en, type_, unit=None, derived=False, note=None):
    c = {"name": name, "label": bi(de, en), "type": type_, "unit": unit}
    if derived:
        c["derived"] = True
    if note:
        c["note"] = note
    return c


def dataset(name, title, columns, rows, refs):
    return {"name": name, "title": title, "columns": columns, "rows": rows, "source_refs": refs}


def ref(page, block, rows=None, note=None):
    r = {"page": str(page), "block": block}
    if rows:
        r["rows"] = rows
    if note:
        r["note"] = note
    return r


def load_archive(aid):
    return json.loads((ARCHIVE / f"{aid}.json").read_text(encoding="utf-8"))


def archive_dataset(aid, name):
    for d in load_archive(aid)["datasets"]:
        if d["name"] == name:
            return d
    raise KeyError(name)


def shared_dataset(fname):
    return json.loads((SHARED / fname).read_text(encoding="utf-8"))


def rows_as_dicts(ds):
    names = [c["name"] for c in ds["columns"]]
    return [dict(zip(names, r)) for r in ds["rows"]]


def de_num(x, decimals=0):
    s = f"{x:,.{decimals}f}"
    return s.replace(",", "§").replace(".", ",").replace("§", ".")


def en_num(x, decimals=0):
    return f"{x:,.{decimals}f}"


def write_feature(obj):
    path = ANALYSES / f"{obj['id']}.json"
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return path


def validate(fid):
    r = subprocess.run(["node", "tools/validate_analysis.mjs", f"data/analyses/{fid}.json"], cwd=ROOT,
                       capture_output=True, text=True, encoding="utf-8")
    print(r.stdout)
    print(r.stderr)
    return r.returncode == 0


def words(s):
    return len(s.split())


def check_limits(obj):
    problems = []

    def lim(label, b, mx):
        for l in ("de", "en"):
            n = words(b[l])
            if n > mx:
                problems.append(f"{label} [{l}] {n}>{mx}")
    lim("title", obj["title"], 12)
    lim("summary", obj["summary"], 75)
    for i, f in enumerate(obj.get("findings", [])):
        lim(f"finding{i+1}", f, 35)
    lim("method", obj["method"], 260)
    for i, c in enumerate(obj.get("caveats", [])):
        lim(f"caveat{i+1}", c, 60)
    for c in obj["charts"]:
        lim(c["id"] + " title", c["title"], 16)
        lim(c["id"] + " caption", c["caption"], 45)
    return problems
