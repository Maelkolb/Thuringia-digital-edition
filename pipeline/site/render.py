"""HTML rendering of canonical page records (transcription pane)."""
from __future__ import annotations

import html
import re

from common import is_numeric

CLASS_REGISTER = {"place": "orte", "nature": "natur", "person": "personen", "organisation": "institutionen",
                  "organism": "organismen", "concept": "sachen"}
CLASS_LABEL = {
    "place": ("Ort", "Place"), "nature": ("Gewässer/Berg/Wald", "Natural feature"), "person": ("Person", "Person"),
    "organisation": ("Institution", "Institution"), "organism": ("Tier/Pflanze", "Animal/plant"),
    "concept": ("Sache/Begriff", "Thing/concept"),
}
TYPE_GROUP = {"Location": "places", "Natural Object": "nature", "Person": "persons", "Organisation": "organisations",
              "Animal": "organisms", "Plant": "organisms", "Artefact": "concepts", "Resource": "concepts",
              "Environment": "concepts", "Climate": "concepts", "Environmental Impact": "concepts"}
ARTICLES = re.compile(r"^(der|die|das|dem|den|des|im|am|zum|zur|bei|von)\s+", re.I)


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def t(de: str, en: str) -> str:
    """Bilingual inline string."""
    if de == en:
        return de
    return f'<span data-l="de">{de}</span><span data-l="en">{en}</span>'


def surface_key(form: str, etype: str) -> str:
    f = re.sub(r"\s+", " ", form).strip().strip(".,;:()[]„“\"'")
    f = ARTICLES.sub("", f)
    if etype in ("Location", "Natural Object", "Organisation", "Person"):
        f = re.sub(r"(?<=[a-zäöü])['’]s$", "", f)
    return f


def line_mark(b: dict) -> str:
    """Start of a printed line; hidden unless the reader switches on the line view."""
    hy = '<span class="hy" aria-hidden="true">-</span>' if b.get("hy") else ""
    return f'{hy}<span class="lb" data-n="{b["n"]}" data-line="{b["id"]}"></span>'


class Renderer:
    def __init__(self, root: str, key_map: dict, entities: dict, fn_markers: list[str] | None = None):
        self.root = root
        self.key_map = key_map
        self.entities = entities
        self.used: dict[str, int] = {}

    # -- inline text with entity spans and footnote refs -------------------
    def inline(self, text: str, spans: list, fn_ids: dict[str, str] | None = None, runin: int = 0,
               breaks: list[dict] | None = None) -> str:
        spans = sorted((s for s in spans if 0 <= s[0] < s[1] <= len(text)), key=lambda s: s[0])
        breaks = sorted(breaks or [], key=lambda b: b["start"])
        at_start = [b for b in breaks if b["start"] == 0]
        inner = [b for b in breaks if 0 < b["start"] < len(text)]

        def piece(a: int, b: int, entity: bool, before_entity: bool = False) -> str:
            if entity:
                cuts = [x for x in inner if a < x["start"] < b]
            else:
                cuts = [x for x in inner if a <= x["start"] < b or (before_entity and x["start"] == b)]
            parts, pos = [], a
            for x in cuts:
                parts.append(self._plain(text[pos:x["start"]], fn_ids))
                parts.append(line_mark(x))
                pos = x["start"]
            parts.append(self._plain(text[pos:b], fn_ids))
            return "".join(parts)

        out, pos = [], 0
        events = []
        for s, e, typ in spans:
            if events and s < events[-1][1]:
                continue  # overlapping annotation: keep the first
            events.append((s, e, typ))
        for s, e, typ in events:
            out.append(piece(pos, s, entity=False, before_entity=True))
            form = text[s:e]
            eid = self.key_map.get(f"{TYPE_GROUP.get(typ, 'concepts')}\t{surface_key(form, typ)}")
            if eid and eid in self.entities:
                ent = self.entities[eid]
                cls = ent["class"]
                self.used[eid] = self.used.get(eid, 0) + 1
                href = f"{self.root}register/{CLASS_REGISTER[cls]}.html#{eid.split(':', 1)[1]}"
                out.append(f'<a class="ent k-{cls}" href="{href}" data-e="{esc(eid)}">{piece(s, e, entity=True)}</a>')
            else:
                out.append(piece(s, e, entity=True))
            pos = e
        out.append(piece(pos, len(text), entity=False))
        res = "".join(out)
        if runin:
            # bold the run-in head ("c) Gemeindeverfassung.") - done on plain prefix only
            head = esc(text[:runin])
            if res.startswith(head):
                res = f'<span class="runin">{head}</span>' + res[len(head):]
        return "".join(line_mark(b) for b in at_start) + res

    @staticmethod
    def _plain(s: str, fn_ids: dict[str, str] | None) -> str:
        s = esc(s).replace("\n", "<br>")
        if fn_ids:
            for marker, fid in fn_ids.items():
                m = esc(marker)
                if m and m in s:
                    s = s.replace(m, f'<a class="fnref" href="#{fid}" id="ref-{fid}" aria-label="Fußnote">{m}</a>', 1)
        return s

    # -- blocks ----------------------------------------------------------------
    def table(self, b: dict, page: dict, fn_ids) -> str:
        rows = b["rows"]
        head = [r for r in rows if r["role"] == "header"]
        body = [r for r in rows if r["role"] != "header"]
        parts = ['<div class="tbl" id="' + b["id"] + '">']
        if b.get("caption"):
            parts.append(f'<p class="tbl-caption">{esc(b["caption"])}</p>')
        label = f'Tabelle / table {b["id"]}, S. {page["label"]}' + (f': {b["caption"]}' if b.get("caption") else "")
        parts.append(f'<div class="tbl-scroll" tabindex="0" role="region" aria-label="{esc(label)}">' + '<table>')
        if head:
            parts.append("<thead>")
            for r in head:
                parts.append("<tr>" + "".join(self._cell(c, "th", fn_ids, header=True) for c in r["cells"]) + "</tr>")
            parts.append("</thead>")
        parts.append("<tbody>")
        for r in body:
            if r["role"] == "group":
                c = r["cells"][0]
                parts.append(f'<tr class="group"><th colspan="{b["n_cols"]}" scope="colgroup">{self.inline(c["text"], c.get("spans", []), fn_ids)}</th></tr>')
                continue
            cls = ' class="total"' if r["role"] == "total" else ""
            parts.append(f"<tr{cls}>" + "".join(self._cell(c, "td", fn_ids) for c in r["cells"]) + "</tr>")
        parts.append("</tbody></table></div>")
        csv = f"{self.root}daten/tabellen/{page['slug']}-{b['id']}.csv"
        parts.append(f'<div class="tbl-tools"><a href="{csv}" download>{t("Tabelle als CSV", "Table as CSV")}</a></div></div>')
        return "".join(parts)

    def _cell(self, c: dict, tag: str, fn_ids, header: bool = False) -> str:
        attrs = ""
        if c.get("colspan"):
            attrs += f' colspan="{c["colspan"]}"'
        if c.get("rowspan"):
            attrs += f' rowspan="{c["rowspan"]}"'
        if header and not c["text"].strip():
            tag = "td"  # empty corner cell: not a header for screen readers
        elif header:
            attrs += ' scope="col"'
        elif is_numeric(c["text"]):
            attrs += ' class="num"'
        return f"<{tag}{attrs}>{self.inline(c['text'], c.get('spans', []), fn_ids)}</{tag}>"

    def page(self, page: dict, prev_slug: str | None, next_slug: str | None, lines: dict | None = None) -> str:
        self.used = {}
        breaks: dict[str, list[dict]] = {}
        for line in (lines or {}).get("lines", []):
            if line.get("n"):
                breaks.setdefault(line["unit"], []).append(line)
        fn_ids = {fn["marker"]: fn["id"] for fn in page["footnotes"] if fn.get("marker") and "*" in fn["marker"]}
        out = []
        # document outline: the page title is <h1>; transcription headings start at <h2>
        # (relative to the highest level on the page), the visual class keeps the absolute level
        levels = [b.get("level", 5) for b in page["blocks"] if b["type"] == "heading"]
        top = min(levels) if levels else 2
        for b in page["blocks"]:
            if b["type"] == "heading":
                lvl = b.get("level", 5)
                tag = f"h{min(6, 2 + lvl - top)}"
                out.append(f'<{tag} class="h h{lvl}" id="{b["id"]}">{self.inline(b["text"], b["spans"], fn_ids, breaks=breaks.get(b["id"]))}</{tag}>')
            elif b["type"] == "paragraph":
                cls = []
                pre = post = ""
                if b.get("continued"):
                    cls.append("cont")
                    if prev_slug:
                        pre = f'<a class="cont-mark" href="{prev_slug}.html#end">{t(f"Fortsetzung von S. {prev_slug}", f"Continued from p. {prev_slug}")}</a>'
                if b.get("continues") and next_slug:
                    post = f'<a class="cont-mark after" href="{next_slug}.html">{t(f"Fortsetzung auf S. {next_slug}", f"Continues on p. {next_slug}")}</a>'
                if b.get("role") == "imprint":
                    cls.append("imprint")
                c = f' class="{" ".join(cls)}"' if cls else ""
                out.append(f'{pre}<p id="{b["id"]}"{c}>{self.inline(b["text"], b["spans"], fn_ids, b.get("runin", 0), breaks.get(b["id"]))}</p>{post}')
                if b.get("editorial_note"):
                    n = b["editorial_note"]
                    out.append(f'<span class="edit-note">{t("Anm. d. Hg.: ", "Editor’s note: ")}{t(esc(n["de"]), esc(n["en"]))}</span>')
            elif b["type"] == "list":
                items = "".join(f'<li>{self.inline(i["text"], i["spans"], fn_ids, breaks=breaks.get(b["id"] + ".i" + str(k)))}</li>'
                                for k, i in enumerate(b["items"]))
                out.append(f'<ul class="blist" id="{b["id"]}">{items}</ul>')
            elif b["type"] == "table":
                out.append(self.table(b, page, fn_ids))
        body = "\n".join(out)
        fns = ""
        if page["footnotes"]:
            items = []
            for fn in page["footnotes"]:
                back = f' <a href="#ref-{fn["id"]}" aria-label="zurück zum Text">↩</a>' if fn.get("marker") in fn_ids else ""
                items.append(f'<p id="{fn["id"]}"><span class="fnmark">{esc(fn["marker"])}</span>{self.inline(fn["text"], fn["spans"], breaks=breaks.get(fn["id"]))}{back}</p>')
            fns = '<section class="footnotes" lang="de" aria-label="Fußnoten">' + "".join(items) + "</section>"
        sig = f'<div class="signature">{t("Bogensignatur", "Signature mark")} {esc(page["signature"])}</div>' if page.get("signature") else ""
        return f'<div class="transcription" lang="de">{body}</div>{fns}{sig}<span id="end"></span>'
