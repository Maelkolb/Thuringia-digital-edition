import json, time, urllib.parse, urllib.request
from pathlib import Path
W = Path(r'C:\Users\totom\Projects\reuss-edition\data\entities\_work\E7')
c2 = json.load(open(W/'gbif_cache2_E7.json', encoding='utf-8'))
BB = 'd7dddbf4-2cf0-4f39-9b2a-bb099caae36c'
HINTS = {'Columba': {'family': 'Columbidae'}, 'Crocuta': {'family': 'Hyaenidae'}, 'Cygnus': {'family': 'Anatidae'},
         'Panthera': {'family': 'Felidae'}, 'Triton palustris': {'family': 'Salamandridae'}, 'Lemna': {'family': 'Araceae'},
         'Balea fragilis': {'family': 'Clausiliidae'}, 'Balea perversa': {'family': 'Clausiliidae'}}
def call(url):
    for a in range(4):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception:
            time.sleep(2*(a+1))
    return {'error': 'failed'}
def clean(r, rank):
    rk = (r.get('rank') or '').lower()
    if r.get('matchType') == 'EXACT' and rk == rank: return True
    if r.get('matchType') == 'HIGHERRANK' and rk == rank and rank != 'species': return True
    return False
out = {}
for key, r in c2.items():
    sci, king, rank = key.split('|')
    if clean(r, rank): continue
    res = dict(r)
    if sci in HINTS:
        q = {'name': sci, 'kingdom': king, 'verbose': 'false', **HINTS[sci]}
        d = call('https://api.gbif.org/v1/species/match?' + urllib.parse.urlencode(q))
        res = {k: d.get(k) for k in ('usageKey','scientificName','canonicalName','rank','status','matchType','confidence','acceptedUsageKey','note')}
        res['via'] = 'match+hint'
        if res.get('acceptedUsageKey'):
            a = call(f"https://api.gbif.org/v1/species/{res['acceptedUsageKey']}"); res['acceptedName'] = a.get('canonicalName')
    if not clean(res, rank) and rank != 'species':
        q = {'q': sci, 'rank': rank.upper(), 'datasetKey': BB, 'status': 'ACCEPTED', 'limit': 25}
        d = call('https://api.gbif.org/v1/species/search?' + urllib.parse.urlencode(q))
        hits = [x for x in d.get('results', []) if (x.get('canonicalName') or '').lower() == sci.lower() and (x.get('rank') or '').lower() == rank and x.get('kingdom') == king]
        res = dict(res); res['search_hits'] = [(h.get('nubKey'), h.get('key'), h.get('canonicalName'), h.get('rank'), h.get('kingdom')) for h in hits]
        if len(hits) >= 1 and hits[0].get('nubKey'):
            res.update({'usageKey': hits[0]['nubKey'], 'rank': hits[0]['rank'], 'matchType': 'EXACT', 'status': 'ACCEPTED', 'via': 'search'})
    out[key] = res
json.dump(out, open(W/'gbif_cache3_E7.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
for k, r in out.items():
    sci, king, rank = k.split('|')
    print(f"{sci} [{rank}] -> {r.get('canonicalName') or r.get('scientificName')} {r.get('rank')} {r.get('matchType')} {r.get('usageKey')} via={r.get('via')} hits={r.get('search_hits')}")
