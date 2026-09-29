from __future__ import annotations
from pathlib import Path
from typing import Any
import yaml
from .models import IncidentPolicy, OperationsSpec, SLOSpec

def load_spec(path: str | Path) -> OperationsSpec:
    data = yaml.safe_load(Path(path).read_text()) or {}
    raw = data.get("operations", data)
    slos = tuple(SLOSpec(**item) for item in raw.get("slos", []))
    policies = tuple(IncidentPolicy(
        severity=item["severity"],
        acknowledgement_minutes=int(item["acknowledgement_minutes"]),
        update_interval_minutes=int(item["update_interval_minutes"]),
        escalation_path=tuple(item.get("escalation_path", [])),
        runbook_url=item.get("runbook_url", ""),
    ) for item in raw.get("incident_policies", []))
    return OperationsSpec(
        name=raw.get("name", ""),
        service=raw.get("service", ""),
        environment=raw.get("environment", ""),
        slos=slos,
        incident_policies=policies,
        paging_enabled=bool(raw.get("paging_enabled", False)),
        metrics_enabled=bool(raw.get("metrics_enabled", False)),
        logs_enabled=bool(raw.get("logs_enabled", False)),
        traces_enabled=bool(raw.get("traces_enabled", False)),
        oncall_roster=tuple(raw.get("oncall_roster", [])),
        status_page_url=raw.get("status_page_url", ""),
        metadata=raw.get("metadata", {}),
    )

def summary(spec: OperationsSpec) -> dict[str, Any]:
    report = spec.readiness_report()
    return {
        "name": spec.name,
        "service": spec.service,
        "environment": spec.environment,
        "slos": [s.__dict__ for s in spec.slos],
        "incident_policies": [p.__dict__ for p in spec.incident_policies],
        **report,
    }
