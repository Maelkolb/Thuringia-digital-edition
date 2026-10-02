from common import *
# p93 density: Einw/Dichte = area
g=grid('93','b4')
print(g[0])
fam={}
for r in g[1:]:
    y=int(r[0])
    vals=[num(x) for x in r[1:]]
    print(y,vals)
# area implied
pop={1834:(27359,22026,19948,69333),1843:(29189,24145,21549,74883),1852:(32378,25074,22372,79824),1861:(34672,26357,22331,83360),1867:(38252,27368,22354,87974)}
fams={1834:(5962,4638,None),1843:(6241,5306,4448),1852:(6881,5526,4672),1861:(7400,5701,4740),1867:(8094,6066,4792)}
for r in g[1:]:
    y=int(r[0]); v=[num(x) for x in r[1:]]
    p=pop[y]
    print(y,'area from Einw:',[round(p[0]/v[1],3),round(p[1]/v[3],3),round(p[2]/v[5],3),round(p[3]/v[7],3)])
    f=fams[y]
    print(y,'area from fam:',[round(f[0]/v[0],3) if f[0] else None,round(f[1]/v[2],3) if f[1] else None,round(f[2]/v[4],3) if v[4] and f[2] else None])
# p94 states
g=grid('94','b1')
for r in g[1:]:
    a=num(r[2]); n=int(r[3].replace(',','')); d=num(r[4]); print(r[1],a,n,d,round(n/a),)
# p94 houses
g=grid('94','b3')
for r in g[3:]:
    print(r)
for r in g[3:]:
    h=[integer(x) for x in r[1:4]]; print(r[0],h[0]+h[1]==h[2])
