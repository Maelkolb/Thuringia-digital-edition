"""Align the detected print lines (data/lines/raw) with the edition's transcript.

Each line's rough Tesseract reading is located in the page's transcript (blocks, list items,
table rows, footnotes, running head) after folding both to lowercase letters and digits.
Result per page in data/lines/aligned/<seq>.json:

    lines:   n (body line number), box [x, y, w, h] in IIIF full-size pixels, unit, start, end,
             hy (line continues a hyphenated word), score
    regions: unit -> bounding box of its lines

    python tools/lines/align_lines.py [--seqs 9,215]
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

from rapidfuzz import fuzz

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "lines" / "raw"
OUT = ROOT / "data" / "lines" / "aligned"
PAGES = ROOT / "data" / "pages"

FOLD = str.maketrans({"ſ": "s", "ä": "a", "ö": "o", "ü": "u", "Ä": "a", "Ö": "o", "Ü": "u"})
HYPHEN_END = re.compile(r"[-⸗=¬]\s*$")
ACCEPT = 72


def fold_char(c: str) -> str:
    c = c.translate(FOLD).lower()
    if c == "ß":
        return "ss"
    return c if c.isalnum() and c.isascii() else ""


def fold(text: str) -> str:
    return "".join(fold_char(c) for c in text)


def units_of(page: dict) -> list[tuple[str, str]]:
    units = []
    head = " ".join(x for x in (page.get("running_header"), page.get("label")) if x)
    if head:
        units.append(("head", head))
    for b in page["blocks"]:
        if b["type"] in ("paragraph", "heading"):
            units.append((b["id"], b["text"]))
        elif b["type"] == "list":
            units += [(f"{b['id']}.i{k}", item["text"]) for k, item in enumerate(b["items"])]
        elif b["type"] == "table":
            if b.get("caption"):
                units.append((f"{b['id']}.cap", b["caption"]))
            units += [(f"{b['id']}.r{k}", " ".join(c["text"] for c in row["cells"])) for k, row in enumerate(b["rows"])]
    for fn in page.get("footnotes", []):
        units.append((fn["id"], fn["text"]))
    if page.get("signature"):
        units.append(("sig", page["signature"]))
    return units


class Target:
    """The folded transcript of a page with a map back to (unit, character offset)."""

    def __init__(self, units: list[tuple[str, str]]):
        chars, self.unit_at, self.offset_at = [], [], []
        for ui, (_, text) in enumerate(units):
            for k, c in enumerate(text):
                for f in fold_char(c):
                    chars.append(f)
                    self.unit_at.append(ui)
                    self.offset_at.append(k)
        self.text = "".join(chars)
        self.units = units


def locate_short(query: str, target: Target) -> tuple[int, int, float]:
    """Page numbers and signature marks: only within the running head or the signature."""
    allowed = {i for i, (u, _) in enumerate(target.units) if u in ("head", "sig")}
    positions = [i for i, u in enumerate(target.unit_at) if u in allowed]
    if not positions:
        return -1, -1, 0.0
    segment = "".join(target.text[i] for i in positions)
    k = segment.find(query)
    if k < 0:
        return -1, -1, 0.0
    return positions[k], positions[k + len(query) - 1] + 1, 100.0


def increasing(items: list[dict]) -> list[dict]:
    """Longest run of lines whose start offsets increase in reading order (drops misplaced matches)."""
    best, prev = [1] * len(items), [-1] * len(items)
    for i in range(len(items)):
        for j in range(i):
            if items[j]["start"] < items[i]["start"] and best[j] + 1 > best[i]:
                best[i], prev[i] = best[j] + 1, j
    i = max(range(len(items)), key=lambda k: best[k], default=-1)
    keep = []
    while i >= 0:
        keep.append(items[i])
        i = prev[i]
    return keep[::-1]


def locate(query: str, target: Target, cursor: int) -> tuple[int, int, float]:
    if len(query) < 6:
        return locate_short(query, target)
    window_start = max(0, cursor - 60)
    window = target.text[window_start: cursor + 3 * len(query) + 400]
    best = fuzz.partial_ratio_alignment(query, window)
    if best and best.score >= ACCEPT:
        return window_start + best.dest_start, window_start + best.dest_end, best.score
    best = fuzz.partial_ratio_alignment(query, target.text)
    if best and best.score >= ACCEPT:
        return best.dest_start, best.dest_end, best.score
    return -1, -1, best.score if best else 0.0


def refine_start(query: str, target: Target, start: int) -> int:
    probe = query[:12]
    candidates = range(max(0, start - 6), min(len(target.text), start + 7))
    return max(candidates, key=lambda s: (fuzz.ratio(probe, target.text[s:s + len(probe)]), -abs(s - start)))


def snap_to_word(text: str, offset: int) -> int:
    if offset <= 0 or not text[offset - 1].isalnum():
        return offset
    for d in range(1, 4):
        if offset - d >= 0 and (offset - d == 0 or not text[offset - d - 1].isalnum()):
            return offset - d
        if offset + d < len(text) and not text[offset + d - 1].isalnum():
            return offset + d
    return offset


def display_box(line: dict, spacing: float) -> list[int]:
    xs = [p[0] for p in line["polygon"]]
    ys = [p[1] for p in line["polygon"]]
    base = statistics.median(p[1] for p in line["baseline"]) if line["baseline"] else max(ys)
    top = max(min(ys), base - 0.78 * spacing)
    bottom = min(max(ys), base + 0.24 * spacing)
    return [min(xs), round(top), max(xs) - min(xs), round(bottom - top)]


def table_lines(page: dict, units: list, lines: list, matched: list, spacing: float) -> list[dict]:
    """Detected lines inside a table (mostly short numeric cells) belong to the table's region.

    They are placed by position: below the last matched line of what precedes the table and above
    the first matched line of what follows it.
    """
    order = {u: i for i, (u, _) in enumerate(units)}
    used = {l["id"] for l in matched}
    extra = []
    for b in page["blocks"]:
        if b["type"] != "table":
            continue
        own = [i for u, i in order.items() if u.split(".")[0] == b["id"]]
        if not own:
            continue
        first, last = min(own), max(own)
        before = [l["box"][1] + l["box"][3] for l in matched if order.get(l["unit"], -1) < first and l["unit"] not in ("head", "sig")]
        after = [l["box"][1] for l in matched if order.get(l["unit"], -1) > last and l["unit"] != "sig"]
        top = max(before) if before else 0
        bottom = min(after) if after else float("inf")
        for line in lines:
            if line["id"] in used or not line["baseline"]:
                continue
            base = statistics.median(p[1] for p in line["baseline"])
            if top < base < bottom:
                extra.append({"id": line["id"], "box": display_box(line, spacing), "unit": b["id"], "start": None, "end": None,
                              "hy": False, "score": 0.0, "table": True})
                used.add(line["id"])
    return extra


def align_page(page: dict, raw: dict) -> dict:
    units = units_of(page)
    target = Target(units)
    lines = sorted(raw["lines"], key=lambda l: (statistics.median(p[1] for p in l["baseline"]) if l["baseline"] else l["box"][1], l["box"][0]))
    bases = [statistics.median(p[1] for p in l["baseline"]) for l in lines if l["baseline"]]
    gaps = [b - a for a, b in zip(bases, bases[1:]) if 25 < b - a < 90]
    spacing = statistics.median(gaps) if gaps else 48.0

    out, cursor, prev_hyphen, last_offset = [], 0, False, {}
    for line in lines:
        query = fold(line["ocr"])
        if len(query) < 2 and not (query.isdigit() and query == fold(page.get("label") or "")):
            prev_hyphen = False
            continue
        start, end, score = locate(query, target, cursor)
        if start < 0:
            prev_hyphen = False
            continue
        start = refine_start(query, target, start)
        end = max(end, start + 1)
        unit_idx = statistics.mode(target.unit_at[start:end])
        uid, text = units[unit_idx]
        positions = [i for i in range(start, end) if target.unit_at[i] == unit_idx]
        offset, offset_end = target.offset_at[positions[0]], target.offset_at[positions[-1]] + 1
        continues_word = prev_hyphen and offset > 0 and text[offset - 1].isalnum()
        if not continues_word:
            offset = snap_to_word(text, offset)
        if end > cursor and score >= 85:
            cursor = end
        out.append({"id": line["id"], "box": display_box(line, spacing), "unit": uid, "start": offset, "end": offset_end,
                    "hy": continues_word, "score": round(score, 1)})
        prev_hyphen = bool(HYPHEN_END.search(line["ocr"]))

    by_unit: dict[str, list[dict]] = {}
    for l in out:
        by_unit.setdefault(l["unit"], []).append(l)
    out = [l for group in by_unit.values() for l in (increasing(group) if group[0]["start"] is not None else group)]
    out += table_lines(page, units, lines, out, spacing)
    out.sort(key=lambda l: (l["box"][1], l["box"][0]))
    n = 0
    for l in out:
        if l["unit"] in ("head", "sig") or l.get("table"):
            l["n"] = None
        else:
            n += 1
            l["n"] = n
    regions = {}
    for l in out:
        block = l["unit"].split(".")[0]
        x, y, w, h = l["box"]
        r = regions.setdefault(block, [x, y, x + w, y + h])
        regions[block] = [min(r[0], x), min(r[1], y), max(r[2], x + w), max(r[3], y + h)]
    regions = {k: [a, b, c - a, d - b] for k, (a, b, c, d) in regions.items()}
    text_units = {u for u, _ in units if "." not in u or ".i" in u}
    unit_text = dict(units)
    covered = sum(len(fold(unit_text[l["unit"]][l["start"]:l["end"]])) for l in out if l["unit"] in text_units and not l.get("table"))
    total = sum(len(fold(t)) for u, t in units if u in text_units and u not in ("head", "sig"))
    return {"seq": page["seq"], "width": raw["width"], "height": raw["height"], "spacing": round(spacing, 1),
            "detected": len(raw["lines"]), "lines": out, "regions": regions,
            "coverage": round(min(1.0, covered / total), 3) if total else 1.0}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seqs", default="")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    files = [RAW / f"{int(s):04d}.json" for s in args.seqs.split(",")] if args.seqs else sorted(RAW.glob("*.json"))
    stats = []
    for f in files:
        page = json.loads((PAGES / f.name).read_text(encoding="utf-8"))
        if page["kind"] != "text":
            continue
        result = align_page(page, json.loads(f.read_text(encoding="utf-8")))
        (OUT / f.name).write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
        stats.append((f.stem, result["detected"], len(result["lines"]), result["coverage"]))
    if stats and not args.seqs:
        summary = {"pages": len(stats), "detected": sum(s[1] for s in stats), "aligned": sum(s[2] for s in stats),
                   "median_coverage": statistics.median(s[3] for s in stats), "pages_below_85": sum(1 for s in stats if s[3] < 0.85)}
        (OUT.parent / "summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    if stats:
        low = [s for s in stats if s[3] < 0.85]
        print(f"{len(stats)} pages; lines aligned {sum(s[2] for s in stats)}/{sum(s[1] for s in stats)}; "
              f"median coverage {statistics.median(s[3] for s in stats):.3f}; pages below 85 %: {len(low)}")
        for s in sorted(low, key=lambda s: s[3])[:15]:
            print("   ", s)


if __name__ == "__main__":
    sys.exit(main())
