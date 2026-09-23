from __future__ import annotations
from pathlib import Path
from typing import Any
import yaml
from .models import ChainEndpoint, IntegrationSpec

def load_spec(path: str | Path) -> IntegrationSpec:
    raw: dict[str, Any] = yaml.safe_load(Path(path).read_text()) or {}
    data = raw.get("integration", raw)
    endpoints = tuple(ChainEndpoint(**item) for item in data.get("endpoints", []))
    return IntegrationSpec(
        name=data.get("name", ""),
        chain_id=int(data.get("chain_id", 0)),
        native_symbol=data.get("native_symbol", ""),
        endpoints=endpoints,
        wallet_adapter=data.get("wallet_adapter", "readonly"),
        observability=data.get("observability", {}),
    )

def summary(spec: IntegrationSpec) -> dict[str, Any]:
    return {"name": spec.name, "chain_id": spec.chain_id, "native_symbol": spec.native_symbol, "wallet_adapter": spec.wallet_adapter, "endpoints": [e.__dict__ for e in spec.endpoints], "health": spec.health_report(), "validation_errors": spec.validate()}
