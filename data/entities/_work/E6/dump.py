import json,sys,re
c=json.load(open('data/entities/candidates/organisations.json',encoding='utf-8'))['entries']
a,b=int(sys.argv[1]),int(sys.argv[2])
W=int(sys.argv[3]) if len(sys.argv)>3 else 60
for i,e in enumerate(c[a:b],a):
    forms=e['forms']
    f=''
    if len(forms)>1 or list(forms)[0]!=e['key']:
        f=' F='+','.join(f'{k}:{v}' for k,v in forms.items())
    br=''
    if e.get('brueckner_register'):
        br=' BR='+';'.join(f"{r['name']}@{','.join(r['pages'][:2])}" for r in e['brueckner_register'][:2])
    ctx=e['contexts'][0]['text']
    m=re.search('⟦.*?⟧',ctx)
    if m:
        ctx=ctx[max(0,m.start()-W):m.end()+W]
    print(f"{i}|{e['key']}|n{e['n']}{f}{br}|p{e['pages'][0]}| {ctx}")
