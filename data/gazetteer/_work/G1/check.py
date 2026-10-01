import json, re, sys
sys.path.insert(0, 'tools')
import importlib.util
spec = importlib.util.spec_from_file_location('vg', 'tools/validate_gazetteer.py')
vg = importlib.util.module_from_spec(spec); sys.argv=['x']; spec.loader.exec_module(vg)
d = json.load(open('data/gazetteer/G1.json', encoding='utf-8'))
ABBR = {'Pf.':'Pferde','R.':'Rinder','K.':'Rinder','Schf.':'Schafe','Schw.':'Schweine','Z.':'Ziegen','G.':'Gänse','Bnst.':'Bienenstöcke','E.':'Esel','Esel':'Esel'}
for e in d['entries']:
    t = vg.article_text(e['start'], e['end']).replace('\n',' ')
    t = re.sub(r'\s+', ' ', t)
    i = t.find('an Vieh')
    if i >= 0 and 'livestock' in e:
        seg = t[i+7:i+400]
        found = {}
        last = 0
        for mm in re.finditer(r'(\d+(?:[—-]\d+)?)\s*(Pf\.|R\.|K\.|Schf\.|Schw\.|Z\.|G\.|Bnst\.|E\.)', seg):
            if mm.start() - last > 60 and found: break
            found[ABBR[mm.group(2)]] = mm.group(1); last = mm.end()
        for k,v in e['livestock'].items():
            if k not in found or str(v) != re.split(r'[—-]', found[k])[0]:
                print(e['id'], 'LIVESTOCK mismatch', k, v, found.get(k))
        for k in found:
            if k not in e['livestock']: print(e['id'], 'LIVESTOCK missing', k, found[k])
    elif 'livestock' in e:
        print(e['id'], 'no Vieh segment found')
    m = re.search(r'in (\d+) (?:Familien|Haushaltungen) (\d+) \(1861: (\d+)\)', t) or re.search(r'(\d+) Familien (\d+) \(1861: (\d+)\)', t)
    if m:
        if e.get('inhabitants') not in (int(m.group(2)),): print(e['id'], 'INHAB', e.get('inhabitants'), m.groups())
    else:
        if e['type'] in ('Dorf',): print(e['id'], 'no inhabitants pattern', e.get('inhabitants'))
