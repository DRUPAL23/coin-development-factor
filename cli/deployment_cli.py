from __future__ import annotations
import argparse, json
from deployment.engine import load_spec, summary

def main() -> int:
    p=argparse.ArgumentParser(description='Validate deployment readiness')
    p.add_argument('config'); p.add_argument('--json', action='store_true')
    args=p.parse_args(); result=summary(load_spec(args.config))
    print(json.dumps(result, indent=2) if args.json else ('VALID' if not result['validation_errors'] else '\n'.join(result['validation_errors'])))
    return 0 if not result['validation_errors'] else 1
if __name__ == '__main__': raise SystemExit(main())
