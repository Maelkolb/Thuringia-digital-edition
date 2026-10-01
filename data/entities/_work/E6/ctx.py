import json,sys
c={e['key']:e for e in json.load(open('data/entities/candidates/organisations.json',encoding='utf-8'))['entries']}
W=int(sys.argv[1])
import re
for k in sys.argv[2:]:
    e=c[k]
    print('==',k,e['n'],e['forms'], 'BR=',[ (r['name'],r['pages']) for r in e.get('brueckner_register',[])])
    for x in e['contexts'][:8]:
        t=x['text']; m=re.search('⟦.*?⟧',t)
        if m: t=t[max(0,m.start()-W):m.end()+W]
        print('  p'+x['page'],x['unit'],t)
