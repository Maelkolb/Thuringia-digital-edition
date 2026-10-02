import re,sys,json,glob,os
def load_entities():
    ents={}
    for f in sorted(glob.glob('data/gazetteer/G*.json')):
        for e in json.load(open(f,encoding='utf-8'))['entries']:
            ents[e['name']]=e
    return ents
def text_of(e):
    s=e['start'];en=e['end']
    a=int(s['page']);b=int(en['page'])
    out=[]
    for p in range(a,b+1):
        fn=f'data/text/pages/{p}.txt'
        if not os.path.exists(fn): continue
        t=open(fn,encoding='utf-8').read()
        blocks=re.split(r'^(?=\[(?:b|fn)\d+ )',t,flags=re.M)
        for bl in blocks:
            m=re.match(r'\[(b\d+|fn\d+) ',bl)
            if not m: continue
            bid=m.group(1)
            if p==a and bid.startswith('b') and int(bid[1:])<int(s['block'][1:]): continue
            if p==b and bid.startswith('b') and int(bid[1:])>int(en['block'][1:]): continue
            out.append((p,bid,bl))
    return out
