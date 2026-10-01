# Working on the Brückner edition — common rules for subagents

You are helping to build a scholarly digital edition of

> Georg Brückner: *Volks- und Landeskunde des Fürstenthums Reuß j. L.*, Gera: Köhler 1870
> (VIII + 840 pages; facsimile: Bayerische Staatsbibliothek, `bsb11005578`, IIIF).

The book is a 19th-century regional geography/ethnography of the principality of Reuss (younger line) in
eastern Thuringia (Gera, Schleiz, Lobenstein-Ebersdorf). Part I (pp. 1–404): nature, people, economy,
state, history. Part II (pp. 405–825): a place-by-place topography (Ortskunde). Back matter: index of
places (826–829), addenda and corrigenda incl. Brückner's own conversion table of historical units
(830–834), list of subscribers (835–840).

The text was transcribed automatically (Gemini 3 Flash, 2026) and then cleaned. Spelling is the 1870
original (Thal, Theil, Procent, Centner …) with modern umlauts and resolved long s. Do **not** modernise
quotations from the source.

Project root: `C:\Users\totom\Projects\reuss-edition` (use absolute paths; Windows; Python 3.14 is `python`,
Node is `node`; set `PYTHONIOENCODING=utf-8` when printing German text from Python).

## Where to read

| what | path |
|---|---|
| one page, citable | `data/text/pages/<page>.txt` (`<page>` = printed page label: `54`, `III`, `scan-1`) |
| a whole chapter | `data/text/sections/<section-id>.txt` (ids: `t1-1` … `t1-5`, `t2-1` … `t2-3`, `back`) |
| canonical JSON (only if you need more) | `data/pages/<scan-seq 4 digits>.json` |
| section tree | `data/structure/structure.json` |
| Brückner's unit table | `data/text/pages/831.txt`, `832.txt` (+ corrigenda 830–834) |

Line format of the text views: every block starts with `[b<n> <type>]`; footnotes `[fn<n> FOOTNOTE *)]`;
tables list their grid rows as `h1`, `r2`, `g3`, `t14` … (h = header row, r = body, g = group row,
t = total row; the number is the 1-based row index of the grid, columns are separated by ` | `).
Cite sources as page label + block id, e.g. `{"page": "54", "block": "b4", "rows": "r2-r13"}`.

## Checking the print (facsimile)

The transcription is good but not perfect, especially in dense number tables. When numbers look
implausible (a printed total does not match the sum, a value is out of line, a column looks shifted),
look at the scan:

```
python tools/facsimile.py 54                       # whole page
python tools/facsimile.py 54 --crop 0,0.45,1,0.75  # region x0,y0,x1,y1 as fractions
```

It prints a local JPEG path; open it with the Read tool. Record every confirmed misreading in your
output (`transcription_issues`), with the transcribed and the printed value. Never silently "fix" a
number without checking the scan.

## Search metadata (every package does this for every page in its range)

Write `data/search/pages/<package-id>.json`:

```json
{
  "package": "A07",
  "pages": [
    {
      "page": "117",
      "summary_de": "Ein bis zwei sachliche Sätze: worum geht es auf dieser Seite?",
      "summary_en": "One or two factual sentences in English.",
      "keywords_de": ["Selbstmord", "Unglücksfälle", "Taubstumme", "Blinde"],
      "keywords_en": ["suicide", "accidents", "deaf-mute", "blind"],
      "subjects": ["Sterblichkeit", "Gesundheit"]
    }
  ],
  "glossary": [
    {"term": "Morgen", "variants": ["Mrg."], "kind": "unit", "de": "Flächenmaß; 1 preuß. Morgen = 0,2553 ha (S. 832).", "en": "Unit of area; 1 Prussian Morgen = 0.2553 ha (p. 832).", "pages": ["225"]}
  ]
}
```

Rules:
* One entry for **every** page label in your range (also pages with a single line; blank pages: `summary_de`: "Leerseite", `summary_en`: "Blank page", empty lists).
* Summaries describe content, they do not evaluate it. Mention the main places, persons, years and the
  kind of material (table, list, narrative). No "This page …" filler; start with the content.
* `keywords_de`: 3–10 search terms a modern user would type, **modern spelling** (Tal, Teil, Prozent,
  Zentner) — the original spelling is already in the full text. Include important proper names.
* `keywords_en`: English equivalents (terms, not translations of names).
* `subjects`: 1–4 terms from `docs/agents/subjects.txt` (exact spelling). Add a new subject only if
  nothing fits, prefixed with `+` (e.g. `"+Glockenkunde"`).
* `glossary`: historical terms, units, currencies, offices, dialect words a modern reader needs explained
  (`kind`: unit | currency | term | office | dialect | institution). Short, factual, sourced where
  possible (Brückner's own table on pp. 831–832 first). Do not repeat a term another page already
  defined in your file — add the page to its `pages` list instead.

Validate: `python tools/validate_search_meta.py data/search/pages/<package-id>.json` (must print OK).

## Ground rules

* Write only inside the output paths named in your task. Never edit `data/pages`, `data/text`,
  `pipeline/` or `site/`.
* Every number you quote in prose must be computed (Python) from the data you extracted — not from
  memory or mental arithmetic.
* German and English texts are written separately, idiomatically; English uses British or American
  spelling consistently (choose American).
* Be scholarly and plain: no hype ("fascinating", "remarkable"), no speculation presented as fact; mark
  interpretations as such ("deutet darauf hin", "suggests").
* When you finish, reply with a short report: files written, what you covered, what you skipped and
  why, transcription problems found.
