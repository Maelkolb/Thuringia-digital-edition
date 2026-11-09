"""Stage 4c - polish the entity registry for readers.

Rewrites data/entities/registry.json in place:
    notes.json            bilingual notes: sets note_de / note_en, removes note (null drops it)
    kinds_en.json         English label of every kind: sets kind_en
    polish_overrides.json German kind spellings ("kind") and whole-field text corrections ("text")
and fixes typography in the reader-facing text fields (en dash in ranges, German page
references and ordinal dots in English, typographic quotes). Running it again changes nothing.
"""
from __future__ import annotations

import re

from common import DATA, read_json, write_json

ENTITIES = DATA / "entities"
GERMAN_FIELDS = ("description_de", "note_de")
ENGLISH_FIELDS = ("description_en", "gloss_en", "note_en")

ROMAN = r"[IVXL]+"
RULER_NAMES = ("Heinrich|Friedrich|Karl|Ludwig|Johann|Georg|Wilhelm|Otto|Albrecht|Albert|Rudolf|Wenzel|Sigismund|"
               "Maximilian|Ferdinand|Leopold|Joseph|Franz|Alexander|Napoleon|Gregor|Gregory|Innocent|Clemens|Clement|"
               "Pius|Boniface|Benedict|August|Christian|Ernst|Philipp|Adolf|Conrad|Konrad|Lothar|Günther|Hermann|"
               "Bernhard|Louis|Charles|Henry|Frederick|William|George|John|Urban|Leo|Paul|Eugen")
ORDINAL = re.compile(rf"\b({ROMAN})\.(?=[\s,;:)–/]|$)")
KEEP_AS_PRINTED = re.compile(r"“[^”]*”|\"[^\"]*\"|\bsee [A-ZÄÖÜ][^;)]*\)?")
AFTER_RULER_NAME = re.compile(rf"\b(?:{RULER_NAMES})\s+(?:{ROMAN}\.?(?:,\s*|\s+(?:and|or)\s+|\s*[–/]\s*))*$")
GERMAN_PAGE_REF = re.compile(r"\bS\. (\d+(?:\s*[–-]\s*\d+)?(?:(?:,\s*|\s+(?:und|and)\s+)\d+(?:\s*[–-]\s*\d+)?)*)")


def en_dash_ranges(text: str) -> str:
    text = re.sub(r"(?<=\d)(\.?)\s?-\s?(?=\d|(?:c|ca|um|nach|vor|after|before)\.? \d)", r"\1–", text)
    return re.sub(r"(?<=\d(?:st|nd|rd|th))-(?=\d)", "–", text)


def drop_ordinal_dots(text: str) -> str:
    quoted_or_cross_reference = [m.span() for m in KEEP_AS_PRINTED.finditer(text)]

    def plain_numeral(m: re.Match) -> str:
        if not text[m.end():].strip() or any(start <= m.start() < end for start, end in quoted_or_cross_reference):
            return m.group(0)
        if len(m.group(1)) > 1 or AFTER_RULER_NAME.search(text[:m.start()]):
            return m.group(1)
        return m.group(0)
    return ORDINAL.sub(plain_numeral, text)


def english_references(text: str) -> str:
    def page_ref(m: re.Match) -> str:
        pages = m.group(1).replace(" und ", " and ")
        return ("pp. " if re.search(r"[–,]| and ", pages) else "p. ") + pages
    text = GERMAN_PAGE_REF.sub(page_ref, text)
    text = re.sub(rf"\bTab\. (?={ROMAN}\b)", "Table ", text)
    return re.sub(r"\bAnm\.", "note", text)


def german_references(text: str) -> str:
    text = re.sub(r"\bpp?\. (?=\d)", "S. ", text)
    return re.sub(r"\bc\. (?=\d)", "ca. ", text)


def english_house_names(text: str) -> str:
    text = text.replace("younger line of Reuss (Reuss j. L.)", "younger line of Reuss")
    return text.replace("Reuss j. L.", "Reuss (younger line)").replace("Reuss ä. L.", "Reuss (elder line)")


def english_quotes(text: str) -> str:
    text = re.sub(r"(?<=\d)'", "′", text)
    text = re.sub(r"„([^„“”\"]*)[“”\"]", r"“\1”", text)
    text = re.sub(r"\"([^\"]*)\"", r"“\1”", text)
    text = re.sub(r"(?<![\w’])'([^']+?)'(?!\w)", r"“\1”", text)
    return text.replace("'", "’")


def german_quotes(text: str) -> str:
    text = re.sub(r"(?<=\d)'", "′", text)
    text = re.sub(r"„([^„“”\"]*)[”\"]", r"„\1“", text)
    text = re.sub(r"\"([^\"]*)\"", r"„\1“", text)
    text = re.sub(r"(?<![\w’])'([^']+?)'(?!\w)", r"„\1“", text)
    return text.replace("'", "’")


def polish_german(text: str) -> str:
    return german_quotes(german_references(en_dash_ranges(text.strip())))


def polish_english(text: str) -> str:
    return english_quotes(drop_ordinal_dots(english_references(english_house_names(en_dash_ranges(text.strip())))))


def polish_entity(entity: dict, notes: dict, kinds_en: dict, overrides: dict, problems: dict) -> None:
    if entity.get("kind"):
        entity["kind"] = overrides["kind"].get(entity["kind"], entity["kind"])
        if entity["kind"] in kinds_en:
            entity["kind_en"] = kinds_en[entity["kind"]]
        else:
            problems["kinds without English"].add(entity["kind"])
    if entity["id"] in notes:
        entity.pop("note", None)
        entity.pop("note_de", None)
        entity.pop("note_en", None)
        note = notes[entity["id"]]
        if note:
            entity["note_de"], entity["note_en"] = note["de"], note["en"]
    elif "note" in entity:
        problems["notes missing from notes.json"].add(entity["id"])
    for field, text in overrides["text"].get(entity["id"], {}).items():
        entity[field] = text
    for field in GERMAN_FIELDS:
        if entity.get(field):
            entity[field] = polish_german(entity[field])
    for field in ENGLISH_FIELDS:
        if entity.get(field):
            entity[field] = polish_english(entity[field])


def main() -> None:
    path = ENTITIES / "registry.json"
    registry = read_json(path)
    notes = read_json(ENTITIES / "notes.json")
    kinds_en = read_json(ENTITIES / "kinds_en.json")
    overrides = read_json(ENTITIES / "polish_overrides.json")
    problems = {"kinds without English": set(), "notes missing from notes.json": set()}
    for entity in registry["entities"]:
        polish_entity(entity, notes, kinds_en, overrides, problems)
    write_json(path, registry, indent=None)
    with_notes = sum(1 for e in registry["entities"] if e.get("note_de"))
    print(f"polished {len(registry['entities'])} entities; {with_notes} with notes")
    for name, items in problems.items():
        if items:
            print(f"{name} ({len(items)}): {', '.join(sorted(items)[:20])}")


if __name__ == "__main__":
    main()
