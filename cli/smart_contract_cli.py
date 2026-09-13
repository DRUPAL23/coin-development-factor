from __future__ import annotations

import argparse
import sys
from pathlib import Path

from contracts.engine import generate_erc20, load_spec, validate_source


def main() -> int:
    parser = argparse.ArgumentParser(description="Coin Development Factory smart-contract CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate")
    validate.add_argument("config")

    generate = sub.add_parser("generate")
    generate.add_argument("config")
    generate.add_argument("output")

    args = parser.parse_args()
    try:
        spec = load_spec(args.config)
        errors = spec.validate()
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1

        if args.command == "validate":
            source = generate_erc20(spec)
            source_errors = validate_source(source)
            if source_errors:
                for error in source_errors:
                    print(f"ERROR: {error}")
                return 1
            print("Smart-contract configuration is valid.")
            return 0

        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(generate_erc20(spec), encoding="utf-8")
        print(f"Generated {output}")
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
