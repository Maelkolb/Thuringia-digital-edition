"""Q01: stack the preview PNGs of each analysis (2 charts per image) into scratch montages for review."""
import glob, json, os, sys
from pathlib import Path
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parents[4]
OUT = Path("C:/Users/totom/AppData/Local/Temp/claude/C--Users-totom/9d5e7ab8-c251-427e-83bd-b145b2d015af/scratchpad/q01/m")
OUT.mkdir(parents=True, exist_ok=True)
pat = sys.argv[1] if len(sys.argv) > 1 else '*'
n = 0
for f in sorted(glob.glob(str(ROOT / 'data/analyses' / f'{pat}.json'))):
    d = json.load(open(f, encoding='utf-8'))

    pngs = [ROOT / 'data/analyses/_preview' / f"{d['id']}__{c['id']}.png" for c in d['charts']]
    pngs = [p for p in pngs if p.exists()]
    for k in range(0, len(pngs), 2):
        ims = [Image.open(p).convert('RGB') for p in pngs[k:k + 2]]
        H = sum(i.height + 16 for i in ims); W = max(i.width for i in ims)
        canvas = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(canvas); y = 0
        for p, im in zip(pngs[k:k + 2], ims):
            dr.text((4, y + 2), p.stem, fill=(200, 0, 0)); y += 16
            canvas.paste(im, (0, y)); y += im.height
        canvas.save(OUT / f"{d['id']}_{k // 2}.png"); n += 1
print(n, 'montages ->', OUT)
