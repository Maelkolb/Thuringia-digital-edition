import json,sys
key=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 8
lo=int(sys.argv[3]) if len(sys.argv)>3 else 0
out=[]
with open('data/entities/mentions.jsonl',encoding='utf-8') as f:
    for l in f:
        if key in l:
            d=json.loads(l)
            if d.get('key')==key: out.append(d)
print(len(out), list(out[0].keys()) if out else '')
step=max(1,len(out)//n)
for d in out[lo::step][:n]:
    print(d['page'],d['unit'],'|',d['ctx'][:260])
