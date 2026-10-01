# Transcription findings reported by subagents (facsimile-checked unless noted)

To be turned into `verified.json` (applied by normalize.py as rule `facsimile_correction`).

## G5 (pp. 706–764)
- Lothra livestock "22 Bmst." → "Bnst." (Bienenstöcke) [checked]
- Thimmendorf "15 Bust." → print reads "Bust."? treated as Bnst.
- Abbreviation "Aßo"/"Aßv" (pp. 745, 748, 764) unexplained in the book
- Print inconsistencies (NOT errors): Lobenstein inhabitants 2843 (p. 719) vs 2833 (pp. 707–708); Frössen 1867: 423 (p. 708) vs 422 (p. 707); p. 708 column sums 6443 vs printed 6453, 22360 vs 22359; Lobenstein assets 7404+37,444=44,848 printed 44,845
- Register page errors: Pollersreuther/Rödelshammer indexed 721 (is 727); Schlößchen 726 (is 727); Ponzelsmühle 763 (is 764)

## G1 (pp. 405–486)
- "Bollersdorf" → "Vollersdorf" on pp. 413, 418, 448 [448 checked]
- "Roschütz" → "Roschitz" p. 423 b3 [checked]
- "Coffe" → "Cosse" pp. 476, 481 (field-name lists) [not checked]
- p. 479 Töppeln "75 K." probably "R." [not checked]
- p. 409: long s (ſ) unresolved in table and b1/b3 ("Caaſchwitz", "Menſchen")
- pp. 411–412: brace subtotals put into extra columns (r5 Groitschen, r13 Lichtenberg; p. 412 Weißig/Zeulsdorf, Kleinfalke/Pohlen) [411 checked]
- Register: Lusan indexed 433 (article on 453); "Terdorf" in register is "Texdorf" (p. 479 checked); Käseschenke indexed 484 (is 485); Zshochern → Zschochern, Stärkenhäuser → Stärkehäuser
- Print inconsistency: p. 440 "1120 Handwerker" vs sum 1174

## G3 (pp. 570–632)
- "Dettersdorf" → "Oettersdorf" pp. 574, 588, 602, 604, 605 (also historic forms "Dettirsdorf", "Dettistorf" → "Oettirsdorf", "Oettistorf"?) [602/604/605 checked]
- p. 606 "203 K." → "203 R." [checked]
- p. 600 "17 Bust." → "17 Bnst." [checked]
- Brückner prints "NON." (= NNO) and "NWN." (= NNW)
- p. 613 fractions as superscripts "1269¹/₃" → 1269 1/3
- Print inconsistency: Schleiz p. 589 "290 Gesellen und Zöglinge" vs table p. 572 "390"
- Register: Glücksmühle (Oschitz 596) not in text; "Rostsmühle" printed "Roßmühle"; Helbigsmühle described p. 593 (index 579)

## G4 (pp. 633–705)
- p. 645 Hirschbach "18 K." → "18 R." [checked]
- p. 675 Kulm church assets "8124 1/2 Thlr." → "8124 1/7" [checked]
- "Aßo" = unexplained money unit (pp. 691, 693)
- Register: "Wüste Höfe" (683) is a field area of Seubtendorf, not a Gemeinde; Mansdorf = Mangelsdorf; "Wetteru" = Wettera

## G2 (pp. 487–569)
- 492 b2 Hartmannsdorf "110 K." → "110 R." [checked]
- 536 b2 "Söllnitz" → "Söllmnitz" [checked]
- 536 b3 "Beizdorf" → "Betzdorf"; forms "Beitzdorf, Bötzdorf, Bitzdorf, Baitzdorf, Etzdorf, Betzlingsdorf" as printed? and 1364 "Beczelinsdorf" → "Peczelinsdorf" [checked]
- Register spellings vs print: Eschwinsdorf/Eschewinsdorf; Ezdorf/Etzdorf; Kretschwitz/Kretzschwitz; Wolftitz/Wolstieg (checked); Wiesenmühle (487) not in text
- Systematic: livestock "K." is a misreading of "R." (Rinder) - seen in G1 (479), G2 (492), G3 (606), G4 (645)
- G2 details also in data/gazetteer/G2.json "transcription_issues"; G4 likewise

## G6 (pp. 765–825)
- No transcription errors found in checked numbers.
- Print inconsistencies: Kießling parts 194 vs printed 190; Gebersreuth 461 vs 444; Göritz 527+104=631 (1861 figure) vs 607; Titschendorf 92 houses vs 37+52=89; Wurzbach "Schmiede" listed twice (10 and 7); Neundorf Kammergut Hornsgrün (779) vs Heinrichsgrün (780)
- Wurzbach "398 Familien 1861 (1841: 1460; 1861: 1863) Einw." - leading "1861" = inhabitants (as printed)
- Register vs text: Alaunwerk 800→803; Hammermühle 809→814/817; Teichmühle 776→777; Abfang→Absang; Starenberg (Görlitz)→Starenburg (Göritz); Wegnersbach (Rießling)→Kießling; Osla→Oßla; Benzka=Venzka; Rosenbaummühle & Teichhäuser not in text
- "G." = Gänse (inferred), "Bnst./Bust./B." = Bienenstöcke

## A02 (pp. 25–52)
- p. 44 (scan 56, early schema): printed TABLE MISSING in transcription - Reichardt's analysis of Neue Quelle and Agnesquelle (Lobenstein): 14 constituents + sum (2,5232 / 1,0082), free carbonic acid, temperature, specific gravity. Values read from facsimile by A02 -> data/analyses/gewaesser-heilquellen-lobenstein-analyse.json (columns marked derived as workaround). TODO: add table block to page 44, then drop derived flags.
- p. 38 b1 "1 Kammschnecke" → "1 Kammerschnecke" [checked]
- Brückner never defines the length unit "Stunde"

## A03 (pp. 53–61)
- p. 57 b2 r4c4 Rothenacker March "Mittel": transcription "0,56", print "—0,56" [checked]
- Print errors (not transcription): p. 57 Ziegenrück December -4,33 inconsistent with means; p. 55/56 Gera March 1856 -6,8 °R inconsistent with Hohenleuben; p. 58 Lobenstein 1863 Oct-Dec identical to Rothenacker 1865
- Temperatures are Réaumur (legacy PNG plotted them as °C)
- Heights pp. 12, 20-22 in preußischer Dezimalfuß (0.3766242 m, p. 11 fn1), not ordinary Prussian foot

## B01 (pp. 826–840)
- p. 832 b8 Nürnberg Fuß "134,775" → print "134,75" par. Linien [checked]
- p. 831 b5 (S. 277): print "zuverzinsenden statt zu verzinsenden"; transcription "zuversindenden statt zu verzindenden" [checked]
- p. 833 b19 (S. 489): print "ganz statt gauz"; transcription "ganz statt ganz" [checked]
- p. 833 b20 (S. 496): print "besondere statt besondeer"; transcription "besonderer" [checked]
- Subscribers: Maucke (not Mauke), Meißner (Meissner), Sieckmann (Siekmann), v. Voß (v. Boss), Weißker ×3 (Weissker), Weißendorf (Weissendorf)
- Print errors: Schleiz Scheffel 1,4237 hl (should be 1,9237); Gera Elle 253,47 vs 253,74 par. Linien
- Transcriber may have silently fixed misprints named in the corrigenda: p. 489 "gauz" printed (transcribed "ganz") [checked]; check pp. 72 (Palicaria/Pulicaria), 84 (Steinschmetter/Steinschmetzer), 80, 86, 350, 503
- Corrigenda for S. 66, 67, 69 (climate) forwarded to A04; S. 219/221/223/230 forwarded to A09
