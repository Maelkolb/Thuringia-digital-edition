import json, glob, sys
root = r"C:\Users\totom\Projects\reuss-edition\data\gazetteer"
entries = []
for f in sorted(glob.glob(root + r"\_work\G2\part*.json")):
    entries += json.load(open(f, encoding="utf-8"))
issues = json.load(open(root + r"\_work\G2\issues.json", encoding="utf-8")) if __import__("os").path.exists(root + r"\_work\G2\issues.json") else []
out = {"package": "G2", "pages": "487-569", "entries": entries, "transcription_issues": issues}
json.dump(out, open(root + r"\G2.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(entries), "entries")
