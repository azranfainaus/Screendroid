#!/usr/bin/env bash
# Scan the local /24 subnet for devices listening on ADB port 5555.

# Get the first non‑loopback IPv4 address
LOCAL_IP=$(hostname -I | awk '{print $1}')
if [[ -z "$LOCAL_IP" ]]; then
  exit 0
fi

BASE=$(echo "$LOCAL_IP" | cut -d. -f1-3)

for i in {1..254}; do
  IP="$BASE.$i"
  timeout 0.2 bash -c "</dev/tcp/$IP/5555" && echo "$IP"
done
