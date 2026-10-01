import sys,re
from pathlib import Path
ROOT=Path(r'C:\Users\totom\Projects\reuss-edition')
# usage: art.py Name page [nchars]
name,page=sys.argv[1],sys.argv[2]
n=int(sys.argv[3]) if len(sys.argv)>3 else 600
tx=(ROOT/f'data/text/pages/{page}.txt').read_text(encoding='utf-8')
m=re.search(r'\] '+re.escape(name)+r'[ ,(]',tx)
if not m:
    m=re.search(re.escape(name),tx)
print(page,tx[m.start():m.start()+n].replace('\n',' ') if m else 'NOT FOUND')
