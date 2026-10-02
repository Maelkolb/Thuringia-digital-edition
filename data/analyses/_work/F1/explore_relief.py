from common import *
import re, collections
a=load('relief-wohnorte-hoehenlage')
ds=ds_of(a,'places')
rows=rows_as_dicts(ds)
b=shared('base_places'); bc=[c['name'] for c in b['columns']]
base=collections.defaultdict(list)
for r in b['rows']: base[r[0]].append(dict(zip(bc,r)))
MAN={'Seifarthsdorf':'Seifartsdorf','Lauenhayn':'Lauenhain','Carolinenfeld':'Karolinenfield','Karolinensfeld':'Karolinenfield','Culm':'Kulm','Dettersdorf':'Oettersdorf','Venzka':'Venzka','Benzka':'Venzka','Mielesdorf':'Mielesdorf','Spilmes':'Spielmes'}
def norm(n):
    n=re.sub(r'\s*\(.*?\)','',n)
    n=n.split(',')[0].strip()
    n=re.sub(r'\s+(oberstes|unterste|Nordgasse|Dorfmitte|Mitte).*$','',n)
    n=n.strip()
    return MAN.get(n,n)
cnt=0; out=[]
for r in rows:
    if r['art']!='Ort' or r['in_klammern']: continue
    n=norm(r['name'])
    if n in base:
        cnt+=1
        out.append((n,r['name'],r['landesteil'],r['hoehe_mitte_m'],base[n][0]['lat']))
print(cnt, len([r for r in rows if r['art']=='Ort' and not r['in_klammern']]))
c=collections.Counter(o[0] for o in out)
for n,k in c.items():
    if k>1: print('dup',n,[ (o[1],o[2],o[3]) for o in out if o[0]==n])
miss=[r['name'] for r in rows if r['art']=='Ort' and not r['in_klammern'] and norm(r['name']) not in base]
print(len(miss),miss)
# sanity: landesteil vs lat
for o in out:
    if (o[2]=='Oberland' and o[4]>50.78) or (o[2]=='Unterland' and o[4]<50.78): print('LAT MISMATCH',o)
print([(o[1],o[2],round(o[3]),o[4]) for o in out if o[0] in ('Rödern','Burkersdorf','Göttengrün','Wernsdorf','Dittersdorf','Mühlberg','Langenberg','Neundorf','Hermsdorf')])

print('--------- fit')
import statistics
import numpy as np
