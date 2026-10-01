"""Manual-assisted Wikidata lookup for states/regions: top hits must match a description regex; results shown for review."""
import json, re, sys, time, urllib.parse, urllib.request, urllib.error
from pathlib import Path

WORK = Path(r'C:\Users\totom\Projects\reuss-edition\data\entities\_work\E1')
UA = {"User-Agent": "reuss-edition/1.0 (scholarly digital edition; entity adjudication)"}
OUT = WORK / 'wd_manual_raw.json'
res = json.loads(OUT.read_text(encoding='utf-8')) if OUT.exists() else {}

# key -> (search term, regex the description (de) must match)
TERMS = {
    'Deutschland': ('Deutschland', r'Staat in Mitteleuropa'),
    'Bayern': ('Königreich Bayern', r'Königreich'),
    'Böhmen': ('Böhmen', r'(historisches )?Land|Region|Landesteil'),
    'Frankreich': ('Frankreich', r'Staat in (West)?[Ee]uropa'),
    'Italien': ('Italien', r'Staat in'),
    'Belgien': ('Belgien', r'Staat in'),
    'Dänemark': ('Dänemark', r'Staat in|Königreich'),
    'Brasilien': ('Brasilien', r'Staat in'),
    'Kanada': ('Kanada', r'Staat in'),
    'Europa': ('Europa', r'Kontinent'),
    'Asien': ('Asien', r'Kontinent'),
    'Königreich Sachsen': ('Königreich Sachsen', r'Königreich'),
    'Kursachsen': ('Kurfürstentum Sachsen', r'Kurfürstentum|Kurland'),
    'Herzogthum S.-Altenburg': ('Herzogtum Sachsen-Altenburg', r'Herzogtum'),
    'Herzogthum S.-Meiningen': ('Herzogtum Sachsen-Meiningen', r'Herzogtum'),
    'Herzogthum S.-Koburg': ('Herzogtum Sachsen-Coburg und Gotha', r'Herzogtum'),
    'Großherzogthum S.-Weimar': ('Großherzogtum Sachsen-Weimar-Eisenach', r'Großherzogtum'),
    'Fürstenthum Schwarzburg-Rudolstadt': ('Fürstentum Schwarzburg-Rudolstadt', r'Fürstentum'),
    'Fürstenthum Schwarzburg-Sondershausen': ('Fürstentum Schwarzburg-Sondershausen', r'Fürstentum'),
    'Herzogthum Anhalt': ('Herzogtum Anhalt', r'Herzogtum'),
    'Fürstenthum Lippe-Detmold': ('Fürstentum Lippe', r'Fürstentum'),
    'Fürstenthum Schaumburg-Lippe': ('Fürstentum Schaumburg-Lippe', r'Fürstentum'),
    'Fürstenthum Waldeck': ('Fürstentum Waldeck', r'Fürstentum'),
    'Großherzogthum Mecklenburg-Schwerin': ('Großherzogtum Mecklenburg-Schwerin', r'Großherzogtum'),
    'Großherzogthum Mecklenburg-Strelitz': ('Großherzogtum Mecklenburg-Strelitz', r'Großherzogtum'),
    'Großherzogthum Baden': ('Großherzogtum Baden', r'Großherzogtum'),
    'Fürstenthum Reuß j. L': ('Reuß jüngerer Linie', r'Fürstentum|Staat'),
    'Fürstenthum Reuß ä. L': ('Reuß älterer Linie', r'Fürstentum|Staat'),
    'Hannover': ('Königreich Hannover', r'Königreich'),
    'Holstein': ('Holstein', r'Region|Landesteil|Landschaft|historisch'),
    'Kärnten': ('Herzogtum Kärnten', r'Herzogtum'),
    'Flandern': ('Flandern', r'Region|Landschaft|historisch'),
    'Hessen-Cassel': ('Landgrafschaft Hessen-Kassel', r'Landgrafschaft'),
    'Hessen-Homburg': ('Landgrafschaft Hessen-Homburg', r'Landgrafschaft'),
    'Brandenburg-Baireuth': ('Markgrafschaft Brandenburg-Bayreuth', r'Markgrafschaft|Fürstentum'),
    'Franken': ('Franken', r'Region|Landschaft|historisch|Kulturraum'),
    'Brandenburg': ('Mark Brandenburg', r'Mark|Land|Kurfürstentum|historisch'),
}


def get(url):
    wait = 4
    for a in range(10):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            ra = e.headers.get('Retry-After') if e.headers else None
            time.sleep(min(90, int(ra)) if ra and ra.isdigit() else wait)
            wait = min(90, wait * 2)
        except Exception:
            time.sleep(wait)
            wait = min(90, wait * 2)
    return None


for k, (term, rx) in TERMS.items():
    if k in res:
        continue
    d = get("https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode(
        {"action": "wbsearchentities", "search": term, "language": "de", "uselang": "de", "format": "json", "limit": 6}))
    if d is None:
        continue
    hits = [(h['id'], h.get('label'), h.get('description')) for h in d.get('search', [])]
    pick = next((h for h in hits if h[2] and re.search(rx, h[2])), None)
    res[k] = {'term': term, 'pick': pick, 'hits': hits}
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
    print(k, '->', pick, flush=True)
    time.sleep(1.5)
print('manual done')
