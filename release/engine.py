from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .models import DisasterRecoverySpec, ReleaseSpec


def load_spec(path: str | Path) -> ReleaseSpec:
    raw: dict[str, Any] = yaml.safe_load(Path(path).read_text()) or {}
    data = raw.get("release", raw)
    recovery = data.get("disaster_recovery", {})
    return ReleaseSpec(
        version=str(data.get("version", "")),
        artifact_digest=str(data.get("artifact_digest", "")),
        signed=bool(data.get("signed", False)),
        reproducible_build=bool(data.get("reproducible_build", False)),
        changelog_present=bool(data.get("changelog_present", False)),
        rollback_plan_present=bool(data.get("rollback_plan_present", False)),
        approvals=tuple(data.get("approvals", [])),
        disaster_recovery=DisasterRecoverySpec(
            backup_verified=bool(recovery.get("backup_verified", False)),
            restore_tested=bool(recovery.get("restore_tested", False)),
            recovery_point_objective_minutes=int(recovery.get("recovery_point_objective_minutes", 0)),
            recovery_time_objective_minutes=int(recovery.get("recovery_time_objective_minutes", 0)),
            runbook_url=str(recovery.get("runbook_url", "")),
            owner=str(recovery.get("owner", "")),
        ),
        metadata=data.get("metadata", {}),
    )


def summary(spec: ReleaseSpec) -> dict[str, Any]:
    return {
        "version": spec.version,
        "artifact_digest": spec.artifact_digest,
        "approvals": list(spec.approvals),
        "readiness": spec.readiness_report(),
        "metadata": spec.metadata,
    }
