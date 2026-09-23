from __future__ import annotations
import argparse, json
from integration.engine import load_spec, summary

def main() -> int:
    parser = argparse.ArgumentParser(description="Validate wallet/chain integration readiness")
    parser.add_argument("config")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = summary(load_spec(args.config))
    print(json.dumps(result, indent=2, sort_keys=True) if args.json else result)
    return 0 if not result["validation_errors"] and result["health"]["ready"] else 1

if __name__ == "__main__": raise SystemExit(main())
