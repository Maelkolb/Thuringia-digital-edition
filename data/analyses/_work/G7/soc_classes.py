"""Harmonisation of the occupational/social classes of the village articles (analysis 2)."""
FARM = {"Bauern", "Pferdebauern", "Kühbauern", "Ochsenbauern", "Hofbauern", "Halbbauern", "Viertelsbauern",
        "große Bauern", "halbe Bauern", "Kleinbauern", "Gutsbauer", "Landwirthe", "Oeconomen",
        "Bäuerlein mit Nebengeschäft"}
HAUS = {"Häusler", "Kleinhäusler", "Feldhäusler", "Hintersiedler", "Hintersattler", "Tropfhäusler",
        "Hausgenossen", "Kleinleute"}
TAG = {"Taglöhner", "Handarbeiter", "Hand- oder Fabrikarbeiter", "Fabrikarbeiter"}
DIENST = {"Dienstboten", "Knechte", "Mägde"}
COMBINED = {"Häusler und Taglöhner", "Taglöhner und Dienstboten"}

# keys that are only a subset of another key of the same article ("darunter ...") and must not be added
SUBSET = {
    "lessen": {"Pferdebauern"}, "wernsdorf-gera": {"Pferdebauern"}, "hirschfeld": {"Pferdebauern"},
    "collis": {"Pferdebauern"}, "otticha": {"Pferdebauern"}, "stublach": {"Pferdebauern"},
    "lusan": {"Fabrikarbeiter", "Handarbeiter"},
}
# explicit statements in the text that a class is absent / has a number the JSON lacks
OVERRIDE = {
    "lerchenhuegel": {"Bauern": 0},     # "keine Privatgüter" (Waldkolonie)
    "karolinenfield": {"Bauern": 0},    # nur Gutspächter, 8 Häusler, 2 Taglöhner, 6 Dienstboten
    "pirk": {"Bauern": 0},              # "aus 33 Häuslern, 11 Handarbeitern und 9 Dienstboten"
    "blankenstein": {"Bauern": 1},      # "nur das Rittergut und ein Bauer"
    "niederboehmsdorf": {"Hausen_special": True},
}


def classes_for(uid, occ):
    """-> dict class -> count (None = not stated), or None if the entry is unusable."""
    if any(k in occ for k in COMBINED):
        return None
    ign = SUBSET.get(uid, set())
    out = {"Bauern": None, "Häusler": None, "Taglöhner": None, "Dienstboten": None}
    for k, v in occ.items():
        if k in ign or not isinstance(v, (int, float)):
            continue
        for name, S in (("Bauern", FARM), ("Häusler", HAUS), ("Taglöhner", TAG), ("Dienstboten", DIENST)):
            if k in S:
                out[name] = (out[name] or 0) + v
    if uid == "niederboehmsdorf":
        # "60 Häusler und 26 Hintersiedler (darunter 15 Taglöhner)": Taglöhner are part of the Hintersiedler
        out["Häusler"] = 60 + (26 - 15)
        out["Taglöhner"] = 15
    for k, v in OVERRIDE.get(uid, {}).items():
        if k in out:
            out[k] = v
    return out
