"""Shared paths and small helpers for the edition pipeline."""
from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
DATA = ROOT / "data"
PAGES_DIR = DATA / "pages"
SITE = ROOT / "site"

BOOK_ID = "bsb11005578"
IIIF_IMAGE = "https://api.digitale-sammlungen.de/iiif/image/v2/bsb11005578_{seq:05d}"
IIIF_CANVAS = "https://api.digitale-sammlungen.de/iiif/presentation/v2/bsb11005578/canvas/{seq}"
IIIF_MANIFEST = "https://api.digitale-sammlungen.de/iiif/presentation/v2/bsb11005578/manifest"
MDZ_VIEWER = "https://www.digitale-sammlungen.de/de/view/bsb11005578?page={seq}"
URN = "urn:nbn:de:bvb:12-bsb11005578-4"

ENTITY_TYPES = [
    "Location", "Person", "Organisation", "Natural Object", "Environment",
    "Animal", "Plant", "Resource", "Artefact", "Climate", "Environmental Impact",
]


def read_json(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_text_atomic(path: Path, text: str) -> None:
    """Write via a temp file + rename: readers (other processes, subagents)
    never see a half-written file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f".{os.getpid()}.tmp")
    tmp.write_text(text, encoding="utf-8")
    for attempt in range(60):  # Windows: target may be open in another process for a moment
        try:
            os.replace(tmp, path)
            return
        except PermissionError:
            time.sleep(0.25)
    os.replace(tmp, path)


def write_json(path: Path, obj: Any, indent: int | None = 1) -> None:
    write_text_atomic(path, json.dumps(obj, ensure_ascii=False, indent=indent))


def page_slug(label: str | None, seq: int) -> str:
    """URL slug of a page: printed label if there is one, else the scan number."""
    if label:
        return label
    return f"scan-{seq}"


NUMERIC_CELL = re.compile(r"^[\s\-–—+±~ca.]*[\d.,½¼¾⅓⅔⅛\s/′'″\"°%-]*\d[\d.,½¼¾⅓⅔⅛\s/′'″\"°%‰-]*\.?$")


def is_numeric(cell: str) -> bool:
    s = (cell or "").strip()
    if not s or s in {"—", "–", "-", "„", '"', "..", "...", "…"}:
        return False
    return bool(NUMERIC_CELL.match(s))


def is_filler(cell: str) -> bool:
    """Dashes / ditto marks that stand for 'nothing' or 'same as above'."""
    return (cell or "").strip() in {"—", "–", "-", "„", '"', "..", "...", "…", "″", "''"}
