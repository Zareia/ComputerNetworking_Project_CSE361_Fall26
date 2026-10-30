#!/usr/bin/env bash
# Usage: sudo ./apply.sh <iface> <profile> [server_port]
# Profiles: loss10 | delay150 (delays server outbound traffic only)
set -euo pipefail
IFACE="${1:-lo}"
PROFILE="${2:?profile required}"
SERVER_PORT="${3:-9000}"

case "$PROFILE" in
  loss10)
    tc qdisc add dev "$IFACE" root netem loss 10%
    ;;
  delay150)
    tc qdisc add dev "$IFACE" root handle 1: prio
    tc qdisc add dev "$IFACE" parent 1:3 handle 30: netem delay 150ms
    tc filter add dev "$IFACE" parent 1:0 protocol ip u32 \
      match ip sport "$SERVER_PORT" 0xffff flowid 1:3
    ;;
  *) echo "unknown profile: $PROFILE" >&2; exit 1 ;;
esac
tc qdisc show dev "$IFACE"
