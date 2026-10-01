from lib import *
dec = parse_all(['dsl_animals.txt','dsl_animals2.txt','dsl_animals3.txt','dsl_plants.txt','dsl_misc.txt'])
[print('ERROR',*e) for e in ERRORS]
print(len(dec),'decided of',len(KEYS))
und=[(i,k) for i,k in enumerate(KEYS) if k not in dec]
print(len(und))
for i,k in und: print(i,k, end=' | ')
