import json,sys,re
w=int(sys.argv[1]); keys=set(sys.argv[2:])
by={k:[] for k in keys}
for m in open('data/entities/mentions.jsonl',encoding='utf-8'):
    d=json.loads(m)
    if d['key'] in keys: by[d['key']].append(d)
for k in sys.argv[2:]:
    print('##',k,len(by[k]))
    for d in by[k]:
        t=d['ctx']; m=re.search(r'⟦.*?⟧',t)
        a=max(0,m.start()-w) if m else 0
        print('  p'+d['page'],t[a:(m.end()+w) if m else None].replace('\n',' '))
