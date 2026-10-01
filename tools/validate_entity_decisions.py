"""Validate an entity-decision package (task type E).

    python tools/validate_entity_decisions.py data/entities/decisions/E1.json
The slice of keys a package must cover is read from data/entities/slices.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLASSES = {"place", "nature", "person", "organisation", "organism", "concept"}
ACTIONS = {"accept", "merge", "reclass", "reject"}
FIELDS = {"key", "action", "label", "class", "kind", "geonames", "lat", "lon", "wikidata", "in_principality",
          "register_page", "gloss_en", "modern", "into", "reason", "note", "scientific", "gbif", "rank",
          "description_de", "description_en"}


def main(path: str) -> int:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    pkg = d.get("package")
    slices = json.loads((ROOT / "data" / "entities" / "slices.json").read_text(encoding="utf-8"))
    if pkg not in slices:
        print(f"FAIL unknown package {pkg!r}")
        return 1
    sl = slices[pkg]
    cands = json.loads((ROOT / "data" / "entities" / "candidates" / f"{sl['group']}.json").read_text(encoding="utf-8"))["entries"]
    all_keys = {e["key"] for e in cands}
    want = set(sl["keys"])
    errors, warnings = [], []
    seen = {}
    for i, x in enumerate(d.get("decisions", [])):
        k = x.get("key")
        tag = f"decision {i} ({k!r})"
        if set(x) - FIELDS:
            errors.append(f"{tag}: unknown fields {sorted(set(x) - FIELDS)}")
        if k in seen:
            errors.append(f"{tag}: duplicate key")
        seen[k] = x
        a = x.get("action")
        if a not in ACTIONS:
            errors.append(f"{tag}: action {a!r}")
            continue
        if a in ("accept", "reclass"):
            if not x.get("label"):
                errors.append(f"{tag}: label required")
            if x.get("class") not in CLASSES:
                errors.append(f"{tag}: class must be one of {sorted(CLASSES)}")
        if a == "merge" and not x.get("into"):
            errors.append(f"{tag}: merge needs 'into'")
        if a == "reject" and not x.get("reason"):
            warnings.append(f"{tag}: reject without reason")
        if ("lat" in x) != ("lon" in x):
            errors.append(f"{tag}: lat and lon go together")
        if "lat" in x and not (-90 <= float(x["lat"]) <= 90 and -180 <= float(x["lon"]) <= 180):
            errors.append(f"{tag}: coordinates out of range")
        if x.get("wikidata") and not str(x["wikidata"]).startswith("Q"):
            errors.append(f"{tag}: wikidata must be a Q-id")
    for k, x in seen.items():
        if x.get("action") == "merge":
            tgt = x["into"]
            if tgt not in seen and tgt not in all_keys:
                errors.append(f"merge {k!r} -> {tgt!r}: target is neither decided here nor a candidate key")
            elif tgt in seen and seen[tgt].get("action") in ("merge", "reject"):
                errors.append(f"merge {k!r} -> {tgt!r}: target is itself {seen[tgt]['action']}d")
    missing = sorted(want - set(seen))
    if missing:
        errors.append(f"{len(missing)} keys of your slice without decision, e.g. {missing[:10]}")
    extra = sorted(set(seen) - want - all_keys)
    if extra:
        warnings.append(f"{len(extra)} decisions for keys not in the candidates, e.g. {extra[:5]}")
    for w in warnings[:30]:
        print("  warn ", w)
    for e in errors[:60]:
        print("  ERROR", e)
    acts = {}
    for x in seen.values():
        acts[x.get("action")] = acts.get(x.get("action"), 0) + 1
    print(("OK" if not errors else "FAIL") + f"  {path}: {len(seen)}/{len(want)} keys decided {acts}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
