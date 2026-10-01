"""Coordinates for Brückner's place articles (data/gazetteer/*.json).

Priority: entity decisions (E-agents, verified GeoNames choice) > the GeoNames
candidate nearest to the principality whose name matches the article name
(populated places first, then any feature class) > none.
Output: data/gazetteer/coords.json  {gazetteer id: {lat, lon, source, geonames}}
"""
from __future__ import annotations

import glob
import json

from common import DATA, read_json, write_json
from entities_prepare import match_key


def main() -> None:
    gaz = []
    for f in sorted(glob.glob(str(DATA / "gazetteer" / "G*.json"))):
        gaz += read_json(f)["entries"]
    decisions = {}
    for f in glob.glob(str(DATA / "entities" / "decisions" / "E*.json")):
        d = read_json(f)
        for x in d.get("decisions", []):
            if x.get("lat") is not None and x.get("action") in ("accept", "reclass"):
                decisions.setdefault(match_key(x.get("label") or x["key"]), x)
                decisions.setdefault(match_key(x["key"]), x)
    cands = {}
    for e in read_json(DATA / "entities" / "candidates" / "places.json")["entries"]:
        if e.get("geonames_candidates"):
            cands[match_key(e["key"])] = e["geonames_candidates"]
    out, missing = {}, []
    for g in gaz:
        if g.get("type") in ("Landestheil", "Sonstiges"):
            continue
        k = match_key(g["name"])
        d = decisions.get(k)
        if d:
            out[g["id"]] = {"lat": d["lat"], "lon": d["lon"], "geonames": d.get("geonames"), "source": "entity decision"}
            continue
        cs = cands.get(k, [])
        near = [c for c in cs if c["km"] <= 45 and c["class"] == "P"] or [c for c in cs if c["km"] <= 45]
        if near:
            c = min(near, key=lambda c: c["km"])
            out[g["id"]] = {"lat": c["lat"], "lon": c["lon"], "geonames": c["geonames"], "source": "GeoNames name match"}
        else:
            missing.append(g["name"])
    write_json(DATA / "gazetteer" / "coords.json", {"coords": out, "missing": missing})
    print(f"coordinates for {len(out)} of {len(gaz)} articles; missing {len(missing)}: {missing[:30]}")


if __name__ == "__main__":
    main()
