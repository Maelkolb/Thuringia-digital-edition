import json
from pathlib import Path
from lib import KEYS
W = Path(r'C:\Users\totom\Projects\reuss-edition\data\entities\_work\E7')
dec = json.load(open(W/'dec_final.json', encoding='utf-8'))
ORDER = ['key','action','label','class','kind','scientific','rank','gbif','modern','gloss_en','into','reason','note']
out = []
for k in KEYS:
    d = dec[k]
    row = {f: d[f] for f in ORDER if f in d and d[f] not in (None, '')}
    extra = set(d) - set(ORDER)
    assert not extra, (k, extra)
    out.append(row)
res = {'package': 'E7', 'group': 'organisms', 'decisions': out}
dst = Path(r'C:\Users\totom\Projects\reuss-edition\data\entities\decisions\E7.json')
dst.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
print('written', dst, len(out))
