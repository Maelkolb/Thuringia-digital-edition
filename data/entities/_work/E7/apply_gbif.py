import json, re
from pathlib import Path
W = Path(r'C:\Users\totom\Projects\reuss-edition\data\entities\_work\E7')
dec = json.load(open(W/'dec_raw.json', encoding='utf-8'))
c2 = json.load(open(W/'gbif_cache2_E7.json', encoding='utf-8'))
c3 = json.load(open(W/'gbif_cache3_E7.json', encoding='utf-8'))
c4 = json.load(open(W/'gbif_cache4_E7.json', encoding='utf-8'))
KING = {'Tier': 'Animalia', 'Pflanze': 'Plantae', 'Pilz': 'Fungi'}
FUZZY_OK = {'Andropogon ischaemon', 'Atropa bella-donna', 'Geranium silvaticum', 'Nuphar luteum', 'Phycodes circinnatum',
            'Phylloscopus sibilatrix', 'Laserpitium pruthenicum', 'Barbaraea arcuata'}
def clean(r, rank):
    rk = (r.get('rank') or '').lower()
    if r.get('matchType') == 'EXACT' and rk == rank: return True
    if r.get('matchType') == 'HIGHERRANK' and rk == rank and rank != 'species': return True
    return False
def accepted_name(n):
    if not n: return None
    p = n.split()
    if len(p) == 3 and p[1] == p[2]: p = p[:2]
    return ' '.join(p)
report = []
nogbif = []
for k, d in dec.items():
    sci = d.get('scientific')
    if not sci: continue
    rank = d['rank']; king = KING[d['kind']]
    key = f'{sci}|{king}|{rank}'
    r = c3.get(key) or c2.get(key)
    use = None
    if r and clean(r, rank) and r.get('status') in ('ACCEPTED', 'DOUBTFUL', 'SYNONYM'):
        use = r
    elif r and r.get('matchType') == 'FUZZY' and sci in FUZZY_OK and (r.get('rank') or '').lower() == 'species':
        use = r
    if use:
        if use.get('status') == 'SYNONYM' and use.get('acceptedUsageKey'):
            d['gbif'] = use['acceptedUsageKey']
            an = accepted_name(use.get('acceptedName'))
            if an and an.lower() != sci.lower():
                d['note'] = (d.get('note', '') + (' ' if d.get('note') else '') + f'GBIF-Name: {an}.').strip()
        else:
            d['gbif'] = use['usageKey']
        report.append((k, sci, rank, d['gbif'], use.get('canonicalName') or use.get('scientificName'), use.get('status'), use.get('matchType')))
    else:
        a4 = c4.get(sci)
        if a4 and sci not in ('Apocynum venetum', 'Triton palustris') and a4.get('matchType') == 'EXACT' and a4.get('status') in ('ACCEPTED', 'SYNONYM'):
            if a4['status'] == 'SYNONYM':
                d['gbif'] = a4['acceptedUsageKey']
            else:
                d['gbif'] = a4['usageKey']
            d['note'] = (d.get('note', '') + (' ' if d.get('note') else '') + f"GBIF-Name: {a4['alt']}.").strip()
            report.append((k, sci, rank, d['gbif'], a4['canonicalName'], a4['status'], 'ALT'))
        else:
            nogbif.append((k, sci, rank, r.get('canonicalName') if r else None, r.get('matchType') if r else None))
json.dump(dec, open(W/'dec_final.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(report), 'with gbif;', len(nogbif), 'without')
json.dump(report, open(W/'gbif_report.json', 'w', encoding='utf-8'), ensure_ascii=False)
for x in nogbif: print('NO', x)
