import json, glob, re, sys, collections
ROOT = 'C:/Users/totom/Projects/reuss-edition/'
W = ROOT + 'data/entities/_work/E8/'
sl = json.load(open(ROOT + 'data/entities/slices.json', encoding='utf-8'))['E8']['keys']
SL = set(sl)
cand = {e['key']: e for e in json.load(open(ROOT + 'data/entities/candidates/concepts.json', encoding='utf-8'))['entries']}
reg = {}
for e in json.load(open(ROOT + 'data/registers/ortsregister.json', encoding='utf-8'))['entries']:
    reg[e['name']] = e

spec = {}      # key -> tuple
src = {}
problems = []
for f in sorted(glob.glob(W + 'd[0-9][0-9].txt')):
    for ln, line in enumerate(open(f, encoding='utf-8').read().split('\n'), 1):
        if not line.strip():
            continue
        p = line.split('|')
        k = p[0]
        if k not in SL:
            problems.append(f'unknown key {k!r} in {f[-7:]}:{ln}')
            continue
        if k in spec:
            problems.append(f'duplicate {k!r}: {src[k]} and {f[-7:]}:{ln} (later wins)')
        spec[k] = p[1:]
        src[k] = f'{f[-7:]}:{ln}'

# auto place entries for Ortsregister names
def reg_pages(e):
    if e.get('pages'):
        return e['pages']
    for s in e.get('see') or []:
        t = reg.get(s) or reg.get(s[:1].upper() + s[1:])
        if t and t.get('pages'):
            return t['pages']
    return []

def auto_place(k):
    e = reg[k]
    lk = k.lower()
    if lk.endswith('mühle'): kind, g = 'Mühle', 'mill'
    elif lk.endswith('hammer'): kind, g = 'Hammer', 'hammer works'
    elif lk.endswith('hütte'): kind, g = 'Hütte', 'works'
    elif lk.endswith('schenke'): kind, g = 'Schenke', 'inn'
    elif lk.endswith('werk'): kind, g = 'Gewerbeanlage', 'works'
    elif lk.endswith('häuser'): kind, g = 'Weiler', 'hamlet'
    elif lk.endswith('hof'): kind, g = 'Gehöft', 'farmstead'
    else: kind, g = 'Einzelhaus', 'house'
    if e.get('wuestung'): kind, g = 'Wüstung', 'abandoned settlement'
    par = e.get('parents')
    if e.get('gemeinde'): note = 'Eigene Gemeinde (Ortsregister).'
    elif par == ['a. G.']: note = 'Außerhalb des Gemeindeverbandes (Ortsregister).'
    elif par: note = 'Ortsregister: unter ' + ', '.join(par) + '.'
    elif e.get('see'): note = 'Ortsregister: siehe ' + ', '.join(e['see']) + '.'
    else: note = ''
    return ['P', k, kind, f'{k} ({g})', note]

for k in sl:
    if k not in spec and k in reg:
        spec[k] = auto_place(k)
        src[k] = 'auto'

missing = [k for k in sl if k not in spec]

# build decision objects
dec = {}
def mk(k, s):
    code = s[0]
    if code == 'A':
        label, kind, gloss = s[1], s[2], s[3]
        note = s[4] if len(s) > 4 else ''
        d = {'key': k, 'action': 'accept', 'label': label, 'class': 'concept', 'kind': kind, 'gloss_en': gloss}
    elif code == 'M':
        return {'key': k, 'action': 'merge', 'into': s[1]}
    elif code == 'R':
        return {'key': k, 'action': 'reject', 'reason': s[1]}
    elif code == 'P':
        label, kind, gloss = s[1], s[2], s[3]
        note = s[4] if len(s) > 4 else ''
        d = {'key': k, 'action': 'reclass', 'label': label, 'class': 'place', 'kind': kind, 'gloss_en': gloss}
        e = reg.get(k)
        if e is not None:
            pg = reg_pages(e)
            d['in_principality'] = True
            if pg: d['register_page'] = pg[0]
        if k == 'Grauer Affe':
            d['in_principality'] = True
            d['register_page'] = '741'
    elif code == 'N':
        label, kind, gloss = s[1], s[2], s[3]
        note = s[4] if len(s) > 4 else ''
        d = {'key': k, 'action': 'reclass', 'label': label, 'class': 'nature', 'kind': kind, 'gloss_en': gloss}
    elif code == 'X':
        cls, label, kind, gloss = s[1], s[2], s[3], s[4]
        note = s[5] if len(s) > 5 else ''
        d = {'key': k, 'action': 'reclass', 'label': label, 'class': cls, 'kind': kind, 'gloss_en': gloss}
    else:
        raise SystemExit(f'bad code {code} for {k}')
    if note:
        d['note'] = note
    return d

for k, s in spec.items():
    dec[k] = mk(k, s)

# canonicalise: accept/reclass key != label where label is itself a slice key
def full(d): return d['action'] in ('accept', 'reclass')
changed = True
swaps = []
for k in list(dec):
    d = dec[k]
    if not full(d):
        continue
    L = d['label']
    if L == k or L not in SL:
        continue
    t = dec.get(L)
    if t is None:
        nd = dict(d); nd['key'] = L
        dec[L] = nd
        dec[k] = {'key': k, 'action': 'merge', 'into': L}
        swaps.append((k, L, 'new'))
    elif full(t) and t['label'] == L:
        dec[k] = {'key': k, 'action': 'merge', 'into': L}
        swaps.append((k, L, 'merge into existing'))
    elif t['action'] == 'merge' and t['into'] == k:
        nd = dict(d); nd['key'] = L
        dec[L] = nd
        dec[k] = {'key': k, 'action': 'merge', 'into': L}
        swaps.append((k, L, 'swap'))
    else:
        problems.append(f'label clash {k!r} -> label {L!r} which is {t["action"]} {t.get("label")!r}')

# label -> key
lab = collections.OrderedDict()
for k, d in dec.items():
    if full(d):
        lab.setdefault(d['label'], [])
        lab[d['label']].append(k)

def labkey(L):
    ks = lab.get(L)
    if not ks: return None
    return L if L in ks else ks[0]

for k, d in dec.items():
    if d['action'] != 'merge':
        continue
    t = d['into']
    if t in dec and full(dec[t]):
        continue
    if t in dec and dec[t]['action'] == 'merge':
        continue
    if t in dec:
        problems.append(f'merge {k!r} -> {t!r}: target {dec[t]["action"]}')
        continue
    lk = labkey(t)
    if lk:
        d['into'] = lk
    else:
        problems.append(f'merge {k!r} -> {t!r}: target unknown')

# resolve chains
for k, d in dec.items():
    if d['action'] != 'merge': continue
    seen = {k}
    t = d['into']
    while t in dec and dec[t]['action'] == 'merge':
        if t in seen:
            problems.append(f'cycle at {k}')
            break
        seen.add(t)
        t = dec[t]['into']
    d['into'] = t
    if t in dec and dec[t]['action'] == 'reject':
        problems.append(f'merge {k!r} ends at rejected {t!r}')

out = {'package': 'E8', 'group': 'concepts', 'decisions': [dec[k] for k in sl if k in dec]}
if '--write' in sys.argv:
    json.dump(out, open(ROOT + 'data/entities/decisions/E8.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('decided', len(dec), 'of', len(sl))
print('missing', len(missing))
for m in missing[:400]:
    print('  MISSING', m)
for p in problems:
    print('  PROBLEM', p)
print('swaps', len(swaps))
acts = collections.Counter(d['action'] for d in dec.values())
print(acts)
