"""Validate a search-metadata package file.

    python tools/validate_search_meta.py data/search/pages/A07.json [--range 105-118]
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUBJECTS = {ln.strip() for ln in (ROOT / "docs" / "agents" / "subjects.txt").read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.startswith("#")}
KINDS = {"unit", "currency", "term", "office", "dialect", "institution"}
order = []
for f in sorted((ROOT / "data" / "pages").glob("*.json")):
    order.append(json.loads(f.read_text(encoding="utf-8"))["slug"])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--range", help="first-last page label expected, e.g. 105-118")
    a = ap.parse_args()
    d = json.loads(Path(a.file).read_text(encoding="utf-8"))
    errors, warnings = [], []
    seen = set()
    for i, p in enumerate(d.get("pages", [])):
        tag = f"page {p.get('page')}"
        if p.get("page") not in order:
            errors.append(f"{tag}: unknown page label")
        if p.get("page") in seen:
            errors.append(f"{tag}: duplicate")
        seen.add(p.get("page"))
        for k in ("summary_de", "summary_en", "keywords_de", "keywords_en", "subjects"):
            if k not in p:
                errors.append(f"{tag}: missing {k}")
        blank = p.get("summary_de") == "Leerseite"
        for k in ("summary_de", "summary_en"):
            v = p.get(k, "")
            if not blank and not (40 <= len(v) <= 500):
                warnings.append(f"{tag}: {k} length {len(v)}")
            if re.match(r"^(Diese Seite|Auf dieser Seite|This page|On this page)", v):
                warnings.append(f"{tag}: {k} starts with filler")
        if not blank and not (3 <= len(p.get("keywords_de", [])) <= 12):
            warnings.append(f"{tag}: keywords_de count {len(p.get('keywords_de', []))}")
        for s in p.get("subjects", []):
            if s.startswith("+"):
                continue
            if s not in SUBJECTS:
                errors.append(f"{tag}: subject {s!r} not in docs/agents/subjects.txt (prefix '+' to propose a new one)")
    if a.range:
        lo, hi = a.range.split("-")
        want = order[order.index(lo): order.index(hi) + 1]
        missing = [x for x in want if x not in seen]
        if missing:
            errors.append(f"missing pages: {missing[:20]}{' …' if len(missing) > 20 else ''}")
    for g in d.get("glossary", []):
        for k in ("term", "kind", "de", "en", "pages"):
            if k not in g:
                errors.append(f"glossary {g.get('term')}: missing {k}")
        if g.get("kind") not in KINDS:
            errors.append(f"glossary {g.get('term')}: kind {g.get('kind')!r} not in {sorted(KINDS)}")
    for w in warnings:
        print("  warn ", w)
    for e in errors:
        print("  ERROR", e)
    print(("OK" if not errors else "FAIL") + f"  {a.file}: {len(seen)} pages, {len(d.get('glossary', []))} glossary terms")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
