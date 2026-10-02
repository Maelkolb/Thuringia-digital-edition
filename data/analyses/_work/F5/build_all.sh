#!/bin/sh
cd "$(dirname "$0")"
for f in wald vieh landw berufe; do PYTHONIOENCODING=utf-8 python build_$f.py 2>&1 | grep -E "^(OK|FAIL)|ERROR|Error"; done
