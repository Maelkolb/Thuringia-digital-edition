from lib import *
# Corrections after cross-checking against the ortsregister (see-references) and E1 conventions.
def OV(key):
    D.pop(key, None)

# Wüstendittersdorf = Dittersdorf (Schleiz), folk name Trillloch (Brückner S. 593; register: "Wüstendittersdorf see Dittersdorf (Schleiz)")
OV('Wüstendittersdorf')
A('Wüstendittersdorf', 'Wüstendittersdorf', 'Dorf', gn=2805533, inp=True, reg=593,
  note='Brückners Dittersdorf (Wüsten-) bei Schleiz, im Volke "Trillloch" (zwei Bauernhöfe, Mühle, Försterei); im Register unter "Dittersdorf (Schleiz)" bzw. "Wüstendittersdorf siehe". Nicht die Wüstung Dittersdorf bei Tanna (S. 689).')
OV('Trillloch'); M('Trillloch', 'Wüstendittersdorf')
OV('Trilloch'); M('Trilloch', 'Wüstendittersdorf')

# Stöcketen: register "Stöcketen siehe Hohenpreis" (Frössen)
OV('Stöcketen'); M('Stöcketen', 'Hohenpreis')

# in_principality fixes (register hit via a differently spelled index entry)
for k in ('Oßla', 'Zschochern', 'Texdorf', 'Metzelsdorf', 'Sieglitzmühle', 'Starenburg'):
    D[k]['in_principality'] = True
for k in ('Zwickau', 'Oesterreich', 'Stein'):
    D[k].pop('register_page', None)

# note for Weißendorf
D['Weißendorf']['note'] = ('Brückner: Schul- und Marktort bei Triebes; seine Lageangabe ("1/4 Stunde SO. von Triebes") '
                           'weicht von den GeoNames-Koordinaten (westlich von Triebes) ab.')

# Flur notes: cleaner wording
for k, d in D.items():
    if d['action'] == 'accept' and d.get('kind') in ('Flur', 'Straße') and d.get('note', '').startswith('Flurstücksname ('):
        inner = d['note'][len('Flurstücksname ('):].rstrip('.').rstrip(')')
        d['note'] = 'Flurname: ' + inner + '.'
D['Weinberg']['note'] = 'Flurname: Hauptflurstück, S. 536 und 641; häufiger Flurname.'
