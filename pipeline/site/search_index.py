"""Static, sharded full-text index for the edition (BM25 on the client).

Documents: every text block (paragraph, heading, list, table, footnote), the
page metadata written by the subagents (summaries/keywords DE+EN), register
entries, gazetteer articles, analyses and glossary terms.

Files written to <site>/suche/:
  docs.json      [kind, target, anchor, section, length, title] per document
  vocab.json     sorted normalised terms with document frequency + display form
  i/<xx>.json    postings shards keyed by the first two characters of a term
  t/<slug>.json  block texts per page (snippets, loaded on demand)
  syn.json       English -> German query expansion (normalised)
  sections.json  section ids, titles, parents
  quick.json     register/section/analysis/glossary labels for autocomplete
"""
from __future__ import annotations

import collections
import json
from pathlib import Path

from norm import fold, norm, tokens

KIND_WEIGHT = {"h": 1.6, "p": 1.0, "t": 0.9, "l": 1.0, "f": 0.9, "m": 0.6, "e": 0.8, "g": 1.1, "a": 1.2, "w": 1.0}


def block_text(b: dict) -> str:
    if b["type"] == "table":
        return "\n".join(" | ".join(c for c in row if c) for row in b["grid"]) + ("\n" + b["caption"] if b.get("caption") else "")
    if b["type"] == "list":
        return "\n".join(i["text"] for i in b["items"])
    return b["text"]


def shard(term: str) -> str:
    t = fold(term)
    key = (t[:2] if len(t) >= 2 else t + "_")
    return "".join(ch if ch.isalnum() else "_" for ch in key)


def build(out: Path, pages: list[dict], sections: list[dict], meta: dict, registry: list[dict], gazetteer: list[dict],
          analyses: list[dict], glossary: list[dict], register_href) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    (out / "i").mkdir(exist_ok=True)
    (out / "t").mkdir(exist_ok=True)
    sec_index = {s["id"]: i for i, s in enumerate(sections)}
    docs: list[list] = []
    postings: dict[str, dict[int, int]] = collections.defaultdict(dict)
    display: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)

    def add(kind: str, target: str, anchor: str, section: str | None, text: str, title: str = "") -> None:
        toks = tokens(text)
        if kind == "e":  # index entries: no years/numbers (they would outrank the pages about the events)
            toks = [t for t in toks if not t.isdigit()]
        if not toks:
            return
        di = len(docs)
        docs.append([kind, target, anchor, sec_index.get(section, -1), len(toks), title])
        for tok in toks:
            n = norm(tok)
            if not n:
                continue
            postings[n][di] = postings[n].get(di, 0) + 1
            if not tok.isdigit():
                display[n][tok] += 1

    kind_of = {"paragraph": "p", "heading": "h", "list": "l", "table": "t"}
    for p in pages:
        texts = {}
        for b in p["blocks"]:
            txt = block_text(b)
            texts[b["id"]] = txt
            add(kind_of[b["type"]], p["slug"], b["id"], b.get("sec"), txt)
        for fn in p["footnotes"]:
            texts[fn["id"]] = fn["text"]
            add("f", p["slug"], fn["id"], p["sections"][-1] if p.get("sections") else None, fn["text"])
        m = meta.get(p["slug"])
        if m:
            mtxt = " ".join([m.get("summary_de", ""), m.get("summary_en", ""), " ".join(m.get("keywords_de", [])),
                             " ".join(m.get("keywords_en", [])), " ".join(m.get("subjects", []))])
            texts["_summary_de"] = m.get("summary_de", "")
            texts["_summary_en"] = m.get("summary_en", "")
            add("m", p["slug"], "", (p.get("section_path") or [None])[-1], mtxt)
        (out / "t" / f"{p['slug']}.json").write_text(json.dumps(texts, ensure_ascii=False), encoding="utf-8")
    for e in registry:
        txt = " ".join([e["label"], " ".join(e.get("forms", {}).keys()), e.get("modern", "") or "", e.get("gloss_en", "") or "",
                        e.get("kind", "") or "", e.get("description_de", "") or "", e.get("description_en", "") or "",
                        e.get("scientific", "") or ""])
        add("e", e["id"], "", None, txt, e["label"])
    for g in gazetteer:
        txt = " ".join([g["name"], " ".join(h["form"] for h in g.get("historic_forms", [])), g.get("dialect_form", "") or "",
                        g.get("type_verbatim", "") or "", g.get("summary_de", ""), g.get("summary_en", ""),
                        " ".join(s["name"] for s in g.get("subplaces", []))])
        add("g", g["id"], g["start"]["page"], None, txt, g["name"])
    for a in analyses:
        txt = " ".join([a["title"]["de"], a["title"]["en"], a["summary"]["de"], a["summary"]["en"],
                        " ".join(a["keywords"]["de"]), " ".join(a["keywords"]["en"])])
        add("a", a["id"], "", a.get("section"), txt, a["title"]["de"])
    for w in glossary:
        txt = " ".join([w["term"], " ".join(w.get("variants", [])), w.get("de", ""), w.get("en", "")])
        add("w", w["id"], "", None, txt, w["term"])

    # postings shards ------------------------------------------------------
    shards: dict[str, dict] = collections.defaultdict(dict)
    for term, plist in postings.items():
        flat = []
        for di, tf in sorted(plist.items()):
            flat += [di, tf]
        shards[shard(term)][term] = flat
    for name, data in shards.items():
        (out / "i" / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    terms = sorted(postings)
    vocab = {"t": terms, "df": [len(postings[t]) for t in terms],
             "d": [display[t].most_common(1)[0][0] if display[t] else t for t in terms]}
    (out / "vocab.json").write_text(json.dumps(vocab, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    avg = sum(d[4] for d in docs) / max(1, len(docs))
    (out / "docs.json").write_text(json.dumps({"docs": docs, "avgLen": avg, "weights": KIND_WEIGHT}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (out / "sections.json").write_text(json.dumps([[s["id"], s.get("num", ""), s["title"], s.get("title_en", ""), s.get("parent")] for s in sections],
                                                  ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    # English -> German expansion from aligned keyword lists ----------------
    # only single-word pairs, and only for English words that are not (also)
    # frequent German words of the book - otherwise e.g. "Gera" -> "von".
    german_df = collections.Counter()
    for t, plist in postings.items():
        german_df[t] = sum(1 for di in plist if docs[di][0] in "phtlf")
    syn: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for m in meta.values():
        de, en = m.get("keywords_de", []), m.get("keywords_en", [])
        if len(de) != len(en):
            continue
        for d, e in zip(de, en):
            et, dt = tokens(e), tokens(d)
            if len(et) != 1 or len(dt) != 1 or et[0][:1].isupper() and dt[0] == et[0]:
                continue
            ne, nd = norm(et[0]), norm(dt[0])
            if ne != nd and len(ne) > 2 and german_df[ne] < 3:
                syn[ne][nd] += 1
    # curated expansions (search-quality agent): data/search/synonyms.json
    cur = Path(__file__).resolve().parents[2] / "data" / "search" / "synonyms.json"
    if cur.exists():
        for item in json.loads(cur.read_text(encoding="utf-8")).get("expansions", []):
            for q in [item["q"]] + item.get("also", []):
                qt = tokens(q)
                if len(qt) != 1:
                    continue
                nq = norm(qt[0])
                for target in item["expand"]:
                    for tt in tokens(target):
                        nt = norm(tt)
                        if nt != nq:
                            syn[nq][nt] += 5
    syn_out = {k: [t for t, _ in v.most_common(6)] for k, v in syn.items() if sum(v.values()) >= 1}
    (out / "syn.json").write_text(json.dumps(syn_out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    # autocomplete -------------------------------------------------------------
    quick = []
    for e in registry:
        if e["n"] >= 2 or not e.get("fallback", True):
            quick.append([e["label"], e["class"], register_href(e), e["n"]])
    for s in sections:
        quick.append([f"{s.get('num', '')} {s['title']}".strip(), "section", f"seite/{s['start_label']}.html", 0])
    for a in analyses:
        quick.append([a["title"]["de"], "analysis", f"auswertungen/{a['id']}.html", 0])
    for w in glossary:
        quick.append([w["term"], "glossary", f"register/glossar.html#{w['id']}", 0])
    (out / "quick.json").write_text(json.dumps(quick, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return {"docs": len(docs), "terms": len(terms), "shards": len(shards), "syn": len(syn_out), "quick": len(quick)}
