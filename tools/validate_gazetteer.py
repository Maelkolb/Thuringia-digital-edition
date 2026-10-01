"""Validate a gazetteer package file (task type G).

    python tools/validate_gazetteer.py data/gazetteer/G1.json
"""
from __future__ import annotations

import json
import re
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TYPES = {"Stadt", "Marktflecken", "Dorf", "Weiler", "Rittergut", "Kammergut", "Vorwerk", "Mühle", "Einzelhof",
         "Wüstung", "Schloss", "Gewerbeanlage", "Landestheil", "Sonstiges"}
DIRS = re.compile(r"^(N|O|S|W|NO|NW|SO|SW|NNO|ONO|OSO|SSO|SSW|WSW|WNW|NNW)$")
LANDESTHEILE = {"Gera", "Schleiz", "Lobenstein-Ebersdorf"}
ALLOWED = {"id", "name", "start", "end", "landestheil", "type_verbatim", "type", "wuestung", "historic_forms",
           "dialect_form", "first_mention_year", "location", "elevation", "parish", "school", "houses",
           "inhabitants", "census_year", "occupations", "crafts", "flur_morgen", "flur_verbatim", "soil",
           "livestock", "municipal_finances", "facilities", "subplaces", "events", "persons", "summary_de",
           "summary_en", "notes"}

pages = {}
order = []
for f in sorted((ROOT / "data" / "pages").glob("*.json")):
    p = json.loads(f.read_text(encoding="utf-8"))
    pages[p["slug"]] = p
    order.append(p["slug"])


def block_text(b: dict) -> str:
    if b["type"] == "table":
        return "\n".join(" | ".join(r) for r in b["grid"])
    if b["type"] == "list":
        return "\n".join(i["text"] for i in b["items"])
    return b["text"]


def article_text(start: dict, end: dict) -> str | None:
    try:
        i0, i1 = order.index(start["page"]), order.index(end["page"])
    except ValueError:
        return None
    out, on = [], False
    for slug in order[i0:i1 + 1]:
        for b in pages[slug]["blocks"] + pages[slug]["footnotes"]:
            if slug == start["page"] and b["id"] == start["block"]:
                on = True
            if on:
                out.append(block_text(b) if "type" in b else b["text"])
            if slug == end["page"] and b["id"] == end["block"]:
                return "\n".join(out)
    return "\n".join(out) if out else None


FRAC = {"½": Fraction(1, 2), "¼": Fraction(1, 4), "¾": Fraction(3, 4), "⅓": Fraction(1, 3), "⅔": Fraction(2, 3), "⅛": Fraction(1, 8)}


def numbers(text: str) -> set[float]:
    s = set()
    for m in re.finditer(r"(\d+(?:[.,]\d+)?)(?:\s+(\d+)/(\d+)|\s?([½¼¾⅓⅔⅛]))?", text):
        base = float(m.group(1).replace(",", "."))
        s.add(round(base, 2))
        if re.fullmatch(r"\d{1,3}(?:[.,]\d{3})+", m.group(1)):
            s.add(float(re.sub(r"[.,]", "", m.group(1))))
        if m.group(2):
            s.add(round(base + int(m.group(2)) / int(m.group(3)), 2))
        if m.group(4):
            s.add(round(base + float(FRAC[m.group(4)]), 2))
    for m in re.finditer(r"(?<!\d)(\d+)/(\d+)", text):
        s.add(round(int(m.group(1)) / int(m.group(2)), 2))
    for ch, v in FRAC.items():
        if ch in text:
            s.add(round(float(v), 2))
    return s


def walk_numbers(obj, path=""):
    if isinstance(obj, bool):
        return
    if isinstance(obj, (int, float)):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("year", "first_mention_year", "census_year") or k.endswith("_verbatim") or k == "verbatim":
                if k in ("year", "first_mention_year", "census_year") and isinstance(v, int):
                    yield f"{path}.{k}", v
                continue
            yield from walk_numbers(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_numbers(v, f"{path}[{i}]")


def main(path: str) -> int:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    errors, warnings = [], []
    ids = set()
    for k in ("package", "pages", "entries"):
        if k not in d:
            errors.append(f"missing top-level key {k}")
    for i, e in enumerate(d.get("entries", [])):
        tag = f"entry {i} ({e.get('id')})"
        extra = set(e) - ALLOWED
        if extra:
            errors.append(f"{tag}: unknown keys {sorted(extra)}")
        for k in ("id", "name", "start", "end", "landestheil", "type", "summary_de", "summary_en"):
            if k not in e:
                errors.append(f"{tag}: missing {k}")
        if e.get("id") in ids:
            errors.append(f"{tag}: duplicate id")
        ids.add(e.get("id"))
        if e.get("id") and not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", e["id"]):
            errors.append(f"{tag}: id must be an ascii slug")
        if e.get("type") not in TYPES:
            errors.append(f"{tag}: type {e.get('type')!r} not in {sorted(TYPES)}")
        if e.get("landestheil") not in LANDESTHEILE:
            errors.append(f"{tag}: landestheil must be one of {sorted(LANDESTHEILE)}")
        loc = e.get("location") or {}
        if loc.get("direction") and not DIRS.match(loc["direction"]):
            errors.append(f"{tag}: direction {loc['direction']!r}")
        for v in (e.get("historic_forms") or []):
            if set(v) - {"form", "year"}:
                errors.append(f"{tag}: historic_forms items take only form/year")
        if "start" in e and "end" in e:
            txt = article_text(e["start"], e["end"])
            if txt is None:
                errors.append(f"{tag}: start/end block not found or end before start")
                continue
            if e["name"].split()[0][:4] not in txt[:400] and not e.get("type") == "Landestheil":
                warnings.append(f"{tag}: name {e['name']!r} not near the start of the article")
            nums = numbers(txt)
            miss = [f"{p}={v}" for p, v in walk_numbers(e) if round(float(v), 2) not in nums]
            if miss:
                (errors if len(miss) > 2 else warnings).append(f"{tag}: numbers not in article text: {miss[:8]}")
        for k in ("summary_de", "summary_en"):
            if k in e and not (30 <= len(e[k]) <= 600):
                warnings.append(f"{tag}: {k} length {len(e[k])}")
    for w in warnings:
        print("  warn ", w)
    for er in errors:
        print("  ERROR", er)
    print(("OK" if not errors else "FAIL") + f"  {path}: {len(d.get('entries', []))} entries, {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
