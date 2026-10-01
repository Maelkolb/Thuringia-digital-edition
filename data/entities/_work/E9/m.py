import json,sys
T={'Environment','Resource','Climate','Environmental Impact'}
keys=sys.argv[1].split('||'); n=int(sys.argv[2]) if len(sys.argv)>2 else 10
w=int(sys.argv[3]) if len(sys.argv)>3 else 160
rows=[json.loads(l) for l in open('data/entities/mentions.jsonl',encoding='utf-8')]
for k in keys:
    c=0
    print('==',k)
    for r in rows:
        if r['key']==k and r['type'] in T:
            t=r['ctx'].replace('\n',' ')
            j=t.find('⟦'); lo=max(0,j-w//2)
            print(f"  p{r['page']} {r['type'][:3]}: {t[lo:lo+w]}")
            c+=1
            if c>=n: break
