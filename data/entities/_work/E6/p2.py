from lib import *

# =====================================================================
# 4. Landesbehoerden, Gerichte, Verwaltung
# =====================================================================
acc("Staatsministerium", "Staatsministerium", kind="Behörde", gloss="State Ministry (government of the principality, Gera)",
    merges=["Staatsministeriums", "Ministerium", "Ministeriums"],
    note="Supreme authority of the principality, seat Gera (p. 434); 'Ministerium' without addition (pp. 268, 436) is the same body.")
acc("Ministerium in Justizsachen", "Ministerium, Abtheilung für Justiz", kind="Behörde", gloss="Ministry, department of justice",
    merges=["Ministeriums Abtheilung für Justiz"])
acc("fürstlichen Ministerium Abtheilung für das Innere", "Ministerium, Abtheilung für das Innere", kind="Behörde",
    gloss="Ministry, department of the interior")
acc("Ministeriums für Kirchen- und Schulangelegenheiten", "Ministerium, Abtheilung für Kirchen- und Schulangelegenheiten",
    kind="Behörde", gloss="Ministry, department of church and school affairs")
acc("Landtag", "Landtag", kind="Landtag", gloss="Landtag (state parliament of the principality)",
    merges=["Landtage", "Landtags", "Landtagen"])
rej("Landtagsmitglied", "title of a person (member of the Landtag), not an institution")
acc("Landrathsamt, fürstl", "Landrathsamt", kind="Behörde", gloss="district office (Landrathsamt)",
    merges=["Landrathsämter"], note="Administrative district office of the principality; in the subscribers' list (p. 837) the offices at Gera and Ebersdorf.")
acc("Justizämter", "Justizamt", kind="Behörde", gloss="justice office (lower court)",
    merges=["Justizamte", "Justizamt", "Justizamt I., fürstl", "Justizamt II., fürstl", "Justizamt, fürstl"],
    note="Local court of first instance; in the subscribers' list (p. 837) the offices at Gera (I and II), Schleiz (II) and Hohenleuben.")
acc("Justizamt zu Ebersdorf", "Justizamt Ebersdorf", kind="Behörde", gloss="justice office at Ebersdorf", register_page="731")
acc("Justizamt zu Lobenstein", "Justizamt Lobenstein", kind="Behörde", gloss="justice office at Lobenstein", register_page="713")
acc("Kreisgerichte", "Kreisgericht", kind="Behörde", gloss="district court (Kreisgericht)",
    merges=["Kreisgerichten", "Kreisgericht, fürstl"], note="Subscribers' list p. 837: the courts at Gera and Schleiz.")
acc("Appellationsgericht zu Eisenach", "Appellationsgericht zu Eisenach", kind="Behörde", gloss="Court of Appeal at Eisenach",
    merges=["Appellationsgericht", "Appellationsgerichts", "Appellationsgerichte"],
    note="Court of appeal for the principality (district by treaty of 23 March 1850, p. 281).")
acc("Oberappellationsgericht zu Jena", "Oberappellationsgericht zu Jena", kind="Behörde", gloss="Higher Court of Appeal at Jena",
    merges=["Oberappellationsgericht", "Oberappellationsgerichte zu Jena", "Oberappellationsgerichts zu Jena"])
acc("Competenzgerichtshof", "Competenzgerichtshof", kind="Behörde", gloss="court of competence (conflicts between courts and administration)",
    merges=["Competenzgerichtshofe"])
acc("Staatsanwaltschaft", "Staatsanwaltschaft", kind="Behörde", gloss="public prosecutor's office")
acc("Geschworenengerichte", "Geschworenengericht", kind="Behörde", gloss="jury court")
acc("Friedensgerichte", "Friedensgericht", kind="Behörde", gloss="conciliation court (justice of the peace)")
acc("Criminalgericht", "Criminalgericht", kind="Behörde", gloss="criminal court (Gera, until 1848)")
acc("Landesregierung", "Landesregierung", kind="Behörde", gloss="state government (Gera, until 1848)")
acc("Landesadministration", "Landesadministration", kind="Behörde", gloss="state administration (Gera, until 1848)")
acc("Steuerdirectorium", "Steuerdirectorium", kind="Behörde", gloss="tax directorate", merges=["Steuerdirectoriums"])
acc("Polizeidirectorium", "Polizeidirectorium", kind="Behörde", gloss="police directorate (Gera, until 1848)")
acc("Hauptstaatskasse", "Hauptstaatskasse", kind="Behörde", gloss="central state treasury (Gera, from 1854)")
acc("Generalinspection", "Generalinspection zu Erfurt", kind="Behörde", gloss="general inspectorate at Erfurt")
acc("Pensionsanstalt", "Pensionsanstalt", kind="Anstalt", gloss="pension fund for civil servants (since 1847)")
acc("Catasterbureau", "Catasterbureau", kind="Behörde", gloss="cadastral office (Gera)",
    merges=["Catasterbureaus", "Rechnungs- und das Katasterbureau", "Kanzleien"],
    note="'Kanzleien' (p. 276) are the two chanceries Rechnungs- und Katasterbureau.")
acc("Einschätzungskommission", "Einschätzungskommission", kind="Behörde", gloss="tax assessment commission")
acc("Kreisausschüsse", "Kreisausschuss", kind="Behörde", gloss="district committee (appeal body in tax matters)")
acc("Bezirksausschüssen", "Bezirksausschuss", kind="Behörde", gloss="district committee")
acc("Hauptsteueramt, fürstl", "Hauptsteueramt", kind="Behörde", gloss="main tax office (Gera)",
    note="Turned in 1867 into a Hauptsteueramt of the Thuringian Zollverein (p. 261).")
acc("Steuerämter", "Steueramt", kind="Behörde", gloss="tax office", merges=["Steuerämtern", "Steueramtes"],
    note="Four: Gera, Schleiz, Lobenstein and Hirschberg (p. 277).")
acc("Salzsteueramte", "Salzsteueramt (Heinrichshall)", kind="Behörde", gloss="salt tax office at Heinrichshall")
acc("Steuerrecepturen", "Steuerreceptur", kind="Behörde", gloss="tax collection point", merges=["Steuerreceptur"])
acc("Bezirkssteuereinnahmen", "Bezirkssteuereinnahme", kind="Behörde", gloss="district tax collection office",
    merges=["Bezirkssteuereinnahmern"])
acc("fürstlichen Kammer", "Fürstliche Kammer", kind="Behörde", gloss="princely chamber (domain administration)",
    merges=["Kammer, fürstl", "reußische Kammer"])
acc("Kammer-Commissariat", "Kammer-Commissariat", kind="Behörde", gloss="chamber commissariat (Untermhaus)")
acc("Kammerarchive", "Kammerarchiv", kind="Behörde", gloss="chamber archive (Schleiz castle)")
acc("Rentamt", "Rentamt", kind="Behörde", gloss="revenue office", merges=["Rentamt, fürstl", "Rentamtes"])
acc("Paragiatsrentamt", "Paragiatsrentamt", kind="Behörde", gloss="revenue office of the apanage lordship")
acc("Forstamt", "Forstamt", kind="Behörde", gloss="forestry office")
acc("Forstei", "Forstei", kind="Behörde", gloss="forestry district (Forstei)",
    note="Generic: the seat of a forestry district, several villages (e.g. pp. 418, 648).")
acc("Bergamte in Lobenstein", "Bergamt zu Lobenstein", kind="Behörde", gloss="mining office at Lobenstein", merges=["Bergamtes"])
acc("Physicatsvertretung", "Physicatsvertretung", kind="Behörde", gloss="deputy of the district physician")
acc("Handelskammer", "Handelskammer", kind="Behörde", gloss="chamber of commerce")
acc("Stadtrath", "Stadtrath", kind="Behörde", gloss="town council",
    note="Generic: the municipal council of a town (Lobenstein pp. 719, 722; subscribers: Gera, Lobenstein).")
acc("Stadtrathe zu Tanna", "Stadtrath zu Tanna", kind="Behörde", gloss="town council of Tanna")
acc("saalburger Rathe", "Rath zu Saalburg", kind="Behörde", gloss="town council of Saalburg", register_page="661")
acc("Kirchkastengerichte zu Saalburg", "Kirchkastengericht zu Saalburg", kind="Behörde", gloss="church-chest court at Saalburg")
acc("Hospitalgerichte", "Hospitalgericht (Lobenstein)", kind="Behörde", gloss="hospital court (Lobenstein)")
acc("Amts-", "Amtsgericht (Lobenstein)", kind="Behörde", gloss="bailiwick court (Lobenstein)",
    note="Fragment of 'Amts-, Stadt-, Pfarr- und Hospitalgerichte' (p. 721); completed.")
acc("Stadt-", "Stadtgericht (Lobenstein)", kind="Behörde", gloss="town court (Lobenstein)",
    note="Fragment of 'Amts-, Stadt-, Pfarr- und Hospitalgerichte' (p. 721); completed.")
acc("Pfarr-", "Pfarrgericht (Lobenstein)", kind="Behörde", gloss="parish court (Lobenstein)",
    note="Fragment of 'Amts-, Stadt-, Pfarr- und Hospitalgerichte' (p. 721); completed.")
acc("Armencommission", "Armencommission", kind="Behörde", gloss="poor-relief commission")
acc("Jagdausschuß", "Jagdausschuß", kind="Gemeindeorgan", gloss="hunting committee (municipal)")
acc("Schulvorstand", "Schulvorstand", kind="Gemeindeorgan", gloss="school board (municipal)")
acc("Canzlei", "Canzlei", kind="Behörde", gloss="chancery",
    note="'der Canzlei, dem Amte und dem Rittergute Haueisen' (p. 725), presumably the chancery at Lobenstein.")
acc("Amte Gera", "Amt Gera", kind="Behörde", gloss="Amt (bailiwick) Gera", merges=["geraer Amt"], register_page="428")
acc("Amte Schleiz", "Amt Schleiz", kind="Behörde", gloss="Amt (bailiwick) Schleiz", register_page="579")
acc("saalburger Amte", "Amt Saalburg", kind="Behörde", gloss="Amt (bailiwick) Saalburg", register_page="661")
acc("burgker Amte", "Amt Burgk", kind="Behörde", gloss="Amt (bailiwick) Burgk")
acc("Amte Ronneburg", "Amt Ronneburg", kind="Behörde", gloss="Amt (bailiwick) Ronneburg")
acc("Amte zu Neustadt a. d. Orla", "Amt Neustadt an der Orla", kind="Behörde", gloss="Amt (bailiwick) Neustadt an der Orla")
acc("schleizer Verwaltungsamt", "Verwaltungsamt Schleiz", kind="Behörde", gloss="administrative office (Verwaltungsamt) Schleiz")
acc("lobensteiner Inspectionsamt", "Inspectionsamt Lobenstein", kind="Behörde", gloss="inspection office (church supervision) Lobenstein",
    merges=["lobensteiner Inspectionsamte"])
concept("Amte", "Amt", "Behördentyp", "Amt (administrative and judicial office)",
        note="Bare 'dem Amte' (p. 725) without a place name.")

# --- Consistorien
acc("Consistorium zu Gera", "Consistorium zu Gera", kind="Behörde", gloss="consistory at Gera (1604-1863)",
    merges=["Consistorium", "Consistoriums", "reußischen"],
    note="Common consistory of the Reuss lands, 1604-1863 (p. 290, 713). Bare 'Consistorium' (pp. 290, 425, 434) and 'das reußische Consistorium' (p. 291) are this one.")
acc("Consistorium zu Altenburg", "Consistorium zu Altenburg", kind="Behörde", gloss="consistory at Altenburg (Saxe-Altenburg)",
    merges=["Altenburger Consistorium", "sächsisch-altenburgischen Consistorium"])
acc("Consistorium zu Plauen", "Consistorium zu Plauen", kind="Behörde", gloss="consistory at Plauen")
acc("Consistorium zu Greiz", "Consistorium zu Greiz", kind="Behörde", gloss="consistory at Greiz",
    merges=["fürstliche Consistorium in Greiz"])
acc("leipziger Consistoriums", "Consistorium zu Leipzig", kind="Behörde", gloss="consistory at Leipzig")
acc("Consistoriums zu Baireuth", "Consistorium zu Baireuth", kind="Behörde", gloss="consistory at Bayreuth")

# --- Post, Telegraph, Eisenbahn
concept("Post", "Post", "Einrichtung", "postal service",
        merges=["Posten", "Postamt", "Postexpedition"], note="Bare post offices and post stations; the Prussian post at Gera is a separate entry.")
acc("preußische Post", "Preußische Post (Gera)", kind="Behörde", gloss="Prussian post (Gera)",
    note="Taken over from the Thurn und Taxis post on 1 July 1867 (p. 434).")
concept("Telegraphenbureau", "Telegraphenbureau", "Einrichtung", "telegraph office", merges=["Telegraphenstation"])
acc("preußisches Telegraphenbureau", "Preußisches Telegraphenbureau (Gera)", kind="Behörde", gloss="Prussian telegraph office (Gera)")
acc("sächsische Telegraphenbureau", "Sächsisches Telegraphenbureau (Gera)", kind="Behörde",
    gloss="Saxon telegraph office (Gera)", note="Merged with the Prussian office in summer 1866 (p. 434).")
acc("thüringer Eisenbahngesellschaft", "Thüringische Eisenbahn-Gesellschaft", kind="Eisenbahngesellschaft",
    gloss="Thuringian Railway Company", merges=["Thüringer Eisenbahngesellschaft", "thüringer Eisenbahn"],
    note="Built the Weißenfels-Gera line (opened 19 March 1859, p. 434).")
acc("sächsisch-bayerische Staatseisenbahn", "Sächsisch-Bayerische Staatseisenbahn", kind="Eisenbahngesellschaft",
    gloss="Saxon-Bavarian State Railway")
acc("gössnitz-geraer Bahn", "Gößnitz-Geraer Bahn", kind="Eisenbahngesellschaft", gloss="Gößnitz-Gera railway company",
    note="The city of Gera held shares worth 50,000 Thaler (p. 438).")

# --- preussische Stellen, Muenzstaette
acc("preußischen Generalstabe", "Preußischer Generalstab", kind="Behörde", gloss="Prussian General Staff")
acc("königl. preußischen Münzstätte zu Berlin", "Königlich preußische Münzstätte zu Berlin", kind="Behörde", gloss="Royal Prussian mint at Berlin")
acc("Landkrankenhauses zu Jena", "Landkrankenhaus zu Jena", kind="Anstalt", gloss="state hospital at Jena",
    note="'Direction des großherzoglichen Landkrankenhauses zu Jena' (p. 274).")
acc("Hebammeninstitute zu Leipzig", "Hebammeninstitut zu Leipzig", kind="Schule", gloss="midwifery institute at Leipzig")
acc("eisenacher Forstlehranstalt", "Forstlehranstalt zu Eisenach", kind="Schule", gloss="forestry school at Eisenach")
