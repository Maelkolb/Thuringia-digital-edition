import json,sys
W=int(sys.argv[1]); keys=set(sys.argv[2:])
n={}
for l in open('data/entities/mentions.jsonl',encoding='utf-8'):
    d=json.loads(l)
    if d['key'] in keys:
        print(d['key'],'p'+str(d['page']),d['unit'],'|',d['ctx'][:2*W+40].replace('\n',' '))
