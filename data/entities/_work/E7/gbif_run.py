import json, sys, time
sys.path.insert(0, r'C:\Users\totom\Projects\reuss-edition\tools')
import gbif_match
from pathlib import Path
W = Path(r'C:\Users\totom\Projects\reuss-edition\data\entities\_work\E7')
cache_p = W/'gbif_cache_E7.json'
cache = json.loads(cache_p.read_text(encoding='utf-8')) if cache_p.exists() else {}
names = [l.strip() for l in (W/'sci_names.txt').read_text(encoding='utf-8').splitlines() if l.strip()]
t=time.time()
for i,n in enumerate(names):
    if n in cache and 'error' not in cache[n]:
        continue
    r = gbif_match.match(n, cache)
    cache[n] = r
    if i % 50 == 0:
        cache_p.write_text(json.dumps(cache, ensure_ascii=False), encoding='utf-8')
        print(i, round(time.time()-t), flush=True)
cache_p.write_text(json.dumps(cache, ensure_ascii=False), encoding='utf-8')
print('done', len(cache))
