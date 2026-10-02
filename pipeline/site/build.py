"""Build the static edition website into ./site

    python pipeline/site/build.py [--skip-charts] [--pages 20,54]

Everything is generated from data/: canonical pages, structure, entity
registry, gazetteer, analyses, search metadata. The output is a plain static
site (no server code) that can be hosted anywhere (GitHub Pages, a
university web server) and opened locally via `python -m http.server`.
"""
from __future__ import annotations

import argparse
import base64
import collections
import datetime as dt
import html
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

from jinja2 import Environment, FileSystemLoader  # noqa: E402

from common import DATA, MDZ_VIEWER, PAGES_DIR, ROOT, read_json, write_text_atomic  # noqa: E402
import render as R  # noqa: E402
import search_index  # noqa: E402

SITE = ROOT / "site"
SRC = ROOT / "site_src"
NODE = ROOT / "tools" / "node_modules"
DATA_SCRIPT_DIRS = ("suche", "auswertungen/specs", "karte", "register/belege")
esc = R.esc

CLASSES = [
    # class, file, label_de, label_en, intro_de, intro_en
    ("place", "orte", "Orte", "Places", "Städte, Dörfer, Wüstungen, Landesteile und Regionen. Orte des Fürstentums sind mit Brückners Ortsartikel (II. Theil) verknüpft.",
     "Towns, villages, deserted settlements, districts and regions. Places of the principality link to Brückner's topographical article (Part II)."),
    ("nature", "natur", "Gewässer, Berge, Wälder", "Natural features", "Flüsse, Bäche, Teiche, Berge, Wälder und Täler.", "Rivers, streams, ponds, mountains, forests and valleys."),
    ("person", "personen", "Personen", "Persons", "Personen, die Brückner nennt – Landesherren, Geistliche, Beamte, Gelehrte. Mehrdeutige Namensformen (z. B. „Heinrich d. ä.“) sind als solche gekennzeichnet.",
     "Persons named by Brückner – rulers, clergy, officials, scholars. Ambiguous name forms (e.g. “Heinrich d. ä.”) are marked as such."),
    ("organisation", "institutionen", "Institutionen", "Institutions", "Klöster, Orden, Behörden, Schulen, Vereine und Körperschaften.", "Monasteries, orders, authorities, schools, societies and corporations."),
    ("organism", "organismen", "Tiere und Pflanzen", "Animals and plants", "Tiere und Pflanzen mit wissenschaftlichem Namen und GBIF-Verknüpfung, soweit bestimmbar.", "Animals and plants with scientific name and GBIF link where identifiable."),
    ("concept", "sachen", "Sachen und Begriffe", "Things and concepts", "Bauwerke, Geräte, Rohstoffe, Lebensräume, Wetter und Ereignisse.", "Buildings, objects, resources, habitats, weather and events."),
]
CLASS_FILE = {c[0]: c[1] for c in CLASSES}
ANA_GROUPS = [
    ("t1-1", "natur", "Die Natur des Landes", "The nature of the land"),
    ("t1-2", "volk", "Das Volk", "The people"),
    ("t1-3", "wirtschaft", "Erwerbsleben", "Economic life"),
    ("t1-4", "staat", "Der Staat", "The state"),
    ("t1-5", "geschichte", "Geschichte des Landes und des Fürstenhauses", "History of the land and the princely house"),
    ("t2", "orte", "Ortskunde", "The places"),
    ("", "buch", "Das Buch und seine Leser", "The book and its readers"),
]
BLOCK_KIND = {"table": ("Tabelle", "table"), "list": ("Liste", "list"), "paragraph": ("Text", "text"), "heading": ("Überschrift", "heading")}


def ana_group(section: str) -> tuple:
    for prefix, gid, de, en in ANA_GROUPS:
        if prefix and (section == prefix or section.startswith(prefix + "-") or section.startswith(prefix + "b")):
            return gid, de, en
    return ANA_GROUPS[-1][1:]


def teaser(text: str, limit: int = 150) -> str:
    first = re.split(r"(?<=[.!?])\s", text.strip(), maxsplit=1)[0]
    return first if len(first) <= limit else first[:limit].rsplit(" ", 1)[0] + " …"


CAT_LABEL = {
    "geography": ("Geographie", "Geography"), "relief": ("Relief", "Relief"), "geology": ("Geologie", "Geology"),
    "hydrology": ("Gewässer", "Hydrology"), "climate": ("Klima", "Climate"), "phenology": ("Phänologie", "Phenology"),
    "flora": ("Pflanzenwelt", "Flora"), "fauna": ("Tierwelt", "Fauna"), "population": ("Bevölkerung", "Population"),
    "health": ("Gesundheit", "Health"), "housing": ("Wohnen", "Housing"), "culture": ("Volkskultur", "Folk culture"),
    "dialect": ("Mundart", "Dialect"), "economy": ("Wirtschaft", "Economy"), "agriculture": ("Landwirtschaft", "Agriculture"),
    "livestock": ("Viehzucht", "Livestock"), "forestry": ("Forstwirtschaft", "Forestry"), "mining": ("Bergbau", "Mining"),
    "industry": ("Industrie", "Industry"), "trade-transport": ("Handel und Verkehr", "Trade and transport"),
    "state": ("Staat", "State"), "finance": ("Finanzen", "Finance"), "justice": ("Rechtspflege", "Justice"),
    "military": ("Militär", "Military"), "church": ("Kirche", "Church"), "education": ("Schule", "Education"),
    "welfare": ("Armenwesen", "Welfare"), "history": ("Geschichte", "History"), "genealogy": ("Genealogie", "Genealogy"),
    "places": ("Ortskunde", "Topography"), "reception": ("Rezeption", "Reception"),
}
RULES = {
    "join_linebreak_hyphen": ("Silbentrennung aufgelöst", "Line-break hyphen joined"),
    "join_inword_hyphen": ("Trennstrich im Wort getilgt", "In-word hyphen removed"),
    "table_no_header_row": ("Tabelle: erste Zeile als Datenzeile statt als Kopf", "Table: first row shown as data, not header"),
    "table_multirow_header": ("Tabelle: mehrzeiliger Kopf mit verbundenen Zellen rekonstruiert", "Table: multi-row header with merged cells rebuilt"),
    "table_group_rows": ("Tabelle: Zwischenzeilen als Gruppenzeilen", "Table: interim rows as group rows"),
    "table_join_split_stub": ("Tabelle: getrennte Zeilenbeschriftung zusammengeführt", "Table: split row label joined"),
    "table_drop_empty_columns": ("Tabelle: leere Spalten entfernt", "Table: empty columns removed"),
    "table_pad_ragged_rows": ("Tabelle: ungleich lange Zeilen aufgefüllt", "Table: ragged rows padded"),
    "drop_empty_table": ("Leere Tabelle verworfen", "Empty table dropped"),
    "signature_from_footnote": ("Bogensignatur war als Fußnote erkannt – als Signatur ausgewiesen", "Printer’s signature had been read as a footnote"),
    "signature_from_page_number": ("Bogensignatur war als Seitenzahl erkannt", "Printer’s signature had been read as page number"),
    "signature_from_paragraph": ("Bogensignatur war als Absatz erkannt", "Printer’s signature had been read as a paragraph"),
    "drop_header_equal_to_opening_heading": ("Kolumnentitel gleich Kapitelüberschrift – nicht doppelt wiedergegeben", "Running head equals chapter heading – not repeated"),
    "manual_blank": ("Leerseite: Transkription des Durchscheinens verworfen", "Blank page: transcription of show-through discarded"),
    "manual_promote_heading": ("Überschrift als solche ausgezeichnet", "Heading marked as heading"),
    "manual_drop_block": ("Block verworfen", "Block dropped"),
    "strip_dot_leaders": ("Füllpunkte (Inhaltsverzeichnis) entfernt", "Dot leaders removed"),
    "resolve_long_s": ("Langes ſ als s wiedergegeben", "Long s rendered as s"),
    "manual_insert_block": ("Fehlender Block nach dem Faksimile ergänzt", "Missing block restored from the facsimile"),
    "facsimile_correction": ("Fehllesung am Faksimile berichtigt", "Misreading corrected against the facsimile"),
}


def i18n(attr: str, de: str, en: str) -> str:
    """An attribute that follows the interface language (see applyLang in edition.js)."""
    de, en = html.escape(de, quote=True), html.escape(en, quote=True)
    return f'{attr}="{de}" data-de-{attr}="{de}" data-en-{attr}="{en}"'


def num(n, lang: str = "de") -> str:
    if not isinstance(n, int):
        return str(n)
    s = f"{n:,}"
    return s.replace(",", ".") if lang == "de" else s


def t(de: str, en: str) -> str:
    return R.t(de, en)


def fold(s: str) -> str:
    s = s.lower().replace("ß", "ss")
    return "".join(ch for ch in unicodedata.normalize("NFD", s) if unicodedata.category(ch) != "Mn")


def sort_key(s: str) -> str:
    s = re.sub(r"^[^A-Za-zÄÖÜäöüß0-9]+", "", s)
    return fold(s)


class Builder:
    def __init__(self, skip_charts: bool, only_pages: set[str] | None):
        self.skip_charts = skip_charts
        self.only_pages = only_pages
        self.site = read_json(DATA / "site.json")
        self.env = Environment(loader=FileSystemLoader(str(SRC / "templates")), autoescape=False, trim_blocks=True, lstrip_blocks=True)
        self.env.globals["t"] = t
        self.env.globals["i18n"] = i18n
        self.env.globals["num"] = num
        self.pages = [read_json(f) for f in sorted(PAGES_DIR.glob("*.json"))]
        self.by_slug = {p["slug"]: p for p in self.pages}
        self.struct = read_json(DATA / "structure" / "structure.json")
        self.sections = {s["id"]: s for s in self.struct["sections"]}
        reg = read_json(DATA / "entities" / "registry.json")["entities"]
        self.entities = {e["id"]: e for e in reg}
        self.key_map = read_json(DATA / "entities" / "key_map.json")
        self.meta = {}
        self.glossary_raw = []
        for f in sorted((DATA / "search" / "pages").glob("*.json")) if (DATA / "search" / "pages").exists() else []:
            d = read_json(f)
            for p in d.get("pages", []):
                self.meta[p["page"]] = p
            self.glossary_raw += d.get("glossary", [])
        self.gazetteer = []
        for f in sorted((DATA / "gazetteer").glob("G*.json")) if (DATA / "gazetteer").exists() else []:
            self.gazetteer += read_json(f).get("entries", [])
        self.analyses = []
        for f in sorted((DATA / "analyses").glob("*.json")):
            try:
                self.analyses.append(read_json(f))
            except json.JSONDecodeError:
                pass
        self.version = self.site["version"]
        cp = DATA / "gazetteer" / "coords.json"
        self.gaz_coords = read_json(cp)["coords"] if cp.exists() else {}

    # ------------------------------------------------------------------ utils
    def write(self, rel: str, content: str) -> None:
        p = SITE / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

    def tpl(self, name: str, rel: str, **kw) -> None:
        depth = rel.count("/")
        root = "../" * depth
        ctx = dict(site=self.site, root=root, path=rel, section=kw.pop("section", ""))
        ctx.update(kw)
        self.write(rel, self.env.get_template(name).render(**ctx))

    def sec_href(self, sid: str, root: str) -> str:
        s = self.sections[sid]
        anchor = f"#{s['start_block']}" if s.get("start_block") else ""
        return f"{root}seite/{s['start_label']}.html{anchor}"

    # ------------------------------------------------------------------ assets
    def assets(self) -> None:
        if SITE.exists() and not self.only_pages:  # partial preview builds keep the rest of the site
            for child in SITE.iterdir():
                if child.name in ("auswertungen",) and self.skip_charts:
                    continue
                if child.is_dir():
                    shutil.rmtree(child)
                else:
                    child.unlink()
        a = SITE / "assets"
        shutil.copytree(SRC / "static", a, dirs_exist_ok=True)
        shutil.copy(SRC / "static" / "js" / "norm.js", a / "js" / "norm.js")
        fonts = a / "fonts"
        fonts.mkdir(parents=True, exist_ok=True)
        for src in [NODE / "@fontsource-variable/newsreader/files/newsreader-latin-wght-normal.woff2",
                    NODE / "@fontsource-variable/newsreader/files/newsreader-latin-ext-wght-normal.woff2",
                    NODE / "@fontsource-variable/newsreader/files/newsreader-latin-wght-italic.woff2",
                    NODE / "@fontsource-variable/source-sans-3/files/source-sans-3-latin-wght-normal.woff2",
                    NODE / "@fontsource-variable/source-sans-3/files/source-sans-3-latin-ext-wght-normal.woff2",
                    NODE / "@fontsource-variable/source-sans-3/files/source-sans-3-latin-wght-italic.woff2",
                    NODE / "@fontsource/ibm-plex-mono/files/ibm-plex-mono-latin-400-normal.woff2",
                    NODE / "@fontsource/ibm-plex-mono/files/ibm-plex-mono-latin-500-normal.woff2"]:
            shutil.copy(src, fonts / src.name)
        self.offline_fonts(a)
        v = a / "vendor"
        (v / "openseadragon").mkdir(parents=True, exist_ok=True)
        shutil.copy(NODE / "openseadragon/build/openseadragon/openseadragon.min.js", v / "openseadragon")
        (v / "leaflet").mkdir(parents=True, exist_ok=True)
        for f in ("leaflet.js", "leaflet.css"):
            shutil.copy(NODE / "leaflet/dist" / f, v / "leaflet" / f)
        shutil.copytree(NODE / "leaflet/dist/images", v / "leaflet/images", dirs_exist_ok=True)
        (v / "vega").mkdir(parents=True, exist_ok=True)
        shutil.copy(NODE / "vega/build/vega.min.js", v / "vega")
        licenses = {
            "OpenSeadragon": "BSD-3-Clause", "Leaflet": "BSD-2-Clause", "Vega": "BSD-3-Clause",
            "Newsreader": "SIL Open Font License 1.1", "Source Sans 3": "SIL Open Font License 1.1", "IBM Plex Mono": "SIL Open Font License 1.1",
        }
        (v / "LICENSES.txt").write_text("\n".join(f"{k}: {val}" for k, val in licenses.items()) + "\n", encoding="utf-8")
        (a / "img" / "favicon.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#6b4423"/>'
            '<text x="32" y="44" text-anchor="middle" font-family="Georgia,serif" font-size="34" font-weight="700" fill="#fbf8f1">B</text></svg>', encoding="utf-8")

    @staticmethod
    def offline_fonts(assets_dir: Path) -> None:
        """Copy of the @font-face rules with the fonts embedded (pages opened from disk cannot load font files)."""
        css = (assets_dir / "css" / "edition.css").read_text(encoding="utf-8")
        rules = re.findall(r"@font-face\s*\{[^}]*\}", css)

        def embed(m: re.Match) -> str:
            data = base64.b64encode((assets_dir / "fonts" / m.group(1)).read_bytes()).decode("ascii")
            return f'url("data:font/woff2;base64,{data}")'

        out = [re.sub(r'url\("\.\./fonts/([^"]+)"\)', embed, r) for r in rules]
        (assets_dir / "css" / "fonts-offline.css").write_text("\n".join(out) + "\n", encoding="utf-8")

    # ------------------------------------------------------------------ registry helpers
    def register_href(self, e: dict, root: str = "") -> str:
        return f"{root}register/{CLASS_FILE[e['class']]}.html#{e['id'].split(':', 1)[1]}"

    def link_gazetteer(self) -> dict[str, dict]:
        """gazetteer id -> registry entity (place) ; adds synthetic entities where needed."""
        by_label = collections.defaultdict(list)
        for e in self.entities.values():
            if e["class"] == "place":
                by_label[fold(e["label"])].append(e)
        out = {}
        for g in self.gazetteer:
            cands = by_label.get(fold(g["name"]), [])
            pick = None
            for e in cands:
                if str(e.get("register_page", "")) == g["start"]["page"] or e.get("in_principality"):
                    pick = e
                    break
            if pick is None and cands:
                pick = max(cands, key=lambda e: e["n"])
            if pick is None:
                eid = f"place:{R.surface_key(g['id'], 'Location')}"
                eid = "place:" + re.sub(r"[^a-z0-9-]", "-", g["id"])
                pick = {"id": eid, "class": "place", "label": g["name"], "kind": g.get("type"), "keys": [], "forms": {}, "n": 0,
                        "pages": [], "fallback": False, "in_principality": True}
                self.entities[eid] = pick
            pick.setdefault("gazetteer", []).append(g)
            c = self.gaz_coords.get(g["id"])
            if c and not pick.get("coords"):
                pick["coords"] = [c["lat"], c["lon"]]
                pick.setdefault("geonames", c.get("geonames"))
            out[g["id"]] = pick
        return out

    # ------------------------------------------------------------------ pages
    def build_pages(self) -> None:
        order = [p["slug"] for p in self.pages]
        ana_by_page = collections.defaultdict(list)
        for a in self.analyses:
            for s in a.get("sources", []):
                if a not in ana_by_page[s["page"]]:
                    ana_by_page[s["page"]].append(a)
        gaz_by_page = collections.defaultdict(list)
        for g in self.gazetteer:
            gaz_by_page[g["start"]["page"]].append(g)
        corr_by_page = self.author_corrections()
        subj_ids = {s: re.sub(r"[^a-z0-9]+", "-", fold(s)).strip("-") for s in self.subject_list()}
        renderer = R.Renderer("../", self.key_map, self.entities)
        for i, p in enumerate(self.pages):
            if self.only_pages and p["slug"] not in self.only_pages:
                continue
            prev_slug = order[i - 1] if i > 0 else None
            next_slug = order[i + 1] if i + 1 < len(order) else None
            lines = self.page_lines(p)
            body = renderer.page(p, prev_slug, next_slug, lines) if p["kind"] == "text" else ""
            used = renderer.used if p["kind"] == "text" else {}
            groups = []
            for cls, file, lde, len_, _, _ in CLASSES:
                items = [(self.entities[eid], n) for eid, n in used.items() if self.entities[eid]["class"] == cls]
                if not items:
                    continue
                items.sort(key=lambda x: (-x[1], sort_key(x[0]["label"])))
                groups.append({"cls": cls, "label_de": lde, "label_en": len_, "entries": [
                    {"id": e["id"], "label": e["label"], "n": n, "href": self.register_href(e, "../")} for e, n in items]})
            ent_json = {eid: {"l": e["label"], "c": e["class"], "k": e.get("kind") or "", "n": e["n"],
                              "m": e.get("modern") or "", "d": e.get("description_de") or e.get("gloss_en") or "",
                              "de": e.get("description_en") or e.get("gloss_en") or ""}
                        for eid in used for e in [self.entities[eid]]}
            crumbs = []
            for sid in p.get("section_path", []):
                s = self.sections[sid]
                short = f"{s.get('num', '')} {s['title']}".strip()
                crumbs.append({"href": self.sec_href(sid, "../"), "title": short, "short": short if len(short) < 42 else short[:40] + "…"})
            meta = self.meta.get(p["slug"], {})
            label = p["label"] or f"Scan {p['seq']}"
            corrections = []
            for c in p["corrections"]:
                de, en = RULES.get(c["rule"], (c["rule"], c["rule"]))
                detail = ""
                if c.get("before"):
                    detail = t(f": „{esc(c['after'])}“ statt „{esc(c['before'])}“", f": “{esc(c['after'])}” instead of “{esc(c['before'])}”")
                elif c.get("value"):
                    detail = f": „{esc(c['value'])}“"
                corrections.append(t(de, en) + detail)
            jsonld = json.dumps({
                "@context": "https://schema.org", "@type": "WebPage", "name": f"Brückner 1870, {label}",
                "isPartOf": {"@type": "Book", "name": "Volks- und Landeskunde des Fürstenthums Reuß j. L.", "author": {"@type": "Person", "name": "Georg Brückner"},
                             "datePublished": "1870", "publisher": "Köhler, Gera", "sameAs": "https://mdz-nbn-resolving.de/urn:nbn:de:bvb:12-bsb11005578-4"},
                "image": f"{p['iiif']['service']}/full/600,/0/default.jpg", "inLanguage": "de", "license": self.site["license_url"],
            }, ensure_ascii=False)
            self.tpl("page.html", f"seite/{p['slug']}.html", section="read", page=p, body=body, prev_slug=prev_slug, next_slug=next_slug,
                     crumbs=crumbs, meta=meta, subjects=[{"id": subj_ids.get(s, ""), "label": s} for s in meta.get("subjects", []) if not s.startswith("+")],
                     ent_groups=groups, ent_json=json.dumps(ent_json, ensure_ascii=False).replace("</", "<\\/"),
                     analyses=[{"id": a["id"], "title": a["title"], "cat_de": CAT_LABEL.get(a["category"], ("", ""))[0],
                                "cat_en": CAT_LABEL.get(a["category"], ("", ""))[1]} for a in ana_by_page.get(p["slug"], [])],
                     gazetteer=[{"name": g["name"], "type": g.get("type_verbatim") or g.get("type"), "inhabitants": g.get("inhabitants"),
                                 "anchor": self.gaz_anchor.get(g["id"], "")} for g in gaz_by_page.get(p["slug"], [])],
                     author_corrections=corr_by_page.get(p["slug"], []), corrections=corrections,
                     mdz_url=MDZ_VIEWER.format(seq=p["seq"]), jsonld=jsonld,
                     has_lines=bool(lines and lines["lines"]), lines_json=self.lines_json(p, lines))

    @staticmethod
    def page_lines(page: dict) -> dict | None:
        f = DATA / "lines" / "aligned" / f"{page['seq']:04d}.json"
        return read_json(f) if f.exists() and page["kind"] == "text" else None

    @staticmethod
    def lines_json(page: dict, lines: dict | None) -> str:
        """Line zones for the facsimile overlay, scaled to the IIIF image size the viewer uses."""
        if not lines or not lines["lines"]:
            return ""
        sx, sy = page["iiif"]["width"] / lines["width"], page["iiif"]["height"] / lines["height"]

        def scale(b: list[int]) -> list[int]:
            return [round(b[0] * sx), round(b[1] * sy), round(b[2] * sx), round(b[3] * sy)]

        data = {"l": [[l["id"], l["n"] or 0, l["unit"].split(".")[0]] + scale(l["box"]) for l in lines["lines"]],
                "r": {k: scale(v) for k, v in lines["regions"].items()}}
        return json.dumps(data, separators=(",", ":"))

    def author_corrections(self) -> dict[str, list]:
        """Brückner's 'Zusätze und Berichtigungen' (pp. 830-834) linked to the pages they concern."""
        out = collections.defaultdict(list)
        for slug in ("830", "831", "832", "833", "834"):
            p = self.by_slug.get(slug)
            if not p:
                continue
            for b in p["blocks"]:
                if b["type"] != "paragraph":
                    continue
                current = None
                for line in b["text"].split("\n"):
                    m = re.match(r"^S\.\s*(\d{1,3})\b", line.strip())
                    if m:
                        current = m.group(1)
                    if current and current in self.by_slug:
                        out[current].append({"text": line.strip(), "page": slug, "block": b["id"]})
        return out

    # ------------------------------------------------------------------ toc
    def build_toc(self) -> None:
        def node(sid: str) -> dict:
            s = self.sections[sid]
            pages = []
            if not s.get("children"):
                for p in self.pages:
                    if s["start_seq"] <= p["seq"] <= s["end_seq"] and p["slug"] in self.meta:
                        pages.append({"slug": p["slug"], "label": p["label"] or f"Scan {p['seq']}", "summary_de": self.meta[p["slug"]].get("summary_de", ""),
                                      "summary_en": self.meta[p["slug"]].get("summary_en", "")})
            printed = [p["label"] for p in self.pages if s["start_seq"] <= p["seq"] <= s["end_seq"] and p["label"]]
            first = s["start_label"] if not s["start_label"].startswith("scan-") or not printed else printed[0]
            last = s["end_label"] if not s["end_label"].startswith("scan-") or not printed else printed[-1]
            pp = f"{first}–{last}" if first != last else first
            pp = pp.replace("scan-", "Scan ")
            return {"id": sid, "num": s.get("num", ""), "title": s["title"], "title_en": s.get("title_en", ""),
                    "href": self.sec_href(sid, ""), "pp": pp,
                    "depth": s["depth"], "children": [node(c) for c in s.get("children", [])], "pages": pages}
        tree = [node(r) for r in self.struct["roots"]]
        self.tpl("toc.html", "inhalt.html", section="toc", tree=tree)

    # ------------------------------------------------------------------ registers
    def build_registers(self) -> None:
        mentions = collections.defaultdict(list)
        with open(DATA / "entities" / "mentions.jsonl", encoding="utf-8") as f:
            for line in f:
                m = json.loads(line)
                eid = self.key_map.get(f"{R.TYPE_GROUP[m['type']]}\t{m['key']}")
                if eid and len(mentions[eid]) < 40:
                    mentions[eid].append([m["page"], m["unit"].split(".")[0], m["ctx"]])
        (SITE / "register" / "belege").mkdir(parents=True, exist_ok=True)
        counts = {}
        for cls, file, lde, len_, ide, ien in CLASSES:
            ents = [e for e in self.entities.values() if e["class"] == cls and (e["n"] > 0 or e.get("gazetteer"))]
            ents.sort(key=lambda e: sort_key(e["label"]))
            counts[cls] = len(ents)
            letters = collections.OrderedDict()
            for e in ents:
                k = sort_key(e["label"])[:1].upper() or "#"
                if not k.isalpha():
                    k = "#"
                letters.setdefault(k, []).append(self.register_item(e))
            kw = {eid.split(":", 1)[1]: mentions.get(eid, []) for eid in (e["id"] for e in ents)}
            (SITE / "register" / "belege" / f"{file}.json").write_text(json.dumps(kw, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
            kinds = collections.Counter(e.get("kind") for e in ents if e.get("kind"))
            self.tpl("register.html", f"register/{file}.html", section="register", cls=cls, file=file, label_de=lde, label_en=len_,
                     intro_de=ide, intro_en=ien, letters=letters, n=len(ents), classes=CLASSES, kinds=[k for k, _ in kinds.most_common(14)])
        self.reg_counts = counts

    def register_item(self, e: dict) -> str:
        anchor = e["id"].split(":", 1)[1]
        auth = []
        if e.get("geonames"):
            auth.append(f'<a href="https://www.geonames.org/{e["geonames"]}" rel="noopener">GeoNames</a>')
        if e.get("wikidata"):
            auth.append(f'<a href="https://www.wikidata.org/wiki/{e["wikidata"]}" rel="noopener">Wikidata</a>')
        if e.get("gbif"):
            auth.append(f'<a href="https://www.gbif.org/species/{e["gbif"]}" rel="noopener">GBIF</a>')
        if e.get("coords"):
            auth.append(f'<a href="../karte.html#{anchor}">{t("Karte", "Map")}</a>')
        desc = []
        if e.get("modern") and e["modern"] != e["label"]:
            desc.append(f'{t("heute", "today")}: {esc(e["modern"])}')
        if e.get("scientific"):
            desc.append(f"<i>{esc(e['scientific'])}</i>")
        if e.get("description_de"):
            desc.append(t(esc(e["description_de"]), esc(e.get("description_en") or e["description_de"])))
        elif e.get("gloss_en"):
            desc.append(f'<span data-l="en">{esc(e["gloss_en"])}</span>')
        if e.get("note"):
            desc.append(f'<span class="muted">{esc(e["note"])}</span>')
        forms = [f for f in e.get("forms", {}) if f != e["label"]][:6]
        if forms:
            desc.append(f'<span class="muted">{t("Formen", "Forms")}: ' + ", ".join(esc(f) for f in forms) + "</span>")
        gaz = ""
        for g in e.get("gazetteer", []):
            facts = [esc(g.get("type_verbatim") or g.get("type") or "")]
            if g.get("inhabitants"):
                facts.append(t(f"{num(g['inhabitants'])} Einwohner", f"{num(g['inhabitants'], 'en')} inhabitants"))
            if g.get("houses"):
                facts.append(t(f"{num(g['houses'])} Häuser", f"{num(g['houses'], 'en')} houses"))
            if g.get("first_mention_year"):
                facts.append(t(f"urkundlich {g['first_mention_year']}", f"first recorded {g['first_mention_year']}"))
            pp = g["start"]["page"] + ("–" + g["end"]["page"] if g["end"]["page"] != g["start"]["page"] else "")
            summ = t(esc(g.get("summary_de", "")), esc(g.get("summary_en", "")))
            gaz += (f'<div class="desc"><b>{t("Ortsartikel", "Place article")}</b> <a href="../seite/{g["start"]["page"]}.html#{g["start"]["block"]}">'
                    f'{t("S.", "p.")} {pp}</a>: {", ".join(x for x in facts if x)}<br>{summ}</div>')
        pages = e.get("pages", [])
        shown = pages[:60]
        refs = ", ".join(f'<a href="../seite/{p}.html?hl={html.escape(e["label"])}">{p}</a>' for p in shown)
        more = t(f' und {len(pages) - 60} weitere', f' and {len(pages) - 60} more') if len(pages) > 60 else ""
        kind = f'<span class="kind">{esc(e["kind"])}</span>' if e.get("kind") else ""
        kwic_btn = f'<button class="more" type="button" data-kwic="{anchor}" aria-expanded="false">{t("Textstellen zeigen", "Show passages")}</button>' if e["n"] else ""
        count = t(f'{num(e["n"])} {"Stelle" if e["n"] == 1 else "Stellen"}', f'{num(e["n"], "en")} {"passage" if e["n"] == 1 else "passages"}')
        return (f'<li class="reg-item" id="{anchor}" data-k="{esc(fold(e["label"]))}" data-kind="{esc(e.get("kind") or "")}">'
                f'<div><span class="name">{esc(e["label"])}</span>{kind}</div>'
                f'<div class="auth">{"".join(auth)}<span class="n">{count}</span></div>'
                + "".join(f'<div class="desc">{d}</div>' for d in desc) + gaz +
                f'<div class="refs">{t("S.", "pp.")} {refs}{more}{kwic_btn}</div></li>')

    def subject_list(self) -> list[str]:
        subj = collections.Counter()
        for m in self.meta.values():
            for s in m.get("subjects", []):
                subj[s.lstrip("+")] += 1
        return sorted(subj, key=sort_key)

    def build_subjects_glossary(self) -> None:
        pages_of = collections.defaultdict(list)
        for slug in [p["slug"] for p in self.pages]:
            for s in self.meta.get(slug, {}).get("subjects", []):
                pages_of[s.lstrip("+")].append(slug)
        items = [{"id": re.sub(r"[^a-z0-9]+", "-", fold(s)).strip("-"), "label": s, "pages": pages_of[s]} for s in self.subject_list()]
        self.tpl("subjects.html", "register/sachregister.html", section="register", items=items, classes=CLASSES)
        # glossary: merge duplicates across packages
        merged = collections.OrderedDict()
        for g in self.glossary_raw:
            k = fold(g["term"])
            if k not in merged:
                merged[k] = dict(g, pages=list(g.get("pages", [])))
            else:
                merged[k]["pages"] += [p for p in g.get("pages", []) if p not in merged[k]["pages"]]
        gl = sorted(merged.values(), key=lambda g: sort_key(g["term"]))
        for g in gl:
            g["id"] = re.sub(r"[^a-z0-9]+", "-", fold(g["term"])).strip("-")
        self.glossary = gl
        self.tpl("glossary.html", "register/glossar.html", section="register", items=gl, classes=CLASSES)
        self.tpl("register_index.html", "register/index.html", section="register", classes=CLASSES, counts=self.reg_counts,
                 n_subjects=len(items), n_glossary=len(gl), n_gazetteer=len(self.gazetteer))

    # ------------------------------------------------------------------ analyses
    def build_analyses(self) -> None:
        if not self.skip_charts:
            r = subprocess.run(["node", str(ROOT / "tools" / "compile_charts.mjs"), str(SITE / "auswertungen")], capture_output=True, text=True, encoding="utf-8")
            print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-500:])
        compiled = self.compiled_specs()
        ok = [a for a in self.analyses if a["id"] in compiled]
        self.analyses_ok = ok
        cards, groups = [], {}
        for a in sorted(ok, key=lambda a: (self.sections.get(a["section"], {}).get("start_seq", 0), a["id"])):
            card = {"id": a["id"], "title": a["title"], "teaser": {k: teaser(a["summary"][k]) for k in ("de", "en")}}
            cards.append(card)
            gid, gde, gen = ana_group(a["section"])
            groups.setdefault(gid, {"id": gid, "de": gde, "en": gen, "entries": []})["entries"].append(card)
        order = [g[1] for g in ANA_GROUPS]
        self.tpl("analyses_index.html", "auswertungen/index.html", section="analyses", cards=cards,
                 groups=sorted(groups.values(), key=lambda g: order.index(g["id"])))
        titles = {a["id"]: a["title"] for a in ok}
        page_blocks = {p["label"]: {b["id"]: b["type"] for b in p["blocks"]} for p in self.pages if p["label"]}
        for a in ok:
            datasets = []
            for ds in a["datasets"]:
                datasets.append({"name": ds["name"], "title": ds["title"], "columns": ds["columns"], "rows": ds["rows"][:500],
                                 "n": len(ds["rows"]), "has_derived": any(c.get("derived") for c in ds["columns"])})
                csv_lines = [",".join(c["name"] for c in ds["columns"])]
                for row in ds["rows"]:
                    csv_lines.append(",".join("" if v is None else ('"' + str(v).replace('"', '""') + '"' if isinstance(v, str) else str(v)) for v in row))
                self.write(f"auswertungen/daten/{a['id']}__{ds['name']}.csv", "﻿" + "\n".join(csv_lines) + "\n")
            sec = self.sections.get(a["section"])
            sources = []
            for src in a["sources"]:
                kind = page_blocks.get(src["page"], {}).get(src["block"])
                sources.append({"page": src["page"], "block": src["block"], "what": BLOCK_KIND.get(kind) if kind != "paragraph" else None})
            self.tpl("analysis.html", f"auswertungen/{a['id']}.html", section="analyses", a=a, datasets=datasets, sources=sources,
                     group=ana_group(a["section"])[1:], sec=sec, sec_href=self.sec_href(a["section"], "../") if sec else None,
                     related=[{"id": r, "title": titles[r]} for r in (a.get("related") or []) if r in titles])
            self.write(f"auswertungen/json/{a['id']}.json", json.dumps(a, ensure_ascii=False, indent=1))

    # ------------------------------------------------------------------ map
    def build_map(self) -> None:
        feats = []
        for e in self.entities.values():
            if e["class"] not in ("place", "nature") or not e.get("coords"):
                continue
            g = (e.get("gazetteer") or [None])[0]
            feats.append({"id": e["id"].split(":", 1)[1], "c": e["class"], "l": e["label"], "k": e.get("kind") or "",
                          "n": e["n"], "lat": e["coords"][0], "lon": e["coords"][1], "in": bool(e.get("in_principality")),
                          "g": {"type": g.get("type_verbatim") or g.get("type"), "inh": g.get("inhabitants"), "houses": g.get("houses"),
                                "first": g.get("first_mention_year"), "page": g["start"]["page"], "block": g["start"]["block"],
                                "de": g.get("summary_de", ""), "en": g.get("summary_en", ""), "lt": g.get("landestheil")} if g else None,
                          "href": f"register/{CLASS_FILE[e['class']]}.html#{e['id'].split(':', 1)[1]}", "p": e["pages"][:12]})
        self.write("karte/orte.json", json.dumps(feats, ensure_ascii=False, separators=(",", ":")))
        self.map_counts = (len(feats), sum(1 for f in feats if f["g"]))
        self.tpl("map.html", "karte.html", section="map", n=len(feats), n_gaz=self.map_counts[1])

    # ------------------------------------------------------------------ search
    def build_search(self) -> None:
        reg = [e for e in self.entities.values() if e["n"] > 0 or e.get("gazetteer")]
        stats = search_index.build(SITE / "suche", self.pages, self.struct["sections"], self.meta, reg, self.gazetteer,
                                   self.analyses_ok, self.glossary, lambda e: self.register_href(e))
        print("search index:", stats)
        self.tpl("search.html", "suche.html", section="search", classes=CLASSES)

    # ------------------------------------------------------------------ downloads
    def build_downloads(self) -> None:
        import tei  # noqa: WPS433
        for p in self.pages:
            if self.only_pages and p["slug"] not in self.only_pages:
                continue
            self.write(f"daten/seiten/{p['slug']}.json", json.dumps(p, ensure_ascii=False, indent=1))
            lines = []
            if p.get("running_header"):
                lines.append(p["running_header"])
            for b in p["blocks"]:
                lines.append(search_index.block_text(b))
            for fn in p["footnotes"]:
                lines.append(f"{fn['marker']} {fn['text']}")
            self.write(f"daten/seiten/{p['slug']}.txt", "\n\n".join(lines) + "\n")
            for b in p["blocks"]:
                if b["type"] == "table":
                    rows = ['"' + '","'.join(c.replace('"', '""') for c in r) + '"' for r in b["grid"]]
                    self.write(f"daten/tabellen/{p['slug']}-{b['id']}.csv", "﻿" + "\n".join(rows) + "\n")
        tei.export(self.pages, self.struct, self.entities, self.key_map, SITE / "daten", self.site, only=self.only_pages)
        # registers as CSV + JSON
        reg = [e for e in self.entities.values() if e["n"] > 0 or e.get("gazetteer")]
        cols = ["id", "class", "label", "kind", "modern", "gloss_en", "scientific", "geonames", "wikidata", "gbif", "lat", "lon", "n", "pages"]
        out = [",".join(cols)]
        for e in sorted(reg, key=lambda e: (e["class"], sort_key(e["label"]))):
            row = [e["id"], e["class"], e["label"], e.get("kind") or "", e.get("modern") or "", e.get("gloss_en") or "", e.get("scientific") or "",
                   str(e.get("geonames") or ""), e.get("wikidata") or "", str(e.get("gbif") or ""),
                   str(e["coords"][0]) if e.get("coords") else "", str(e["coords"][1]) if e.get("coords") else "", str(e["n"]), " ".join(e["pages"])]
            out.append(",".join('"' + v.replace('"', '""') + '"' for v in row))
        self.write("daten/register.csv", "﻿" + "\n".join(out) + "\n")
        self.write("daten/register.json", json.dumps([{k: v for k, v in e.items() if k not in ("keys",)} for e in reg], ensure_ascii=False))
        self.write("daten/ortsartikel.json", json.dumps(self.gazetteer, ensure_ascii=False, indent=1))

    # ------------------------------------------------------------------ static pages
    def build_static_pages(self) -> None:
        n_ents = sum(1 for e in self.entities.values() if e["n"] > 0)
        stats = {"pages": sum(1 for p in self.pages if p["kind"] == "text"), "mentions": sum(e["n"] for e in self.entities.values()),
                 "entities": n_ents, "analyses": len(self.analyses_ok), "places": len(self.gazetteer), "map_places": self.map_counts[0], "map_gaz": self.map_counts[1], "tables": sum(1 for p in self.pages for b in p["blocks"] if b["type"] == "table")}
        self.stats = stats
        featured = [a for a in self.analyses_ok][:6]
        self.tpl("index.html", "index.html", section="home", stats=stats, featured=featured,
                 cats=CAT_LABEL)
        rep = read_json(DATA / "reports" / "normalize_report.json")
        ls = DATA / "lines" / "summary.json"
        lines_summary = read_json(ls) if ls.exists() else {"pages": 0, "detected": 0, "aligned": 0}
        for name in ("einleitung", "richtlinien", "zitieren", "daten", "impressum"):
            self.tpl(f"doc_{name}.html", f"edition/{name}.html", section="about", stats=stats, rep=rep, rules=RULES, lines=lines_summary)
        self.tpl("404.html", "404.html")
        urls = ["index.html", "inhalt.html", "karte.html", "suche.html", "auswertungen/index.html", "register/index.html"]
        urls += [f"seite/{p['slug']}.html" for p in self.pages]
        urls += [f"register/{c[1]}.html" for c in CLASSES] + [f"auswertungen/{a['id']}.html" for a in self.analyses_ok]
        if self.site["base_url"]:
            sm = "".join(f"<url><loc>{self.site['base_url']}{u}</loc></url>" for u in urls)
            self.write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>')
            self.write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {self.site['base_url']}sitemap.xml\n")
        self.write(".nojekyll", "")

    @staticmethod
    def compiled_specs() -> set[str]:
        specs = SITE / "auswertungen" / "specs"
        return {f.stem for f in specs.glob("*.js")} | {f.stem for f in specs.glob("*.json")} if specs.exists() else set()

    @staticmethod
    def data_as_scripts() -> int:
        """Internal data files become scripts calling RJ.put(key, data) (see RJ.load in edition.js),
        because browsers block fetch() on pages opened from disk (file://)."""
        n = 0
        for d in DATA_SCRIPT_DIRS:
            for f in sorted((SITE / d).rglob("*.json")):
                key = f.relative_to(SITE).with_suffix("").as_posix()
                write_text_atomic(f.with_suffix(".js"), f"RJ.put({json.dumps(key)},{f.read_text(encoding='utf-8')});\n")
                f.unlink()
                n += 1
        return n

    def run_search_only(self) -> None:
        """Rebuild only the search index (fast; used by the search-quality work)."""
        gaz_links = self.link_gazetteer()
        compiled = self.compiled_specs()
        self.analyses_ok = [a for a in self.analyses if a["id"] in compiled]
        merged = collections.OrderedDict()
        for g in self.glossary_raw:
            k = fold(g["term"])
            if k not in merged:
                merged[k] = dict(g, pages=list(g.get("pages", [])))
        self.glossary = sorted(merged.values(), key=lambda g: sort_key(g["term"]))
        for g in self.glossary:
            g["id"] = re.sub(r"[^a-z0-9]+", "-", fold(g["term"])).strip("-")
        self.build_search()
        self.data_as_scripts()

    def run(self) -> None:
        self.assets()
        gaz_links = self.link_gazetteer()
        self.gaz_anchor = {gid: e["id"].split(":", 1)[1] for gid, e in gaz_links.items()}
        self.build_registers()
        self.build_subjects_glossary()
        self.build_analyses()
        self.build_pages()
        self.build_toc()
        self.build_map()
        self.build_search()
        self.build_downloads()
        self.build_static_pages()
        self.data_as_scripts()
        n = sum(1 for _ in SITE.rglob("*") if _.is_file())
        size = sum(f.stat().st_size for f in SITE.rglob("*") if f.is_file())
        print(f"site: {n} files, {size / 1e6:.1f} MB")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-charts", action="store_true")
    ap.add_argument("--pages", help="comma-separated page slugs (quick preview builds)")
    ap.add_argument("--only-search", action="store_true", help="rebuild only the search index in site/suche")
    ap.add_argument("--only-tei", action="store_true", help="rebuild only the TEI files in site/daten")
    a = ap.parse_args()
    b = Builder(a.skip_charts, set(a.pages.split(",")) if a.pages else None)
    if a.only_search:
        b.run_search_only()
    elif a.only_tei:
        import tei  # noqa: WPS433
        b.link_gazetteer()
        tei.export(b.pages, b.struct, b.entities, b.key_map, SITE / "daten", b.site, only=b.only_pages)
    else:
        b.run()
