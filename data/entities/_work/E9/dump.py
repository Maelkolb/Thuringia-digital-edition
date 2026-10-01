import json,sys
s=json.load(open('data/entities/slices.json',encoding='utf-8'))['E9']['keys']
c={x['key']:x for x in json.load(open('data/entities/candidates/concepts.json',encoding='utf-8'))['entries']}
a,b=int(sys.argv[1]),int(sys.argv[2])
ctxn=int(sys.argv[3]) if len(sys.argv)>3 else 0
abbr={'Environment':'Env','Resource':'Res','Climate':'Cli','Environmental Impact':'Imp'}
for i,k in enumerate(s[a:b],a):
    x=c[k]
    t=','.join(f"{abbr.get(t,t[:3])}{v}" if len(x['types'])>1 else abbr.get(t,t[:3]) for t,v in x['types'].items())
    f=''
    if len(x['forms'])>1 or list(x['forms'])[0]!=k:
        f=' F:'+';'.join(f"{a}{'' if v==1 else '×'+str(v)}" for a,v in x['forms'].items())
    line=f"{i}|{k}|{x['n']}|{t}{f}"
    if ctxn:
        for cx in x['contexts'][:ctxn]:
            line+=' ||'+cx['text'][:110].replace('\n',' ')
    print(line)
