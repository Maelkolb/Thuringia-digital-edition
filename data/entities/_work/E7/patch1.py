import re
fix = {
 'Staar': ('Staar','Star'),
 'Kukuk': ('Kukuk','Kuckuck'),
 'Hausrothschwänzchen': None,
 'Gartenrothschwänzchen': ('Gartenrothschwänzchen','Gartenrotschwanz'),
 'Rothkehlchen': ('Rothkehlchen','Rotkehlchen'),
 'Fitislaubvogel': ('Fitislaubvogel','Fitis (Fitis-Laubsänger)'),
 'Waldlaubvögel': ('Waldlaubvogel','Waldlaubsänger'),
 'Fliegenschnapper': ('Fliegenschnapper','Fliegenschnäpper'),
 'Moor- und kleine Pfulschnepfe': ('Moor- und kleine Pfulschnepfe','Moor- und kleine Pfuhlschnepfe'),
 'Schwarz-, Grau- und Weißpecht': ('Schwarz-, Grau- und Weißpecht',''),
 'Rauchfußbussard': ('Rauchfußbussard','Raufußbussard'),
 'Kreuzschnäbel': ('Kreuzschnabel',''),
 'Schleihe': ('Schleihe','Schleie'),
 'Flußkrebs': ('Flußkrebs','Flusskrebs'),
 'Dammhirsche': ('Dammhirsch','Damhirsch'),
 'Hasen': ('Hase','Feldhase'),
 'Eichhorn': ('Eichhorn','Eichhörnchen'),
 'Amseln': ('Amsel',''),
}
for fn in ['dsl_animals.txt','dsl_animals2.txt']:
    out=[]
    for l in open(fn,encoding='utf-8').read().split('\n'):
        p=l.split('|')
        if p[0]=='T' and p[1] in fix and fix[p[1]]:
            lab,mod=fix[p[1]]
            while len(p)<7: p.append('')
            p[2]=lab; p[6]=mod
            l='|'.join(p).rstrip('|')
        out.append(l)
    open(fn,'w',encoding='utf-8').write('\n'.join(out))
