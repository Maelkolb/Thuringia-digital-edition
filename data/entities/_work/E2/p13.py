from lib import *
# Harmonisation with E1 conventions and revisions (applied last, overrides earlier decisions).
import lib

def OV(key):
    D.pop(key, None)

# --- Landestheile: use E1's canonical keys
OV('Landrathsbezirk Gera'); M('Landrathsbezirk Gera', 'Bezirk Gera')
OV('Landestheil Schleiz'); M('Landestheil Schleiz', 'Bezirk Schleiz')
for k, d in list(D.items()):
    if d['action'] == 'merge':
        if d['into'] == 'Landestheil Schleiz':
            d['into'] = 'Bezirk Schleiz'
        elif d['into'] == 'Landrathsbezirk Gera':
            d['into'] = 'Bezirk Gera'
OV('Lobenstein-Ebersdorf')
A('Lobenstein-Ebersdorf', 'Bezirk Lobenstein-Ebersdorf', 'Landestheil', inp=True,
  gloss='Lobenstein-Ebersdorf district (Landrathsbezirk)',
  note='Einer der drei Landestheile (Landrathsbezirke) des Fürstenthums neben Gera und Schleiz.')

# --- court district labels / table row labels: reject like E1 (Gera I, Gera Summe)
for k, why in [('Lobenstein I', 'court district label (Einzelgericht Lobenstein I) in a judicial statistics table'),
               ('Lobenstein II', 'court district label (Einzelgericht Lobenstein II) in a judicial statistics table'),
               ('Schleiz I', 'court district label (Einzelgericht Schleiz I) in a judicial statistics table'),
               ('Schleiz II', 'court district label (Einzelgericht Schleiz II) in a judicial statistics table'),
               ('Schleiz Städte', 'table row label (towns of the Schleiz district), not a place'),
               ('Schleiz Plattland', 'table row label (countryside of the Schleiz district), not a place'),
               ('Schleiz Summe', 'table row label (total for the Schleiz district), not a place'),
               ('Lobenstein-Ebersdorf Städte', 'table row label (towns of the Lobenstein-Ebersdorf district), not a place'),
               ('Lobenstein-Ebersdorf Plattland', 'table row label (countryside of the Lobenstein-Ebersdorf district), not a place'),
               ('Lobenstein-Ebersdorf Summe', 'table row label (total for the Lobenstein-Ebersdorf district), not a place')]:
    OV(k); R(k, why)

# --- coordinated pairs: reject like E1 (Hohen- und Tiefendorf)
for k, why in [('Wüst- und Kleinfalke', 'coordinated pair of two places (Wüstfalke and Kleinfalke), not a single entity'),
               ('Zwötzen= Leumnitz', 'coordinated pair of two places (Zwötzen, Leumnitz; parish list), not a single entity'),
               ('Schilbach= Zollgrün', 'coordinated pair of two places (Schilbach, Zollgrün; parish list), not a single entity'),
               ('Langen- und Kleinwolschendorf', 'coordinated pair of two places (Langenwolschendorf, Kleinwolschendorf), not a single entity'),
               ('Scheuben- noch Langengrobsdorf', 'coordinated pair of two places (Scheubengrobsdorf, Langengrobsdorf), not a single entity'),
               ('Ober- und Niedergrün', 'coordinated pair of two places (Obergrün = Langgrün, Niedergrün), not a single entity')]:
    OV(k); R(k, why)

# --- noble families / houses: reclass to person register (cf. E1: Kaffenberg)
def FAM(key, label, note):
    OV(key)
    RC(key, label, 'person', 'Adelsfamilie', note=note)
FAM('Thüngen', 'von Thüngen', '"einer von Thüngen der Ruzze" (S. 353): noble family, not a place reference.')
FAM('Landwüst', 'von Landwüst', 'In der Liste der reußischen Vasallen (S. 266): noble family name.')
FAM('Löbschitz', 'von Löbschitz', 'In der Liste der reußischen Vasallen (S. 266): noble family name.')
FAM('Oberweimar', 'von Oberweimar', 'In der Liste der reußischen Vasallen (S. 266): noble family name.')
FAM('Tautenburg', 'Schenken von Tautenburg', '"Christian Schenk v. Tautenburg" (genealogical table): noble family, not a place reference.')
FAM('Lobdaburg', 'Grafen von Lobdaburg', '"aus dem gräfl. Hause Lobdaburg" (genealogical table): noble family (Lobdeburg-Arnshaugk).')
FAM('Meran', 'Haus Meran', 'Dynasty (Andechs-Meranien), nicht ein Ort.')
FAM('Uttenhoven', 'von Uttenhoven', 'Fräulein von Uttenhoven in einer Sage: noble family, not a place reference.')
FAM('Schwarzburg-Leutenberg', 'Haus Schwarzburg-Leutenberg', '"Wilburg aus dem Hause Schwarzburg-Leutenberg": noble house.')
OV('Roßla'); R('Roßla', 'part of a noble house name (Stolberg-Roßla) in a genealogical table, not a place reference')

# --- Flurnames (cf. E1: Flur entries for Hauptflurstücke)
def FLUR(key, where, label=None, kind='Flur', extra=''):
    OV(key)
    note = f'Flurstücksname ({where}).' + (' ' + extra if extra else '')
    A(key, label or key, kind, inp=True, note=note, gloss=f'{label or key} (field name)')

for k, w in [('Teichäcker', 'Hauptflurstück in der Flur Pöppeln, S. 449'),
             ('Vogeläcker', 'Hauptflurstück in der Flur Pöppeln, S. 449'),
             ('Tännicht', 'Hauptflurstück in der Flur Laasen, S. 558'),
             ('Lerchenberg', 'Hauptflurstück in der Flur Wernsdorf, S. 531'),
             ('Schiffswiese', 'Hauptflurstück in der Flur Thieschitz, S. 477'),
             ('Neuwiesen', 'Hauptflurstück in der Flur Thieschitz, S. 477'),
             ('Tännigswand', 'Hauptflurstück in der Flur Mühlsdorf, S. 481'),
             ('Steinberg', 'Hauptflurstück in der Flur Mühlsdorf, S. 481; häufiger Flurname'),
             ('Lehmgrube', 'Hauptflurstück in der Flur Mühlsdorf, S. 481'),
             ('löhmaer Weggelänge', 'Hauptflurstück, S. 625'),
             ('langenbucher Weggelänge', 'Hauptflurstück, S. 625'),
             ('Loh', 'Hauptflurstück in der Flur Leitlitz, S. 626'),
             ('Leukera', 'Hauptflurstück in der Flur Leitlitz, S. 626'),
             ('Taubenthal', 'Hauptflurstück in der Flur Hohenleuben, S. 641'),
             ('Lausehügel', 'Hauptflurstück in der Flur Hohenleuben, S. 641'),
             ('Unterleube', 'Hauptflurstück in der Flur Hohenleuben, S. 641'),
             ('Oberleube', 'Hauptflurstück in der Flur Hohenleuben, S. 641'),
             ('Töpfersberg', 'Hauptflurstück, S. 644'),
             ('Schieferberg', 'Hauptflurstück, S. 644'),
             ('rothe Hiele', 'Hauptflurstück, S. 644'),
             ('Trifthügel', 'Hauptflurstück, S. 644'),
             ('langer Busch', 'Hauptflurstück, S. 644'),
             ('langer Winkel', 'Hauptflurstück, S. 644'),
             ('Lehden', 'Hauptflurstück, S. 644'),
             ('Mönchsleite', 'Hauptflurstück, S. 644'),
             ('Leitenwiesen', 'Hauptflurstück in der Flur Schönbrunn, S. 743'),
             ('Trahholz', 'Hauptflurstück (Tröhholz) in der Flur Schönbrunn, S. 743'),
             ('Thiergarten', 'Hauptflurstück in der Flur Schönbrunn, S. 743'),
             ('Steinbühl', 'Hauptflurstück, S. 750'),
             ('Pfaffenwiesen', 'Flurstück bei Lichtenbrunn, S. 780'),
             ('Scheibe', 'Flurstück bei Lichtenbrunn, S. 780'),
             ('Mühlwiesen', 'Hauptflurstück, S. 823'),
             ('Wetterau', 'Hauptflurstück, S. 823; nicht zu verwechseln mit der Wettera (Wetterau)'),
             ('Stuffsacker', 'Flurstück bei Saaldorf, S. 727'),
             ('Schillerau', 'Wiesengrund, S. 792'),
             ('Polich', 'Flurname bei Saalburg (Gottesacker), S. 737'),
             ('Stutenkamm', 'Flurname bei Lichtenbrunn, S. 780'),
             ('Osterfelde', 'Flurname bei Hohenleuben (Hainberg), S. 639'),
             ('Pastholz', 'Flurname bei Wüstfalke, S. 567'),
             ('Schellenneun', 'Flurname (Grenzmarke) bei Wüstfalke, S. 565'),
             ('Weinberg', 'Flurstücksname, S. 536 und 641; häufiger Flurname'),
             ('Modera', 'Wiesengrundstück des Saalburger Klosters, S. 673'),
             ('Rothenbühl', 'Wiesengrundstück des Saalburger Klosters, S. 673'),
             ('Schindlera', 'Wiesengrundstück des Saalburger Klosters, S. 673'),
             ('Schrollera', 'Wiesengrundstück des Saalburger Klosters, S. 673'),
             ('Weidenwarth', 'Wiesengrundstück des Saalburger Klosters, S. 673'),
             ('Lippisch', 'Wiesengrundstück des Saalburger Klosters, S. 673')]:
    FLUR(k, w)
FLUR('Töpfergasse', 'Gasse in Hohenleuben (Pfarrschenke), S. 640', kind='Straße')
FLUR('Saalgasse', 'Gasse in Hirschberg (Leichenhof), S. 813', kind='Straße')
