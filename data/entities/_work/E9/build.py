import json,glob,sys,re
ROOT='C:/Users/totom/Projects/reuss-edition/'
sl=json.load(open(ROOT+'data/entities/slices.json',encoding='utf-8'))['E9']['keys']
cand={x['key']:x for x in json.load(open(ROOT+'data/entities/candidates/concepts.json',encoding='utf-8'))['entries']}
dec={}
errs=[]
for f in sorted(glob.glob(ROOT+'data/entities/_work/E9/d*.txt')):
    for ln,line in enumerate(open(f,encoding='utf-8'),1):
        line=line.rstrip('\n')
        if not line.strip() or line.startswith('#'): continue
        if ' => ' not in line:
            errs.append(f'{f}:{ln} no =>'); continue
        lhs,rhs=line.split(' => ',1)
        keys=[k.strip() for k in lhs.split(' ;; ')]
        act,_,rest=rhs.partition(' ')
        parts=[p.strip() for p in rest.split(' | ')]
        for k in keys:
            if k not in cand: errs.append(f'{f}:{ln} unknown key {k!r}'); continue
            if k in dec: errs.append(f'{f}:{ln} duplicate {k!r}')
            if act=='M':
                dec[k]={'key':k,'action':'merge','into':parts[0]}
            elif act=='R':
                dec[k]={'key':k,'action':'reject','reason':parts[0]}
            elif act=='A':
                if len(keys)>1: errs.append(f'{f}:{ln} A with multiple keys')
                parts+=['']*(5-len(parts))
                label,kind,gloss,modern,note=parts[:5]
                cls='concept'
                if ':' in kind: cls,kind=kind.split(':',1)
                d={'key':k,'action':'accept','label':label,'class':cls,'kind':kind}
                if gloss: d['gloss_en']=gloss
                if modern and modern!=label: d['modern']=modern
                if note: d['note']=note
                dec[k]=d
            else: errs.append(f'{f}:{ln} bad action {act!r}')
# merge target checks
for k,d in dec.items():
    if d['action']=='merge':
        t=d['into']
        if t not in dec and t not in cand: errs.append(f'merge {k} -> {t} unknown')
        elif t in dec and dec[t]['action']!='accept': errs.append(f'merge {k} -> {t} target is {dec[t]["action"]}')
missing=[k for k in sl if k not in dec]
print('decided',len(dec),'missing',len(missing),'errors',len(errs))
for e in errs[:40]: print(' ERR',e)
if missing: print('first missing idx',sl.index(missing[0]), missing[:5])
if '--write' in sys.argv:
    out={'package':'E9','group':'concepts','decisions':[dec[k] for k in sl if k in dec]}
    json.dump(out,open(ROOT+'data/entities/decisions/E9.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
    print('written')
