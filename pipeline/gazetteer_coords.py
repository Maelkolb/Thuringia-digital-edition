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
    # pass 1: index decisions whose Brückner register page is this article's page (or no conflicting page)
    for g in gaz:
        if g.get("type") in ("Landestheil", "Sonstiges"):
            continue
        d = decisions.get(match_key(g["name"]))
        pages = {g["start"]["page"], g["end"]["page"]}
        if d and (not d.get("register_page") or str(d["register_page"]) in pages or d.get("in_principality") is False):
            if d.get("register_page") and str(d["register_page"]) not in pages:
                continue
            out[g["id"]] = {"lat": d["lat"], "lon": d["lon"], "geonames": d.get("geonames"), "source": "entity decision"}
    # district centroids from pass 1 -> plausibility check for name matches
    import statistics
    cent = {}
    for lt in {g["landestheil"] for g in gaz}:
        pts = [out[g["id"]] for g in gaz if g["landestheil"] == lt and g["id"] in out]
        if pts:
            cent[lt] = (statistics.median(p["lat"] for p in pts), statistics.median(p["lon"] for p in pts))

    def dist_km(a, b):
        return ((a[0] - b[0]) * 111.2) ** 2 + ((a[1] - b[1]) * 111.2 * 0.64) ** 2

    for g in gaz:
        if g.get("type") in ("Landestheil", "Sonstiges") or g["id"] in out:
            continue
        cs = cands.get(match_key(g["name"]), [])
        c0 = cent.get(g["landestheil"])
        ok = [c for c in cs if c0 and dist_km((c["lat"], c["lon"]), c0) ** 0.5 <= 22]
        ok = [c for c in ok if c["class"] == "P"] or ok
        if len(ok) >= 1:
            c = min(ok, key=lambda c: dist_km((c["lat"], c["lon"]), c0))
            out[g["id"]] = {"lat": c["lat"], "lon": c["lon"], "geonames": c["geonames"], "source": "GeoNames name match within district"}
        else:
            missing.append(g["name"])
    write_json(DATA / "gazetteer" / "coords.json", {"coords": out, "missing": missing})
    print(f"coordinates for {len(out)} of {len(gaz)} articles; missing {len(missing)}: {missing[:30]}")


if __name__ == "__main__":
    main()
