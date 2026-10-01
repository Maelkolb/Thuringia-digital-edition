import json, re, subprocess, sys
from lib import *
exec(open('gen_latin.py',encoding='utf-8').read().split("latin=[]")[0])  # reuse tables (merge_map, epithet, label_fix, ...)
FILES=['dsl_animals.txt','dsl_animals2.txt','dsl_animals3.txt','dsl_plants.txt','dsl_misc.txt','dsl_misc2.txt','dsl_latin_merges.txt']
dec=parse_all(FILES)
for e in ERRORS: print('PARSE ERROR',e)
latin=json.load(open('latin_idx.json'))
for i in latin:
    k=KEYS[i]
    if k in dec: continue
    label = epithet.get(k) or label_fix.get(k) or k
    label = label.strip()
    sci = sci_fix.get(k) or norm_sci(label)
    sci = norm_sci(sci)
    pg = BYKEY[k]['pages'][0]
    if i<=107: grp=''
    d={'key':k,'action':'accept','label':label,'class':'organism','kind':'Pflanze','scientific':sci,'rank':'species'}
    notes=[]
    en=extra_notes.get(sci[:1].upper()+sci[1:]) or extra_notes.get(label) or extra_notes.get(sci)
    if en: notes.append(en)
    if k in epithet: notes.append('Gattungsname aus der Vorzeile der Tabelle ergänzt (S. 73).') if k not in ('Halleri','arenosa','paucistamineus','cheiranthoides','lanceolatum','Philonotis') else notes.append('Gattungsname aus der Vorzeile der Tabelle ergänzt (S. 73).')
    if pg=='60': notes.append('Phänologische Beobachtungen (Gera), S. 60.')
    elif k=='Gentiana ciliata': pass
    elif pg in('72',) or (pg=='73' and i<=511 and 422<=i): notes.append('Verzeichnis der nur im Unterland vorkommenden Phanerogamen (S. 72-73).')
    elif pg in ('73','74') or (pg=='75' and k=='Telekia speciosa'): 
        if k not in ('Telekia speciosa',): notes.append('Verzeichnis der nur im Oberland vorkommenden Phanerogamen (S. 73-75).')
    if notes: d['note']=' '.join(notes)
    dec[k]=d
json.dump(dec, open('dec_raw.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
names=sorted({(d['scientific']) for d in dec.values() if d.get('scientific')})
open('sci_names.txt','w',encoding='utf-8').write('\n'.join(names)+'\n')
print(len(dec),'decisions;',len(names),'sci names')
und=[k for k in KEYS if k not in dec]
print('undecided',len(und),und[:50])
