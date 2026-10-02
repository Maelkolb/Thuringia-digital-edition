"""Collect facsimile-verified transcription corrections into data/corrections/verified.json.

Sources
* `transcription_issues` in data/analyses/*.json and data/gazetteer/*.json
  (written by the subagents, each with checked_facsimile = true/false)
* MANUAL below: issues reported in agent hand-backs (see agent_findings.md)

A correction is applied by normalize.py only if the transcribed string occurs
in the cited block (or on the page when no block is given) and the
replacement is unambiguous. Ambiguous or unchecked issues are reported but
not applied; they remain documented in the analyses / place articles.
"""
from __future__ import annotations

import json
import re

from common import DATA, PAGES_DIR, read_json, write_json

# page, find, replace, block (optional), source, note
MANUAL = [
    ("448", "Bollersdorf", "Vollersdorf", None, "G1", "Fraktur V/B; checked on the scan"),
    ("413", "Bollersdorf", "Vollersdorf", None, "G1", "same misreading as p. 448"),
    ("418", "Bollersdorf", "Vollersdorf", None, "G1", "same misreading as p. 448"),
    ("423", "Roschütz", "Roschitz", None, "G1", "checked on the scan"),
    ("602", "Dettersdorf", "Oettersdorf", None, "G3", "Fraktur Oe/De; checked on the scan"),
    ("604", "Dettersdorf", "Oettersdorf", None, "G3", "checked on the scan"),
    ("605", "Dettersdorf", "Oettersdorf", None, "G3", "checked on the scan"),
    ("574", "Dettersdorf", "Oettersdorf", None, "G3", "same misreading as pp. 602-605"),
    ("588", "Dettersdorf", "Oettersdorf", None, "G3", "same misreading as pp. 602-605"),
    ("606", "203 K.", "203 R.", None, "G3", "R. = Rinder; checked on the scan"),
    ("600", "17 Bust.", "17 Bnst.", None, "G3", "Bnst. = Bienenstöcke; checked on the scan"),
    ("645", "18 K.", "18 R.", None, "G4", "checked on the scan"),
    ("675", "8124 1/2", "8124 1/7", None, "G4", "checked on the scan"),
    ("492", "110 K.", "110 R.", None, "G2", "checked on the scan"),
    ("536", "Söllnitz", "Söllmnitz", "b2", "G2", "checked on the scan"),
    ("536", "Beizdorf", "Betzdorf", "b3", "G2", "checked on the scan"),
    ("536", "Beczelinsdorf", "Peczelinsdorf", "b3", "G2", "checked on the scan"),
    ("38", "Kammschnecke", "Kammerschnecke", "b1", "A02", "checked on the scan"),
    ("108", "4,103", "4,03", "b1", "A07", "checked on the scan"),
    ("832", "134,775", "134,75", "b8", "B01", "checked; reproduces the printed m³ value"),
    ("831", "zuversindenden statt zu verzindenden", "zuverzinsenden statt zu verzinsenden", "b5", "B01", "checked on the scan"),
    ("833", "ganz statt ganz", "ganz statt gauz", "b19", "B01", "the corrigendum quotes the misprint; checked on the scan"),
    ("394", "§", "H.", None, "A12", "printed 'H.' (Heinrich) in Tab. VII was read as '§'; checked on the scan"),
    ("479", "75 K.", "75 R.", "b3", "G1", "R. = Rinder; same misreading as pp. 492, 606, 645 (all checked)"),
    ("6", "27,154", "27,54", None, "A01", "spurious '1' after the decimal comma (Lobenstein); checked on the scan"),
    ("6", "28,105", "28,05", None, "A01", "spurious '1' (Bellevue); checked on the scan"),
    ("6", "6,127", "6,27", None, "A01", "spurious '1' (St. Gangloff); checked on the scan"),
    ("84", "Steinschmetzer", "Steinschmetter", None, "A05", "printed form (corrected by the author on p. 831 to Steinschmätzer); checked"),
    ("72", "Pulicaria dysenterica", "Palicaria dysenterica", None, "A05", "printed form (corrected by the author on p. 830); checked"),
    ("277", "Braumalzbesteuer", "Braumalzsteuer", "b1", "A11", "checked on the scan"),
    ("275", "sechstellige", "sechsellige", "b4", "A11", "checked on the scan"),
    ("332", "Würschengriin", "Würschengrün", "b3", "E2", "checked on the scan"),
    ("147", "Thründorf", "Thrändorf", "b3", "A08", "Fraktur ä/ü; checked on the scan"),
    ("7", "Rödersdorf", "Rüdersdorf", "b1", "land-lage-grenzen", "mill near Gera in the table of surveyed points; checked on the scan (b3 prints Rödersdorf near Schleiz)"),
    ("7", "Lohma", "Löhma", "b3", "land-lage-grenzen", "checked on the scan"),
    ("22", "Karolinensfeld", "Karolinenfeld", None, "relief-hoehen", "checked on the scan"),
    ("58", "Karolinensfeld", "Karolinenfeld", "b4", "relief-hoehen", "same misreading as p. 22"),
    ("47", "Bittera", "Wittera", "b4", "gewaesser", "Fraktur W/B; checked on the scan"),
    ("48", "Wioschwitz", "Moschwitz", "b4", "gewaesser", "checked on the scan"),
    ("299", "1,10", "1,40", "b3", "kirche-schule", "the print has 1,40, a misprint for 1,10 (117 : 106); the transcription had corrected it silently"),
]
SUBSCRIBER_FIXES = [("v. Boss", "v. Voß"), ("Weissker", "Weißker"), ("Weissendorf", "Weißendorf"), ("Meissner", "Meißner"),
                    ("Siekmann", "Sieckmann"), ("Mauke", "Maucke")]


def page_index():
    out = {}
    for f in PAGES_DIR.glob("*.json"):
        p = read_json(f)
        out[p["slug"]] = p
    return out


def block_text(p, bid):
    for b in p["blocks"] + p["footnotes"]:
        if b["id"] == bid:
            if b.get("grid"):
                return "\n".join(" | ".join(r) for r in b["grid"])
            if b.get("items"):
                return "\n".join(i["text"] for i in b["items"])
            return b.get("text", "")
    return None


def main() -> None:
    pages = page_index()
    out, skipped = [], []

    def add(page, find, repl, block, source, note, checked=True, force=False):
        p = pages.get(page)
        if not p:
            skipped.append((page, find, "unknown page"))
            return
        text = block_text(p, block) if block else "\n".join(block_text(p, b["id"]) or "" for b in p["blocks"] + p["footnotes"])
        if text is None:
            skipped.append((page, find, f"unknown block {block}"))
            return
        if find == repl or not find.strip():
            return
        n = text.count(find)
        if n == 0 and repl in text:
            return  # already corrected (normalize applied it before)
        if n == 0:
            skipped.append((page, find, "string not in transcription"))
            return
        if n > 1 and len(find) < 6 and not force:
            skipped.append((page, find, f"ambiguous ({n} occurrences)"))
            return
        out.append({"page": page, "find": find, "replace": repl, "block": block, "count": "all", "source": source,
                    "checked_facsimile": checked, "note": note})

    for page, find, repl, block, src, note in MANUAL:
        add(page, find, repl, block, src, note, force=True)
    for page in ("835", "836", "837", "838", "839", "840"):
        for find, repl in SUBSCRIBER_FIXES:
            p = pages.get(page)
            if p and any(find in (block_text(p, b["id"]) or "") for b in p["blocks"]):
                add(page, find, repl, None, "B01", "subscriber list; checked on the scan")
    for f in list((DATA / "analyses").glob("*.json")) + list((DATA / "analyses" / "_archive").glob("*.json")) + list((DATA / "gazetteer").glob("G*.json")):
        try:
            d = read_json(f)
        except json.JSONDecodeError:
            continue
        for t in d.get("transcription_issues", []) or []:
            if not t.get("checked_facsimile"):
                skipped.append((t.get("page"), t.get("transcribed"), f"unchecked ({f.stem})"))
                continue
            tr, fa = (t.get("transcribed") or "").strip(), (t.get("facsimile") or "").strip()
            if not tr or not fa or len(tr) > 80 or " / " in tr:
                skipped.append((t.get("page"), tr, f"not a simple replacement ({f.stem})"))
                continue
            if any(c["page"] == t.get("page") and c["find"] == tr for c in out):
                continue
            add(str(t.get("page")), tr, fa, t.get("block") if re.fullmatch(r"(b|fn)\d+", str(t.get("block") or "")) else None,
                f.stem, t.get("note", ""))
    # corrections applied in an earlier run no longer find their wrong form in data/pages: keep them
    previous = DATA / "corrections" / "verified.json"
    if previous.exists():
        have = {(c["page"], c["find"]) for c in out}
        for c in read_json(previous)["corrections"]:
            p = pages.get(c["page"])
            text = "\n".join(block_text(p, b["id"]) or "" for b in p["blocks"]) if p else ""
            if (c["page"], c["find"]) not in have and c["replace"] in text:
                out.append(c)
                have.add((c["page"], c["find"]))
    write_json(DATA / "corrections" / "verified.json", {"_doc": __doc__.strip().splitlines()[0], "corrections": out,
                                                        "not_applied": [{"page": a, "text": b, "reason": c} for a, b, c in skipped]})
    print(f"corrections: {len(out)} applied, {len(skipped)} not applied")
    for s in skipped[:40]:
        print("  -", s)


if __name__ == "__main__":
    main()
