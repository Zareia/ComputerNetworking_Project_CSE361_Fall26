#!/usr/bin/env bash
# Usage: sudo ./apply.sh <iface> <profile>
# Profiles: loss10 | delay150
set -euo pipefail
IFACE="${1:-lo}"
PROFILE="${2:?profile required}"

case "$PROFILE" in
  loss10)   tc qdisc add dev "$IFACE" root netem loss 10% ;;
  delay150) tc qdisc add dev "$IFACE" root netem delay 150ms ;;
  *) echo "unknown profile: $PROFILE" >&2; exit 1 ;;
esac
tc qdisc show dev "$IFACE"
