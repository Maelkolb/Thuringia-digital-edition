import json, re, sys
import importlib.util
spec = importlib.util.spec_from_file_location('vg', 'tools/validate_gazetteer.py')
vg = importlib.util.module_from_spec(spec); spec.loader.exec_module(vg)
d = json.load(open('data/gazetteer/G6.json', encoding='utf-8'))
def stems(k):
    k = k.split(' (')[0]
    return k[:5].lower()
bad = 0
for e in d['entries']:
    txt = vg.article_text(e['start'], e['end']).replace('\n', ' ')
    low = txt.lower()
    for fld in ('occupations', 'crafts'):
        for k, v in (e.get(fld) or {}).items():
            st = stems(k)
            if k.startswith('Ackerbau'):
                continue
            ok = False
            # number followed (within 120 chars, no sentence stop) by stem
            for m in re.finditer(r'(?<![\d/.,])(\d[\d.]*)(?![\d/])', low):
                if m.group(1).replace('.', '') != str(v):
                    continue
                seg = low[m.end(): m.end() + 130]
                seg = re.split(r'\. [A-ZÄÖÜ]|\.\s', seg)[0] if False else seg
                if st in seg.split('. ')[0]:
                    ok = True; break
            if not ok:
                bad += 1
                print(e['id'], fld, k, v, 'NOT FOUND near stem')
print('bad', bad)
