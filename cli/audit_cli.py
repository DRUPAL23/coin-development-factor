from __future__ import annotations
import argparse, json
from audit.engine import load_spec

def main() -> None:
    p=argparse.ArgumentParser(description='Validate audit and mainnet launch controls')
    p.add_argument('config')
    p.add_argument('--json', action='store_true')
    args=p.parse_args(); report=load_spec(args.config).report()
    if args.json: print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"network={report['network']} release={report['release_version']} ready={report['ready']}")
        for e in report['validation_errors']: print(f"ERROR: {e}")
    raise SystemExit(0 if report['ready'] else 1)
if __name__ == '__main__': main()
