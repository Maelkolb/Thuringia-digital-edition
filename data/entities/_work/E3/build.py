import sys, glob, json, importlib, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dec
from lib import E, S
for f in sorted(glob.glob(os.path.join(HERE, 'p[0-9][0-9].py'))):
    name = os.path.basename(f)[:-3]
    try:
        importlib.import_module(name)
    except AssertionError as e:
        print('ASSERT in', name, e)
        raise
D = dec.D
missing = [k for k in S if k not in D]
print('decided', len(D), 'slice', len(S), 'missing', len(missing))
print(missing[:60])
extra = [k for k in D if k not in S]
print('extra', extra)
for k, x in D.items():
    if x['action'] == 'merge':
        t = x['into']
        if t not in D and t not in E:
            print('BAD target', k, '->', t)
        elif t in D and D[t]['action'] in ('merge', 'reject'):
            print('TARGET not accepted', k, '->', t, D[t]['action'])
GN = {}
for e in E.values():
    for g in e.get('geonames_candidates', []):
        GN[g['geonames']] = g
for k, x in D.items():
    if 'geonames' in x:
        g = GN.get(x['geonames'])
        if not g:
            print('GN unknown', k, x['geonames'])
            continue
        x['lat'] = g['lat']
        x['lon'] = g['lon']
for k, x in D.items():
    if x['action'] == 'reclass' and x['class'] == 'place' and E[k].get('brueckner_register'):
        regs = E[k]['brueckner_register']
        r = regs[0]
        if r.get('pages'):
            x['register_page'] = r['pages'][0]
print(collections.Counter(x['action'] for x in D.values()))
WDF = os.path.join(HERE, 'wd_map.json')
if os.path.exists(WDF):
    for k, q in json.load(open(WDF, encoding='utf-8')).items():
        assert k in D and D[k]['action'] in ('accept', 'reclass'), k
        D[k]['wikidata'] = q
res = []
for k in S:
    if k in D:
        x = D[k]
        y = {'key': k}
        y.update({kk: vv for kk, vv in x.items() if kk != 'key'})
        res.append(y)
out = {'package': 'E3', 'group': 'nature', 'decisions': res}
os.makedirs(os.path.join(HERE, '..', '..', 'decisions'), exist_ok=True)
with open(os.path.join(HERE, '..', '..', 'decisions', 'E3.json'), 'w', encoding='utf-8') as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
