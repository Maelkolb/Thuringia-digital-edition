import copy
import json
import os
import re
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


def drop_columns(ds, names):
    keep = [i for i, c in enumerate(ds["columns"]) if c["name"] not in names]
    assert len(keep) == len(ds["columns"]) - len(names), names
    ds["columns"] = [ds["columns"][i] for i in keep]
    ds["rows"] = [[r[i] for i in keep] for r in ds["rows"]]


def map_column(ds, name, mapping, label=None):
    i = colnames(ds).index(name)
    for r in ds["rows"]:
        if r[i] not in (None, ""):
            r[i] = mapping[r[i]]
    if label:
        ds["columns"][i]["label"] = label
    ds["columns"][i]["type"] = "string"
    ds["columns"][i].pop("note", None)


BRITISH = [
    (r"\bneighbor", "neighbour"), (r"\bNeighbor", "Neighbour"),
    (r"\bgray\b", "grey"), (r"\bGray\b", "Grey"),
    (r"\bcolor", "colour"), (r"\bColor", "Colour"),
    (r"\bliter(s?)\b", r"litre\1"), (r"\bmeter(s?)\b", r"metre\1"),
    (r"\bcenter", "centre"), (r"\bCenter", "Centre"),
    (r"\blabor", "labour"), (r"\bLabor", "Labour"),
    (r"\blabeled\b", "labelled"), (r"\blabeling\b", "labelling"),
    (r"\btoward\b", "towards"), (r"\bjudgment", "judgement"),
    (r"\bfavor", "favour"), (r"\bhonor", "honour"), (r"\bbehavior", "behaviour"),
    (r"\btraveled", "travelled"), (r"\bmodeled", "modelled"), (r"\bdefense\b", "defence"),
    (r"\b(analy|digiti|normali|organi|recogni|reali|characteri|standardi|summari|speciali|emphasi|categori|centrali|utili)z", r"\1s"),
    (r"\b(Analy|Digiti|Normali|Organi|Recogni|Reali|Characteri|Standardi|Summari|Speciali|Emphasi|Categori|Centrali|Utili)z", r"\1s"),
    (r"\bUpper Land\b", "Oberland"), (r"\bLower Land\b", "Unterland"),
]


def british(text):
    for pattern, replacement in BRITISH:
        text = re.sub(pattern, replacement, text)
    return text


def british_english(node):
    if isinstance(node, list):
        return [british_english(n) for n in node]
    if not isinstance(node, dict):
        return node
    if set(node) == {"de", "en"} and isinstance(node["en"], str):
        return {"de": node["de"], "en": british(node["en"])}
    if "columns" in node and "rows" in node:
        english = [i for i, c in enumerate(node["columns"]) if c["name"].endswith("_en")]
        node = dict(node, rows=[[british(v) if i in english and isinstance(v, str) else v for i, v in enumerate(r)] for r in node["rows"]])
    return {k: british_english(v) if k != "rows" else v for k, v in node.items()}


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
        json.dump(british_english(a), f, ensure_ascii=False, indent=1)
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
