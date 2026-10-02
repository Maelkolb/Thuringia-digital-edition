from common import *
import statistics as st
g=grid("55","b7"); m=[(int(r[0]),[num(x) for x in r[1:13]]) for r in g[1:13]]
a=[(int(r[0]),[num(x) for x in r[1:6]]) for r in grid("55","b9")[1:13]]
ann=[v[4] for y,v in a]
print("annual mean R",st.mean(ann), st.mean(ann)*1.25)
print("warm",max(a,key=lambda t:t[1][4]),"cold",min(a,key=lambda t:t[1][4]))
print("max",max(a,key=lambda t:t[1][2]),"min",min(a,key=lambda t:t[1][3]))
print("range mean R", st.mean([v[2]-v[3] for y,v in a]), "max range", max((v[2]-v[3],y) for y,v in a), "min range", min((v[2]-v[3],y) for y,v in a))
print("summer mean", st.mean(v[0] for y,v in a), "winter", st.mean(v[1] for y,v in a))
mm=[st.mean(v[j] for y,v in m) for j in range(12)]
print("monthly means",[round(x,2) for x in mm])
print("cycle amp R", max(mm)-min(mm), (max(mm)-min(mm))*1.25)
sd=[st.stdev(v[j] for y,v in m) for j in range(12)]
print("sd",[round(x,2) for x in sd])
allm=[(v[j],y,j+1) for y,v in m for j in range(12)]
print(max(allm),min(allm), sorted(allm)[:4], sorted(allm)[-4:])
# year ranks
for y,v in a: print(y, v)
# anomaly extremes
an=[((v[j]-mm[j])*1.25,y,j+1) for y,v in m for j in range(12)]
print(sorted(an)[:5], sorted(an)[-5:])
# corr summer winter
import math
def corr(x,y):
    mx,my=st.mean(x),st.mean(y); return sum((a-mx)*(b-my) for a,b in zip(x,y))/math.sqrt(sum((a-mx)**2 for a in x)*sum((b-my)**2 for b in y))
print("corr summer-winter", corr([v[0] for y,v in a],[v[1] for y,v in a]))
print("annual 1856-60 vs 1861-67 means", st.mean(v[4] for y,v in a if y<=1860), st.mean(v[4] for y,v in a if y>1860))
print("trend", )
