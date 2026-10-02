"""Parse the life dates of the persons printed in Tab. VI-XIV (pp. 394-402)."""
import re, json, sys
from common import *

# (page, block) of the genealogical tables / lists of Tab. VI-XIV
BLOCKS = [("394","b2","VI"),("395","b2","VII"),("395","b3","VII"),("395","b4","VII"),("395","b5","VII"),
          ("396","b2","VIII"),("396","b3","VIII"),("396","b4","VIII"),("396","b5","VIII"),("396","b6","VIII"),("396","b7","VIII"),("396","b8","VIII"),
          ("397","b2","IX"),("397","b3","IX"),("397","b4","IX"),
          ("398","b2","X"),("399","b2","XI"),("399","b3","XI"),("399","b4","XI"),
          ("400","b2","XII"),("400","b3","XII"),("401","b2","XIII"),("401","b3","XIII"),("401","b4","XIII"),("401","b5","XIII"),("401","b6","XIII"),("401","b7","XIII"),("401","b8","XIII"),
          ("402","b2","XIV")]
# header paragraphs / headings with a person
HEADS = [("394","b1"),("395","b2"),("396","b1"),("397","b1"),("398","b1"),("399","b1"),("400","b2"),("401","b1"),("402","b1")]

def norm(t):
    t = t.replace("ſ","s").replace("+","†")
    t = re.sub(r"=\s+", "", t)       # hyphenation artefacts: Doro= thea
    t = re.sub(r"-\s*\n\s*", "", t)
    t = re.sub(r"\s+", " ", t)
    return t

if __name__ == "__main__":
    for pg,b,tab in BLOCKS[:6]:
        bl = block(pg,b)
        if bl.get("grid"):
            for i,row in enumerate(bl["grid"]):
                for j,c in enumerate(row):
                    if c: print(pg,b,i+1,j+1,"|",norm(c))
        else:
            print(pg,b,"|",norm(bl["text"]))
