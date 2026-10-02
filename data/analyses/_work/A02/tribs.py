"""Parse the numbered tributary lists of chapter 6 (pp. 45-53)."""
import re
from common import *

# (river, basin, bank, [(page, first block, last block)])
LISTS = [
    ("Rodach", "Main", "links", [("45", "b9", "b11")]),
    ("Rodach", "Main", "rechts", [("45", "b12", "b13")]),
    ("Saale", "Saale-Oberland", "rechts", [("46", "b4", "b12"), ("46", "b14", "b18"), ("47", "b1", "b8"), ("48", "b2", "b2")]),
    ("Saale", "Saale-Oberland", "links", [("48", "b4", "b10"), ("49", "b1", "b5")]),
    ("Weida", "Saale-Oberland", "links", [("50", "b2", "b8")]),
    ("Weida", "Saale-Oberland", "rechts", [("50", "b9", "b16")]),
    ("Elster", "Elster-Unterland", "links", [("51", "b2", "b8"), ("52", "b2", "b6")]),
    ("Elster", "Elster-Unterland", "rechts", [("52", "b7", "b15"), ("53", "b2", "b8")]),
]


def bid_range(a, b):
    n0, n1 = int(a[1:]), int(b[1:])
    return [f"b{i}" for i in range(n0, n1 + 1)]


def parse():
    out = []
    for river, basin, bank, segs in LISTS:
        for page, a, b in segs:
            for bid in bid_range(a, b):
                t = text(page, bid)
                m = re.match(r"^(?:(?:Links|Rechts):\s*)?(\d+)\)\s*(.*)$", t, re.S)
                if river == "Rodach":
                    num = None
                    body = t
                else:
                    if not m:
                        raise SystemExit(f"no number: {page} {bid} {t[:60]}")
                    num, body = int(m.group(1)), m.group(2)
                out.append(dict(river=river, basin=basin, bank=bank, num=num, page=page, block=bid, body=body))
    return out


if __name__ == "__main__":
    rows = parse()
    for r in rows:
        print(r["river"], r["bank"], r["num"], r["page"], r["block"], "|", r["body"][:70])
    from collections import Counter
    print(Counter((r["river"], r["bank"]) for r in rows))
