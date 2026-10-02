"""TEI P5 export: the whole book as one document + one document per page.

Structure: <div> nesting from the section tree, <pb/> with @facs pointing to a
<surface> (BSB IIIF image), <fw> for running heads and printer's signatures,
paragraphs that run over a page break are kept as ONE <p> with an inner
<pb/>, tables as <table>/<row>/<cell> with @role="label", @cols/@rows,
footnotes as <note place="foot">, entities as <placeName>/<persName>/
<orgName>/<name>/<rs> with @ref into a <standOff> of authority records.
Printed lines (data/lines/aligned): <zone> per line and per block on the page's
<surface>, <lb n="…" facs="#…"/> at every line start (break="no" inside a
hyphenated word), @facs on blocks pointing to their zone.
"""
from __future__ import annotations

import collections
import re
from pathlib import Path
from xml.sax.saxutils import escape as xesc

import json

import render as R

LINES = Path(__file__).resolve().parents[2] / "data" / "lines" / "aligned"


def page_lines(p: dict) -> dict | None:
    f = LINES / f"{p['seq']:04d}.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() and p["kind"] == "text" else None


def zone_box(p: dict, lines: dict, box: list) -> str:
    sx, sy = p["iiif"]["width"] / lines["width"], p["iiif"]["height"] / lines["height"]
    x, y, w, h = box
    return f'ulx="{round(x * sx)}" uly="{round(y * sy)}" lrx="{round((x + w) * sx)}" lry="{round((y + h) * sy)}"'

TEI_NS = "http://www.tei-c.org/ns/1.0"
ELEM = {"place": ("placeName", None), "nature": ("name", "nature"), "person": ("persName", None),
        "organisation": ("orgName", None), "organism": ("name", "organism"), "concept": ("rs", "concept")}


def xml_id(eid: str) -> str:
    s = re.sub(r"[^A-Za-z0-9_.-]", "-", eid.replace(":", "-"))
    return s if re.match(r"[A-Za-z_]", s) else "e-" + s


class TEI:
    def __init__(self, entities: dict, key_map: dict):
        self.entities = entities
        self.key_map = key_map
        self.used: set[str] = set()
        self.placed: set[str] = set()
        self.surface = ""

    def lb(self, b: dict) -> str:
        brk = ' break="no"' if b.get("hy") else ""
        return f'<lb n="{b["n"]}"{brk} facs="#{self.surface}-l{b["n"]}"/>'

    def inline(self, text: str, spans: list, fn_marks: dict | None = None, breaks: list[dict] | None = None) -> str:
        spans = sorted((s for s in spans if 0 <= s[0] < s[1] <= len(text)), key=lambda s: s[0])
        breaks = sorted(breaks or [], key=lambda b: b["start"])
        inner = [b for b in breaks if 0 < b["start"] < len(text)]

        def piece(a: int, z: int, entity: bool, before_entity: bool = False) -> str:
            if entity:
                cuts = [x for x in inner if a < x["start"] < z]
            else:
                cuts = [x for x in inner if a <= x["start"] < z or (before_entity and x["start"] == z)]
            parts, pos = [], a
            for x in cuts:
                parts.append(self._t(text[pos:x["start"]], fn_marks))
                parts.append(self.lb(x))
                pos = x["start"]
            parts.append(self._t(text[pos:z], fn_marks))
            return "".join(parts)

        out, pos, last_end = [], 0, -1
        for s, e, typ in spans:
            if s < last_end:
                continue
            form = text[s:e]
            eid = self.key_map.get(f"{R.TYPE_GROUP.get(typ, 'concepts')}\t{R.surface_key(form, typ)}")
            ent = self.entities.get(eid) if eid else None
            out.append(piece(pos, s, entity=False, before_entity=True))
            if ent:
                el, typ_attr = ELEM[ent["class"]]
                self.used.add(eid)
                t = f' type="{typ_attr}"' if typ_attr else ""
                out.append(f'<{el}{t} ref="#{xml_id(eid)}">{piece(s, e, entity=True)}</{el}>')
            else:
                out.append(piece(s, e, entity=True))
            pos = last_end = e
        out.append(piece(pos, len(text), entity=False))
        return "".join(self.lb(b) for b in breaks if b["start"] == 0) + "".join(out)

    def _t(self, s: str, fn_marks: dict | None) -> str:
        s = xesc(s).replace("\n", "<lb/>")
        if fn_marks:
            for mk, note in fn_marks.items():
                if mk not in self.placed and xesc(mk) in s:
                    s = s.replace(xesc(mk), note, 1)  # each note once, at its first marker
                    self.placed.add(mk)
        return s

    def table(self, b: dict) -> str:
        rows = []
        for r in b["rows"]:
            role = ' role="label"' if r["role"] in ("header", "group") else ""
            cells = []
            for c in r["cells"]:
                a = ""
                if r["role"] == "group":
                    a += f' cols="{b["n_cols"]}"'
                elif c.get("colspan"):
                    a += f' cols="{c["colspan"]}"'
                if c.get("rowspan"):
                    a += f' rows="{c["rowspan"]}"'
                if r["role"] == "header":
                    a += ' role="label"'
                cells.append(f"<cell{a}>{self.inline(c['text'], c.get('spans', []))}</cell>")
            rows.append(f"<row{role}>{''.join(cells)}</row>")
        head = f"<head>{xesc(b['caption'])}</head>" if b.get("caption") else ""
        return f'<table xml:id="{{pid}}-{b["id"]}" rows="{len(b["rows"])}" cols="{b["n_cols"]}">{head}{"".join(rows)}</table>'

    def page_parts(self, p: dict, full_book: bool = False) -> list[tuple[str, str, dict]]:
        """(kind, xml, block) per block, footnotes inlined at their marker as <note>.

        Only headings that open a section of the book structure become <head>
        (in the full book, where the <div> is opened right before them); all
        other headings are <ab type="heading">, which TEI allows anywhere."""
        pid = f"p{p['slug']}"
        self.placed = set()
        self.surface = f"f{p['seq']:04d}"
        lines = page_lines(p)
        breaks: dict[str, list[dict]] = {}
        regions = (lines or {}).get("regions", {})
        for line in (lines or {}).get("lines", []):
            if line.get("n"):
                breaks.setdefault(line["unit"], []).append(line)

        def facs(block_id: str) -> str:
            return f' facs="#{self.surface}-{block_id}"' if block_id in regions else ""

        notes = {}
        for fn in p["footnotes"]:
            notes[fn["marker"]] = (f'<note place="foot" n="{xesc(fn["marker"])}" xml:id="{pid}-{fn["id"]}"{facs(fn["id"])}>'
                                   f'{self.inline(fn["text"], fn["spans"], breaks=breaks.get(fn["id"]))}</note>')
        marks = {k: v for k, v in notes.items() if "*" in k}
        parts = []
        for b in p["blocks"]:
            if b["type"] == "heading":
                el = "head" if (full_book and b.get("opens")) else 'ab type="heading"'
                x = f'<{el} xml:id="{pid}-{b["id"]}"{facs(b["id"])}>{self.inline(b["text"], b["spans"], marks, breaks.get(b["id"]))}</{el.split()[0]}>'
            elif b["type"] == "paragraph":
                x = self.inline(b["text"], b["spans"], marks, breaks.get(b["id"]))
            elif b["type"] == "list":
                x = '<list xml:id="{}-{}"{}>{}</list>'.format(pid, b["id"], facs(b["id"]), "".join(
                    f"<item>{self.inline(i['text'], i['spans'], marks, breaks.get(b['id'] + '.i' + str(k)))}</item>" for k, i in enumerate(b["items"])))
            else:
                x = self.table(b).replace("{pid}", pid).replace(f'xml:id="{pid}-{b["id"]}"', f'xml:id="{pid}-{b["id"]}"{facs(b["id"])}', 1)
            parts.append((b["type"], x, b))
        # footnotes whose marker was not found in the text: append at the end of the page
        rest = "".join(v for k, v in notes.items() if k not in self.placed)
        if rest:
            parts.append(("notes", rest, {}))
        return parts


def header(site: dict, scope: str, extra_source: str = "") -> str:
    return f"""<teiHeader>
  <fileDesc>
    <titleStmt>
      <title type="main">Volks- und Landeskunde des Fürstenthums Reuß j. L.</title>
      <title type="sub">Digitale Edition{scope}</title>
      <author><persName ref="https://d-nb.info/gnd/119209217">Brückner, Georg</persName> (1800–1881)</author>
      {''.join(f'<editor><persName>{xesc(n)}</persName></editor>' for n in site['editors'])}
      <respStmt><resp>Automatische Transkription und Entitätenerkennung</resp><name>Google Gemini 3 Flash (2026)</name></respStmt>
      <respStmt><resp>Layout-Korrektur, Register, Auswertungen, Edition</resp>{''.join(f'<persName>{xesc(n)}</persName>' for n in site['editors'])}<name>Claude (Anthropic)</name></respStmt>
    </titleStmt>
    <editionStmt><edition n="{site['version']}">Version {site['version']}, <date when="{site['date']}">{site['date']}</date></edition></editionStmt>
    <publicationStmt>
      <publisher>{xesc(site['institution'])}</publisher>
      <date when="{site['date']}">{site['date'][:4]}</date>
      <availability><licence target="{site['license_url']}">{site['license_text']} (Transkription, Annotation, Daten). Faksimiles: Bayerische Staatsbibliothek München, NoC-NC 1.0.</licence></availability>
    </publicationStmt>
    <sourceDesc>
      <bibl type="original">
        <author>Brückner, Georg</author>
        <title>Volks- und Landeskunde des Fürstenthums Reuß j. L. Im Auftrage des regierenden Landesfürsten verfaßt</title>
        <pubPlace>Gera</pubPlace><publisher>Köhler</publisher><date when="1870">1870</date>
        <extent>VIII, 840 S.</extent>
        <idno type="URN">urn:nbn:de:bvb:12-bsb11005578-4</idno>
        <idno type="BSB">bsb11005578</idno>
        <idno type="shelfmark">München, Bayerische Staatsbibliothek, Germ.sp. 78 ld</idno>{extra_source}
      </bibl>
    </sourceDesc>
  </fileDesc>
  <encodingDesc>
    <projectDesc><p>Digitale Edition auf Grundlage einer automatischen Transkription des BSB-Digitalisats (Gemini 3 Flash, 2026), regelbasiert korrigiert und strukturiert; Register durch KI-Agenten bereinigt und mit Normdaten verknüpft.</p></projectDesc>
    <editorialDecl>
      <normalization><p>Historische Schreibung beibehalten; Umlaute modern (ä, ö, ü statt e-Superskript); langes s als s; Ligaturen aufgelöst.</p></normalization>
      <hyphenation eol="none"><p>Silbentrennung am Zeilenende aufgelöst; am Seitenende erhaltene Trennungen sind über das Seitenende hinweg in einem Absatz zusammengeführt.</p></hyphenation>
      <correction><p>Layoutfehler der automatischen Erkennung (Tabellenköpfe, Bogensignaturen, Trennstriche) sind regelbasiert korrigiert und je Seite protokolliert. Inhaltliche Druckfehler sind nicht korrigiert.</p></correction>
    </editorialDecl>
  </encodingDesc>
  <profileDesc><langUsage><language ident="de">Deutsch (1870)</language></langUsage></profileDesc>
  <revisionDesc><change when="{site['date']}">Version {site['version']}</change></revisionDesc>
</teiHeader>"""


def standoff(tei: TEI) -> str:
    groups = collections.defaultdict(list)
    for eid in sorted(tei.used):
        e = tei.entities[eid]
        groups[e["class"]].append(e)
    out = ["<standOff>"]

    def idnos(e):
        x = ""
        if e.get("geonames"):
            x += f'<idno type="GeoNames">https://www.geonames.org/{e["geonames"]}</idno>'
        if e.get("wikidata"):
            x += f'<idno type="Wikidata">https://www.wikidata.org/entity/{e["wikidata"]}</idno>'
        if e.get("gbif"):
            x += f'<idno type="GBIF">https://www.gbif.org/species/{e["gbif"]}</idno>'
        return x

    if groups["place"] or groups["nature"]:
        out.append("<listPlace>")
        for e in groups["place"] + groups["nature"]:
            geo = f'<location><geo>{e["coords"][0]} {e["coords"][1]}</geo></location>' if e.get("coords") else ""
            typ = ' type="nature"' if e["class"] == "nature" else ""
            out.append(f'<place xml:id="{xml_id(e["id"])}"{typ}><placeName>{xesc(e["label"])}</placeName>'
                       + (f'<placeName type="modern">{xesc(e["modern"])}</placeName>' if e.get("modern") else "")
                       + (f'<desc>{xesc(e["kind"])}</desc>' if e.get("kind") else "") + geo + idnos(e) + "</place>")
        out.append("</listPlace>")
    if groups["person"]:
        out.append("<listPerson>")
        for e in groups["person"]:
            note = f'<note>{xesc(e.get("description_de") or e.get("note") or "")}</note>' if (e.get("description_de") or e.get("note")) else ""
            out.append(f'<person xml:id="{xml_id(e["id"])}"><persName>{xesc(e["label"])}</persName>{note}{idnos(e)}</person>')
        out.append("</listPerson>")
    if groups["organisation"]:
        out.append("<listOrg>")
        for e in groups["organisation"]:
            out.append(f'<org xml:id="{xml_id(e["id"])}"><orgName>{xesc(e["label"])}</orgName>{idnos(e)}</org>')
        out.append("</listOrg>")
    for cls in ("organism", "concept"):
        if groups[cls]:
            out.append(f'<listObject type="{cls}">')
            for e in groups[cls]:
                sci = f'<objectName type="scientific">{xesc(e["scientific"])}</objectName>' if e.get("scientific") else ""
                gl = f'<objectName xml:lang="en">{xesc(e["gloss_en"])}</objectName>' if e.get("gloss_en") else ""
                out.append(f'<object xml:id="{xml_id(e["id"])}"><objectIdentifier><objectName>{xesc(e["label"])}</objectName>{sci}{gl}{idnos(e)}</objectIdentifier></object>')
            out.append("</listObject>")
    out.append("</standOff>")
    return "\n".join(out)


def facsimile(pages: list[dict]) -> str:
    out = ["<facsimile>"]
    for p in pages:
        sid = f"f{p['seq']:04d}"
        out.append(f'<surface xml:id="{sid}" n="{xesc(p["label"] or "")}" ulx="0" uly="0" lrx="{p["iiif"]["width"]}" lry="{p["iiif"]["height"]}">'
                   f'<graphic url="{p["iiif"]["service"]}/full/full/0/default.jpg" mimeType="image/jpeg"/>')
        lines = page_lines(p)
        if lines:
            for block, box in lines["regions"].items():
                if block not in ("head", "sig"):
                    out.append(f'<zone xml:id="{sid}-{block}" type="block" {zone_box(p, lines, box)}/>')
            for line in lines["lines"]:
                if line.get("n"):
                    out.append(f'<zone xml:id="{sid}-l{line["n"]}" type="line" n="{line["n"]}" {zone_box(p, lines, line["box"])}/>')
        out.append("</surface>")
    out.append("</facsimile>")
    return "".join(out)


def export(pages: list[dict], struct: dict, entities: dict, key_map: dict, out_dir: Path, site: dict, only=None) -> None:
    sections = {s["id"]: s for s in struct["sections"]}
    # ---- full book --------------------------------------------------------
    tei = TEI(entities, key_map)
    body: list[str] = []
    stack: list[str] = []
    open_p = False

    def close_p():
        nonlocal open_p
        if open_p:
            body.append("</p>")
            open_p = False

    starts = collections.defaultdict(list)
    for s in struct["sections"]:
        starts[(s["start_seq"], s.get("start_block"))].append(s)
    for p in pages:
        pid = f"p{p['slug']}"
        pb = f'<pb n="{xesc(p["label"] or "")}" facs="#f{p["seq"]:04d}" xml:id="{pid}"/>'
        page_level = sorted(starts.get((p["seq"], None), []), key=lambda s: s["depth"])
        for s in page_level:
            close_p()
            while stack and sections[stack[-1]]["depth"] >= s["depth"]:
                body.append("</div>")
                stack.pop()
            body.append(f'<div type="section" n="{xesc(s.get("num", ""))}" xml:id="{xml_id("sec-" + s["id"])}">')
            stack.append(s["id"])
        if open_p:
            body.append(pb)
        else:
            body.append(pb)
        if p.get("running_header"):
            body.append(f'<fw type="header" place="top">{xesc(p["running_header"])}</fw>')
        if p["kind"] != "text":
            continue
        for kind, x, b in tei.page_parts(p, full_book=True):
            for s in sorted(starts.get((p["seq"], b.get("id")), []), key=lambda s: s["depth"]):
                close_p()
                while stack and sections[stack[-1]]["depth"] >= s["depth"]:
                    body.append("</div>")
                    stack.pop()
                body.append(f'<div type="section" n="{xesc(s.get("num", ""))}" xml:id="{xml_id("sec-" + s["id"])}">')
                stack.append(s["id"])
            if kind == "paragraph":
                if b.get("continued") and open_p:
                    body.append(x)
                else:
                    close_p()
                    rend = ' rend="imprint"' if b.get("role") == "imprint" else ""
                    body.append(f'<p xml:id="{pid}-{b["id"]}"{rend}>{x}')
                    open_p = True
                if not b.get("continues"):
                    close_p()
            elif kind == "notes":
                if open_p:
                    body.append(x)
                else:
                    body.append(f"<p>{x}</p>")
            else:
                close_p()
                body.append(x)
        if p.get("signature"):
            if open_p:
                body.append(f'<fw type="sig" place="bottom">{xesc(p["signature"])}</fw>')
            else:
                body.append(f'<fw type="sig" place="bottom">{xesc(p["signature"])}</fw>')
    close_p()
    while stack:
        body.append("</div>")
        stack.pop()
    doc = (f'<?xml version="1.0" encoding="UTF-8"?>\n<?xml-model href="https://tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>\n'
           f'<TEI xmlns="{TEI_NS}" xml:lang="de">\n{header(site, "")}\n{facsimile(pages)}\n<text><body>\n' + "\n".join(body) + f"\n</body></text>\n{standoff(tei)}\n</TEI>\n")
    out_dir.mkdir(parents=True, exist_ok=True)
    if not only:
        (out_dir / "brueckner1870.tei.xml").write_text(doc, encoding="utf-8")
    # ---- per page -----------------------------------------------------------
    for p in pages:
        if only and p["slug"] not in only:
            continue
        t = TEI(entities, key_map)
        parts = []
        if p.get("running_header"):
            parts.append(f'<fw type="header" place="top">{xesc(p["running_header"])}</fw>')
        if p["kind"] == "text":
            for kind, x, b in t.page_parts(p):
                if kind == "paragraph":
                    rend = ' rend="imprint"' if b.get("role") == "imprint" else ""
                    parts.append(f'<p xml:id="p{p["slug"]}-{b["id"]}"{rend}>{x}</p>')
                elif kind == "notes":
                    parts.append(f"<p>{x}</p>")
                else:
                    parts.append(x)
        if p.get("signature"):
            parts.append(f'<fw type="sig" place="bottom">{xesc(p["signature"])}</fw>')
        if not any(x.startswith(("<p", "<ab", "<list", "<table")) for x in parts):
            parts.append("<p/>")
        label = p["label"] or f"Scan {p['seq']}"
        doc = (f'<?xml version="1.0" encoding="UTF-8"?>\n<TEI xmlns="{TEI_NS}" xml:lang="de">\n{header(site, ", " + ("S. " + label if p["label"] else label))}\n'
               f'{facsimile([p])}\n<text><body><div type="page" n="{xesc(p["label"] or "")}"><pb n="{xesc(p["label"] or "")}" facs="#f{p["seq"]:04d}"/>\n'
               + "\n".join(parts) + f"\n</div></body></text>\n{standoff(t)}\n</TEI>\n")
        (out_dir / "seiten" / f"{p['slug']}.xml").write_text(doc, encoding="utf-8")
