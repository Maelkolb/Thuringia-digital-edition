import json,sys
s=json.load(open('data/entities/slices.json',encoding='utf-8'))['E9']['keys']
c={x['key']:x for x in json.load(open('data/entities/candidates/concepts.json',encoding='utf-8'))['entries']}
a,b=int(sys.argv[1]),int(sys.argv[2]); nctx=int(sys.argv[3]); w=int(sys.argv[4])
for i,k in enumerate(s[a:b],a):
    x=c[k]
    f=''
    if len(x['forms'])>1 or list(x['forms'])[0]!=k:
        f=' F:'+';'.join(f"{a}×{v}" for a,v in x['forms'].items())
    print(f"{i}|{k}|{x['n']}|{'/'.join(t[:3] for t in x['types'])}{f}")
    for cx in x['contexts'][:nctx]:
        t=cx['text'].replace('\n',' ')
        j=t.find('⟦')
        lo=max(0,j-w//2); print('   p'+cx['page']+': '+t[lo:lo+w])
