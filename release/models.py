from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class DisasterRecoverySpec:
    backup_verified: bool = False
    restore_tested: bool = False
    recovery_point_objective_minutes: int = 0
    recovery_time_objective_minutes: int = 0
    runbook_url: str = ""
    owner: str = ""

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.backup_verified:
            errors.append("disaster_recovery.backup_verified must be true")
        if not self.restore_tested:
            errors.append("disaster_recovery.restore_tested must be true")
        if self.recovery_point_objective_minutes <= 0:
            errors.append("disaster_recovery.recovery_point_objective_minutes must be positive")
        if self.recovery_time_objective_minutes <= 0:
            errors.append("disaster_recovery.recovery_time_objective_minutes must be positive")
        if not self.runbook_url.strip():
            errors.append("disaster_recovery.runbook_url is required")
        if not self.owner.strip():
            errors.append("disaster_recovery.owner is required")
        return errors


@dataclass(frozen=True)
class ReleaseSpec:
    version: str
    artifact_digest: str
    signed: bool = False
    reproducible_build: bool = False
    changelog_present: bool = False
    rollback_plan_present: bool = False
    approvals: tuple[str, ...] = ()
    disaster_recovery: DisasterRecoverySpec = field(default_factory=DisasterRecoverySpec)
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.version.strip():
            errors.append("release.version is required")
        if not self.artifact_digest.startswith("sha256:"):
            errors.append("release.artifact_digest must start with sha256:")
        if not self.signed:
            errors.append("release.signed must be true")
        if not self.reproducible_build:
            errors.append("release.reproducible_build must be true")
        if not self.changelog_present:
            errors.append("release.changelog_present must be true")
        if not self.rollback_plan_present:
            errors.append("release.rollback_plan_present must be true")
        if len(self.approvals) < 2:
            errors.append("release.approvals must contain at least two approvers")
        errors.extend(self.disaster_recovery.validate())
        return errors

    def readiness_report(self) -> dict[str, Any]:
        checks = {
            "config_valid": not self.validate(),
            "artifact_signed": self.signed,
            "reproducible_build": self.reproducible_build,
            "changelog_present": self.changelog_present,
            "rollback_plan_present": self.rollback_plan_present,
            "two_person_approval": len(self.approvals) >= 2,
            "backup_verified": self.disaster_recovery.backup_verified,
            "restore_tested": self.disaster_recovery.restore_tested,
        }
        return {
            "ready": all(checks.values()),
            "checks": checks,
            "version": self.version,
            "validation_errors": self.validate(),
        }
