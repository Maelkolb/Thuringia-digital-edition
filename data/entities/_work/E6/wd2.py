import sys,json,time,urllib.request,urllib.parse
UA={"User-Agent":"reuss-edition/1.0 (scholarly digital edition; contact: edition maintainer)"}
def get(params):
    url="https://www.wikidata.org/w/api.php?"+urllib.parse.urlencode(params)
    for a in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=30) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception as e:
            time.sleep(2*(a+1))
    return None
def search(t,lang='de',limit=7):
    d=get({"action":"wbsearchentities","search":t,"language":lang,"uselang":lang,"format":"json","limit":limit})
    return d.get('search',[]) if d else None
if __name__=='__main__':
    lang='de'
    for t in sys.argv[1:]:
        if t.startswith('--lang='): lang=t[7:]; continue
        h=search(t,lang)
        print('##',t)
        if h is None: print('   REQUEST FAILED'); continue
        for x in h: print('   ',x['id'],'|',x.get('label'),'|',x.get('description'))
        time.sleep(0.3)
