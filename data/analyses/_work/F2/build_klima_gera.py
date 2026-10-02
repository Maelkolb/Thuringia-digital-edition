from common import *

FID = 'klima-gera'
aT = load('klima-gera-temperatur-1856-1867')
aP = load('klima-gera-luftdruck-1856-1867')
aR = load('klima-regenmenge-gera-1860-1867')
aW = load('klima-witterungserscheinungen-gera-1856-1867')

# ---------------------------------------------------------------- datasets
d_tm = ds(aT, 'monthly'); d_tm['name'] = 'temp_monthly'
d_ta = ds(aT, 'annual'); d_ta['name'] = 'temp_annual'
d_pa = ds(aP, 'annual'); d_pa['name'] = 'pressure_annual'
d_w = ds(aW, 'monthly'); d_w['name'] = 'weather_events'
d_ry = ds(aR, 'yearly'); d_ry['name'] = 'rain_yearly'
d_rr = ds(aR, 'reference'); d_rr['name'] = 'rain_reference'

tm = rows(d_tm)
ta = rows(d_ta)
pa = rows(d_pa)
wm = rows(d_w)
ry = rows(d_ry)
rr = rows(d_rr)

# ---------------------------------------------------------------- numbers for the texts
N = {}
N['annual_mean'] = statistics.mean(r['annual_c'] for r in ta)
cold = min(ta, key=lambda r: r['annual_c'])
warm = max(ta, key=lambda r: r['annual_c'])
N['cold_year'], N['cold_val'] = cold['year'], cold['annual_c']
N['warm_year'], N['warm_val'] = warm['year'], warm['annual_c']
hi = max(ta, key=lambda r: r['max_c'])
lo = min(ta, key=lambda r: r['min_c'])
N['max_year'], N['max_val'] = hi['year'], hi['max_c']
N['min_year'], N['min_val'] = lo['year'], lo['min_c']
winter = [abs(r['anomaly_c']) for r in tm if r['month'] in (12, 1, 2)]
summer = [abs(r['anomaly_c']) for r in tm if r['month'] in (6, 7, 8, 9)]
N['winter_max'] = max(winter)
N['summer_max'] = max(summer)

gew = [r for r in wm if r['phenomenon'] == 'Gewitter']
gew_total = sum(r['days'] or 0 for r in gew)
gew_summer = sum(r['days'] or 0 for r in gew if r['month'] in (6, 7, 8))
N['gew_per_year'] = gew_total / 12
N['gew_summer_pct'] = 100 * gew_summer / gew_total
nov_gew = [r for r in gew if r['month'] == 11][0]['days']
aug_snow = [r for r in wm if r['phenomenon'] == 'Schnee' and r['month'] == 8][0]['days']
aug_frost = [r for r in wm if r['phenomenon'] == 'Reif' and r['month'] == 8][0]['days']
assert nov_gew in (None, 0) and aug_snow in (None, 0) and aug_frost in (None, 0)

ref_th = [r for r in rr if r['label'].startswith('Th')][0]
N['rain_mean_mm'] = [r for r in rr if r['label'].startswith('Gera')][0]['mm']
N['th_mm'] = ref_th['mm']
wet = max(ry, key=lambda r: r['annual_mm'])
dry = min(ry, key=lambda r: r['annual_mm'])
N['wet_year'], N['wet_mm'] = wet['year'], wet['annual_mm']
N['dry_year'], N['dry_mm'] = dry['year'], dry['annual_mm']
N['above'] = sum(1 for r in ry if r['annual_mm'] > ref_th['mm'])
assert N['above'] == 3 and len(ry) == 8

early = [r['pressure_hpa'] for r in pa if r['year'] <= 1864]
late = [r['pressure_hpa'] for r in pa if r['year'] >= 1865]
N['p_early_lo'], N['p_early_hi'] = min(early), max(early)
N['p_jump_lo'] = min(late) - statistics.mean(early)
N['p_jump_hi'] = max(late) - statistics.mean(early)
print({k: (round(v, 2) if isinstance(v, float) else v) for k, v in N.items()})


def dn(x, nd=1):
    return de_num(x, nd)


def en(x, nd=1):
    return en_num(x, nd)


# ---------------------------------------------------------------- charts
tooltip_temp = [
    {'field': 'year', 'title': bi('Jahr', 'Year')},
    {'field': 'month_label', 'title': bi('Monat', 'Month')},
    {'field': 'temp_r', 'title': bi('Monatsmittel (°R, gedruckt)', 'Monthly mean (°R, as printed)')},
    {'field': 'temp_c', 'title': bi('Monatsmittel (°C)', 'Monthly mean (°C)'), 'format': '.1f'},
    {'field': 'anomaly_c', 'title': bi('Abweichung (K)', 'Deviation (K)'), 'format': '+.1f'},
]

c1 = {
    'id': 'c1',
    'dataset': 'temp_monthly',
    'title': bi(
        f"Im Winter schwankten Monatsmittel stark, im Sommer kaum: Juni bis September wichen höchstens {dn(N['summer_max'])} K ab",
        f"Winter months varied widely, summer months hardly: June to September never departed more than {en(N['summer_max'])} K"),
    'caption': bi(
        'Abweichung jedes Monatsmittels der Temperatur in Gera vom Mittel desselben Kalendermonats der zwölf Jahre, in Kelvin; Zahlen ab 4 K Abweichung. Aus Réaumur umgerechnet. Quelle: S. 55.',
        'Deviation of each monthly mean temperature at Gera from the mean of the same calendar month over the twelve years, in kelvin; numbers where the deviation is 4 K or more. Converted from Réaumur. Source: p. 55.'),
    'vegalite': {
        'height': 300,
        'encoding': {
            'x': {'field': 'year', 'type': 'ordinal', 'axis': {'title': None, 'labelAngle': 0}},
            'y': {'field': 'month', 'type': 'ordinal', 'axis': {'title': None, 'labelExpr': month_axis_expr()}},
        },
        'layer': [
            {
                'mark': {'type': 'rect'},
                'encoding': {
                    'color': {
                        'field': 'anomaly_c', 'type': 'quantitative',
                        'scale': {'domain': [-6, 0, 6], 'range': ['@accent', '@paper', '@negative'], 'clamp': True, 'interpolate': 'lab'},
                        'legend': {'title': bi('Abweichung vom Mittel des Kalendermonats (K)', 'Deviation from the mean of the calendar month (K)'),
                                   'titleLimit': 500, 'values': [-6, -3, 0, 3, 6], 'gradientLength': 280,
                                   'labelExpr': "datum.value > 0 ? '+' + datum.value : (datum.value < 0 ? '−' + abs(datum.value) : '0')"},
                    },
                    'tooltip': tooltip_temp,
                },
            },
            {
                'transform': [{'filter': 'abs(datum.anomaly_c) >= 4'}],
                'mark': {'type': 'text', 'style': 'label'},
                'encoding': {'text': {'field': 'anomaly_c', 'type': 'quantitative', 'format': '+.1f'},
                             'color': {'condition': {'test': 'abs(datum.anomaly_c) >= 5', 'value': '@paper'}, 'value': '@ink'}},
            },
        ],
    },
}

# --- c2: calendar of weather events
order_expr = "{'Schnee':1,'Reif':2,'Sturm':3,'Hoehenrauch':4,'Regen':5,'Gewitter':6,'Nebel':7}[datum.phenomenon]"
name_de = "{'Schnee':'Schnee','Reif':'Reif','Sturm':'Sturm','Hoehenrauch':'Höhenrauch','Regen':'Regen','Gewitter':'Gewitter','Nebel':'Nebel'}[datum.phenomenon]"
name_en = "{'Schnee':'Snow','Reif':'Hoarfrost','Sturm':'Storm','Hoehenrauch':'Haze','Regen':'Rain','Gewitter':'Thunderstorm','Nebel':'Fog'}[datum.phenomenon]"
c2 = {
    'id': 'c2',
    'dataset': 'weather_events',
    'title': bi('Jede Erscheinung hat ihre Jahreszeit: Gewitter im Sommer, Schnee und Reif im Winter, Nebel im Herbst',
                'Each phenomenon has its season: thunderstorms in summer, snow and hoarfrost in winter, fog in autumn'),
    'caption': bi(
        'Anteil jedes Monats an der Jahressumme der Erscheinung in Gera, 1856 bis 1867 (Prozent); die Zahl nennt den stärksten Monat, in Klammern der Durchschnitt pro Jahr. Quelle: S. 66, Regen nach S. 830 berichtigt.',
        'Share of each month in the annual total of the phenomenon at Gera, 1856 to 1867 (percent); the number marks the strongest month, in brackets the average per year. Source: p. 66, rain as corrected on p. 830.'),
    'vegalite': {
        'height': {'step': 30},
        'transform': [
            {'filter': "indexof(['Schnee','Reif','Sturm','Hoehenrauch','Regen','Gewitter','Nebel'], datum.phenomenon) >= 0"},
            {'joinaggregate': [{'op': 'sum', 'field': 'per_year', 'as': 'year_total'}, {'op': 'max', 'field': 'share_of_year', 'as': 'row_max'}], 'groupby': ['phenomenon']},
            {'calculate': order_expr, 'as': 'row_order'},
            {'calculate': {'de': name_de + " + ' (' + format(datum.year_total, '.0f') + ')'", 'en': name_en + " + ' (' + format(datum.year_total, '.0f') + ')'"}, 'as': 'row_label'},
        ],
        'encoding': {
            'x': {'field': 'month', 'type': 'ordinal', 'axis': {'title': None, 'labelAngle': 0, 'labelExpr': month_axis_expr()}},
            'y': {'field': 'row_label', 'type': 'nominal', 'sort': {'field': 'row_order', 'op': 'min'}, 'axis': {'title': None, 'labelLimit': 200}},
        },
        'layer': [
            {
                'mark': {'type': 'rect'},
                'encoding': {
                    'color': {'field': 'share_of_year', 'type': 'quantitative',
                              'scale': {'range': 'heatmap', 'domain': [0, 24], 'clamp': True},
                              'legend': {'title': bi('Anteil an der Jahressumme (%)', 'Share of the annual total (%)'), 'titleLimit': 500, 'values': [0, 6, 12, 18, 24], 'format': 'd', 'gradientLength': 240}},
                    'tooltip': [
                        {'field': 'row_label', 'title': bi('Erscheinung (pro Jahr)', 'Phenomenon (per year)')},
                        {'field': 'month_label', 'title': bi('Monat', 'Month')},
                        {'field': 'days', 'title': bi('Zahl in zwölf Jahren', 'Count in twelve years'), 'format': 'd'},
                        {'field': 'share_of_year', 'title': bi('Anteil (%)', 'Share (%)'), 'format': '.1f'},
                    ],
                },
            },
            {
                'transform': [{'filter': 'datum.share_of_year == datum.row_max'}],
                'mark': {'type': 'text', 'style': 'label'},
                'encoding': {
                    'text': {'field': 'share_of_year', 'type': 'quantitative', 'format': '.0f'},
                    'color': {'condition': {'test': 'datum.share_of_year > 13', 'value': '@paper'}, 'value': '@ink'},
                },
            },
        ],
    },
}

# --- c3: rain per year
lookup = [
    {'calculate': "'Thüringen (allgemein)'", 'as': 'refkey'},
    {'lookup': 'refkey', 'from': {'data': {'name': 'rain_reference'}, 'key': 'label', 'fields': ['mm']}, 'as': 'ref_mm'},
]
tooltip_rain = [
    {'field': 'year', 'title': bi('Jahr', 'Year')},
    {'field': 'annual_zoll', 'title': bi('Niederschlag (Pariser Zoll)', 'Precipitation (Paris inches)'), 'format': '.2f'},
    {'field': 'annual_mm', 'title': bi('Niederschlag (mm)', 'Precipitation (mm)'), 'format': '.0f'},
    {'field': 'days_total', 'title': bi('Tage mit Regen oder Schnee', 'Days with rain or snow'), 'format': 'd'},
]
c3 = {
    'id': 'c3',
    'dataset': 'rain_yearly',
    'extra_datasets': ['rain_reference'],
    'title': bi('Die Regenmenge lag in Gera nur in drei von acht Jahren über dem thüringischen Mittel',
                'Rainfall at Gera exceeded the Thuringian average in only three of eight years'),
    'caption': bi(
        'Jahresniederschlag in Gera 1860 bis 1867 nach Brückners Regenmessung (Pariser Zoll, umgerechnet in Millimeter), Linie: allgemeines Mittel für Thüringen (21,12 Zoll). Quelle: S. 68 f., Berichtigungen S. 830.',
        'Annual precipitation at Gera, 1860 to 1867, from Brückner’s rain gauge (Paris inches, converted to millimeters); line: general average for Thuringia (21.12 inches). Source: pp. 68 f., corrections p. 830.'),
    'vegalite': {
        'height': 280,
        'transform': lookup,
        'encoding': {
            'x': {'field': 'year', 'type': 'ordinal', 'axis': {'title': None, 'labelAngle': 0}},
            'y': {'field': 'annual_mm', 'type': 'quantitative', 'scale': {'domain': [0, 700]},
                  'axis': {'title': bi('Niederschlag (mm)', 'Precipitation (mm)'), 'values': [0, 200, 400, 600]}},
        },
        'layer': [
            {
                'mark': {'type': 'bar', 'width': {'band': 0.7}},
                'encoding': {
                    'color': {'condition': {'test': 'datum.annual_mm > datum.ref_mm', 'value': '@accent'}, 'value': '@context'},
                    'tooltip': tooltip_rain,
                },
            },
            {
                'mark': {'type': 'text', 'style': 'label', 'baseline': 'top', 'dy': 3},
                'encoding': {
                    'text': {'field': 'annual_mm', 'type': 'quantitative', 'format': '.0f'},
                    'color': {'condition': {'test': 'datum.annual_mm > datum.ref_mm', 'value': '@paper'}, 'value': '@ink'},
                },
            },
            {
                'mark': {'type': 'rule', 'strokeDash': [4, 3], 'color': '@ink2', 'strokeWidth': 1.5},
                'encoding': {'x': None, 'y': {'field': 'ref_mm', 'type': 'quantitative'}},
            },
            {
                'transform': [{'filter': 'datum.year == 1860'}],
                'mark': {'type': 'text', 'style': 'annotation', 'align': 'left', 'baseline': 'bottom', 'dy': -5, 'dx': -22},
                'encoding': {
                    'y': {'field': 'ref_mm', 'type': 'quantitative'},
                    'text': {'value': bi(f"Thüringen, Mittel {N['th_mm']} mm", f"Thuringia, average {N['th_mm']} mm")},
                },
            },
        ],
    },
}

# ---------------------------------------------------------------- the feature
f = {
    'id': FID,
    'title': bi('Wetter in Gera 1856–1867', 'Weather in Gera, 1856–1867'),
    'category': 'climate',
    'section': 't1-1-7',
    'merges': ['klima-gera-temperatur-1856-1867', 'klima-gera-luftdruck-1856-1867', 'klima-regenmenge-gera-1860-1867', 'klima-witterungserscheinungen-gera-1856-1867'],
    'sources': [
        {'page': '54', 'block': 'b1'}, {'page': '54', 'block': 'b4'}, {'page': '55', 'block': 'b7'}, {'page': '55', 'block': 'b9'},
        {'page': '66', 'block': 'b3', 'rows': 'r2-r15'}, {'page': '68', 'block': 'b7'}, {'page': '69', 'block': 'b1', 'rows': 'r2-r10'},
        {'page': '830', 'block': 'b3'}, {'page': '830', 'block': 'b6'},
    ],
    'summary': bi(
        f"Für Gera druckt Brückner Wetterbeobachtungen aus zwölf Jahren (1856 bis 1867): Monatsmittel der Temperatur und des Luftdrucks, die Regenmenge seit 1860 und die Zahl von Nebel, Regen, Schnee, Reif und Gewittern. Das Jahresmittel der Temperatur beträgt {dn(N['annual_mean'])} °C (aus Réaumur umgerechnet), die Regenmenge im Mittel {N['rain_mean_mm']} mm, Gewitter zählt er {dn(N['gew_per_year'])} im Jahr.",
        f"For Gera, Brückner prints twelve years of weather observations (1856 to 1867): monthly mean temperature and air pressure, rainfall from 1860, and counts of fog, rain, snow, hoarfrost and thunderstorms. The mean annual temperature is {en(N['annual_mean'])} °C (converted from Réaumur), mean rainfall {N['rain_mean_mm']} mm, and he counts {en(N['gew_per_year'])} thunderstorms a year."),
    'findings': [
        bi(f"Das Jahresmittel liegt bei {dn(N['annual_mean'])} °C und reicht von {dn(N['cold_val'])} °C ({N['cold_year']}) bis {dn(N['warm_val'])} °C ({N['warm_year']}). Höchster Stand: {dn(N['max_val'])} °C ({N['max_year']}), tiefster: {dn(N['min_val'])} °C ({N['min_year']}).",
           f"The annual mean is {en(N['annual_mean'])} °C and ranges from {en(N['cold_val'])} °C ({N['cold_year']}) to {en(N['warm_val'])} °C ({N['warm_year']}). Highest reading: {en(N['max_val'])} °C ({N['max_year']}), lowest: {en(N['min_val'])} °C ({N['min_year']})."),
        bi(f"{N['gew_summer_pct']:.0f} Prozent der Gewitter von 1856 bis 1867 fielen in Juni bis August; im November gab es keines. Schnee und Reif traten im August nie auf.",
           f"{N['gew_summer_pct']:.0f} percent of the thunderstorms from 1856 to 1867 fell in June to August; there was none in November. Snow and hoarfrost never occurred in August."),
        bi(f"1860 bis 1867 fielen im Mittel {N['rain_mean_mm']} mm Niederschlag, von {N['dry_mm']:.0f} mm ({N['dry_year']}) bis {N['wet_mm']:.0f} mm ({N['wet_year']}); das thüringische Mittel beträgt {N['th_mm']} mm.",
           f"From 1860 to 1867 the average was {N['rain_mean_mm']} mm of precipitation, from {N['dry_mm']:.0f} mm ({N['dry_year']}) to {N['wet_mm']:.0f} mm ({N['wet_year']}); the Thuringian average is {N['th_mm']} mm."),
    ],
    'method': bi(
        'Die Monatsmittel der Temperatur (S. 55) sind in Grad Réaumur gedruckt und mit 1,25 in °C umgerechnet; die Skala nennt Brückner nicht ausdrücklich, sie folgt aus S. 70 und aus der Plausibilität der Werte. Die Abweichung im ersten Diagramm ist das Monatsmittel minus das Mittel desselben Kalendermonats über die zwölf Jahre, neu aus den 144 Werten berechnet. Winter, Sommer und Jahresmittel sowie Höchst- und Tiefststand stammen aus Brückners zweiter Tabelle (S. 55).\n'
        'Das zweite Diagramm teilt die Monatssummen der Erscheinungen (S. 66, Summen über zwölf Jahre) durch die Jahressumme der jeweiligen Erscheinung. Die Regenzahlen sind nach Brückners Berichtigung (S. 830) eingesetzt: Januar 87, Juli 181, August 152, Dezember 84. Gezeigt werden sieben Erscheinungen; Sonnen- und Mondhöfe sowie Zodiakal- und Nordlicht stehen nur im Datensatz.\n'
        'Die Regenmenge steht auf S. 69 in Pariser Zoll Höhe (1 Zoll = 27,07 mm). Brückner berichtigt auf S. 830 mehrere Jahresmittel; die Auswertung verwendet die berichtigten Werte, der Datensatz nennt die gedruckten daneben. Der Luftdruck (S. 54) ist in Pariser Linien gedruckt (1 Linie = 2,2558 mm Quecksilbersäule, 1 mm = 1,3332 hPa) und nur als Jahresmittel aufgenommen.',
        'The monthly mean temperatures (p. 55) are printed in degrees Réaumur and converted at 1.25 to °C; Brückner does not state the scale explicitly, it follows from p. 70 and from the plausibility of the values. The deviation in the first chart is the monthly mean minus the mean of the same calendar month over the twelve years, recomputed from the 144 values. Winter and summer means, annual means and the highest and lowest readings come from Brückner’s second table (p. 55).\n'
        'The second chart divides the monthly totals of the phenomena (p. 66, sums over twelve years) by the annual total of each phenomenon. The rain counts use Brückner’s correction (p. 830): January 87, July 181, August 152, December 84. Seven phenomena are shown; solar and lunar halos and zodiacal light and aurora appear only in the dataset.\n'
        'Rainfall is given on p. 69 as a depth in Paris inches (1 inch = 27.07 mm). On p. 830 Brückner corrects several annual means; the analysis uses the corrected values, and the dataset lists the printed ones alongside. Air pressure (p. 54) is printed in Paris lines (1 line = 2.2558 mm of mercury, 1 mm = 1.3332 hPa) and is included only as annual means.'),
    'conversions': [
        {'from': 'Grad Réaumur (°R)', 'to': 'Grad Celsius (°C)', 'factor_or_formula': '°C = °R × 1,25', 'reference': '80 Teilstriche zwischen Eis- und Siedepunkt (Réaumur) gegenüber 100 (Celsius); von Brückner nicht tabelliert'},
        {'from': 'Pariser Zoll (Regenhöhe)', 'to': 'mm', 'factor_or_formula': 'mm = Zoll × 27,07', 'reference': '1 Zoll = 12 Pariser Linien; 443,296 Pariser Linien = 1 m (Brückner S. 831)'},
        {'from': 'Pariser Linie (Barometer)', 'to': 'hPa', 'factor_or_formula': 'hPa = Linien × 2,2558 mm × 1,3332 hPa/mm', 'reference': '1 Pariser Fuß = 324,84 mm; 1 Linie = 1/144 Fuß'},
    ],
    'caveats': [
        bi('Die Temperaturskala nennt Brückner im Klimakapitel nicht. Angenommen wird Grad Réaumur (S. 70 nennt »° R.«); wären es Celsiusgrade, lägen alle °C-Werte um ein Fünftel niedriger. Die Beobachter wechselten (Kratzsch, Schmidt), Instrument und Aufstellung sind nicht beschrieben.',
           'Brückner does not name the temperature scale in the climate chapter. Réaumur is assumed (p. 70 gives »° R.«); if the values were Celsius, all °C figures would be one fifth lower. The observers changed (Kratzsch, Schmidt); instrument and exposure are not described.'),
        bi(f"Der Luftdruck liegt ab 1865 um {N['p_jump_lo']:.0f} bis {N['p_jump_hi']:.0f} hPa höher als 1856 bis 1864 ({N['p_early_lo']:.0f} bis {N['p_early_hi']:.0f} hPa). Das deutet eher auf einen Wechsel von Instrument oder Aufstellung als auf eine Klimaänderung; Gleichartigkeit der Temperaturreihe ist daher nicht belegt.",
           f"From 1865 air pressure is {N['p_jump_lo']:.0f} to {N['p_jump_hi']:.0f} hPa higher than in 1856 to 1864 ({N['p_early_lo']:.0f} to {N['p_early_hi']:.0f} hPa). This suggests a change of instrument or exposure rather than of climate; the homogeneity of the temperature series is therefore not established."),
        bi('Der März 1856 (−6,8 °R) widerspricht Hohenleuben, wo für denselben Monat +0,28 °R gedruckt sind. Geras gedruckte Winter- und Jahresmittel 1856 sind mit −6,8 gerechnet, der Fehler läge also in der Vorlage. Der Wert wird unverändert gezeigt und prägt die Extreme im ersten Diagramm.',
           'March 1856 (−6.8 °R) contradicts Hohenleuben, where +0.28 °R is printed for the same month. Gera’s printed winter and annual means for 1856 are computed with −6.8, so the error would lie in the source. The value is shown unchanged and shapes the extremes in the first chart.'),
        bi('Ob Tage oder einzelne Ereignisse gezählt wurden, sagt Brückner nicht; Kratzsch notierte nur ein- bis zweimal täglich, kurze Erscheinungen können fehlen. Acht Regenjahre sind eine kurze Reihe, und Brückners Fließtext (S. 69) übernimmt die Berichtigungen von S. 830 nicht.',
           'Brückner does not say whether days or single events were counted; Kratzsch noted only once or twice a day, so short phenomena may be missing. Eight rain years are a short series, and Brückner’s running text (p. 69) does not adopt the corrections of p. 830.'),
    ],
    'datasets': [d_tm, d_w, d_ry, d_rr, d_ta, d_pa],
    'charts': [c1, c2, c3],
    'keywords': {
        'de': ['Wetter', 'Klima', 'Gera', 'Temperatur', 'Luftdruck', 'Niederschlag', 'Regen', 'Gewitter', 'Nebel', 'Réaumur', 'Thermometer'],
        'en': ['weather', 'climate', 'Gera', 'temperature', 'air pressure', 'precipitation', 'rain', 'thunderstorm', 'fog', 'Réaumur', 'thermometer'],
    },
    'related': ['klima-stationen', 'wind-gewitter', 'phaenologie'],
    'generated_by': 'Claude Sonnet 5.5 (Agent F2), aus 4 Einzelauswertungen zusammengeführt',
    'date': '2026-10-02',
}
tr = [t for a in (aT, aP, aR, aW) for t in (a.get('transcription_issues') or [])]
if tr:
    f['transcription_issues'] = tr

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
