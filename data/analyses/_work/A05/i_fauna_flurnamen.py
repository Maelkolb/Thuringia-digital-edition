"""Analysis: animal names in field and place names (p. 82)."""
import re
from collections import Counter
from common import *

t = text("82", "b1")
body = t.split("folgende: ", 1)[1].split(". Ob der Lauseberg", 1)[0]
items = [x.strip() for x in body.split(", ")]
print(len(items), items[:5], items[-3:])

# prefix -> (animal de, animal en, group de, group en, gone?)
A = [
    ("Wisent", "Wisent", "Wisent (European bison)", "S", 1), ("Bär", "Bär", "Bear", "S", 1), ("Wolf", "Wolf", "Wolf", "S", 1), ("Wölfe", "Wolf", "Wolf", "S", 1),
    ("Luchs", "Luchs", "Lynx", "S", 1), ("Fuchs", "Fuchs", "Fox", "S", 0), ("Hirsch", "Hirsch", "Red deer", "S", 0), ("Reh", "Reh", "Roe deer", "S", 0),
    ("Hasen", "Hase", "Hare", "S", 0), ("Dachs", "Dachs", "Badger", "S", 0), ("Eber", "Eber", "Boar", "S", 0), ("Iltis", "Iltis", "Polecat", "S", 0),
    ("Hamster", "Hamster", "Hamster", "S", 0), ("Igel", "Igel", "Hedgehog", "S", 0), ("Mäuse", "Maus", "Mouse", "S", 0), ("Otter", "Otter", "Otter", "S", 0),
    ("Falken", "Falke", "Falcon", "V", 0), ("Geier", "Geier", "Vulture", "V", 0), ("Staren", "Star", "Starling", "V", 0), ("Kranich", "Kranich", "Crane", "V", 0),
    ("Krähen", "Krähe", "Crow", "V", 0), ("Eulen", "Eule", "Owl", "V", 0), ("Lerchen", "Lerche", "Lark", "V", 0), ("Wachtel", "Wachtel", "Quail", "V", 0),
    ("Tauben", "Taube", "Pigeon, dove", "V", 0), ("Schwalben", "Schwalbe", "Swallow", "V", 0), ("Pfauen", "Pfau", "Peacock", "V", 0), ("Kröten", "Kröte", "Toad", "A", 0),
    ("Bär", "Bär", "Bear", "S", 1),
]
GRP = {"S": ("Säugetier", "Mammal"), "V": ("Vogel", "Bird"), "A": ("Lurch (Amphibie)", "Amphibian")}
rows = []
for it in items:
    base = re.sub(r"\s*\(.*\)", "", it)
    for pre, de_, en_, g, gone in A:
        if base.startswith(pre):
            rows.append([it, de_, en_, GRP[g][0], GRP[g][1], "ausgerottet/verschwunden" if gone else "vorhanden", "extirpated or vanished" if gone else "present", "82", "b1"])
            break
    else:
        raise AssertionError(it)
cnt = Counter(r[1] for r in rows)
n = len(rows)
gone_names = sum(1 for r in rows if r[5].startswith("ausgerottet"))
by_group = Counter(r[3] for r in rows)
print(n, gone_names, dict(by_group), cnt.most_common(8))
# group by animal for the chart
tab = []
for k, v in cnt.most_common():
    ex = [r[0] for r in rows if r[1] == k]
    r0 = next(r for r in rows if r[1] == k)
    tab.append([k, r0[2], r0[3], r0[4], r0[5], r0[6], v, ", ".join(ex)])
tab.sort(key=lambda r: (-r[6], r[0]))
# Brückner's statements on the vanished animals
need("Der Bär, Luchs und Wolf, die vormals in starker Zahl in den heimischen Waldgebieten hausten, sind seit einem Jahrhundert vollkommen ausgerottet", "82", "b2")
need("ist längst verschwunden", "83", "b1")
n_animals = len(cnt)
mam = by_group["Säugetier"]
bird = by_group["Vogel"]
top = cnt.most_common(3)
print(top)
pc = lambda a, b: 100 * a / b
wolf, bear, lynx = cnt["Wolf"], cnt["Bär"], cnt["Luchs"]

ana = {
    "id": "fauna-tiernamen-in-flurnamen",
    "title": bi("Tiernamen in Flur- und Ortsnamen", "Animal names in field and place names"),
    "category": "fauna",
    "section": "t1-1-9",
    "sources": [{"page": "82", "block": "b1"}, {"page": "82", "block": "b2"}, {"page": "83", "block": "b1"}],
    "summary": bi(
        f"Brückner führt als »topographische Fauna« {n} Flur- und Ortsnamen auf, die Tiere enthalten (Haustiere ausgenommen), und folgert, dass das Volk nur Wirbeltiere in Namen festgehalten habe. Ausgezählt gehören die Namen zu {n_animals} Tieren; am häufigsten sind Wolf, Bär und Hirsch. {de(pc(gone_names, n), 0)} % der Namen erinnern an ein Tier, das nach Brückner ausgerottet/verschwunden ist.",
        f"As “topographical fauna” Brückner lists {n} field and place names that contain animals (domestic animals excluded) and concludes that the people recorded only vertebrates in names. Counted, the names refer to {n_animals} animals; the most frequent are wolf, bear and deer. {en(pc(gone_names, n), 0)} % of the names recall an animal that, according to Brückner, is exterminated or vanished from the country."),
    "method": bi(
        f"Die Namenliste auf S. 82 wurde vollständig erfasst ({n} Namen, Doppelform »Bärenthal (auch Berthel)« einfach gezählt) und nach dem Tiernamen im Wortstamm einem Tier zugeordnet (Wolf-/Wölfe-, Bär-, Hirsch- usw.). Ob ein Tier im Land vorkommt, richtet sich nach Brückners Aussagen auf S. 82–83: Bär, Luchs und Wolf seien seit einem Jahrhundert ausgerottet, das Wisent längst verschwunden. Die Zuordnung zu Säugetier, Vogel und Lurch ist redaktionell. Der Hinweis auf den Lauseberg (»Ob der Lauseberg vom Insect den Namen hat, wird bezweifelt«) ist nicht mitgezählt.",
        f"The list of names on p. 82 was captured in full ({n} names; the double form “Bärenthal (auch Berthel)” counted once) and assigned to an animal by the animal name in the word stem (Wolf-/Wölfe-, Bär-, Hirsch- etc.). Whether an animal occurs in the country follows Brückner's statements on pp. 82–83: bear, lynx and wolf have been exterminated for a century, the wisent vanished long ago. The assignment to mammal, bird and amphibian is editorial. The remark on the Lauseberg (“Ob der Lauseberg vom Insect den Namen hat, wird bezweifelt”) was not counted."),
    "findings": [
        bi(f"Von den {n} Namen beziehen sich {mam} auf Säugetiere ({de(pc(mam, n), 0)} %), {bird} auf Vögel und {by_group['Lurch (Amphibie)']} auf einen Lurch (Kröte). Am häufigsten ist der Wolf ({wolf} Namen), danach der Bär ({bear}) und der Hirsch ({cnt['Hirsch']}).",
           f"Of the {n} names, {mam} refer to mammals ({en(pc(mam, n), 0)} %), {bird} to birds and {by_group['Lurch (Amphibie)']} to an amphibian (toad). The wolf is the most frequent ({wolf} names), followed by the bear ({bear}) and the deer ({cnt['Hirsch']})."),
        bi(f"Auf die vier Tiere, die nach Brückner ausgerottet oder verschwunden sind (Wolf, Bär, Luchs, Wisent), entfallen {gone_names} Namen ({de(pc(gone_names, n), 0)} %); sie erinnern an eine Fauna, die im Land seit mindestens hundert Jahren fehlt.",
           f"The four animals that according to Brückner are exterminated or vanished (wolf, bear, lynx, wisent) account for {gone_names} names ({en(pc(gone_names, n), 0)} %); they recall a fauna absent from the country for at least a hundred years."),
        bi("Nach Brückner halten die Namen nur Wirbeltiere fest (Säugetiere, Vögel, wenige Lurche); für alle übrigen Tierordnungen habe das Volk »kein Auge gehabt«. Auch die Zahlen stützen das für die erfassten Namen.",
           "According to Brückner the names record only vertebrates (mammals, birds, a few amphibians); for all other animal orders the people “had no eye”. The counts support this for the names captured."),
    ],
    "caveats": [
        bi("Namen wie Ebersberg, Ebersdorf, Starenburg oder Falkenberg können auch auf Personennamen oder Burgnamen zurückgehen; Brückner wertet alle als Zeugnisse der Fauna. Die Namen sind nicht datiert.",
           "Names such as Ebersberg, Ebersdorf, Starenburg or Falkenberg may also derive from personal or castle names; Brückner treats all as evidence of the fauna. The names are not dated."),
        bi("Eine Unterscheidung zwischen Flur- und Ortsnamen trifft Brückner nicht (Beispiele für Ortsnamen: Hirschberg, Ebersdorf, Igelsdorf). Der Eintrag »Wisent« steht vermutlich für den Flussnamen Wiesenthal (richtiger Wisentthal), den Brückner auf S. 83 so erklärt.",
           "Brückner makes no distinction between field and place names (examples of place names: Hirschberg, Ebersdorf, Igelsdorf). The entry “Wisent” presumably stands for the river name Wiesenthal (more correctly Wisentthal), which Brückner explains thus on p. 83."),
    ],
    "datasets": [
        {"name": "names",
         "title": bi("Namen mit Tierbezug (S. 82)", "Names with an animal reference (p. 82)"),
         "columns": [
             col("name", "Name (Druck)", "Name (print)", "string", None),
             col("animal_de", "Tier", "Animal", "string", None, True, "redaktionelle Zuordnung nach dem Wortstamm"),
             col("animal_en", "Tier (EN)", "Animal (EN)", "string", None, True),
             col("group_de", "Gruppe", "Group", "string", None, True),
             col("group_en", "Gruppe (EN)", "Group (EN)", "string", None, True),
             col("status_de", "Vorkommen heute nach Brückner", "Occurrence today according to Brückner", "string", None, True),
             col("status_en", "Vorkommen (EN)", "Occurrence (EN)", "string", None, True),
             col("page", "Seite", "Page", "string", None),
             col("block", "Block", "Block", "string", None),
         ],
         "rows": rows, "source_refs": [{"page": "82", "block": "b1"}]},
        {"name": "by_animal",
         "title": bi("Namen je Tier", "Names per animal"),
         "columns": [
             col("animal_de", "Tier", "Animal", "string", None, True),
             col("animal_en", "Tier (EN)", "Animal (EN)", "string", None, True),
             col("group_de", "Gruppe", "Group", "string", None, True),
             col("group_en", "Gruppe (EN)", "Group (EN)", "string", None, True),
             col("status_de", "Vorkommen heute nach Brückner", "Occurrence today according to Brückner", "string", None, True),
             col("status_en", "Vorkommen (EN)", "Occurrence (EN)", "string", None, True),
             col("names", "Zahl der Namen", "Number of names", "integer", "Namen", True),
             col("examples", "Namen im Druck", "Names as printed", "string", None),
         ],
         "rows": tab, "source_refs": [{"page": "82", "block": "b1"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "by_animal",
         "title": bi("Tiere in Flur- und Ortsnamen", "Animals in field and place names"),
         "caption": bi(f"Zahl der Namen je Tier ({n} Namen, {n_animals} Tiere; Haustiere ausgenommen). Farbig hervorgehoben sind die Tiere, die nach Brückner ausgerottet/verschwunden sind.",
                       f"Number of names per animal ({n} names, {n_animals} animals; domestic animals excluded). The animals that according to Brückner are exterminated or vanished from the country are highlighted."),
         "vegalite": {"height": 460, "mark": "bar",
                      "encoding": {
                          "y": {"field": {"de": "animal_de", "en": "animal_en"}, "type": "nominal", "sort": "-x", "title": None},
                          "x": {"field": "names", "type": "quantitative", "title": bi("Namen", "Names"), "axis": {"tickMinStep": 1}},
                          "color": {"field": {"de": "status_de", "en": "status_en"}, "type": "nominal", "title": bi("Heute im Land", "Today in the country"),
                                    "legend": {"columns": 1, "labelLimit": 300},
                                    "scale": {"domain": [{"de": "vorhanden", "en": "present"}, {"de": "ausgerottet/verschwunden", "en": "extirpated or vanished"}]}},
                          "tooltip": [{"field": {"de": "animal_de", "en": "animal_en"}, "title": bi("Tier", "Animal")},
                                      {"field": {"de": "group_de", "en": "group_en"}, "title": bi("Gruppe", "Group")},
                                      {"field": "names", "title": bi("Namen", "Names")},
                                      {"field": "examples", "title": bi("Namen", "Names")}]}}},
    ],
    "keywords": {"de": ["Flurnamen", "Ortsnamen", "Tiernamen", "Wolf", "Bär", "Luchs", "Wisent", "Hirsch", "Fauna", "Namenkunde"],
                 "en": ["field names", "place names", "animal names", "wolf", "bear", "lynx", "wisent", "deer", "fauna", "onomastics"]},
    "related": ["fauna-aenderungen-seit-1647", "wald-baumarten-flurnamen"],
    "generated_by": GEN,
    "date": DATE,
}
write(ana)
