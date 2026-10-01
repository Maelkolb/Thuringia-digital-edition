# Task type A — analyses ("Auswertungen") of quantitative content

Read `00_common.md` first.

The edition shows, next to the transcription, analyses that turn Brückner's tables, number series and
structured lists into charts with a short scholarly commentary. A first, inconsistent set existed for
pp. 54–65 (PNG images, iframes, bespoke JS). **All analyses are now encoded the same way**: one JSON
file per analysis, validated against `schemas/analysis.schema.json`, charts as Vega-Lite specs that the
edition renders with one shared theme. A complete worked example:
`data/analyses/klima-gera-luftdruck-1856-1867.json` (read it before you start).

## What to analyse

Go through every page of your range. Candidates:
* every table with numbers (statistics, measurements, heights, coordinates, prices, counts);
* number series in prose or lists (years with values, dates of events);
* structured lists that can be counted or placed in time (species lists by group, dated events,
  rulers with life dates, foundations, fires);
* related tables on neighbouring pages belong in **one** analysis (e.g. temperature for four stations).

Skip what has no analytical value (a single number, a table of three cells). Typical yield: one analysis
per substantial topic; a chapter with many tables may give 5–10. Quality over quantity. Don't duplicate
an analysis that already exists in `data/analyses/` (check the folder; your package may list topics that
another package covers).

Good analyses answer a question the reader actually has: How did the population grow? Which district
had the highest infant mortality? How does the climate of Schleiz (500 m) differ from Gera (200 m)?
When do the migrant birds arrive? Combine Brückner's numbers into derived measures where this helps
(rates, shares, converted units, means) and mark such columns `"derived": true`.

## File format (summary — the schema is authoritative)

`data/analyses/<id>.json`, `id` = kebab-case ASCII, topic first, e.g. `bevoelkerung-geburten-1834-1867`.

* `title`, `summary`, `method`, `findings[]`, `caveats[]`: every text as `{"de": …, "en": …}`.
  - summary: 2–4 sentences: what the source contains + what the charts show.
  - method: where the numbers come from (pages/blocks), what you did (selection, conversion, sums),
    known gaps. Name conversion factors.
  - findings: 2–5 statements, each verifiable in the data, numbers computed by code.
  - caveats: data quality, units, OCR doubts, comparability.
* `category` (enum in the schema), `section` (innermost section id from the page header, e.g. `t1-2-1`).
* `sources`: every block you used. `datasets[].source_refs`: blocks the dataset's printed numbers come from.
* `datasets`: tidy tables (one observation per row; long format for charts with several series).
  Column `name` = snake_case ASCII; `label` bilingual; `type` integer | number | string | date
  (ISO `YYYY-MM-DD` or `YYYY`); `unit`. **Every numeric column whose values are not printed in the
  source must have `"derived": true`** (conversions, sums, rates, codes such as month numbers 1–12,
  latitude in decimal degrees). The validator checks that all non-derived numbers occur in the cited
  blocks; >5 % misses fail.
* `charts` (1–4): `vegalite` = a Vega-Lite v6 spec **without data** (the dataset named in `dataset` is
  injected; extra datasets via `extra_datasets` and `{"data": {"name": …}}` in a layer). Any visible string
  may be `{"de": …, "en": …}`. Chart title and caption live in the chart object, not in the spec.
* `conversions`: each unit conversion with factor and reference (prefer Brückner pp. 831–832).
* `transcription_issues`: confirmed misreadings (see common rules).
* `keywords` (de/en), optional `related` (ids), `supersedes_legacy` when you replace one of the old
  pp. 54–65 visualisations, `generated_by`: "Claude Sonnet 5.5 (subagent A<nn>)", `date`.

## Chart rules (the edition's design system)

* Do not set colours, fonts, `config`, `width` or `background`; the theme supplies them. Use
  `height` 180–420. For colour use the defaults: categorical for identity (≤ 8 series, fixed order — a
  series keeps its colour across charts of the same analysis), `"scale": {"range": "ramp"}` or the
  default for sequential magnitude (heatmaps), `"scale": {"range": "diverging", "domainMid": 0}` for
  signed deviations.
* One y-axis per chart. Never two measures with different scales on one plot (no dual axis, no
  `resolve: independent y`); use small multiples (`facet`/`row`/`column`) or index to a base.
* Forms: line (+points when ≤ 30 points) for time series; bar for categories (sorted by value unless
  the categories have a natural order); heatmap (`rect`) for year × month; dot/range plots for min–max;
  `arc`/radial for wind directions; `tick`/`bar` with `x`/`x2` for date ranges (arrival–departure,
  lifespans); facets for several stations or districts.
* Every chart has a `tooltip` encoding with the meaningful fields (titled bilingually).
* ≥ 2 series → legend (the theme puts it on top). Label axes with unit, e.g. `"°C"`, `"hPa"`.
* Historical temperature in Réaumur: convert to °C (×1.25) in a derived column and plot °C.
* Time axes: use `"type": "ordinal"` for years when ≤ 20 years, else `"temporal"` with `timeUnit`
  or a quantitative year axis with `"format": "d"`.
* Keep it calm: no 3-D, no pies for close values, no more than ~7 colour classes.

## Workflow

1. Read your pages (`data/text/sections/…` or page files). Note all candidate tables/series.
2. For each analysis write a small Python script in your scratch folder `data/analyses/_work/<package-id>/`
   that reads the canonical page JSON (`data/pages/*.json`, block `grid` for tables) and writes the
   analysis JSON — do not type numbers by hand. Keep the script (it documents the derivation).
3. `node tools/validate_analysis.mjs data/analyses/<id>.json` → must print `OK`. Fix every ERROR; read
   the warnings.
4. Look at every preview PNG it writes (`data/analyses/_preview/<id>__c<n>.png`) with the Read tool and
   fix what looks wrong (overlapping labels, unreadable ticks, misleading scale, empty chart).
5. Write the search metadata for all pages of your range (see common rules) and validate it.
