from lib import *
# Wikidata ids taken from cached search hits (tools/wikidata_search.py cache); the API was unreachable during this run.
for k, q in [('Lobenstein', 'Q505656'), ('Plauen', 'Q3952'), ('Weida', 'Q519751'), ('Sachsen', 'Q153015'),
             ('Thüringen', 'Q1205'), ('Wurzbach', 'Q530139'), ('Ronneburg', 'Q554655'), ('Preußen', 'Q27306'),
             ('Saalfeld', 'Q155984'), ('Tanna', 'Q706897'), ('Saalburg', 'Q518398')]:
    D[k]['wikidata'] = q
