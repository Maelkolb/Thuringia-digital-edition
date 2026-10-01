# -*- coding: utf-8 -*-
import importlib.util, glob, json, os, re, sys

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(here, "..", "..", "..", ".."))
E, P, G = [], [], []
for f in sorted(glob.glob(os.path.join(here, "c[0-9][0-9].py"))):
    spec = importlib.util.spec_from_file_location(os.path.basename(f)[:-3], f)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    E += m.E
    P += m.P
    G += getattr(m, "G", [])

# merge glossary by term
seen = {}
for g in G:
    if g["term"] in seen:
        seen[g["term"]]["pages"] = sorted(set(seen[g["term"]]["pages"]) | set(g["pages"]), key=int)
    else:
        seen[g["term"]] = g
G = list(seen.values())

# recompute glossary page lists from the page texts (range 405-486)
PAT = {
    "Thlr.": [r"Thlr\.", "Thaler"],
    "Morgen": ["Morgen"],
    "Häusler": ["Häusler"],
    "Taglöhner": ["Taglöhner", "Taglohn"],
    "Gerichtsbarkeit": ["Gerichtsbarkeit", "Obergerichte", "Niedergerichte", "Erbgerichte"],
    "Amtsdorf": ["Amtsdorf", "Amtsdörfer", "Küchendorf", "Küchendörfer", "Mischdorf", "Mischdörfer"],
    "Decem": [r"decempflichtig", r"Decem[ ,.]", r"Rauchzehnt", r"den Zehnten"],
    "Wüstung": ["Wüstung", r"wüsten Orten"],
    "Pflege Langenberg": ["Pflege Langenberg", "Reichspflege"],
    "Erbkretschmar": [r"Erbkret\w*", "Erbschenke"],
    "Pertinenzstück": ["Pertinenz", "Grundstücksverband"],
    "Pferdebauer": ["Pferdebauer", "Kühbauer"],
}
pagetext = {}
for p in range(405, 487):
    txt = open(os.path.join(root, "data", "text", "pages", "%d.txt" % p), encoding="utf-8").read()
    lines = [ln for ln in txt.splitlines() if not ln.startswith("##### ")]
    pagetext[str(p)] = "\n".join(lines)
for g in G:
    pats = PAT.get(g["term"], [re.escape(g["term"])] + [re.escape(v) for v in g.get("variants", [])])
    rx = re.compile("|".join(pats), re.I)
    pages = [p for p in pagetext if rx.search(pagetext[p])]
    if not pages:
        print("WARNING glossary term without hit:", g["term"])
    else:
        g["pages"] = pages

out = {"package": "G1", "pages": "405-486", "entries": E}
json.dump(out, open(os.path.join(root, "data", "gazetteer", "G1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
meta = {"package": "G1", "pages": P, "glossary": G}
json.dump(meta, open(os.path.join(root, "data", "search", "pages", "G1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(len(E), "entries", len(P), "pages", len(G), "glossary")
