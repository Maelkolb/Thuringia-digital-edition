"""Stage 1 - turn the raw Gemini page JSON into canonical page records.

No text is re-extracted. Everything here is deterministic and logged:

* unify the two raw schemas (``content_blocks`` vs. the early
  ``body_paragraphs``/``tables`` of pp. 44 and 53)
* page identity from the BSB IIIF manifest (scan sequence, printed label,
  image service), never from the model's page-number guess
* printer's signature marks ("27*", "35*") that the model read as page
  numbers or footnotes -> ``signature``
* running headers: dropped where they merely duplicate the opening heading
* line-break hyphens inside a line ("Som- merberg") -> joined
* tables: padded, empty columns dropped, multi-row headers detected and
  rebuilt with colspan/rowspan from the model's ``None`` placeholders,
  single-label rows -> group rows, split stub labels re-joined
* paragraph continuation and word division across page breaks
* entities re-anchored to the exact text unit (paragraph, table cell,
  list item, footnote) - the model's character offsets are wrong for 88 %
  of mentions, so the context string and the claimed offset are used to
  pick the right occurrence.

Output: data/pages/<seq>.json + data/reports/normalize_report.json
"""
from __future__ import annotations

import collections
import glob
import re
import unicodedata
from dataclasses import dataclass, field

from common import DATA, IIIF_CANVAS, IIIF_IMAGE, PAGES_DIR, SOURCE, is_filler, is_numeric, page_slug, read_json, write_json

MANUAL = DATA / "corrections" / "manual.json"
VERIFIED_FILE = DATA / "corrections" / "verified.json"
VERIFIED: dict[str, list] = {}
DOT_LEADER = re.compile(r"\s*(?:\.\s){3,}\.?\s*$|\s*\.{4,}\s*$")


# ---------------------------------------------------------------------------
# loading
# ---------------------------------------------------------------------------

def seq_of(rec: dict) -> int:
    if "seq" in rec:
        return int(rec["seq"])
    m = re.search(r"seq_(\d+)", rec["image_filename"])
    return int(m.group(1))


def load_raw() -> dict[int, dict]:
    raw: dict[int, dict] = {}
    files = glob.glob(str(SOURCE / "json_batch1" / "*.json")) + glob.glob(str(SOURCE / "json_batch2" / "*.json"))
    for f in files:
        rec = read_json(f)
        rec["_source"] = "colab-2026-01" if "json_batch1" in f else "colab-2026-03"
        raw[seq_of(rec)] = rec
    for f in sorted(glob.glob(str(DATA / "raw_fill" / "seq_*.json"))):
        rec = read_json(f)
        rec["_source"] = "gapfill-2026-10"
        raw[seq_of(rec)] = rec  # gap fills replace empty originals (pp. 527, 739)
    for rec in raw.values():
        st = rec["structure"]
        if "content_blocks" not in st:  # early schema
            blocks = [{"block_type": "paragraph", "content": p} for p in st.pop("body_paragraphs", [])]
            blocks += [{"block_type": "table", "content": t} for t in st.pop("tables", [])]
            st["content_blocks"] = blocks
            rec["_early_schema"] = True
        for i, b in enumerate(st["content_blocks"]):
            b.setdefault("block_index", i)
    return raw


def load_manifest() -> dict[int, dict]:
    m = read_json(SOURCE / "bsb_manifest.json")
    out = {}
    for i, c in enumerate(m["sequences"][0]["canvases"], start=1):
        lab = c["label"]
        mm = re.match(r"^(\S+)\s+\(\d+\)$", lab)
        out[i] = {"label": mm.group(1) if mm else None, "width": c["width"], "height": c["height"]}
    return out


# ---------------------------------------------------------------------------
# text units with entity spans and offset-preserving edits
# ---------------------------------------------------------------------------

@dataclass
class Unit:
    """A text unit = the smallest piece the OCR text was built from."""
    text: str
    spans: list = field(default_factory=list)  # [start, end, type]

    def edit(self, start: int, end: int, repl: str) -> None:
        delta = len(repl) - (end - start)
        self.text = self.text[:start] + repl + self.text[end:]
        new = []
        for s, e, t in self.spans:
            if e <= start:
                new.append([s, e, t])
            elif s >= end:
                new.append([s + delta, e + delta, t])
            else:  # span overlaps the edit: stretch / shrink it
                new.append([min(s, start), max(e + delta, start + len(repl)) if e > start else e, t])
        self.spans = new


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


# ---------------------------------------------------------------------------
# entity anchoring
# ---------------------------------------------------------------------------

def find_all(hay: str, needle: str) -> list[int]:
    out, i = [], hay.find(needle)
    while i >= 0:
        out.append(i)
        i = hay.find(needle, i + 1)
    return out


def ws_squash(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def anchor_entities(ocr_text: str, seg_offsets: list[tuple[int, int, Unit]], entities: list[dict], stats: collections.Counter) -> None:
    """Attach each NER mention to the text unit that contains it."""
    used: set[tuple[int, int]] = set()
    for ent in sorted(entities, key=lambda e: e.get("start_char", 0)):
        txt = nfc(ent.get("text") or "").strip()
        etype = ent.get("entity_type")
        if not txt or not etype:
            stats["entity_empty"] += 1
            continue
        occ = find_all(ocr_text, txt)
        if not occ:
            # tolerate whitespace differences (line breaks inside names)
            pat = re.escape(ws_squash(txt)).replace(r"\ ", r"\s+")
            occ = [m.start() for m in re.finditer(pat, ocr_text)]
            if occ:
                stats["entity_ws_match"] += 1
        if not occ:
            stats["entity_unmatched"] += 1
            continue
        ctx = ws_squash(nfc(ent.get("context") or ""))
        claimed = int(ent.get("start_char") or 0)

        def score(o: int) -> tuple:
            window = ws_squash(ocr_text[max(0, o - 80): o + len(txt) + 80])
            ctx_hit = 1 if ctx and ctx in window else 0
            # partial context: count context words present around the hit
            words = [w for w in re.findall(r"\w+", ctx) if len(w) > 2]
            near = sum(1 for w in words if w in window)
            return ((o, o + len(txt)) not in used, ctx_hit, near, -abs(o - claimed))

        best = max(occ, key=score)
        if (best, best + len(txt)) in used:
            stats["entity_duplicate"] += 1
            continue
        used.add((best, best + len(txt)))
        for start, end, unit in seg_offsets:
            if start <= best and best + len(txt) <= end:
                unit.spans.append([best - start, best - start + len(txt), etype])
                stats["entity_anchored"] += 1
                stats["entity_offset_was_exact"] += int(best == claimed)
                break
        else:
            stats["entity_crosses_units"] += 1


# ---------------------------------------------------------------------------
# tables
# ---------------------------------------------------------------------------

TOTAL_ROW = re.compile(r"^(Summa|Summe|Sa\.|Zusammen|Zus\.|Durchschn|Im Ganzen|Ueberhaupt|Überhaupt|Total|Mittel)", re.I)


def row_numeric_frac(row: list) -> float:
    vals = [c for c in row if c is not None and str(c).strip() and not is_filler(str(c))]
    if not vals:
        return 0.0
    return sum(is_numeric(str(c)) for c in vals) / len(vals)


def build_table(content: dict, cell_units: dict, log: list) -> dict:
    """Rebuild a table with header rows, spans and row roles.

    ``cell_units`` maps (row, col) of the raw grid to the Unit carrying text + spans.
    """
    raw = content.get("cells") or []
    width = max((len(r) for r in raw), default=0)
    grid = [[(r[j] if j < len(r) else None) for j in range(width)] for r in raw]
    if any(len(r) != width for r in raw):
        log.append({"rule": "table_pad_ragged_rows"})
    # drop columns that are empty everywhere
    keep = [j for j in range(width) if any(grid[i][j] not in (None, "") for i in range(len(grid)))]
    if len(keep) < width:
        log.append({"rule": "table_drop_empty_columns", "dropped": [j for j in range(width) if j not in keep]})
    colmap = {j: k for k, j in enumerate(keep)}
    grid = [[row[j] for j in keep] for row in grid]
    ncols = len(keep)
    nrows = len(grid)

    # header rows -------------------------------------------------------
    fracs = [row_numeric_frac(r) for r in grid]
    lower = fracs[nrows // 2:] or fracs
    body_numeric = sorted(lower)[len(lower) // 2] if lower else 0
    header_rows = 0
    if nrows >= 2:
        if body_numeric >= 0.4:
            for i in range(min(5, nrows - 1)):
                if fracs[i] < 0.25:
                    header_rows += 1
                else:
                    break
        else:
            first = [str(c).strip() for c in grid[0] if c not in (None, "")]
            later_digits = sum(1 for r in grid[1:] if any(re.search(r"\d", str(c or "")) for c in r))
            if first and all(not re.search(r"\d", c) and len(c) <= 40 for c in first) and later_digits >= (nrows - 1) / 2:
                header_rows = 1
    if header_rows == 0:
        log.append({"rule": "table_no_header_row", "note": "first row is data (legacy edition rendered it as <th>)"})
    elif header_rows > 1:
        log.append({"rule": "table_multirow_header", "rows": header_rows})

    covered = [[False] * ncols for _ in range(nrows)]
    rows_out = []
    # stub labels split over two rows ("Lobenst.-" / "Ebersd.", "Fürsten-" / "thum")
    stub_join: dict[int, int] = {}
    for i in range(header_rows, nrows - 1):
        a, b = grid[i][0], grid[i + 1][0]
        if isinstance(a, str) and isinstance(b, str) and a.rstrip().endswith("-") and b.strip() and not is_numeric(b):
            stub_join[i] = i + 1
    for i in range(nrows):
        role = "header" if i < header_rows else "body"
        nonempty = [j for j in range(ncols) if grid[i][j] not in (None, "")]
        if role == "body" and ncols >= 3 and len(nonempty) == 1 and not is_numeric(str(grid[i][nonempty[0]])):
            role = "group"
        elif role == "body" and nonempty and TOTAL_ROW.match(str(grid[i][nonempty[0]]).strip()):
            role = "total"
        cells = []
        for j in range(ncols):
            if covered[i][j]:
                continue
            val = grid[i][j]
            orig = (i, keep[j])
            unit = cell_units.get(orig) or Unit("" if val is None else str(val))
            colspan = rowspan = 1
            if role == "group":
                if j != 0:
                    continue
                k = nonempty[0]
                unit = cell_units.get((i, keep[k])) or Unit(str(grid[i][k]))
                colspan = ncols
                for jj in range(ncols):
                    covered[i][jj] = True
            elif role == "header" and val is not None:
                # extend right over None placeholders
                jj = j + 1
                while jj < ncols and grid[i][jj] is None and not covered[i][jj]:
                    jj += 1
                colspan = jj - j
                # extend down over None placeholders inside the header block
                ii = i + 1
                while ii < header_rows and all(grid[ii][x] is None for x in range(j, j + colspan)):
                    ii += 1
                rowspan = ii - i
                for r in range(i, i + rowspan):
                    for c in range(j, j + colspan):
                        covered[r][c] = True
            elif j == 0 and i in stub_join:
                nxt = cell_units.get((i + 1, keep[0])) or Unit(str(grid[i + 1][0]))
                joined = Unit(unit.text, [list(s) for s in unit.spans])
                left = joined.text.rstrip()
                if nxt.text[:1].islower():
                    joined.text = left[:-1]
                    off = len(joined.text)
                else:
                    joined.text = left
                    off = len(joined.text)
                joined.text += nxt.text
                joined.spans += [[s + off, e + off, t] for s, e, t in nxt.spans]
                unit = joined
                rowspan = 2
                covered[i + 1][0] = True
                log.append({"rule": "table_join_split_stub", "text": joined.text})
            cell = {"text": unit.text, "spans": unit.spans}
            if colspan > 1:
                cell["colspan"] = colspan
            if rowspan > 1:
                cell["rowspan"] = rowspan
            if val is None and role != "group":
                cell["empty"] = True
            cells.append(cell)
            covered[i][j] = True
        rows_out.append({"role": role, "cells": cells})
    if any(r["role"] == "group" for r in rows_out):
        log.append({"rule": "table_group_rows", "n": sum(r["role"] == "group" for r in rows_out)})
    plain = [["" if c is None else str(c) for c in r] for r in grid]
    return {"n_cols": ncols, "header_rows": header_rows, "rows": rows_out, "grid": plain,
            "caption": content.get("caption") or None}


# ---------------------------------------------------------------------------
# paragraph-level fixes
# ---------------------------------------------------------------------------

NO_JOIN_NEXT = {"und", "od", "oder", "mit", "bis", "sowie", "wie", "als", "resp", "u", "nebst", "noch", "beziehungsweise", "bezw", "theils", "zum", "zur"}
LINEBREAK_HYPHEN = re.compile(r"(?<=[A-Za-zÄÖÜäöüß])[-¬]\s+(?=([a-zäöüß][\wäöüß]*))")


VOCAB: set[str] = set()
INWORD_HYPHEN = re.compile(r"(?<![\w-])([A-ZÄÖÜa-zäöüß][a-zäöüß]+)-([a-zäöüß]{2,})(?![\w-])")


def build_vocab(raw: dict) -> None:
    for rec in raw.values():
        VOCAB.update(w.lower() for w in re.findall(r"[A-Za-zÄÖÜäöüß]{4,}", rec.get("ocr_text") or ""))


def dehyphenate(unit: Unit, log: list) -> None:
    # a) hyphen kept inside a word without the line break: join only when the
    #    joined form is attested elsewhere in the book ("Ge-setze" -> "Gesetze",
    #    but "reußisch-plauisch" stays)
    for m in reversed(list(INWORD_HYPHEN.finditer(unit.text))):
        joined = m.group(1) + m.group(2)
        if joined.lower() in VOCAB:
            unit.edit(m.start(1) + len(m.group(1)), m.start(2), "")
            log.append({"rule": "join_inword_hyphen", "before": m.group(0), "after": joined})
    while True:
        for m in LINEBREAK_HYPHEN.finditer(unit.text):
            nxt = m.group(1)
            if nxt.rstrip(".") in NO_JOIN_NEXT:
                continue
            if len(nxt) <= 2 and unit.text[m.end() + len(nxt): m.end() + len(nxt) + 1] == ".":
                continue  # abbreviation ("Spittel- d. i. Spitalacker")
            before = unit.text[max(0, m.start() - 12): m.end() + len(nxt)]
            unit.edit(m.start(), m.end(), "")
            log.append({"rule": "join_linebreak_hyphen", "before": before.strip(), "after": unit.text[max(0, m.start() - 12): m.start() + len(nxt)].strip()})
            break
        else:
            return


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

SIGNATURE = re.compile(r"^\d{1,2}\*{0,2}$")


def norm_cmp(s: str | None) -> str:
    return re.sub(r"[\W_]+", "", (s or "").lower())


def normalize_page(seq: int, rec: dict | None, canvas: dict, manual: dict, stats: collections.Counter) -> dict:
    label = canvas["label"]
    page = {
        "seq": seq,
        "label": label,
        "slug": page_slug(label, seq),
        "iiif": {"service": IIIF_IMAGE.format(seq=seq), "canvas": IIIF_CANVAS.format(seq=seq),
                 "width": canvas["width"], "height": canvas["height"]},
        "kind": "text",
        "running_header": None,
        "signature": None,
        "blocks": [],
        "footnotes": [],
        "corrections": [],
        "provenance": None,
    }
    log = page["corrections"]
    override = manual.get(str(seq), {})
    if rec is None or not rec["structure"]["content_blocks"] or override.get("kind") == "blank":
        page["kind"] = override.get("kind", "blank")
        if rec is not None and rec["structure"]["content_blocks"] and override.get("kind") == "blank":
            log.append({"rule": "manual_blank", "reason": override.get("reason")})
        if rec is not None:
            page["provenance"] = {"source": rec["_source"], "model": rec.get("model_used"), "timestamp": rec.get("processing_timestamp")}
        return page
    if override.get("kind"):
        page["kind"] = override["kind"]
    st = rec["structure"]
    if override.get("insert_blocks"):
        blocks = st["content_blocks"]
        nxt = max((b["block_index"] for b in blocks), default=-1) + 1
        for ins in override["insert_blocks"]:
            nb = dict(ins["block"], block_index=nxt, _inserted=True)
            pos = next((i + 1 for i, b in enumerate(blocks) if b["block_index"] == ins["after_block_index"]), len(blocks))
            blocks.insert(pos, nb)
            log.append({"rule": "manual_insert_block", "block": f"b{nxt + 1}", "reason": override.get("reason")})
            nxt += 1
    page["provenance"] = {"source": rec["_source"], "model": rec.get("model_used"), "timestamp": rec.get("processing_timestamp"),
                          "early_schema": bool(rec.get("_early_schema"))}

    # rebuild the exact OCR text the NER saw, unit by unit ----------------
    units_order: list[tuple[str, object, Unit]] = []
    if st.get("header"):
        units_order.append(("header", None, Unit(nfc(st["header"]))))
    block_units: list[tuple[dict, object]] = []
    for b in st["content_blocks"]:
        c = b.get("content")
        if b["block_type"] == "table" and isinstance(c, dict):
            cu = {}
            for i, row in enumerate(c.get("cells") or []):
                for j, cell in enumerate(row):
                    if cell:
                        u = Unit(nfc(str(cell)))
                        cu[(i, j)] = u
                        units_order.append(("cell", (b["block_index"], i, j), u))
            block_units.append((b, cu))
        elif isinstance(c, list):
            items = []
            for k, item in enumerate(c):
                u = Unit(nfc(str(item)))
                items.append(u)
                units_order.append(("item", (b["block_index"], k), u))
            block_units.append((b, items))
        else:
            u = Unit(nfc(str(c or "")))
            units_order.append(("text", b["block_index"], u))
            block_units.append((b, u))
    fn_units = []
    for fn in st.get("footnotes") or []:
        u = Unit(nfc(fn.get("text") or ""))
        fn_units.append((fn, u))
        units_order.append(("fn", None, u))
    pieces, offsets, pos = [], [], 0
    for _, _, u in units_order:
        if pieces:
            pos += 2
        offsets.append((pos, pos + len(u.text), u))
        pieces.append(u.text)
        pos += len(u.text)
    rebuilt = "\n\n".join(pieces)
    ocr_text = nfc(rec.get("ocr_text") or "")
    if rebuilt != ocr_text:
        stats["ocr_text_rebuild_mismatch"] += 1
        # fall back to anchoring against the rebuilt text (unit boundaries known)
    anchor_entities(rebuilt, offsets, rec.get("entities") or [], stats)

    # character-level clean-up and facsimile-verified corrections ----------
    # (after anchoring, so entity spans are carried along by Unit.edit)
    unit_block = {}
    for kind, ref, u in units_order:
        unit_block[id(u)] = (kind, ref)
    for kind, ref, u in units_order:
        for m in reversed(list(re.finditer("ſ", u.text))):
            u.edit(m.start(), m.end(), "s")
            if not any(c["rule"] == "resolve_long_s" for c in log):
                log.append({"rule": "resolve_long_s"})
        m = DOT_LEADER.search(u.text)
        if m and kind == "cell":
            u.edit(m.start(), m.end(), "")
            if not any(c["rule"] == "strip_dot_leaders" for c in log):
                log.append({"rule": "strip_dot_leaders"})
    for corr in VERIFIED.get(label or "", []):
        done = 0
        for kind, ref, u in units_order:
            if corr.get("block") and not (kind in ("text", "item", "cell") and f"b{(ref if kind == 'text' else ref[0]) + 1}" == corr["block"]):
                continue
            i = u.text.find(corr["find"])
            while i >= 0 and (corr.get("count", "all") == "all" or done < int(corr["count"])):
                u.edit(i, i + len(corr["find"]), corr["replace"])
                done += 1
                i = u.text.find(corr["find"], i + len(corr["replace"]))
        if done:
            log.append({"rule": "facsimile_correction", "before": corr["find"], "after": corr["replace"],
                        "source": corr.get("source", ""), "n": done})
        else:
            stats["verified_correction_not_found"] += 1
            print(f"  correction not found on p. {label}: {corr['find']!r}")

    # signatures + page number noise --------------------------------------
    printed = (st.get("page_number_printed") or "").strip() if isinstance(st.get("page_number_printed"), str) else str(st.get("page_number_printed") or "")
    if printed and label and printed != label and SIGNATURE.match(printed):
        page["signature"] = printed
        log.append({"rule": "signature_from_page_number", "value": printed})
    for fn_i, (fn, u) in enumerate(fn_units, start=1):
        mk = (fn.get("marker") or "").strip()
        if SIGNATURE.match(mk) and (not u.text.strip() or u.text.strip() == mk or SIGNATURE.match(u.text.strip())):
            page["signature"] = mk
            log.append({"rule": "signature_from_footnote", "value": mk})
            continue
        dehyphenate(u, log)
        page["footnotes"].append({"id": f"fn{fn_i}", "marker": mk, "text": u.text, "spans": u.spans})

    # running header -----------------------------------------------------
    header = nfc(st["header"]).strip() if st.get("header") else None
    first = st["content_blocks"][0] if st["content_blocks"] else None
    if header and first and first["block_type"] == "heading" and norm_cmp(first["content"]) == norm_cmp(header):
        log.append({"rule": "drop_header_equal_to_opening_heading", "value": header})
        header = None
    if header and SIGNATURE.match(header):
        header = None
    page["running_header"] = header

    # blocks -------------------------------------------------------------
    drop = set(override.get("drop_blocks", []))
    for b, payload in block_units:
        if b["block_index"] in drop:
            log.append({"rule": "manual_drop_block", "block": b["block_index"], "reason": override.get("reason")})
            continue
        bt = b["block_type"]
        bid = f"b{b['block_index'] + 1}"  # stable: raw block index, gaps allowed
        if bt == "table" and isinstance(b.get("content"), dict):
            for u in payload.values():
                dehyphenate(u, log)
            tlog: list = []
            table = build_table(b["content"], payload, tlog)
            for t in tlog:
                t["block"] = bid
            log.extend(tlog)
            if not table["rows"]:
                log.append({"rule": "drop_empty_table", "block": bid})
                continue
            page["blocks"].append({"id": bid, "type": "table", "src": b["block_index"], **table})
        elif bt == "list" or isinstance(payload, list):
            items = []
            for u in payload:
                dehyphenate(u, log)
                items.append({"text": u.text, "spans": u.spans})
            page["blocks"].append({"id": bid, "type": "list", "src": b["block_index"], "items": items})
        else:
            u = payload
            if not u.text.strip():
                continue
            dehyphenate(u, log)
            if bt != "heading" and SIGNATURE.match(u.text.strip()) and b is st["content_blocks"][-1]:
                page["signature"] = u.text.strip()
                log.append({"rule": "signature_from_paragraph", "value": u.text.strip()})
                continue
            btype = "heading" if bt == "heading" else "paragraph"
            if b["block_index"] in override.get("promote_heading", []):
                btype = "heading"
                log.append({"rule": "manual_promote_heading", "block": bid, "reason": override.get("reason")})
            blk = {"id": bid, "type": btype, "src": b["block_index"], "text": u.text, "spans": u.spans}
            if re.match(r"^Druck von .{3,60} in \w+\.?$", u.text.strip()):
                blk["role"] = "imprint"
            note = override.get("note")
            if note and note.get("block_src") == b["block_index"]:
                blk["editorial_note"] = {"de": note["text_de"], "en": note["text_en"]}
            page["blocks"].append(blk)
    for c in log:
        stats["fix:" + c["rule"]] += 1
    return page


def link_continuations(pages: list[dict]) -> None:
    """Flag paragraphs that run over a page break, incl. divided words."""
    text_pages = [p for p in pages if p["kind"] == "text" and p["blocks"]]
    for a, b in zip(text_pages, text_pages[1:]):
        if b["seq"] != a["seq"] + 1:
            continue
        last, first = a["blocks"][-1], b["blocks"][0]
        if last["type"] != "paragraph" or first["type"] != "paragraph":
            continue
        lt, ft = last["text"].rstrip(), first["text"].lstrip()
        if not ft:
            continue
        hyphen = lt.endswith(("-", "¬")) and ft[:1].isalpha()
        if hyphen or (ft[:1].islower() and not re.search(r"[.!?]$", lt)):
            last["continues"] = True
            first["continued"] = True
            if hyphen and ft[:1].islower():
                tail = re.search(r"(\S+)[-¬]$", lt)
                head = re.match(r"([\wäöüßÄÖÜ]+)", ft)
                if tail and head:
                    last["word_division"] = {"word": tail.group(1) + head.group(1), "part": tail.group(1) + "-"}
                    first["word_division"] = {"word": tail.group(1) + head.group(1), "part": head.group(1)}


def main() -> None:
    raw = load_raw()
    build_vocab(raw)
    if VERIFIED_FILE.exists():
        for c in read_json(VERIFIED_FILE)["corrections"]:
            VERIFIED.setdefault(c["page"], []).append(c)
    canvases = load_manifest()
    manual = read_json(MANUAL) if MANUAL.exists() else {}
    stats: collections.Counter = collections.Counter()
    pages = []
    for seq in sorted(canvases):
        page = normalize_page(seq, raw.get(seq), canvases[seq], manual.get("pages", {}), stats)
        pages.append(page)
    link_continuations(pages)
    stats["pages"] = len(pages)
    stats["pages_text"] = sum(p["kind"] == "text" for p in pages)
    stats["pages_with_continuation"] = sum(any(b.get("continued") for b in p["blocks"]) for p in pages)
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    for p in pages:
        write_json(PAGES_DIR / f"{p['seq']:04d}.json", p)
    write_json(DATA / "reports" / "normalize_report.json", dict(sorted(stats.items())))
    for k, v in sorted(stats.items()):
        print(f"{k:45s} {v}")


if __name__ == "__main__":
    main()
