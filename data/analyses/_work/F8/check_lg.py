from f8common import *
from collections import Counter, defaultdict
ch=arch('geschichte-chronik-ereignisse-530-1867')
la=arch('geschichte-landerwerb-landverlust-1248-1690')
lt=arch('geschichte-landesteilungen-linien-1240-1870')
ev=rows(dataset(ch,'events'))
tr=rows(dataset(la,'transactions'))
ho=rows(dataset(lt,'houses'))
print(len(ev),len(tr),len(ho))
print(Counter(r['kind'] for r in ev))
print('events before 1200', sum(1 for r in ev if r['year']<1200))
# half century
hc=Counter((r['half_label'],r['kind']) for r in tr)
labs=sorted(set(r['half_label'] for r in tr))
for l in labs: print(l, hc[(l,'acq')], hc[(l,'loss')])
acq=lambda a,b: sum(1 for r in tr if r['kind']=='acq' and a<=r['year']<=b)
los=lambda a,b: sum(1 for r in tr if r['kind']=='loss' and a<=r['year']<=b)
print('<=1349',acq(0,1349),los(0,1349),'1350-1399',acq(1350,1399),los(1350,1399),'1400-1574',acq(1400,1574),los(1400,1574),'>=1575',acq(1575,9999),los(1575,9999))
print(Counter(r['mode'] for r in tr if r['kind']=='loss' and 1350<=r['year']<=1399))
print(Counter((r['house'],r['kind']) for r in tr))
# events in chronik by half century and kind
c=Counter((r['half_label'],r['kind']) for r in ev)
print(sorted(set(r['half_label'] for r in ev)))
kinds=['acq','loss','dyn','treaty','war','found','disaster']
for l in sorted(set(r['half_label'] for r in ev)):
    print(l, [c[(l,k)] for k in kinds], sum(c[(l,k)] for k in kinds))
# simultaneous
def count(y,branch=None):
    return sum(1 for h in ho if h['start_year']<=y<h['end_plot'] and (branch is None or h['branch']==branch))
for y in [1240,1305,1564,1583,1625,1647,1668,1678,1694,1698,1711,1768,1802,1824,1848,1869]:
    print(y,count(y),[count(y,b) for b in ('voigte','alt','jung')])
print('----')
def share(a,b,ks):
    tot=[r for r in ev if a<=r['year']<=b]
    return sum(1 for r in tot if r['kind'] in ks), len(tot)
print('<1500 land', share(0,1499,['acq','loss']), 'dyn+found', share(0,1499,['dyn','found']))
print('>=1500 land', share(1500,9999,['acq','loss']), 'dyn+found', share(1500,9999,['dyn','found']))
print('>=1550 land', share(1550,9999,['acq','loss']), 'dyn+found', share(1550,9999,['dyn','found']))
print('1200-1499 land', share(1200,1499,['acq','loss']))
print('>=1600', share(1600,9999,['acq','loss']), share(1600,9999,['dyn','found','disaster']))
print(Counter(r['kind'] for r in ev if r['year']>=1600))
print(Counter(r['kind'] for r in ev if r['year']<1500))
print(Counter(r['kind'] for r in ev if 1200<=r['year']<1500))
