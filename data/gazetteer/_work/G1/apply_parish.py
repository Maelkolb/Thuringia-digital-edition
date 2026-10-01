# -*- coding: utf-8 -*-
import glob
files = sorted(glob.glob('data/gazetteer/_work/G1/c0[0-9].py'))
E = "…"
pairs = [
 ("Schlosskapelle/-kirche, dem h. Georg geweiht; Pastorat seit 1854 beim ersten Diacon zu Gera als Hofprediger und Pfarrer zu Untermhaus",
  "von 1852 an begann wieder der Gottesdienst in der Schlosskirche, deren Pastorat seit 1854 der erste Diacon zu Gera als Hofprediger und als Pfarrer zu Untermhaus verwaltet"),
 ("großes Kirch- und Pfarrdorf; Parochie Untermhaus, Gries und Cuba seit 1736",
  "großes Kirch- und Pfarrdorf " + E + " 1736 wurden unter Heinrich XXV. die vorher nach Gera in die Hauptkirche gepfarrten Gemeinden Untermhaus, Gries und Cuba von der Stadt getrennt, zu einer eigenen Parochie vereinigt"),
 ("gehört zu der dasigen herzoglich altenburgischen Kirche, Pfarrei und Schule",
  "In kirchlicher und scholarer Beziehung gehört sie zu der dasigen herzoglich altenburgischen Kirche, Pfarrei und Schule"),
 ("Die St. Salvatorkirche dient seitdem der Stadt als Hauptpfarrkirche; Parochie Gera mit 19,957 Seelen",
  "Die St. Salvatorkirche dient seitdem der Stadt als Hauptpfarrkirche " + E + " Zur Stadt gehören die Filiale Tinz, Lusan und Oberröppisch und als eingepfarrte Orte Pöppeln, Debschwitz, Pforten und Bieblach"),
 ("1604 zur Parochie erhoben, mit Leumnitz als Filial; seit 1844 Mutterkirche mit Pfarrsitz in Leumnitz",
  "Im Jahre 1604 erhob man den Ort zur Parochie und verband mit ihr Leumnitz als Filial " + E + " Zwötzen aber als Mutterkirche erhalten wurde"),
 ("von jeher und noch nach Unterröppisch gepfarrt und nach Sirbis geschult (Weimar)",
  "Das Dörfchen war von jeher und ist noch nach Unterröppisch gepfarrt und nach Sirbis geschult"),
 ("Pfarr- und Kirchdorf; Filial ist das altenburgische Dorf St. Gangloff",
  "Zu ihr gehört kein eingepfarrter Ort, dagegen als Filial das altenburgische Dorf St. Gangloff"),
 ("Kirch- und Pfarrdorf; Filial Geißen, eingepfarrt Kleinsaara",
  "freundliches Kirch- und Pfarrdorf " + E + " Eingepfarrt ist Kleinsaara"),
 ("Der Ort pfarrt, begräbt und schult nach Frankenthal\", \"school\": {\"exists\": False, \"pupils\": 60",
  "Der Ort pfarrt, begräbt und schult, dermalen mit 60 Kindern, nach Frankenthal\", \"school\": {\"exists\": False, \"pupils\": 60"),
 ("Der Ort pfarrt, begräbt und schult nach dem 1/4 Stunde entfernten Frankenthal",
  "Der Ort pfarrt, begräbt und schult, gegenwärtig mit 38 Kindern, nach dem 1/4 Stunde entfernten Frankenthal"),
 ("Eingepfarrt sind Ernsee, Scheubengrobsdorf, Windischenbernsdorf und Töppeln und außerdem ist Mühlsdorf ihr Filial; Parochie 1720 Seelen",
  "Eingepfarrt sind Ernsee, Scheubengrobsdorf, Windischenbernsdorf und Töppeln und außerdem ist Mühlsdorf ihr Filial. Demnach umfaßt die Parochie 1720 Seelen"),
 ("Kirche, in die Rubitz und Milbitz eingepfarrt sind",
  "eine auf der Kirchberghöhe erbaute Kirche, in die jetzt wie früher die zwei nahe gelegenen Dörfer Rubitz und Milbitz eingepfarrt sind"),
 ("Von jeher pfarrt, begräbt und schult der Ort nach dem ganz nahen Thieschütz",
  "Von jeher pfarrt, begräbt und schult der Ort (jetzt mit 11 Kindern) nach dem ganz nahen Thieschütz"),
 ("Rubitz pfarrt, begräbt und schult von jeher nach Thieschitz",
  "Rubitz pfarrt, begräbt und schult von jeher, jetzt mit 43 Kindern, nach Thieschitz"),
 ("Der Ort pfarrt, begräbt und schult nach Frankenthal\"}",
  "Der Ort pfarrt, begräbt und schult, jetzt mit 37 Kindern, nach Frankenthal, war aber in früherer Zeit mit der Kirche in Pottendorf in Verband\"}"),
 ("die Reformation fand sie als Filial von Frankenthal vor, das sie seitdem geblieben ist",
  "sicher aber ist, daß die Reformation sie als Filial von Frankenthal vorfand, das sie seitdem geblieben ist"),
]
for old, new in pairs:
    n = 0
    for f in files:
        s = open(f, encoding='utf-8').read()
        c = s.count(old)
        if c:
            s = s.replace(old, new)
            open(f, 'w', encoding='utf-8').write(s)
            n += c
    print(n, old[:60])
