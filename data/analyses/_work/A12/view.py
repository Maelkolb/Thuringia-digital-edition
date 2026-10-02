import subprocess,sys
from PIL import Image
SP=r"C:/Users/totom/AppData/Local/Temp/claude/C--Users-totom/9d5e7ab8-c251-427e-83bd-b145b2d015af/scratchpad"
pg=sys.argv[1]; rot=int(sys.argv[2]) # 90 = ccw, -90 = cw, 0 none
out=subprocess.check_output([sys.executable,r'C:/Users/totom/Projects/reuss-edition/tools/facsimile.py',pg,'--width','2400'],text=True).strip()
im=Image.open(out)
if rot: im=im.rotate(rot,expand=True)
w,h=im.size
# split into 2x2 tiles with overlap
tiles={'a':(0,0,w//2+150,h//2+100),'b':(w//2-150,0,w,h//2+100),'c':(0,h//2-100,w//2+150,h),'d':(w//2-150,h//2-100,w,h)}
for k,box in tiles.items():
    im.crop(box).save(SP+f"/v{pg}_{k}.png")
print(im.size)
