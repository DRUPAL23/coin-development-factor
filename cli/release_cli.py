from __future__ import annotations

import argparse
import json

from release.engine import load_spec, summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate release and disaster-recovery readiness")
    parser.add_argument("config")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = summary(load_spec(args.config))
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        readiness = report["readiness"]
        print(f"version={report['version']} ready={readiness['ready']}")
        for error in readiness["validation_errors"]:
            print(f"ERROR: {error}")


if __name__ == "__main__":
    main()
