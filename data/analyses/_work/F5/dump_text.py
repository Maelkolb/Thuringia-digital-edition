import json, sys
sys.stdout.reconfigure(encoding='utf-8')
def w(s): return len(s.split())
for fid in sys.argv[1:]:
    d=json.load(open(f'../../{fid}.json',encoding='utf-8'))
    print('='*90); print(fid)
    for lang in ['de','en']:
        print(f'--- {lang}')
        print('TITLE', d['title'][lang])
        print('SUMMARY', w(d['summary'][lang]), d['summary'][lang])
        for f in d.get('findings',[]): print('FIND', w(f[lang]), f[lang])
        for c in d['charts']:
            print('CHART', c['id'], w(c['title'][lang]), c['title'][lang]); print('  CAP', w(c['caption'][lang]), c['caption'][lang])
        print('METHOD', w(d['method'][lang]), d['method'][lang])
        for c in d.get('caveats',[]): print('CAVEAT', w(c[lang]), c[lang])
