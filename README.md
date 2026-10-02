# Brückner 1870 – Digital Edition

Digital scholarly edition of **Georg Brückner: *Volks- und Landeskunde des Fürstenthums Reuß j. L.*, Gera: Köhler 1870** (VIII + 840 pp.), based on the copy of the Bayerische Staatsbibliothek (bsb11005578, IIIF).

The repository contains the canonical edition data, the pipeline that produces it from the automatic transcription, the work of the AI subagents (analyses, place articles, registers, search metadata) and the generator of the static website.

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
| Wikidata via GeoNames | `pipeline/wikidata_enrich.py` | `data/entities/wikidata_by_geonames.json` |
| place-article coordinates | `pipeline/gazetteer_coords.py` | `data/gazetteer/coords.json` |
| website, search index, TEI | `pipeline/site/build.py` (`--only-search`, `--only-tei`, `--skip-charts`, `--pages 20,54`) | `site/` |

Manual editorial decisions (blank pages, restored blocks, promoted headings) are in `data/corrections/manual.json`, each with its reason. Every automatic correction is logged in the page record (`corrections`) and shown on the page.

## Subagent work

Instructions and validators for the AI subagents are in `docs/agents/` and `tools/`:

* analyses (`docs/agents/10_analyses.md`, `schemas/analysis.schema.json`, `tools/validate_analysis.mjs`) → `data/analyses/*.json`, scripts in `data/analyses/_work/<package>/`
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
