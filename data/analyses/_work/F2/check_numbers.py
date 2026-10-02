"""Recompute the headline numbers of the four F2 features from the datasets inside the written JSON files
and assert that they appear (German and English formatting) in the texts."""
from common import *


def load_feature(fid):
    return json.load(open(OUT / f'{fid}.json', encoding='utf-8'))


def table(f, name):
    d = [x for x in f['datasets'] if x['name'] == name][0]
    return rows(d)


def texts(f, lang):
    parts = [f['title'][lang], f['summary'][lang]]
    parts += [x[lang] for x in f.get('findings', [])]
    for c in f['charts']:
        parts += [c['title'][lang], c['caption'][lang]]
    parts += [x[lang] for x in f.get('caveats', [])]
    return '\n'.join(parts)


def de(x, nd=1):
    return de_num(x, nd)


def en(x, nd=1):
    return en_num(x, nd)


def expect(label, f, value, nd=1, also_int=False):
    ok = []
    for lang, fmt in (('de', de), ('en', en)):
        t = texts(f, lang)
        s = fmt(value, nd)
        found = s in t
        ok.append(found)
        if not found:
            print(f'  MISSING [{lang}] {label}: {s}')
    return all(ok)


bad = 0

# ------------------------------------------------------------------ klima-gera
f = load_feature('klima-gera')
ta = table(f, 'temp_annual')
tm = table(f, 'temp_monthly')
ry = table(f, 'rain_yearly')
rr = table(f, 'rain_reference')
pa = table(f, 'pressure_annual')
we = table(f, 'weather_events')
checks = [
    ('annual mean', statistics.mean(r['annual_c'] for r in ta), 1),
    ('cold year value', min(r['annual_c'] for r in ta), 1),
    ('warm year value', max(r['annual_c'] for r in ta), 1),
    ('max reading', max(r['max_c'] for r in ta), 1),
    ('min reading', min(r['min_c'] for r in ta), 1),
    ('summer max deviation', max(abs(r['anomaly_c']) for r in tm if r['month'] in (6, 7, 8, 9)), 1),
    ('thunderstorms per year', sum(r['days'] or 0 for r in we if r['phenomenon'] == 'Gewitter') / 12, 1),
    ('driest mm', min(r['annual_mm'] for r in ry), 0),
    ('wettest mm', max(r['annual_mm'] for r in ry), 0),
]
for label, v, nd in checks:
    if not expect(label, f, v, nd):
        bad += 1
th = [r for r in rr if r['label'].startswith('Th')][0]['mm']
assert sum(1 for r in ry if r['annual_mm'] > th) == 3
gew = [r for r in we if r['phenomenon'] == 'Gewitter']
pct = 100 * sum(r['days'] or 0 for r in gew if r['month'] in (6, 7, 8)) / sum(r['days'] or 0 for r in gew)
assert f'{pct:.0f}' == '64'
early = statistics.mean(r['pressure_hpa'] for r in pa if r['year'] <= 1864)
jump = [r['pressure_hpa'] - early for r in pa if r['year'] >= 1865]
assert f'{min(jump):.0f}' == '8' and f'{max(jump):.0f}' == '11'
print('klima-gera checked')

# ------------------------------------------------------------------ klima-stationen
f = load_feature('klima-stationen')
st = table(f, 'stations')
tr = table(f, 'trend')[0]
sa = table(f, 'station_annual')
sd = table(f, 'station_days')
slope = (tr['y0'] - tr['y1']) / (tr['x1'] - tr['x0']) * 100
if not expect('slope', f, slope, 2):
    bad += 1
for r in st:
    if r['judgement'] == 'high':
        if not expect('excess ' + r['station'], f, r['excess_k'], 1):
            bad += 1
g = {r['year']: r['annual_c'] for r in sa if r['station'] == 'Gera'}
h = {r['year']: r['annual_c'] for r in sa if r['station'] == 'Hohenleuben'}
s = {r['year']: r['annual_c'] for r in sa if r['station'] == 'Schleiz'}
if not expect('Gera-Hohenleuben', f, statistics.mean(g[y] - h[y] for y in range(1856, 1861)), 2):
    bad += 1
if not expect('Schleiz-Gera', f, statistics.mean(s[y] - g[y] for y in range(1863, 1868)), 2):
    bad += 1
days = {(r['station'], r['measure']): r['days'] for r in sd}
assert round(days[('Gera', 'gemischt')]) == 243 and round(days[('Hohenleuben', 'gemischt')]) == 55
assert days[('Rothenacker', 'Nebel')] == 76.5 and days[('Schleiz', 'Nebel')] == 16
fog_ratio = days[('Rothenacker', 'Nebel')] / days[('Schleiz', 'Nebel')]
mix_ratio = days[('Gera', 'gemischt')] / days[('Hohenleuben', 'gemischt')]
assert 4 <= mix_ratio < 4.5 and 4.5 < fog_ratio < 5, (fog_ratio, mix_ratio)
print('klima-stationen checked')

# ------------------------------------------------------------------ wind-gewitter
f = load_feature('wind-gewitter')
ws = table(f, 'wind_stations')
share = {(r['station'], r['direction']): r['share'] for r in ws}
for key in [('Gera', 'S'), ('Gera', 'N'), ('Hohenleuben', 'W'), ('Schleiz', 'SW')]:
    if not expect(str(key), f, share[key], 1):
        bad += 1
for station in ('Gera', 'Hohenleuben', 'Schleiz', 'Rothenacker'):
    total = sum(r['count'] for r in ws if r['station'] == station)
    for r in ws:
        if r['station'] == station:
            assert abs(100 * r['count'] / total - r['share']) < 0.06, (station, r['direction'])
tm_ = table(f, 'thunder_monthly')
tot = {}
for r in tm_:
    tot[r['month']] = tot.get(r['month'], 0) + (r['count'] or 0)
assert sum(tot.values()) == 346 and tot[11] == 0
assert f'{100 * (tot[6] + tot[7] + tot[8]) / 346:.0f}' == '65'
ta_ = {(r['station'], r['kind']): r['per_year'] for r in table(f, 'thunder_annual')}
for key in [('Gera', 'mean'), ('Rothenacker', 'mean'), ('Schleiz', 'mean')]:
    if not expect(str(key), f, ta_[key], 1):
        bad += 1
print('wind-gewitter checked')

# ------------------------------------------------------------------ phaenologie
f = load_feature('phaenologie')
bl = table(f, 'bloom')
G = {(r['species'], r['year']): r['doy'] for r in bl if r['station'] == 'Gera'}
H = {(r['species'], r['year']): r['doy'] for r in bl if r['station'] == 'Hohenleuben'}
diff = statistics.mean(H[k] - G[k] for k in G if k in H)
if not expect('bloom difference', f, diff, 1):
    bad += 1
sp = [r for r in table(f, 'spring') if r['station'] == 'Hohenleuben' and r['temp_mar_may_c'] is not None]
reg = statistics.linear_regression([r['temp_mar_may_c'] for r in sp], [r['index_days'] for r in sp])
if not expect('slope', f, abs(reg.slope), 1):
    bad += 1
if not expect('r temp', f, statistics.correlation([r['temp_mar_may_c'] for r in sp], [r['index_days'] for r in sp]), 2):
    bad += 1
bs = table(f, 'bird_species')
if not expect('r birds', f, statistics.correlation([r['mean_arrival_doy'] for r in bs], [r['mean_departure_doy'] for r in bs]), 2):
    bad += 1
stays = [r['mean_stay_days'] for r in bs if r['mean_stay_days'] is not None]
assert f'{max(stays):.0f}' == '265' and f'{min(stays):.0f}' == '99'
print('phaenologie checked')

print('PROBLEMS:', bad)
