import json, sys
sys.path.insert(0,'.')
import meta_pages_a, meta_pages_b
from meta_pages_a import PAGES
from meta_glossary import GLOSSARY
labels=[p['page'] for p in PAGES]
want=[str(i) for i in range(570,633)]
assert labels==want, (set(want)-set(labels), [l for l in labels if l not in want], len(labels))
d={"package":"G3","pages":PAGES,"glossary":GLOSSARY}
json.dump(d,open('../../../search/pages/G3.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
print(len(PAGES),'pages',len(GLOSSARY),'glossary')
