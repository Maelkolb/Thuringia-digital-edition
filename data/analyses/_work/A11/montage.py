"""Helper: stack several preview PNGs vertically into one image in the scratchpad for quick review."""
import sys
from pathlib import Path
from PIL import Image
PREV = Path(r"C:\Users\totom\Projects\reuss-edition\data\analyses\_preview")
SP = Path(r"C:\Users\totom\AppData\Local\Temp\claude\C--Users-totom\9d5e7ab8-c251-427e-83bd-b145b2d015af\scratchpad")
names = sys.argv[2:]
aid = sys.argv[1]
ims = [Image.open(PREV / f"{aid}__{n}.png").convert("RGB") for n in names]
w = max(i.width for i in ims)
h = sum(i.height for i in ims) + 10 * (len(ims) - 1)
out = Image.new("RGB", (w, h), (251, 248, 241))
y = 0
for i in ims:
    out.paste(i, (0, y))
    y += i.height + 10
dst = SP / f"m_{aid}_{'_'.join(names)}.png"
out.save(dst)
print(dst, out.size)
