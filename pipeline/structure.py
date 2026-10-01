"""Stage 2 - resolve the book structure onto pages and blocks.

* every TOC section gets an exact start (scan + block) by matching its title
  against the headings on its start page
* chapter V (history) gets its sub-sections from the numbered headings
* every block gets the id of the innermost section it belongs to
* every heading gets a level: section heads by depth, other headings one
  below the innermost section

Writes data/structure/structure.json and updates data/pages/*.json in place.
"""
from __future__ import annotations

import difflib
import re

from common import DATA, PAGES_DIR, read_json, write_json


def words(s: str) -> list[str]:
    s = s.lower().replace("ue", "ü") if False else s.lower()
    return [w for w in re.findall(r"[a-zäöüß]{3,}", s)]


def similarity(a: str, b: str) -> float:
    wa, wb = set(words(a)), set(words(b))
    if not wa or not wb:
        return 0.0
    overlap = len(wa & wb) / min(len(wa), len(wb))
    ratio = difflib.SequenceMatcher(None, " ".join(words(a)), " ".join(words(b))).ratio()
    return max(overlap, ratio)


def main() -> None:
    pages = [read_json(f) for f in sorted(PAGES_DIR.glob("*.json"))]
    by_slug = {p["slug"]: p for p in pages}
    order = [p["seq"] for p in pages]
    toc = read_json(DATA / "structure" / "toc.json")

    flat: list[dict] = []

    def resolve(sec: dict, depth: int, parent: str | None) -> dict:
        start_page = by_slug[sec["start"]]
        end_page = by_slug[sec["end"]]
        node = {k: sec[k] for k in ("id", "title", "title_en") if k in sec}
        if "num" in sec:
            node["num"] = sec["num"]
        node.update({"depth": depth, "parent": parent, "start_seq": start_page["seq"], "end_seq": end_page["seq"],
                     "start_label": sec["start"], "end_label": sec["end"]})
        # find the heading that opens the section on its start page
        full = f"{sec.get('num', '')} {sec['title']}"
        best, best_score = None, 0.0
        for b in start_page["blocks"]:
            if b["type"] != "heading":
                continue
            sc = similarity(b["text"], sec["title"])
            if sc > best_score:
                best, best_score = b, sc
        if best is not None and best_score >= 0.6:
            node["start_block"] = best["id"]
            best.setdefault("opens", []).append(sec["id"])
        elif sec.get("num") and any(b["type"] == "paragraph" and re.match(re.escape(sec["num"][0]) + r"[.)]\s", b["text"]) for b in start_page["blocks"]):
            # run-in head: "c) Gemeindeverfassung. An die Stelle ..."
            b = next(b for b in start_page["blocks"] if b["type"] == "paragraph" and re.match(re.escape(sec["num"][0]) + r"[.)]\s", b["text"]))
            node["start_block"] = b["id"]
            m = re.match(r"^([a-zA-Z0-9]+[.)]\s+(?:[^.]{0,60}\.)?)", b["text"])
            title_hit = m and similarity(m.group(1), sec["title"]) >= 0.6
            b["runin"] = len(m.group(1)) if title_hit else len(re.match(r"^\S+", b["text"]).group(0))
            b.setdefault("opens", []).append(sec["id"])
            best_score = 1.0
        else:
            node["start_block"] = None  # section starts at the top of the page / heading not transcribed
        node["match_score"] = round(best_score, 2)
        flat.append(node)
        kids = []
        for ch in sec.get("children", []):
            kids.append(resolve(ch, depth + 1, sec["id"]))
        if sec.get("auto_children"):
            kids.extend(auto_children(node, pages, depth + 1, sec["id"]))
        node["children"] = [k["id"] for k in kids]
        return node

    def auto_children(node: dict, pages: list[dict], depth: int, parent: str) -> list[dict]:
        out = []
        n = 0
        for p in pages:
            if not (node["start_seq"] <= p["seq"] <= node["end_seq"]):
                continue
            for b in p["blocks"]:
                if b["type"] == "heading" and re.match(r"^\d+\.\s+\S", b["text"]) and "Tab." not in b["text"][:6]:
                    n += 1
                    title = re.sub(r"^\d+\.\s+", "", b["text"]).strip().rstrip(".")
                    child = {"id": f"{parent}-{n}", "num": b["text"].split()[0], "title": title, "depth": depth,
                             "parent": parent, "start_seq": p["seq"], "start_label": p["slug"], "start_block": b["id"],
                             "auto": True, "children": []}
                    b.setdefault("opens", []).append(child["id"])
                    out.append(child)
        for a, b in zip(out, out[1:]):
            a["end_seq"] = b["start_seq"]
        if out:
            out[-1]["end_seq"] = node["end_seq"]
        for c in out:
            c["end_label"] = next(p["slug"] for p in pages if p["seq"] == c["end_seq"])
        flat.extend(out)
        return out

    roots = [resolve(s, 1, None) for s in toc["sections"]]

    # section membership: walk all blocks in reading order ------------------
    starts = []  # (seq, block_index or -1, depth, id)
    for node in flat:
        p = next(p for p in pages if p["seq"] == node["start_seq"])
        idx = -1
        if node.get("start_block"):
            idx = next(i for i, b in enumerate(p["blocks"]) if b["id"] == node["start_block"])
        starts.append((node["start_seq"], idx, node["depth"], node["id"]))
    starts.sort()
    by_id = {n["id"]: n for n in flat}
    stack: list[str] = []
    si = 0
    for p in pages:
        page_secs = []
        for i in range(-1, len(p["blocks"])):
            while si < len(starts) and (starts[si][0], starts[si][1]) <= (p["seq"], i):
                _, _, depth, sid = starts[si]
                stack = [s for s in stack if by_id[s]["depth"] < depth]
                stack.append(sid)
                si += 1
            if i == -1:
                p["section_path"] = list(stack)
                continue
            b = p["blocks"][i]
            b["sec"] = stack[-1] if stack else None
            if b["sec"] not in page_secs:
                page_secs.append(b["sec"])
            if b["type"] == "heading":
                if b.get("opens"):
                    b["level"] = min(6, max(by_id[s]["depth"] for s in b["opens"]) + 1)
                else:
                    cur = by_id[stack[-1]]["depth"] if stack else 1
                    b["level"] = min(6, cur + 2)
        p["sections"] = page_secs
    for p in pages:
        write_json(PAGES_DIR / f"{p['seq']:04d}.json", p)
    write_json(DATA / "structure" / "structure.json", {"roots": [r["id"] for r in roots], "sections": flat})
    weak = [(n["id"], n["start_label"], n["match_score"]) for n in flat if not n.get("start_block") and not n.get("auto")]
    print(f"sections: {len(flat)}  unmatched start headings: {len(weak)}")
    for w in weak:
        print("  no heading match:", w)


if __name__ == "__main__":
    main()
