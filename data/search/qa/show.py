import json,sys,io,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
f=sys.argv[1]; cat=sys.argv[2] if len(sys.argv)>2 else None; n=int(sys.argv[3]) if len(sys.argv)>3 else 4
R=json.load(open(f,encoding='utf-8'))
for r in R:
    if cat and not r['cat'].startswith(cat): continue
    st=r['status'].replace('\n',' ')
    print(f"## {r['q']} -> {st}" + (f"  [{r['didyoumean']}]" if r['didyoumean'] else '') + (f"  CHIPS: {' | '.join(e[:28] for e in r['entities'][:3])}" if r['entities'] else ''))
    for h in r['hits'][:n]:
        loc=h['title'] if h['kind'] in('Register','Glossar','Auswertung','Ortsartikel') else h['title'].replace('Seite ','S.')
        sn=re.sub(r'\s+',' ',h['snippet'])[:105]
        print(f"   {h['kind'][:5]} {loc[:30]} :: {sn}")
