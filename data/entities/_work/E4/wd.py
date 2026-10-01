import json, sys, urllib.request, time
UA = {"User-Agent": "reuss-edition/1.0 (scholarly digital edition; contact: edition maintainer)"}
def ent(q):
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{q}.json"
    for a in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                d = json.loads(r.read().decode('utf-8'))
            break
        except Exception as e:
            time.sleep(2)
    else:
        return None
    e = d['entities'][q]
    def val(p):
        cl = e['claims'].get(p, [])
        out = []
        for c in cl:
            v = c['mainsnak'].get('datavalue', {}).get('value')
            if isinstance(v, dict) and 'time' in v: out.append(v['time'])
            elif isinstance(v, dict) and 'id' in v: out.append(v['id'])
            else: out.append(v)
        return out
    return {'id': q, 'label_de': e['labels'].get('de', {}).get('value'), 'label_en': e['labels'].get('en', {}).get('value'),
            'desc_de': e['descriptions'].get('de', {}).get('value'), 'desc_en': e['descriptions'].get('en', {}).get('value'),
            'birth': val('P569'), 'death': val('P570'), 'father': val('P22'), 'instance': val('P31')}
if __name__ == '__main__':
    for q in sys.argv[1:]:
        print(json.dumps(ent(q), ensure_ascii=False)); time.sleep(0.3)
