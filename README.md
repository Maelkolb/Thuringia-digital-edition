# Brückner 1870 – Digital Edition

**Live edition:** https://maelkolb.github.io/Thuringia-digital-edition/ (GitHub Pages, branch `gh-pages`; publish a new build with `python pipeline/site/build.py && sh tools/publish_pages.sh`).

Digital scholarly edition of **Georg Brückner: *Volks- und Landeskunde des Fürstenthums Reuß j. L.*, Gera: Köhler 1870** (VIII + 840 pp.), based on the copy of the Bayerische Staatsbibliothek (bsb11005578, IIIF).

The repository contains the canonical edition data, the pipeline that produces it from the automatic transcription, the material produced with language models (analyses, place articles, register decisions, page summaries) and the generator of the static website.

## Quick start

```bash
# Python 3.12+ (bs4, lxml, jinja2, pillow, requests), Node 20+
cd tools && npm install && cd ..
python pipeline/site/build.py            # builds ./site (≈ 1 min)
cd site && python -m http.server 8642    # open http://127.0.0.1:8642
```

The site is fully static (no server code, no CDN, self-hosted fonts) and can be deployed to any web server or GitHub Pages. It also works opened straight from disk (double-click `site/index.html`): internal data (search index, chart specs, map places, index citations) is written as scripts calling `RJ.put(key, data)` and loaded with `RJ.load(key)` (edition.js), because browsers block `fetch()` on `file://`; fonts come from an embedded copy (`assets/css/fonts-offline.css`). Only the facsimiles (BSB IIIF) and map tiles (TopPlusOpen, BKG; OpenStreetMap as fallback) need the internet. Check both modes with `node tools/check_render.mjs site file|http`. Set `base_url` in `data/site.json` before publishing (canonical links, sitemap, citations).

## Data flow

| step | script | output |
|---|---|---|
| raw transcription (Gemini 3 Flash, 2026) | Colab notebook / `source/hde_2026-03-03` | `source/json_batch1`, `source/json_batch2` |
| gap fill (11 missing/empty pages) | `pipeline/fill_missing_pages.py`, `pipeline/manual_fill.py` | `data/raw_fill/` |
| canonical pages + layout corrections | `pipeline/normalize.py` | `data/pages/<scan>.json`, `data/reports/normalize_report.json` |
| book structure | `pipeline/structure.py` (`data/structure/toc.json`) | `data/structure/structure.json` |
| text views for reading/agents | `pipeline/export_text.py` | `data/text/` |
| Brückner's place index | `pipeline/ortsregister.py` | `data/registers/ortsregister.json` |
| facsimile-verified corrections | `pipeline/collect_corrections.py` | `data/corrections/verified.json` (applied by normalize) |
| entity candidates | `pipeline/entities_prepare.py` (GeoNames DE dump in `source/geonames/`, not in git) | `data/entities/candidates/`, `mentions.jsonl` |
| entity registry | `pipeline/entities_build.py` (decisions `data/entities/decisions/E*.json`) | `data/entities/registry.json`, `key_map.json` |
| register polish: bilingual notes, English kinds, typography | `pipeline/entities_polish.py`, run by `entities_build.py` (`data/entities/notes.json`, `kinds_en.json`, `polish_overrides.json`) | `data/entities/registry.json` (in place) |
| Wikidata via GeoNames | `pipeline/wikidata_enrich.py` | `data/entities/wikidata_by_geonames.json` |
| place-article coordinates | `pipeline/gazetteer_coords.py` | `data/gazetteer/coords.json` |
| website, search index, TEI | `pipeline/site/build.py` (`--only-search`, `--only-tei`, `--skip-charts`, `--pages 20,54`, `--only-analyses klima-gera`) | `site/` |

Manual editorial decisions (blank pages, restored blocks, promoted headings) are in `data/corrections/manual.json`, each with its reason. Every automatic correction is logged in the page record (`corrections`) and shown on the page. After `normalize.py`, always run `structure.py`, `export_text.py` and `tools/lines/align_lines.py`, in that order. Name forms that later text fixes changed (the Fraktur double hyphen, for example) keep their register link through `data/entities/key_aliases.json`, which the site builder merges into the key map.

## Work done with language models

Analyses, place articles, register decisions and page metadata were produced with Claude (Anthropic) from written briefs and checked by validators. The briefs are in `docs/agents/`, the validators in `tools/`:

* analyses (`docs/agents/10_analyses.md` and `40_features.md`, `schemas/analysis.schema.json`, `tools/validate_analysis.mjs`) → `data/analyses/*.json`. The 32 analyses on the site are written by the builder scripts in `data/analyses/_work/F1–F8/` from the earlier single analyses in `data/analyses/_archive/`; `bevoelkerung-1647-1867.json` is edited by hand. Run a builder from the repository root, then `python pipeline/site/build.py --only-analyses <id>` to see the result. The chart colours and text styles for light and dark mode are in `tools/vega_theme.mjs`
* place articles (`20_gazetteer.md`, `tools/validate_gazetteer.py`) → `data/gazetteer/G1–G6.json`
* registers (`30_entities.md`, `tools/validate_entity_decisions.py`) → `data/entities/decisions/E1–E9.json`
* search metadata (`00_common.md`, `tools/validate_search_meta.py`) → `data/search/pages/*.json`; curated query expansions `data/search/synonyms.json`

Helpers: `tools/facsimile.py` (IIIF crops), `tools/gbif_match.py`, `tools/wikidata_search.py`.

## Quality assurance

* `node tools/validate_analysis.mjs --all` – schema, sources, printed numbers vs. transcription, chart compilation
* `python tools/validate_tei.py --sample 30` – TEI P5 (tei_all) validation
* `node tools/shot.mjs <dir> "seite/54.html|w390 dark"` – screenshots (headless Edge)
* `node tools/a11y.mjs index.html seite/117.html` – axe-core accessibility audit
* `node tools/search_probe.mjs queries.txt` – search result probes

## Licences

Transcription, annotations, registers, place articles, analyses and edition texts: CC BY 4.0. Facsimiles: Bayerische Staatsbibliothek, NoC-NC 1.0 (embedded via IIIF, not redistributed). Coordinates GeoNames (CC BY 4.0), taxonomy GBIF (CC BY 4.0), Wikidata (CC0). Vendored libraries: OpenSeadragon, Leaflet, Vega (BSD); fonts Newsreader, Source Sans 3, IBM Plex Mono (OFL).

## Printed lines and image regions

`tools/lines/modal_lines.py` detects the printed lines on every BSB scan with kraken (blla) and reads each line with
Tesseract (`frak2021`, UB Mannheim) on Modal (`uvx --from modal modal run tools/lines/modal_lines.py`, about 18 s per page,
10 containers; output `data/lines/raw/`). `tools/lines/align_lines.py` aligns the readings with the transcription
(`data/lines/aligned/`, summary in `data/lines/summary.json`). The site uses them for the line view and the text/facsimile
highlighting, the TEI export for `<lb facs>` and `<zone>`. Check the page view with `node tools/check_pageview.mjs 203`.
