"""Stage 3 - plain-text views of the canonical pages for reading by humans and
subagents. Every line carries a citable id (page label + block id, table rows
r1..rn), so derived work can point back to the exact source.

data/text/pages/<slug>.txt      one file per page
data/text/sections/<id>.txt     all pages of a top-level chapter, in order
data/text/plain.txt             the whole book, reading text only
"""
from __future__ import annotations

from common import DATA, PAGES_DIR, read_json, write_text_atomic

OUT = DATA / "text"


def render_page(p: dict, sections: dict) -> str:
    sec = " > ".join(f"{sections[s].get('num', '')} {sections[s]['title']}".strip() for s in p.get("section_path", []) if s in sections)
    head = f"##### PAGE {p['label'] or p['slug']} | scan {p['seq']} | {sec or '-'}"
    if p.get("running_header"):
        head += f" | running header: {p['running_header']}"
    lines = [head]
    if p["kind"] != "text":
        lines.append(f"[{p['kind']} page]")
    for b in p["blocks"]:
        tag = b["id"]
        if b["type"] == "heading":
            lines.append(f"[{tag} H{b.get('level', '')}] {b['text']}")
        elif b["type"] == "paragraph":
            flags = []
            if b.get("continued"):
                flags.append("continued from previous page")
            if b.get("continues"):
                flags.append("continues on next page")
            f = f" ({'; '.join(flags)})" if flags else ""
            lines.append(f"[{tag} P{f}] {b['text']}")
        elif b["type"] == "list":
            lines.append(f"[{tag} LIST]")
            for i, it in enumerate(b["items"], 1):
                lines.append(f"  - i{i}: {it['text']}")
        elif b["type"] == "table":
            cap = f" caption: {b['caption']}" if b.get("caption") else ""
            lines.append(f"[{tag} TABLE {len(b['grid'])} rows x {b['n_cols']} cols, header_rows={b['header_rows']}{cap}]")
            for i, row in enumerate(b["grid"], 1):
                role = b["rows"][i - 1]["role"]
                mark = {"header": "h", "group": "g", "total": "t"}.get(role, "r")
                lines.append(f"  {mark}{i} | " + " | ".join(c.replace("\n", " ") for c in row))
    for fn in p["footnotes"]:
        lines.append(f"[{fn['id']} FOOTNOTE {fn['marker']}] {fn['text']}")
    if p.get("signature"):
        lines.append(f"[signature mark: {p['signature']}]")
    return "\n".join(lines) + "\n"


def main() -> None:
    pages = [read_json(f) for f in sorted(PAGES_DIR.glob("*.json"))]
    struct = read_json(DATA / "structure" / "structure.json")
    sections = {s["id"]: s for s in struct["sections"]}
    (OUT / "pages").mkdir(parents=True, exist_ok=True)
    (OUT / "sections").mkdir(parents=True, exist_ok=True)
    rendered = {}
    for p in pages:
        txt = render_page(p, sections)
        rendered[p["seq"]] = txt
        write_text_atomic(OUT / "pages" / f"{p['slug']}.txt", txt)
    for s in struct["sections"]:
        if s["depth"] > 2 and not s["id"].startswith("t1-5"):
            continue
        body = [rendered[p["seq"]] for p in pages if s["start_seq"] <= p["seq"] <= s["end_seq"]]
        write_text_atomic(OUT / "sections" / f"{s['id']}.txt", "\n".join(body))
    plain = []
    for p in pages:
        for b in p["blocks"]:
            if b["type"] in ("heading", "paragraph"):
                plain.append(b["text"])
    write_text_atomic(OUT / "plain.txt", "\n\n".join(plain))
    print("pages:", len(pages))


if __name__ == "__main__":
    main()
