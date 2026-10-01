import json,sys
sys.path.insert(0,'C:/Users/totom/Projects/reuss-edition/data/entities/_work/E3')
from lib import E,S
D={}
def _put(k,x):
    assert k in E,('unknown key',k)
    assert k not in D,('dup',k)
    x['key']=k; D[k]=x
def A(k,label,kind,gn=None,ip=None,note=None,gloss=None,modern=None,wd=None,cls='nature'):
    x={'action':'accept','label':label,'class':cls,'kind':kind}
    if gn: x['geonames']=gn
    if ip is not None: x['in_principality']=ip
    if note: x['note']=note
    if gloss: x['gloss_en']=gloss
    if modern: x['modern']=modern
    if wd: x['wikidata']=wd
    _put(k,x)
def M(k,into):
    _put(k,{'action':'merge','into':into})
def R(k,reason):
    _put(k,{'action':'reject','reason':reason})
def C(k,label,kind,gloss=None,note=None,modern=None):
    x={'action':'reclass','class':'concept','label':label,'kind':kind}
    if modern: x['modern']=modern
    if gloss: x['gloss_en']=gloss
    if note: x['note']=note
    _put(k,x)
def P(k,label,kind,note=None,gloss=None,gn=None,ip=None):
    x={'action':'reclass','class':'place','label':label,'kind':kind}
    if gn: x['geonames']=gn
    if ip is not None: x['in_principality']=ip
    if note: x['note']=note
    if gloss: x['gloss_en']=gloss
    _put(k,x)
def O(k,cls,label,kind,note=None,gloss=None):
    x={'action':'reclass','class':cls,'label':label,'kind':kind}
    if note: x['note']=note
    if gloss: x['gloss_en']=gloss
    _put(k,x)
