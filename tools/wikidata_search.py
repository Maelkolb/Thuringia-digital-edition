"""Look up Wikidata items (to verify QIDs - never guess them).

    python tools/wikidata_search.py "Heinrich Posthumus Reuß" "Kloster Cronschwitz"
    python tools/wikidata_search.py --lang en "Elster river"

Prints JSON lines with the top hits: id, label, description. Cached in
data/entities/_wikidata_cache.json.
"""
from __future__ import annotations

import argparse
import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path

CACHE = Path(__file__).resolve().parents[1] / "data" / "entities" / "_wikidata_cache.json"
UA = {"User-Agent": "reuss-edition/1.0 (scholarly digital edition; contact: edition maintainer)"}


def search(term: str, lang: str, cache: dict) -> list:
    key = f"{lang}:{term}"
    if key in cache:
        return cache[key]
    url = "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode(
        {"action": "wbsearchentities", "search": term, "language": lang, "uselang": lang, "format": "json", "limit": 5})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                d = json.loads(r.read().decode("utf-8"))
            break
        except Exception:  # noqa: BLE001
            time.sleep(2 * (attempt + 1))
    else:
        return [{"error": "request failed"}]
    hits = [{"id": h["id"], "label": h.get("label"), "description": h.get("description")} for h in d.get("search", [])]
    cache[key] = hits
    time.sleep(0.2)
    return hits


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("terms", nargs="+")
    ap.add_argument("--lang", default="de")
    a = ap.parse_args()
    try:  # several agents share the cache; tolerate a concurrent write
        cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    except (json.JSONDecodeError, OSError):
        cache = {}
    for t in a.terms:
        print(json.dumps({"term": t, "hits": search(t, a.lang, cache)}, ensure_ascii=False))
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    tmp = CACHE.with_suffix(f".{os.getpid()}.tmp")
    tmp.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, CACHE)


if __name__ == "__main__":
    main()
