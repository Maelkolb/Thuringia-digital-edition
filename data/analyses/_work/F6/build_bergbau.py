from common import *
import bergbau_charts as C

IDS = ["bergbau-bestand-oberland-vor-1648", "bergbau-erzbergbau-zeitleiste-ober-unterland",
       "bergbau-huettenwerke-oberland-betriebszeiten", "bergbau-saline-heinrichshall-absatz-1857-1863",
       "bergbau-schieferbrueche-lobenstein-1868"]
A = {i: archive(i) for i in IDS}
a_best, a_erz, a_hue, a_sal, a_sch = (A[k] for k in IDS)

# ---------------------------------------------------------------- datasets
ds_werke = dataset(a_hue, "werke")
ds_unt = dataset(a_erz, "unternehmungen")
ds_sal = dataset(a_sal, "veraenderung")
ds_gruben = dataset(a_best, "gruben")
ds_ausbeute = dataset(a_erz, "ausbeute")

werke, unt, sal = rows(ds_werke), rows(ds_unt), rows(ds_sal)
gruben, ausb = rows(ds_gruben), rows(ds_ausbeute)

# ---------------------------------------------------------------- numbers (all prose numbers come from here)
n_gruben = sum(r["count"] for r in gruben)
n_eisen = sum(r["count"] for r in gruben if r["ore_group"] == "Eisen")
share_eisen = n_eisen / n_gruben * 100

n_werke = len(werke)
n_betrieb = sum(1 for r in werke if r["status"] == "in Betrieb")
n_umg = sum(1 for r in werke if r["fate_group"] in ("Gerberei", "Mühle/Ziegelei", "Textilfabrik"))
n_aufg = sum(1 for r in werke if r["fate_group"] == "Aufgegeben")
n_textil = sum(1 for r in werke if r["fate_group"] == "Textilfabrik")
assert n_betrieb + n_umg + n_aufg == n_werke
closed = [r for r in werke if r["end_year"]]
first_close = min(r["end_year"] for r in closed)
last_close = max(r["end_year"] for r in closed)
alive_start = sorted(r["start_year"] for r in werke if r["status"] == "in Betrieb")

ul = [r for r in unt if r["region"] == "Unterland"]
n_ul = len(ul)
early = sum(1 for r in ul if r["start_plot"] <= 1609)
gap = sum(1 for r in ul if 1610 <= r["start_plot"] <= 1687)
late = sum(1 for r in ul if r["start_plot"] >= 1688)
assert early + gap + late == n_ul
ul_last = max(r["end_plot"] for r in ul)

lost = [r for r in sal if r["ctr_1863"] is None]
lost_1857 = sum(r["ctr_1857"] for r in lost)
kochsalz = {"1857": 27527, "1863": 23898}       # printed in the running text, p. 251 b1
drop_pct = (kochsalz["1857"] - kochsalz["1863"]) / kochsalz["1857"] * 100
table_1857 = sum(r["ctr_1857"] for r in sal)
table_1863 = sum((r["ctr_1863"] or 0) for r in sal)

erz_total = sum(r["zollcentner"] for r in ausb)
erz_eisen = next(r["zollcentner"] for r in ausb if r["product"] == "Eisenerze")
erz_share = erz_eisen / erz_total * 100

NUMS = dict(n_gruben=n_gruben, n_eisen=n_eisen, share_eisen=round(share_eisen, 1), n_werke=n_werke,
            n_betrieb=n_betrieb, n_umg=n_umg, n_aufg=n_aufg, n_textil=n_textil, first_close=first_close,
            last_close=last_close, alive_start=alive_start, n_ul=n_ul, early=early, gap=gap, late=late,
            ul_last=ul_last, lost_1857=lost_1857, drop_pct=round(drop_pct, 1), table_1857=table_1857,
            table_1863=table_1863, erz_eisen=erz_eisen, erz_total=erz_total, erz_share=round(erz_share, 1))
print(NUMS)

NUM_DE = {1: "ein", 3: "drei", 4: "vier", 5: "fünf", 6: "sechs", 11: "elf"}
NUM_EN = {1: "one", 3: "three", 4: "four", 5: "five", 6: "six", 11: "eleven"}
assert (n_betrieb, n_umg, n_aufg, n_werke) == (5, 11, 6, 22)
assert (n_gruben, n_eisen) == (349, 319)

# ---------------------------------------------------------------- texts
title = {"de": "Bergbau, Hütten und Salz", "en": "Mining, ironworks and salt"}

summary = {
    "de": (f"Brückner verfolgt den Bergbau von den Silbergruben bei Schleiz (1318) bis zur Saline Heinrichshall. "
           f"Vor dem Dreißigjährigen Krieg zählte das Oberland {n_gruben} Gruben, {n_eisen} davon auf Eisen. "
           f"Von {n_werke} später verzeichneten Hammer- und Hüttenwerken liefen 1869 noch {NUM_DE[n_betrieb]}. "
           f"Im Unterland endete der Metallbergbau um 1750. Die Saline gab 1863 {de(kochsalz['1863'])} Zentner Kochsalz ab, "
           f"{de(drop_pct, 1)} Prozent weniger als 1857."),
    "en": (f"Brückner traces mining from the silver mines near Schleiz (1318) to the Heinrichshall saltworks. "
           f"Before the Thirty Years’ War the Oberland had {n_gruben} mines, {n_eisen} of them for iron. "
           f"Of {n_werke} ironworks and hammer mills recorded for later times, only {NUM_EN[n_betrieb]} were still running in 1869. "
           f"In the Unterland metal mining ended around 1750. In 1863 the saltworks delivered {en(kochsalz['1863'])} hundredweight of table salt, "
           f"{en(drop_pct, 1)} percent less than in 1857."),
}

findings = [
    {"de": (f"Vor dem Dreißigjährigen Krieg waren {n_eisen} von {n_gruben} Gruben des Oberlandes Eisengruben ({de(share_eisen)} Prozent). "
            f"1860 war Eisenerz {de(erz_share, 1)} Prozent der Förderung: {de(erz_eisen)} von {de(erz_total)} Zollzentnern, Flussspat eingerechnet."),
     "en": (f"Before the Thirty Years’ War, {n_eisen} of the {n_gruben} mines of the Oberland were iron mines ({en(share_eisen)} percent). "
            f"In 1860 iron ore was {en(erz_share, 1)} percent of the output: {en(erz_eisen)} of {en(erz_total)} customs hundredweight, fluorspar included.")},
    {"de": (f"Die {len(closed)} stillgelegten Werke endeten zwischen {first_close} und {last_close}; {NUM_DE[n_textil]} wurden Textilbetriebe. "
            f"Die {NUM_DE[n_betrieb]} noch laufenden Werke gehen auf Jahre zwischen {alive_start[0]} und {alive_start[-1]} zurück."),
     "en": (f"The {len(closed)} closed works ended between {first_close} and {last_close}; {NUM_EN[n_textil]} became textile mills. "
            f"The {NUM_EN[n_betrieb]} works still running date back to years between {alive_start[0]} and {alive_start[-1]}.")},
    {"de": (f"Der Salzabsatz sank 1863 gegenüber 1857, weil Greiz, Möschlitz und Zeulenroda nichts mehr erhielten (im Druck ein Strich). "
            f"Sie hatten 1857 zusammen {de(lost_1857)} Zentner bezogen."),
     "en": (f"Salt sales fell in 1863 compared with 1857 because Greiz, Möschlitz and Zeulenroda received none (a dash in the print). "
            f"In 1857 they had taken {en(lost_1857)} hundredweight between them.")},
]

charts = [
    {"id": "c1", "dataset": "werke",
     "title": {"de": f"Von {n_werke} Hüttenwerken des Oberlandes liefen 1869 noch {NUM_DE[n_betrieb]}; {NUM_DE[n_umg]} wurden umgenutzt, {NUM_DE[n_aufg]} aufgegeben",
               "en": f"Of {n_werke} Oberland ironworks, {NUM_EN[n_betrieb]} still ran in 1869; {NUM_EN[n_umg]} were converted, {NUM_EN[n_aufg]} abandoned"},
     "caption": {"de": "Betriebszeit der Hütten- und Hammerwerke des Oberlandes seit 1648, nach ihrem Schicksal gruppiert (blau: noch in Betrieb, orange: umgenutzt, grau: aufgegeben). Quelle: S. 244–246.",
                 "en": "Operating period of the ironworks and hammer mills of the Oberland since 1648, grouped by their fate (blue: still running, orange: converted, grey: abandoned). Source: pp. 244–246."},
     "vegalite": C.c1},
    {"id": "c2", "dataset": "unternehmungen",
     "title": {"de": f"Im Unterland sind Gruben und Hütten fast nur vor 1610 und nach 1687 belegt",
               "en": f"In the Unterland mines and smelters are documented almost only before 1610 and after 1687"},
     "caption": {"de": f"Gruben, Hütten und Werke des Unterlandes mit Jahreszahl, je Ort; Balken: Zeitraum, Punkt: einzelnes Jahr (Mutung, Verleihung, Erwähnung). {n_ul} Belege, davon nur {gap} zwischen 1610 und 1687. Quelle: S. 249–250.",
                 "en": f"Mines, smelters and works of the Unterland with a date, by place; bar: period, dot: single year (claim, grant, mention). {n_ul} records, only {gap} of them between 1610 and 1687. Source: pp. 249–250."},
     "vegalite": C.c2},
    {"id": "c3", "dataset": "veraenderung",
     "title": {"de": "Der Salzabsatz sank 1863, weil Greiz, Möschlitz und Zeulenroda nichts mehr erhielten",
               "en": "Salt sales fell in 1863 because Greiz, Möschlitz and Zeulenroda received none"},
     "caption": {"de": "Kochsalz, das die Saline Heinrichshall 1857 und 1863 an ihre 20 Verkaufsstellen (Debitstellen) abgab, in Zentnern. Sortiert nach der Menge von 1857. Quelle: S. 251.",
                 "en": "Table salt that the Heinrichshall saltworks delivered to its 20 sales outlets (Debitstellen) in 1857 and 1863, in hundredweight. Sorted by the 1857 quantity. Source: p. 251."},
     "vegalite": C.c3},
]

method = {
    "de": ("Die Zahlen stammen aus Brückners Abschnitt Bergbau (S. 242–251). Die Gruben vor dem Dreißigjährigen Krieg zählt die Tabelle S. 243, "
           "die Hüttenwerke S. 244. Für die Betriebszeiten der Hütten- und Hammerwerke seit 1648 wurden die Jahreszahlen der Absätze S. 245–246 übernommen: "
           "Beginn ist das Jahr der Gründung, Erneuerung oder Wiederinbetriebnahme, Ende das der Stilllegung. Werke, die der Text als noch bestehend nennt, "
           "laufen im ersten Diagramm bis 1870. Das spätere Schicksal (Textilfabrik, Mühle, Ziegelei, Gerberei, aufgegeben) ist aus dem Wortlaut gruppiert. "
           "Das zweite Diagramm zeigt alle Gruben, Hütten und Werke des Unterlandes, für die Brückner ein Jahr oder einen Zeitraum nennt; die Orte sind nach dem frühesten Beleg sortiert. "
           "Beim dritten Diagramm wurde die Tabelle der Debitstellen (S. 251) Ort für Ort übernommen; ein Strich im Druck gilt als keine Lieferung. "
           "Die Gesamtmengen für 1857 und 1863 stehen im Text derselben Seite. Maßeinheit ist der Zentner (Zollzentner) zu 100 Zollpfund, also 50 kg."),
    "en": ("The figures come from Brückner’s section on mining (pp. 242–251). The mines before the Thirty Years’ War are counted in the table on p. 243, "
           "the smelting works on p. 244. For the operating periods of the ironworks and hammer mills since 1648 the dates in the paragraphs on pp. 245–246 were taken over: "
           "the start is the year of founding, renewal or reopening, the end that of closure. Works that the text calls still extant run to 1870 in the first chart. "
           "Their later fate (textile mill, mill, brickworks, tannery, abandoned) is grouped from the wording. "
           "The second chart shows all mines, smelters and works of the Unterland for which Brückner gives a year or a period; places are sorted by their earliest record. "
           "For the third chart the table of sales outlets (p. 251) was transcribed place by place; a dash in the print is read as no delivery. "
           "The totals for 1857 and 1863 are in the text of the same page. The unit is the hundredweight (Zollzentner) of 100 customs pounds, that is 50 kg."),
}

caveats = [
    {"de": ("Die Jahre der Hütten- und Hammerwerke stammen aus Brückners Aufzählung; einige Daten sind ungefähr. Aufgenommen sind nur Werke, die er als später eingegangen oder noch bestehend nennt. "
            f"Brückner datiert den Niedergang des oberländischen Hüttenwesens auf 1858; alle {len(closed)} Stilllegungen der Liste liegen früher."),
     "en": ("The years for the ironworks and hammer mills come from Brückner’s list; some dates are approximate. Only works that he names as closed later or still extant are included. "
            f"Brückner dates the decline of the Oberland ironworks to 1858; all {len(closed)} closures in the list are earlier.")},
    {"de": ("Ein Punkt im zweiten Diagramm kann Mutung (Antrag auf Bergbaurecht), Verleihung, Inbetriebnahme oder bloße Erwähnung bedeuten und belegt nicht, dass die Grube in dem Jahr förderte. "
            "Der Eisenerzbergbau des Oberlandes, nach Brückner der Hauptzweig, ist ohne Jahresangaben beschrieben und daher nicht dargestellt."),
     "en": ("A dot in the second chart can mean a claim, a grant, the start of work or a mere mention, and does not show that the mine was producing in that year. "
            "Iron-ore mining in the Oberland, according to Brückner the main branch, is described without dates and is therefore not shown.")},
    {"de": (f"Die Tabelle der Debitstellen ergibt addiert {de(table_1857)} (1857) und {de(table_1863)} Zentner (1863); im Text nennt Brückner {de(kochsalz['1857'])} und {de(kochsalz['1863'])}. "
            "Die Transkription stimmt mit dem Druck überein (Faksimile geprüft). Was der Strich für 1863 bedeutet, sagt Brückner nicht."),
     "en": (f"The table of sales outlets adds up to {en(table_1857)} (1857) and {en(table_1863)} hundredweight (1863); in the text Brückner gives {en(kochsalz['1857'])} and {en(kochsalz['1863'])}. "
            "The transcription agrees with the print (checked against the facsimile). Brückner does not say what the dash for 1863 means.")},
    {"de": ("Die Zahl der Gruben vor dem Dreißigjährigen Krieg beruht auf Brückners Zusammenstellung aus den Akten; ein Stichjahr nennt er nicht, und ob alle Gruben gleichzeitig bestanden, bleibt offen."),
     "en": ("The number of mines before the Thirty Years’ War rests on Brückner’s compilation from the records; he gives no reference year, and whether all mines existed at the same time remains open.")},
]

a = {
    "id": "bergbau",
    "title": title,
    "category": "mining",
    "section": "t1-3-5",
    "merges": IDS,
    "sources": uniq_sources(*[A[i]["sources"] for i in IDS]),
    "summary": summary,
    "findings": findings,
    "method": method,
    "conversions": [{"from": "Zollcentner", "to": "kg", "factor_or_formula": "1 Zollcentner = 100 Zollpfund = 50 kg",
                     "reference": "1 Zollpfund = 0,5 kg (S. 832)"}],
    "caveats": caveats,
    "datasets": [ds_werke, ds_unt, ds_sal, ds_gruben, ds_ausbeute],
    "charts": charts,
    "keywords": {
        "de": ["Bergbau", "Eisenerz", "Hammerwerke", "Hüttenwerke", "Saline Heinrichshall", "Kochsalz", "Kupfer", "Trebnitz", "Köstritz", "Alaun", "Oberland", "Unterland"],
        "en": ["mining", "iron ore", "hammer mills", "smelting works", "Heinrichshall saltworks", "table salt", "copper", "Trebnitz", "Köstritz", "alum", "Oberland", "Unterland"]},
    "related": ["geologie-boden", "berufe-gewerbe", "wald-holz", "staatsfinanzen"],
    "generated_by": GENERATED_BY.format(n=len(IDS)),
    "date": DATE,
}
check_limits(a)
write_analysis(a)
