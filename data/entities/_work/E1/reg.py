import json,sys,re,difflib
d=json.load(open('data/registers/ortsregister.json',encoding='utf-8'))['entries']
pat=re.compile(sys.argv[1],re.I)
for e in d:
    if pat.search(e['name']):
        print({k:v for k,v in e.items() if k not in ('register_page','ausser_gemeindeverband')})
