from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class SecurityFinding:
    rule_id: str
    severity: str
    message: str


_FORBIDDEN_PATTERNS = (
    ("SC001", "high", r"tx\.origin", "tx.origin must not be used for authorization"),
    ("SC002", "high", r"delegatecall\s*\(", "delegatecall requires explicit upgrade/security review"),
    ("SC003", "medium", r"selfdestruct\s*\(", "selfdestruct is prohibited in generated contracts"),
    ("SC004", "medium", r"block\.timestamp", "timestamp-dependent logic requires explicit review"),
)


def scan_solidity(source: str) -> list[SecurityFinding]:
    """Run conservative lexical security checks on Solidity source."""
    findings: list[SecurityFinding] = []
    for rule_id, severity, pattern, message in _FORBIDDEN_PATTERNS:
        if re.search(pattern, source):
            findings.append(SecurityFinding(rule_id, severity, message))
    if "MAX_SUPPLY" not in source:
        findings.append(SecurityFinding("SC005", "high", "missing explicit MAX_SUPPLY cap"))
    if "_mint(msg.sender," not in source:
        findings.append(SecurityFinding("SC006", "medium", "initial mint allocation marker not found"))
    return findings


def blocking_findings(findings: list[SecurityFinding]) -> list[SecurityFinding]:
    return [finding for finding in findings if finding.severity in {"high", "critical"}]
