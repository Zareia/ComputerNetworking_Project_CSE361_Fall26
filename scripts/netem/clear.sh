#!/usr/bin/env bash
# Usage: sudo ./clear.sh <iface>
IFACE="${1:-lo}"
tc qdisc del dev "$IFACE" root 2>/dev/null || true
tc qdisc show dev "$IFACE"
