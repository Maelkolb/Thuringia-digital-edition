"""Independent check: recompute the numbers quoted in the lead, findings, titles and captions of the three F7 features
from the datasets stored in the published JSON files and assert that they occur in the German and English texts."""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(r"C:\Users\totom\Projects\reuss-edition\data\analyses")


def load(fid):
    return json.loads((ROOT / f"{fid}.json").read_text(encoding="utf-8"))


def table(d, name):
    ds = next(x for x in d["datasets"] if x["name"] == name)
    cols = [c["name"] for c in ds["columns"]]
    return [dict(zip(cols, r)) for r in ds["rows"]]


def texts(d):
    out = {"de": [], "en": []}
    for lang in out:
        out[lang] += [d["summary"][lang]] + [f[lang] for f in d.get("findings", [])]
        for c in d["charts"]:
            out[lang] += [c["title"][lang], c["caption"][lang]]
    return {k: " ".join(v) for k, v in out.items()}


def de(x, k=0):
    return f"{x:,.{k}f}".replace(",", "§").replace(".", ",").replace("§", ".")


def en(x, k=0):
    return f"{x:,.{k}f}"


bad = 0


def expect(txt, label, de_s, en_s):
    global bad
    for lang, s in (("de", de_s), ("en", en_s)):
        ok = s in txt[lang]
        if not ok:
            bad += 1
        print(("ok   " if ok else "MISS ") + f"[{lang}] {label}: {s}")


# ---------------------------------------------------------------- verfassung-verwaltung
d = load("verfassung-verwaltung")
t = texts(d)
rep = table(d, "representation")
towns = next(r for r in rep if r["group_en"] == "Towns")
rural = next(r for r in rep if r["group_en"] != "Towns")
assert towns["population"] + rural["population"] == 87974
expect(t, "inhabitants per urban seat", de(towns["population"] / towns["seats"]), en(towns["population"] / towns["seats"]))
expect(t, "inhabitants per rural seat", de(rural["population"] / rural["seats"]), en(rural["population"] / rural["seats"]))
expect(t, "factor", de(rural["population"] / rural["seats"] / (towns["population"] / towns["seats"]), 1), en(rural["population"] / rural["seats"] / (towns["population"] / towns["seats"]), 1))
expect(t, "share towns", de(towns["population"] / 87974 * 100), en(towns["population"] / 87974 * 100))
off = table(d, "officials")
for m, n_ in (("Gendarmen", 24), ("Ärzte", 32), ("Justizämter", 8)):
    assert sum(r["count"] for r in off if r["measure_de"] == m) == n_
    expect(t, f"total {m}", str(n_), str(n_))
doc = [r["per_10000"] for r in off if r["measure_de"] == "Ärzte"]
expect(t, "physicians per 10,000 range", f"{de(min(doc), 1)} bis {de(max(doc), 1)}", f"{en(min(doc), 1)} to {en(max(doc), 1)}")
gen = {r["district"]: r for r in off if r["measure_de"] == "Gendarmen"}
expect(t, "gendarmes Gera / Lobenstein", f"{de(gen['Gera']['per_10000'], 1)} im Landesteil Gera, {de(gen['Lobenstein-Ebersdorf']['per_10000'], 1)}", f"{en(gen['Gera']['per_10000'], 1)} in the Gera district, {en(gen['Lobenstein-Ebersdorf']['per_10000'], 1)}")
per_sqm = [r["per_sqm"] for r in gen.values()]
expect(t, "gendarmes per sqm", f"{de(min(per_sqm), 1)} bis {de(max(per_sqm), 1)}", f"{en(min(per_sqm), 1)} to {en(max(per_sqm), 1)}")
cont = table(d, "contingent")
expect(t, "contingent first/last", f"{int(cont[0]['total'])} Mann", f"{int(cont[0]['total'])} men")
expect(t, "contingent last", f"{int(cont[-1]['total'])} Mann", f"{int(cont[-1]['total'])} men")
expect(t, "factor 37", f"{de(cont[-1]['total'] / cont[0]['total'])}fache", f"{en(cont[-1]['total'] / cont[0]['total'])}-fold")

# ---------------------------------------------------------------- kirche-schule
d = load("kirche-schule")
t = texts(d)
pl = table(d, "schulorte")
own = [r for r in pl if r["school"] == "eigene Schule"]
expect(t, "own school", f"{len(own)} von {len(pl)} Orten", f"{len(own)} of {len(pl)} places")
for lt in ("Gera", "Schleiz", "Lobenstein-Ebersdorf"):
    xs = [r for r in pl if r["landestheil"] == lt]
    o = [r for r in xs if r["school"] == "eigene Schule"]
    expect(t, f"share {lt}", f"{de(len(o) / len(xs) * 100)} Prozent", f"{en(len(o) / len(xs) * 100)} percent")
sl = table(d, "schulen_lehrer")
land = [r for r in sl if r["name_de"].endswith(", Land")]
lo, hi = min(r["pupils_per_teacher"] for r in land), max(r["pupils_per_teacher"] for r in land)
expect(t, "country range", f"{de(lo)} bis {de(hi)}", f"{en(lo)} to {en(hi)}")
land_avg = sum(r["pupils"] for r in land) / sum(r["teachers"] for r in land)
expect(t, "country average", de(land_avg), en(land_avg))
gy = [r["pupils_per_teacher"] for r in sl if r["name_de"].startswith("Gymnasium")]
expect(t, "gymnasium range", f"{de(min(gy))} bis {de(max(gy))}", f"{en(min(gy))} to {en(max(gy))}")
vol = [r for r in sl if r["kind"] == "Volksschule"]
expect(t, "volksschulen totals", f"{sum(r['schools'] for r in vol)} Volksschulen mit {sum(r['teachers'] for r in vol)} Lehrern und {de(sum(r['pupils'] for r in vol))} Schülern", f"{sum(r['schools'] for r in vol)} elementary schools with {sum(r['teachers'] for r in vol)} teachers and {en(sum(r['pupils'] for r in vol))} pupils")
pay = table(d, "gehaelter")
posts = sum(r["posts"] for r in pay if r["posts"])
expect(t, "posts >= 800", f"{sum(r['posts'] for r in pay if r['posts'] and r['lo'] >= 800)} von {posts} Pfarrstellen", f"{sum(r['posts'] for r in pay if r['posts'] and r['lo'] >= 800)} of {posts} pastorates")
expect(t, "lowest pastorate", f"zahlte {min(r['lo'] for r in pay if r['kind'] == 'Pfarrer')}", f"paid {min(r['lo'] for r in pay if r['kind'] == 'Pfarrer')}")
eph = table(d, "ephorien")
expect(t, "ephories", f"{sum(r['parishes'] for r in eph)} Parochien, {sum(r['churches'] for r in eph)} Kirchen und {sum(r['clergy'] for r in eph)} Geistlichen", f"{sum(r['parishes'] for r in eph)} parishes, {sum(r['churches'] for r in eph)} churches and {sum(r['clergy'] for r in eph)} clergy")

# ---------------------------------------------------------------- armenwesen-stiftungen
d = load("armenwesen-stiftungen")
t = texts(d)
soc = table(d, "societies")
fou = table(d, "foundations")
sti = table(d, "stipends")
tl = table(d, "gruendungen")
expect(t, "societies", f"{len(soc)} Selbsthilfeeinrichtungen", f"{len(soc)} self-help institutions")
n1860 = sum(1 for r in soc if 1860 <= r["year"] <= 1869)
expect(t, "1860s", f"{n1860} der {len(soc)}", f"{n1860} of the {len(soc)}")
expect(t, "before 1850", f"Nur {sum(1 for r in soc if r['year'] < 1850)} der", f"Only {sum(1 for r in soc if r['year'] < 1850)} of the")
cap = sum(r["capital"] for r in fou)
first = max(r["capital"] for r in fou)
expect(t, "capital total", de(cap), en(cap))
expect(t, "capital first", de(first), en(first))
expect(t, "capital others", de(cap - first), en(cap - first))
expect(t, "share first", f"{de(first / cap * 100)} Prozent", f"{en(first / cap * 100)} percent")
prince = sum(r["capital"] for r in fou if r["group_de"] == "Fürstenhaus")
expect(t, "share princely", f"{de(prince / cap * 100)} Prozent", f"{en(prince / cap * 100)} percent")
expect(t, "stipends annual", f"{len(sti)} Stipendien mit {de(round(sum(r['annual_total'] for r in sti)))} Taler", f"{len(sti)} stipends with {en(round(sum(r['annual_total'] for r in sti)))} thalers")
expect(t, "first stipend", str(min(r["year"] for r in tl if r["kind"] == "Stipendium")), str(min(r["year"] for r in tl if r["kind"] == "Stipendium")))
expect(t, "dated institutions", f"aller {len(tl)} datierten", f"all {len(tl)} dated")
orte = table(d, "selbsthilfe_orte")
gera = next(r for r in orte if r["place"] == "Gera")
expect(t, "Gera mentions", f"allein {gera['institutions']} nennen", f"{gera['institutions']} name the town of Gera")
print("\nMISSING:", bad)
