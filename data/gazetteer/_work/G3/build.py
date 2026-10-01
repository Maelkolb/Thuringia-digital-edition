import json, sys
sys.path.insert(0, '.')
import part1, part2, part3
entries = part1.ENTRIES + part2.ENTRIES + part3.ENTRIES
# drop None years? keep as the schema example does (year: null)
order = ["id","name","start","end","landestheil","type_verbatim","type","wuestung","historic_forms","dialect_form","first_mention_year","location","elevation","parish","school","houses","inhabitants","census_year","occupations","crafts","flur_morgen","flur_verbatim","soil","livestock","municipal_finances","facilities","subplaces","events","persons","summary_de","summary_en","notes"]
out=[]
for e in entries:
    extra=set(e)-set(order)
    assert not extra, (e['id'], extra)
    out.append({k:e[k] for k in order if k in e})
d={"package":"G3","pages":"570-633","entries":out}
json.dump(d, open('../../G3.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print(len(out),'entries')
