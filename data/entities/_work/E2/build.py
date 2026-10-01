import json,sys
from pathlib import Path
import p01,p02,p03,p04,p05,p06,p07,p08,p09,p10,p11,p12,p13,p14,p15
from lib import D,SLICE,ROOT
miss=[k for k in SLICE if k not in D]
print('missing',miss)
out=[D[k] for k in SLICE if k in D]
issues=[
 {"page":"332","block":"b3","transcribed":"Würschengriin","printed":"Würschengrün","note":"ü als ii transkribiert; Facsimile geprüft"},
 {"page":"432","block":"b1","transcribed":"Ropschitz","printed":"Ropschitz","note":"kein Fehler; Fußnote erklärt: Dies ist Oberröppisch"},
]
issues=issues[:1]
d={"package":"E2","group":"places","decisions":out,"transcription_issues":issues}
p=ROOT/'data'/'entities'/'decisions'
p.mkdir(parents=True,exist_ok=True)
(p/'E2.json').write_text(json.dumps(d,ensure_ascii=False,indent=1),encoding='utf-8')
import collections
print(collections.Counter(x['action'] for x in out))
