import subprocess, sys, time, json
terms = [l.strip() for l in open(sys.argv[1], encoding='utf-8') if l.strip()]
out = open(sys.argv[2], 'a', encoding='utf-8')
for t in terms:
    for attempt in range(5):
        r = subprocess.run([sys.executable, 'tools/wikidata_search.py', t], capture_output=True, text=True, encoding='utf-8')
        line = r.stdout.strip()
        if 'request failed' in line:
            time.sleep(25)
            continue
        break
    out.write(line + '\n'); out.flush()
    time.sleep(4)
