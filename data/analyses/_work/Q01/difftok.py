"""Q01: token-level summary of changes between the backup (scratchpad) and the current analyses."""
import glob, re, collections, difflib, os, sys
SP = "C:/Users/totom/AppData/Local/Temp/claude/C--Users-totom/9d5e7ab8-c251-427e-83bd-b145b2d015af/scratchpad/q01/backup_before"
cnt = collections.Counter()
for f in sorted(glob.glob(SP + '/*.json')):
    name = os.path.basename(f)
    a = open(f, encoding='utf-8').read(); b = open('data/analyses/' + name, encoding='utf-8').read()
    if a == b: continue
    ta = re.findall(r"[\wäöüÄÖÜß’'.-]+", a); tb = re.findall(r"[\wäöüÄÖÜß’'.-]+", b)
    sm = difflib.SequenceMatcher(None, ta, tb, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != 'equal':
            x = ' '.join(ta[i1:i2]); y = ' '.join(tb[j1:j2])
            if x.replace("'", "’") == y: continue
            cnt[(x, y)] += 1
for (x, y), c in cnt.most_common(int(sys.argv[1]) if len(sys.argv) > 1 else 150): print(c, '|', x, '->', y)
print(len(cnt))
