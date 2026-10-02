from common import *

FID = 'wind-gewitter'
aG = load('klima-wind-gera-1856-1865')
aV = load('klima-wind-stationen-vergleich')
aT = load('klima-gewitter-gera-stationen')

# ---------------------------------------------------------------- datasets
d_ws = ds(aV, 'annual'); d_ws['name'] = 'wind_stations'
d_wg = ds(aG, 'monthly'); d_wg['name'] = 'wind_gera_monthly'
d_tm = ds(aT, 'monthly'); d_tm['name'] = 'thunder_monthly'
d_ta = ds(aT, 'annual'); d_ta['name'] = 'thunder_annual'
d_td = ds(aT, 'direction'); d_td['name'] = 'thunder_direction'

ws = rows(d_ws)
wg = rows(d_wg)
tm = rows(d_tm)
ta = rows(d_ta)
td = rows(d_td)

# ---------------------------------------------------------------- numbers
N = {}
share = {(r['station'], r['direction']): r['share'] for r in ws}
for k in [('Gera', 'S'), ('Gera', 'N'), ('Hohenleuben', 'W'), ('Schleiz', 'SW'), ('Schleiz', 'W'), ('Rothenacker', 'W'), ('Rothenacker', 'SW')]:
    N['%s_%s' % k] = share[k]
N['gera_total'] = sum(r['count'] for r in ws if r['station'] == 'Gera')
gm = {(r['month'], r['direction']): r['month_share'] for r in wg}
N['S_jan'] = gm[(1, 'S')]
N['S_jun'] = gm[(6, 'S')]
N['W_jul'] = gm[(7, 'W')]
N['N_apr'] = gm[(4, 'N')]
winter_months = (12, 1, 2)
summer_months = (6, 7, 8)


def season_share(direction, months):
    num = sum(r['count'] for r in wg if r['direction'] == direction and r['month'] in months)
    den = sum(r['count'] for r in wg if r['month'] in months)
    return 100 * num / den


N['S_winter'] = season_share('S', winter_months)
N['S_summer'] = season_share('S', summer_months)
N['W_summer'] = season_share('W', summer_months)
N['N_summer'] = season_share('N', summer_months)
# summer: W and N are the two most frequent directions in the three months together
summer_rank = sorted(['N', 'NO', 'O', 'SO', 'S', 'SW', 'W', 'NW'], key=lambda d: -season_share(d, summer_months))
print('summer rank', summer_rank[:3], [round(season_share(d, summer_months), 1) for d in summer_rank[:3]])
winter_rank = sorted(['N', 'NO', 'O', 'SO', 'S', 'SW', 'W', 'NW'], key=lambda d: -season_share(d, winter_months))
print('winter rank', winter_rank[:3], [round(season_share(d, winter_months), 1) for d in winter_rank[:3]])

YEARS_TOTAL = sum({(r['period']): r['years'] for r in tm}.values())
assert YEARS_TOTAL == 15
tot = {}
for r in tm:
    tot[r['month']] = tot.get(r['month'], 0) + (r['count'] or 0)
N['thunder_total'] = sum(tot.values())
N['thunder_summer'] = tot[6] + tot[7] + tot[8]
N['thunder_summer_pct'] = 100 * N['thunder_summer'] / N['thunder_total']
N['thunder_nov'] = tot[11]
N['thunder_may_sep_pct'] = 100 * sum(tot[m] for m in (5, 6, 7, 8, 9)) / N['thunder_total']
ann = {(r['station'], r['kind']): r for r in ta}
N['g_py'] = ann[('Gera', 'mean')]['per_year']
N['s_py'] = ann[('Schleiz', 'mean')]['per_year']
N['r_py'] = ann[('Rothenacker', 'mean')]['per_year']
dirshare = {(r['station'], r['direction']): r['share'] for r in td}
N['thunder_W_hoh'] = dirshare[('Hohenleuben', 'W')]
N['thunder_W_gera'] = dirshare[('Gera', 'W')]
N['thunder_S_gera'] = dirshare[('Gera', 'S')]
print({k: (round(v, 2) if isinstance(v, float) else v) for k, v in N.items()})
thunder_peak = {m: tot[m] / YEARS_TOTAL for m in tot}
print({m: round(v, 2) for m, v in thunder_peak.items()})


GT_DE = f"{N['gera_total']:,}".replace(',', '.')
GT_EN = f"{N['gera_total']:,}"


def dn(x, nd=1):
    return de_num(x, nd)


def en(x, nd=1):
    return en_num(x, nd)


# ---------------------------------------------------------------- c1: roses
R_MAX = 58
K = R_MAX / math.sqrt(40)
ring_delta = round(1.2 / K, 4)
THETA = {'domain': [0.5, 8.5], 'range': [-0.3927, 5.8905]}
dir_label = {'de': 'datum.direction', 'en': "{'N':'N','NO':'NE','O':'E','SO':'SE','S':'S','SW':'SW','W':'W','NW':'NW'}[datum.direction]"}
station_label = {
    'de': "{'Gera':'Gera 1856–1865','Hohenleuben':'Hohenleuben (7 Jahre)','Schleiz':'Schleiz 1866–1867','Rothenacker':'Rothenacker 1867'}[datum.station]",
    'en': "{'Gera':'Gera 1856–1865','Hohenleuben':'Hohenleuben (7 years)','Schleiz':'Schleiz 1866–1867','Rothenacker':'Rothenacker 1867'}[datum.station]",
}


def theta_enc(field):
    return {'field': field, 'type': 'quantitative', 'scale': dict(THETA), 'stack': False}


def radius_enc(field='share'):
    return {'field': field, 'type': 'quantitative', 'scale': {'type': 'sqrt', 'domain': [0, 40], 'rangeMax': R_MAX}}


c1 = {
    'id': 'c1',
    'dataset': 'wind_stations',
    'title': bi('In Gera dominiert der Südwind, an den Oberlandorten Südwest bis West',
                'At Gera the south wind dominates, at the Oberland places south-west to west'),
    'caption': bi(
        'Anteil der acht Richtungen an den Windbeobachtungen (Fläche der Keile proportional, Ringe bei 10, 20, 30 und 40 Prozent). Farbig: Richtungen mit mindestens 20 Prozent. Beobachtungsreihen unterschiedlich lang (10, 7, 2 und 1 Jahr). Quelle: S. 62 bis 64.',
        'Share of the eight directions among the wind observations (wedge area proportional, rings at 10, 20, 30 and 40 percent). Colored: directions with at least 20 percent. Series of different length (10, 7, 2 and 1 years). Source: pp. 62 to 64.'),
    'vegalite': {
        'autosize': {'type': 'pad'},
        'columns': 4,
        'spacing': 6,
        'facet': {'field': 'station_label', 'type': 'nominal', 'sort': {'field': 'station_order', 'op': 'min'}, 'title': None},
        'spec': {
            'width': 200,
            'height': 200,
            'layer': [
                {
                    'transform': [
                        {'filter': 'datum.dir_index == 1'},
                        {'calculate': '[10, 20, 30, 40]', 'as': 'ring'},
                        {'flatten': ['ring']},
                        {'calculate': f'pow(sqrt(datum.ring) - {ring_delta}, 2)', 'as': 'ring_in'},
                    ],
                    'mark': {'type': 'arc', 'opacity': 0.55, 'strokeWidth': 0, 'color': '@context'},
                    'encoding': {
                        'theta': {'value': 0}, 'theta2': {'value': 6.2832},
                        'radius': {'field': 'ring', 'type': 'quantitative', 'scale': {'type': 'sqrt', 'domain': [0, 40], 'rangeMax': R_MAX}},
                        'radius2': {'field': 'ring_in', 'type': 'quantitative'},
                    },
                },
                {
                    'mark': {'type': 'arc'},
                    'encoding': {
                        'theta': theta_enc('dir_lo'), 'theta2': {'field': 'dir_hi'},
                        'radius': radius_enc(),
                        'color': {'condition': {'test': 'datum.share >= 20', 'value': '@accent'}, 'value': '@context'},
                        'tooltip': [
                            {'field': 'station_label', 'title': bi('Ort', 'Place')},
                            {'field': 'dir_label', 'title': bi('Richtung', 'Direction')},
                            {'field': 'share', 'title': bi('Anteil (%)', 'Share (%)'), 'format': '.1f'},
                            {'field': 'count', 'title': bi('Beobachtungen', 'Observations'), 'format': ',d'},
                        ],
                    },
                },
                {
                    'transform': [{'filter': 'datum.share >= 20'}, {'calculate': "format(datum.share, '.0f') + ' %'", 'as': 'vlab'}],
                    'mark': {'type': 'text', 'style': 'label', 'radiusOffset': 8},
                    'encoding': {'theta': theta_enc('dir_index'), 'radius': radius_enc(), 'text': {'field': 'vlab'}},
                },
                {
                    'mark': {'type': 'text', 'style': 'label-muted', 'fontSize': 11},
                    'encoding': {'theta': theta_enc('dir_index'), 'radius': {'value': 90}, 'text': {'field': 'dir_label'}},
                },
            ],
        },
        'transform': [
            {'calculate': station_label, 'as': 'station_label'},
            {'calculate': dir_label, 'as': 'dir_label'},
            {'calculate': 'datum.dir_index - 0.5', 'as': 'dir_lo'},
            {'calculate': 'datum.dir_index + 0.5', 'as': 'dir_hi'},
        ],
    },
}

# ---------------------------------------------------------------- c2: Gera by month, S / W / N highlighted
dirname = {'de': "{'S':'Süd','W':'West','N':'Nord'}[datum.direction]", 'en': "{'S':'South','W':'West','N':'North'}[datum.direction]"}
c2 = {
    'id': 'c2',
    'dataset': 'wind_gera_monthly',
    'title': bi('In Gera weht im Winter vor allem Südwind, im Sommer überwiegen West und Nord',
                'At Gera the south wind prevails in winter; in summer west and north lead'),
    'caption': bi(
        'Anteil der Richtungen an den Windbeobachtungen jedes Monats in Gera, 1856 bis 1865 (Prozent). Farbig: Süd, West und Nord; grau: die fünf übrigen Richtungen. Quelle: S. 62.',
        'Share of the directions among the wind observations of each month at Gera, 1856 to 1865 (percent). Colored: south, west and north; gray: the five other directions. Source: p. 62.'),
    'vegalite': {
        'height': 320,
        'encoding': {
            'x': {'field': 'month', 'type': 'quantitative', 'scale': {'domain': [0.7, 12.3], 'nice': False},
                  'axis': {'title': None, 'values': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 'labelExpr': month_axis_expr(), 'grid': False}},
            'y': {'field': 'month_share', 'type': 'quantitative', 'scale': {'domain': [0, 45]},
                  'axis': {'title': bi('Anteil der Beobachtungen (%)', 'Share of observations (%)'), 'values': [0, 10, 20, 30, 40]}},
        },
        'layer': [
            {
                'transform': [{'filter': "indexof(['S','W','N'], datum.direction) < 0"}],
                'mark': {'type': 'line', 'strokeWidth': 1.5, 'color': '@context'},
                'encoding': {'detail': {'field': 'direction'}},
            },
            {
                'transform': [{'filter': "indexof(['S','W','N'], datum.direction) >= 0"}],
                'mark': {'type': 'line', 'strokeWidth': 3},
                'encoding': {'color': {'field': 'direction', 'type': 'nominal', 'legend': None,
                                       'scale': {'domain': ['S', 'W', 'N'], 'range': ['@accent', '@accent2', '@accent3']}}},
            },
            {
                'transform': [{'filter': "indexof(['S','W','N'], datum.direction) >= 0"}],
                'mark': {'type': 'point', 'filled': True, 'size': 28},
                'encoding': {
                    'color': {'field': 'direction', 'type': 'nominal', 'legend': None,
                              'scale': {'domain': ['S', 'W', 'N'], 'range': ['@accent', '@accent2', '@accent3']}},
                    'tooltip': [
                        {'field': 'month_label', 'title': bi('Monat', 'Month')},
                        {'field': 'direction', 'title': bi('Richtung', 'Direction')},
                        {'field': 'month_share', 'title': bi('Anteil (%)', 'Share (%)'), 'format': '.1f'},
                        {'field': 'count', 'title': bi('Beobachtungen', 'Observations'), 'format': 'd'},
                    ],
                },
            },
            {
                'transform': [{'filter': "(datum.direction == 'S' && datum.month == 1) || (datum.direction == 'W' && datum.month == 7) || (datum.direction == 'N' && datum.month == 4)"},
                              {'calculate': dirname, 'as': 'dname'},
                              {'calculate': "datum.dname + ' ' + format(datum.month_share, '.0f') + ' %'", 'as': 'lab'}],
                'mark': {'type': 'text', 'style': 'label', 'dy': -12, 'align': 'center'},
                'encoding': {'text': {'field': 'lab'},
                             'color': {'field': 'direction', 'type': 'nominal', 'legend': None,
                                       'scale': {'domain': ['S', 'W', 'N'], 'range': ['@accent', '@accent2', '@accent3']}}},
            },
        ],
    },
}

# ---------------------------------------------------------------- c3: thunderstorms by month
thunder_pct = f"{N['thunder_summer_pct']:.0f}"
c3 = {
    'id': 'c3',
    'dataset': 'thunder_monthly',
    'title': bi(f"Gewitter in Gera: {thunder_pct} Prozent fallen in Juni bis August, im November gab es keines",
                f"Thunderstorms at Gera: {thunder_pct} percent fall in June to August, none occurred in November"),
    'caption': bi(
        f'Mittlere Zahl der Gewitter pro Jahr und Monat in Gera, 1853 bis 1867 ({N["thunder_total"]} Gewitter in 15 Jahren, Perioden 1853 bis 1858 und 1859 bis 1867 zusammengefasst). Quelle: S. 67, Berichtigung S. 830.',
        f'Mean number of thunderstorms per year and month at Gera, 1853 to 1867 ({N["thunder_total"]} thunderstorms in 15 years, periods 1853 to 1858 and 1859 to 1867 combined). Source: p. 67, correction p. 830.'),
    'vegalite': {
        'height': 280,
        'transform': [
            {'calculate': 'isValid(datum.count) ? datum.count : 0', 'as': 'count0'},
            {'aggregate': [{'op': 'sum', 'field': 'count0', 'as': 'total'}], 'groupby': ['month']},
            {'calculate': f'datum.total / {YEARS_TOTAL}', 'as': 'per_year'},
        ],
        'encoding': {
            'x': {'field': 'month', 'type': 'ordinal', 'axis': {'title': None, 'labelAngle': 0, 'labelExpr': month_axis_expr()}},
            'y': {'field': 'per_year', 'type': 'quantitative', 'scale': {'domain': [0, 6.5]},
                  'axis': {'title': bi('Gewitter pro Jahr', 'Thunderstorms per year'), 'values': [0, 2, 4, 6]}},
        },
        'layer': [
            {
                'mark': {'type': 'bar', 'width': {'band': 0.72}},
                'encoding': {
                    'color': {'condition': {'test': 'datum.month >= 6 && datum.month <= 8', 'value': '@accent'}, 'value': '@context'},
                    'tooltip': [
                        {'field': 'month', 'title': bi('Monat', 'Month')},
                        {'field': 'total', 'title': bi('Gewitter in 15 Jahren', 'Thunderstorms in 15 years'), 'format': 'd'},
                        {'field': 'per_year', 'title': bi('pro Jahr', 'per year'), 'format': '.1f'},
                    ],
                },
            },
            {
                'transform': [{'filter': 'datum.per_year >= 0.5'}],
                'mark': {'type': 'text', 'style': 'label', 'dy': -7},
                'encoding': {'text': {'field': 'per_year', 'type': 'quantitative', 'format': '.1f'}},
            },
            {
                'transform': [{'filter': 'datum.total == 0'}],
                'mark': {'type': 'text', 'style': 'annotation', 'dy': -9},
                'encoding': {'text': {'value': bi('keines', 'none')}},
            },
            {
                'transform': [{'filter': 'datum.month == 7'}],
                'mark': {'type': 'text', 'style': 'label', 'color': '@accent'},
                'encoding': {'y': {'datum': 6.2, 'type': 'quantitative'},
                             'text': {'value': bi(f"{thunder_pct} Prozent der Gewitter", f"{thunder_pct} percent of the thunderstorms")}},
            },
        ],
    },
}

# ---------------------------------------------------------------- the feature
f = {
    'id': FID,
    'title': bi('Wind und Gewitter', 'Wind and thunderstorms'),
    'category': 'climate',
    'section': 't1-1-7',
    'merges': ['klima-wind-gera-1856-1865', 'klima-wind-stationen-vergleich', 'klima-gewitter-gera-stationen'],
    'sources': [
        {'page': '54', 'block': 'b1'}, {'page': '62', 'block': 'b1'}, {'page': '62', 'block': 'b3', 'rows': 'r2-r15'},
        {'page': '63', 'block': 'b2', 'rows': 'r2-r15'}, {'page': '63', 'block': 'b4', 'rows': 'r2-r15'}, {'page': '63', 'block': 'b6', 'rows': 'r2-r15'},
        {'page': '64', 'block': 'b1'}, {'page': '66', 'block': 'b3', 'rows': 'r2-r15'}, {'page': '67', 'block': 'b2', 'rows': 'r2-r15'},
        {'page': '67', 'block': 'b6'}, {'page': '67', 'block': 'b7', 'rows': 'r2-r4'}, {'page': '68', 'block': 'b2', 'rows': 'r2-r4'}, {'page': '830', 'block': 'b4'},
    ],
    'summary': bi(
        f"Brückner wertet Windrichtungen und Gewitter aus. In Gera (1856 bis 1865, {GT_DE} Beobachtungen) ist Süd die häufigste Richtung ({dn(N['Gera_S'])} Prozent), auf den Oberlandorten Hohenleuben, Schleiz und Rothenacker überwiegen West und Südwest. Gewitter zählt er in Gera {dn(N['g_py'])} im Jahr, {thunder_pct} Prozent davon im Juni bis August.",
        f"Brückner analyzes wind directions and thunderstorms. At Gera (1856 to 1865, {GT_EN} observations) south is the most frequent direction ({en(N['Gera_S'])} percent); at the Oberland places of Hohenleuben, Schleiz and Rothenacker west and south-west prevail. He counts {en(N['g_py'])} thunderstorms a year at Gera, {thunder_pct} percent of them in June to August."),
    'findings': [
        bi(f"In Gera kommen {dn(N['Gera_S'])} Prozent der Winde aus Süd und {dn(N['Gera_N'])} aus Nord; in Hohenleuben {dn(N['Hohenleuben_W'])} Prozent aus West, in Schleiz {dn(N['Schleiz_SW'])} aus Südwest.",
           f"At Gera {en(N['Gera_S'])} percent of the winds come from the south and {en(N['Gera_N'])} from the north; at Hohenleuben {en(N['Hohenleuben_W'])} percent from the west, at Schleiz {en(N['Schleiz_SW'])} from the south-west."),
        bi(f"Im Winter (Dezember bis Februar) kommt in Gera mehr als jede dritte Beobachtung aus Süden ({dn(N['S_winter'])} Prozent), im Sommer nur {dn(N['S_summer'])} Prozent; im Sommer führt West mit {dn(N['W_summer'])} Prozent.",
           f"In winter (December to February) more than every third observation at Gera is from the south ({en(N['S_winter'])} percent), in summer only {en(N['S_summer'])} percent; in summer west leads with {en(N['W_summer'])} percent."),
        bi(f"Gera zählt {dn(N['g_py'])} Gewitter im Jahr, Rothenacker {dn(N['r_py'])}, Schleiz {dn(N['s_py'])}; Brückner nennt 19 als Durchschnitt dieser Breite. Sie ziehen meist aus West: in Hohenleuben {dn(N['thunder_W_hoh'])}, in Gera {dn(N['thunder_W_gera'])} Prozent.",
           f"Gera counts {en(N['g_py'])} thunderstorms a year, Rothenacker {en(N['r_py'])}, Schleiz {en(N['s_py'])}; Brückner gives 19 as the average for this latitude. They mostly arrive from the west: {en(N['thunder_W_hoh'])} percent at Hohenleuben, {en(N['thunder_W_gera'])} at Gera."),
    ],
    'method': bi(
        'Die Windtabellen (S. 62 und 63) geben je Monat und Richtung eine Zahl von Beobachtungen der unteren Strömung, für Gera 1856 bis 1865, für Hohenleuben »in sieben Jahren«, für Schleiz 1866 und 1867, für Rothenacker 1867. Brückner hat die 16 Richtungen von Gera auf acht zurückgeführt (S. 62). Weil die Reihen verschieden lang sind, werden Prozentanteile verglichen: Anteil einer Richtung an der Summe des Ortes bzw. des Monats. In den Windrosen ist die Fläche der Keile dem Anteil proportional. Winter bedeutet Dezember bis Februar, Sommer Juni bis August (nicht Brückners Einteilung).\n'
        'Die Gewitter je Monat stehen für Gera in zwei Perioden (1853 bis 1858 und 1859 bis 1867, S. 67); das Diagramm teilt die Summe beider durch 15 Jahre. Den Oktoberwert der ersten Periode berichtigt Brückner auf 1 (S. 830). Die Jahreszahlen je Ort ergeben sich aus den Summen der Tabellen S. 66 und 67 geteilt durch die Jahre; die Zugrichtung der Gewitter (S. 68) betrifft 134 Gewitter in Gera und 47 in Hohenleuben. Brückners gedruckte Jahresmittel der Winde und seine Vergleichstabelle (S. 64) werden nicht verwendet, weil sie von den Zeilensummen abweichen.',
        'The wind tables (pp. 62 and 63) give a number of observations of the lower current for each month and direction: for Gera 1856 to 1865, for Hohenleuben »in seven years«, for Schleiz 1866 and 1867, for Rothenacker 1867. Brückner reduced the 16 directions of Gera to eight (p. 62). Because the series differ in length, percentages are compared: the share of a direction in the total of the place or month. In the wind roses the area of the wedges is proportional to the share. Winter means December to February, summer June to August (not Brückner’s division).\n'
        'The thunderstorms per month are given for Gera in two periods (1853 to 1858 and 1859 to 1867, p. 67); the chart divides the sum of both by 15 years. Brückner corrects the October value of the first period to 1 (p. 830). The annual figures per place result from the totals of the tables on pp. 66 and 67 divided by the years; the direction of motion of the thunderstorms (p. 68) concerns 134 storms at Gera and 47 at Hohenleuben. Brückner’s printed annual means of the winds and his comparison table (p. 64) are not used because they deviate from the row sums.'),
    'caveats': [
        bi(f"Die Windtabellen nennen keine Einheit. Die Summe {GT_DE} für Gera entspricht bei zehn Jahren rund 3,5 Beobachtungen am Tag, Brückner nennt aber höchstens drei Ablesungen (S. 54). Gezählt ist die untere Strömung an der Windfahne; Windstärke und Windstille fehlen.",
           f"The wind tables name no unit. The total of {GT_EN} for Gera corresponds to about 3.5 observations a day over ten years, whereas Brückner gives at most three readings (p. 54). The lower current at the wind vane is counted; wind force and calms are missing."),
        bi('Bei Hohenleuben liegen alle Monatssummen nahe 15 mal der Monatslänge (Januar 465 = 15 mal 31); das deutet auf 15 Jahre mit einer Ablesung täglich statt der genannten sieben Jahre. Schleiz (zwei Jahre) und Rothenacker (ein Jahr) sind sehr kurze Reihen. Prozentanteile sind davon unberührt.',
           'At Hohenleuben all monthly sums are close to 15 times the length of the month (January 465 = 15 times 31); this suggests 15 years with one reading a day instead of the stated seven years. Schleiz (two years) and Rothenacker (one year) are very short series. Percentages are unaffected.'),
        bi('Brückner erklärt die Südwinde in Gera mit der Ablenkung durch das Elstertal, die Westwinde im Oberland mit der freien Plateaulage (S. 64). Die Daten passen dazu, belegen es aber nicht. Die gedruckten Jahresmittel weichen teils von den Summen ab (Gera W: 204,6 gedruckt, 198,6 gerechnet); das Faksimile bestätigt den Druck.',
           'Brückner explains the south winds at Gera by deflection in the Elster valley and the west winds in the Oberland by the open plateau (p. 64). The data fit this but do not prove it. The printed annual means partly deviate from the sums (Gera W: 204.6 printed, 198.6 computed); the facsimile confirms the print.'),
        bi('Ob Gewitter oder Gewittertage gezählt wurden, sagt Brückner nicht; die Vergleichszahl 19 für 50 bis 52,5° nördlicher Breite nennt keine Quelle. Schleiz und Rothenacker beruhen auf zwei Jahren; Gera zählte 1861 45, 1864 nur 10 Gewitter. Die Zugrichtungen beruhen auf 134 und 47 Fällen.',
           'Brückner does not say whether thunderstorms or thunderstorm days were counted; the comparison figure 19 for 50 to 52.5° north gives no source. Schleiz and Rothenacker rest on two years; Gera counted 45 thunderstorms in 1861 and only 10 in 1864. The directions of motion rest on 134 and 47 cases.'),
    ],
    'datasets': [d_ws, d_wg, d_tm, d_ta, d_td],
    'charts': [c1, c2, c3],
    'keywords': {
        'de': ['Wind', 'Windrichtung', 'Windrose', 'Gewitter', 'Gera', 'Hohenleuben', 'Schleiz', 'Rothenacker', 'Elstertal', 'Klima'],
        'en': ['wind', 'wind direction', 'wind rose', 'thunderstorm', 'Gera', 'Hohenleuben', 'Schleiz', 'Rothenacker', 'Elster valley', 'climate'],
    },
    'related': ['klima-gera', 'klima-stationen', 'relief-hoehen'],
    'generated_by': 'Claude Sonnet 5.5 (Agent F2), aus 3 Einzelauswertungen zusammengeführt',
    'date': '2026-10-02',
}
tr_issues = [t for a in (aG, aV, aT) for t in (a.get('transcription_issues') or [])]
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
