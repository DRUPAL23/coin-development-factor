from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal

from staking.engine import calculate_reward, load_policy, summarize


def main() -> int:
    parser = argparse.ArgumentParser(description="Coin Development Factory staking CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate")
    validate.add_argument("config")
    reward = sub.add_parser("reward")
    reward.add_argument("config")
    reward.add_argument("amount", type=Decimal)
    reward.add_argument("duration_days", type=int)
    args = parser.parse_args()
    try:
        policy = load_policy(args.config)
        errors = policy.validate()
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        if args.command == "validate":
            print(json.dumps(summarize(args.config), indent=2))
        else:
            print(json.dumps(calculate_reward(policy, args.amount, args.duration_days), indent=2))
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
