"""Validate the edition's TEI files against tei_all (RELAX NG) with lxml.

    python tools/validate_tei.py site/daten/brueckner1870.tei.xml site/daten/seiten/54.xml ...
    python tools/validate_tei.py --sample 40      # full book + 40 random page files
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
RNG = ROOT / "tools" / "tei" / "tei_all.rng"


def main(argv: list[str]) -> int:
    files = [a for a in argv if not a.startswith("--")]
    if "--sample" in argv:
        n = int(argv[argv.index("--sample") + 1])
        pages = sorted((ROOT / "site" / "daten" / "seiten").glob("*.xml"))
        files = [str(ROOT / "site" / "daten" / "brueckner1870.tei.xml")] + [str(p) for p in random.Random(1).sample(pages, min(n, len(pages)))]
        files = [f for f in files if f not in argv]
    schema = etree.RelaxNG(etree.parse(str(RNG)))
    bad = 0
    for f in files:
        doc = etree.parse(f)
        ok = schema.validate(doc)
        if not ok:
            bad += 1
            errs = list(schema.error_log)
            print(f"INVALID {f}: {len(errs)} errors")
            for e in errs[:8]:
                print(f"   line {e.line}: {e.message}")
        else:
            print(f"valid   {f}")
    print(f"{len(files) - bad}/{len(files)} valid")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
