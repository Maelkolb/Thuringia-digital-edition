# Task type G — Ortskunde gazetteer (Part II, pp. 407–825)

Read `00_common.md` first.

Part II describes every place of the principality in a fixed pattern: name with historical forms
("urkundlich 1358 Czwoczen …"), type ("Kirch- und Grenzdorf"), location and distance ("¾ Stunde südlich
von Gera"), setting, history, church/parish, school (pupils), houses and inhabitants, occupations,
crafts, area of the parish land (Flur) in Morgen and soil quality, municipal finances, notable
features. Your job is to turn the articles in your page range into structured, source-referenced
records. They feed the edition's place register, map and statistical analyses.

## Which articles

Brückner's own index (`data/registers/ortsregister.json`, parsed from pp. 826–829) lists every
Gemeinde (no parent), Wüstung (`wuestung: true`) and Bestandtheil (with `parents`, e.g. a mill belonging
to a village) with page numbers. Your package prompt gives you the list of index entries whose page lies
in your range. Create:

* one **entry** for every article that starts in your range: every Gemeinde, every Wüstung that has its
  own paragraph, and the opening chapter articles of the district (e.g. the overview of Landestheil
  Gera, the town of Gera itself — towns get one entry, their quarters go into `subplaces`);
* Bestandtheile (mills, manors, single farms, forester's houses …) go into the `subplaces` list of the
  entry whose article mentions them.

An article ends where the next article begins. If your last article continues beyond your page range,
read it to its end.

## Output

`data/gazetteer/<package-id>.json`:

```json
{
  "package": "G1",
  "pages": "407-468",
  "entries": [
    {
      "id": "zwoetzen",
      "name": "Zwötzen",
      "start": {"page": "451", "block": "b2"},
      "end": {"page": "452", "block": "b4"},
      "landestheil": "Gera",
      "type_verbatim": "Kirch- und Grenzdorf",
      "type": "Dorf",
      "wuestung": false,
      "historic_forms": [{"form": "Zwecen", "year": null}, {"form": "Czwoczen", "year": 1358}],
      "dialect_form": "Zwiezen",
      "first_mention_year": 1358,
      "location": {"verbatim": "3/4 Stunde südlich von Gera", "relative_to": "Gera", "distance_hours": 0.75, "direction": "S"},
      "elevation": {"value": 610, "unit": "Fuß", "verbatim": "610' hoch"},
      "parish": {"status": "Kirchdorf", "church_of": null, "verbatim": "Kirch- und Grenzdorf"},
      "school": {"exists": true, "pupils": 104},
      "houses": 87,
      "inhabitants": 1265,
      "occupations": {"Bauern": 3, "Häusler": 38, "Taglöhner": 12, "Dienstboten": 20, "Handwerker": 26},
      "crafts": {"Harmonikamacher": 3, "Bäcker": 2, "Schmied": 1},
      "flur_morgen": 706.54,
      "flur_verbatim": "706 7/13 Morgen",
      "soil": "2/3 gering, 1/3 gut",
      "livestock": {"Pferde": 4, "Rinder": 120},
      "municipal_finances": {"verbatim": "1 Morgen Wiesen im Werthe von 100 Thlr., … 900 Thlr. Schulden … circa 175 Thlr.", "assets_thaler": 100, "debts_thaler": 900, "expenditure_thaler": 175},
      "facilities": ["Kirche", "Schule", "Brauerei", "Mühle", "Ziegelei", "Feuerspritze"],
      "subplaces": [{"name": "Fuchsmühle", "kind": "Mühle", "page": "452"}],
      "events": [{"year": 1640, "event_de": "Brand", "event_en": "fire"}],
      "persons": ["Heinrich LXVII."],
      "summary_de": "2–3 Sätze: Lage, Charakter, Besonderheiten.",
      "summary_en": "2–3 sentences in English."
    }
  ]
}
```

Rules:
* `id`: ASCII slug of the name (ä→ae, ö→oe, ü→ue, ß→ss; lower case; hyphens), unique; disambiguate
  homonyms with the Landestheil or parent (`dittersdorf-tanna`).
* `type`: one of `Stadt`, `Marktflecken`, `Dorf`, `Weiler`, `Rittergut`, `Kammergut`, `Vorwerk`,
  `Mühle`, `Einzelhof`, `Wüstung`, `Schloss`, `Gewerbeanlage`, `Landestheil`, `Sonstiges`.
* Use **only** what the text says. Omit a field (do not write `null` or guess) when the article does not
  give it. Numbers exactly as printed; fractions converted (`706 7/13` → 706.54, keep `*_verbatim`).
  `distance_hours`: Stunden as a number (¾ → 0.75); `direction`: N, NO, O, SO, S, SW, W, NW (+ NNO …)
  as printed (German letters).
* `occupations`/`crafts`/`livestock`/`facilities`: keys as printed (nominative singular or plural as in
  the text), values = counts. A list "3 Harmonikamacher, Zeugarbeiter und Zimmerleute" means 3 of each.
* `inhabitants`/`houses`: the figures for the place itself (not the parish). If several years are given,
  use the latest and add `"census_year"` when stated.
* `events`: only dated events (fires, foundations, sales, wars, plagues, church buildings), short.
* Keep summaries factual (no evaluation), German and English written separately.

Validate: `python tools/validate_gazetteer.py data/gazetteer/<package-id>.json` — checks structure,
ids, that block references exist, and that every number appears in the article text. Must print OK.

Then write the search metadata for every page of your range (common rules).
