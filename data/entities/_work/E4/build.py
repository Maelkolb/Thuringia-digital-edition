# -*- coding: utf-8 -*-
import json, sys
sys.path.insert(0, r'C:\Users\totom\Projects\reuss-edition\data\entities\_work\E4')
import part1, part2, part3, part4
from part1 import D, KEYS, KS
missing = [k for k in KEYS if k not in D]
print('decided', len(D), 'of', len(KEYS), 'missing', len(missing))
for k in missing:
    print('   MISSING', repr(k))
# order as in slice
out = {'package': 'E4', 'group': 'persons', 'decisions': [D[k] for k in KEYS if k in D]}
if not missing:
    json.dump(out, open(r'C:\Users\totom\Projects\reuss-edition\data\entities\decisions\E4.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('written')
