"""Fetch a facsimile page (or a region of it) from the BSB IIIF image service.

    python tools/facsimile.py 54                     # whole page, 1400 px wide
    python tools/facsimile.py 54 --crop 0,0.45,1,0.75 # x0,y0,x1,y1 as fractions
    python tools/facsimile.py 54 --crop 0,0.5,0.5,1 --width 1600

Prints the local path of the JPEG (cached in data/facsimile_cache/); open it
with an image viewer / the Read tool to compare transcription and print.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "data" / "facsimile_cache"


def page_info(label: str) -> dict:
    for f in (ROOT / "data" / "pages").glob("*.json"):
        p = json.loads(f.read_text(encoding="utf-8"))
        if p["slug"] == label:
            return p
    sys.exit(f"unknown page label {label!r} (use the printed page number, e.g. 54, or III, or scan-1)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("page")
    ap.add_argument("--crop", help="x0,y0,x1,y1 as fractions of width/height")
    ap.add_argument("--width", type=int, default=1400)
    a = ap.parse_args()
    p = page_info(a.page)
    w, h = p["iiif"]["width"], p["iiif"]["height"]
    region = "full"
    tag = "full"
    if a.crop:
        x0, y0, x1, y1 = (float(v) for v in a.crop.split(","))
        region = f"{int(x0 * w)},{int(y0 * h)},{int((x1 - x0) * w)},{int((y1 - y0) * h)}"
        tag = a.crop.replace(",", "_")
    url = f"{p['iiif']['service']}/{region}/{a.width},/0/default.jpg"
    CACHE.mkdir(parents=True, exist_ok=True)
    out = CACHE / f"{p['slug']}__{tag}__{a.width}.jpg"
    if not out.exists():
        with urllib.request.urlopen(url, timeout=120) as r:
            out.write_bytes(r.read())
    print(out)


if __name__ == "__main__":
    main()
