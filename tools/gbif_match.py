"""Match scientific names against the GBIF backbone taxonomy.

    python tools/gbif_match.py "Alauda arvensis" "Fagus sylvatica" ...
    python tools/gbif_match.py --file names.txt         # one name per line

Prints JSON lines: name, usageKey, scientificName, rank, status, matchType,
confidence, kingdom, family. Results are cached in data/entities/_gbif_cache.json.
"""
from __future__ import annotations

import argparse
import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path

CACHE = Path(__file__).resolve().parents[1] / "data" / "entities" / "_gbif_cache.json"


def match(name: str, cache: dict) -> dict:
    if name in cache:
        return cache[name]
    url = "https://api.gbif.org/v1/species/match?" + urllib.parse.urlencode({"name": name, "verbose": "false"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                d = json.loads(r.read().decode("utf-8"))
            break
        except Exception:  # noqa: BLE001
            time.sleep(2 * (attempt + 1))
    else:
        return {"name": name, "error": "request failed"}
    out = {"name": name, "usageKey": d.get("usageKey"), "scientificName": d.get("scientificName"),
           "rank": d.get("rank"), "status": d.get("status"), "matchType": d.get("matchType"),
           "confidence": d.get("confidence"), "kingdom": d.get("kingdom"), "family": d.get("family"),
           "acceptedUsageKey": d.get("acceptedUsageKey")}
    cache[name] = out
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*")
    ap.add_argument("--file")
    a = ap.parse_args()
    names = list(a.names)
    if a.file:
        names += [ln.strip() for ln in Path(a.file).read_text(encoding="utf-8").splitlines() if ln.strip()]
    try:  # several agents share the cache; tolerate a concurrent write
        cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    except (json.JSONDecodeError, OSError):
        cache = {}
    for n in names:
        print(json.dumps(match(n, cache), ensure_ascii=False))
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        tmp = CACHE.with_suffix(f".{os.getpid()}.tmp")
        tmp.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
        os.replace(tmp, CACHE)


if __name__ == "__main__":
    main()
