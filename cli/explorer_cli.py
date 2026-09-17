from __future__ import annotations

import argparse
import json

from explorer.indexer import Indexer
from explorer.models import Block, Transaction


def main() -> int:
    parser = argparse.ArgumentParser(description="Coin Development Factory explorer CLI")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    indexer = Indexer()
    block = Block(0, "0x" + "0" * 64, "0x" + "0" * 64, 1, 0)
    indexer.add_block(block)
    payload = indexer.status()
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"Indexed: {payload['indexed']}; latest block: {payload['latest_block']['number']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
