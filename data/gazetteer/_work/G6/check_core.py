import json, re, sys
import importlib.util
spec = importlib.util.spec_from_file_location('vg', 'tools/validate_gazetteer.py')
vg = importlib.util.module_from_spec(spec); spec.loader.exec_module(vg)
d = json.load(open('data/gazetteer/G6.json', encoding='utf-8'))
for e in d['entries']:
    txt = vg.article_text(e['start'], e['end']).replace('\n', ' ')
    print('==', e['id'], '| houses', e.get('houses'), '| inh', e.get('inhabitants'), '| pupils', (e.get('school') or {}).get('pupils'), '| flur', e.get('flur_morgen'))
    for m in re.finditer(r'[^.]{0,90}(?:Einw\.|Einwohner)[^.]{0,30}', txt):
        print('   E:', m.group(0)[:160])
        break
    for m in re.finditer(r'[^.]{0,60}(?:Schulkind|Kinder sind|Unterricht erhalten|Schulkinder)[^.]{0,30}', txt):
        print('   S:', m.group(0)[:130])
    for m in re.finditer(r'[^.]{0,40}Morgen (?:umfass|groß|enthalt)[^.]{0,20}|Flur,[^.]{0,60}Morgen[^.]{0,20}', txt):
        print('   F:', m.group(0)[:130]); break
