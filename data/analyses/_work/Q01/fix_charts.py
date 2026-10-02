"""Q01: idempotent chart fixes found in the visual review of the preview PNGs (run after patch_misc.py).

Each entry: (analysis id, chart id, function(vegalite spec) -> spec).  Re-validate with
  node tools/validate_analysis.mjs data/analyses/<id>.json
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
AN = ROOT / "data" / "analyses"


def walk_dicts(n):
    if isinstance(n, dict):
        yield n
        for v in n.values():
            yield from walk_dicts(v)
    elif isinstance(n, list):
        for x in n:
            yield from walk_dicts(x)


def legend_top(spec):
    """design system: legends sit on top (no explicit orient)"""
    for d in walk_dicts(spec):
        lg = d.get("legend")
        if isinstance(lg, dict) and lg.get("orient") == "right":
            del lg["orient"]
    return spec


def legend_columns(n):
    def f(spec):
        for d in walk_dicts(spec):
            lg = d.get("legend")
            if isinstance(lg, dict) and d.get("field") and d.get("type") == "nominal":
                lg["columns"] = n
        return spec
    return f


def replace_format(old, new):
    def f(spec):
        for d in walk_dicts(spec):
            if d.get("format") == old:
                d["format"] = new
        return spec
    return f


def axis_label_limit(n):
    def f(spec):
        for d in walk_dicts(spec):
            ax = d.get("axis")
            if isinstance(ax, dict) and isinstance(ax.get("labelLimit"), int) and ax["labelLimit"] < n:
                ax["labelLimit"] = n
        return spec
    return f


def boxplot_tooltip(spec):
    m = spec.get("mark")
    if isinstance(m, dict) and m.get("type") == "boxplot" and "tooltip" not in m:
        m["tooltip"] = True
    return spec


FIXES = [
    ("bevoelkerung-sterblichkeit-1858-1867", "c4", legend_top),
    ("bevoelkerung-wanderung-1864-1867", "c1", legend_top),
    ("industrie-gewerbe-1864-einzelne-gewerbe", "c3", legend_columns(2)),
]
EXTRA = [
    ("verkehr-eisenbahn-geldinstitute-zeitleiste", "c2", replace_format(".4~f", ".1~f")),
    ("landwirtschaft-agrarreformen-1836-1868", "c3", axis_label_limit(340)),
    ("relief-erhebungen-hoechste-punkte", "c3", boxplot_tooltip),
    ("orte-sozialstruktur-doerfer-1867", "c1", legend_columns(2)),
]


def apply(extra_only=False):
    changed = set()
    for i, c, fn in FIXES + EXTRA:
        p = AN / f"{i}.json"
        d = json.load(open(p, encoding="utf-8"))
        for ch in d["charts"]:
            if ch["id"] == c:
                new = fn(json.loads(json.dumps(ch["vegalite"])))
                if new != ch["vegalite"]:
                    ch["vegalite"] = new
                    changed.add(i)
        if i in changed:
            p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    return sorted(changed)


if __name__ == "__main__":
    ch = apply()
    print("charts changed in:", ch)
