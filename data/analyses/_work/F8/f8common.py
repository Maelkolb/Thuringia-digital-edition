import copy
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\totom\Projects\reuss-edition"
AN = os.path.join(ROOT, "data", "analyses")


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def arch(aid):
    return load(os.path.join(AN, "_archive", aid + ".json"))


def dataset(a, name, new_name=None):
    ds = [d for d in a["datasets"] if d["name"] == name][0]
    ds = copy.deepcopy(ds)
    if new_name:
        ds["name"] = new_name
    return ds


def rows(ds):
    cols = [c["name"] for c in ds["columns"]]
    return [dict(zip(cols, r)) for r in ds["rows"]]


def colnames(ds):
    return [c["name"] for c in ds["columns"]]


def add_column(ds, name, label_de, label_en, values, typ="number", unit=None, note=None):
    col = {"name": name, "label": {"de": label_de, "en": label_en}, "type": typ, "unit": unit, "derived": True}
    if note:
        col["note"] = note
    ds["columns"].append(col)
    assert len(values) == len(ds["rows"])
    for r, v in zip(ds["rows"], values):
        r.append(v)


def base_places():
    return load(os.path.join(AN, "_shared", "base_places.json"))


def base_rivers():
    return load(os.path.join(AN, "_shared", "base_rivers.json"))


def bi(de, en):
    return {"de": de, "en": en}


def words(s):
    return len(s.split())


def write_feature(a, fid, validate=True):
    path = os.path.join(AN, fid + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(a, f, ensure_ascii=False, indent=1)
    # length report
    for k in ("summary", "method"):
        print(k, words(a[k]["de"]), words(a[k]["en"]))
    for i, x in enumerate(a.get("findings", [])):
        print("finding", i + 1, words(x["de"]), words(x["en"]))
    for c in a["charts"]:
        print(c["id"], "title", words(c["title"]["de"]), words(c["title"]["en"]), "caption", words(c["caption"]["de"]), words(c["caption"]["en"]))
    if validate:
        r = subprocess.run(["node", "tools/validate_analysis.mjs", path], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        print(r.stdout)
        print(r.stderr[-1500:])


def de_en(de, en):
    return {"de": de, "en": en}


def fmt_de(x, nd=0):
    s = f"{x:,.{nd}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")
