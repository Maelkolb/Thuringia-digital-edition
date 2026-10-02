"""Shared base layers for map charts in the analyses (data/analyses/_shared).

    base_places.json   every place of the principality with coordinates, Landestheil and type
    base_rivers.json   simplified courses of the main rivers (OpenStreetMap, ODbL; Weiße Elster from Natural Earth)

Both are written in the analysis dataset format, ready to copy into an analysis's
"datasets" and to use as "extra_datasets" of a map chart. Coordinates are derived
(GeoNames, OpenStreetMap), so the columns carry "derived": true.

    python tools/analysis_base_layers.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = DATA / "analyses" / "_shared"
BBOX = (11.40, 50.30, 12.35, 51.00)  # lon/lat extent of the principality with a margin


def read(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def section_start(section_id: str) -> str:
    sec = next(s for s in read(DATA / "structure" / "structure.json")["sections"] if s["id"] == section_id)
    return sec["start_label"]


def places() -> dict:
    coords = read(DATA / "gazetteer" / "coords.json")["coords"]
    rows, seen = [], set()
    for f in sorted((DATA / "gazetteer").glob("G*.json")):
        for g in read(f)["entries"]:
            c = coords.get(g["id"])
            if not c or g.get("wuestung"):
                continue
            lat, lon = (c["lat"], c["lon"]) if isinstance(c, dict) else c
            rows.append([g["name"], round(lon, 5), round(lat, 5), g.get("landestheil"), g.get("type"), True])
            seen.add(g["name"])
    for e in read(DATA / "entities" / "registry.json")["entities"]:
        if e["class"] == "place" and e.get("coords") and e.get("in_principality") and e["label"] not in seen:
            rows.append([e["label"], round(e["coords"][1], 5), round(e["coords"][0], 5), None, e.get("kind"), False])
            seen.add(e["label"])
    rows.sort(key=lambda r: r[0])
    return {
        "name": "orte_basis",
        "title": {"de": "Orte des Fürstentums mit Koordinaten (Kartengrundlage)", "en": "Places of the principality with coordinates (base map)"},
        "columns": [
            {"name": "ort", "label": {"de": "Ort", "en": "Place"}, "type": "string"},
            {"name": "lon", "label": {"de": "Länge", "en": "Longitude"}, "type": "number", "unit": "°", "derived": True, "note": "GeoNames"},
            {"name": "lat", "label": {"de": "Breite", "en": "Latitude"}, "type": "number", "unit": "°", "derived": True, "note": "GeoNames"},
            {"name": "landestheil", "label": {"de": "Landesteil", "en": "District"}, "type": "string"},
            {"name": "typ", "label": {"de": "Typ", "en": "Type"}, "type": "string"},
            {"name": "ortsartikel", "label": {"de": "Eigener Ortsartikel", "en": "Own place article"}, "type": "string", "derived": True},
        ],
        "rows": [r[:5] + ["ja" if r[5] else "nein"] for r in rows],
        "source_refs": [{"page": "826", "block": "b3", "note": "Ortsregister; Koordinaten aus GeoNames"}],
    }


def rivers() -> dict | None:
    files = [OUT / "rivers_osm.json", OUT / "rivers_elster.json"]
    ways = []
    for f in files:
        try:
            ways += read(f)["elements"]
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            continue
    if not ways:
        return None
    rows = []
    inside = lambda p: BBOX[0] <= p["lon"] <= BBOX[2] and BBOX[1] <= p["lat"] <= BBOX[3]  # noqa: E731
    for k, w in enumerate(ways):
        name = w.get("tags", {}).get("name") or "Weiße Elster"
        pts = w.get("geometry", [])
        step = max(1, len(pts) // 25)
        keep = pts[::step] + ([pts[-1]] if pts and (len(pts) - 1) % step else [])
        runs, run = [], []
        for p in keep:
            if inside(p):
                run.append(p)
            elif run:
                runs.append(run)
                run = []
        runs.append(run)
        for j, run in enumerate(r for r in runs if len(r) >= 2):
            for i, p in enumerate(run):
                rows.append([name, f"{name}-{k}-{j}", i, round(p["lon"], 4), round(p["lat"], 4)])
    return {
        "name": "fluesse_basis",
        "title": {"de": "Flussläufe (Kartengrundlage, OpenStreetMap)", "en": "River courses (base map, OpenStreetMap)"},
        "columns": [
            {"name": "fluss", "label": {"de": "Fluss", "en": "River"}, "type": "string"},
            {"name": "abschnitt", "label": {"de": "Abschnitt", "en": "Segment"}, "type": "string", "derived": True},
            {"name": "folge", "label": {"de": "Folge", "en": "Order"}, "type": "integer", "derived": True},
            {"name": "lon", "label": {"de": "Länge", "en": "Longitude"}, "type": "number", "unit": "°", "derived": True, "note": "© OpenStreetMap-Mitwirkende, ODbL; Weiße Elster: Natural Earth"},
            {"name": "lat", "label": {"de": "Breite", "en": "Latitude"}, "type": "number", "unit": "°", "derived": True, "note": "© OpenStreetMap-Mitwirkende, ODbL; Weiße Elster: Natural Earth"},
        ],
        "rows": rows,
        "source_refs": [{"page": section_start("t1-1-6"), "block": "b1", "note": "Gewässer; Geometrie © OpenStreetMap-Mitwirkende (ODbL), Weiße Elster nach Natural Earth (gemeinfrei)"}],
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    p = places()
    (OUT / "base_places.json").write_text(json.dumps(p, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"base_places: {len(p['rows'])} places, {sum(1 for r in p['rows'] if r[3])} with Landestheil")
    r = rivers()
    if r:
        (OUT / "base_rivers.json").write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"base_rivers: {len(r['rows'])} points, rivers {sorted({x[0] for x in r['rows']})}")


if __name__ == "__main__":
    main()
