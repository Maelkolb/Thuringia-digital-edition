# -*- coding: utf-8 -*-
"""Builds data/search/pages/A11.json from meta_pages.py and meta_glossary.py (glossary page lists computed from the page texts)."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from meta_pages import PAGES
from meta_glossary import G

ROOT = Path(__file__).resolve().parents[3].parent
texts = {}
for p in range(263, 311):
    texts[str(p)] = (ROOT / "data" / "text" / "pages" / f"{p}.txt").read_text(encoding="utf-8")
EXCLUDE = {"Contingent": ("302",), "Helm": ("272",)}
pages_out = []
seen = set()
for page, sde, sen, kde, ken, subj in PAGES:
    assert page not in seen, page
    seen.add(page)
    pages_out.append({"page": page, "summary_de": sde, "summary_en": sen, "keywords_de": kde, "keywords_en": ken, "subjects": subj})
assert seen == {str(p) for p in range(263, 311)}, sorted({str(p) for p in range(263, 311)} - seen)
glossary = []
for term, variants, kind, de, en, patterns in G:
    pages = []
    for p in range(263, 311):
        t = texts[str(p)]
        if any(re.search(pt, t) for pt in patterns):
            pages.append(str(p))
    if not pages:
        print("NO PAGES for", term)
        continue
    pages = [p for p in pages if p not in EXCLUDE.get(term, ())]
    glossary.append({"term": term, "variants": variants, "kind": kind, "de": de, "en": en, "pages": pages})
out = {"package": "A11", "pages": pages_out, "glossary": glossary}
dst = ROOT / "data" / "search" / "pages" / "A11.json"
dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(dst, len(pages_out), len(glossary))
for g in glossary:
    print(g["term"], g["pages"])
