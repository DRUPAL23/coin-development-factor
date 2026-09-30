#!/bin/sh
set -eu

required="DAEMON_URL COIN NET DB_DIRECTORY SERVICES SSL_CERTFILE SSL_KEYFILE"
for name in $required; do
  eval "value=\${$name:-}"
  if [ -z "$value" ]; then
    echo "missing required variable: $name" >&2
    exit 1
  fi
done

case "$COIN:$NET" in
  AceCoin:testnet) ;;
  *) echo "unsupported integration target: $COIN:$NET" >&2; exit 1 ;;
esac

case "${ACECOIN_TESTNET_GENESIS_HASH:-}" in
  ""|REPLACE_WITH_REAL_TESTNET_GENESIS_HASH|0000000000000000000000000000000000000000000000000000000000000000)
    echo "ACECOIN_TESTNET_GENESIS_HASH is not configured" >&2
    exit 1
    ;;
esac

echo "AceCoin ElectrumX configuration passed static validation."
