from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

SEVERITIES = {"critical", "high", "medium", "low", "info"}
REQUIRED_CONTROLS = ("security_audit_complete", "key_ceremony_rehearsed", "rollback_plan_tested", "incident_response_approved", "legal_review_complete")

@dataclass(frozen=True)
class AuditFinding:
    finding_id: str
    severity: str
    title: str
    status: str = "open"
    owner: str = ""
    evidence: str = ""
    remediation: str = ""

    def validate(self) -> list[str]:
        errors=[]
        if not self.finding_id.strip(): errors.append("finding_id is required")
        if self.severity not in SEVERITIES: errors.append(f"unsupported severity: {self.severity}")
        if not self.title.strip(): errors.append(f"{self.finding_id}: title is required")
        if self.status not in {"open","accepted","resolved"}: errors.append(f"{self.finding_id}: unsupported status")
        if self.severity in {"critical","high"} and self.status != "resolved": errors.append(f"{self.finding_id}: critical/high findings must be resolved")
        return errors

@dataclass(frozen=True)
class LaunchControlSpec:
    name: str
    release_version: str
    network: str
    controls: dict[str, bool] = field(default_factory=dict)
    findings: tuple[AuditFinding, ...] = ()
    evidence: dict[str, str] = field(default_factory=dict)
    change_freeze: bool = False
    rollback_window_minutes: int = 0
    signoff_roles: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> list[str]:
        errors=[]
        if not self.name.strip(): errors.append("audit.name is required")
        if not self.release_version.strip(): errors.append("audit.release_version is required")
        if self.network not in {"testnet","staging","mainnet"}: errors.append("audit.network is unsupported")
        if self.network == "mainnet" and self.rollback_window_minutes < 30: errors.append("mainnet rollback_window_minutes must be at least 30")
        if self.network == "mainnet" and not self.change_freeze: errors.append("mainnet change_freeze must be enabled")
        if not self.signoff_roles: errors.append("at least one signoff role is required")
        for control in REQUIRED_CONTROLS:
            if not self.controls.get(control, False): errors.append(f"required control not satisfied: {control}")
        for finding in self.findings: errors.extend(finding.validate())
        if self.network == "mainnet" and any(f.severity in {"critical","high"} and f.status != "resolved" for f in self.findings): errors.append("mainnet cannot launch with unresolved critical/high findings")
        return errors

    def report(self) -> dict[str, object]:
        errors=self.validate()
        return {"ready": not errors, "validation_errors": errors, "controls": {k:self.controls.get(k,False) for k in REQUIRED_CONTROLS}, "findings": [f.__dict__ for f in self.findings], "release_version": self.release_version, "network": self.network}
