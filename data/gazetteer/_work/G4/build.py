import json, sys, importlib, os
sys.path.insert(0, os.path.dirname(__file__))
parts = sys.argv[1:] or ["p1","p2","p3","p4"]
entries = []
for p in parts:
    try:
        m = importlib.import_module(p)
    except ModuleNotFoundError:
        continue
    entries += m.ENTRIES
for e in entries:
    if "events" in e:
        e["events"] = sorted(e["events"], key=lambda x: x["year"])
out = {"package": "G4", "pages": "633-705", "entries": entries}
if os.path.exists(os.path.join(os.path.dirname(__file__), "issues.json")):
    out["transcription_issues"] = json.load(open(os.path.join(os.path.dirname(__file__), "issues.json"), encoding="utf-8"))
dst = r"C:\Users\totom\Projects\reuss-edition\data\gazetteer\G4.json"
json.dump(out, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(entries), "entries ->", dst)
