import json, sys, time, urllib.parse, urllib.request
from pathlib import Path
W = Path(r'C:\Users\totom\Projects\reuss-edition\data\entities\_work\E7')
dec = json.load(open(W/'dec_raw.json', encoding='utf-8'))
cache_p = W/'gbif_cache2_E7.json'
cache = json.loads(cache_p.read_text(encoding='utf-8')) if cache_p.exists() else {}
KING = {'Tier': 'Animalia', 'Pflanze': 'Plantae', 'Pilz': 'Fungi'}
def call(url):
    for a in range(4):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception as e:
            time.sleep(2*(a+1))
    return {'error': 'failed'}
triples = {}
overrides = json.load(open(W/'gbif_overrides.json', encoding='utf-8')) if (W/'gbif_overrides.json').exists() else {}
for d in dec.values():
    if d.get('scientific'):
        sci = overrides.get(d['scientific'], d['scientific'])
        triples[(sci, d['rank'], KING[d['kind']])] = 1
t = time.time()
for i, (sci, rank, king) in enumerate(sorted(triples)):
    key = f'{sci}|{king}|{rank}'
    if key in cache and 'error' not in cache[key]:
        continue
    q = {'name': sci, 'kingdom': king, 'verbose': 'false'}
    if rank not in ('species',):
        q['rank'] = rank.upper()
    d = call('https://api.gbif.org/v1/species/match?' + urllib.parse.urlencode(q))
    out = {k: d.get(k) for k in ('usageKey', 'scientificName', 'canonicalName', 'rank', 'status', 'matchType', 'confidence', 'acceptedUsageKey', 'note')}
    out['query'] = sci
    if out.get('acceptedUsageKey'):
        a = call(f"https://api.gbif.org/v1/species/{out['acceptedUsageKey']}")
        out['acceptedName'] = a.get('canonicalName') or a.get('scientificName')
        out['acceptedRank'] = a.get('rank')
    cache[key] = out
    if i % 60 == 0:
        cache_p.write_text(json.dumps(cache, ensure_ascii=False), encoding='utf-8'); print(i, round(time.time()-t), flush=True)
cache_p.write_text(json.dumps(cache, ensure_ascii=False), encoding='utf-8')
print('done', len(cache))
