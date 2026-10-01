"""Stage 4a - collect every entity mention, group surface forms into keys and
attach authority candidates, as input for the adjudication subagents.

Mentions -> data/entities/mentions.jsonl (one per mention, with context)
Candidates -> data/entities/candidates/<group>.json

Groups: places (Location), nature (Natural Object), persons, organisations,
organisms (Animal, Plant), concepts (Artefact, Resource, Environment, Climate,
Environmental Impact).
"""
from __future__ import annotations

import collections
import csv
import json
import math
import re
import sys
import unicodedata

from common import DATA, PAGES_DIR, SOURCE, read_json, write_json

csv.field_size_limit(sys.maxsize)
GROUPS = {
    "Location": "places", "Natural Object": "nature", "Person": "persons", "Organisation": "organisations",
    "Animal": "organisms", "Plant": "organisms", "Artefact": "concepts", "Resource": "concepts",
    "Environment": "concepts", "Climate": "concepts", "Environmental Impact": "concepts",
}
CENTER = (50.62, 11.85)  # Reuss j. L., between Schleiz and Gera
CORE = (50.30, 51.00, 11.40, 12.30)  # lat0, lat1, lon0, lon1


def units_of(p: dict):
    for b in p["blocks"]:
        if b["type"] in ("paragraph", "heading"):
            yield b["id"], b
        elif b["type"] == "list":
            for i, it in enumerate(b["items"], 1):
                yield f"{b['id']}.i{i}", it
        elif b["type"] == "table":
            for r, row in enumerate(b["rows"], 1):
                for c, cell in enumerate(row["cells"], 1):
                    yield f"{b['id']}.r{r}c{c}", cell
    for fn in p["footnotes"]:
        yield fn["id"], fn


def strip_accents(s: str) -> str:
    return "".join(ch for ch in unicodedata.normalize("NFD", s) if unicodedata.category(ch) != "Mn")


def match_key(s: str) -> str:
    """Spelling-tolerant key: 1870 vs modern orthography, case, umlauts."""
    s = s.lower().strip()
    s = re.sub(r"^(bad|markt|stadt|schloss|schloß)\s+", "", s)
    s = s.replace("ß", "ss").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
    s = s.replace("th", "t").replace("ph", "f").replace("y", "i")
    s = re.sub(r"c(?=[aou])", "k", s)
    s = re.sub(r"c(?=[ei])", "z", s)
    s = s.replace("ck", "k").replace("dt", "t")
    s = strip_accents(s)
    return re.sub(r"[^a-z]", "", s)


ARTICLES = re.compile(r"^(der|die|das|dem|den|des|im|am|zum|zur|bei|von)\s+", re.I)


def surface_key(form: str, etype: str) -> str:
    f = re.sub(r"\s+", " ", form).strip().strip(".,;:()[]„“\"'")
    f = ARTICLES.sub("", f)
    if etype in ("Location", "Natural Object", "Organisation", "Person"):
        f = re.sub(r"(?<=[a-zäöü])['’]s$", "", f)  # Gera's
    return f


def km(a, b):
    la1, lo1 = map(math.radians, a)
    la2, lo2 = map(math.radians, b)
    d = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(d))


def load_geonames():
    idx = collections.defaultdict(list)
    with open(SOURCE / "geonames" / "DE.txt", encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE):
            gid, name, ascii_, alts, lat, lon, fclass, fcode = row[:8]
            lat, lon = float(lat), float(lon)
            if not (49.0 <= lat <= 52.6 and 9.5 <= lon <= 15.0):
                continue
            if fclass not in "PHTLAS":
                continue
            rec = {"geonames": int(gid), "name": name, "lat": round(lat, 5), "lon": round(lon, 5), "class": fclass,
                   "code": fcode, "admin1": row[10], "population": int(row[14] or 0),
                   "km": round(km(CENTER, (lat, lon)), 1)}
            keys = {match_key(name), match_key(ascii_)}
            for alt in alts.split(","):
                if alt and not re.search(r"\d|http", alt) and len(alt) < 40:
                    keys.add(match_key(alt))
            for k in keys:
                if k:
                    idx[k].append(rec)
    return idx


def main() -> None:
    pages = [read_json(f) for f in sorted(PAGES_DIR.glob("*.json"))]
    mentions = []
    for p in pages:
        for uid, u in units_of(p):
            txt = u["text"]
            for n, (s, e, t) in enumerate(u.get("spans", [])):
                form = txt[s:e]
                mentions.append({
                    "page": p["slug"], "seq": p["seq"], "unit": uid, "start": s, "end": e, "type": t, "form": form,
                    "key": surface_key(form, t),
                    "ctx": (txt[max(0, s - 70):s] + "⟦" + form + "⟧" + txt[e:e + 70]).replace("\n", " "),
                })
    out = DATA / "entities"
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "mentions.jsonl", "w", encoding="utf-8") as f:
        for m in mentions:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")

    register = read_json(DATA / "registers" / "ortsregister.json")["entries"]
    reg_idx = collections.defaultdict(list)
    for r in register:
        if "pages" in r:
            reg_idx[match_key(r["name"])].append({"name": r["name"], "parents": r.get("parents", []), "pages": r["pages"],
                                                  "wuestung": r.get("wuestung", False), "gemeinde": r.get("gemeinde", False)})
    print("loading GeoNames …")
    geo = load_geonames()

    groups: dict[str, dict] = collections.defaultdict(dict)
    for m in mentions:
        g = GROUPS[m["type"]]
        k = m["key"]
        ent = groups[g].setdefault(k, {"key": k, "types": collections.Counter(), "forms": collections.Counter(),
                                        "n": 0, "pages": [], "contexts": []})
        ent["n"] += 1
        ent["types"][m["type"]] += 1
        ent["forms"][m["form"]] += 1
        if m["page"] not in ent["pages"]:
            ent["pages"].append(m["page"])
        if len(ent["contexts"]) < 4 and (not ent["contexts"] or m["page"] != ent["contexts"][-1]["page"]):
            ent["contexts"].append({"page": m["page"], "unit": m["unit"], "text": m["ctx"]})
    for g, ents in groups.items():
        lst = []
        for k, e in ents.items():
            rec = {"key": k, "n": e["n"], "types": dict(e["types"]), "forms": dict(e["forms"].most_common(8)),
                   "pages": e["pages"][:15] + (["…"] if len(e["pages"]) > 15 else []), "n_pages": len(e["pages"]),
                   "contexts": e["contexts"]}
            if g in ("places", "nature"):
                mk = match_key(k)
                if reg_idx.get(mk):
                    rec["brueckner_register"] = reg_idx[mk]
                cands = sorted(geo.get(mk, []), key=lambda r: (r["km"], -r["population"]))
                # keep nearby candidates first, then the most populous far ones
                near = [c for c in cands if c["km"] <= 60][:5]
                far = sorted([c for c in cands if c["km"] > 60], key=lambda r: -r["population"])[:3]
                if near or far:
                    rec["geonames_candidates"] = near + far
            lst.append(rec)
        lst.sort(key=lambda r: -r["n"])
        write_json(out / "candidates" / f"{g}.json", {"group": g, "n_keys": len(lst), "entries": lst})
        auto = sum(1 for r in lst if r.get("geonames_candidates") or r.get("brueckner_register"))
        print(f"{g:14s} keys {len(lst):5d}  mentions {sum(r['n'] for r in lst):6d}  with candidates {auto}")


if __name__ == "__main__":
    main()
