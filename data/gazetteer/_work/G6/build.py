# -*- coding: utf-8 -*-
import json, sys, importlib.util, pathlib
here = pathlib.Path(__file__).parent
entries = []
for n in range(1, 6):
    spec = importlib.util.spec_from_file_location(f"part{n}", here / f"part{n}.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    entries += m.ENTRIES
def key(e):
    return (int(e["start"]["page"]), int(e["start"]["block"][1:]))
entries.sort(key=key)
out = {"package": "G6", "pages": "765-825", "entries": entries}
dst = here.parents[1] / "G6.json"
dst.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(len(entries), "entries ->", dst)
for e in entries:
    print(e["id"], e["start"], e["end"])
