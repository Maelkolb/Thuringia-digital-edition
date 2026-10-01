import json, re, sys
from pathlib import Path
ROOT = Path(r'C:\Users\totom\Projects\reuss-edition')
W = ROOT/'data'/'entities'/'_work'/'E7'
CANDS = json.load(open(ROOT/'data'/'entities'/'candidates'/'organisms.json', encoding='utf-8'))['entries']
KEYS = [e['key'] for e in CANDS]
KEYSET = set(KEYS)
BYKEY = {e['key']: e for e in CANDS}

def rk(k):
    k = k.strip()
    if k.startswith('#'):
        return KEYS[int(k[1:])]
    if k not in KEYSET:
        raise KeyError(f'unknown key {k!r}')
    return k

RANKS = {'genus','family','order','class','suborder','subfamily','phylum','kingdom','subphylum','subclass','species','subspecies'}

def split_sci(s):
    s = (s or '').strip()
    if not s:
        return None, None
    m = re.match(r'^(.*?)\s*\[(\w+)\]$', s)
    if m:
        return m.group(1).strip(), m.group(2)
    return s, ('species' if ' ' in s else 'genus')

ERRORS = []

def parse_all(files):
    """returns decisions dict key -> decision (no gbif yet)"""
    dec = {}
    def put(k, d, src):
        if k in dec:
            raise ValueError(f'duplicate decision for {k!r} ({src}); existing {dec[k]}')
        dec[k] = d
    merges = []
    for fn in files:
        for ln, line in enumerate((W/fn).read_text(encoding='utf-8').split('\n'), 1):
            line = line.rstrip('\r')
            if not line.strip() or line.startswith('#') :
                if line.startswith('#') and not re.match(r'^#\d', line):
                    continue
            if not line.strip() or (line.startswith('# ') or line=='#'):
                continue
            p = line.split('|')
            t = p[0]
            src = f'{fn}:{ln}'
            try:
                if t in ('T', 'P', 'F'):
                    p += [''] * (7 - len(p))
                    key = rk(p[1]); label = p[2]; sci, rank = split_sci(p[3])
                    d = {'key': key, 'action': 'accept', 'label': label, 'class': 'organism',
                         'kind': {'T': 'Tier', 'P': 'Pflanze', 'F': 'Pilz'}[t]}
                    if sci:
                        d['scientific'] = sci; d['rank'] = rank
                    if p[4].strip(): d['gloss_en'] = p[4].strip()
                    if p[5].strip(): d['note'] = p[5].strip()
                    if p[6].strip(): d['modern'] = p[6].strip()
                    put(key, d, src)
                elif t == 'M':
                    into = rk(p[1])
                    for k in p[2].split('~'):
                        k = rk(k)
                        put(k, {'key': k, 'action': 'merge', 'into': into}, src)
                        merges.append((k, into, src))
                elif t == 'R':
                    key = rk(p[1])
                    put(key, {'key': key, 'action': 'reject', 'reason': p[2]}, src)
                elif t == 'C':
                    p += [''] * (7 - len(p))
                    key = rk(p[1])
                    d = {'key': key, 'action': 'reclass', 'class': p[2], 'label': p[3], 'kind': p[4]}
                    if p[5].strip(): d['gloss_en'] = p[5].strip()
                    if p[6].strip(): d['note'] = p[6].strip()
                    put(key, d, src)
                elif t.startswith('EOF') or t == '':
                    pass
                else:
                    raise ValueError(f'bad line type {t!r}')
            except Exception as e:
                ERRORS.append((src, line[:100], str(e)))
    return dec
