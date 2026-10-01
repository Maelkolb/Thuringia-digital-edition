import sys,json,subprocess,time
terms=sys.argv[1:]
for t in terms:
    for attempt in range(3):
        r=subprocess.run(['python','tools/wikidata_search.py',t],capture_output=True,text=True,encoding='utf-8')
        try:
            d=json.loads(r.stdout.strip().splitlines()[0])
        except Exception as e:
            time.sleep(3); continue
        if d['hits'] and 'error' in d['hits'][0]:
            time.sleep(4); continue
        break
    print('##',t)
    for h in d['hits']: print('   ',h.get('id'),'|',h.get('label'),'|',h.get('description'))
