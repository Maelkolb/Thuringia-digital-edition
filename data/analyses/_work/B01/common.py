"""Shared helpers for the B01 scripts (back matter: Maße, Subscribenten, Berichtigungen)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3].parent  # reuss-edition
PAGES = ROOT / "data" / "pages"
OUT = ROOT / "data" / "analyses"


def load_page(label: str) -> dict:
    for f in sorted(PAGES.glob("*.json")):
        p = json.loads(f.read_text(encoding="utf-8"))
        if p["slug"] == label:
            return p
    raise KeyError(label)


def block(label: str, bid: str) -> dict:
    p = load_page(label)
    for b in p["blocks"] + p.get("footnotes", []):
        if b["id"] == bid:
            return b
    raise KeyError((label, bid))


def write_analysis(a: dict) -> Path:
    out = OUT / f"{a['id']}.json"
    out.write_text(json.dumps(a, ensure_ascii=False, indent=1), encoding="utf-8")
    return out
