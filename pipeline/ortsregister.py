"""Parse Brückner's own Ortsregister (pp. 826-829) into structured entries.

Line forms (Bemerkung on p. 826: "W. bezeichnet Wüstung und a. G. außer
Gemeindeverband. Orte ohne Parenthese bezeichnen Gemeinden, dagegen Orte mit
Parenthese sind Bestandtheile der in der Parenthese eingeschlossenen Gemeinde"):

    Gera 428.
    Desse W. 489.
    Abfang (Kießling) 786.
    Hammermühle (Zollgrün, Hirschberg) 693. 809.
    Aergerniß s. Birkenhain.
    Fuchsmühle s. Hohenleuben, Kraftsdorf, Zschippern.

Output: data/registers/ortsregister.json
"""
from __future__ import annotations

import re

from common import DATA, PAGES_DIR, read_json, write_json

LINE = re.compile(
    r"^(?P<name>.+?)"
    r"(?P<w>\s+W\.)?"
    r"(?:\s+\((?P<parent>[^)]*)\))?"
    r"(?P<ag>\s+\(?a\.\s?G\.\)?)?"
    r"(?P<w2>\s+W\.)?"
    r"\s+(?P<pages>\d{3}\.(?:\s*\d{3}\.)*)\s*$"
)
SEE = re.compile(r"^(?P<name>.+?)\s+s\.\s+(?P<target>.+?)\.?$")


def lines_of_register() -> list[tuple[str, str, str]]:
    out = []
    for f in sorted(PAGES_DIR.glob("*.json")):
        p = read_json(f)
        if p["label"] not in {"826", "827", "828", "829"}:
            continue
        for b in p["blocks"]:
            if b["type"] == "table":
                # two printed columns -> read column 1 then column 2
                for col in range(b["n_cols"]):
                    for row in b["grid"]:
                        if col < len(row) and row[col].strip():
                            out.append((row[col].strip(), p["label"], b["id"]))
            elif b["type"] == "list":
                out += [(i["text"].strip(), p["label"], b["id"]) for i in b["items"]]
            elif b["type"] == "paragraph" and not b["text"].startswith("Bemerkung"):
                out += [(ln.strip(), p["label"], b["id"]) for ln in b["text"].split("\n") if ln.strip()]
    return out


def main() -> None:
    entries, unparsed = [], []
    for text, page, block in lines_of_register():
        text = text.replace("ſ", "s")
        m = SEE.match(text)
        if m and not re.search(r"\d{3}\.$", text):
            entries.append({"name": m.group("name").strip(), "see": [t.strip() for t in m.group("target").split(",")],
                            "register_page": page})
            continue
        m = LINE.match(text)
        if not m:
            unparsed.append({"text": text, "page": page, "block": block})
            continue
        parent = m.group("parent")
        entries.append({
            "name": m.group("name").strip().rstrip(","),
            "parents": [x.strip() for x in parent.split(",")] if parent else [],
            "wuestung": bool(m.group("w") or m.group("w2")),
            "ausser_gemeindeverband": bool(m.group("ag")),
            "gemeinde": not parent and not (m.group("w") or m.group("w2")),
            "pages": re.findall(r"\d{3}", m.group("pages")),
            "register_page": page,
        })
    write_json(DATA / "registers" / "ortsregister.json", {"source": "Brückner 1870, pp. 826-829", "entries": entries, "unparsed": unparsed})
    print(f"entries {len(entries)}  gemeinden {sum(e.get('gemeinde', False) for e in entries)}  "
          f"wüstungen {sum(e.get('wuestung', False) for e in entries)}  see-refs {sum('see' in e for e in entries)}  unparsed {len(unparsed)}")
    for u in unparsed[:40]:
        print("  ?", u["page"], u["text"])


if __name__ == "__main__":
    main()
