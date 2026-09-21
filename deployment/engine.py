from __future__ import annotations
from pathlib import Path
from typing import Any
import yaml
from .models import DeploymentSpec

def load_spec(path: str | Path) -> DeploymentSpec:
    data: dict[str, Any] = yaml.safe_load(Path(path).read_text()) or {}
    raw = data.get("deployment", data)
    return DeploymentSpec(
        name=str(raw.get("name", "")), environment=str(raw.get("environment", "testnet")), provider=str(raw.get("provider", "docker")),
        chain_id=int(raw.get("chain_id", 0)), rpc_url=str(raw.get("rpc_url", "")), explorer_url=str(raw.get("explorer_url", "")),
        image=str(raw.get("image", "")), replicas=int(raw.get("replicas", 1)), validators=int(raw.get("validators", 1)),
        readiness={str(k): bool(v) for k, v in (raw.get("readiness") or {}).items()},
        secrets_required=tuple(str(x) for x in (raw.get("secrets_required") or [])), resources=raw.get("resources") or {},
    )

def summary(spec: DeploymentSpec) -> dict[str, object]:
    return {"name": spec.name, "environment": spec.environment, "provider": spec.provider, "chain_id": spec.chain_id, "rpc_url": spec.rpc_url, "explorer_url": spec.explorer_url, "replicas": spec.replicas, "validators": spec.validators, "validation_errors": spec.validate(), "readiness": spec.readiness_report()}
