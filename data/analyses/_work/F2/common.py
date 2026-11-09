import json, sys, math, statistics, subprocess, copy, re
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


def english_quotes(node):
    """English texts use English quotation marks; the German guillemets stay in the German texts."""
    if isinstance(node, dict):
        if set(node) == {'de', 'en'} and isinstance(node['en'], str):
            node['en'] = node['en'].replace('»', '“').replace('«', '”')
            return
        for k, v in node.items():
            if k != 'rows':
                english_quotes(v)
    elif isinstance(node, list):
        for v in node:
            english_quotes(v)


BRITISH_SPELLING = {
    'meter': 'metre', 'meters': 'metres', 'kilometer': 'kilometre', 'kilometers': 'kilometres',
    'millimeter': 'millimetre', 'millimeters': 'millimetres', 'centimeter': 'centimetre', 'centimeters': 'centimetres',
    'color': 'colour', 'colors': 'colours', 'colored': 'coloured', 'gray': 'grey',
    'neighbor': 'neighbour', 'neighbors': 'neighbours', 'neighboring': 'neighbouring',
    'labeled': 'labelled', 'labeling': 'labelling', 'meager': 'meagre', 'center': 'centre',
    'normalized': 'normalised', 'criticize': 'criticise', 'criticizes': 'criticises', 'criticized': 'criticised',
    'analyze': 'analyse', 'analyzes': 'analyses', 'digitized': 'digitised',
}
_BRITISH_RE = re.compile(r'\b(' + '|'.join(BRITISH_SPELLING) + r')\b', re.IGNORECASE)


def _british_word(m):
    word = m.group(0)
    new = BRITISH_SPELLING[word.lower()]
    return new[0].upper() + new[1:] if word[0].isupper() else new


def british_english(node):
    """The edition writes British English; this fixes the spelling of every English text before writing."""
    if isinstance(node, dict):
        if set(node) == {'de', 'en'} and isinstance(node['en'], str):
            node['en'] = _BRITISH_RE.sub(_british_word, node['en'])
            return
        for k, v in node.items():
            if k != 'rows':
                british_english(v)
    elif isinstance(node, list):
        for v in node:
            british_english(v)


def write_feature(f):
    english_quotes(f)
    british_english(f)
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
