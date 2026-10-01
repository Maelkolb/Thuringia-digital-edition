import glob,sys,re
d='data/entities/_work/E5/'
def load():
    files={}
    for fn in sorted(glob.glob(d+'dec_*.txt')):
        files[fn]=open(fn,encoding='utf-8').read().split('\n')
    return files
def find(files,key):
    hits=[]
    for fn,L in files.items():
        for i,l in enumerate(L):
            for sep in (' => ',' -> ',' !! '):
                if l.startswith(key+sep): hits.append((fn,i))
    return hits
def replace(files,key,newline):
    h=find(files,key); assert len(h)==1,(key,h)
    fn,i=h[0]; files[fn][i]=newline
def save(files):
    for fn,L in files.items(): open(fn,'w',encoding='utf-8').write('\n'.join(L))
