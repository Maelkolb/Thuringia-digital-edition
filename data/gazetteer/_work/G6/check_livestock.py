import json, re, sys
sys.path.insert(0, 'tools')
import importlib.util
spec = importlib.util.spec_from_file_location('vg', 'tools/validate_gazetteer.py')
vg = importlib.util.module_from_spec(spec); spec.loader.exec_module(vg)
d = json.load(open('data/gazetteer/G6.json', encoding='utf-8'))
MAP = {'Pf': 'Pferde', 'R': 'Rinder', 'Schf': 'Schafe', 'Schw': 'Schweine', 'Z': 'Ziegen', 'G': 'Gänse', 'Bnst': 'Bienenstöcke', 'Bust': 'Bienenstöcke', 'B': 'Bienenstöcke', 'Es': 'Esel'}
for e in d['entries']:
    txt = vg.article_text(e['start'], e['end'])
    m = re.search(r'Vieh ((?:\d+ (?:Pf|R|Schf|Schw|Z|G|Bnst|Bust|B|Es)\.,? ?(?:und )?)+)', txt)
    if not m:
        print(e['id'], 'no livestock seq in text; dict:', e.get('livestock')); continue
    seq = {MAP[k]: int(n) for n, k in re.findall(r'(\d+) (Pf|R|Schf|Schw|Z|G|Bnst|Bust|B|Es)\.', m.group(1))}
    ok = seq == e.get('livestock')
    print(e['id'], 'OK' if ok else f'DIFF text={seq} dict={e.get("livestock")}')
