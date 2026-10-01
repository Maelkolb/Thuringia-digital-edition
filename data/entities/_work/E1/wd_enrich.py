"""Verify Wikidata ids for accepted places by name + coordinates (P625 within tolerance)."""
import json, math, re, sys, time, urllib.parse, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(r'C:\Users\totom\Projects\reuss-edition')
WORK = ROOT / 'data' / 'entities' / '_work' / 'E1'
CACHE = WORK / 'wd_cache.json'
UA = {"User-Agent": "reuss-edition/1.0 (scholarly digital edition; entity adjudication)"}
cache = json.loads(CACHE.read_text(encoding='utf-8')) if CACHE.exists() else {'search': {}, 'ent': {}}


def get(url):
    wait = 3
    for a in range(8):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:  # noqa
            ra = e.headers.get('Retry-After') if e.headers else None
            time.sleep(min(90, int(ra)) if ra and ra.isdigit() else wait)
            wait = min(90, wait * 2)
        except Exception as e:  # noqa
            time.sleep(wait)
            wait = min(90, wait * 2)
    return None


def search(term):
    k = term
    if k in cache['search']:
        return cache['search'][k]
    d = get("https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode(
        {"action": "wbsearchentities", "search": term, "language": "de", "uselang": "de", "format": "json", "limit": 7}))
    if d is None:
        return []
    hits = [h['id'] for h in d.get('search', [])]
    cache['search'][k] = hits
    time.sleep(1.0)
    return hits


def entities(ids):
    need = [i for i in ids if i not in cache['ent']]
    for i in range(0, len(need), 40):
        chunk = need[i:i + 40]
        d = get("https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode(
            {"action": "wbgetentities", "ids": '|'.join(chunk), "props": "labels|descriptions|claims", "languages": "de|en", "format": "json"}))
        if d is None:
            continue
        for q in chunk:
            e = (d or {}).get('entities', {}).get(q)
            if not e:
                cache['ent'][q] = None
                continue
            coords = None
            cl = e.get('claims', {}).get('P625')
            if cl:
                v = cl[0]['mainsnak'].get('datavalue', {}).get('value')
                if v:
                    coords = [v['latitude'], v['longitude']]
            p31 = [c['mainsnak']['datavalue']['value']['id'] for c in e.get('claims', {}).get('P31', [])
                   if c['mainsnak'].get('datavalue')]
            cache['ent'][q] = {'label': e.get('labels', {}).get('de', {}).get('value') or e.get('labels', {}).get('en', {}).get('value'),
                               'desc': e.get('descriptions', {}).get('de', {}).get('value') or e.get('descriptions', {}).get('en', {}).get('value'),
                               'coords': coords, 'p31': p31}
        time.sleep(1.0)
    return {i: cache['ent'].get(i) for i in ids}


def hav(la1, lo1, la2, lo2):
    R = 6371; p = math.pi / 180
    d = math.sin((la2 - la1) * p / 2) ** 2 + math.cos(la1 * p) * math.cos(la2 * p) * math.sin((lo2 - lo1) * p / 2) ** 2
    return 2 * R * math.asin(math.sqrt(d))


def norm(s):
    s = s.lower()
    s = re.sub(r'\(.*?\)', '', s)
    s = re.sub(r'^(bad|stadt|kreisfreie stadt)\s+', '', s)
    s = s.replace('ß', 'ss').replace('/vogtl.', '').replace('/elster', '').replace('-', '').replace(' ', '')
    return s.strip()


def main():
    dec = json.loads((ROOT / 'data' / 'entities' / 'decisions' / 'E1.json').read_text(encoding='utf-8'))['decisions']
    skip = {'Flur','Haus','Platz','Straße','Gehöft','Hütte','Hammer','Mühle','Wüstung','Gewerbeanlage','Jagdhaus','Gasthaus','Gasthof','Landsitz','Stadtteil','Kammergut','Vorwerk'}
    todo = [d for d in dec if d['action'] in ('accept', 'reclass') and d.get('class') == 'place' and 'lat' in d and d['kind'] not in skip]
    pri = {'Stadt', 'Marktflecken', 'Burg', 'Herrschaft', 'Land', 'Region', 'Amt', 'Fürstentum', 'Herzogtum', 'Königreich', 'Großherzogtum', 'Landgrafschaft', 'Kontinent'}
    todo.sort(key=lambda d: (0 if d['kind'] in pri else 1))
    import os
    todo = todo[:int(os.environ.get('LIMIT', '150'))]
    res = {}
    wa = WORK / 'wd_auto.json'
    if wa.exists():
        res = json.loads(wa.read_text(encoding='utf-8'))
    for n, d in enumerate(todo):
        if d['key'] in res:
            continue
        names = []
        for nm in (d.get('modern'), d['label']):
            if nm and nm not in names:
                names.append(nm)
        tried = []
        best = None
        for nm in names:
            term = re.sub(r'\s*\(.*?\)', '', nm).strip()
            ids = search(term)
            ents = entities(ids)
            for q in ids:
                e = ents.get(q)
                if not e or not e['coords'] or not e['label']:
                    continue
                dist = hav(d['lat'], d['lon'], e['coords'][0], e['coords'][1])
                ln = norm(e['label'])
                cands = {norm(x) for x in names} | {norm(term)}
                if dist <= 6 and (ln in cands or any(ln.startswith(c) or c.startswith(ln) for c in cands if len(c) > 3)):
                    pen = 2.5 if (e['desc'] or '').lower().startswith(('siedlung', 'ortsteil', 'wüstung')) else 0
                    if best is None or dist + pen < best[0]:
                        best = (dist + pen, q, e['label'], e['desc'])
            if best:
                break
        res[d['key']] = best
        wa.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
        CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding='utf-8')
        if (n + 1) % 25 == 0:
            CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding='utf-8')
            print(n + 1, len(todo), file=sys.stderr)
    CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding='utf-8')
    out = {k: v for k, v in res.items()}
    (WORK / 'wd_auto.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    ok = sum(1 for v in out.values() if v)
    print('matched', ok, 'of', len(out))


main()
