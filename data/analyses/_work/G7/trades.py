"""Harmonisation of the craft / trade names of the place articles (analysis 3)."""
import re

GROUPS = {1: ("Bau, Stein", "Building, stone"), 2: ("Holz", "Wood"),
          3: ("Metall", "Metal"), 4: ("Textil", "Textiles"), 5: ("Leder, Kleidung", "Leather, clothing"),
          6: ("Nahrung, Wirte", "Food, inns"), 7: ("Übrige", "Other")}

# canonical trade -> (group, English name, verbatim spellings)
TRADES = {
    "Maurer": (1, "Mason", ["Maurer", "Maurermeister"]),
    "Zimmerer": (1, "Carpenter", ["Zimmerleute", "Zimmermann", "Zimmerer", "Zimmermeister"]),
    "Dachdecker": (1, "Roofer (slater, tiler)", ["Schieferdecker", "Dachdecker", "Ziegel- und Schieferdecker"]),
    "Glaser": (1, "Glazier", ["Glaser"]),
    "Steinhauer": (1, "Stonecutter", ["Steinhauer", "Steinmetzen", "Steinmetz"]),
    "Ziegler": (1, "Brick maker", ["Ziegelbrenner", "Ziegler", "Ziegelbrennerei"]),
    "Tischler": (2, "Joiner", ["Tischler", "Harmonikatischler"]),
    "Wagner": (2, "Wheelwright", ["Wagner", "Stellmacher"]),
    "Böttcher": (2, "Cooper", ["Böttcher"]),
    "Drechsler": (2, "Turner", ["Drechsler"]),
    "Korbmacher": (2, "Basket maker", ["Korbmacher"]),
    "Seiler": (2, "Rope maker", ["Seiler"]),
    "Schmied": (3, "Blacksmith", ["Schmied", "Schmiede", "Hufschmied", "Hufschmiede"]),
    "Schlosser": (3, "Locksmith", ["Schlosser"]),
    "Klempner": (3, "Tinsmith", ["Klempner", "Klemptner"]),
    "Weber": (4, "Weaver", ["Weber", "Leinweber", "Leineweber", "Webermeister", "Zeug- und Leinweber", "Zeugmacher"]),
    "Strumpfwirker": (4, "Stocking weaver", ["Strumpfwirker"]),
    "Tuchmacher": (4, "Cloth maker", ["Tuchmacher"]),
    "Färber": (4, "Dyer", ["Färber"]),
    "Posamentirer": (4, "Trimmings maker", ["Posamentirer"]),
    "Schneider": (5, "Tailor", ["Schneider"]),
    "Schuhmacher": (5, "Shoemaker", ["Schuhmacher"]),
    "Gerber": (5, "Tanner", ["Gerber", "Rothgerber", "Weißgerber", "Lohgerber"]),
    "Sattler": (5, "Saddler", ["Sattler"]),
    "Fleischer": (6, "Butcher", ["Fleischer"]),
    "Bäcker": (6, "Baker", ["Bäcker"]),
    "Müller": (6, "Miller", ["Müller"]),
    "Brauer": (6, "Brewer", ["Brauer"]),
    "Wirt": (6, "Innkeeper", ["Wirth", "Wirthe", "Schenkwirthe"]),
    "Seifensieder": (7, "Soap boiler", ["Seifensieder"]),
    "Krämer und Händler": (7, "Shopkeeper and dealer", ["Krämer", "Händler", "Kleinkrämer", "Handelsleute", "Handelsconcessionisten"]),
    "Uhrmacher": (7, "Watchmaker", ["Uhrmacher"]),
    "Gärtner": (7, "Gardener", ["Gärtner"]),
    "Barbier": (7, "Barber", ["Barbier", "Barbierer"]),
}
VERB = {}
for canon, (g, en, vs) in TRADES.items():
    for v in vs:
        VERB[v] = canon

JOURNEYMEN = re.compile(r"(gesellen|gehilfen|Gesellen)$")


def canon(key):
    """canonical trade of a verbatim key, or None for journeymen."""
    base = re.sub(r"\s*\(zugleich[^)]*\)", "", key).strip()
    if JOURNEYMEN.search(base):
        return None
    return VERB.get(base, base)


def info(c):
    if c in TRADES:
        g, en, _ = TRADES[c]
        return g, en
    return 7, c
