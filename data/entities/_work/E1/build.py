import sys, glob, importlib, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
for f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p[0-9][0-9].py'))):
    importlib.import_module(os.path.basename(f)[:-3])
D = lib.D
missing = [k for k in lib.SLICE if k not in D]
extra = [k for k in D if k not in set(lib.SLICE)]
print('decided', len(D), 'slice', len(lib.SLICE), 'missing', len(missing), 'extra', len(extra))
print('MISSING:', missing)
print('EXTRA:', extra)
# wikidata enrichment (verified by name + coordinates, or manually checked)
wd = {}
for fn in ('wd_auto.json', 'wd_manual.json'):
    fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), fn)
    if os.path.exists(fp):
        for k, v in json.load(open(fp, encoding='utf-8')).items():
            if v:
                wd[k] = v[1] if isinstance(v, list) else v
skipwd = set()
if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wd_reject.json')):
    skipwd = set(json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wd_reject.json'), encoding='utf-8')))
n_wd = 0
for k, x in D.items():
    if x['action'] in ('accept', 'reclass') and k in wd and k not in skipwd and 'wikidata' not in x:
        x['wikidata'] = wd[k]
        n_wd += 1
print('wikidata ids added', n_wd)
out = {'package': 'E1', 'group': 'places', 'decisions': [D[k] for k in lib.SLICE if k in D]}
path = os.path.join(str(lib.ROOT), 'data', 'entities', 'decisions', 'E1.json')
os.makedirs(os.path.dirname(path), exist_ok=True)
json.dump(out, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('written', path)
