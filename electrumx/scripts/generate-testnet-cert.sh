#!/bin/sh
set -eu

HOST="${1:-electrum-testnet.example.org}"
OUT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")/../certs" && pwd)"

mkdir -p "$OUT_DIR"

openssl req -x509 -newkey rsa:4096 -sha256 -nodes \
  -days 365 \
  -keyout "$OUT_DIR/server.key" \
  -out "$OUT_DIR/server.crt" \
  -subj "/CN=$HOST" \
  -addext "subjectAltName=DNS:$HOST"

chmod 600 "$OUT_DIR/server.key"
chmod 644 "$OUT_DIR/server.crt"

echo "Created:"
echo "  $OUT_DIR/server.crt"
echo "  $OUT_DIR/server.key"
