#!/usr/bin/env bash
# Usage: sudo ./capture_pcap.sh <iface> <port> <output.pcap>
set -euo pipefail
IFACE="${1:-lo}"
PORT="${2:-9000}"
OUT="${3:-results/pcap/capture.pcap}"
tcpdump -i "$IFACE" -w "$OUT" udp port "$PORT"
