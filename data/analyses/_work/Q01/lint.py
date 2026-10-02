"""Q01: text linter over all analyses (prose fields only)."""
import json, glob, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]

BRIT = re.compile(r"\b(metres?|kilometres?|centimetres?|millimetres?|colours?|coloured|centres?|centred|neighbou?r\w*|labou?r\w*|favou?r\w*|honou?r\w*|behaviou?r\w*|organis\w+|analys(?:e|ed|es|ing)\b|recognis\w+|categoris\w+|summaris\w+|emphasis(?:e|ed)\b|grey|programme\w*|defence|licence|whilst|per cent|artefact\w*|catalogue\w*|judgement|ageing|plough\w*|tonnes?|mould\w*|travell\w+|cancell\w+|modell\w+|labell\w+|signall\w+|fuelled|storey|sceptic\w*|manoeuvr\w+|oesophag\w+|mediaeval|sulphur|aluminium|harbour\w*|rumour\w*|vigour|glamour|savour\w*|endeavour\w*|utilis\w+|normalis\w+|standardis\w+|characteris\w+|generalis\w+|specialis\w+|minimis\w+|maximis\w+|visualis\w+|realis\w+|criticis\w+|apologis\w+|prioritis\w+|stabilis\w+|capitalis\w+|industrialis\w+|urbanis\w+|colonis\w+|civilis\w+|localis\w+|mobilis\w+|digitis\w+|romanis\w+|germanis\w+|sorbian)\b", re.I)
OLD = re.compile(r"(?<![»\"“‚'])\b(\w*(?:[Tt]heil\w*|[Tt]hal(?!er)\w*|[Tt]haler\w*|Thlr\w*|[Pp]rocent\w*|[Cc]entner\w*|[Cc]ubik\w*|[Cc]onto\w*|Fürstenthum\w*|Landestheil\w*|Landtheil\w*|Todt\w*|todt\w*|Wirthschaft\w*|wirthschaft\w*|Gränz\w*|[Ss]eit\b|Rath\b|Räthe\w*|Gemeinderäth\w*|Cultur\w*|Classe\w*|Kirchen-?[Vv]isit\w*|Mühle\w*Thal|Gewerbtreib\w*|Betrieb?e\b)\w*)")

def walk_strings(d):
    """yield (path, lang, text) for prose fields."""
    def bi(path, n):
        if isinstance(n, dict) and 'de' in n and 'en' in n:
            yield path, 'de', n['de']; yield path, 'en', n['en']
    yield from bi('title', d['title'])
    yield from bi('summary', d['summary'])
    yield from bi('method', d['method'])
    for i, f in enumerate(d['findings']): yield from bi(f'findings[{i}]', f)
    for i, f in enumerate(d.get('caveats', [])): yield from bi(f'caveats[{i}]', f)
    for i, c in enumerate(d['charts']):
        yield from bi(f'charts[{i}].title', c['title']); yield from bi(f'charts[{i}].caption', c['caption'])
    for lang in ('de', 'en'):
        for i, k in enumerate(d['keywords'][lang]): yield f'kw[{i}]', lang, k
    for ds in d['datasets']:
        yield from bi(f"ds {ds['name']}.title", ds['title'])
        for c in ds['columns']: yield from bi(f"col {ds['name']}.{c['name']}", c['label'])

def lint(d, which):
    out = []
    for path, lang, t in walk_strings(d):
        if lang == 'en':
            if 'brit' in which:
                for m in BRIT.finditer(t): out.append((path, 'BRIT', m.group(0)))
            if 'dec' in which:
                for m in re.finditer(r"(?<![\d.,])\d{1,3},\d{1,2}(?![\d,])", t): out.append((path, 'EN-comma-decimal', t[max(0,m.start()-25):m.end()+15]))
        else:
            if 'dec' in which:
                for m in re.finditer(r"(?<![\d.,])\d+\.\d{1,2}(?![\d.])", t):
                    ctx = t[max(0,m.start()-3):m.end()+3]
                    out.append((path, 'DE-point-decimal', t[max(0,m.start()-25):m.end()+15]))
            if 'old' in which:
                for m in OLD.finditer(t): out.append((path, 'OLD', m.group(1)))
    return out

if __name__ == '__main__':
    which = set(sys.argv[1].split(',')) if len(sys.argv) > 1 else {'brit', 'dec', 'old'}
    pat = sys.argv[2] if len(sys.argv) > 2 else '*'
    import collections
    cnt = collections.Counter()
    for f in sorted(glob.glob(str(ROOT/'data'/'analyses'/f'{pat}.json'))):
        d = json.load(open(f, encoding='utf-8'))
        for path, kind, ex in lint(d, which):
            cnt[(kind, ex.lower() if kind in ('BRIT','OLD') else '')] += 1
            if '-v' in sys.argv or True:
                print(d['id'][:48].ljust(48), path.ljust(22), kind, '|', ex)
    print(cnt.most_common(60))
