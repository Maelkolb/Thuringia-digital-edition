"""Builds data/search/synonyms.json from data/search/qa/syn_source.txt and validates it against the built index.

  python data/search/qa/build_synonyms.py [--no-block]

Checks: every target word exists in the index vocabulary (after normalisation); warns about very frequent targets,
key collisions, multi-word keys, >4 distinct targets (the index builder keeps only the 4 best per key).
Also writes "blocker" entries: the index builder derives English->German pairs from the agents' keyword lists by a
cross product of tokens, which produces junk for German words and names (Gera > von, landesteil ...; Vogt > von, gera;
Wolf > im, kor). A blocker is an entry whose targets are four non-words (qxqa ...) that outrank the junk in the
builder's most_common(4) and are ignored by the client because they are not in the vocabulary.
"""
import io, json, re, sys, collections
from pathlib import Path

ROOT = Path(r"C:\Users\totom\Projects\reuss-edition")
sys.path.insert(0, str(ROOT / "pipeline" / "site"))
from norm import norm, tokens  # noqa: E402

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
SRC = ROOT / "data/search/qa/syn_source.txt"
OUT = ROOT / "data/search/synonyms.json"
FILL = ["qxqa", "qxqb", "qxqc", "qxqd"]

V = json.load(open(ROOT / "site/suche/vocab.json", encoding="utf-8"))
VI = {t: i for i, t in enumerate(V["t"])}
DF = lambda n: V["df"][VI[n]] if n in VI else 0
AUTO = json.load(open(ROOT / "data/search/qa/syn_baseline.json", encoding="utf-8"))  # index built without curation

# German word frequency in the book text (normalised stems), to recognise German keys among the auto-derived ones
book = open(ROOT / "data/text/plain.txt", encoding="utf-8").read()
BOOKF = collections.Counter(norm(t) for t in tokens(book) if not t.isdigit())


def parse():
    out, mode, sec = [], "DE", ""
    for ln, line in enumerate(SRC.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#") and not line.startswith("##"):
            continue
        if line.startswith("##"):
            sec = line[2:].strip()
            mode = "EN" if sec.startswith("EN") else "DE"
            continue
        if ">" not in line:
            print("!! no '>' in line", ln, line)
            continue
        ks, ts = line.split(">", 1)
        keys = [k.strip() for k in ks.split(",") if k.strip()]
        targets = ts.split()
        out.append({"keys": keys, "targets": targets, "mode": mode, "sec": sec, "ln": ln})
    return out


def plural_variants(k):
    k = k.lower()
    v = []
    if k.endswith("y") and not k.endswith(("ay", "ey", "oy")):
        v.append(k[:-1] + "ies")
    if k.endswith("fe"):
        v.append(k[:-2] + "ves")
    elif k.endswith("f"):
        v.append(k[:-1] + "ves")
    v += [k + "s", k + "es"]
    return v


def main():
    block = "--no-block" not in sys.argv
    entries = parse()
    warnings = []
    keynorm = {}  # norm -> entry line
    result = []
    used_norms = set()
    for e in entries:
        keys = []
        for k in e["keys"]:
            if len(tokens(k)) != 1:
                warnings.append(f"L{e['ln']}: multi-word key skipped: {k}")
                continue
            keys.append(k)
        if not keys:
            continue
        if e["mode"] == "EN":
            more = []
            for k in keys:
                more += plural_variants(k)
            keys += more
        # dedupe by norm, keep first spelling
        seen, final = set(), []
        for k in keys:
            n = norm(k)
            if n in seen:
                continue
            seen.add(n)
            final.append(k)
        for k in final:
            n = norm(k)
            if n in keynorm and keynorm[n] != e["ln"]:
                warnings.append(f"L{e['ln']}: key '{k}' (norm {n}) also defined on line {keynorm[n]}")
            keynorm.setdefault(n, e["ln"])
        # targets
        tl, tn = [], []
        for t in e["targets"]:
            if len(tokens(t)) != 1:
                warnings.append(f"L{e['ln']}: multi-word target {t}")
                continue
            n = norm(t)
            if n in tn:
                continue
            if DF(n) == 0:
                warnings.append(f"L{e['ln']}: target '{t}' (norm {n}) NOT IN INDEX  [{e['keys'][0]}]")
                continue
            tl.append(t)
            tn.append(n)
        # drop targets that equal every key norm only (self expansion is skipped by the builder anyway)
        real = [t for t, n in zip(tl, tn) if n not in {norm(k) for k in final}]
        if len(tn) > 4:
            warnings.append(f"L{e['ln']}: {len(tn)} distinct targets, only first 4 count: {e['keys'][0]}")
        for t, n in zip(tl, tn):
            if DF(n) > 1500:
                warnings.append(f"L{e['ln']}: very frequent target '{t}' df={DF(n)}  [{e['keys'][0]}]")
        if not real:
            warnings.append(f"L{e['ln']}: no usable target: {e['keys'][0]}")
            continue
        # pad with fillers if auto-derived pairs would otherwise survive in the builder's top 4
        pad = False
        autos = set()
        for k in final:
            autos |= set(AUTO.get(norm(k), []))
        if autos - set(tn) and len(tn) < 4:
            pad = True
        expand = tl[:4] if len(tn) > 4 else tl[:]
        if pad:
            # the 4-slot cap: real targets first, then fillers
            expand = tl[:4] + FILL[: max(0, 4 - len(set(tn[:4])))]
        item = {"q": final[0], "expand": expand}
        if len(final) > 1:
            item["also"] = final[1:]
        item["note"] = e["sec"] + (" +pad" if pad else "")
        result.append(item)
        used_norms |= {norm(k) for k in final}

    # blockers for German words / names whose auto-derived pairs are noise
    blockers = []
    if block:
        # German words / names in the book are blocked; these capitalised words are English or have usable auto pairs
        keep_cap = {"Hospital", "Doctor", "Character", "Hussiten", "Idiom", "Instrument", "Altar", "Pyramide", "Regiment",
                    "Saints", "German", "Primogenitur", "Statuten"}
        # lower-case German function words / adjectives that the cross product turned into keys
        block_low = {"alten", "fast", "ferner", "finden", "gefunden", "geraer", "gehört", "gelegen", "licht", "mit", "nackte",
                     "nun", "sonst", "später", "warmen", "gewesen", "wilde", "worden", "will", "sen", "ver", "bunten"}
        for n, targets in sorted(AUTO.items()):
            if n in used_norms or n not in VI:
                continue
            german = BOOKF.get(n, 0) >= 3
            if not german:
                continue
            disp = V["d"][VI[n]]
            if not ((disp[0].isupper() and disp not in keep_cap) or disp in block_low):
                continue
            if len(tokens(disp)) != 1:
                continue
            blockers.append({"q": disp, "expand": FILL[:], "note": "BLOCK auto noise: " + ",".join(targets)})
        print(f"blockers: {len(blockers)}")
    allitems = result + blockers
    json.dump({"expansions": allitems}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    nkeys = sum(1 + len(i.get("also", [])) for i in result)
    print(f"curated entries: {len(result)}  keys: {nkeys}  blockers: {len(blockers)}")
    for w in warnings:
        print("WARN", w)
    # fillers must not be in the vocabulary
    print("fillers in vocab:", [f for f in FILL if norm(f) in VI])
    return 0


main()
