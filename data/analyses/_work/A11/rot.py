"""Helper: fetch facsimile (optionally a crop), rotate it for reading rotated tables, save in scratchpad."""
import subprocess, sys
from pathlib import Path
from PIL import Image
SP = Path(r"C:\Users\totom\AppData\Local\Temp\claude\C--Users-totom\9d5e7ab8-c251-427e-83bd-b145b2d015af\scratchpad")
label = sys.argv[1]; crop = sys.argv[2] if len(sys.argv) > 2 else None
angle = int(sys.argv[3]) if len(sys.argv) > 3 else 90  # counter-clockwise degrees
width = sys.argv[4] if len(sys.argv) > 4 else "1800"
cmd = ["python", "tools/facsimile.py", label, "--width", width] + (["--crop", crop] if crop and crop != "full" else [])
out = subprocess.run(cmd, capture_output=True, text=True, cwd=r"C:\Users\totom\Projects\reuss-edition").stdout.strip()
im = Image.open(out).rotate(angle, expand=True)
dst = SP / f"{label}_{(crop or 'full').replace(',', '_')}_r{angle}.png"
im.save(dst)
print(dst)
