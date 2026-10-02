"""Q01: one-off repair. fix_text.py first modernised bilingual nodes inside scale.domain / sort / range / values
of Vega-Lite specs, but those strings must stay identical to the data values (or to the string literals of
calculate expressions), so a changed domain entry made a colour/stack segment disappear. This script restores those
nodes from the pre-normalisation backup (scratchpad); fix_text.py now skips them (PROTECT_KEYS)."""
import glob, json, os, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
BACKUP = Path("C:/Users/totom/AppData/Local/Temp/claude/C--Users-totom/9d5e7ab8-c251-427e-83bd-b145b2d015af/scratchpad/q01/backup_before")
PROTECT = {"domain", "sort", "range", "values"}

def merge(cur, old, protected=False):
    if isinstance(cur, dict) and isinstance(old, dict):
        if set(cur) == {"de", "en"} and set(old) == {"de", "en"}:
            return old if protected else cur
        return {k: merge(v, old.get(k, v), protected or (k in PROTECT)) for k, v in cur.items()}
    if isinstance(cur, list) and isinstance(old, list) and len(cur) == len(old):
        return [merge(a, b, protected) for a, b in zip(cur, old)]
    return cur

n = 0
for f in sorted(glob.glob(str(ROOT / "data/analyses/*.json"))):
    name = os.path.basename(f)
    if name.startswith(("orte-", "ortskunde-")) or not (BACKUP / name).exists():
        continue
    cur = json.load(open(f, encoding="utf-8")); old = json.load(open(BACKUP / name, encoding="utf-8"))
    changed = False
    for c, o in zip(cur["charts"], old["charts"]):
        new = merge(c["vegalite"], o["vegalite"])
        if new != c["vegalite"]:
            c["vegalite"] = new; changed = True
    if changed:
        Path(f).write_text(json.dumps(cur, ensure_ascii=False, indent=1), encoding="utf-8"); n += 1; print("reverted domains in", name)
print(n, "files")
