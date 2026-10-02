#!/bin/sh
# Q01 post-processing: run after (re-)running any package build script, in this order.
cd "$(dirname "$0")/../../../.." || exit 1
export PYTHONIOENCODING=utf-8
python data/analyses/_work/Q01/fix_text.py
python data/analyses/_work/Q01/patch_misc.py
python data/analyses/_work/Q01/fix_text.py
python data/analyses/_work/Q01/fix_charts.py
node tools/validate_analysis.mjs --all
