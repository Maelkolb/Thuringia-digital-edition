import json,sys,io,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
base,new,grades=sys.argv[1:4]
start=int(sys.argv[4]) if len(sys.argv)>4 else 0; end=int(sys.argv[5]) if len(sys.argv)>5 else 10**6
G={}
for l in open(grades,encoding='utf-8'):
    p=l.rstrip('\n').split('\t'); G[p[0]]=p[1]
a=json.load(open(base,encoding='utf-8')); b=json.load(open(new,encoding='utf-8'))
def key(r): return [h['href'] for h in r['hits'][:3]]
i=0
for x,y in zip(a,b):
    if key(x)==key(y): continue
    i+=1
    if i<=start or i>end: continue
    st=y['status'].replace('\n',' ')
    print(f"## {y['q']} [base {G.get(y['q'],'?')}] {x['status'].split(chr(10))[0]} -> {st}")
    for h in y['hits'][:3]:
        loc=h['title'] if h['kind'] in('Register','Glossar','Auswertung','Ortsartikel') else h['title'].replace('Seite ','S.')
        print(f"   {h['kind'][:5]} {loc[:30]} :: {re.sub(chr(10),' ',h['snippet'])[:95]}")
