"""Q01: structural chart lint (tooltip present, bar baseline, resolve, colour series count)."""
import json, glob, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]

def marks(vl):
    out = []
    def w(n):
        if isinstance(n, dict):
            m = n.get('mark')
            if m is not None: out.append(m if isinstance(m, str) else m.get('type'))
            for k, v in n.items(): w(v)
        elif isinstance(n, list):
            for x in n: w(x)
    w(vl); return out

def find(n, key, acc):
    if isinstance(n, dict):
        for k, v in n.items():
            if k == key: acc.append(v)
            find(v, key, acc)
    elif isinstance(n, list):
        for x in n: find(x, key, acc)

for f in sorted(glob.glob(str(ROOT / 'data/analyses/*.json'))):
    d = json.load(open(f, encoding='utf-8'))
    if d['id'].startswith(('orte-', 'ortskunde-')): continue
    for ch in d['charts']:
        vl = ch['vegalite']; msgs = []
        ms = marks(vl)
        tips = []; find(vl, 'tooltip', tips)
        if not tips: msgs.append('NO-TOOLTIP')
        rs = []; find(vl, 'resolve', rs)
        for r in rs:
            if 'independent' in json.dumps(r): msgs.append('RESOLVE-INDEPENDENT')
        # bar with zero false
        scales = []; find(vl, 'scale', scales)
        if 'bar' in ms and any(isinstance(s, dict) and s.get('zero') is False for s in scales): msgs.append('BAR-NONZERO-SCALE')
        h = vl.get('height')
        if h is None and 'facet' not in vl and 'spec' not in vl: msgs.append('NO-HEIGHT')
        elif isinstance(h, int) and not (160 <= h <= 460): msgs.append(f'HEIGHT={h}')
        # dataset row count of color domain
        ds = next(x for x in d['datasets'] if x['name'] == ch['dataset'])
        cols = [c['name'] for c in ds['columns']]
        cf = []; find(vl, 'color', cf)
        for c in cf:
            if isinstance(c, dict) and 'field' in c and c['field'] in cols:
                n = len({r[cols.index(c['field'])] for r in ds['rows']})
                if n > 8 and c.get('type') in ('nominal', 'ordinal', None) and 'scale' not in c: msgs.append(f"COLOR-{c['field']}={n}")
        if msgs: print(d['id'][:50].ljust(50), ch['id'], ms[:3], msgs)
