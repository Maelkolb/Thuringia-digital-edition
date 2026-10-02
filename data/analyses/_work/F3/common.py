import copy
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\totom\Projects\reuss-edition"
ANALYSES = os.path.join(ROOT, "data", "analyses")
ARCHIVE = os.path.join(ANALYSES, "_archive")
SHARED = os.path.join(ANALYSES, "_shared")

DATE = "2026-10-02"
GENERATED_BY = "Claude Sonnet 5.5 (Agent F3), aus {k} Einzelauswertungen zusammengeführt"


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def archived(aid):
    return load_json(os.path.join(ARCHIVE, aid + ".json"))


def dataset(aid, name):
    for d in archived(aid)["datasets"]:
        if d["name"] == name:
            return copy.deepcopy(d)
    raise KeyError((aid, name))


def dicts(ds):
    cols = [c["name"] for c in ds["columns"]]
    return [dict(zip(cols, r)) for r in ds["rows"]]


def bi(de, en):
    return {"de": de, "en": en}


def col(name, de, en, type_="string", unit=None, derived=False, note=None):
    c = {"name": name, "label": bi(de, en), "type": type_, "unit": unit}
    if derived:
        c["derived"] = True
    if note:
        c["note"] = note
    return c


def make_dataset(name, title_de, title_en, columns, rows, source_refs):
    return {
        "name": name,
        "title": bi(title_de, title_en),
        "columns": columns,
        "rows": rows,
        "source_refs": source_refs,
    }


def add_columns(ds, new_cols, fn):
    """Append derived columns; fn(row_dict) -> list of values in the order of new_cols."""
    rows = dicts(ds)
    ds["columns"] = ds["columns"] + new_cols
    ds["rows"] = [r + fn(d) for r, d in zip(ds["rows"], rows)]
    return ds


def base_layers():
    places = load_json(os.path.join(SHARED, "base_places.json"))
    rivers = load_json(os.path.join(SHARED, "base_rivers.json"))
    return places, rivers


def coordinate_lookup():
    places, _ = base_layers()
    out = {}
    for r in places["rows"]:
        name, lon, lat, landesteil = r[0], r[1], r[2], r[3]
        if name not in out:
            out[name] = (lon, lat, landesteil)
    return out


def words(s):
    return len(s.split())


def n_de(x, d=0):
    s = f"{x:,.{d}f}"
    return s.replace(",", "§").replace(".", ",").replace("§", ".")


def n_en(x, d=0):
    return f"{x:,.{d}f}"


def tip(field, de, en, fmt=None, type_=None):
    t = {"field": field, "title": bi(de, en) if en is not None else de}
    if fmt:
        t["format"] = fmt
    if type_:
        t["type"] = type_
    return t


def write_feature(obj):
    path = os.path.join(ANALYSES, obj["id"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    return path


def check_lengths(obj):
    problems = []

    def chk(label, b, mx):
        for lang in ("de", "en"):
            n = words(b[lang])
            if n > mx:
                problems.append(f"{label} [{lang}] {n} > {mx}")

    chk("title", obj["title"], 12)
    chk("summary", obj["summary"], 75)
    for i, f in enumerate(obj.get("findings", [])):
        chk(f"finding{i+1}", f, 35)
    for i, c in enumerate(obj.get("caveats", [])):
        chk(f"caveat{i+1}", c, 60)
    chk("method", obj["method"], 260)
    for c in obj["charts"]:
        chk(c["id"] + " title", c["title"], 16)
        chk(c["id"] + " caption", c["caption"], 45)
    return problems


def union_sources(*aids):
    seen = []
    keys = set()
    for aid in aids:
        for s in archived(aid).get("sources", []):
            k = (s["page"], s["block"], s.get("rows"))
            if k not in keys:
                keys.add(k)
                seen.append({kk: vv for kk, vv in s.items()})
    return seen


def union_issues(*aids):
    out = []
    for aid in aids:
        for t in archived(aid).get("transcription_issues") or []:
            out.append(t)
    return out
