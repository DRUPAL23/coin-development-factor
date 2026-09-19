#!/bin/sh
set -eu

: "${COIN:=AceCoin}"
: "${NET:=testnet}"
: "${DB_DIRECTORY:=/data/electrumx}"
: "${SERVICES:=ssl://0.0.0.0:50002,rpc://127.0.0.1:8000}"
: "${REPORT_SERVICES:=ssl://127.0.0.1:50002}"

export COIN NET DB_DIRECTORY SERVICES REPORT_SERVICES

exec python /opt/electrumx/electrumx_server
