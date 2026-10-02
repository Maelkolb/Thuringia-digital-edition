"""Derive metric base values and the internal consistency checks for Brückner's unit table."""
import re
from fractions import Fraction
from parse_units import parse, num, BASE
from common import block

LIN_PER_M = num(re.search(r"\((\d+,\d+) pariser Linien = 1 Meter", block("831", "b7")["text"]).group(1))
TOL_PCT = 0.05  # a recomputed value within +-0.05 % of the printed one counts as "ok" (printing of 4-6 digits)


def mixed(s: str) -> float:
    """'136 23/32' -> 136.71875 ; '126' -> 126 ; '136 1/2' -> 136.5"""
    parts = s.split()
    v = Fraction(0)
    for p in parts:
        v += Fraction(p)
    return float(v)


def build():
    recs = parse()
    # editorial fix, verified on the facsimile: p. 832 b8 prints "134,75", the transcription has "134,775"
    for r in recs:
        r["note"] = ""
        if r["page"] == "832" and r["block"] == "b8":
            if r["district"] == "Gera":
                r["foot"] = r["foot"]
            elif r["district"] == "Schleiz":
                r["foot"] = 125.3   # "leipziger Maß, wie bei Gera"
                r["note"] = "Fuß wie bei Gera (leipziger Maß) – Angabe im Kopf des Abschnitts"
            elif r["district"] == "Lobenstein":
                assert abs(r["foot"] - 134.775) < 1e-9
                r["foot"] = 134.75
                r["note"] = "Fuß zu 134,75 par. Linien (Druck; die Transkription liest 134,775, siehe transcription_issues)"
        # reference length column
        r["ref_len"] = r["ref_par_lin"] if r["ref_par_lin"] else (r.get("foot") if r["quantity"] in ("firewood",) else None)
        # kanne fraction
        m = re.search(r"\(([0-9/]+) preuß\. Quart\)", r["definition"])
        r["quart"] = m.group(1) if m else None
        # base value
        if r["value"] is not None:
            f, ub = BASE[r["unit_printed"]]
            r["base"] = round(r["value"] * f, 6)
            r["unit_base"] = ub
        else:
            r["base"], r["unit_base"] = None, ""

    def find(unit, district=None, defn_part=None):
        c = [r for r in recs if r["unit"] == unit and (district is None or r["district"] == district)
             and (defn_part is None or defn_part in r["definition"])]
        assert len(c) == 1, (unit, district, defn_part, len(c))
        return c[0]

    kanne = {r["district"]: r for r in recs if r["unit"] == "Kanne"}
    quart_l = kanne["Hirschberg"]["base"]            # 1 Kanne = 1 preuß. Quart in Hirschberg
    baufuss = find("Baufuß"); pfuss = find("preuß. Fuß"); pruthe = find("preuß. Ruthe")
    elle_leipz = find("Elle", "Schleiz"); quadr_ruthe = find("preuß. Quadratruthe")
    kubikfuss = find("leipziger Kubikfuß")

    for r in recs:
        r["recomp"] = None; r["rule"] = ""
        u, d = r["unit"], r["district"]
        if r["base"] is None:
            continue
        if u == "Baufuß":
            r["recomp"] = 125.3 / LIN_PER_M
            r["rule"] = "125,3 par. L. ÷ 443,296 par. L./m (Fuß des leipziger Maßes, S. 832)"
        elif u == "preuß. Fuß":
            r["recomp"] = r["ref_par_lin"] / LIN_PER_M; r["rule"] = "139,13 par. L. ÷ 443,296 par. L./m"
        elif u == "preuß. Ruthe":
            r["recomp"] = 12 * pfuss["base"]; r["rule"] = "12 × preuß. Fuß (gedruckter Wert)"
        elif u == "Elle" and r["ref_par_lin"]:
            r["recomp"] = r["ref_par_lin"] / LIN_PER_M
            r["rule"] = f"{str(r['ref_par_lin']).replace('.', ',')} par. L. ÷ 443,296 par. L./m"
        elif u == "Elle" and d == "Saalburg":
            r["recomp"] = elle_leipz["base"] * (24 + 1.75) / 24
            r["rule"] = "leipziger Elle (gedruckter Wert) × 25,75/24 (1 Elle = 24 Zoll, Zusatz 1 3/4 Zoll)"
        elif u == "sächsische Quadratelle":
            r["recomp"] = elle_leipz["base"] ** 2; r["rule"] = "(leipziger Elle 0,565311 m)²"
        elif u == "preuß. Quadratruthe":
            r["recomp"] = pruthe["base"] ** 2; r["rule"] = "(preuß. Ruthe 3,766242 m)²"
        elif u == "preuß. Morgen":
            r["recomp"] = 180 * quadr_ruthe["base"]; r["rule"] = "180 × preuß. Quadratruthe (gedruckter Wert)"
        elif u == "Kanne" and r["quart"] and d != "Hirschberg":
            r["recomp"] = float(Fraction(r["quart"])) * quart_l
            r["rule"] = f"{r['quart']} × 1 preuß. Quart (= Kanne in Hirschberg, 1,1450 L)"
        elif r["n_kannen"] and u != "Kanne":
            r["recomp"] = r["n_kannen"] * kanne[d]["base"]
            r["rule"] = f"{r['n_kannen']} Kannen × {str(kanne[d]['value']).replace('.', ',')} L (Kanne in {d})"
        elif u == "leipziger Kubikfuß":
            r["recomp"] = baufuss["base"] ** 3; r["rule"] = "(Baufuß 0,282655 m)³"
        elif u == "Klafter":
            m = re.search(r"\(([0-9 /]+) (?:Kubikfuß|nürnberger Kubikellen)\)", r["definition"])
            n = mixed(m.group(1))
            if d == "Lobenstein":
                r["recomp"] = n * (r["ref_len"] / LIN_PER_M) ** 3
                r["rule"] = f"{m.group(1)} × (134,75 par. L. ÷ 443,296)³"
            else:
                r["recomp"] = n * kubikfuss["base"]
                r["rule"] = f"{m.group(1)} Kubikfuß × 0,022582 m³"
        elif u in ("Ruthe", "Schachtruthe") and r["value"] is not None:
            n = 96 if u == "Ruthe" else 27
            r["recomp"] = n * elle_leipz["base"] ** 3
            r["rule"] = f"{n} leipziger Kubikellen × (0,565311 m)³"
        elif u == "preuß. Meile":
            r["recomp"] = 2000 * pruthe["base"]; r["rule"] = "2000 preuß. Ruthen × 3,766242 m"
    for r in recs:
        if r["recomp"] is not None:
            r["recomp"] = round(r["recomp"], 6)
            r["dev"] = round((r["base"] - r["recomp"]) / r["recomp"] * 100, 4)
            r["check"] = "ok" if abs(r["dev"]) <= TOL_PCT else "abweichend"
        else:
            r["dev"] = None; r["check"] = ""
    return recs


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print("LIN_PER_M", LIN_PER_M)
    for r in build():
        print(r["unit"], "|", r["district"], "|", r["base"], r["unit_base"], "|", r["recomp"], r["dev"], r["check"], "|", r["rule"])
