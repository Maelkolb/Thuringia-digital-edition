import json,re,math,collections
from pathlib import Path
ROOT=Path('C:/Users/totom/Projects/reuss-edition')
c=json.load(open(ROOT/'data/entities/candidates/nature.json',encoding='utf-8'))
E={x['key']:x for x in c['entries']}
S=json.load(open(ROOT/'data/entities/slices.json',encoding='utf-8'))['E3']['keys']
def hav(la1,lo1,la2,lo2):
    R=6371;p=math.pi/180
    d=math.sin((la2-la1)*p/2)**2+math.cos(la1*p)*math.cos(la2*p)*math.sin((lo2-lo1)*p/2)**2
    return 2*R*math.asin(math.sqrt(d))
_places=None
def places():
    global _places
    if _places is None:
        p=json.load(open(ROOT/'data/entities/candidates/places.json',encoding='utf-8'))['entries']
        d=collections.defaultdict(list)
        for e in p:
            for g in e.get('geonames_candidates',[]):
                if g.get('class')=='P' and g['km']<=60:
                    d[e['key']].append((g['lat'],g['lon']))
            # forms
        _places=d
    return _places
_mentions=None
def mentions():
    global _mentions
    if _mentions is None:
        m=collections.defaultdict(list)
        for l in open(ROOT/'data/entities/mentions.jsonl',encoding='utf-8'):
            x=json.loads(l)
            if x['key'] in E: m[x['key']].append(x)
        _mentions=m
    return _mentions
_pc={}
def block(page,unit):
    if page not in _pc:
        f=ROOT/'data/text/pages'/f'{page}.txt'
        t=f.read_text(encoding='utf-8') if f.exists() else ''
        blocks={}
        cur=None
        for line in t.split('\n'):
            m=re.match(r'\[(b\d+|fn\d+) ',line)
            if m:
                cur=m.group(1); blocks[cur]=line
            elif cur: blocks[cur]+='\n'+line
        _pc[page]=blocks
    return _pc[page].get(unit,'')
def seg(m,win=90):
    if '.' in m['unit']:
        return m['ctx']
    b=block(m['page'],m['unit']); i=b.find(m['form'])
    return b[max(0,i-win):i+len(m['form'])+win] if i>=0 else m['ctx']
def verify(k,win=60,maxd=3.5):
    """best (cand, place, km) per candidate"""
    x=E[k]; pl=places(); best={}
    cands=[g for g in x.get('geonames_candidates',[]) if g['km']<=60 and g.get('class')!='P']
    if not cands: return []
    for m in mentions().get(k,[]):
        sg=seg(m,win)
        for w in set(re.findall(r'[A-ZÄÖÜ][\w\-äöüß]+',sg)):
            if w in pl and w!=k:
                for g in cands:
                    for la,lo in pl[w]:
                        d=hav(g['lat'],g['lon'],la,lo)
                        if d<=maxd and (g['geonames'] not in best or d<best[g['geonames']][1]):
                            best[g['geonames']]=(w,round(d,1))
    return [(g,)+v for g,v in best.items()]
