import urllib.request, urllib.parse, json, time, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'wd.json')
UA = {"User-Agent": "reuss-edition/1.0 (scholarly digital edition; contact: edition maintainer)"}
terms = ["Elbe", "Main Fluss", "Fichtelgebirge", "Frankenwald", "Thüringer Wald", "Erzgebirge", "Harz", "Donau", "Unstrut", "Pleiße", "Orla Fluss", "Wisenta", "Selbitz Saale", "Weida Fluss"]
try:
    cache = json.load(open(OUT, encoding='utf-8'))
except Exception:
    cache = {}
for t in terms:
    if t in cache and cache[t] and 'error' not in cache[t][0]:
        continue
    url = "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode(
        {"action": "wbsearchentities", "search": t, "language": "de", "uselang": "de", "format": "json", "limit": 5})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                d = json.loads(r.read().decode('utf-8'))
            cache[t] = [{"id": h["id"], "label": h.get("label"), "description": h.get("description")} for h in d.get("search", [])]
            break
        except Exception as e:
            cache[t] = [{"error": repr(e)}]
            time.sleep(30 * (attempt + 1))
    json.dump(cache, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    time.sleep(10)
print('done')
