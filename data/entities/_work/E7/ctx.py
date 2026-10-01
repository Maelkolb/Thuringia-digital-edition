import json,sys,re
c=json.load(open('data/entities/candidates/organisms.json',encoding='utf-8'))['entries']
a,b=int(sys.argv[1]),int(sys.argv[2])
w=int(sys.argv[3]) if len(sys.argv)>3 else 70
mx=int(sys.argv[4]) if len(sys.argv)>4 else 1
for i in range(a,b):
    e=c[i]
    out=[]
    for x in e['contexts'][:mx]:
        t=x['text']
        m=re.search('⟦',t)
        s=max(0,m.start()-w) if m else 0
        out.append(f"p{x['page']}: "+t[s:s+2*w+len(e['key'])+4].replace('\n',' '))
    print(f"{i} {e['key']} ({e['n']}) "+' // '.join(out))
