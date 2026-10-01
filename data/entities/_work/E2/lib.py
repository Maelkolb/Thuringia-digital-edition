import json, sys
from pathlib import Path
ROOT = Path(r'C:\Users\totom\Projects\reuss-edition')
_c = json.load(open(ROOT/'data/entities/candidates/places.json', encoding='utf-8'))['entries']
C = {x['key']: x for x in _c}
GN = {}
for x in _c:
    for g in x.get('geonames_candidates', []):
        GN.setdefault(g['geonames'], g)
SLICE = json.load(open(ROOT/'data/entities/slices.json', encoding='utf-8'))['E2']['keys']
D = {}
KIND_EN = {'Stadt': 'town', 'Dorf': 'village', 'Weiler': 'hamlet', 'Rittergut': 'manor', 'Mühle': 'mill',
           'Wüstung': 'deserted settlement', 'Landestheil': 'district', 'Amt': 'administrative district',
           'Herrschaft': 'lordship', 'Land': 'country', 'Staat': 'state', 'Region': 'region',
           'Gebirge': 'mountain range', 'Flur': 'field area', 'Marktflecken': 'market town',
           'Haus': 'house', 'Gehöft': 'farmstead', 'Vorwerk': 'estate farm', 'Schloss': 'castle',
           'Gasthaus': 'inn', 'Hammer': 'ironworks', 'Hütte': 'works', 'Straße': 'street', 'Platz': 'square',
           'Stadtteil': 'town quarter', 'Kreis': 'district', 'Provinz': 'province', 'Herzogtum': 'duchy',
           'Fürstentum': 'principality', 'Königreich': 'kingdom', 'Großherzogtum': 'grand duchy',
           'Kontinent': 'continent', 'Forsthaus': 'forester\'s house', 'Kolonie': 'colony', 'Gut': 'estate',
           'Kloster': 'monastery', 'Vorstadt': 'suburb', 'Ortsteil': 'locality', 'Gemeinde': 'municipality',
           'Bezirk': 'district', 'Burg': 'castle', 'Flurname': 'field name', 'Gasthof': 'inn', 'Kloster': 'convent', 'Ruine': 'ruin', 'Forst': 'forest district', 'Kreisstadt': 'district town', 'Reich': 'empire', 'Landgrafschaft': 'landgraviate', 'Bergwerk': 'mine', 'Adelsfamilie': 'noble family', 'Kurfürstentum': 'electorate', 'Gau': 'Gau (early medieval district)', 'Gewerbeanlage': 'industrial site', 'Kammergut': 'crown estate', 'Landsitz': 'country seat', 'Jagdhaus': 'hunting lodge', 'Landschaft': 'landscape region'}
def _put(d):
    k = d['key']
    assert k in C, k
    assert k not in D, 'dup ' + k
    D[k] = d
def _reg(key, reg):
    r = C[key].get('brueckner_register', [])
    if reg is None:
        return (r[0]['pages'][0] if r else None)
    if isinstance(reg, int) and reg < 20:
        return r[reg]['pages'][0]
    return str(reg)
def A(key, label, kind, gn=None, inp=None, reg=None, modern=None, note=None, wd=None, lat=None, lon=None,
      gloss=None, cls='place'):
    d = {'key': key, 'action': 'accept', 'label': label, 'class': cls, 'kind': kind}
    if gn:
        g = GN[gn]
        d['geonames'] = gn
        d['lat'] = round(g['lat'], 5); d['lon'] = round(g['lon'], 5)
    if lat is not None:
        d['lat'] = lat; d['lon'] = lon
    if wd: d['wikidata'] = wd
    hasreg = bool(C[key].get('brueckner_register'))
    if inp is None:
        inp = hasreg
    if inp != 'omit':
        d['in_principality'] = bool(inp)
    rp = _reg(key, reg)
    if rp: d['register_page'] = rp
    if modern: d['modern'] = modern
    if gloss is None:
        ke = KIND_EN.get(kind)
        gloss = f"{modern or label} ({ke})" if ke else (modern or label)
    d['gloss_en'] = gloss
    if note: d['note'] = note
    _put(d)
def RC(key, label, cls, kind, gn=None, note=None, gloss=None, wd=None, lat=None, lon=None, modern=None):
    d = {'key': key, 'action': 'reclass', 'label': label, 'class': cls, 'kind': kind}
    if gn:
        g = GN[gn]; d['geonames'] = gn; d['lat'] = round(g['lat'], 5); d['lon'] = round(g['lon'], 5)
    if lat is not None:
        d['lat'] = lat; d['lon'] = lon
    if wd: d['wikidata'] = wd
    if modern: d['modern'] = modern
    if gloss: d['gloss_en'] = gloss
    if note: d['note'] = note
    _put(d)
def M(key, into):
    _put({'key': key, 'action': 'merge', 'into': into})
def R(key, reason):
    _put({'key': key, 'action': 'reject', 'reason': reason})
def MR(keys, into):
    for k in keys.split('|'):
        M(k, into)
