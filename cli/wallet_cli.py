from __future__ import annotations

import argparse
import json
import sys

from wallets.engine import load_spec, summarize


def main() -> int:
    parser = argparse.ArgumentParser(description="Coin Development Factory wallet policy CLI")
    parser.add_argument("config")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        spec = load_spec(args.config)
        errors = spec.validate()
        if args.json:
            print(json.dumps(summarize(args.config), indent=2))
        else:
            if errors:
                for error in errors:
                    print(f"ERROR: {error}")
            else:
                print(f"Wallet policy is valid: {spec.name} ({spec.wallet_type})")
        return 1 if errors else 0
    except (OSError, ValueError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
