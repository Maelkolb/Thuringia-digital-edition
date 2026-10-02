from common import *

FID = 'phaenologie'
aB = load('phaenologie-bluetezeiten-gera-hohenleuben-1851-1861')
aV = load('phaenologie-zugvoegel-gera-1859-1864')

# ---------------------------------------------------------------- datasets
d_bl = ds(aB, 'bloom'); d_bl['name'] = 'bloom'
d_sp = ds(aB, 'spring'); d_sp['name'] = 'spring'
d_tr = ds(aB, 'trend'); d_tr['name'] = 'trend'
d_tt = ds(aB, 'trees'); d_tt['name'] = 'trees'
d_bs = ds(aV, 'species'); d_bs['name'] = 'bird_species'
d_bo = ds(aV, 'observations'); d_bo['name'] = 'bird_observations'

bl = rows(d_bl)
sp = rows(d_sp)
bs = rows(d_bs)
bo = rows(d_bo)

# ---------------------------------------------------------------- numbers
N = {}
G = {(r['species'], r['year']): r['doy'] for r in bl if r['station'] == 'Gera'}
H = {(r['species'], r['year']): r['doy'] for r in bl if r['station'] == 'Hohenleuben'}
common = sorted(set(y for _, y in G) & set(y for _, y in H))
print('common years', common)
pairs = [(k, H[k] - G[k]) for k in G if k in H]
N['pairs'] = len(pairs)
N['diff_mean'] = statistics.mean(d for _, d in pairs)
N['years_lo'], N['years_hi'] = common[0], common[-1]
per_sp = {}
for (s, y), d in pairs:
    per_sp.setdefault(s, []).append(d)
N['later_species'] = sum(1 for v in per_sp.values() if statistics.mean(v) > 0)
N['n_species'] = len(per_sp)
ELEV_G = (505 + 600) / 2
ELEV_H = (975 + 1050) / 2
N['dh_ft'] = ELEV_H - ELEV_G
N['schubler'] = N['dh_ft'] * 8 / 1000
# spread of dates per species and station (all years)
spread = {}
for st in ('Gera', 'Hohenleuben'):
    for s in set(k[0] for k in (G if st == 'Gera' else H)):
        v = [d for (ss, y), d in (G if st == 'Gera' else H).items() if ss == s]
        spread[(st, s)] = (max(v) - min(v), len(v))
N['spread_lo'] = min(v[0] for v in spread.values())
N['spread_hi'] = max(v[0] for v in spread.values())
hs = [r for r in sp if r['station'] == 'Hohenleuben' and r['temp_mar_may_c'] is not None]
xs = [r['temp_mar_may_c'] for r in hs]
ys = [r['index_days'] for r in hs]
N['r_temp'] = statistics.correlation(xs, ys)
N['slope'] = statistics.linear_regression(xs, ys).slope
N['n_temp'] = len(hs)
warm = max(hs, key=lambda r: r['temp_mar_may_c'])
cold = min(hs, key=lambda r: r['temp_mar_may_c'])
N['warm_year'], N['warm_idx'], N['warm_t'] = warm['year'], warm['index_days'], warm['temp_mar_may_c']
N['cold_year'], N['cold_idx'], N['cold_t'] = cold['year'], cold['index_days'], cold['temp_mar_may_c']
N['latest_year'] = max(hs, key=lambda r: r['index_days'])['year']
mean_arr = [r['mean_arrival_doy'] for r in bs]
mean_dep = [r['mean_departure_doy'] for r in bs]
N['r_birds'] = statistics.correlation(mean_arr, mean_dep)
N['n_birds'] = len(bs)
en_name = {r['species_de']: r['species_en'] for r in bs}
stays = [(r['mean_stay_days'], r['species_de']) for r in bs if r['mean_stay_days'] is not None]
N['stay_max'], N['stay_max_sp'] = max(stays)
N['stay_min'], N['stay_min_sp'] = min(stays)
N['arr_first'] = min((r['arrival_start'] for r in bo if r['arrival_start']), key=lambda x: x[5:])
N['arr_last'] = max((r['arrival_end'] for r in bo if r['arrival_end']), key=lambda x: x[5:])
N['dep_first'] = min((r['departure_start'] for r in bo if r['departure_start']), key=lambda x: x[5:])
N['dep_last'] = max((r['departure_end'] for r in bo if r['departure_end']), key=lambda x: x[5:])
print({k: (round(v, 2) if isinstance(v, float) else v) for k, v in N.items()})
print(spread[('Gera', 'Prunus cerasus')], spread[('Hohenleuben', 'Sambucus nigra')])
print([ (r['species_de'], r['arrival_start']) for r in bo if r['arrival_start'] == N['arr_first']], [ (r['species_de'], r['arrival_end']) for r in bo if r['arrival_end'] == N['arr_last']])
print([ (r['species_de'], r['departure_start']) for r in bo if r['departure_start'] == N['dep_first']], [ (r['species_de'], r['departure_end']) for r in bo if r['departure_end'] == N['dep_last']])


def dn(x, nd=1):
    return de_num(x, nd)


def en(x, nd=1):
    return en_num(x, nd)


MONTH_DE = {1: 'Januar', 2: 'Februar', 3: 'März', 4: 'April', 5: 'Mai', 6: 'Juni', 7: 'Juli', 8: 'August', 9: 'September', 10: 'Oktober', 11: 'November', 12: 'Dezember'}
MONTH_EN = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}


def date_de(iso):
    y, m, d = iso.split('-')
    return f'{int(d)}. {MONTH_DE[int(m)]}'


def date_en(iso):
    y, m, d = iso.split('-')
    return f'{MONTH_EN[int(m)]} {int(d)}'


# ---------------------------------------------------------------- c1: bloom calendar strips
doy_ticks = [60, 91, 121, 152, 182]
tick_de = "{'60':'1. März','91':'1. April','121':'1. Mai','152':'1. Juni','182':'1. Juli'}[datum.value]"
tick_en = "{'60':'Mar 1','91':'Apr 1','121':'May 1','152':'Jun 1','182':'Jul 1'}[datum.value]"
st_scale = {'domain': ['Gera', 'Hohenleuben'], 'range': ['@accent', '@accent2']}
y_enc = {'field': 'sp_label', 'type': 'nominal', 'sort': {'field': 'sp_mean', 'op': 'min'}, 'axis': {'title': None, 'labelLimit': 240, 'grid': True}}
yoff = {'field': 'station', 'type': 'nominal', 'sort': ['Gera', 'Hohenleuben']}
col = {'field': 'station', 'type': 'nominal', 'scale': st_scale, 'legend': None}
X = lambda f: {'field': f, 'type': 'quantitative'}
c_bloom = {
    'id': 'c2',
    'dataset': 'bloom',
    'title': bi(f"Hohenleuben blühte {N['years_lo']} bis {N['years_hi']} im Mittel {dn(N['diff_mean'])} Tage später als Gera",
                f"Hohenleuben flowered on average {en(N['diff_mean'])} days later than Gera in {N['years_lo']} to {N['years_hi']}"),
    'caption': bi(
        f"Tag des ersten Aufblühens von zwölf Pflanzen in den vier gemeinsamen Jahren {N['years_lo']} bis {N['years_hi']}: ein Punkt je Jahr, Strich: früheste bis späteste Blüte, Raute: Mittel. Sortiert nach mittlerem Termin. Quelle: S. 60.",
        f"Day of first flowering of twelve plants in the four common years {N['years_lo']} to {N['years_hi']}: one dot per year, line: earliest to latest, diamond: mean. Sorted by mean date. Source: p. 60."),
    'vegalite': {
        'height': {'step': 15},
        'transform': [
            {'filter': f"datum.year >= {N['years_lo']} && datum.year <= {N['years_hi']} && datum.species != 'Vitis vinifera'"},
            {'joinaggregate': [{'op': 'min', 'field': 'doy', 'as': 'dmin'}, {'op': 'max', 'field': 'doy', 'as': 'dmax'}, {'op': 'mean', 'field': 'doy', 'as': 'dmean'}], 'groupby': ['species', 'station']},
            {'joinaggregate': [{'op': 'mean', 'field': 'doy', 'as': 'sp_mean'}], 'groupby': ['species']},
            {'calculate': {'de': 'datum.species_de', 'en': 'datum.species_en'}, 'as': 'sp_label'},
        ],
        'encoding': {'y': y_enc, 'yOffset': yoff},
        'layer': [
            {
                'mark': {'type': 'rule', 'strokeWidth': 4, 'opacity': 0.35},
                'encoding': {
                    'x': dict(X('dmin'), scale={'domain': [70, 200], 'nice': False},
                              axis={'title': None, 'values': doy_ticks, 'labelExpr': {'de': tick_de, 'en': tick_en}, 'grid': True, 'labelAngle': 0}),
                    'x2': {'field': 'dmax'}, 'color': col},
            },
            {
                'mark': {'type': 'point', 'filled': True, 'size': 34, 'opacity': 0.9},
                'encoding': {
                    'x': X('doy'), 'color': col,
                    'tooltip': [
                        {'field': 'sp_label', 'title': bi('Pflanze', 'Plant')},
                        {'field': 'station', 'title': bi('Ort', 'Place')},
                        {'field': 'year', 'title': bi('Jahr', 'Year')},
                        {'field': 'printed', 'title': bi('Datum (gedruckt, Tag./Monat.)', 'Date (as printed, day/month)')},
                        {'field': 'doy', 'title': bi('Tag im Jahr', 'Day of year'), 'format': 'd'},
                    ],
                },
            },
            {
                'mark': {'type': 'point', 'shape': 'diamond', 'filled': True, 'size': 110, 'stroke': '@paper', 'strokeWidth': 1.2},
                'encoding': {'x': X('dmean'), 'color': col,
                             'tooltip': [{'field': 'sp_label', 'title': bi('Pflanze', 'Plant')}, {'field': 'station', 'title': bi('Ort', 'Place')},
                                         {'field': 'dmean', 'title': bi('Mittel (Tag im Jahr)', 'Mean (day of year)'), 'format': '.1f'}]},
            },
            {
                'transform': [{'filter': "datum.species == 'Viola odorata' && datum.year == " + str(N['years_hi'])}],
                'mark': {'type': 'text', 'style': 'label', 'align': 'left', 'dx': 9},
                'encoding': {'x': X('dmax'), 'text': {'field': 'station'}, 'color': col},
            },
        ],
    },
}

# ---------------------------------------------------------------- c2: temperature scatter
c_temp = {
    'id': 'c3',
    'dataset': 'spring',
    'extra_datasets': ['trend'],
    'title': bi(f"Je wärmer das Frühjahr, desto früher die Blüte: etwa {dn(abs(N['slope']), 0)} Tage je Grad",
                f"The warmer the spring, the earlier the flowering: about {en(abs(N['slope']), 0)} days per degree"),
    'caption': bi(
        f"Frühjahrsindex von Hohenleuben (mittlere Abweichung der zwölf Blühtermine eines Jahres vom Mittel der Art, in Tagen; positiv = später) gegen die Mitteltemperatur von März bis Mai (°C). Gerade: Regression, r = {dn(N['r_temp'], 2)}, {N['n_temp']} Jahre. Quelle: S. 56, 60.",
        f"Spring index of Hohenleuben (mean deviation of a year’s twelve flowering dates from the mean of the species, in days; positive = later) against the mean temperature of March to May (°C). Line: regression, r = {en(N['r_temp'], 2)}, {N['n_temp']} years. Source: pp. 56, 60."),
    'vegalite': {
        'height': 340,
        'transform': [{'filter': "datum.station == 'Hohenleuben' && isValid(datum.temp_mar_may_c)"}],
        'layer': [
            {
                'mark': {'type': 'rule', 'strokeDash': [3, 3], 'color': '@muted'},
                'encoding': {'y': {'datum': 0, 'type': 'quantitative', 'scale': {'domain': [-12, 12]},
                                   'axis': {'title': bi('Frühjahrsindex (Tage, positiv = später)', 'Spring index (days, positive = later)'), 'values': [-10, -5, 0, 5, 10], 'format': '+d',
                                            'labelExpr': "datum.value > 0 ? '+' + datum.value : (datum.value < 0 ? '\\u2212' + abs(datum.value) : '0')"}},
                             'x': None},
            },
            {
                'data': {'name': 'trend'},
                'mark': {'type': 'rule', 'color': '@ink2', 'strokeWidth': 1.5},
                'encoding': {
                    'x': {'field': 'x0', 'type': 'quantitative', 'scale': {'domain': [5.6, 9.1]}, 'axis': {'title': bi('Mitteltemperatur März bis Mai (°C)', 'Mean temperature March to May (°C)'), 'values': [6, 7, 8, 9], 'format': 'd', 'grid': False}},
                    'x2': {'field': 'x1'},
                    'y': {'field': 'y0', 'type': 'quantitative'},
                    'y2': {'field': 'y1'},
                },
            },
            {
                'mark': {'type': 'circle', 'size': 120, 'color': '@accent2', 'opacity': 1},
                'encoding': {
                    'x': {'field': 'temp_mar_may_c', 'type': 'quantitative'},
                    'y': {'field': 'index_days', 'type': 'quantitative'},
                    'tooltip': [
                        {'field': 'year', 'title': bi('Jahr', 'Year')},
                        {'field': 'temp_mar_may_c', 'title': bi('Mitteltemperatur März bis Mai (°C)', 'Mean temperature March to May (°C)'), 'format': '.1f'},
                        {'field': 'index_days', 'title': bi('Frühjahrsindex (Tage)', 'Spring index (days)'), 'format': '+.1f'},
                    ],
                },
            },
        ] + [
            {
                'transform': [{'filter': ('indexof([1861, 1858], datum.year) >= 0' if left else 'indexof([1861, 1858], datum.year) < 0')}],
                'mark': {'type': 'text', 'style': style, 'align': 'right' if left else 'left', 'dx': -10 if left else 10},
                'encoding': {'x': {'field': 'temp_mar_may_c', 'type': 'quantitative'}, 'y': {'field': 'index_days', 'type': 'quantitative'}, 'text': {'field': 'year', 'type': 'ordinal'}},
            }
            for left in (True, False) for style in ('place-halo', 'place-label')
        ] + [
            {
                'transform': [{'filter': 'datum.year == 1855'}],
                'mark': {'type': 'text', 'style': 'annotation', 'align': 'right', 'dy': -7, 'color': '@muted'},
                'encoding': {'x': {'datum': 9.05, 'type': 'quantitative'}, 'y': {'datum': 0, 'type': 'quantitative'},
                             'text': {'value': bi('Mittel der Art', 'mean of the species')}},
            },
            {
                'data': {'name': 'trend'},
                'transform': [{'calculate': 'datum.y0 + (6.2 - datum.x0) * (datum.y1 - datum.y0) / (datum.x1 - datum.x0)', 'as': 'y_at'}],
                'mark': {'type': 'text', 'style': 'annotation', 'align': 'left', 'dy': -15, 'dx': 2},
                'encoding': {'x': {'datum': 6.2, 'type': 'quantitative'}, 'y': {'field': 'y_at', 'type': 'quantitative'},
                             'text': {'value': bi(f"{dn(abs(N['slope']))} Tage früher je Grad", f"{en(abs(N['slope']))} days earlier per degree")}},
            },
        ],
    },
}

# ---------------------------------------------------------------- c3: birds
month_ticks = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
mt_de = "{'1':'Jan','32':'Feb','60':'Mär','91':'Apr','121':'Mai','152':'Jun','182':'Jul','213':'Aug','244':'Sep','274':'Okt','305':'Nov','335':'Dez'}[datum.value]"
mt_en = "{'1':'Jan','32':'Feb','60':'Mar','91':'Apr','121':'May','152':'Jun','182':'Jul','213':'Aug','244':'Sep','274':'Oct','305':'Nov','335':'Dec'}[datum.value]"
bird_x_scale = {'domain': [20, 380], 'nice': False}
bird_x_axis = {'title': None, 'values': month_ticks, 'labelExpr': {'de': mt_de, 'en': mt_en}, 'grid': True, 'labelAngle': 0, 'labelAlign': 'left', 'labelOffset': 2}
bird_y = {'field': 'sp_label', 'type': 'nominal', 'sort': {'field': 'mean_arrival_doy', 'op': 'min'}, 'axis': {'title': None, 'labelLimit': 250, 'grid': True}}
bird_calc = [{'calculate': {'de': 'datum.species_de', 'en': 'datum.species_en'}, 'as': 'sp_label'}]
c_bird = {
    'id': 'c1',
    'dataset': 'bird_species',
    'extra_datasets': ['bird_observations'],
    'title': bi(f"Je später die Ankunft, desto früher der Abzug: Die {N['stay_max_sp']} bleibt {N['stay_max']:.0f} Tage, die {N['stay_min_sp']} {N['stay_min']:.0f}",
                f"Later arrival, earlier departure: the {en_name[N['stay_max_sp']].lower()} stays {N['stay_max']:.0f} days, the {en_name[N['stay_min_sp']].lower()} {N['stay_min']:.0f}"),
    'caption': bi(
        'Ludwig Müllers Beobachtungen in Gera 1859 bis 1864. Balken: vom mittleren Ankunftstermin zum mittleren Abzugstermin der Art; Punkte: einzelne Jahre; Zahl: mittlere Aufenthaltsdauer der Jahre mit Ankunft und Abzug. Sortiert nach Ankunft. Quelle: S. 61.',
        'Ludwig Müller’s observations at Gera, 1859 to 1864. Bar: from the mean arrival date to the mean departure date of the species; dots: single years; number: mean length of stay in years with both arrival and departure. Sorted by arrival. Source: p. 61.'),
    'vegalite': {
        'height': {'step': 24},
        'transform': bird_calc,
        'encoding': {'y': bird_y},
        'layer': [
            {
                'mark': {'type': 'bar', 'height': 10, 'cornerRadius': 5, 'color': '@accent', 'opacity': 0.85},
                'encoding': {
                    'x': dict(X('mean_arrival_doy'), scale=bird_x_scale, axis=bird_x_axis),
                    'x2': {'field': 'mean_departure_doy'},
                    'tooltip': [
                        {'field': 'sp_label', 'title': bi('Art', 'Species')},
                        {'field': 'mean_arrival_doy', 'title': bi('mittlere Ankunft (Tag im Jahr)', 'mean arrival (day of year)'), 'format': '.0f'},
                        {'field': 'mean_departure_doy', 'title': bi('mittlerer Abzug (Tag im Jahr)', 'mean departure (day of year)'), 'format': '.0f'},
                        {'field': 'mean_stay_days', 'title': bi('mittlere Aufenthaltsdauer (Tage)', 'mean length of stay (days)'), 'format': '.0f'},
                    ],
                },
            },
            {
                'data': {'name': 'bird_observations'},
                'transform': bird_calc,
                'mark': {'type': 'point', 'filled': True, 'size': 24, 'color': '@ink2', 'opacity': 0.8, 'stroke': '@paper', 'strokeWidth': 0.8},
                'encoding': {'x': X('arrival_doy'), 'y': bird_y,
                             'tooltip': [{'field': 'sp_label', 'title': bi('Art', 'Species')}, {'field': 'year', 'title': bi('Jahr', 'Year')},
                                         {'field': 'arrival_printed', 'title': bi('Ankunft (gedruckt)', 'Arrival (as printed)')}]},
            },
            {
                'data': {'name': 'bird_observations'},
                'transform': bird_calc + [{'filter': 'isValid(datum.departure_doy)'}],
                'mark': {'type': 'point', 'filled': True, 'size': 24, 'color': '@ink2', 'opacity': 0.8, 'stroke': '@paper', 'strokeWidth': 0.8},
                'encoding': {'x': X('departure_doy'), 'y': bird_y,
                             'tooltip': [{'field': 'sp_label', 'title': bi('Art', 'Species')}, {'field': 'year', 'title': bi('Jahr', 'Year')},
                                         {'field': 'departure_printed', 'title': bi('Abzug (gedruckt)', 'Departure (as printed)')}]},
            },
            {
                'transform': [{'filter': 'isValid(datum.mean_stay_days)'},
                              {'calculate': {'de': "format(datum.mean_stay_days, '.0f') + ' Tage'", 'en': "format(datum.mean_stay_days, '.0f') + ' days'"}, 'as': 'stay_lab'}],
                'mark': {'type': 'text', 'style': 'label', 'align': 'right'},
                'encoding': {'x': {'datum': 380, 'type': 'quantitative', 'scale': bird_x_scale, 'axis': bird_x_axis}, 'text': {'field': 'stay_lab'}},
            },
        ],
    },
}

# ---------------------------------------------------------------- feature
f = {
    'id': FID,
    'title': bi('Vogelzug und Blüte im Jahreslauf', 'Bird migration and flowering through the year'),
    'category': 'phenology',
    'section': 't1-1-7',
    'merges': ['phaenologie-bluetezeiten-gera-hohenleuben-1851-1861', 'phaenologie-zugvoegel-gera-1859-1864'],
    'sources': [
        {'page': '60', 'block': 'b2'}, {'page': '60', 'block': 'b3'}, {'page': '60', 'block': 'b5', 'rows': 'r1-r13'}, {'page': '60', 'block': 'b7', 'rows': 'r1-r14'},
        {'page': '61', 'block': 'b2', 'rows': 'r1-r3'}, {'page': '61', 'block': 'b3'}, {'page': '61', 'block': 'b4'}, {'page': '61', 'block': 'b5', 'rows': 'r1-r16'},
        {'page': '56', 'block': 'b2', 'rows': 'r2-r9'}, {'page': '12', 'block': 'b1', 'rows': 'r1'}, {'page': '20', 'block': 'b3', 'rows': 'r16'},
    ],
    'summary': bi(
        f"Brückner druckt Ankunft und Abzug von {N['n_birds']} Zugvögeln in Gera (1859 bis 1864) sowie die Tage des ersten Aufblühens von zwölf Pflanzen in Gera (1851 bis 1856) und Hohenleuben (1853 bis 1861). Die Vögel kamen zwischen dem {date_de(N['arr_first'])} und dem {date_de(N['arr_last'])} an und zogen zwischen dem {date_de(N['dep_first'])} und dem {date_de(N['dep_last'])} ab. Hohenleuben blühte {N['years_lo']} bis {N['years_hi']} im Mittel {dn(N['diff_mean'])} Tage später als Gera.",
        f"Brückner prints the arrival and departure of {N['n_birds']} migratory birds at Gera (1859 to 1864) and the days of first flowering of twelve plants at Gera (1851 to 1856) and Hohenleuben (1853 to 1861). The birds arrived between {date_en(N['arr_first'])} and {date_en(N['arr_last'])} and left between {date_en(N['dep_first'])} and {date_en(N['dep_last'])}. Hohenleuben flowered on average {en(N['diff_mean'])} days later than Gera in {N['years_lo']} to {N['years_hi']}."),
    'findings': [
        bi(f"Je später die Ankunft, desto früher der Abzug (r = {dn(N['r_birds'], 2)} über {N['n_birds']} Arten). Die mittlere Aufenthaltsdauer reicht von {N['stay_min']:.0f} Tagen ({N['stay_min_sp']}) bis {N['stay_max']:.0f} ({N['stay_max_sp']}).",
           f"The later the arrival, the earlier the departure (r = {en(N['r_birds'], 2)} across {N['n_birds']} species). The mean length of stay ranges from {N['stay_min']:.0f} days ({en_name[N['stay_min_sp']].lower()}) to {N['stay_max']:.0f} ({en_name[N['stay_max_sp']].lower()})."),
        bi(f"Hohenleuben blühte {N['years_lo']} bis {N['years_hi']} bei {N['later_species']} von {N['n_species']} Arten im Mittel später als Gera ({N['pairs']} Paare). Schüblers Regel von 8 Tagen je 1000 Fuß ergäbe bei rund {N['dh_ft']:.0f} Fuß Höhenunterschied {dn(N['schubler'])} Tage.",
           f"In {N['years_lo']} to {N['years_hi']} Hohenleuben flowered later than Gera in {N['later_species']} of {N['n_species']} species ({N['pairs']} pairs). Schübler’s rule (8 days per 1,000 feet) gives {en(N['schubler'])} days for the {N['dh_ft']:.0f} feet difference in height."),
        bi(f"Je Grad wärmerem Frühjahr (März bis Mai) blühte es in Hohenleuben etwa {dn(abs(N['slope']))} Tage früher (r = {dn(N['r_temp'], 2)}, {N['n_temp']} Jahre). {N['warm_year']} war das wärmste Frühjahr und das früheste, {N['cold_year']} das kälteste und spät.",
           f"Per degree of warmer spring (March to May), flowering at Hohenleuben came about {en(abs(N['slope']))} days earlier (r = {en(N['r_temp'], 2)}, {N['n_temp']} years). {N['warm_year']} was warmest and earliest, {N['cold_year']} coldest and late."),
    ],
    'method': bi(
        'Brückner druckt die Termine als Brüche, bei denen der Monat der Nenner und der Tag der Zähler ist (S. 60). Sie sind in Tage des Jahres umgesetzt (normiertes Jahr ohne Schalttag, 1. Januar = 1; 1. März = 60, 1. Juli = 182). Die lateinischen Namen sind im Druck teils abgekürzt und vereinheitlicht; deutsche und englische Namen sind eine editorische Zuordnung. Der Frühjahrsindex eines Jahres ist das Mittel der Abweichungen der Blühtermine aller Arten (außer der Weinrebe) vom Mittel der jeweiligen Art an derselben Station; positive Werte bedeuten späte Blüte. Die Mitteltemperatur März bis Mai von Hohenleuben stammt aus den Monatsmitteln auf S. 56 (°R × 1,25); das Jahr 1853 hat keine Temperatur. Die Höhen der Ortslagen (Gera 505 bis 600, Hohenleuben 975 bis 1050 Dezimalfuß, S. 12 und 20) ergeben mit ihren Mitten 460 Fuß Unterschied.\n'
        'Bei den Zugvögeln (S. 61) sind Tagesspannen der Ankunft (»21.–26./4.«) mit ihrer Mitte eingesetzt. Der Balken verbindet die mittlere Ankunft mit dem mittleren Abzug der Art aus allen vorhandenen Jahren; die Aufenthaltsdauer ist Abzug minus Ankunft desselben Jahres und nur bei vollständigem Paar berechnet. Die Entwicklungsstufen von Rosskastanie und Birnbaum (S. 61) stehen als Tabelle »trees« im Datensatz.',
        'Brückner prints the dates as fractions in which the month is the denominator and the day the numerator (p. 60). They are converted to days of the year (normalized year without leap day, 1 January = 1; 1 March = 60, 1 July = 182). The Latin names are partly abbreviated in the print and have been unified; German and English names are an editorial assignment. The spring index of a year is the mean of the deviations of the flowering dates of all species (except grapevine) from the mean of that species at the same station; positive values mean late flowering. The mean temperature March to May for Hohenleuben comes from the monthly means on p. 56 (°R × 1.25); the year 1853 has no temperature. The heights of the places (Gera 505 to 600, Hohenleuben 975 to 1050 decimal feet, pp. 12 and 20) give a difference of 460 feet between their midpoints.\n'
        'For the migratory birds (p. 61), ranges of days for arrival (»21.–26./4.«) are entered at their midpoint. The bar joins the mean arrival with the mean departure of the species from all available years; the length of stay is departure minus arrival of the same year and is computed only for complete pairs. The development stages of horse chestnut and pear tree (p. 61) are in the dataset as the table »trees«.'),
    'conversions': [
        {'from': 'Datumsbruch (Tag./Monat.)', 'to': 'Tag im Jahr', 'factor_or_formula': 'Tag im Jahr = Tage vor Monatsbeginn (Nicht-Schaltjahr) + Tag; bei Tagesspannen Mitte der Spanne', 'reference': 'Erläuterung Brückner S. 60: Monat als Nenner, Tag als Zähler'},
        {'from': 'Grad Réaumur (°R)', 'to': 'Grad Celsius (°C)', 'factor_or_formula': '°C = °R × 1,25', 'reference': 'von Brückner nicht tabelliert'},
    ],
    'caveats': [
        bi('Die Termine sind »erstes Aufblühen« bzw. Ankunft und Abzug; Beobachter und Kriterien sind kaum beschrieben. Die Reihen sind kurz: Gera sechs, Hohenleuben neun Jahre, die Vögel sechs Jahre eines Beobachters. Nur 32 von 84 möglichen Art-Jahr-Kombinationen haben Ankunft und Abzug.',
           'The dates mean »first flowering« or arrival and departure; observers and criteria are barely described. The series are short: six years at Gera, nine at Hohenleuben, six years of one observer for the birds. Only 32 of 84 possible species-year combinations have both arrival and departure.'),
        bi('In 5 von 25 Zeilen weicht Brückners Spalte »Tage der Differenz« um 1 bis 3 Tage von den gedruckten Terminen ab. Der Weißdorn in Hohenleuben blühte 1858 und 1860 vor dem Apfel (3. und 2. Mai); das Faksimile bestätigt die Zahlen. Die Daten werden unverändert gezeigt.',
           'In 5 of 25 rows Brückner’s column »days of difference« deviates by 1 to 3 days from the printed dates. The hawthorn at Hohenleuben flowered before the apple in 1858 and 1860 (3 and 2 May); the facsimile confirms the figures. The data are shown unchanged.'),
        bi('Der Zusammenhang mit der Temperatur beruht auf acht Jahren einer Station und ist explorativ; die Temperaturskala (Réaumur) ist nicht ausdrücklich genannt. Brückner hält Schüblers Höhenregel für das Land für zu schwach (S. 61); der Vergleich Gera und Hohenleuben stützt sie hier nur zufällig.',
           'The link with temperature rests on eight years from one station and is exploratory; the temperature scale (Réaumur) is not stated explicitly. Brückner considers Schübler’s height rule too weak for the country (p. 61); the comparison of Gera and Hohenleuben supports it here only by chance.'),
        bi('Die Artbestimmung der alten Vogelnamen ist unsicher: »Hausschwalbe« kann Rauch- oder Mehlschwalbe meinen, »Bachstelze« neben der Weißen Bachstelze eine andere Art; die Turmschwalbe ist der Mauersegler. Überwinterer wie Lerche und Star sind in milden Wintern kaum von Zugvögeln zu trennen.',
           'The identification of the old bird names is uncertain: »Hausschwalbe« can mean barn swallow or house martin, »Bachstelze« next to the White Wagtail another species; the »Turmschwalbe« is the swift. Overwintering birds such as skylark and starling can hardly be told from migrants in mild winters.'),
    ],
    'datasets': [d_bl, d_sp, d_tr, d_bs, d_bo, d_tt],
    'charts': [c_bird, c_bloom, c_temp],
    'keywords': {
        'de': ['Phänologie', 'Blüte', 'Blühtermine', 'Zugvögel', 'Vogelzug', 'Ankunft', 'Abzug', 'Gera', 'Hohenleuben', 'Frühling', 'Schübler'],
        'en': ['phenology', 'flowering', 'bloom dates', 'migratory birds', 'bird migration', 'arrival', 'departure', 'Gera', 'Hohenleuben', 'spring', 'Schübler'],
    },
    'related': ['klima-gera', 'klima-stationen', 'pflanzenwelt', 'tierwelt'],
    'generated_by': 'Claude Sonnet 5.5 (Agent F2), aus 2 Einzelauswertungen zusammengeführt',
    'date': '2026-10-02',
}
tr_issues = [t for a in (aB, aV) for t in (a.get('transcription_issues') or [])]
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
