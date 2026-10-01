# -*- coding: utf-8 -*-
import json, re, pathlib, importlib.util
here = pathlib.Path(__file__).parent
root = here.parents[3]
def load(name):
    spec = importlib.util.spec_from_file_location(name, here / f"{name}.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
pm = load("pages_meta"); gm = load("glossary_meta")
order = [str(p) for p in range(765, 826)]
have = {p["page"] for p in pm.PAGES}
assert have == set(order), (set(order) - have, have - set(order))
pages = sorted(pm.PAGES, key=lambda p: int(p["page"]))
texts = {p: (root / "data" / "text" / "pages" / f"{p}.txt").read_text(encoding="utf-8") for p in order}
gl = []
for g in gm.GLOSS:
    rx = re.compile(g["_rx"])
    pg = [p for p in order if rx.search(texts[p])]
    if not pg:
        print("NO PAGES for", g["term"])
        continue
    d = {k: v for k, v in g.items() if k != "_rx"}
    d["pages"] = pg
    if not d["variants"]:
        d.pop("variants")
    gl.append(d)
out = {"package": "G6", "pages": pages, "glossary": gl}
dst = root / "data" / "search" / "pages" / "G6.json"
dst.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(len(pages), "pages;", len(gl), "glossary terms ->", dst)
for g in gl: print(g["term"], len(g["pages"]), g["pages"][:6])
