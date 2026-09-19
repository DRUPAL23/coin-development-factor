from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal

from governance.engine import evaluate_proposal, load_policy
from governance.models import Proposal


def main() -> int:
    parser = argparse.ArgumentParser(description="Coin Development Factory governance CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate")
    validate.add_argument("config")
    evaluate = sub.add_parser("evaluate")
    evaluate.add_argument("config")
    evaluate.add_argument("proposal_id")
    evaluate.add_argument("title")
    evaluate.add_argument("proposal_type")
    evaluate.add_argument("proposer")
    evaluate.add_argument("voting_power")
    evaluate.add_argument("total_voting_power")
    evaluate.add_argument("yes_votes")
    evaluate.add_argument("no_votes")
    evaluate.add_argument("abstain_votes", nargs="?", default="0")
    args = parser.parse_args()
    try:
        policy = load_policy(args.config)
        policy_errors = policy.validate()
        if policy_errors:
            for error in policy_errors:
                print(f"ERROR: {error}")
            return 1
        if args.command == "validate":
            print("Governance policy is valid.")
            return 0
        proposal = Proposal(
            proposal_id=args.proposal_id,
            title=args.title,
            proposal_type=args.proposal_type,
            proposer=args.proposer,
            voting_power=Decimal(args.voting_power),
            total_voting_power=Decimal(args.total_voting_power),
            yes_votes=Decimal(args.yes_votes),
            no_votes=Decimal(args.no_votes),
            abstain_votes=Decimal(args.abstain_votes),
        )
        result = evaluate_proposal(policy, proposal)
        print(json.dumps(result, indent=2))
        return 0 if not result["validation_errors"] else 1
    except (OSError, ValueError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
