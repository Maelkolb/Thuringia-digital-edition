import sys,json,os
sys.path.insert(0,'tools')
import wikidata_search as w
terms=[l.strip() for l in open(sys.argv[1],encoding='utf-8') if l.strip()]
cache=json.loads(w.CACHE.read_text(encoding='utf-8')) if w.CACHE.exists() else {}
for t in terms:
    key,_,term=t.partition(' | ')
    h=w.search(term,'de',cache)
    print('##',key,'<=',term)
    for x in h[:4]: print('   ',x.get('id'),'|',x.get('label'),'|',(x.get('description') or '')[:90])
tmp=w.CACHE.with_suffix('.e5.tmp'); tmp.write_text(json.dumps(cache,ensure_ascii=False),encoding='utf-8'); os.replace(tmp,w.CACHE)
