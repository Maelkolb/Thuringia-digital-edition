# -*- coding: utf-8 -*-
import json, re, sys, glob
import importlib.util
spec = importlib.util.spec_from_file_location('vg', 'tools/validate_gazetteer.py')
vg = importlib.util.module_from_spec(spec); sys.argv = ['x']; spec.loader.exec_module(vg)
d = json.load(open('data/gazetteer/G1.json', encoding='utf-8'))


def norm(x):
    return re.sub(r'\s+', ' ', x)


SPLIT = re.compile(r'(?<!Thlr)(?<!Mk)(?<!Pf)(?<!Gr)(?<!Sgr)(?<!Chr)(?<!Nic)(?<!Ao)(?<!Dr)(?<!Joh)(?<!Fr)(?<!Heinr)(?<!Aug)(?<!Gottl)(?<!Jul)(?<!Conr)(?<!Gottfr)(?<!incl)\.\s+(?=[A-ZÄÖÜ„])')
CUT = re.compile(r'(?<=Thlr\.) (?=(Der|Die|Das|Zu|Sie|Ihr|An|Im|Hier|Außer|Ein|Eine|Nach|Es)\b)')
files = sorted(glob.glob('data/gazetteer/_work/G1/c0[0-9].py'))
manual = {
    'untermhaus': "Ihr Grundeigenthum, 3 5/6 Morgen groß und 7500 Thlr. werth, besteht in Communalgebäuden, freien Plätzen, Ortsstraßen und 3 Communicationswegen. An Kapital hat sie circa 1000 Thlr., an Schulden circa 6000 Thlr., wovon ein Theil auf Cuba kommt; ihre Jahresausgabe beträgt 600 bis 700 Thlr.",
    'gera': "ein Vermögen von 540,600 Thlr., darunter 135,000 Thlr. (Versicherungswerth) an 22 Communalgebäuden, 208,500 Thlr. (Verkaufswerth) an Waldungen, 12000 Thlr. an Feldern, Wiesen und Gärten … 128180 Thlr. 12 Sgr. 4 Pf. 128071 Thlr. 13 Sgr. 9 Pf.",
}
BS = chr(92)
for e in d['entries']:
    mf = e.get('municipal_finances')
    if not mf:
        continue
    t = norm(vg.article_text(e['start'], e['end']).replace('\n', ' '))
    if e['id'] in manual:
        v = manual[e['id']]
    else:
        sents = SPLIT.split(t)
        cands = [s for s in sents if re.search(r'Gemeinde', s) and re.search(r'Thlr|Vermögen|Schulden|Ausgabe|Etat|Bedarf', s) and re.search(r'besitzt|besaß|hat |Vermögen|Schulden', s)]
        v = CUT.split(cands[0])[0].rstrip('. ')
        if v.endswith('Thlr'):
            v += '.'
    old = mf['verbatim']
    done = 0
    for f in files:
        s = open(f, encoding='utf-8').read()
        if old in s:
            s = s.replace(old, v.replace(BS, BS + BS).replace('"', BS + '"'), 1)
            open(f, 'w', encoding='utf-8').write(s)
            done += 1
    if done != 1:
        print('NOT REPLACED', e['id'], done)
    print(e['id'], '->', v[:150])
