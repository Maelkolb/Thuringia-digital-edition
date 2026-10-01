# Search QA report (subagent S01, 2026-10-01)

Saved by the main session from S01's hand-back (the subagent could not write report files).

## Results (top-3 relevance judged per query; good = ≥2 of top 3 relevant)

| set | queries | zero-hit before → after | good / partly / bad before | after |
|---|---|---|---|---|
| A main (tuned on) | 279 | 3 → 0 | 151 / 103 / 25 | 168 / 96 / 15 |
| B held-out (written before curating) | 131 | 3 → 1 | 61 / 60 / 10 | 71 / 54 / 6 |
| C round 3, modern wording | 43 | 7 → 0 | 8 / 23 / 12 | 18 / 22 / 3 |

Instructive cases: Textilindustrie (0 → 58 hits via Weberei/Tuchmacher), Geburtenrate (0 → 222), Kartoffelanbau, Hochzeitsbräuche, Vogt (Voigt; junk pair `vog > von, gera` removed), Hirschberg/Gera/Weida (junk automatic pairs removed), Kurort, Lebenserwartung, Wasserversorgung, wolves, Maß (Maaß), Ahnenforschung.

## synonyms.json

582 curated entries (≈390 EN→DE, ≈165 modern DE→1870), every target checked against the index vocabulary; 197 "blockers" (non-word targets) neutralise junk automatic pairs. Rules: no expansion of German keys the book uses ≥10 times (except measured cases); no English keys that fold to German function words (dye, myth, hat, man, state) or frequent German nouns (rat, cost, craft, tanner, born, tale, pests). Generator: `build_synonyms.py` from `syn_source.txt`.

## Engine problems reported (status after the main-session fixes, see below)

1. Register/glossary/place/analysis stubs outrank text (kind weights + BM25 length bonus).
2. No exact-title boost (Gera, Saalburg, Tanna articles not in top 8).
3. Fold/stem collisions on short words (Frost/Fronen `fro`, Kloster/clothes `klo`, Tal/Thaler/tale).
4. Automatic EN→DE pairs from unaligned keyword cross products are mostly noise.
5. English words colliding with German function words after folding (myth→mit, dye→die, the→te).
6. No stop words: natural-language questions fail.
7. Phrase filter applied after rendering (counts and facets include rejected blocks).
8. AND per block (multi-word queries miss pages where words are in different blocks).
9. Fuzzy fallback ranked by length, not edit distance; suggestion not clickable.
10. Duplicate / mis-linked register results (lookup by label).
11. Entity chips are plain prefix matches (Gera → Geräthschaft).
12. Front matter (contents pages) ranks as content.
13. Years match register persons before event pages.
14. Hit count counts blocks, not pages.
15. Digit+letter compounds split ("30jährigen").
16. syn.json: one weight, ≤4 targets, loaded eagerly.
17. Stale built search.js (fixed by rebuild).

Query sets, grades and results are in this folder (`queries*.txt`, `grades_*.tsv`, `results_*.json`); `probe_fast.mjs` runs a whole set in one page load.
