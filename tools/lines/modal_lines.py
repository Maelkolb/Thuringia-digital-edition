"""Line detection (kraken blla) and a rough Fraktur reading per line (Tesseract frak2021) on Modal.

The reading only serves to align each detected line with the edition's transcript (align_lines.py).

    uvx modal run tools/lines/modal_lines.py --seqs 9,203,251      # a few pages
    uvx modal run tools/lines/modal_lines.py                       # every page in data/pages
"""
from __future__ import annotations

import json
from pathlib import Path

import modal

IIIF = "https://api.digitale-sammlungen.de/iiif/image/v2/bsb11005578_{seq:05d}/full/full/0/default.jpg"
FRAK2021 = "https://ub-backup.bib.uni-mannheim.de/~stweil/tesstrain/frak2021/tessdata_best/frak2021-0.905.traineddata"

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("libgl1", "libglib2.0-0", "tesseract-ocr", "curl")
    .run_commands(f"curl -sL -o /usr/share/tesseract-ocr/5/tessdata/frak2021.traineddata {FRAK2021}")
    .pip_install("kraken>=7.1,<7.2", "pillow", "requests")
)
app = modal.App("reuss-lines", image=image)


def _read_line(crop) -> tuple[str, float]:
    import os
    import subprocess
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        crop.save(f.name)
        tsv = subprocess.run(["tesseract", f.name, "stdout", "-l", "frak2021", "--psm", "7", "tsv"],
                             capture_output=True, text=True, encoding="utf-8",
                             env={**os.environ, "OMP_THREAD_LIMIT": "1"}).stdout
    os.unlink(f.name)
    words, confs = [], []
    for row in tsv.splitlines()[1:]:
        cols = row.split("	")
        if len(cols) == 12 and cols[11].strip():
            words.append(cols[11])
            confs.append(float(cols[10]))
    return " ".join(words), (sum(confs) / len(confs) if confs else 0.0)


@app.function(cpu=8, memory=8192, timeout=3600, max_containers=10, retries=1)
def process(seqs: list[int]) -> list[dict]:
    import io
    import time
    from concurrent.futures import ThreadPoolExecutor
    from importlib import resources

    import requests
    import torch
    from kraken import blla
    from kraken.lib import vgsl
    from PIL import Image

    torch.set_num_threads(8)
    model = vgsl.TorchVGSLModel.load_model(str(resources.files("kraken").joinpath("blla.mlmodel")))
    out = []
    for seq in seqs:
        im = Image.open(io.BytesIO(requests.get(IIIF.format(seq=seq), timeout=120).content)).convert("RGB")
        t0 = time.time()
        w, h = im.size
        seg = blla.segment(im, model=model, device="cpu")
        t_seg = time.time() - t0
        found = []
        for i, line in enumerate(seg.lines):
            poly = [[int(x), int(y)] for x, y in line.boundary or []]
            base = [[int(x), int(y)] for x, y in line.baseline or []]
            if not poly:
                continue
            xs, ys = [p[0] for p in poly], [p[1] for p in poly]
            box = [max(0, min(xs) - 4), max(0, min(ys) - 3), min(w, max(xs) + 4), min(h, max(ys) + 3)]
            found.append((i, line, poly, base, box))
        with ThreadPoolExecutor(max_workers=8) as pool:
            readings = list(pool.map(lambda f: _read_line(im.crop(f[4]).convert("L")), found))
        lines = [{"id": f"k{i:03d}", "baseline": base, "polygon": poly, "box": box,
                  "region": (line.regions or [None])[0], "ocr": text, "conf": round(conf, 1)}
                 for (i, line, poly, base, box), (text, conf) in zip(found, readings)]
        print(f"seq {seq}: {len(lines)} lines, segmentation {t_seg:.0f} s, reading {time.time() - t0 - t_seg:.0f} s")
        regions = [{"id": r.id, "type": t, "polygon": [[int(x), int(y)] for x, y in r.boundary]}
                   for t, items in (seg.regions or {}).items() for r in items]
        out.append({"seq": seq, "width": w, "height": h, "lines": lines, "regions": regions})
    return out


@app.local_entrypoint()
def main(seqs: str = "", force: bool = False):
    root = Path(__file__).resolve().parents[2]
    OUT = root / "data" / "lines" / "raw"
    OUT.mkdir(parents=True, exist_ok=True)
    if seqs:
        todo = [int(s) for s in seqs.split(",")]
    else:
        todo = [json.loads(p.read_text(encoding="utf-8"))["seq"] for p in sorted((root / "data" / "pages").glob("*.json"))]
    if not force:
        todo = [s for s in todo if not (OUT / f"{s:04d}.json").exists()]
    chunks = [todo[i:i + 4] for i in range(0, len(todo), 4)]
    print(f"{len(todo)} pages in {len(chunks)} chunks")
    done = 0
    for result in process.map(chunks, order_outputs=False):
        for page in result:
            (OUT / f"{page['seq']:04d}.json").write_text(json.dumps(page, ensure_ascii=False), encoding="utf-8")
            done += 1
        print(f"{done}/{len(todo)} pages; last {result[-1]['seq']}: {len(result[-1]['lines'])} lines")
