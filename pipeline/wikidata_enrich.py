"""Add Wikidata ids to places and natural features via their GeoNames id.

Wikidata items carry the GeoNames id in property P1566, so one SPARQL query
per batch maps our verified GeoNames choices to Wikidata items - no name
guessing. Ambiguous mappings (one GeoNames id -> several items) are skipped.
Output: data/entities/wikidata_by_geonames.json  {geonames id: {qid, label}}
"""
from __future__ import annotations

import glob
import json
import time
import urllib.parse
import urllib.request

from common import DATA, read_json, write_json

UA = {"User-Agent": "reuss-edition/1.0 (scholarly digital edition of Brückner 1870; batch GeoNames->Wikidata lookup)",
      "Accept": "application/sparql-results+json"}


def main() -> None:
    ids = set()
    for f in glob.glob(str(DATA / "entities" / "decisions" / "E*.json")):
        for x in read_json(f).get("decisions", []):
            if x.get("geonames"):
                ids.add(str(x["geonames"]))
    for f in glob.glob(str(DATA / "gazetteer" / "coords.json")):
        for c in read_json(f)["coords"].values():
            if c.get("geonames"):
                ids.add(str(c["geonames"]))
    out_path = DATA / "entities" / "wikidata_by_geonames.json"
    result = read_json(out_path) if out_path.exists() else {}
    result = {k: v for k, v in result.items() if v is not None or k.startswith("_")}  # retry earlier failures
    todo = sorted(i for i in ids if i not in result)
    print(f"{len(ids)} GeoNames ids, {len(todo)} to look up")
    found = {}
    for k in range(0, len(todo), 150):
        batch = todo[k:k + 150]
        q = ("SELECT ?item ?gn ?itemLabel WHERE { VALUES ?gn { " + " ".join(f'"{g}"' for g in batch) +
             " } ?item wdt:P1566 ?gn . SERVICE wikibase:label { bd:serviceParam wikibase:language \"de,en\". } }")
        url = "https://query.wikidata.org/sparql?" + urllib.parse.urlencode({"query": q, "format": "json"})
        for attempt in range(6):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                    data = json.loads(r.read().decode("utf-8"))
                break
            except Exception as e:  # noqa: BLE001
                print("  retry", attempt, e, flush=True)
                time.sleep(70)  # WDQS may throttle to 1 request / minute
        else:
            continue
        for b in data["results"]["bindings"]:
            gn = b["gn"]["value"]
            qid = b["item"]["value"].rsplit("/", 1)[1]
            found.setdefault(gn, []).append({"qid": qid, "label": b.get("itemLabel", {}).get("value")})
        for gn in batch:  # only answered batches are recorded
            hits = found.get(gn, [])
            result[gn] = hits[0] if len(hits) == 1 else ({"ambiguous": [h["qid"] for h in hits]} if hits else {"none": True})
        write_json(out_path, result)
        print(f"  batch {k // 150 + 1}: {sum(1 for g in batch if g in found)} of {len(batch)} found", flush=True)
        time.sleep(65)
    write_json(out_path, result)
    ok = sum(1 for v in result.values() if v and "qid" in v)
    print(f"mapped {ok} of {len(result)} GeoNames ids to Wikidata")


if __name__ == "__main__":
    main()
