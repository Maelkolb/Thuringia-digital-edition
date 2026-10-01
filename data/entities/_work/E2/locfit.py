import json,re,math,glob
from pathlib import Path
ROOT=Path(r'C:\Users\totom\Projects\reuss-edition')
C={x['key']:x for x in json.load(open(ROOT/'data/entities/candidates/places.json',encoding='utf-8'))['entries']}
REF={}
for k,x in C.items():
    gl=[g for g in x.get('geonames_candidates',[]) if g['km']<=75 and g['code'].startswith('PPL')]
    if gl:
        gl.sort(key=lambda g:-(g.get('population') or 0))
        REF[k]=(gl[0]['lat'],gl[0]['lon'])
REF['Gera']=(50.8803,12.0819)
BR={'N':0,'NNO':22.5,'NON':22.5,'NO':45,'ONO':67.5,'NOO':67.5,'O':90,'OSO':112.5,'SOO':112.5,'SO':135,'SSO':157.5,'SOS':157.5,'S':180,'SSW':202.5,'SWS':202.5,'SW':225,'WSW':247.5,'SWW':247.5,'W':270,'WNW':292.5,'NWW':292.5,'NW':315,'NNW':337.5,'NWN':337.5}
def hav(la1,lo1,la2,lo2):
    R=6371;p=math.pi/180
    d=math.sin((la2-la1)*p/2)**2+math.cos(la1*p)*math.cos(la2*p)*math.sin((lo2-lo1)*p/2)**2
    return 2*R*math.asin(math.sqrt(d))
def bearing(la1,lo1,la2,lo2):
    p=math.pi/180
    y=math.sin((lo2-lo1)*p)*math.cos(la2*p)
    x=math.cos(la1*p)*math.sin(la2*p)-math.sin(la1*p)*math.cos(la2*p)*math.cos((lo2-lo1)*p)
    return (math.atan2(y,x)/p+360)%360
PAT=re.compile(r'((?:\d+\s+)?\d+/\d+|\d+(?:,\d+)?)\s*Stunden?\s+((?:[NOSW]{1,3}))\.?\s+(?:von|vom|bei)\s+(?:dem\s+)?([A-ZÄÖÜ][\wäöüß-]+)')
def parse(txt):
    m=PAT.search(txt)
    if not m: return None
    h=m.group(1)
    if '/' in h:
        parts=h.split()
        val=0
        for q in parts:
            if '/' in q:
                a,b=q.split('/'); val+=int(a)/int(b)
            else: val+=int(q)
    else: val=float(h.replace(',','.'))
    d=m.group(2)
    return val,d,m.group(3)
def fit(text,gns):
    r=parse(text)
    if not r: return None
    h,d,ref=r
    if ref not in REF or d not in BR: return ('noref',h,d,ref)
    la0,lo0=REF[ref]
    out=[]
    for g in gns:
        dist=hav(la0,lo0,g['lat'],g['lon']); br=bearing(la0,lo0,g['lat'],g['lon'])
        bd=abs((br-BR[d]+180)%360-180)
        out.append((g['geonames'],round(dist,1),round(br),round(bd)))
    return (h,d,ref,round(h*4.2,1),out)
