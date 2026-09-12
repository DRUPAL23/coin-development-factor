from __future__ import annotations

import argparse
import json
import sys

from tokenomics.engine import calculate, load_config


def main() -> int:
    parser = argparse.ArgumentParser(description="Coin Development Factory tokenomics CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    for command in ("validate", "calculate"):
        cmd = sub.add_parser(command)
        cmd.add_argument("config")

    args = parser.parse_args()
    try:
        if args.command == "validate":
            model = load_config(args.config)
            errors = model.validate()
            if errors:
                for error in errors:
                    print(f"ERROR: {error}")
                return 1
            print("Tokenomics configuration is valid.")
            return 0

        print(json.dumps(calculate(args.config), indent=2))
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
