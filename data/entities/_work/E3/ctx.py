import sys
sys.path.insert(0,'C:/Users/totom/Projects/reuss-edition/data/entities/_work/E3')
from lib import *
k=sys.argv[1]; W=int(sys.argv[2]) if len(sys.argv)>2 else 70; lim=int(sys.argv[3]) if len(sys.argv)>3 else 40
for m in mentions().get(k,[])[:lim]:
    b=block(m['page'],m['unit'])
    i=b.find(m['form'])
    seg=b[max(0,i-W):i+len(m['form'])+W].replace('\n',' ') if i>=0 else m['ctx']
    print(f"[{m['page']}] {m['form']!r}: ...{seg}...")
