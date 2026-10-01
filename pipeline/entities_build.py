"""Stage 4b - build the entity registry from candidates + adjudication decisions.

Decisions (data/entities/decisions/*.json, written by the E-subagents) win;
keys without a decision fall back to "accept as printed" in the default class
of their group, so the edition can be built at any time.

Entities are identified by (class, label): two keys accepted with the same
canonical label become one entry; homonyms with different authority ids stay
apart. Output:
    data/entities/registry.json   entities with forms, pages, authorities
    data/entities/key_map.json    (group, key) -> entity id | null (rejected)
"""
from __future__ import annotations

import collections
import json
import re
import unicodedata

from common import DATA, PAGES_DIR, read_json, write_json

GROUP_DEFAULT = {"places": "place", "nature": "nature", "persons": "person", "organisations": "organisation",
                 "organisms": "organism", "concepts": "concept"}
TYPE_GROUP = {"Location": "places", "Natural Object": "nature", "Person": "persons", "Organisation": "organisations",
              "Animal": "organisms", "Plant": "organisms", "Artefact": "concepts", "Resource": "concepts",
              "Environment": "concepts", "Climate": "concepts", "Environmental Impact": "concepts"}


def slug(s: str) -> str:
    s = s.lower().replace("ß", "ss").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
    s = "".join(ch for ch in unicodedata.normalize("NFD", s) if unicodedata.category(ch) != "Mn")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:60] or "x"


def load_decisions() -> dict[tuple[str, str], dict]:
    out = {}
    slices = read_json(DATA / "entities" / "slices.json") if (DATA / "entities" / "slices.json").exists() else {}
    for f in sorted((DATA / "entities" / "decisions").glob("*.json")):
        d = read_json(f)
        group = d.get("group") or slices.get(d.get("package"), {}).get("group")
        for x in d.get("decisions", []):
            out[(group, x["key"])] = x
    return out


def main() -> None:
    decisions = load_decisions()
    groups = {}
    for g in GROUP_DEFAULT:
        p = DATA / "entities" / "candidates" / f"{g}.json"
        groups[g] = {e["key"]: e for e in read_json(p)["entries"]}

    def resolve(group: str, key: str, depth: int = 0) -> dict | None:
        """Final decision for a key, following merge chains (also across groups)."""
        x = decisions.get((group, key))
        if x is None:
            return {"action": "accept", "label": key, "class": GROUP_DEFAULT[group], "_fallback": True}
        if x["action"] == "reject":
            return None
        if x["action"] == "merge" and depth < 6:
            tgt = x["into"]
            for g in [group] + [gg for gg in GROUP_DEFAULT if gg != group]:
                if (g, tgt) in decisions or tgt in groups[g]:
                    return resolve(g, tgt, depth + 1)
            return {"action": "accept", "label": tgt, "class": GROUP_DEFAULT[group]}
        return x

    entities: dict[str, dict] = {}
    key_map: dict[str, str | None] = {}
    by_label: dict[tuple[str, str], list[str]] = collections.defaultdict(list)
    for g, keys in groups.items():
        for key, cand in keys.items():
            d = resolve(g, key)
            if d is None:
                key_map[f"{g}\t{key}"] = None
                continue
            cls = d.get("class") or GROUP_DEFAULT[g]
            label = (d.get("label") or key).strip()
            auth = d.get("geonames") or d.get("wikidata") or d.get("gbif") or ""
            base = f"{cls}:{slug(label)}"
            # homonyms: same label, different authority -> separate ids
            eid = base
            existing = [e for e in by_label[(cls, slug(label))]]
            for e in existing:
                ea = entities[e]["_auth"]
                if not auth or not ea or ea == str(auth):
                    eid = e
                    break
            else:
                if existing:
                    eid = f"{base}-{len(existing) + 1}"
            if eid not in entities:
                entities[eid] = {"id": eid, "class": cls, "label": label, "kinds": collections.Counter(), "keys": [],
                                 "forms": collections.Counter(), "n": 0, "_auth": str(auth) if auth else "",
                                 "fallback": bool(d.get("_fallback"))}
                by_label[(cls, slug(label))].append(eid)
            e = entities[eid]
            e["keys"].append(f"{g}\t{key}")
            e["n"] += cand["n"]
            e["forms"].update(cand["forms"])
            if d.get("kind"):
                e["kinds"][d["kind"]] += cand["n"]
            if not d.get("_fallback"):
                e["fallback"] = False
            for fld in ("modern", "gloss_en", "description_de", "description_en", "note", "scientific", "rank",
                        "in_principality", "register_page"):
                if d.get(fld) not in (None, "") and fld not in e:
                    e[fld] = d[fld]
            for fld in ("geonames", "wikidata", "gbif"):
                if d.get(fld) and fld not in e:
                    e[fld] = d[fld]
            if d.get("lat") is not None and "coords" not in e:
                e["coords"] = [round(float(d["lat"]), 5), round(float(d["lon"]), 5)]
            key_map[f"{g}\t{key}"] = eid

    # pages per entity from the mention list
    pages_of = collections.defaultdict(list)
    with open(DATA / "entities" / "mentions.jsonl", encoding="utf-8") as f:
        for line in f:
            m = json.loads(line)
            eid = key_map.get(f"{TYPE_GROUP[m['type']]}\t{m['key']}")
            if eid and (not pages_of[eid] or pages_of[eid][-1] != m["page"]):
                pages_of[eid].append(m["page"])
    out = []
    for eid, e in entities.items():
        e["kind"] = e["kinds"].most_common(1)[0][0] if e["kinds"] else None
        e["forms"] = dict(e["forms"].most_common(12))
        e["pages"] = pages_of.get(eid, [])
        del e["kinds"], e["_auth"]
        out.append(e)
    out.sort(key=lambda e: (e["class"], e["label"].lower()))
    write_json(DATA / "entities" / "registry.json", {"entities": out}, indent=None)
    write_json(DATA / "entities" / "key_map.json", key_map, indent=None)
    cnt = collections.Counter(e["class"] for e in out)
    dec = sum(1 for e in out if not e["fallback"])
    print(f"entities {len(out)} ({dict(cnt)}); decided {dec}; rejected keys {sum(v is None for v in key_map.values())}; "
          f"decisions loaded {len(decisions)}")


if __name__ == "__main__":
    main()
