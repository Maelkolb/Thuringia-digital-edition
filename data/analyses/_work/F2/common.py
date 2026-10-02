import json, sys, math, statistics, subprocess, copy
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(r'C:\Users\totom\Projects\reuss-edition')
ARCH = ROOT / 'data' / 'analyses' / '_archive'
SHARED = ROOT / 'data' / 'analyses' / '_shared'
OUT = ROOT / 'data' / 'analyses'


def load(aid):
    return json.load(open(ARCH / f'{aid}.json', encoding='utf-8'))


def ds(arch, name):
    for d in arch['datasets']:
        if d['name'] == name:
            return copy.deepcopy(d)
    raise KeyError(name)


def rows(d):
    names = [c['name'] for c in d['columns']]
    return [dict(zip(names, r)) for r in d['rows']]


def bi(de, en):
    return {'de': de, 'en': en}


def de_num(x, nd=1):
    """German decimal format for text."""
    s = f'{x:.{nd}f}'.replace('.', ',')
    return s.replace('-', '\u2212')


def en_num(x, nd=1):
    return f'{x:.{nd}f}'.replace('-', '\u2212')


def words(s):
    return len(s.split())


def write_feature(f):
    p = OUT / f"{f['id']}.json"
    json.dump(f, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return p


def validate(fid):
    r = subprocess.run(['node', 'tools/validate_analysis.mjs', f'data/analyses/{fid}.json'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    print(r.stdout)
    print(r.stderr[-2000:])


def month_axis_expr():
    return bi("['Jan','Feb','Mär','Apr','Mai','Jun','Jul','Aug','Sep','Okt','Nov','Dez'][datum.value-1]",
              "['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][datum.value-1]")
