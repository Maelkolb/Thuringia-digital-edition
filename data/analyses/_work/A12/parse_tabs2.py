import re, sys
from common import *
from parse_tabs import BLOCKS, HEADS, norm

BM = re.compile(r"(?:geb\.|(?<![A-Za-zäöü])g\.)\s*(u\.\s*†\s*)?")
def cells():
    for pg,b,tab in BLOCKS:
        bl = block(pg,b)
        if bl.get("grid"):
            for i,row in enumerate(bl["grid"]):
                for j,c in enumerate(row):
                    if c: yield pg,b,tab,f"r{i+1}c{j+1}",norm(c)
        else:
            yield pg,b,tab,"p",norm(bl["text"])
if __name__=="__main__":
    multi=0; single=0; zero=0
    for pg,b,tab,pos,t in cells():
        t=t.replace("§","H.")
        n=len(BM.findall(t))
        if n==0: zero+=1; print("ZERO",pg,b,pos,t[:150])
        elif n==1: single+=1
        else: multi+=1
    print(zero,single,multi)
