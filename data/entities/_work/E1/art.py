import sys,re
name,page=sys.argv[1],sys.argv[2]
n=int(sys.argv[3]) if len(sys.argv)>3 else 700
t=open(f'data/text/pages/{page}.txt',encoding='utf-8').read()
m=re.search(r'(?<![\wäöü])'+re.escape(name)+r'(?= \(|, | |\n)',t)
i=[m.start() for m in re.finditer(r'\] '+re.escape(name)+r'(?= |,|\()',t)]
i=i[0]+2 if i else (m.start() if m else 0)
print(t[i:i+n].replace('\n',' '))
