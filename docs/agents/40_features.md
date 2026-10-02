# Analyses, second round: fewer pieces, better designed

Read `docs/agents/00_common.md` first (sources, citation format, facsimile check, ground rules).

The edition had 125 single analyses (now archived in `data/analyses/_archive/`). Readers found them
too many, too text-heavy and visually generic. They are being merged into **32 thematic pieces**
("features"), each a short, well-designed piece of data journalism about one topic of the book.
The archived analyses are your raw material: their datasets were extracted from the print and
validated against it, so reuse them (copy datasets exactly, with `source_refs`, `derived` flags and
`transcription_issues`) instead of re-extracting. Re-read the source pages where you need context.

The reference piece is `data/analyses/bevoelkerung-1647-1867.json` (open it, and its previews
`data/analyses/_preview/bevoelkerung-1647-1867__c1.png` … `c3.png`). Match or beat its quality.

## What a feature is

Same JSON format as before (`schemas/analysis.schema.json`), one file `data/analyses/<id>.json`, plus:

* `"merges": [...]` – the ids of the archived analyses it absorbs (all of them, see the plan below).
* at most **3 charts**, ideally 2–3; the first chart is also the thumbnail in the gallery, so make it
  the strongest and most characteristic picture of the topic.
* `title`: short noun phrase, ≤ 12 words, e.g. "Klima in Gera 1856–1867".
* `summary` (the lead, shown under the title): ≤ 75 words. What Brückner documents, the two or three
  most important numbers, one sentence of context. No method talk here.
* `findings`: 0–3 bullets, each ≤ 35 words, each a concrete, checkable statement with a number.
* chart `title`: a **statement of what the chart shows**, ≤ 16 words ("Gera wuchs am schnellsten,
  Lobenstein-Ebersdorf schrumpfte nach 1855"), not a label ("Einwohner nach Bezirk").
* chart `caption`: ≤ 45 words: what is plotted, the unit, anything needed to read it, the source pages.
* `method` (collapsed on the page): ≤ 260 words, plain; conversions in `conversions`.
* `caveats` ≤ 4, each ≤ 60 words. `transcription_issues` carried over from the merged analyses.
* `datasets`: those the charts use, plus at most one or two further tables worth downloading.
* `related`: ids of other features from the plan below (2–4).
* `generated_by`: "Claude Sonnet 5.5 (Agent F<n>), aus <k> Einzelauswertungen zusammengeführt";
  `date`: "2026-10-02".

`node tools/validate_analysis.mjs data/analyses/<id>.json` enforces all limits, checks every printed
number against the cited source blocks, compiles both languages and dark mode, and writes previews
to `data/analyses/_preview/<id>__c<n>.png`.

## Design rules (every chart)

1. **One message per chart.** Decide what the reader should see, then choose the form. If a chart
   needs a paragraph to be understood, it is the wrong chart.
2. **Direct labels instead of legends** for ≤ 4 series: label line ends, label the bars/points that
   matter. A legend only when direct labels are impossible (maps, many categories).
3. **Highlight and context.** Put the focus in colour (`@accent`), everything else in `@context`
   (bars, lines) or `@muted` (points, secondary text). Use the categorical colours (`@accent`,
   `@accent2`, `@accent3`, in this order) only when the categories themselves are the message.
   Never more than 4 colours in one chart.
4. **Forms that work for this material:**
   * comparisons of a few groups across two moments → dumbbell (see c2 of the reference);
   * rankings → sorted lollipop or bar, horizontal, values labelled (c3 of the reference);
   * time series → lines without point markers when there are more than ~12 points; annotate
     events from the book with a rule + short text; index to a base year when levels differ;
   * year × month (climate) → heatmap (`rect`, `"scale": {"range": "diverging", "domainMid": …}` for
     anomalies or `"range": "heatmap"`), or a monthly band (min–max area + mean line);
   * places → **map** (recipe below);
   * periods of operation, reigns, dated events → timeline/Gantt (`bar` with `x` and `x2` on years);
   * age structure → population pyramid (two bars mirrored, men left as negative values);
   * directions (wind, storms) → radial chart (`arc` with `theta` + `radius`) as small multiples;
   * many parallel series → small multiples (`facet` / `row`/`column`), shared scales, not spaghetti.
5. **No** pie or donut charts (except a radial wind chart), no 3D, no dual axes, no stacked bars with
   more than 4 segments, no rainbow scales, no legend for a single series, no point markers on every
   value of a long line, no numbers on every bar of a long chart (label max, min and the focus).
6. **Sort** categorical axes by value unless the order itself means something (time, size classes,
   Ober-/Unterland). Put long labels on the y axis.
7. **Tooltips** on every data mark (`tooltip` with titles in both languages and `format`).
8. Size: width comes from the page (do not set `width` for single views); height 220–420 px, or
   `{"step": 18–24}` for one row per category. Facets/concats need explicit cell widths; keep the
   total ≤ 860 px wide.
9. Numbers: `format` with `,d` / `.1f` – the page switches to German separators automatically.
10. Bilingual: every text in a spec as `{"de": …, "en": …}`; category values from the data stay in
    the source language (Brückner's spelling), translate labels with `calculate`/`labelExpr` only
    where needed.

### Colours and text styles

Never write hex colours. Use the tokens, they become the right colour in light and dark mode:
`@accent @accent2 @accent3` (data), `@context` (grey bars/lines), `@muted` (grey points, rules),
`@ink`, `@ink2` (text), `@paper` (background, halos, strokes), `@land` (base map dots), `@river`,
`@positive`, `@negative`.

Text marks: `"style": "label"` (data labels, bold), `"label-muted"` (secondary values),
`"annotation"` (event notes), `"place-halo"` + `"place-label"` (two layers, halo first, for place names
on maps). Do not set font sizes or colours on text marks unless necessary.

### Map recipe

Shared base layers (copy them into your `datasets` and list them in the chart's `extra_datasets`):

* `data/analyses/_shared/base_places.json` → dataset `orte_basis` (199 places: `ort`, `lon`, `lat`,
  `landestheil`, `typ`, `ortsartikel`)
* `data/analyses/_shared/base_rivers.json` → dataset `fluesse_basis` (Saale, Weiße Elster, Weida,
  Wisenta, Selbitz, Orla, Auma as `fluss`, `abschnitt`, `folge`, `lon`, `lat`)

Your own place data needs `lon`/`lat`; join coordinates from `orte_basis` by name in Python when you
build the dataset (mark the columns `"derived": true`, note "GeoNames"). Working example:
`data/analyses/_work/maptest.json` (preview `_preview/maptest__c1.png`):

```json
{"height": 560, "projection": {"type": "mercator"},
 "layer": [
  {"data": {"name": "fluesse_basis"}, "mark": {"type": "line", "color": "@river", "strokeWidth": 1.2},
   "encoding": {"longitude": {"field": "lon", "type": "quantitative"}, "latitude": {"field": "lat", "type": "quantitative"},
                "detail": {"field": "abschnitt"}, "order": {"field": "folge"}}},
  {"data": {"name": "orte_basis"}, "mark": {"type": "circle", "size": 10, "color": "@land"},
   "encoding": {"longitude": {"field": "lon", "type": "quantitative"}, "latitude": {"field": "lat", "type": "quantitative"}}},
  {"transform": [{"filter": "isValid(datum.lon) && isValid(datum.lat)"}],
   "mark": {"type": "circle", "stroke": "@paper", "strokeWidth": 0.8, "opacity": 0.85},
   "encoding": {"longitude": …, "latitude": …, "size": {"field": "…", "type": "quantitative", "scale": {"type": "sqrt", "range": [6, 700]}}, "color": …, "tooltip": …}},
  {"transform": [{"filter": "indexof(['Gera','Schleiz','Lobenstein','Hirschberg','Saalburg','Tanna','Ebersdorf','Hohenleuben'], datum.name) >= 0"}],
   "mark": {"type": "text", "style": "place-halo", "dy": -12}, "encoding": {"longitude": …, "latitude": …, "text": {"field": "name"}}},
  { … same with "style": "place-label" … }
 ]}
```

Maps are worth it where the book gives values per place (Ortskunde, Sagenorte, Wüstungen, stations,
surveyed points, subscribers' home towns, heights of places). One map per feature is usually enough.

## Text rules

German first, then an idiomatic English version (American spelling). Plain, scholarly, concrete; no
"fascinating", "remarkable", "boom", no rhetorical questions, no "–" dashes as sentence glue (use a
full stop or a semicolon), no "·" separators anywhere. Modern spelling in our own text (Landesteil,
Fürstentum, Prozent, Taler); quotations and data values keep Brückner's spelling. Every number in a
title, lead, finding or caption must be computed in Python from the datasets – write the check
script into `data/analyses/_work/<your agent id>/`.

## Working loop (do not skip)

1. Read the archived analyses of your features (`data/analyses/_archive/<id>.json`) and the source
   pages they cite (`data/text/pages/<page>.txt`). Decide the 2–3 messages per feature.
2. Build the feature with a Python script in `data/analyses/_work/<agent id>/` (keeps it reproducible).
3. Validate. Fix every error. Warnings about "fit-y" for step heights can be ignored.
4. **Open every preview PNG with the Read tool and look at it critically**: overlapping labels, cut-off
   text, empty space, unreadable small multiples, colours without meaning, a title that the picture
   does not show. Iterate until each chart passes. Check one chart in dark mode as well:
   `node tools/debug_svg.mjs data/analyses/<id>.json c1` writes `debug.svg` (light) – for dark,
   trust the tokens.
5. Report: files written, for each feature the charts (form + message), what you dropped from the
   merged analyses and why, transcription problems found.

Write only `data/analyses/<your feature ids>.json` and files under `data/analyses/_work/<agent id>/`.
Do not touch other agents' files, the archive, the base layers, the tools or the site.

## The plan

Sections: use the section of the main source chapter. `F<n>` is the agent.

| agent | id | title (draft) | section | merges (archived ids) | ideas |
|---|---|---|---|---|---|
| F1 | `land-lage-grenzen` | Lage, Fläche und Grenzen | t1-1-2 | grenzen-umfang-nachbarlaender, lage-vermessene-punkte-laenge-breite, flaeche-fuerstenthum-vermessung-nachbarn | map of the surveyed points (printed coordinates!), boundary length by neighbouring state for Ober- and Unterland, area estimates over time |
| F1 | `relief-hoehen` | Berge und Höhenlage | t1-1-4 | relief-erhebungen-hoechste-punkte, relief-hoehe-und-lage-neigung, relief-hoehenstufen-oberland-unterland, relief-wohnorte-hoehenlage, relief-bergnamen | map of places coloured by height (sequential ramp), highest summits, Oberland vs. Unterland height bands |
| F1 | `geologie-boden` | Gesteine, Böden und Bodenschätze | t1-1-5 | geologie-formationen-bodenguete, geologie-formationen-rohstoffe, geologie-fossilfunde-zechstein-clymenienkalk | formation × soil quality, useful minerals per formation |
| F1 | `gewaesser` | Flüsse, Quellen und Heilquellen | t1-1-6 | gewaesser-hauptfluesse-lauf-gefaelle, gewaesser-quellen-muendungen-hoehen, gewaesser-nebenfluesse-verzeichnis, gewaesser-heilquellen-lobenstein-analyse | longitudinal profiles (height vs. course) of Saale/Elster/Weida, tributaries by side, the Lobenstein spring analysis |
| F2 | `klima-gera` | Wetter in Gera 1856–1867 | t1-1-7 | klima-gera-temperatur-1856-1867, klima-gera-luftdruck-1856-1867, klima-regenmenge-gera-1860-1867, klima-witterungserscheinungen-gera-1856-1867 | heatmap year × month of temperature (anomaly), monthly mean with range band, rain |
| F2 | `klima-stationen` | Klima an den Beobachtungsorten | t1-1-7 | klima-stationen-temperatur-vergleich, klima-hoehenlage-temperatur-luftdruck, klima-niederschlagstage-stationen, klima-bewoelkung-stationen, klima-quellentemperatur-brunnen | temperature vs. elevation (labelled stations), station map, wet/foggy days |
| F2 | `wind-gewitter` | Wind und Gewitter | t1-1-7 | klima-wind-gera-1856-1865, klima-wind-stationen-vergleich, klima-gewitter-gera-stationen | wind roses as small multiples, thunderstorm months |
| F2 | `phaenologie` | Blüte und Vogelzug | t1-1-7 | phaenologie-bluetezeiten-gera-hohenleuben-1851-1861, phaenologie-zugvoegel-gera-1859-1864 | calendar strip plots (day of year), Gera vs. Hohenleuben |
| F3 | `pflanzenwelt` | Pflanzenwelt | t1-1-8 | flora-artenzahlen-phanerogamen-kryptogamen, flora-exklusivarten-unterland-oberland, flora-seltene-pflanzen-fundorte, wald-baumarten-flurnamen | species numbers, Unterland vs. Oberland, rare plants' sites (map?) |
| F3 | `tierwelt` | Tierwelt und ihr Wandel | t1-1-9 | fauna-artenzahlen-tiergruppen, fauna-fische-gewaesser, fauna-voegel-unterland-oberland, fauna-voegel-zugzeiten-und-seltene-gaeste, fauna-aenderungen-seit-1647, fauna-tiernamen-in-flurnamen | timeline of vanished animals (wolf, bear …), species per group, fish per river |
| F3 | `sagen-brauch` | Sagen, Bräuche und Volksmedizin | t1-2-8 | kultur-sagenorte-nach-typ-und-landestheil, kultur-volkskalender-bauernjahr, gesundheit-volksmedizin-hausmittel-nach-leiden, mundart-sprachproben-orte-und-textsorten | map of legend sites by type, the folk calendar as a year strip |
| F3 | `ortsnamen` | Ortsnamen, erste Erwähnungen und Wüstungen | t2 | ortsnamen-sorbische-wurzeln, orte-erste-erwaehnungen-namensformen, kultur-ortssiegel-motive, orte-wuestungen-ortskunde | map of deserted villages, first records by century, Sorbian name roots |
| F4 | `geburten-sterbefaelle` | Geburten, Ehen und Sterbefälle 1858–1867 | t1-2-1 | bevoelkerung-natuerlicher-zuwachs-1858-1867, bevoelkerung-geburten-1858-1867, bevoelkerung-sterblichkeit-1858-1867, bevoelkerung-uneheliche-geburten-1858-1867, bevoelkerung-todtgeborene-1858-1867, bevoelkerung-geburtensaldo-wanderung-1859-1867, bevoelkerung-eheschliessungen-1858-1867, bevoelkerung-sterblichkeit-lobenstein-1794-1804, gesundheit-selbstmord-unglueck-1858-1867 | births vs. deaths with the gap shaded, illegitimacy by district, the 1866 mortality peak annotated |
| F4 | `alter-familie` | Alter, Geschlecht und Familienstand | t1-2-1 | bevoelkerung-altersaufbau-1864, bevoelkerung-familienstand-ehen-1864, bevoelkerung-geschlecht-alter-1834-1867, bevoelkerung-wanderung-1864-1867 | population pyramid 1864, marital status by age, birthplaces |
| F4 | `gesundheit` | Krankheit, Ärzte und Seuchen | t1-2-6 | gesundheit-krankheitsstatistik-lobenstein-gera-hohenleuben, gesundheit-medizinalwesen-und-seuchen-zeitleiste, gesundheit-taubstumme-blinde-1864-1867, gesundheit-militaer-tauglichkeit-1864-1866 | epidemic timeline, main diseases by place, fitness of recruits |
| F4 | `siedlung-wohnen` | Siedlungen und Häuser 1867 | t2 | bevoelkerung-gemeindegroessen-1867, wohnen-wohnhaeuser-wohndichte-1867, orte-siedlungsbild-1867, wohnen-kirchenneubauten-1611-1842 | map of places by size (see maptest), size classes, persons per house, church building over time |
| F5 | `berufe-gewerbe` | Berufe, Gewerbe und Industrie 1864 | t1-3-1 | wirtschaft-berufsklassen-1864, industrie-gewerbe-1864-einzelne-gewerbe, industrie-hauptzweige-staedte-plattland-1864, handel-gewerbe-nach-landesteilen-1864 | occupational classes, the big trades (weavers!) by district, towns vs. countryside |
| F5 | `landwirtschaft` | Boden, Besitz und Ernte | t1-3-2 | landwirtschaft-bodennutzung-1854, landwirtschaft-grundbesitz-1854, landwirtschaft-ernte-versorgung, landwirtschaft-agrarreformen-1836-1868, landwirtschaft-kammer-rittergueter-1854, wirtschaft-loehne-pacht-landwirtschaft-1860er | land use by district, holding sizes, self-sufficiency in grain, wages |
| F5 | `viehzucht` | Viehbestand 1843–1867 | t1-3-3 | viehzucht-bestand-1843-1867, orte-viehbestand-1867 | change by species (dumbbell 1843→1867), cattle per place on a map |
| F5 | `wald-holz` | Wald und Holz | t1-3-4 | forstwirtschaft-waldflaeche-besitz, forstwirtschaft-holzpreise-zuwachs | forest ownership, wood prices 1800–1868 (indexed lines) |
| F6 | `bergbau` | Bergbau, Hütten und Salz | t1-3-5 | bergbau-bestand-oberland-vor-1648, bergbau-erzbergbau-zeitleiste-ober-unterland, bergbau-huettenwerke-oberland-betriebszeiten, bergbau-saline-heinrichshall-absatz-1857-1863, bergbau-schieferbrueche-lobenstein-1868 | Gantt of works in operation, salt sales, mines before 1648 |
| F6 | `handel-verkehr` | Handel, Märkte und Verkehr | t1-3-7 | handel-verkehr-begleitscheine-1858-1867, verkehr-eisenbahn-geldinstitute-zeitleiste, handel-jahrmaerkte-marktorte-landesteile, staat-chausseen-laenge-kosten-1868, kultur-zeitungsbezug-durch-die-post | timeline of railways/banks, markets per town (map), trade volumes |
| F6 | `staatsfinanzen` | Staatshaushalt, Schulden und Versicherung | t1-4-3 | staat-haushalt-einnahmen-ausgaben-1866-1868, staat-schulden-kassenscheine-1857-1866, versicherung-feuerversicherung-1867-orte | where the money came from and went (sorted bars), debt over time |
| F6 | `rechtspflege` | Gerichte und Strafen 1864–1867 | t1-4-4 | justiz-freiwillige-gerichtsbarkeit-1864-1867, justiz-gefangene-hafttage-1864-1867, justiz-kreisgerichte-berufungen-konkurse-1864-1867, justiz-strafsachen-einzelrichter-uebertretungen-1864-1867, justiz-strafsachen-kreisgerichte-staatsanwaltschaft-1864-1867, justiz-zivilrechtspflege-einzelgerichte-1864-1867 | one overview of caseloads, offences ranked, prisoners |
| F7 | `verfassung-verwaltung` | Landtag, Verwaltung und Militär | t1-4-1b | verfassung-landtag-gemeinderaete-vertretung, verwaltung-aerzte-gendarmen-justizaemter-landestheile, militaer-kontingent-reichsmatrikel-bis-1867 | representation in the Landtag vs. population, officials per district, contingent over time |
| F7 | `kirche-schule` | Kirchen und Schulen | t1-4-6 | kirche-ephorien-pfarreien-besoldung-1868, schule-volksschulen-schueler-lehrer-1863-1868, schule-hoehere-anstalten-schueler-lehrer-1868, orte-schulen-gemeindehaushalt | pupils per teacher by district, school places on a map, clergy pay |
| F7 | `armenwesen-stiftungen` | Armenpflege, Kassen und Stiftungen | t1-4-8 | armenwesen-selbsthilfe-kassen-gruendungsjahre-1777-1869, armenwesen-stiftungen-kapital-1828-1866, schule-stipendien-stiftungen-betraege-gruendung | foundations over time (timeline/cumulative), capital by purpose |
| F8 | `landesgeschichte` | Landesgeschichte: Erwerb, Verlust und Teilungen | t1-5 | geschichte-chronik-ereignisse-530-1867, geschichte-landerwerb-landverlust-1248-1690, geschichte-landesteilungen-linien-1240-1870 | timeline of acquisitions/losses, lines of the house as a Gantt, events per century |
| F8 | `haus-reuss` | Die Voigte und das Haus Reuß | t1-5-3 | genealogie-voigte-heinriche-1143-1572, genealogie-reuss-lebensdauer-kindersterblichkeit-1550-1850 | life spans as lines (Gantt), child mortality by birth cohort |
| F8 | `dorfleben` | Bauern, Häusler und Handwerker in den Dörfern | t2 | orte-sozialstruktur-doerfer-1867, orte-handwerk-gewerbe-doerfer, orte-flur-boden-pacht | maps or small multiples of social structure, crafts by village, land per inhabitant and rent |
| F8 | `buch-leser` | Das Buch, seine Leser und seine Maße | subscribenten | subskribenten-leserschaft-1870, zusaetze-berichtigungen-1870, masse-gewichte-umrechnung-1869 | subscribers by place (map) and profession, corrections by chapter, the unit table as a compact reference chart |
| – | `bevoelkerung-1647-1867` | done (reference) | t1-2-1 | bevoelkerung-entwicklung-1647-1867, bevoelkerung-dichte-1834-1867, bevoelkerung-stadt-land-1833-1867 | |

Use exactly these ids (they are linked from other features). Titles may be improved. Check the
archive ids against `data/analyses/_archive/` (some are long; the table may shorten them – use the
full archived id in `merges`).
