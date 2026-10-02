"""A09 / analysis 10: Holzpreise 1800-1868, Normalklafter-Preise und Zuwachs (p. 241)."""
import sys, re
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent))
from a09common import *

# ---------------------------------------------------------------- price series (b6)
g6 = grid("241", "b6")
SORT = [("Bauholz", "Construction timber", 1), ("Blochholz", "Log timber (Blochholz)", 2), ("Feuerholz", "Firewood", 3)]
holz = []
for ri in range(1, 5):
    r = g6[ri]
    jahr = int(r[0])
    for ci, (de, en, nn_) in enumerate(SORT):
        txt = r[1 + ci].replace("Sgr.,", "").replace('"', "").strip().rstrip(",")
        if "-" in txt:
            a, b = [num(x.strip()) for x in txt.split("-")]
        else:
            a = b = num(txt)
        holz.append([de, en, nn_, jahr, re.sub(r"\s+", " ", (r[1 + ci])).strip(), round(a, 3), round(b, 3), round((a + b) / 2, 3)])
print(holz)
hp = {(r[0], r[3]): r for r in holz}

# ---------------------------------------------------------------- Normalklafter prices (b4)
g4 = grid("241", "b4")
KL = []
for ri, (de, en) in enumerate((("Nutzholz", "Timber for construction and trade"), ("Brennholz", "Firewood"), ("Stock- und Wurzelholz", "Stumps and roots")), start=1):
    r = g4[ri]
    lo = num(r[1].replace("Thaler,", "").replace('"', "").strip().rstrip(","))
    hi = num(r[2].replace("Thaler.", "").replace('"', "").strip().rstrip("."))
    KL.append([de, en, ri, lo, hi, round(lo * 30 / 126, 2), round(hi * 30 / 126, 2)])
print(KL)

# ---------------------------------------------------------------- Zuwachs (b3 text)
b3 = block("241", "b3")["text"]
assert "bei den Domainenforsten auf 1/2, bei den Gemeinde- und Stiftungswäldern auf 2/5 bis 1/2, bei den Privatwäldern indeß nur auf 1/10 bis 1/5 Klaster" in b3
assert "Ertrag von 40 Cubikfuß" in b3
b8 = block("241", "b8")["text"]
assert "20 Cubikfuß" in b8
KLAFTER_M3 = 2.8454   # Brückner S. 832: Klafter 126 Kubikfuß = 2,8454 m3 (Landestheil Gera)
ZW = [("Domänenforsten", "Domain forests", 1, 1 / 2, 1 / 2, 40, "1/2"),
      ("Gemeinde- und Stiftungswälder", "Municipal and foundation forests", 2, 2 / 5, 1 / 2, 40, "2/5 bis 1/2"),
      ("Privatwälder", "Private woodland", 3, 1 / 10, 1 / 5, 20, "1/10 bis 1/5")]
zuw = []
for de, en, nr, lo, hi, ertrag, txt in ZW:
    zuw.append([de, en, nr, txt, round(lo, 3), round(hi, 3), round(lo * KLAFTER_M3 / MORGEN_HA, 2), round(hi * KLAFTER_M3 / MORGEN_HA, 2), ertrag])
print(zuw)

# ---------------------------------------------------------------- numbers for the text
fac = {s[0]: hp[(s[0], 1868)][7] / hp[(s[0], 1800)][7] for s in SORT}
print(fac)
_r1, _r2 = KL[0][4] / KL[1][4], KL[0][3] / KL[1][3]
ratio_nutz_brenn_hi, ratio_nutz_brenn_lo = max(_r1, _r2), min(_r1, _r2)
bau40 = hp[("Bauholz", 1840)]
bau68 = hp[("Bauholz", 1868)]
feu40 = hp[("Feuerholz", 1840)]
feu20 = hp[("Feuerholz", 1820)]
zw_dom = zuw[0][7]
zw_priv = (zuw[2][6], zuw[2][7])
print(bau40, bau68, feu40, feu20, zw_dom, zw_priv)
priv_vs_dom_lo = 100 * zuw[2][4] / zuw[0][4]
priv_vs_dom_hi = 100 * zuw[2][5] / zuw[0][5]
print(priv_vs_dom_lo, priv_vs_dom_hi)

R_P = {"page": "241", "block": "b6", "rows": "r2-r5"}
R_K = {"page": "241", "block": "b4", "rows": "r3-r5"}
R_Z = [{"page": "241", "block": "b3"}, {"page": "241", "block": "b8"}]
R_TXT = [{"page": "241", "block": "b5"}, {"page": "241", "block": "b7"}]


def col(name, de, en, typ, unit=None, derived=False, note=None):
    d = {"name": name, "label": bi(de, en), "type": typ, "unit": unit}
    if derived:
        d["derived"] = True
    if note:
        d["note"] = note
    return d


FR = "gedruckt als gemischter Bruch (z. B. 1 1/6), hier als Dezimalzahl"
ana = {
    "id": "forstwirtschaft-holzpreise-zuwachs",
    "title": bi("Holzpreise 1800–1868 und Zuwachs der Wälder", "Timber prices 1800–1868 and growth of the forests"),
    "category": "forestry",
    "section": "t1-3-4",
    "sources": R_TXT + [R_P, R_K] + R_Z + [{"page": "832", "block": "b8"}],
    "summary": bi(
        "Am Ende des Abschnitts Forstwirthschaft nennt Brückner die Entwicklung der Holzpreise seit 1800 (Bauholz, Blochholz, Feuerholz je Cubikfuß), die in den letzten Jahren erzielten Preise für Domanialholz im Oberland (je Normalklafter) und Schätzungen für Zuwachs und Ertrag je Morgen nach Besitzart. Die Diagramme zeigen den Preisanstieg, die Preisspannen der Sortimente und den Zuwachs der Domänen-, Gemeinde- und Privatwälder.",
        "At the end of the section on forestry Brückner gives the development of timber prices since 1800 (construction timber, log timber, firewood per cubic foot), the prices obtained for domain timber in the Upper Land in recent years (per standard cord), and estimates of growth and yield per Morgen by type of owner. The charts show the price rise, the price ranges of the assortments, and the growth of the domain, municipal and private forests."),
    "method": bi(
        "Die Preise je Cubikfuß weiches Holz stammen aus der Tabelle auf S. 241 (Block b6), die Preise je Normalklafter aus Block b4, Zuwachs und Ertrag aus dem Absatz Block b3 bzw. b8. Brückner schreibt die Preise in Silbergroschen (Sgr.) und gemischten Brüchen (z. B. »1 1/6«); sie sind als Dezimalzahlen übernommen (der gedruckte Wortlaut steht in der Spalte preis_text). Für 1840 gibt er Spannen an; Diagramm 1 zeigt dann Spanne und Mitte. Die Preise je Normalklafter (= 126 Cubikfuß Rauminhalt) wurden mit 1 Thaler = 30 Silbergroschen in Silbergroschen je Cubikfuß umgerechnet (Währungsfaktor des preußischen Münzsystems, nicht aus Brückners Tabelle). Der Zuwachs je Morgen ist in Klaftern angegeben; er wurde mit Brückners Klafter von 126 Kubikfuß = 2,8454 m³ (S. 832, Landestheil Gera) und 1 Morgen = 0,255322 ha (S. 832) in Raummeter je Hektar und Jahr umgerechnet.",
        "The prices per cubic foot of soft wood come from the table on p. 241 (block b6), the prices per standard cord from block b4, growth and yield from the paragraph in blocks b3 and b8. Brückner writes the prices in silver groschen (Sgr.) and mixed fractions (e.g. “1 1/6”); they were taken over as decimals (the printed wording is in the column preis_text). For 1840 he gives ranges; chart 1 then shows range and midpoint. The prices per standard cord (Normalklafter = 126 cubic feet of volume) were converted to silver groschen per cubic foot with 1 Thaler = 30 silver groschen (conversion factor of the Prussian monetary system, not from Brückner's table). Growth per Morgen is given in cords; it was converted with Brückner's cord of 126 cubic feet = 2.8454 m³ (p. 832, district of Gera) and 1 Morgen = 0.255322 ha (p. 832) into stacked cubic metres per hectare and year."),
    "findings": [
        bi(f"Von 1800 bis 1868 steigt der Preis je Cubikfuß für Bauholz von 1 1/6 auf 3 Sgr. (das {de_num(fac['Bauholz'],1)}-Fache), für Blochholz von 1 1/4 auf 3 1/2 Sgr. ({de_num(fac['Blochholz'],1)}-Fache) und für Feuerholz von 1/3 auf 1 Sgr. ({de_num(fac['Feuerholz'],1)}-Fache). Brückner fasst dies als Verdreifachung seit 1800 zusammen.",
           f"From 1800 to 1868 the price per cubic foot rises for construction timber from 1 1/6 to 3 Sgr. ({en_num(fac['Bauholz'],1)} times), for log timber from 1 1/4 to 3 1/2 Sgr. ({en_num(fac['Blochholz'],1)} times) and for firewood from 1/3 to 1 Sgr. ({en_num(fac['Feuerholz'],1)} times). Brückner summarizes this as a tripling since 1800."),
        bi(f"Feuerholz verteuert sich vor allem bis 1840 (von 1/3 über 5/12 auf 1 Sgr.) und bleibt bis 1868 bei 1 Sgr.; Bau- und Blochholz steigen auch danach weiter (Bauholz von {de_num(bau40[5],2)}–{de_num(bau40[6],2)} Sgr. 1840 auf 3 Sgr. 1868).",
           f"Firewood becomes dearer above all until 1840 (from 1/3 through 5/12 to 1 Sgr.) and stays at 1 Sgr. until 1868; construction and log timber continue to rise afterwards (construction timber from {en_num(bau40[5],2)}–{en_num(bau40[6],2)} Sgr. in 1840 to 3 Sgr. in 1868)."),
        bi(f"Für das Domanialholz des Oberlandes nennt Brückner in den letzten Jahren je Normalklafter 6–15 Thaler für Nutzholz, 2–6 für Brennholz und 2–5 für Stock- und Wurzelholz; umgerechnet sind das {de_num(KL[0][5],2)}–{de_num(KL[0][6],2)} Sgr. je Cubikfuß für Nutzholz und {de_num(KL[1][5],2)}–{de_num(KL[1][6],2)} Sgr. für Brennholz. Nutzholz kostet damit das {de_num(ratio_nutz_brenn_lo,1)}- bis {de_num(ratio_nutz_brenn_hi,1)}-Fache von Brennholz.",
           f"For the domain timber of the Upper Land Brückner gives, per standard cord, 6–15 Thaler for timber, 2–6 for firewood and 2–5 for stumps and roots in recent years; converted this is {en_num(KL[0][5],2)}–{en_num(KL[0][6],2)} Sgr. per cubic foot for timber and {en_num(KL[1][5],2)}–{en_num(KL[1][6],2)} Sgr. for firewood. Timber thus costs {en_num(ratio_nutz_brenn_lo,1)} to {en_num(ratio_nutz_brenn_hi,1)} times as much as firewood."),
        bi(f"Den jährlichen Zuwachs veranschlagt Brückner je Morgen für die Domänenforsten auf 1/2 Klafter (rund {de_num(zw_dom,1)} Raummeter je Hektar), für Gemeinde- und Stiftungswälder auf 2/5 bis 1/2 und für Privatwälder nur auf 1/10 bis 1/5 Klafter ({de_num(zw_priv[0],1)}–{de_num(zw_priv[1],1)} Raummeter je Hektar); der Privatwald wächst demnach nur mit {de_num(priv_vs_dom_lo,0)}–{de_num(priv_vs_dom_hi,0)} % der Domänenleistung.",
           f"Brückner estimates the annual growth per Morgen at 1/2 cord for the domain forests (about {en_num(zw_dom,1)} stacked cubic metres per hectare), at 2/5 to 1/2 for municipal and foundation forests and at only 1/10 to 1/5 cord for private woodland ({en_num(zw_priv[0],1)}–{en_num(zw_priv[1],1)} stacked cubic metres per hectare); private woodland thus grows at only {en_num(priv_vs_dom_lo,0)}–{en_num(priv_vs_dom_hi,0)} % of the domain rate."),
        bi("Der Nettoertrag des gesamten Frankenwaldes betrug 1647 etwa 1730 Thaler, nach Brückner »um mehr als 20 Mal geringer« als der heutige Nettoabwurf; im Durchschnitt wird der Ertrag der Domänen-, Gemeinde- und Stiftungswälder mit 40, der der meisten Privatwälder mit höchstens 20 Cubikfuß je Jahr angesetzt.",
           "The net yield of the whole Frankenwald in 1647 was about 1,730 Thaler, according to Brückner “more than 20 times lower” than today's net proceeds; on average the yield of the domain, municipal and foundation forests is put at 40 cubic feet a year, that of most private woodland at 20 at most."),
    ],
    "caveats": [
        bi("Die Preisreihe hat nur vier Zeitpunkte (1800, 1820, 1840, 1868); Verlauf und Schwankungen zwischen diesen Jahren sind nicht belegt. Welches Holz (Maß, Herkunft) die Tabelle meint, sagt Brückner nur mit »weiches Holz« – Nadelholz – und »Cubikfuß«; ob Fest- oder Raummaß, bleibt offen.",
           "The price series has only four points in time (1800, 1820, 1840, 1868); development and fluctuations between these years are not documented. Brückner describes the wood only as “soft wood” – conifer – and “cubic foot”; whether this is solid or stacked measure remains open."),
        bi("Die Ertragszahlen (40 bzw. 20 Cubikfuß, dazu »27,469« und »9157« Normalklafter für Oberholz und Stockholz) sind in der Vorlage nicht eindeutig auf die Fläche bezogen und passen nicht zu den Klafter-Zuwächsen; sie werden deshalb nur zitiert, nicht umgerechnet. Der Zuwachs in Raummetern ist eine Näherung mit der geraer Klafter von 126 Kubikfuß (2,8454 m³).",
           "The yield figures (40 and 20 cubic feet, plus “27,469” and “9157” standard cords for timber and stump wood) are not clearly related to the area in the source and do not fit the growth figures in cords; they are therefore only quoted, not converted. The growth in cubic metres is an approximation with the Gera cord of 126 cubic feet (2.8454 m³)."),
        bi("Die Preise je Normalklafter gelten für Domanialholz im Oberland »in den letzten Jahren« (ohne Jahresangabe); die Umrechnung auf Silbergroschen je Cubikfuß setzt die Normalklafter von 126 Cubikfuß Rauminhalt und 1 Thaler = 30 Silbergroschen voraus.",
           "The prices per standard cord apply to domain timber in the Upper Land “in recent years” (no year given); the conversion to silver groschen per cubic foot presupposes the standard cord of 126 cubic feet of volume and 1 Thaler = 30 silver groschen."),
    ],
    "conversions": [
        {"from": "Normalklafter", "to": "Kubikfuß", "factor_or_formula": "1 Normalklafter = 126 Cubikfuß Rauminhalt", "reference": "Brückner S. 241"},
        {"from": "Thaler", "to": "Silbergroschen", "factor_or_formula": "1 Thaler = 30 Silbergroschen", "reference": "preußisches Münzsystem; nicht in Brückners Tabelle"},
        {"from": "Klafter (126 Kubikfuß, Gera)", "to": "Kubikmeter", "factor_or_formula": "1 Klafter = 2,8454 m³", "reference": "Brückner S. 832, V. Holzmaße a)"},
        {"from": "preußischer Morgen", "to": "Hektar", "factor_or_formula": "ha = Morgen × 0,255322", "reference": "Brückner S. 832"},
    ],
    "datasets": [
        {"name": "holzpreise", "title": bi("Preis je Cubikfuß weiches Holz", "Price per cubic foot of soft wood"),
         "columns": [
             col("holzart_de", "Sortiment", "Assortment", "string"),
             col("holzart_en", "Sortiment (englisch)", "Assortment (English)", "string"),
             col("holzart_nr", "Reihenfolge Sortiment", "Assortment order", "integer", derived=True),
             col("jahr", "Jahr", "Year", "integer"),
             col("preis_text", "Preis (gedruckt)", "Price (as printed)", "string"),
             col("preis_von", "Preis, Untergrenze", "Price, lower limit", "number", "Sgr. je Cubikfuß", derived=True, note=FR),
             col("preis_bis", "Preis, Obergrenze", "Price, upper limit", "number", "Sgr. je Cubikfuß", derived=True, note=FR),
             col("preis_mitte", "Preis, Mitte der Spanne", "Price, midpoint of the range", "number", "Sgr. je Cubikfuß", derived=True),
         ],
         "rows": holz, "source_refs": [R_P]},
        {"name": "normalklafter", "title": bi("Preis je Normalklafter Domanialholz (Oberland)", "Price per standard cord of domain timber (Upper Land)"),
         "columns": [
             col("sorte_de", "Sortiment", "Assortment", "string"),
             col("sorte_en", "Sortiment (englisch)", "Assortment (English)", "string"),
             col("sorte_nr", "Reihenfolge", "Order", "integer", derived=True),
             col("min_thlr", "niedrigster Preis", "Lowest price", "integer", "Thaler je Normalklafter"),
             col("max_thlr", "höchster Preis", "Highest price", "integer", "Thaler je Normalklafter"),
             col("min_sgr_cf", "niedrigster Preis je Cubikfuß", "Lowest price per cubic foot", "number", "Sgr. je Cubikfuß", derived=True, note="Thaler × 30 / 126"),
             col("max_sgr_cf", "höchster Preis je Cubikfuß", "Highest price per cubic foot", "number", "Sgr. je Cubikfuß", derived=True, note="Thaler × 30 / 126"),
         ],
         "rows": KL, "source_refs": [R_K]},
        {"name": "zuwachs", "title": bi("Zuwachs je Morgen nach Besitzart", "Growth per Morgen by type of owner"),
         "columns": [
             col("besitzart_de", "Besitzart", "Type of owner", "string"),
             col("besitzart_en", "Besitzart (englisch)", "Type of owner (English)", "string"),
             col("besitzart_nr", "Reihenfolge", "Order", "integer", derived=True),
             col("zuwachs_text", "Zuwachs (gedruckt)", "Growth (as printed)", "string"),
             col("zuwachs_von", "Zuwachs, Untergrenze", "Growth, lower limit", "number", "Klafter je Morgen und Jahr", derived=True, note="gedruckte Brüche als Dezimalzahl"),
             col("zuwachs_bis", "Zuwachs, Obergrenze", "Growth, upper limit", "number", "Klafter je Morgen und Jahr", derived=True, note="gedruckte Brüche als Dezimalzahl"),
             col("rm_ha_von", "Zuwachs, Untergrenze", "Growth, lower limit", "number", "Raummeter je ha und Jahr", derived=True, note="Klafter × 2,8454 m³ / 0,255322 ha"),
             col("rm_ha_bis", "Zuwachs, Obergrenze", "Growth, upper limit", "number", "Raummeter je ha und Jahr", derived=True, note="Klafter × 2,8454 m³ / 0,255322 ha"),
             col("ertrag_cf", "Ertrag im Durchschnitt", "Average yield", "integer", "Cubikfuß je Jahr"),
         ],
         "rows": zuw, "source_refs": R_Z},
    ],
    "charts": [
        {"id": "c1", "dataset": "holzpreise",
         "title": bi("Preis je Cubikfuß weiches Holz 1800–1868", "Price per cubic foot of soft wood, 1800–1868"),
         "caption": bi("Silbergroschen je Cubikfuß. Für 1840 nennt Brückner Spannen (senkrechte Linien), sonst Einzelwerte. Alle drei Sortimente sind 1868 deutlich teurer als 1800.",
                       "Silver groschen per cubic foot. For 1840 Brückner gives ranges (vertical lines), otherwise single values. All three assortments are markedly dearer in 1868 than in 1800."),
         "vegalite": {
             "height": 300,
             "layer": [
                 {"mark": {"type": "line", "point": True},
                  "encoding": {"x": {"field": "jahr", "type": "quantitative", "title": bi("Jahr", "Year"), "axis": {"format": "d", "values": [1800, 1820, 1840, 1868]}, "scale": {"domain": [1795, 1873]}},
                               "y": {"field": "preis_mitte", "type": "quantitative", "title": bi("Silbergroschen je Cubikfuß", "Silver groschen per cubic foot"), "scale": {"zero": True}},
                               "color": {"field": {"de": "holzart_de", "en": "holzart_en"}, "type": "nominal", "title": None, "scale": {"domain": [bi(s[0], s[1]) for s in SORT]}},
                               "tooltip": [{"field": {"de": "holzart_de", "en": "holzart_en"}, "title": bi("Sortiment", "Assortment")}, {"field": "jahr", "title": bi("Jahr", "Year"), "format": "d"},
                                           {"field": "preis_text", "title": bi("gedruckt", "as printed")}, {"field": "preis_mitte", "title": bi("Mitte, Sgr.", "midpoint, Sgr."), "format": ".2f"}]}},
                 {"transform": [{"filter": "datum.preis_bis > datum.preis_von"}],
                  "mark": {"type": "rule", "strokeWidth": 3, "opacity": 0.6},
                  "encoding": {"x": {"field": "jahr", "type": "quantitative"}, "y": {"field": "preis_von", "type": "quantitative"}, "y2": {"field": "preis_bis"},
                               "color": {"field": {"de": "holzart_de", "en": "holzart_en"}, "type": "nominal", "title": None, "scale": {"domain": [bi(s[0], s[1]) for s in SORT]}}}}]}},
        {"id": "c2", "dataset": "normalklafter",
         "title": bi("Preise für Domanialholz im Oberland (je Normalklafter)", "Prices of domain timber in the Upper Land (per standard cord)"),
         "caption": bi("Niedrigster und höchster Preis in Thalern je Normalklafter (126 Cubikfuß) in den letzten Jahren vor 1870. Umgerechnet liegt Nutzholz bei 1,4–3,6 Sgr. je Cubikfuß, im Einklang mit den 3 Sgr. für Bauholz 1868.",
                       "Lowest and highest price in Thaler per standard cord (126 cubic feet) in the last years before 1870. Converted, timber lies at 1.4–3.6 Sgr. per cubic foot, in line with the 3 Sgr. for construction timber in 1868."),
         "vegalite": {
             "height": 200,
             "layer": [
                 {"mark": {"type": "bar", "size": 8, "opacity": 1},
                  "encoding": {"y": {"field": {"de": "sorte_de", "en": "sorte_en"}, "type": "nominal", "sort": {"field": "sorte_nr", "op": "min"}, "title": None, "axis": {"labelLimit": 300}},
                               "x": {"field": "min_thlr", "type": "quantitative", "title": bi("Thaler je Normalklafter", "Thaler per standard cord"), "scale": {"zero": True}}, "x2": {"field": "max_thlr"}}},
                 {"mark": {"type": "point", "filled": True, "size": 90, "opacity": 1},
                  "encoding": {"y": {"field": {"de": "sorte_de", "en": "sorte_en"}, "type": "nominal", "sort": {"field": "sorte_nr", "op": "min"}},
                               "x": {"field": "min_thlr", "type": "quantitative"}}},
                 {"mark": {"type": "point", "filled": True, "size": 90, "opacity": 1},
                  "encoding": {"y": {"field": {"de": "sorte_de", "en": "sorte_en"}, "type": "nominal", "sort": {"field": "sorte_nr", "op": "min"}},
                               "x": {"field": "max_thlr", "type": "quantitative"},
                               "tooltip": [{"field": {"de": "sorte_de", "en": "sorte_en"}, "title": bi("Sortiment", "Assortment")},
                                           {"field": "min_thlr", "title": bi("von, Thaler", "from, Thaler")}, {"field": "max_thlr", "title": bi("bis, Thaler", "to, Thaler")},
                                           {"field": "min_sgr_cf", "title": bi("von, Sgr. je Cubikfuß", "from, Sgr. per cubic foot"), "format": ".2f"},
                                           {"field": "max_sgr_cf", "title": bi("bis, Sgr. je Cubikfuß", "to, Sgr. per cubic foot"), "format": ".2f"}]}}]}},
        {"id": "c3", "dataset": "zuwachs",
         "title": bi("Jährlicher Zuwachs nach Besitzart", "Annual growth by type of owner"),
         "caption": bi("Von Brückner veranschlagter Zuwachs in Klaftern je Morgen und Jahr, umgerechnet in Raummeter je Hektar (Tooltip). Der Privatwald wächst deutlich langsamer als der Staats- und Gemeindewald.",
                       "Growth per Morgen and year estimated by Brückner in cords, converted to stacked cubic metres per hectare (tooltip). Private woodland grows markedly more slowly than state and municipal forest."),
         "vegalite": {
             "height": 200,
             "layer": [
                 {"mark": {"type": "bar", "size": 8, "opacity": 1},
                  "encoding": {"y": {"field": {"de": "besitzart_de", "en": "besitzart_en"}, "type": "nominal", "sort": {"field": "besitzart_nr", "op": "min"}, "title": None, "axis": {"labelLimit": 300}},
                               "x": {"field": "zuwachs_von", "type": "quantitative", "title": bi("Klafter je Morgen und Jahr", "Cords per Morgen and year"), "scale": {"zero": True}}, "x2": {"field": "zuwachs_bis"}}},
                 {"mark": {"type": "point", "filled": True, "size": 90, "opacity": 1},
                  "encoding": {"y": {"field": {"de": "besitzart_de", "en": "besitzart_en"}, "type": "nominal", "sort": {"field": "besitzart_nr", "op": "min"}},
                               "x": {"field": "zuwachs_von", "type": "quantitative"}}},
                 {"mark": {"type": "point", "filled": True, "size": 90, "opacity": 1},
                  "encoding": {"y": {"field": {"de": "besitzart_de", "en": "besitzart_en"}, "type": "nominal", "sort": {"field": "besitzart_nr", "op": "min"}},
                               "x": {"field": "zuwachs_bis", "type": "quantitative"},
                               "tooltip": [{"field": {"de": "besitzart_de", "en": "besitzart_en"}, "title": bi("Besitzart", "Type of owner")},
                                           {"field": "zuwachs_text", "title": bi("Zuwachs (gedruckt, Klafter)", "Growth (printed, cords)")},
                                           {"field": "rm_ha_von", "title": bi("von, Raummeter je ha", "from, stacked m³ per ha"), "format": ".1f"},
                                           {"field": "rm_ha_bis", "title": bi("bis, Raummeter je ha", "to, stacked m³ per ha"), "format": ".1f"},
                                           {"field": "ertrag_cf", "title": bi("Ertrag, Cubikfuß", "yield, cubic feet")}]}}]}},
    ],
    "keywords": {
        "de": ["Holzpreise", "Bauholz", "Blochholz", "Feuerholz", "Brennholz", "Normalklafter", "Zuwachs", "Ertrag", "Forstwirtschaft", "Frankenwald", "Preisentwicklung"],
        "en": ["timber prices", "construction timber", "firewood", "standard cord", "growth", "yield", "forestry", "Frankenwald", "price development"],
    },
    "related": ["forstwirtschaft-waldflaeche-besitz"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(ana)
