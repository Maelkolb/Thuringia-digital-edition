"""Prepares the school places and school links for kirche-schule (map chart).

Reads the archived dataset `schools` of orte-schulen-gemeindehaushalt (173 municipalities), corrects one
misclassification (Kleinfalke), joins coordinates from the shared place layer and adds the school place
each village without a school belonged to (read from the place articles, G1 to G6).
"""
import json
import re
import sys
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\F7")
from common import *
from gaz import load_entities, text_of

import os
os.chdir(ROOT)

# village without school -> (school place, regex that finds the sentence in the article, status)
LINKS = {
    "Ernsee": ("Frankenthal", r"schult mit 23 Kindern nach Frankenthal"),
    "Cuba": ("Untermhaus", r"schult seit 1696 nach Untermhaus"),
    "Bieblach": ("Tinz", r"nach Tinz oder Gera zur Schule"),
    "Debschwitz": ("Lusan", r"Seitdem gehen die Kinder nach Lusan"),
    "Oberröppisch": ("Lusan", r"schult aber nach Lusan"),
    "Zeulsdorf": ("Dürrenebersdorf", r"Seine Schule hat Zeulsdorf in Dürrenebersdorf"),
    "Weißig": ("Dürrenebersdorf", r"wohin auch Weißig mit 18 Kindern schult"),
    "Gorlitzsch": ("Sirbis", r"nach Sirbis geschult"),
    "Schöna": ("Hundhaupten", r"Schöna schult nach Hundhaupten"),
    "Kleinsaara": ("Großsaara", r"schult von jeher nach Großsaara"),
    "Langengrobsdorf": ("Geißen", r"schult nach Geißen"),
    "Windischenbernsdorf": ("Frankenthal", r"schult, dermalen mit 60 Kindern, nach Frankenthal"),
    "Scheubengrobsdorf": ("Frankenthal", r"nach dem 1/4 Stunde entfernten Frankenthal"),
    "Milbitz": ("Thieschitz", r"nach dem ganz nahen Thieschütz"),
    "Rubitz": ("Thieschitz", r"jetzt mit 43 Kindern, nach Thieschitz"),
    "Töppeln": ("Frankenthal", r"schult, jetzt mit 37 Kindern, nach Frankenthal"),
    "Pörsdorf": ("Rüdersdorf", r"Pörsdorf hat seine Schule in Rüdersdorf"),
    "Niederndorf": ("Harpersdorf", r"Der Ort schult nach Harpersdorf"),
    "Kaltenborn": ("Harpersdorf", r"Schule in Harpersdorf"),
    "Stübnitz": ("Rüdersdorf", r"schult nach Rüdersdorf"),
    "Grüna": ("Reichardsdorf", r"schult aber seit Anfang dieses Jahrhunderts nach Reichardsdorf"),
    "Stublach": ("Langenberg", r"schult \(mit 27 Kindern\) nach Langenberg"),
    "Steinbrücken": ("Roben", r"schult nach Roben"),
    "Rusitz": ("Roben", r"schult von jeher nach Roben"),
    "Lessen": ("Großaga", r"schult nach Großaga"),
    "Kleinaga": ("Großaga", r"schult mit 46 Kindern nach Großaga"),
    "Reichenbach": ("Großaga", r"schult mit circa 13 Kindern nach Großaga"),
    "Seeligenstädt": ("Dorna", r"schult nach Dorna"),
    "Hermsdorf": ("Heukewalde", r"nach Heukewalde"),
    "Kretzschwitz": ("Dorna", r"schult nach Dorna"),
    "Söllmnitz": ("Wernsdorf", r"seitdem nach Wernsdorf"),
    "Bethenhausen": ("Hirschfeld", r"Der Ort schult nach Hirschfeld"),
    "Naundorf": ("Großenstein", r"schult nach seinem Pfarrdorfe Großenstein"),
    "Caasen": ("Groitschen", r"Schule, Grabstätte und Kirche in Groitschen"),
    "Waaswitz": ("Groitschen", r"mit Groitschen verbunden worden"),
    "Culm": ("Groitschen", r"schult aber nach Groitschen"),
    "Zschippach": ("Dorna", r"Zschippach schult nach Dorna"),
    "Negis": ("Dorna", r"von jeher nach Dorna"),
    "Schwaara": ("Trebnitz", r"nach Trebnitz geschult"),
    "Laasen": ("Trebnitz", r"nach Trebnitz gepfarrt und geschult"),
    "Zschippern": ("Thränitz", r"schult seit früher Zeit nach Thränitz"),
    "Collis": ("Thränitz", r"nach dem weimarer Kirchdorf Thränitz"),
    "Lichtenberg": ("Niebra", r"nach dem 3/4 Stunde entfernten Kirchdorf Niebra"),
    "Pohlen": ("Wolfersdorf", r"Pohlen schult nach seinem 1 Stunde entfernten Mutterkirchdorf"),
    "Otticha": ("Niebra", r"Auch schult es dahin"),
    "Rödersdorf": ("Tegau", r"seit 1605 ist er nach Tegau geschult"),
    "Dragensdorf": ("Dittersdorf", r"auch dahin mit 27 Kindern schult"),
    "Burkersdorf": ("Pahren", r"Dahin schult auch Burkersdorf"),
    "Hirschbach": ("Langenwetzendorf", r"Der Ort schult, kircht"),
    "Neuärgerniß": ("Göttendorf", r"1865 nach Göttendorf geschult"),
    "Pöllwitz": ("Altpöllwitz", r"Neupöllwitz schickt 15 Kinder zur Schule"),
    "Kleinwolschendorf": ("Langenwolschendorf", r"schult wie früher so heute nach Langenwolschendorf"),
    "Frankendorf": ("Tanna", r"schult, pfarrt, begräbt, verkehrt und blickt nach Tanna"),
    "Oberkoskau": ("Unterkoskau", r"wohin es pfarrt, schult und begräbt"),
    "Spielmes": ("Stelzen", r"seitdem schult der ganze Ort nach Stelzen"),
    "Pöritzsch": ("Zoppothen", r"schult nach Zoppothen"),
    "Karolinenfield": ("Remptendorf", r"schult mit neun Schulkindern dahin"),
    "Kießling": ("Harra", r"schulen auch dahin"),
    "Pirk": ("Lerchenhügel", r"seitdem nach Lerchenhügel"),
}
# Bieblach may attend Tinz or Gera (both are mentioned); the second link is added separately
EXTRA_LINKS = [("Bieblach", "Gera", r"nach Tinz oder Gera zur Schule")]
# own school although the gazetteer field says otherwise (checked in the article, p. 566 to 567)
# GeoNames name match is a different place (Reichenbach is 3/4 hour south of Großaga, the matched point is 16 km away)
BAD_COORDINATES = {"Reichenbach"}
CORRECTIONS = {"Kleinfalke": {"exists": True, "note": "eigene Schule seit 1810 (S. 567), im Gazetteer-Feld fälschlich ohne Schule"}}


def build():
    arch = archive_dataset("orte-schulen-gemeindehaushalt", "schools")
    cols = [c["name"] for c in arch["columns"]]
    rows = [dict(zip(cols, r)) for r in arch["rows"]]
    base_rows = shared_dataset("base_places.json")["rows"]
    base_by_name = {}
    for r in base_rows:
        base_by_name.setdefault(r[0], []).append(r)

    def base_lookup(name, landestheil):
        cands = base_by_name.get(name, [])
        for r in cands:
            if r[3] == landestheil:
                return r
        return cands[0] if len(cands) == 1 else None

    ents = load_entities()
    out = []
    for r in rows:
        own = r["status_de"] == "eigene Schule"
        if r["name"] in CORRECTIONS:
            own = CORRECTIONS[r["name"]]["exists"]
        b = base_lookup(r["name"], r["landestheil"])
        if r["name"] in BAD_COORDINATES:
            b = None
        out.append({
            "name": r["name"], "landestheil": r["landestheil"], "kind": r["class_de"], "inhabitants": r["inhabitants"],
            "own": own, "pupils": r["pupils"],
            "lon": b[1] if b else None, "lat": b[2] if b else None,
        })
    by = {(o["name"], o["landestheil"]): o for o in out}
    by_name = {}
    for o in out:
        by_name.setdefault(o["name"], []).append(o)
    links = []
    link_refs = []
    names_in_dataset = set(by_name)
    for place, (target, pat) in LINKS.items():
        e = ents[place]
        found = None
        for p, bid, t in text_of(e):
            if re.search(pat, t):
                found = (p, bid)
                break
        assert found, (place, pat)
        links.append({"place": place, "school_place": target, "page": str(found[0]), "block": found[1]})
        link_refs.append(ref(found[0], found[1]))
    for place, target, pat in EXTRA_LINKS:
        e = ents[place]
        for p, bid, t in text_of(e):
            if re.search(pat, t):
                links.append({"place": place, "school_place": target, "page": str(p), "block": bid})
                break
    # school place of every village without school
    for o in out:
        if not o["own"] and o["name"] not in LINKS:
            raise SystemExit(f"missing link for {o['name']}")
    for l in links:
        o = by_name[l["place"]][0]
        cands = by_name.get(l["school_place"], [])
        t = next((c for c in cands if c["landestheil"] == o["landestheil"]), cands[0] if cands else None)
        if t is None:
            tb = base_lookup(l["school_place"], o["landestheil"])
            l["school_lon"], l["school_lat"] = (tb[1], tb[2]) if tb else (None, None)
        else:
            l["school_lon"], l["school_lat"] = t["lon"], t["lat"]
        l["place_lon"], l["place_lat"] = o["lon"], o["lat"]
        l["drawn"] = all(v is not None for v in (l["school_lon"], l["school_lat"], l["place_lon"], l["place_lat"]))
        l["inside"] = l["school_place"] in names_in_dataset
    return out, links, arch["source_refs"], link_refs


if __name__ == "__main__":
    out, links, refs, lrefs = build()
    print(len(out), sum(o["own"] for o in out), sum(not o["own"] for o in out))
    print("with coordinates", sum(o["lon"] is not None for o in out))
    print("links", len(links), "drawn", sum(l["drawn"] for l in links))
    for l in links:
        if not l["drawn"]:
            print("not drawn:", l["place"], "->", l["school_place"], "inside" if l["inside"] else "outside", l["place_lon"], l["school_lon"])
    miss_pup = [o["name"] for o in out if o["own"] and o["pupils"] is None]
    print("own school without pupil number:", miss_pup)
    print("outside targets:", sorted({l["school_place"] for l in links if not l["inside"]}))
    print("targets not own school in dataset:", sorted({l["school_place"] for l in links if l["inside"] and not next(o for o in out if o["name"]==l["school_place"])["own"]}))
