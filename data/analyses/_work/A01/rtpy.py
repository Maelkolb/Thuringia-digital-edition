import json, subprocess, sys
SCR = r"C:\Users\totom\AppData\Local\Temp\claude\C--Users-totom\9d5e7ab8-c251-427e-83bd-b145b2d015af\scratchpad"
BASE = r"C:\Users\totom\Projects\reuss-edition\data\analyses"
def test(src_id, chart_idx, mutate, name="zz-test-a01"):
    a = json.load(open(f"{BASE}\{src_id}.json", encoding="utf-8"))
    a["id"] = name
    ch = a["charts"][chart_idx]
    ch["id"] = "c1"
    a["charts"] = [ch]
    mutate(ch["vegalite"])
    p = f"{SCR}\{name}.json"
    json.dump(a, open(p, "w", encoding="utf-8"), ensure_ascii=False)
    r = subprocess.run(["node", "rt.mjs", p], capture_output=True, text=True, encoding="utf-8")
    print(r.stdout, r.stderr[-600:])
