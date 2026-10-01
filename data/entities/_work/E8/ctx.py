import json,sys
c=json.load(open('C:/Users/totom/Projects/reuss-edition/data/entities/candidates/concepts.json',encoding='utf-8'))['entries']
idx={e['key']:e for e in c}
n=int(sys.argv[1]); w=int(sys.argv[2])
for k in sys.argv[3:]:
    e=idx[k]
    print(f"## {k} (n={e['n']}) forms={e['forms'] if len(e['forms'])>1 else ''}")
    for x in e['contexts'][:n]:
        t=x['text']
        i=t.find('⟦')
        a=max(0,i-w); 
        print('  ',x['page'],t[a:i+w+20].replace('\n',' '))
