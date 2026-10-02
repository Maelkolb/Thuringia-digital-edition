"""Parse the Subscriptionsliste (pp. 835-840) from the canonical page JSON into one record per list entry.

Record fields: page, block, row (grid row label rN), copies, title (Herr/Frau/...), name, occupation, place,
raw name cell, and (for rows that Gemini split over two grid rows) the merged text.
"""
import re
from common import load_page, block

PAGES = ["835", "836", "837", "838", "839", "840"]
DITTO = {'"', '„', '”', '“', "''", '″'}
INITIAL = re.compile(r"^(?:[A-ZÄÖÜ][a-zäöü]{0,3}\.)(?:\s*[A-ZÄÖÜ][a-zäöü]{0,3}\.)*$")  # E.  Joh.  Fr. Eug.  G. G.


def strip_period(s: str) -> str:
    s = s.strip()
    return s[:-1].strip() if s.endswith(".") and not s.endswith("Dr.") and not s.endswith("em.") and not s.endswith("b. Lobst.") else s


def split_name_occ(cell: str):
    """835 only: 'Herr Albrecht, E., Gastgeber' -> (title, name, occupation)."""
    title = ""
    m = re.match(r"^(Herr|Frau)\s+(.*)$", cell)
    if m:
        title, cell = m.group(1), m.group(2)
    elif cell.startswith('"'):
        title, cell = '"', cell[1:].strip()
    parts = [p.strip() for p in cell.split(",")]
    # name = first part + following initials
    name_parts = [parts[0]]
    i = 1
    while i < len(parts) and INITIAL.match(parts[i]) and i < len(parts) - 0:
        # an initial is only part of the name when something follows (the occupation)
        if i == len(parts) - 1:
            break
        name_parts.append(parts[i]); i += 1
    name = ", ".join(name_parts)
    occ = ", ".join(parts[i:])
    return title, name, occ


def parse():
    out = []
    for lab in PAGES:
        blk = [b for b in load_page(lab)["blocks"] if b["type"] == "table"][0]
        grid = blk["grid"]
        pending = None
        for ri, row in enumerate(grid, start=1):
            if ri == 1:
                continue  # header 'Expl.'
            row = [c.strip() for c in row]
            expl = row[0]
            cells = row[1:]
            rec = {"page": lab, "block": blk["id"], "row": f"r{ri}"}
            if expl == "" and out:
                # continuation row of a name that Gemini split over two grid rows
                prev = out[-1]
                cont_name = cells[0] if cells else ""
                cont_place = [c for c in cells[1:] if c][-1] if any(cells[1:]) else ""
                prev["name"] = (prev["name"] + (" " if not prev["name"].endswith("-") else "") + cont_name).strip()
                prev["place"] = cont_place or prev["place"]
                prev["row"] += f"+r{ri}"
                continue
            if lab == "835":
                name_cell, place = cells[0], cells[1]
                if name_cell.startswith(("Herr ", '"', "Frau ")):
                    title, name, occ = split_name_occ(name_cell)
                else:
                    title, name, occ = "", name_cell, ""
                rec.update(copies=expl, title=title, name=name, occupation=occ, place=place)
            else:
                # drop trailing empties
                while cells and cells[-1] == "":
                    cells.pop()
                title = ""
                if cells and (cells[0] in DITTO):
                    title = '"'; cells = cells[1:]
                elif lab in ("838", "839", "840") and cells and cells[0] in ("Herr", "Frau"):
                    title = cells[0]; cells = cells[1:]
                if lab in ("836", "837"):
                    # 4 columns: name | occupation | place
                    if cells and cells[0].startswith(("Herr ", "Frau ")):
                        title, cells[0] = cells[0].split(" ", 1)
                    elif cells and cells[0][:1] in DITTO:
                        title, cells[0] = '"', cells[0][1:].strip()
                    name, occ, place = (cells + ["", "", ""])[:3]
                else:
                    if cells and cells[0].startswith(("Herr ", "Frau ")):
                        title, cells[0] = cells[0].split(" ", 1)
                    if len(cells) == 3:
                        name, occ, place = cells
                    elif len(cells) == 2:
                        name, occ, place = cells[0], "", cells[1]
                    else:
                        raise ValueError((lab, ri, cells))
                rec.update(copies=expl, title=title, name=name, occupation=occ, place=place)
            out.append(rec)
    return out


if __name__ == "__main__":
    import sys, io
    sys.stdout.reconfigure(encoding="utf-8")
    recs = parse()
    for r in recs:
        print(r["page"], r["row"], "|", r["copies"], "|", r["title"], "|", r["name"], "|", r["occupation"], "|", r["place"])
