#!/usr/bin/env bash
# Runs every scenario (baseline, worker_crash, severe_loss, delayed_acks)
# at least 5 times each, capturing pcaps for at least two runs per scenario.
set -euo pipefail
cd "$(dirname "$0")/.."

REPEATS="${REPEATS:-5}"
IFACE="${IFACE:-lo}"

# TODO: loop over scenarios and seeds, apply netem, run, remove netem
