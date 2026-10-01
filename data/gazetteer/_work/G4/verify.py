import json, re, sys
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\tools")
import importlib.util
spec = importlib.util.spec_from_file_location("vg", r"C:\Users\totom\Projects\reuss-edition\tools\validate_gazetteer.py")
vg = importlib.util.module_from_spec(spec); spec.loader.exec_module(vg)
d = json.load(open(r"C:\Users\totom\Projects\reuss-edition\data\gazetteer\G4.json", encoding="utf-8"))
LS = {"Pf.":"Pferde","R.":"Rinder","Schf.":"Schafe","Schw.":"Schweine","Z.":"Ziegen","G.":"Gänse","Bnst.":"Bienenstöcke"}
for e in d["entries"]:
    t = vg.article_text(e["start"], e["end"])
    t = t.replace("\n"," ")
    msgs = []
    m = re.search(r"(\d+) Privathäuser", t)
    if m and int(m.group(1)) != e.get("houses"): msgs.append(f"houses text={m.group(1)} entry={e.get('houses')}")
    m = re.search(r"(\d[\d.]*)(?: \(\d{4}: \d+\))? (?:Einw\.|Seelen|Einwohner)", t)
    if m and int(m.group(1).replace('.','')) != e.get("inhabitants"): msgs.append(f"inh text={m.group(1)} entry={e.get('inhabitants')}")
    m = re.search(r"an Vieh((?:[^.]|(?<=Pf)\.|(?<=Schf)\.|(?<=Schw)\.|(?<=R)\.|(?<=Z)\.|(?<=G)\.|(?<=Bnst)\.|(?<=Es)\.|(?<=K)\.)*)", t)
    if m:
        seg = m.group(1)
        found = {}
        for n, ab in re.findall(r"(?:über )?(\d+) (Pf|R|Schf|Schw|Z|G|Bnst|K|Es)\.", seg):
            found[ab] = int(n)
        mp = {"Pf":"Pferde","R":"Rinder","Schf":"Schafe","Schw":"Schweine","Z":"Ziegen","G":"Gänse","Bnst":"Bienenstöcke"}
        lv = e.get("livestock", {})
        for ab, n in found.items():
            k = mp.get(ab)
            if k and lv.get(k) != n: msgs.append(f"livestock {k}: text={n} entry={lv.get(k)}")
        for k, v in lv.items():
            ab = [a for a, kk in mp.items() if kk == k]
            if ab and ab[0] not in found and k != "Esel": msgs.append(f"livestock {k}={v} not found in text")
    if msgs: print(e["id"], msgs)
print("done")

print("--- occupations/crafts check")
for e in d["entries"]:
    t = vg.article_text(e["start"], e["end"]).replace("\n"," ")
    miss = []
    for sec in ("occupations","crafts"):
        for k, n in e.get(sec, {}).items():
            # find "n word" or "..., n word, word and word" lists: accept if number n directly precedes key or key appears after a list start
            key = re.escape(k.split(" (")[0])
            if re.search(rf"(?<!\d){n} {key}", t): continue
            # list context "N A, B, C und D": key appears and number n appears within 90 chars before
            ok = False
            for mm in re.finditer(key, t):
                seg = t[max(0, mm.start()-110):mm.start()]
                if re.search(rf"(?<!\d){n} [A-ZÄÖÜ][a-zäöüß-]+", seg):
                    ok = True; break
            if not ok: miss.append(f"{k}={n}")
    if miss: print(e["id"], miss)
