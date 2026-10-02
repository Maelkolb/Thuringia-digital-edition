#!/bin/sh
# rebuilds all A01 analyses from the canonical page JSON and validates them
set -e
cd "$(dirname "$0")"
export PYTHONIOENCODING=utf-8
python a01_lage.py > /dev/null
python build_lage_text.py
python build_flaeche.py > /dev/null
python build_grenzen.py > /dev/null
python build_wohnorte_text.py > /dev/null
python build_hoehenstufen.py > /dev/null
python build_neigung_text.py > /dev/null
python build_erhebungen_text.py > /dev/null
python build_bergnamen_text.py > /dev/null
cd ../../../..
node tools/validate_analysis.mjs data/analyses/lage-vermessene-punkte-laenge-breite.json data/analyses/flaeche-fuerstenthum-vermessung-nachbarn.json data/analyses/grenzen-umfang-nachbarlaender.json data/analyses/relief-hoehenstufen-oberland-unterland.json data/analyses/relief-wohnorte-hoehenlage.json data/analyses/relief-hoehe-und-lage-neigung.json data/analyses/relief-erhebungen-hoechste-punkte.json data/analyses/relief-bergnamen.json
