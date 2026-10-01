import json,sys,re
c=json.load(open('data/entities/candidates/places.json',encoding='utf-8'))['entries']
pat=re.compile(sys.argv[1],re.I)
maxkm=float(sys.argv[2]) if len(sys.argv)>2 else 80
seen={}
for x in c:
    for g in x.get('geonames_candidates',[]):
        if pat.search(g['name']) and g['km']<=maxkm:
            seen.setdefault(g['geonames'],(g,x['key']))
for g,k in sorted(seen.values(),key=lambda t:t[0]['km']):
    print(f"{g['geonames']} {g['name']} {g['code']} pop={g.get('population')} ({g['lat']:.4f},{g['lon']:.4f}) km={g['km']} [key {k}]")
