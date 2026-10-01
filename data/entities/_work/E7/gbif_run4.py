import json, time, urllib.parse, urllib.request
from pathlib import Path
W = Path(r'C:\Users\totom\Projects\reuss-edition\data\entities\_work\E7')
ALT = {
 'Ribes grossularia': ('Ribes uva-crispa', 'Plantae'),
 'Rosa pimpinellifolia': ('Rosa spinosissima', 'Plantae'),
 'Ledum palustre': ('Rhododendron tomentosum', 'Plantae'),
 'Orchis sambucina': ('Dactylorhiza sambucina', 'Plantae'),
 'Linaria elatine': ('Kickxia elatine', 'Plantae'),
 'Scirpus ovatus': ('Eleocharis ovata', 'Plantae'),
 'Arabis arenosa': ('Arabidopsis arenosa', 'Plantae'),
 'Arabis halleri': ('Arabidopsis halleri', 'Plantae'),
 'Gentiana ciliata': ('Gentianopsis ciliata', 'Plantae'),
 'Cotoneaster vulgaris': ('Cotoneaster integerrimus', 'Plantae'),
 'Trifolium ochroleucum': ('Trifolium ochroleucon', 'Plantae'),
 'Cephalanthera pallens': ('Cephalanthera damasonium', 'Plantae'),
 'Lithospermum purpureo-coeruleum': ('Buglossoides purpurocaerulea', 'Plantae'),
 'Ranunculus philonotis': ('Ranunculus sardous', 'Plantae'),
 'Prunus dulcis': ('Prunus amygdalus', 'Plantae'),
 'Apocynum venetum': ('Apocynum venetum L.', 'Plantae'),
 'Balea fragilis': ('Balea perversa', 'Animalia'),
 'Triton palustris': ('Lissotriton vulgaris', 'Animalia'),
}
def call(url):
    for a in range(4):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception:
            time.sleep(2*(a+1))
    return {'error': 'failed'}
out = {}
for orig, (alt, king) in ALT.items():
    d = call('https://api.gbif.org/v1/species/match?' + urllib.parse.urlencode({'name': alt, 'kingdom': king, 'verbose': 'false'}))
    r = {k: d.get(k) for k in ('usageKey','scientificName','canonicalName','rank','status','matchType','confidence','acceptedUsageKey')}
    r['alt'] = alt
    out[orig] = r
    print(orig, '->', alt, '|', r['canonicalName'], r['rank'], r['status'], r['matchType'], r['usageKey'], r['acceptedUsageKey'])
json.dump(out, open(W/'gbif_cache4_E7.json', 'w', encoding='utf-8'), ensure_ascii=False)
