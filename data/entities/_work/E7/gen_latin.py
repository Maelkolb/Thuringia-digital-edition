from lib import *
import re
out=[]
merge_map = {  # key -> target key
 'Anemone nem':'Anemone nemorosa','Ficaria verna':'Ranunculus Ficaria','Prim. officinal':'Primula officinalis',
 'Ribes grossul':'Ribes Grossularia','Saxifraga gran':'Saxifraga granulata','Crataeg. Oxyat':'Crataegus Oxyacantha',
 'Apocynum':'Apocynum Venetum','Apoc. Venetum':'Apocynum Venetum','Neottia Nidus avis, Rich':'Neottia Nidus avis',
 'Pulicaria':'Pulicaria dysenterica',
}
epithet = {  # key -> full name (genus from the preceding line of the table, '-' = same genus)
 'campestris':'Cineraria campestris','retroflexus':'Amaranthus retroflexus','ustulata':'Orchis ustulata',
 'calcitrapa':'Centaurea calcitrapa','coriophora':'Orchis coriophora','apifera':'Ophrys apifera',
 'ensifolia':'Cephalanthera ensifolia','rubra':'Cephalanthera rubra','media':'Pyrola media',
 'cruciata':'Gentiana cruciata','nutans':'Ornithogalum nutans','rotundum':'Allium rotundum',
 'vernalis':'Scrophularia vernalis','spuria':'Linaria spuria','paucistamineus':'Ranunculus paucistamineus',
 'cheiranthoides':'Erysimum cheiranthoides','lanceolatum':'Erysimum lanceolatum','arenosa':'Arabis arenosa',
 'Halleri':'Arabis Halleri','Philonotis':'Ranunculus Philonotis','Elatine':'Linaria Elatine',
}
label_fix = {'Allium acutangulum Schr':'Allium acutangulum','Libanotis montana, Crtz':'Libanotis montana',
             'Phyteum orbiculare':'Phyteuma orbiculare'}
# sci overrides (modern/correct spellings)
sci_fix = {'Phyteum orbiculare':'Phyteuma orbiculare','Neottia Nidus avis':'Neottia nidus-avis'}
extra_notes = {
 'Laserpitium pruthenicum':'Nach S. 830 aus der Liste S. 72 und als Pflanze des Oberlandes (S. 79) zu streichen.',
 'Gentiana ciliata':'Nach S. 830 aus der Liste der nur im Unterland vorkommenden Pflanzen zu streichen (auch im Oberland).',
 'Neottia Nidus avis':'Nach S. 830 aus der Liste der nur im Unterland vorkommenden Pflanzen zu streichen (auch im Oberland).',
 'Nuphar luteum':'Zweifelhaft (S. 73); S. 830: kommt im Oberland öfters vor, der Stern entfällt.',
 'Apocynum Venetum':'S. 73: zweifelhaft; S. 75 und 830: verwildert im Küchengarten bei Untermhaus, nach dem Hofgärtner Papst Apocynum venetum.',
 'Sedum villosum':'S. 74 als vilosum gedruckt; S. 830 verbessert (kommt nur auf nassen, schwach sauren Wiesen vor).',
 'Phyteuma orbiculare':'S. 830 als Phyteum orbiculare gedruckt (Schreibfehler); nach S. 830 dem Oberland eigentümlich.',
 'Libanotis montana':'Nach S. 830 dem Oberland eigentümlich.',
 'Salvia verticillata':'Nach S. 830 dem Unterland eigentümlich (Nachtrag).',
 'Allogonium converfaceum':'Alge zwischen Köstritz und Caaschwitz (S. 77).',
 'Chaetophora tuberculosa':'Alge bei Debschwitz (S. 77).',
 'Telekia speciosa':'Nur im mährischen Gesenke heimisch; einmal unter rätselhaften Umständen an der Elster gefunden (S. 75).',
 'Ranunculus Philonotis':'S. 73 als Philonotis mit Vorzeichen »zweifelhaft«; Gattung aus der Vorzeile ergänzt.',
}
def norm_sci(label):
    parts=label.split()
    if len(parts)>=2:
        return parts[0]+' '+' '.join(p.lower() if i==0 else p for i,p in enumerate(parts[1:]))
    return label
latin=[]
for i,k in enumerate(KEYS):
    idx=i
    if k in merge_map:
        out.append(f'M|{merge_map[k]}|#{i}')
        continue
    is_latin = (k in epithet) or (k in label_fix) or re.match(r'^[A-Z][a-z]+ [a-zA-Z-]+( [a-z-]+)?$', k)
    if not is_latin: continue
    # only plants not decided elsewhere: filter by candidates' type and later undecided set
    latin.append(i)
import json
json.dump(latin, open('latin_idx.json','w'))
open('dsl_latin_merges.txt','w',encoding='utf-8').write('\n'.join(out)+'\n')
