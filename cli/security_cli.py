from __future__ import annotations

import argparse
from pathlib import Path
import sys

from security.static_checks import blocking_findings, scan_solidity


def main() -> int:
    parser = argparse.ArgumentParser(description="Coin Development Factory Solidity security scanner")
    parser.add_argument("source")
    args = parser.parse_args()
    try:
        findings = scan_solidity(Path(args.source).read_text(encoding="utf-8"))
        for finding in findings:
            print(f"{finding.severity.upper()} {finding.rule_id}: {finding.message}")
        if blocking_findings(findings):
            return 1
        print("No blocking security findings.")
        return 0
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
