import json,sys,re
c=json.load(open('data/entities/candidates/persons.json',encoding='utf-8'))
ents={e['key']:e for e in c['entries']}
w=int(sys.argv[1]); 
for k in sys.argv[2:]:
    e=ents[k]; print('##',k,e['n'],e['forms'],e['types'])
    for x in e['contexts']:
        t=x['text']; m=re.search(r'⟦.*?⟧',t)
        a=max(0,m.start()-w) if m else 0
        print('  p'+x['page'],t[a:m.end()+w if m else None])
