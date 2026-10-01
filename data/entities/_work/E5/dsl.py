import json,sys,glob,re
ABBR={
 'gem':'Gemahlin','adl':'Adliger','adlf':'Adlige','pf':'Pfarrer','gl':'Geistlicher','lehr':'Lehrer','bea':'Beamter',
 'gel':'Gelehrter','sch':'Schriftsteller','gut':'Gutsbesitzer','kai':'Kaiser','kön':'König','hl':'Heiliger',
 'bis':'Bischof','prz':'Prinzessin','prn':'Prinz','sub':'Subskribent','bürg':'Bürger','mil':'Militär',
 'äbt':'Äbtissin','non':'Nonne','sage':'Sagengestalt','kauf':'Kaufmann','hw':'Handwerker',
}
def parse(fn):
    out=[]
    for ln in open(fn,encoding='utf-8'):
        ln=ln.rstrip('\n')
        if not ln.strip(): continue
        if ' !! ' in ln:
            k,r=ln.split(' !! ',1); out.append({'key':k.strip(),'action':'reject','reason':r.strip()}); continue
        if ' -> ' in ln:
            k,t=ln.split(' -> ',1); out.append({'key':k.strip(),'action':'merge','into':t.strip()}); continue
        if ' => ' in ln:
            k,rest=ln.split(' => ',1); k=k.strip()
            parts=[p.strip() for p in rest.split(' | ')]
            kind=ABBR.get(parts[0],parts[0])
            lab=k.replace('= ','').replace('=','-').replace('ſ','s')
            x={'key':k,'action':'accept','label':lab,'class':'person','kind':kind}
            for p in parts[1:]:
                if p.startswith('l='): x['label']=p[2:]
                elif p.startswith('d='):
                    de,_,en=p[2:].partition(' ;; ')
                    x['description_de']=de.strip()
                    if en: x['description_en']=en.strip()
                elif p.startswith('n='): x['note']=p[2:]
                elif p.startswith('q='): x['wikidata']=p[2:]
                elif p.startswith('w='): x['_w']=p[2:]
                elif p.startswith('pg='): x['register_page']=p[3:]
                else: raise SystemExit('bad part %r in %r'%(p,ln))
            out.append(x); continue
        raise SystemExit('bad line: '+ln)
    return out
if __name__=='__main__':
    allx=[]
    for fn in sorted(glob.glob('data/entities/_work/E5/dec_*.txt')):
        allx+=parse(fn)
    keys=json.load(open('data/entities/_work/E5/keys_sorted.json',encoding='utf-8'))
    seen=set(); dup=[]
    for x in allx:
        if x['key'] in seen: dup.append(x['key'])
        seen.add(x['key'])
    print('decided',len(seen),'of',len(keys),'dups',dup,'unknown',[k for k in seen if k not in keys][:10])
    # overrides (wikidata etc.)
    import os
    ov='data/entities/_work/E5/overrides.json'
    ovd=json.load(open(ov,encoding='utf-8')) if os.path.exists(ov) else {}
    for x in allx:
        if x['key'] in ovd: x.update(ovd[x['key']])
    todo={x['key']:x.pop('_w') for x in allx if '_w' in x}
    json.dump(todo,open('data/entities/_work/E5/wd_todo.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
    json.dump({'package':'E5','group':'persons','decisions':allx},open('data/entities/decisions/E5.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
    miss=[k for k in keys if k not in seen]; print('missing',len(miss))
