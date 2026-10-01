import json,sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
sys.path.insert(0,r'C:\Users\totom\Projects\reuss-edition\pipeline\site')
from norm import fold,norm
V=json.load(open(r'C:\Users\totom\Projects\reuss-edition\site\suche\vocab.json',encoding='utf-8'))
for p in sys.argv[1:]:
    f=fold(p)
    m=[(V['df'][i],V['d'][i]) for i,t in enumerate(V['t']) if t.startswith(f)]
    m.sort(reverse=True)
    print(p,'::',' '.join(f"{d}({df})" for df,d in m[:14]))
