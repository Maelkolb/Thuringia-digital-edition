"""Python port of site_src/static/js/search.js ranking, for debugging expansions (not for grading)."""
import json, sys, math, re, io
sys.path.insert(0, r'C:\Users\totom\Projects\reuss-edition\pipeline\site')
from norm import fold, norm, tokens
BASE = r'C:\Users\totom\Projects\reuss-edition\site\suche'
D = json.load(open(BASE + r'\docs.json', encoding='utf-8'))
V = json.load(open(BASE + r'\vocab.json', encoding='utf-8'))
SYN = json.load(open(BASE + r'\syn.json', encoding='utf-8'))
VI = {t: i for i, t in enumerate(V['t'])}
_sh = {}
def shard(term):
    t = fold(term); k = t[:2] if len(t) >= 2 else t + '_'
    return ''.join(c if c.isalnum() else '_' for c in k)
def postings(term):
    s = shard(term)
    if s not in _sh:
        try: _sh[s] = json.load(open(BASE + r'\i\%s.json' % s, encoding='utf-8'))
        except Exception: _sh[s] = {}
    return _sh[s].get(term, [])
def lev(a, b, mx):
    if abs(len(a) - len(b)) > mx: return mx + 1
    prev = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        cur = [i]; best = i
        for j in range(1, len(b) + 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] != b[j - 1])))
            best = min(best, cur[j])
        if best > mx: return mx + 1
        prev = cur
    return prev[-1]
def expand(word, is_last):
    n = norm(word); out = []
    if n in VI: out.append((n, 1, 'exact'))
    for s in SYN.get(n, []):
        if s in VI: out.append((s, .8, 'syn'))
    if n.isdigit(): return out
    f = fold(word)
    exact_df = V['df'][VI[n]] if n in VI else 0
    if is_last and len(f) >= 3 and exact_df < 5:
        c = 0
        for t in V['t']:
            if c >= 12: break
            if t != n and t.startswith(n if len(f) > 5 else f): out.append((t, .35, 'prefix')); c += 1
    if not out and len(n) >= 4:
        mx = 2 if len(n) >= 8 else 1; cands = []
        for k, tt in enumerate(V['t']):
            if abs(len(tt) - len(n)) > mx or tt[0] != n[0]: continue
            d = lev(n, tt, mx)
            if d <= mx: cands.append((d, -V['df'][k], tt))
        cands.sort()
        for d, _, tt in cands[:5]: out.append((tt, .5, 'fuzzy'))
    return out
def parse(q):
    phrases = []; excl = []; words = []
    def rep(m): phrases.append(m.group(1)); return ' ' + m.group(1) + ' '
    q = re.sub(r'[„“"”]([^„“"”]+)[„“"”]', rep, q)
    for w in q.split():
        if w[0] == '-' and len(w) > 1:
            for t in tokens(w[1:]): excl.append(norm(t))
            continue
        for t in tokens(w): words.append(t)
    return words, phrases, excl
def search(q, show=True, top=10):
    words, phrases, excl = parse(q)
    groups = [expand(w, i == len(words) - 1) for i, w in enumerate(words)]
    N = len(D['docs']); scores = {}; matched = {}
    for gi, g in enumerate(groups):
        for t, w, kind in g:
            p = postings(t); df = len(p) / 2; idf = math.log(1 + (N - df + .5) / (df + .5))
            for i in range(0, len(p), 2):
                di, tf = p[i], p[i + 1]; doc = D['docs'][di]
                s = idf * (tf * 2.2) / (tf + 1.2 * (1 - .75 + .75 * doc[4] / D['avgLen'])) * w * D['weights'].get(doc[0], 1)
                scores[di] = scores.get(di, 0) + s; matched.setdefault(di, set()).add(gi)
    ex = set()
    for t in excl:
        p = postings(t)
        for i in range(0, len(p), 2): ex.add(p[i])
    need = sum(1 for g in groups if g)
    ids = [d for d in scores if d not in ex]
    andids = [d for d in ids if len(matched[d]) >= need]
    mode = 'and'
    if not andids and need > 1: mode = 'or'
    else: ids = andids
    res = sorted(ids, key=lambda d: -scores[d])
    if show:
        print('Q:', q, '| groups:', [[(t, kind) for t, w, kind in g][:8] for g in groups], '| hits', len(res), mode)
        for d in res[:top]:
            doc = D['docs'][d]; print('   ', round(scores[d], 2), doc[0], doc[1], doc[2], doc[5][:40])
    return res, groups, mode
if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    for q in sys.argv[1:]: search(q)
