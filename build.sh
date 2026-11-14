#!/bin/bash
set -e

MODE="${1:-trial}"

if [ "$MODE" = "full" ]; then
  echo "non ancora disponibile: mancano le misure del vano"
  exit 1
fi

if [ "$MODE" != "trial" ]; then
  echo "Modalità sconosciuta: $MODE. Usa 'trial' o 'full'."
  exit 1
fi

echo "==> Esecuzione controlli geometrici e tolleranze FDM (pytest)..."
.venv/bin/python -m pytest checks/check_fit.py -v

echo "==> Generando i file CAD per la piastra di prova (.step e .stl)..."
.venv/bin/python src/generate_adapter.py

echo "==> Generando il progetto 3MF con Bambu Studio..."
BAMBU_CLI="/Applications/BambuStudio.app/Contents/MacOS/BambuStudio"
PROJECT_DIR="$(pwd)"
OUTPUT_DIR="${PROJECT_DIR}/output"

$BAMBU_CLI \
  "${OUTPUT_DIR}/trial_plate.stl" \
  --load-settings "/Applications/BambuStudio.app/Contents/Resources/profiles/BBL/machine/Bambu Lab A1 mini 0.4 nozzle.json;/Applications/BambuStudio.app/Contents/Resources/profiles/BBL/process/0.16mm Optimal @BBL A1M.json" \
  --load-filaments "/Applications/BambuStudio.app/Contents/Resources/profiles/BBL/filament/Generic PETG @BBL A1M.json" \
  --export-3mf "${OUTPUT_DIR}/trial_plate_temp.3mf"

echo "==> Applicando le patch per il profilo di stampa PETG..."
.venv/bin/python src/patch_3mf.py "${OUTPUT_DIR}/trial_plate_temp.3mf" "${OUTPUT_DIR}/trial_plate.3mf"
rm "${OUTPUT_DIR}/trial_plate_temp.3mf"

echo "==> Fatto! File pronto in output/trial_plate.3mf"
