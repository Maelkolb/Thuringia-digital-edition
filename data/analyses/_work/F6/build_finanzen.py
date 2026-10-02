from common import *
import finanzen_charts as C

IDS = ["staat-haushalt-einnahmen-ausgaben-1866-1868", "staat-schulden-kassenscheine-1857-1866",
       "versicherung-feuerversicherung-1867-orte"]
A = {i: archive(i) for i in IDS}
a_haus, a_schuld, a_vers = (A[k] for k in IDS)

# ---------------------------------------------------------------- datasets
ds_haushalt = dataset(a_haus, "structure", new_name="haushalt")
haushalt = rows(ds_haushalt)
TOTAL_REV = sum(r["thaler"] for r in haushalt if r["side_key"] == "a_einnahmen")
TOTAL_EXP = sum(r["thaler"] for r in haushalt if r["side_key"] == "b_ausgaben")
assert (TOTAL_REV, TOTAL_EXP) == (296000, 290000)
assert_in_page("276", "296,000")
assert_in_page("276", "290,000")

ds_income = dataset(a_haus, "income", add_cols=[(col("share_pct", "Anteil an den veranschlagten Einnahmen", "Share of budgeted revenue", "number", "%", True,
                                                      f"Posten : {TOTAL_REV} Taler (Gesamtvoranschlag S. 276)"),
                                                 lambda r: r["thaler"] / TOTAL_REV * 100)])
ds_debt = dataset(a_schuld, "debt")
ds_notes = dataset(a_schuld, "notes")
ds_places = dataset(a_vers, "places")

income, debt, notes, places = rows(ds_income), rows(ds_debt), rows(ds_notes), rows(ds_places)

# ---------------------------------------------------------------- numbers
ind = sum(r["thaler"] for r in income if r["group_key"] == "a_ind")
dirc = sum(r["thaler"] for r in income if r["group_key"] == "b_dir")
rest = TOTAL_REV - ind - dirc
share_ind, share_dir, share_rest = (x / TOTAL_REV * 100 for x in (ind, dirc, rest))
assert ind == 154650 and dirc == 81160 and rest == 60190
assert share_ind > 50
zoll = next(r for r in income if r["item_key"] == "zoll")
mil = next(r for r in haushalt if r["comp_key"] == "d_mil")["thaler"]
chs = next(r for r in haushalt if r["comp_key"] == "e_chs")["thaler"]
geb = next(r for r in haushalt if r["comp_key"] == "f_geb")["thaler"]
named_exp = mil + chs + geb
named_share = named_exp / TOTAL_EXP * 100
mil_share = mil / TOTAL_EXP * 100

d57 = next(r["debt_thaler"] for r in debt if r["year"] == 1857)
d66 = next(r["debt_thaler"] for r in debt if r["year"] == 1866)
debt_chg = (d66 / d57 - 1) * 100
assert_in_page("277", "320,000")
KASSENSCHEINE = 320000
head = next(r for r in notes if r["state_de"] == "Reuß j. L.")["thaler_per_head"]
rank = 1 + sum(1 for r in notes if r["thaler_per_head"] > head)
assert (head, rank, len(notes)) == (3.63, 3, 10)

bld = sum(r["buildings"] for r in places)
val = sum(r["buildings_value"] for r in places)
assert (bld, val) == (18773, 20079612)
assert_in_page("304", "18773") and assert_in_page("304", "20079612")
town = [r for r in places if r["kind_key"] == "a"]
land = [r for r in places if r["kind_key"] == "b"]
t_avg = sum(r["buildings_value"] for r in town) / sum(r["buildings"] for r in town)
l_avg = sum(r["buildings_value"] for r in land) / sum(r["buildings"] for r in land)
land_b = sum(r["buildings"] for r in land) / bld * 100
land_v = sum(r["buildings_value"] for r in land) / val * 100
town_b, town_v = 100 - land_b, 100 - land_v
top = max(places, key=lambda r: r["value_per_building"])
low = min(places, key=lambda r: r["value_per_building"])

print(dict(ind=ind, dirc=dirc, rest=rest, shares=(round(share_ind, 1), round(share_dir, 1), round(share_rest, 1)),
           zoll=(zoll["thaler"], round(zoll["share_pct"], 1)), exp=(mil, chs, geb, named_exp, round(named_share, 1), round(mil_share, 1)),
           debt=(round(d57), round(d66), round(debt_chg, 1)), head=head, rank=rank,
           ins=(bld, val, round(t_avg), round(l_avg), round(land_b, 1), round(land_v, 1)),
           top=(top["place_de"], top["value_per_building"]), low=(low["place_de"], low["value_per_building"])))

# ---------------------------------------------------------------- texts
title = {"de": "Staatshaushalt, Schulden und Versicherung", "en": "State budget, debt and insurance"}

summary = {
    "de": (f"Für die Finanzperiode 1866/68 veranschlagte der Staat Einnahmen von {de(TOTAL_REV)} und Ausgaben von {de(TOTAL_EXP)} Talern im Jahr; "
           f"{de(share_ind)} Prozent der Einnahmen kamen aus indirekten Steuern. Die verzinsliche Staatsschuld sank von 1857 bis 1866 um {de(-debt_chg)} Prozent "
           f"auf {de(d66)} Taler. Ende 1867 waren {de(bld)} Gebäude mit {de(val / 1e6, 1)} Millionen Talern gegen Feuer versichert."),
    "en": (f"For the financial period 1866/68 the state budgeted revenue of {en(TOTAL_REV)} and expenditure of {en(TOTAL_EXP)} thalers a year; "
           f"{en(share_ind)} percent of the revenue came from indirect taxes. The interest-bearing public debt fell by {en(-debt_chg)} percent from 1857 to 1866, "
           f"to {en(d66)} thalers. At the end of 1867, {en(bld)} buildings were insured against fire for {en(val / 1e6, 1)} million thalers."),
}

findings = [
    {"de": (f"Von den veranschlagten Ausgaben ({de(TOTAL_EXP)} Taler) nennt Brückner nur {de(named_share, 1)} Prozent einzeln: Militär {de(mil)}, "
            f"Chausseeunterhaltung {de(chs)}, Staatsgebäude und Wege {de(geb)} Taler."),
     "en": (f"Of the budgeted expenditure ({en(TOTAL_EXP)} thalers) Brückner itemises only {en(named_share, 1)} percent: military {en(mil)}, "
            f"road maintenance {en(chs)}, state buildings and paths {en(geb)} thalers.")},
    {"de": (f"Zur verzinslichen Schuld treten {de(KASSENSCHEINE)} Taler unverzinsliche Kassenscheine. Mit {de(head, 2)} Talern Kassenscheinen je Kopf steht Reuß j. L. "
            f"an dritter Stelle von zehn verglichenen Staaten."),
     "en": (f"In addition to the interest-bearing debt there are {en(KASSENSCHEINE)} thalers of non-interest-bearing treasury notes. At {en(head, 2)} thalers of notes per head, "
            f"Reuss (Younger Line) ranks third among ten states compared.")},
    {"de": (f"Auf dem Land standen {de(land_b)} Prozent der versicherten Gebäude, aber nur {de(land_v)} Prozent der Versicherungssumme; "
            f"in den sechs Städten {de(town_b)} und {de(town_v)} Prozent."),
     "en": (f"Rural communities held {en(land_b)} percent of the insured buildings but only {en(land_v)} percent of the insured sum; "
            f"the six towns held {en(town_b)} and {en(town_v)} percent.")},
]

n_items = len(income)
charts = [
    {"id": "c1", "dataset": "income",
     "title": {"de": f"Mehr als die Hälfte der Staatseinnahmen kam aus indirekten Steuern, ein Drittel aus Zöllen und Abgaben",
               "en": f"More than half of state revenue came from indirect taxes, a third from customs and levies"},
     "caption": {"de": f"Veranschlagte Steuereinnahmen je Jahr in Talern, Anteil an den Gesamteinnahmen von {de(TOTAL_REV)} Talern. Die genannten Steuern machen {de(share_ind + share_dir, 1)} Prozent aus; der Rest ({de(rest)} Taler) ist nicht aufgeschlüsselt. Quelle: S. 276–277.",
                 "en": f"Budgeted tax revenue per year in thalers, share of the total revenue of {en(TOTAL_REV)} thalers. The taxes named make up {en(share_ind + share_dir, 1)} percent; the rest ({en(rest)} thalers) is not itemised. Source: pp. 276–277."},
     "vegalite": C.revenue_chart(
         f"Indirekte Steuern: {de(ind)} Taler ({de(share_ind)} % der Einnahmen)", f"Indirect taxes: {en(ind)} thalers ({en(share_ind)}% of revenue)",
         f"Direkte Steuern: {de(dirc)} Taler ({de(share_dir)} %)", f"Direct taxes: {en(dirc)} thalers ({en(share_dir)}%)")},
    {"id": "c2", "dataset": "debt", "extra_datasets": ["haushalt"],
     "title": {"de": f"Die verzinsliche Staatsschuld sank von 1857 bis 1866 um {de(-debt_chg)} Prozent, lag aber über den Jahreseinnahmen",
               "en": f"The interest-bearing debt fell {en(-debt_chg)} percent from 1857 to 1866 but stayed above annual revenue"},
     "caption": {"de": f"Verzinsliche Staatsschuld in Talern, 1857 bis 1861 und 1866; für 1862 bis 1865 nennt Brückner keine Werte. Gestrichelt: veranschlagte Jahreseinnahmen 1866/68 von {de(TOTAL_REV)} Talern. Quelle: S. 276–277.",
                 "en": f"Interest-bearing public debt in thalers, 1857 to 1861 and 1866; Brückner gives no figures for 1862 to 1865. Dashed: budgeted annual revenue 1866/68 of {en(TOTAL_REV)} thalers. Source: pp. 276–277."},
     "vegalite": C.c2},
    {"id": "c3", "dataset": "places",
     "title": {"de": f"Städtische Gebäude waren im Schnitt mit {de(t_avg)} Talern gegen Feuer versichert, ländliche mit {de(l_avg)}",
               "en": f"Buildings in towns were insured against fire for {en(t_avg)} thalers on average, rural ones for {en(l_avg)}"},
     "caption": {"de": "Versicherungssumme je Gebäude (Immobiliar) Ende 1867, sechs Städte und die Landgemeinden der drei Landesteile. Strichlinien: Durchschnitt aller Städte bzw. Landgemeinden. Quelle: S. 304.",
                 "en": "Insured sum per building (immovables) at the end of 1867, six towns and the rural communities of the three districts. Dashed lines: average of all towns and of all rural communities. Source: p. 304."},
     "vegalite": C.c3},
]

method = {
    "de": ("Die Posten der Einnahmen stehen auf S. 276–277: der Gesamtvoranschlag im Text, die indirekten Steuern in einer Tabelle, die direkten in einer Kurztabelle. "
           f"Die Summe der direkten Steuern ist aus den beiden gedruckten Einzelposten gebildet ({de(dirc)}). Der Anteil eines Postens ist sein Betrag geteilt durch die veranschlagten Jahreseinnahmen von {de(TOTAL_REV)} Talern. "
           "Die Ausgaben nennt Brückner nur teilweise (Militär S. 272, Chausseen und Staatsgebäude S. 275); der Rest ist die Differenz zum Gesamtvoranschlag. "
           "Die Staatsschuld steht in Talern, Silbergroschen und Pfennigen (S. 277) und wurde mit 1 Taler = 30 Silbergroschen = 360 Pfennige in Taler umgerechnet. "
           "Die Kassenscheine je Kopf stehen im Text S. 277–278. Die Feuerversicherung stammt aus den beiden Tabellen S. 304; die Summe je Gebäude und die Durchschnitte für Städte und Landgemeinden sind berechnet."),
    "en": ("The items of revenue are on pp. 276–277: the overall budget in the text, the indirect taxes in a table, the direct taxes in a short table. "
           f"The total of the direct taxes is formed from the two printed items ({en(dirc)}). The share of an item is its amount divided by the budgeted annual revenue of {en(TOTAL_REV)} thalers. "
           "Brückner itemises expenditure only in part (military p. 272, highways and state buildings p. 275); the rest is the difference from the overall budget. "
           "The public debt is given in thalers, silver groschen and pfennigs (p. 277) and was converted with 1 thaler = 30 silver groschen = 360 pfennigs. "
           "The treasury notes per head are in the text on pp. 277–278. The fire insurance figures come from the two tables on p. 304; the sum per building and the averages for towns and rural communities are computed."),
}

caveats = [
    {"de": ("Gedruckt ist als Summe der direkten Steuern 81.100 Taler; die beiden Posten (53.600 und 27.560) ergeben 81.160. Die Differenz steht so im Original (Faksimile geprüft); hier gilt die Summe der Einzelposten. "
            "Die direkten Steuern nennt Brückner ohne Jahr (»seither«); ob sie dem Voranschlag 1866/68 entsprechen, ist offen."),
     "en": ("The printed total of the direct taxes is 81,100 thalers; the two items (53,600 and 27,560) add up to 81,160. The difference is in the original (checked against the facsimile); here the sum of the items is used. "
            "Brückner gives the direct taxes without a year (“hitherto”); whether they match the 1866/68 budget is open.")},
    {"de": ("Die Militärkosten gibt Brückner »auf die Finanzperiode 1866/68« an; hier sind sie wie die Gesamtsummen als Jahresbetrag gelesen. Bezöge sich die Zahl auf alle drei Jahre, läge ihr Anteil bei einem Drittel."),
     "en": ("Brückner gives the military costs “for the financial period 1866/68”; like the overall totals they are read here as an annual amount. If the figure covered all three years, its share would be a third.")},
    {"de": ("Für 1862 bis 1865 fehlen Werte der Staatsschuld. Das Jahr der 320.000 Taler Kassenscheine und des Staatenvergleichs nennt Brückner nicht. Die Versicherungssummen sind Versicherungswerte, keine Schätzungen des Gebäudewerts; "
            "Gera, Lobenstein, Tanna und Wurzbach sind von der magdeburger Landfeuersocietät ausgeschlossen."),
     "en": ("Values for the public debt are missing for 1862 to 1865. Brückner does not give the year of the 320,000 thalers of treasury notes or of the comparison of states. The insured sums are insurance values, not estimates of the value of the buildings; "
            "Gera, Lobenstein, Tanna and Wurzbach are excluded from the Magdeburg fire society.")},
]

a = {
    "id": "staatsfinanzen",
    "title": title,
    "category": "finance",
    "section": "t1-4-3",
    "merges": IDS,
    "sources": uniq_sources(*[A[i]["sources"] for i in IDS]),
    "summary": summary,
    "findings": findings,
    "method": method,
    "conversions": [{"from": "Thaler", "to": "Silbergroschen / Pfennige", "factor_or_formula": "1 Thaler = 30 Silbergroschen = 360 Pfennige",
                     "reference": "Brückner S. 278 (Dreißigthalerfuß seit 1857)"}],
    "caveats": caveats,
    "datasets": [ds_income, ds_debt, ds_places, ds_haushalt, ds_notes],
    "charts": charts,
    "transcription_issues": [],
    "keywords": {
        "de": ["Staatshaushalt", "Steuern", "Staatsschuld", "Kassenscheine", "Feuerversicherung", "Zölle", "Salzregie", "Reuß jüngerer Linie"],
        "en": ["state budget", "taxes", "public debt", "treasury notes", "fire insurance", "customs duties", "salt monopoly", "Reuss Younger Line"]},
    "related": ["verfassung-verwaltung", "handel-verkehr", "bergbau", "siedlung-wohnen"],
    "generated_by": GENERATED_BY.format(n=len(IDS)),
    "date": DATE,
}
for i in IDS:
    a["transcription_issues"] += A[i].get("transcription_issues", [])
if not a.get("transcription_issues"):
    a.pop("transcription_issues", None)
check_limits(a)
write_analysis(a)
