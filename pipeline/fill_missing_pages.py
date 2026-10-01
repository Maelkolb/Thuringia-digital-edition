"""Fill pages the original Colab run never extracted (front matter, p. 243) or
returned empty (pp. 527, 739).

Re-uses the exact OCR + NER prompts, model and thinking level of the
historical-digital-edition snapshot of 2026-03-03 (commit a77b152) that produced
the main run, so the added pages share the provenance of the rest of the book.
Output: data/raw_fill/page_XXXX.json in the original page-JSON schema.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "source" / "hde_2026-03-03"))
from google import genai  # noqa: E402
from src.config import ENTITY_TYPES, MODEL_ID, THINKING_LEVEL  # noqa: E402

FALLBACK_MODEL = os.environ.get("FALLBACK_MODEL", "gemini-3.5-flash")
from src.ner import perform_ner  # noqa: E402
from src.ocr import perform_ocr  # noqa: E402
from src.pipeline import _build_ocr_text  # noqa: E402

IIIF = "https://api.digitale-sammlungen.de/iiif/image/v2/bsb11005578_{seq:05d}/full/full/0/default.jpg"
# seq -> page key used by the edition (printed page number or roman numeral)
TARGETS = {
    5: "title", 7: "III", 8: "IV", 9: "V", 10: "VI", 11: "VII", 12: "VIII",
    13: "1", 255: "243", 539: "527", 751: "739",
}


def main() -> None:
    key = os.environ.get("GEMINI_API_KEY") or Path.home().joinpath("Downloads", "gemini_key.txt").read_text().strip()
    client = genai.Client(api_key=key)
    out_dir = ROOT / "data" / "raw_fill"
    img_dir = ROOT / "data" / "raw_fill" / "images"
    img_dir.mkdir(parents=True, exist_ok=True)
    only = set(sys.argv[1:])
    for seq, label in TARGETS.items():
        if only and str(seq) not in only:
            continue
        out = out_dir / f"seq_{seq:04d}.json"
        if out.exists():
            print("skip", seq)
            continue
        img = img_dir / f"bsb11005578_seq_{seq:03d}.jpg"
        if not img.exists():
            r = requests.get(IIIF.format(seq=seq), timeout=120)
            r.raise_for_status()
            img.write_bytes(r.content)
        t0 = time.time()
        # the original pipeline swallowed API errors and stored empty pages
        # (that is how pp. 527/739 ended up blank) -> retry, never save empties
        model = MODEL_ID
        for attempt in range(8):
            # the preview model is frequently overloaded (503) -> after two
            # failed attempts fall back to the GA successor; recorded per page
            if attempt >= 2:
                model = FALLBACK_MODEL
            ocr = perform_ocr(client, img, model, thinking_level=THINKING_LEVEL)
            text = _build_ocr_text(ocr)
            if ocr.get("content_blocks") or label in ("title",):
                break
            time.sleep(10 * (attempt + 1))
        if not ocr.get("content_blocks") and label != "title":
            print(f"seq {seq}: OCR failed after retries")
            continue
        ents = []
        for attempt in range(8):
            ents = perform_ner(client, text, ENTITY_TYPES, model, thinking_level=THINKING_LEVEL) if text.strip() else []
            if ents or len(text) < 200:
                break
            time.sleep(20 * (attempt + 1))
        rec = {
            "page_number": int(label) if label.isdigit() else label,
            "seq": seq,
            "image_filename": img.name,
            "structure": ocr,
            "ocr_text": text,
            "entities": [e.__dict__ for e in ents],
            "processing_timestamp": dt.datetime.now().isoformat(),
            "model_used": model,
            "note": "gap fill 2026-10-01, same prompts/model as main run (hde a77b152)",
        }
        out.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"seq {seq} ({label}): {len(ocr.get('content_blocks', []))} blocks, {len(text)} chars, {len(ents)} entities, {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
