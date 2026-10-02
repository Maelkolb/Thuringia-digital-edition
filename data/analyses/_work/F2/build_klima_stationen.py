from common import *

FID = 'klima-stationen'
aH = load('klima-hoehenlage-temperatur-luftdruck')
aS = load('klima-stationen-temperatur-vergleich')
aN = load('klima-niederschlagstage-stationen')
aB = load('klima-bewoelkung-stationen')
aQ = load('klima-quellentemperatur-brunnen')

base_places = json.load(open(SHARED / 'base_places.json', encoding='utf-8'))
base_rivers = json.load(open(SHARED / 'base_rivers.json', encoding='utf-8'))
coords = {r[0]: (r[1], r[2]) for r in base_places['rows']}

# ---------------------------------------------------------------- stations (scatter + map)
d_st = ds(aH, 'stations')
YEARS = {'Gera': 12, 'Hohenleuben': 7, 'Schleiz': 5, 'Saalburg': 1, 'Lobenstein': 1, 'Rothenacker': 2, 'Stelzen': None, 'Grumbach': None, 'Ziegenrück': None}
d_st['columns'] += [
    {'name': 'years', 'label': bi('Beobachtungsjahre', 'Years of observation'), 'type': 'integer', 'unit': 'Jahre', 'derived': True,
     'note': 'aus dem Zeitraum der Spalte period; Stelzen und Grumbach: nur Jahresmittel unbekannten Zeitraums'},
    {'name': 'lon', 'label': bi('Länge', 'Longitude'), 'type': 'number', 'unit': '°', 'derived': True, 'note': 'GeoNames'},
    {'name': 'lat', 'label': bi('Breite', 'Latitude'), 'type': 'number', 'unit': '°', 'derived': True, 'note': 'GeoNames'},
]
for r in d_st['rows']:
    name = r[0]
    r.append(YEARS[name])
    if name in coords:
        r += [coords[name][0], coords[name][1]]
    else:
        r += [None, None]
d_st['title'] = bi('Beobachtungsorte: Höhenlage und Jahresmittel der Temperatur', 'Observation sites: elevation and annual mean temperature')
st = rows(d_st)

d_tr = ds(aH, 'trend')
d_tr['name'] = 'trend'
tr = rows(d_tr)[0]

# ---------------------------------------------------------------- station annual table
d_sa = ds(aS, 'annual')
d_sa['name'] = 'station_annual'
sa = rows(d_sa)

# ---------------------------------------------------------------- days per year (precipitation, fog, frost, sky)
nb = {(r['station'], r['phenomenon']): r for r in rows(ds(aN, 'annual_printed'))}
sky = {(r['station'], r['category']): r for r in rows(ds(aB, 'annual'))}
four = ['Gera', 'Hohenleuben', 'Schleiz', 'Rothenacker']
meas = [('Niederschlag', 'Niederschlagstage'), ('Nebel', 'Nebel'), ('Reif', 'Reif'), ('bedeckt', 'bedeckt'), ('gemischt', 'gemischt'), ('hell', 'hell')]
sd_rows = []
for si, s in enumerate(four, 1):
    for mi, (m, _) in enumerate(meas, 1):
        if m == 'Niederschlag':
            if s == 'Gera':
                regen = 1544 / 12  # corrected sum (S. 830) / 12 years
                val = regen + nb[(s, 'Schnee')]['mean_printed']
            elif s == 'Hohenleuben':
                val = nb[(s, 'Regen')]['mean_printed']  # Regen und Schnee zusammen
            else:
                val = nb[(s, 'Regen')]['mean_printed'] + nb[(s, 'Schnee')]['mean_printed']
            printed = None
        elif m in ('Nebel', 'Reif'):
            printed = nb[(s, m)]['mean_printed']
            val = printed
        else:
            printed = sky[(s, m)]['days_per_year']
            val = printed
        sd_rows.append([s, si, m, mi, printed, round(val, 1)])
d_sd = {
    'name': 'station_days',
    'title': bi('Tage pro Jahr an vier Orten: Niederschlag, Nebel, Reif, Himmelsansicht', 'Days per year at four places: precipitation, fog, hoarfrost, sky'),
    'columns': [
        {'name': 'station', 'label': bi('Ort', 'Place'), 'type': 'string', 'unit': None},
        {'name': 'station_order', 'label': bi('Reihenfolge des Orts', 'Order of the place'), 'type': 'integer', 'unit': None, 'derived': True},
        {'name': 'measure', 'label': bi('Größe', 'Measure'), 'type': 'string', 'unit': None, 'derived': True,
         'note': 'Niederschlag = Regen plus Schnee (Hohenleuben: Regen und Schnee zusammen); bedeckt, gemischt, hell = Himmelsansicht'},
        {'name': 'measure_order', 'label': bi('Reihenfolge der Größe', 'Order of the measure'), 'type': 'integer', 'unit': None, 'derived': True},
        {'name': 'days_printed', 'label': bi('Tage pro Jahr (gedruckt)', 'Days per year (as printed)'), 'type': 'number', 'unit': 'Tage'},
        {'name': 'days', 'label': bi('Tage pro Jahr', 'Days per year'), 'type': 'number', 'unit': 'Tage', 'derived': True,
         'note': 'gedruckter Wert; für Niederschlag die Summe aus Regen und Schnee, Gera mit der berichtigten Regensumme 1544 (S. 830)'},
    ],
    'rows': sd_rows,
    'source_refs': [{'page': '67', 'block': 'b4', 'rows': 'r2-r5'}, {'page': '65', 'block': 'b4', 'rows': 'r2-r5'}, {'page': '830', 'block': 'b3'}],
}
sd = rows(d_sd)

d_sp = ds(aQ, 'measurements')
d_sp['name'] = 'springs'

# ---------------------------------------------------------------- numbers
N = {}
slope = (tr['y0'] - tr['y1']) / (tr['x1'] - tr['x0']) * 100
N['slope'] = slope
high = [r for r in st if r['judgement'] == 'high']
N['ex_lo'] = min(r['excess_k'] for r in high)
N['ex_hi'] = max(r['excess_k'] for r in high)
ex = {r['station']: r['excess_k'] for r in st}
elev = {r['station']: r['elevation_m'] for r in st}
good = [r for r in st if r['judgement'] != 'high' and r['elevation_m'] is not None]
N['good_lo'] = min(r['elevation_m'] for r in good)
N['good_hi'] = max(r['elevation_m'] for r in good)
gen = {r['year']: r['annual_c'] for r in sa if r['station'] == 'Gera'}
hoh = {r['year']: r['annual_c'] for r in sa if r['station'] == 'Hohenleuben'}
sch = {r['year']: r['annual_c'] for r in sa if r['station'] == 'Schleiz'}
d1 = [gen[y] - hoh[y] for y in range(1856, 1861)]
N['gh_mean'] = statistics.mean(d1)
N['gh_all'] = all(x > 0 for x in d1)
N['gh_n'] = len(d1)
d2 = [sch[y] - gen[y] for y in range(1863, 1868)]
N['sg_mean'] = statistics.mean(d2)
N['sg_n_warmer'] = sum(1 for x in d2 if x > 0)
N['gs_dh'] = elev['Schleiz'] - elev['Gera']


def sdv(station, measure):
    return [r['days'] for r in sd if r['station'] == station and r['measure'] == measure][0]


N['fog_lo'] = min(sdv(s, 'Nebel') for s in four)
N['fog_hi'] = max(sdv(s, 'Nebel') for s in four)
N['mix_lo'] = min(sdv(s, 'gemischt') for s in four)
N['mix_hi'] = max(sdv(s, 'gemischt') for s in four)
N['fog_ratio'] = N['fog_hi'] / N['fog_lo']
N['mix_ratio'] = N['mix_hi'] / N['mix_lo']
N['pre_lo'] = min(sdv(s, 'Niederschlag') for s in four)
N['pre_hi'] = max(sdv(s, 'Niederschlag') for s in four)
print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in N.items()})
print({r['station']: (r['elevation_m'], r['annual_c'], r['excess_k']) for r in st})
for r in sd:
    print(r['station'], r['measure'], r['days'])


def r0(x):
    return int(math.floor(x + 0.5))


def dn(x, nd=1):
    return de_num(x, nd)


def en(x, nd=1):
    return en_num(x, nd)


# ---------------------------------------------------------------- c1: scatter
t_station = {'field': 'station', 'title': bi('Ort', 'Place')}
def tooltip_station():
    return [
        t_station,
        {'field': 'period', 'title': bi('Beobachtungszeitraum', 'Period')},
        {'field': 'elevation_m', 'title': bi('Höhe (m)', 'Elevation (m)'), 'format': '.0f'},
        {'field': 'annual_r', 'title': bi('Jahresmittel (°R, gedruckt)', 'Annual mean (°R, as printed)'), 'format': '.2f'},
        {'field': 'annual_c', 'title': bi('Jahresmittel (°C)', 'Annual mean (°C)'), 'format': '.1f'},
        {'field': 'excess_k', 'title': bi('Abstand zur Geraden (K)', 'Distance from line (K)'), 'format': '+.1f'},
    ]


c1 = {
    'id': 'c1',
    'dataset': 'stations',
    'extra_datasets': ['trend'],
    'title': bi(f"Die von Brückner als zu warm beurteilten Orte liegen {dn(N['ex_lo'])} bis {dn(N['ex_hi'])} K über der Höhengeraden",
                f"Places Brückner judged too warm lie {en(N['ex_lo'])} to {en(N['ex_hi'])} K above the line of the others"),
    'caption': bi(
        f"Jahresmittel der Temperatur (aus Réaumur umgerechnet) und Höhe der Ortslage (Mitte der Höhenspanne, in Metern). Gerade durch Gera, Hohenleuben, Stelzen und Grumbach ({dn(N['slope'], 2)} K je 100 m); Zahlen: Abstand zur Geraden. Quelle: S. 12, 20 bis 22, 55 bis 58.",
        f"Annual mean temperature (converted from Réaumur) and elevation of the place (middle of the height range, in meters). Line through Gera, Hohenleuben, Stelzen and Grumbach ({en(N['slope'], 2)} K per 100 m); numbers: distance from the line. Source: pp. 12, 20 to 22, 55 to 58."),
    'vegalite': {
        'height': 400,
        'transform': [{'filter': 'isValid(datum.elevation_m)'}],
        'layer': [
            {
                'data': {'name': 'trend'},
                'mark': {'type': 'rule', 'color': '@muted', 'strokeWidth': 1.5},
                'encoding': {
                    'x': {'field': 'y0', 'type': 'quantitative', 'scale': {'domain': [6, 10.4]},
                          'axis': {'title': bi('Jahresmittel der Temperatur (°C)', 'Annual mean temperature (°C)'), 'values': [6, 7, 8, 9, 10], 'format': 'd', 'grid': False}},
                    'x2': {'field': 'y1'},
                    'y': {'field': 'x0', 'type': 'quantitative', 'scale': {'domain': [150, 730]},
                          'axis': {'title': bi('Höhe der Ortslage (m)', 'Elevation of the place (m)'), 'values': [200, 300, 400, 500, 600, 700]}},
                    'y2': {'field': 'x1'},
                },
            },
            {
                'data': {'name': 'trend'},
                'transform': [{'calculate': "datum.y0 + (290 - datum.x0) * (datum.y1 - datum.y0) / (datum.x1 - datum.x0)", 'as': 'x_at'}],
                'mark': {'type': 'text', 'style': 'annotation', 'align': 'left', 'dx': 12, 'fill': '@muted'},
                'encoding': {
                    'x': {'field': 'x_at', 'type': 'quantitative'},
                    'y': {'datum': 290, 'type': 'quantitative'},
                    'text': {'value': bi(f"{dn(N['slope'], 2)} K je 100 m", f"{en(N['slope'], 2)} K per 100 m")},
                },
            },
            {
                'transform': [{'filter': "datum.judgement == 'high'"}],
                'mark': {'type': 'rule', 'strokeDash': [3, 3], 'color': '@accent2', 'strokeWidth': 1.5},
                'encoding': {
                    'y': {'field': 'elevation_m', 'type': 'quantitative'},
                    'x': {'field': 'annual_c', 'type': 'quantitative'},
                    'x2': {'field': 'trend_c'},
                },
            },
            {
                'mark': {'type': 'circle', 'size': 130, 'opacity': 1},
                'encoding': {
                    'y': {'field': 'elevation_m', 'type': 'quantitative'},
                    'x': {'field': 'annual_c', 'type': 'quantitative'},
                    'color': {'condition': {'test': "datum.judgement == 'high'", 'value': '@accent2'}, 'value': '@accent'},
                    'tooltip': tooltip_station(),
                },
            },
        ] + [
            {
                'transform': [{'calculate': "datum.judgement == 'high' ? datum.station + ' +' + format(datum.excess_k, '.1f') + ' K' : datum.station", 'as': 'lab'}],
                'mark': {'type': 'text', 'style': 'place-halo' if halo else 'label', 'align': 'left', 'dx': 10},
                'encoding': dict({
                    'y': {'field': 'elevation_m', 'type': 'quantitative'},
                    'x': {'field': 'annual_c', 'type': 'quantitative'},
                    'text': {'field': 'lab'}},
                    **({} if halo else {'color': {'condition': {'test': "datum.judgement == 'high'", 'value': '@accent2'}, 'value': '@ink2'}})),
            }
            for halo in (True, False)
        ] + [
            {
                'transform': [{'filter': "datum.station == 'Gera'"}],
                'mark': {'type': 'text', 'style': 'annotation', 'align': 'right', 'color': '@accent2'},
                'encoding': {'x': {'datum': 10.4, 'type': 'quantitative'}, 'y': {'datum': 715, 'type': 'quantitative'},
                             'text': {'value': bi('Orange: von Brückner als zu warm beurteilt (S. 58)', 'Orange: judged too warm by Brückner (p. 58)')}},
            },
            {
                'transform': [{'filter': "datum.station == 'Gera'"}],
                'mark': {'type': 'text', 'style': 'annotation', 'align': 'right', 'color': '@accent'},
                'encoding': {'x': {'datum': 10.4, 'type': 'quantitative'}, 'y': {'datum': 685, 'type': 'quantitative'},
                             'text': {'value': bi('Blau: nicht beanstandet', 'Blue: not criticized')}},
            },
        ],
    },
}

# ---------------------------------------------------------------- c2: map
def lonlat():
    return {'longitude': {'field': 'lon', 'type': 'quantitative'}, 'latitude': {'field': 'lat', 'type': 'quantitative'}}


label_sets = [
    (['Gera'], 'left', 24),
    (['Hohenleuben', 'Schleiz'], 'left', 16),
    (['Stelzen'], 'left', 9),
    (['Saalburg', 'Lobenstein', 'Rothenacker'], 'right', -14),
    (['Grumbach'], 'right', -9),
]


def map_labels(style_name, dy_name, dy_temp):
    out = []
    for names, align, dx in label_sets:
        out.append({
            'transform': [{'filter': f"indexof({names}, datum.station) >= 0"}],
            'mark': {'type': 'text', 'style': style_name, 'align': align, 'dx': dx, 'dy': dy_name},
            'encoding': dict(lonlat(), text={'field': 'station'}),
        })
    return out


def temp_labels(style_name):
    out = []
    for names, align, dx in label_sets:
        out.append({
            'transform': [{'filter': f"indexof({names}, datum.station) >= 0"},
                          {'calculate': "format(datum.annual_c, '.1f') + ' °C'", 'as': 'tlab'}],
            'mark': {'type': 'text', 'style': style_name, 'align': align, 'dx': dx, 'dy': 12},
            'encoding': dict(lonlat(), text={'field': 'tlab'}),
        })
    return out


c2 = {
    'id': 'c2',
    'dataset': 'stations',
    'extra_datasets': ['orte_basis', 'fluesse_basis'],
    'title': bi('Gemessen wurde an acht Orten, aber nur in Gera und Hohenleuben länger als fünf Jahre',
                'Temperatures were recorded at eight places, but only Gera and Hohenleuben for more than five years'),
    'caption': bi(
        'Orte mit gedruckten Temperaturmitteln. Größe: Zahl der Beobachtungsjahre; Stelzen und Grumbach: nur ein Jahresmittel unbekannten Zeitraums (Pfarrämter). Zahl: Jahresmittel in °C. Ziegenrück (Preußen, 1848 bis 1856) liegt außerhalb. Quelle: S. 54 bis 58.',
        'Places with printed temperature means. Size: years of observation; Stelzen and Grumbach: a single annual mean of unknown period (parish offices). Number: annual mean in °C. Ziegenrück (Prussia, 1848 to 1856) lies outside. Source: pp. 54 to 58.'),
    'vegalite': {
        'height': 560,
        'projection': {'type': 'mercator'},
        'layer': [
            {'data': {'name': 'fluesse_basis'}, 'mark': {'type': 'line', 'color': '@river', 'strokeWidth': 1.2, 'interpolate': 'monotone'},
             'encoding': {'longitude': {'field': 'lon', 'type': 'quantitative'}, 'latitude': {'field': 'lat', 'type': 'quantitative'},
                          'detail': {'field': 'abschnitt'}, 'order': {'field': 'folge'}}},
            {'data': {'name': 'orte_basis'}, 'mark': {'type': 'circle', 'size': 10, 'color': '@land', 'opacity': 1},
             'encoding': {'longitude': {'field': 'lon', 'type': 'quantitative'}, 'latitude': {'field': 'lat', 'type': 'quantitative'}}},
            {
                'transform': [{'filter': 'isValid(datum.lon) && isValid(datum.years)'}],
                'mark': {'type': 'circle', 'color': '@accent', 'stroke': '@paper', 'strokeWidth': 1, 'opacity': 0.9},
                'encoding': dict(lonlat(), size={
                    'field': 'years', 'type': 'quantitative', 'scale': {'type': 'sqrt', 'domain': [0, 12], 'range': [40, 520]},
                    'legend': {'title': bi('Beobachtungsjahre', 'Years of observation'), 'titleLimit': 300, 'values': [1, 5, 12], 'orient': 'top-left', 'direction': 'vertical',
                               'symbolFillColor': '@accent', 'symbolStrokeColor': '@paper'}},
                    tooltip=[t_station, {'field': 'period', 'title': bi('Zeitraum', 'Period')},
                             {'field': 'annual_c', 'title': bi('Jahresmittel (°C)', 'Annual mean (°C)'), 'format': '.1f'},
                             {'field': 'elevation_m', 'title': bi('Höhe (m)', 'Elevation (m)'), 'format': '.0f'}]),
            },
            {
                'transform': [{'filter': 'isValid(datum.lon) && !isValid(datum.years)'}],
                'mark': {'type': 'circle', 'color': '@muted', 'size': 70, 'stroke': '@paper', 'strokeWidth': 1},
                'encoding': dict(lonlat(), tooltip=[t_station, {'field': 'period', 'title': bi('Zeitraum', 'Period')},
                                                    {'field': 'annual_c', 'title': bi('Jahresmittel (°C)', 'Annual mean (°C)'), 'format': '.1f'}]),
            },
            {
                'transform': [{'filter': "datum.station == 'Gera'"}],
                'mark': {'type': 'circle', 'color': '@muted', 'size': 70, 'stroke': '@paper', 'strokeWidth': 1},
                'encoding': {'longitude': {'datum': 11.262, 'type': 'quantitative'}, 'latitude': {'datum': 50.838, 'type': 'quantitative'}},
            },
            {
                'transform': [{'filter': "datum.station == 'Gera'"}],
                'mark': {'type': 'text', 'style': 'annotation', 'align': 'left', 'dx': 10},
                'encoding': {'longitude': {'datum': 11.262, 'type': 'quantitative'}, 'latitude': {'datum': 50.838, 'type': 'quantitative'},
                             'text': {'value': bi('nur Jahresmittel, Zeitraum unbekannt', 'annual mean only, period unknown')}},
            },
        ] + map_labels('place-halo', -2, 0) + map_labels('place-label', -2, 0) + temp_labels('label-muted'),
    },
}

# ---------------------------------------------------------------- c3: range dumbbells
meas_label_de = "{'Niederschlag':'Niederschlagstage','Nebel':'Nebeltage','Reif':'Reiftage','bedeckt':'bedeckte Tage','gemischt':'gemischte Tage','hell':'helle Tage'}[datum.measure]"
meas_label_en = "{'Niederschlag':'Precipitation days','Nebel':'Foggy days','Reif':'Hoarfrost days','bedeckt':'Overcast days','gemischt':'Mixed days','hell':'Clear days'}[datum.measure]"
tip_days = [{'field': 'station', 'title': bi('Ort', 'Place')}, {'field': 'measure', 'title': bi('Größe', 'Measure')},
            {'field': 'days', 'title': bi('Tage pro Jahr', 'Days per year'), 'format': '.1f'}]
c3 = {
    'id': 'c3',
    'dataset': 'station_days',
    'title': bi(f"Zwischen den vier Orten unterscheiden sich Nebeltage und gemischte Tage um das Vier- bis Fünffache",
                f"Foggy and mixed days differ between the four places by a factor of four to five"),
    'caption': bi(
        'Tage pro Jahr in Gera, Hohenleuben, Schleiz und Rothenacker. Punkte: die vier Orte, beschriftet sind der höchste und der niedrigste Wert. Niederschlagstage: Regen plus Schnee. Beobachtungsreihen von 2 bis 15 Jahren. Quelle: S. 65, 67.',
        'Days per year at Gera, Hohenleuben, Schleiz and Rothenacker. Dots: the four places; the highest and lowest values are labelled. Days with precipitation: rain plus snow. Observation series of 2 to 15 years. Source: pp. 65, 67.'),
    'vegalite': {
        'height': {'step': 44},
        'transform': [
            {'joinaggregate': [{'op': 'max', 'field': 'days', 'as': 'dmax'}, {'op': 'min', 'field': 'days', 'as': 'dmin'}], 'groupby': ['measure']},
            {'calculate': {'de': meas_label_de, 'en': meas_label_en}, 'as': 'mlabel'},
            {'calculate': "format(datum.days, '.0f')", 'as': 'dlab'},
            {'calculate': 'datum.station + " " + datum.dlab', 'as': 'slab'},
        ],
        'encoding': {
            'y': {'field': 'mlabel', 'type': 'nominal', 'sort': {'field': 'measure_order', 'op': 'min'}, 'axis': {'title': None, 'labelLimit': 260}},
        },
        'layer': [
            {
                'mark': {'type': 'rule', 'strokeWidth': 2, 'color': '@context'},
                'encoding': {
                    'x': {'field': 'dmin', 'type': 'quantitative', 'scale': {'domain': [-75, 300]},
                          'axis': {'title': bi('Tage pro Jahr', 'Days per year'), 'values': [0, 50, 100, 150, 200, 250, 300], 'grid': False}},
                    'x2': {'field': 'dmax'},
                },
            },
            {
                'mark': {'type': 'point', 'filled': True, 'size': 60, 'color': '@muted'},
                'encoding': {'x': {'field': 'days', 'type': 'quantitative'}, 'tooltip': tip_days},
            },
            {
                'transform': [{'filter': 'datum.days == datum.dmax || datum.days == datum.dmin'}],
                'mark': {'type': 'point', 'filled': True, 'size': 110, 'color': '@accent'},
                'encoding': {'x': {'field': 'days', 'type': 'quantitative'}, 'tooltip': tip_days},
            },
            {
                'transform': [{'filter': 'datum.days == datum.dmax'}],
                'mark': {'type': 'text', 'style': 'label', 'align': 'left', 'dx': 10},
                'encoding': {'x': {'field': 'days', 'type': 'quantitative'}, 'text': {'field': 'slab'}},
            },
            {
                'transform': [{'filter': 'datum.days == datum.dmin'}],
                'mark': {'type': 'text', 'style': 'label', 'align': 'right', 'dx': -10},
                'encoding': {'x': {'field': 'days', 'type': 'quantitative'}, 'text': {'field': 'slab'}},
            },
        ],
    },
}

# ---------------------------------------------------------------- feature
f = {
    'id': FID,
    'title': bi('Klima an den Beobachtungsorten', 'Climate at the observation sites'),
    'category': 'climate',
    'section': 't1-1-7',
    'merges': ['klima-stationen-temperatur-vergleich', 'klima-hoehenlage-temperatur-luftdruck', 'klima-niederschlagstage-stationen', 'klima-bewoelkung-stationen', 'klima-quellentemperatur-brunnen'],
    'sources': [
        {'page': '12', 'block': 'b1', 'rows': 'r1'}, {'page': '20', 'block': 'b3'}, {'page': '21', 'block': 'b1'}, {'page': '22', 'block': 'b1'},
        {'page': '54', 'block': 'b1'}, {'page': '55', 'block': 'b9', 'rows': 'r2-r14'}, {'page': '56', 'block': 'b3'}, {'page': '56', 'block': 'b6'},
        {'page': '57', 'block': 'b3'}, {'page': '57', 'block': 'b8'}, {'page': '58', 'block': 'b2'}, {'page': '58', 'block': 'b3'},
        {'page': '65', 'block': 'b4', 'rows': 'r2-r7'}, {'page': '67', 'block': 'b4', 'rows': 'r2-r5'}, {'page': '69', 'block': 'b3'}, {'page': '70', 'block': 'b1'}, {'page': '70', 'block': 'b2'},
    ],
    'summary': bi(
        f"Neben Gera druckt Brückner Temperaturreihen für Hohenleuben, Schleiz und Rothenacker, Jahresmittel für vier weitere Orte sowie Nebel-, Niederschlags- und Himmelszahlen. Das Jahresmittel sinkt um {dn(N['slope'], 2)} K je 100 m Höhe; Schleiz, Lobenstein, Saalburg und Rothenacker liegen darüber, was Brückner selbst als zu hoch beanstandet. Die Zahlen für Nebel und Himmelsansicht gehen zwischen den Orten weit auseinander.",
        f"Besides Gera, Brückner prints temperature series for Hohenleuben, Schleiz and Rothenacker, annual means for four more places, and counts of fog, precipitation and sky conditions. The annual mean falls by {en(N['slope'], 2)} K per 100 m of height; Schleiz, Lobenstein, Saalburg and Rothenacker lie above that line, which Brückner himself criticizes as too high. The figures for fog and sky conditions differ widely between the places."),
    'findings': [
        bi(f"Gera, Hohenleuben, Stelzen und Grumbach liegen nahe an einer Geraden ({dn(N['slope'], 2)} K je 100 m); Saalburg liegt {dn(ex['Saalburg'])} K, Lobenstein {dn(ex['Lobenstein'])} K, Schleiz {dn(ex['Schleiz'])} K und Rothenacker {dn(ex['Rothenacker'])} K darüber.",
           f"Gera, Hohenleuben, Stelzen and Grumbach lie close to a line ({en(N['slope'], 2)} K per 100 m); Saalburg lies {en(ex['Saalburg'])} K, Lobenstein {en(ex['Lobenstein'])} K, Schleiz {en(ex['Schleiz'])} K and Rothenacker {en(ex['Rothenacker'])} K above it."),
        bi(f"1856 bis 1860 war Gera in jedem Jahr wärmer als Hohenleuben, im Mittel um {dn(N['gh_mean'], 2)} K. Schleiz war 1863 bis 1867 im Mittel {dn(N['sg_mean'], 2)} K wärmer als Gera, obwohl etwa {r0(N['gs_dh'] / 10) * 10} m höher gelegen.",
           f"From 1856 to 1860 Gera was warmer than Hohenleuben every year, by {en(N['gh_mean'], 2)} K on average. From 1863 to 1867 Schleiz averaged {en(N['sg_mean'], 2)} K warmer than Gera, although about {r0(N['gs_dh'] / 10) * 10} m higher."),
        bi(f"Gera zählt {r0(N['mix_hi'])} gemischte Tage im Jahr, Hohenleuben nur {r0(N['mix_lo'])}. Nebeltage reichen von {r0(N['fog_lo'])} (Schleiz) bis {dn(N['fog_hi'])} (Rothenacker). Brückner führt das auf uneinheitliche Abgrenzung durch die Beobachter zurück.",
           f"Gera counts {r0(N['mix_hi'])} mixed days a year, Hohenleuben only {r0(N['mix_lo'])}. Foggy days range from {r0(N['fog_lo'])} (Schleiz) to {en(N['fog_hi'])} (Rothenacker). Brückner attributes this to observers drawing the categories differently."),
    ],
    'method': bi(
        'Die Jahresmittel der Temperatur stammen aus Brückners Durchschnittszeilen (S. 55 bis 58); sie sind in Grad Réaumur gedruckt und mit 1,25 in °C umgerechnet. Die Höhen der Ortslagen entnimmt die Auswertung seiner Höhenliste (S. 12, 20 bis 22) in preußischen Dezimalfuß, bei Spannen die Mitte; 1 Dezimalfuß = 0,3766242 m (S. 831). Die Gerade ist die Regression der Jahresmittel auf die Höhe für Gera, Hohenleuben, Stelzen und Grumbach, also die Orte, die Brückner nicht beanstandet; Ziegenrück hat keine Höhe. Die Beobachtungsjahre der Karte folgen dem Zeitraum der Angabe.\n'
        'Nebel, Reif, Regen und Schnee sind die gedruckten Jahresmittel (S. 67); Niederschlagstage sind Regen plus Schnee, für Gera mit der berichtigten Regensumme 1544 (S. 830), für Hohenleuben die gedruckte Spalte »Regen und Schnee«. Die bedeckten, gemischten und hellen Tage stehen auf S. 65. Hof und Arnstadt, die Brückner dort zum Vergleich nennt, werden nicht gezeigt. Die Vergleiche gleicher Jahre im Befund stützen sich auf die Jahresmittel der Tabelle »station_annual«. Die Temperaturen von Quellen und Brunnen (S. 69 f.) sind einzelne Messungen ohne Höhe und stehen nur im Datensatz »springs«.',
        'The annual mean temperatures come from Brückner’s average rows (pp. 55 to 58); they are printed in degrees Réaumur and converted at 1.25 to °C. The elevations of the places are taken from his list of heights (pp. 12, 20 to 22) in Prussian decimal feet, using the middle of a range; 1 decimal foot = 0.3766242 m (p. 831). The line is the regression of the annual means on elevation for Gera, Hohenleuben, Stelzen and Grumbach, the places Brückner does not criticize; Ziegenrück has no elevation. The years of observation on the map follow the period given.\n'
        'Fog, hoarfrost, rain and snow are the printed annual means (p. 67); days with precipitation are rain plus snow, for Gera with the corrected rain total of 1544 (p. 830), for Hohenleuben the printed column »rain and snow«. Overcast, mixed and clear days are on p. 65. Hof and Arnstadt, which Brückner names there for comparison, are not shown. The comparisons of equal years in the findings rest on the annual means in the table »station_annual«. The temperatures of springs and wells (pp. 69 f.) are single readings without elevation and appear only in the dataset »springs«.'),
    'conversions': [
        {'from': 'preuß. Dezimalfuß (Höhen)', 'to': 'm', 'factor_or_formula': 'm = Dezimalfuß × 0,3766242 (1 Dezimalfuß = 1/10 preuß. Ruthe)', 'reference': 'Brückner S. 11 Fußnote (Dezimalfuß, Pegel Swinemünde); S. 831: 1 preuß. Ruthe = 3,766242 m. Gegenprobe S. 12: Bahnhof Gera 607,53 rhein. Fuß = 190,7 m = 506 Dezimalfuß (gedruckt 502)'},
        {'from': 'Grad Réaumur (°R)', 'to': 'Grad Celsius (°C)', 'factor_or_formula': '°C = °R × 1,25', 'reference': '80 gegenüber 100 Teilstriche zwischen Eis- und Siedepunkt; von Brückner nicht tabelliert'},
    ],
    'caveats': [
        bi('Die Temperaturskala nennt Brückner nicht; angenommen wird Réaumur (S. 70). Die Reihen sind kurz und nicht gleichzeitig: ein Jahr (Lobenstein, Saalburg) bis zwölf Jahre (Gera). Höhen sind Ortshöhen, nicht die Höhe des Thermometers. Vier Punkte erlauben keine verlässliche Abnahmerate; die Gerade dient dem Vergleich.',
           'Brückner does not name the temperature scale; Réaumur is assumed (p. 70). The series are short and not simultaneous: one year (Lobenstein, Saalburg) to twelve years (Gera). Heights are heights of the places, not of the thermometer. Four points do not give a reliable lapse rate; the line serves for comparison.'),
        bi('Brückner hält die Werte von Schleiz, Rothenacker, Lobenstein und Saalburg im Vergleich mit Ziegenrück und Hohenleuben und gemessen an der Vegetation für zu hoch (S. 58). Instrument, Aufstellung und Beobachtungstermine sind nirgends angegeben; die Orte außerhalb von Gera wurden von Lehrern, Ärzten und Pfarrämtern beobachtet.',
           'Brückner considers the values of Schleiz, Rothenacker, Lobenstein and Saalburg too high compared with Ziegenrück and Hohenleuben and judged by the vegetation (p. 58). Instrument, exposure and times of observation are nowhere stated; outside Gera the observers were teachers, physicians and parish offices.'),
        bi('Ziegenrücks gedruckter Dezember (−4,33 °R) passt nicht zu seinen Winter- (1,25) und Jahresmitteln (5,65); diese verlangen etwa −0,43 °R. Lobensteins Oktober bis Dezember 1863 sind mit Rothenacker 1865 identisch. Beides steht so im Druck und wird unverändert gezeigt, geht aber nicht in die Abbildungen ein.',
           'Ziegenrück’s printed December (−4.33 °R) does not fit its winter (1.25) and annual means (5.65); these require about −0.43 °R. Lobenstein’s October to December 1863 are identical with Rothenacker 1865. Both stand so in the print and are shown unchanged, but do not enter the charts.'),
        bi('Die Reihen für Nebel, Niederschlag und Himmel sind 15 (Hohenleuben), 12 bzw. 10 (Gera), 2 (Schleiz) und 2 Jahre (Rothenacker) lang und stammen von verschiedenen Beobachtern. Hohenleuben trennt Regen und Schnee nicht. Die Gera-Reihe der Himmelsansicht (S. 64) nennt nur »in 10 Jahren«, keinen Zeitraum. Brückner spricht selbst von »auffällig starken Abweichungen« (S. 65).',
           'The series for fog, precipitation and sky are 15 (Hohenleuben), 12 or 10 (Gera), 2 (Schleiz) and 2 years (Rothenacker) long and come from different observers. Hohenleuben does not separate rain and snow. The Gera series of sky conditions (p. 64) states only »in 10 years«, no period. Brückner himself speaks of »striking deviations« (p. 65).'),
    ],
    'datasets': [d_st, d_tr, d_sd, d_sa, d_sp,
                 {k: base_places[k] for k in ('name', 'title', 'columns', 'rows', 'source_refs')},
                 {k: base_rivers[k] for k in ('name', 'title', 'columns', 'rows', 'source_refs')}],
    'charts': [c1, c2, c3],
    'keywords': {
        'de': ['Klima', 'Temperatur', 'Höhenlage', 'Messstationen', 'Hohenleuben', 'Schleiz', 'Rothenacker', 'Nebel', 'Bewölkung', 'Niederschlag', 'Quellentemperatur'],
        'en': ['climate', 'temperature', 'elevation', 'weather stations', 'Hohenleuben', 'Schleiz', 'Rothenacker', 'fog', 'cloud cover', 'precipitation', 'spring temperature'],
    },
    'related': ['klima-gera', 'wind-gewitter', 'relief-hoehen', 'phaenologie'],
    'generated_by': 'Claude Sonnet 5.5 (Agent F2), aus 5 Einzelauswertungen zusammengeführt',
    'date': '2026-10-02',
}
tr_issues = [t for a in (aH, aS, aN, aB, aQ) for t in (a.get('transcription_issues') or [])]
if tr_issues:
    f['transcription_issues'] = tr_issues

for key in ('summary', 'title'):
    for l in ('de', 'en'):
        print(key, l, words(f[key][l]))
for i, x in enumerate(f['findings']):
    print('finding', i, [words(x['de']), words(x['en'])])
for c in f['charts']:
    print(c['id'], 'title', words(c['title']['de']), words(c['title']['en']), 'caption', words(c['caption']['de']), words(c['caption']['en']))
print('method', words(f['method']['de']), words(f['method']['en']))
for c in f['caveats']:
    print('caveat', words(c['de']), words(c['en']))

write_feature(f)
