import sys,json
from pathlib import Path
ROOT=Path(r'C:\Users\totom\Projects\reuss-edition')
key=sys.argv[1]; w=int(sys.argv[2]) if len(sys.argv)>2 else 150
rows=[]
for l in open(ROOT/'data/entities/mentions.jsonl',encoding='utf-8'):
    if f'"key": "{key}"' in l:
        d=json.loads(l)
        if d['key']==key: rows.append(d)
print(key,len(rows))
for d in rows:
    c=d['ctx']
    i=c.find('⟦')
    s=max(0,i-w//2); 
    print(f"  [{d['page']} {d['unit']}] {c[s:s+w+10]}")
