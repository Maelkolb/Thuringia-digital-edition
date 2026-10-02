"""Independent check: recompute the headline numbers from the datasets inside the written feature files
and assert that they occur in the German and English texts (titles, summary, findings, captions)."""
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
from common import OUT, num

fails = []


def load(fid):
    return json.load(open(OUT + fid + ".json", encoding="utf-8"))


def rows(d, name):
    ds = next(x for x in d["datasets"] if x["name"] == name)
    cols = [c["name"] for c in ds["columns"]]
    return [dict(zip(cols, r)) for r in ds["rows"]]


def texts(d, lang):
    t = [d["title"][lang], d["summary"][lang]] + [f[lang] for f in d["findings"]]
    for c in d["charts"]:
        t += [c["title"][lang], c["caption"][lang]]
    return " ".join(t)


def expect(d, label, value, dec=0):
    for lang in ("de", "en"):
        s = num(value, dec, lang)
        if s not in texts(d, lang):
            fails.append(f"{d['id']} [{lang}] {label}: '{s}' not found")


# --- geburten-sterbefaelle
d = load("geburten-sterbefaelle")
v = [r for r in rows(d, "vital") if r["district"] == "Reuß j. L."]
expect(d, "births", sum(r["births"] for r in v))
expect(d, "deaths", sum(r["deaths"] for r in v))
expect(d, "stillborn", sum(r["stillborn"] for r in v))
expect(d, "surplus", sum(r["births"] - r["deaths"] for r in v))
expect(d, "min surplus", min(r["births"] - r["deaths"] for r in v))
expect(d, "max surplus", max(r["births"] - r["deaths"] for r in v))
expect(d, "births per year", sum(r["births"] for r in v) / len(v))
expect(d, "deaths per year", sum(r["deaths"] for r in v) / len(v))
m = {(r["district"], r["area"]): r for r in rows(d, "marriages_mean")}
expect(d, "marriages per year", m[("Reuß j. L.", "Zusammen")]["pairs"])
im = {(r["district"], r["area"]): r["illegit_pct"] for r in rows(d, "illegit_mean")}
for k in [("Reuß j. L.", "Zusammen"), ("Lobenstein-Ebersdorf", "Zusammen"), ("Schleiz", "Zusammen"), ("Gera", "Zusammen")]:
    expect(d, f"illegit {k}", im[k], 1)
il = {(r["year"], r["district"], r["area"]): r["illegit_pct"] for r in rows(d, "illegit")}
expect(d, "illegit 1858", il[(1858, "Reuß j. L.", "Zusammen")], 1)
expect(d, "illegit 1867", il[(1867, "Reuß j. L.", "Zusammen")], 1)
p = rows(d, "periods")
tot = {}
for r in p:
    a = tot.setdefault(r["district"], [0, 0])
    a[0] += r["natural_increase"]
    a[1] += r["increase"]
expect(d, "nat total", tot["Fürstentum"][0])
expect(d, "inc total", tot["Fürstentum"][1])
expect(d, "mig total", tot["Fürstentum"][0] - tot["Fürstentum"][1])
expect(d, "mig lob", tot["Lobenstein-Ebersdorf"][0] - tot["Lobenstein-Ebersdorf"][1])
expect(d, "share lost", (tot["Fürstentum"][0] - tot["Fürstentum"][1]) / tot["Fürstentum"][0] * 100)

# --- alter-familie
d = load("alter-familie")
ac = {r["age_class"]: r for r in rows(d, "age_classes_econ") if r["region"] == "Reuß j. L. (1864)"}
expect(d, "youth", ac["Jugend (0–14 Jahre)"]["permille_total"] / 10, 1)
expect(d, "old", ac["Greisenalter (über 60 Jahre)"]["permille_total"] / 10, 1)
expect(d, "pop", sum(r["total"] for r in ac.values()))
sy = rows(d, "single_years")
men = sum(r["persons"] for r in sy if r["sex"] == "männlich")
women = sum(r["persons"] for r in sy if r["sex"] == "weiblich")
expect(d, "women per 100", women / men * 100, 1)
expect(d, "first year", sum(r["persons"] for r in sy if r["age"] == 1))
mb = {(r["age_class"], r["sex"]): r["share_pct"] for r in rows(d, "married_by_age") if r["area"] == "Fürstentum"}
expect(d, "m60", mb[("über 60", "männlich")], 1)
expect(d, "f60", mb[("über 60", "weiblich")], 1)
cc = {(r["sex"], r["status"]): r["persons"] for r in rows(d, "civil_counts") if r["district"] == "Fürstentum" and r["settlement"] == "insgesamt"}
expect(d, "widows", cc[("weiblich", "verwitwet")])
expect(d, "widowers", cc[("männlich", "verwitwet")])
bp = {(r["district"], r["origin"]): r["pct"] for r in rows(d, "birthplace") if r["area"] == "Zusammen"}
expect(d, "home lob", bp[("Lobenstein-Ebersdorf", "Geburtsgemeinde")], 2)
expect(d, "home gera", bp[("Gera", "Geburtsgemeinde")], 2)
expect(d, "away", bp[("Reuß j. L.", "auswärts")], 1)
expect(d, "home all", bp[("Reuß j. L.", "Geburtsgemeinde")], 0)

# --- gesundheit
d = load("gesundheit")
mean = {r["category_de"]: r for r in rows(d, "mean")}
expect(d, "fit count", mean["Brauchbar"]["avg_count"])
assert round(mean["Brauchbar"]["pct_mean"] / 10) == 3  # title: "drei von zehn"
under = next(r for k, r in mean.items() if k.startswith("Unterw"))
expect(d, "under", under["pct_mean"], 1)
sk = {r["place"]: r["percent"] for r in rows(d, "diseases") if r["disease_de"].startswith("Krätze")}
expect(d, "skin gera", sk["Gera"], 1)
for r in rows(d, "gera_skin"):
    expect(d, "gera skin period", r["percent_printed"], 1)
ev = rows(d, "events")
expect(d, "208", next(r for r in ev if r["year"] == 1756)["value"])
expect(d, "gap", 1826 - 1756)
dis = {r["condition"]: r["count_total"] for r in rows(d, "disability") if r["district"] == "Reuß j. L." and r["year"] == 1867 and r["area"] == "Überhaupt"}
expect(d, "deaf", dis["Taubstumme"])
expect(d, "blind", dis["Blinde"])

# --- siedlung-wohnen
d = load("siedlung-wohnen")
pl = rows(d, "places")
tp = sum(r["inhabitants"] for r in pl)
expect(d, "total pop", tp)
expect(d, "n places", len(pl))
expect(d, "small", sum(1 for r in pl if r["inhabitants"] < 1000))
expect(d, "big", sum(1 for r in pl if r["inhabitants"] >= 1000))
expect(d, "share big", sum(r["inhabitants"] for r in pl if r["inhabitants"] >= 1000) / tp * 100)
expect(d, "share gera", next(r for r in pl if r["name"] == "Gera")["inhabitants"] / tp * 100, 1)
expect(d, "gera", next(r for r in pl if r["name"] == "Gera")["inhabitants"])
expect(d, "schleiz", next(r for r in pl if r["name"] == "Schleiz")["inhabitants"])
expect(d, "<=500", sum(1 for r in pl if r["inhabitants"] <= 500))
expect(d, "located", sum(1 for r in pl if r["lon"] is not None))
h = {(r["district"], r["settlement"]): r["persons_per_house"] for r in rows(d, "houses")}
expect(d, "pph all", h[("Fürstentum", "Zusammen")], 2)
expect(d, "pph towns", h[("Fürstentum", "Städte")], 2)
expect(d, "pph rural", h[("Fürstentum", "Landorte")], 2)
expect(d, "pph gera", h[("Gera", "Städte")], 2)
expect(d, "pph gera rural", h[("Gera", "Landorte")], 1)
cmp = {r["region"]: r["persons_per_house"] for r in rows(d, "persons_per_house_compare")}
expect(d, "thuringia", cmp["Thüringen (Durchschnitt)"], 2)
expect(d, "saxony", cmp["Sachsen"], 2)
ch = rows(d, "new_churches")
expect(d, "n churches", len(ch))
expect(d, "peak", sum(1 for r in ch if 1710 <= r["year_start"] < 1740))
expect(d, "17th", sum(1 for r in ch if r["year_start"] < 1700))
expect(d, "18th", sum(1 for r in ch if 1700 <= r["year_start"] < 1800))

print("\n".join(fails) if fails else "all checks passed")
sys.exit(1 if fails else 0)
