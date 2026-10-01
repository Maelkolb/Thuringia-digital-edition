# Task type E — entity registers (adjudication of annotated names)

Read `00_common.md` first.

The transcription carries ~32,000 automatic entity annotations in 11 classes (Location, Person,
Organisation, Natural Object, Environment, Animal, Plant, Resource, Artefact, Climate, Environmental
Impact). The edition turns them into **registers** (Ortsregister, Personenregister, …) and links them to
authority files. The annotations are noisy: inflected forms (Gera's, Schleizer, Kirchen), abbreviations
(R. = Rinder in the village livestock lists), wrong classes (a river tagged as town), generic words that
are not names. Your job: one **decision** per key of your slice.

## Input

`data/entities/candidates/<group>.json`, entries sorted by frequency:

```json
{"key": "Gera", "n": 1144, "types": {"Location": 1144}, "forms": {"Gera": 1141, "Gera's": 3},
 "pages": ["3", "4", …], "n_pages": 410, "contexts": [{"page": "3", "unit": "b2", "text": "… ⟦Gera⟧ …"}],
 "brueckner_register": [{"name": "Gera", "pages": ["428"], "gemeinde": true, …}],
 "geonames_candidates": [{"geonames": 2921232, "name": "Gera", "lat": 50.88, "lon": 12.08, "code": "PPLA3", "km": 33.2}, …]}
```

`key` = the surface form without leading article and possessive 's. More context: grep
`data/entities/mentions.jsonl` (one JSON line per mention with `key`, `page`, `unit`, `ctx`) or read the
page text. Brückner's own index entries (`brueckner_register`) refer to the article of that place in
Part II — the strongest evidence for places inside the principality.

## Output

`data/entities/decisions/<package-id>.json`:

```json
{"package": "E1", "group": "places", "decisions": [
  {"key": "Gera", "action": "accept", "label": "Gera", "class": "place", "kind": "Stadt",
   "geonames": 2921232, "lat": 50.88, "lon": 12.08, "wikidata": "Q3955", "in_principality": true,
   "register_page": "428", "gloss_en": "Gera (town)"},
  {"key": "Geraer", "action": "merge", "into": "Gera"},
  {"key": "Elster", "action": "reclass", "class": "nature", "label": "Weiße Elster", "kind": "Fluss"},
  {"key": "Unterland", "action": "accept", "label": "Unterland (reußisches)", "class": "place", "kind": "Region",
   "note": "Brückner's term for the northern, lower part of the principality"},
  {"key": "im Osten", "action": "reject", "reason": "relative direction, not a name"}
]}
```

* `action`:
  - `accept` — a register entry of its own. `label` = the canonical form for the register: the place,
    person or thing as Brückner names it in the nominative (keep 1870 spelling: `Cöstritz` stays if that
    is the book's form; add the modern name in `modern`, e.g. `"modern": "Bad Köstritz"`).
  - `merge` — same entity as another key (`into` = that key, which must be accepted in your file or in
    the candidate list). Use for inflections, abbreviations, spelling variants.
  - `reclass` — accepted, but belongs to another register (`class`: place | nature | person |
    organisation | organism | concept) — e.g. a river annotated as Location.
  - `reject` — not a name / not an entity of any register (generic words, fragments, OCR noise).
    Give a `reason`.
* `class` + `kind`: places — Stadt, Dorf, Weiler, Rittergut, Mühle, Wüstung, Landestheil, Amt,
  Herrschaft, Land/Staat, Region, Gebirge, Flur …; nature — Fluss, Bach, Teich, Berg, Wald, Tal, Quelle,
  Gestein …; persons — kind = role (Landesherr, Vogt, Geistlicher, Gelehrter, Beamter …); organisation —
  Kloster, Behörde, Verein, Schule, Orden …; organism — Tier, Pflanze; concept — Bauwerk, Gerät,
  Material, Lebensraum, Wetter, Ereignis ….
* Authority links (only when **verified**, never from memory):
  - places/nature: `geonames` id + `lat`/`lon` from the candidates (choose the candidate that fits the
    context; places inside the principality are usually < 60 km from the centre). For places outside
    the candidate area (Prag, Wien, Leipzig, Nürnberg …) you may give `lat`/`lon` you are certain of and
    a verified `wikidata` id.
  - persons, organisations, major places: `wikidata` id via `python tools/wikidata_search.py "<name>"`
    — only if the hit clearly is the same entity (dates, office). Most local persons have none: fine.
  - organisms: `scientific` (Latin name, as precise as the 1870 usage allows: species, genus or family)
    and `gbif` key via `python tools/gbif_match.py "<Latin name>"` (use the usageKey of an EXACT or
    high-confidence match). Livestock and crops too (Rind → *Bos taurus*, Kartoffel → *Solanum
    tuberosum*). Generic group words (Vieh, Wild, Getreide) → accept with `kind` and no taxon.
* `gloss_en`: short English rendering for the English interface (e.g. "Kirche" → "church", "Häusler" →
  "cottager"). For persons: name unchanged, optional `description_de`/`description_en` (one line: role,
  dates if stated in the book).
* `note`: anything the register should tell the reader (ambiguities, homonyms).

Work through the **whole** slice. Singletons (n = 1) are the majority — decide them quickly from the
context (most are fine as `accept`; merge obvious variants; reject noise). Use Python to assemble the
file; keep your working notes in `data/entities/_work/<package-id>/`.

Validate: `python tools/validate_entity_decisions.py data/entities/decisions/<package-id>.json` (checks
coverage of your slice, actions, merge targets, coordinates). Must print OK.
