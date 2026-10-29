#!/usr/bin/env bash
# Baseline (LAN): 1 server + 4 workers, no netem, 1000 tasks.
set -euo pipefail
cd "$(dirname "$0")/.."

SEED="${SEED:-1}"
RUN_DIR="results/logs/$(date +%Y%m%d_%H%M%S)_baseline_seed${SEED}"
mkdir -p "$RUN_DIR"
export PYTHONPATH=src

# TODO: start server, start 4 workers, wait for completion, collect CSVs
echo "Run directory: $RUN_DIR"
