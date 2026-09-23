from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlparse

@dataclass(frozen=True)
class ChainEndpoint:
    name: str
    url: str
    transport: str = "http"
    timeout_seconds: float = 5.0
    required: bool = True

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.name.strip(): errors.append("endpoint.name is required")
        if urlparse(self.url).scheme not in {"http", "https", "ws", "wss"}: errors.append(f"endpoint.{self.name}.url must use http(s) or ws(s)")
        if self.timeout_seconds <= 0: errors.append(f"endpoint.{self.name}.timeout_seconds must be positive")
        return errors

@dataclass(frozen=True)
class IntegrationSpec:
    name: str
    chain_id: int
    native_symbol: str
    endpoints: tuple[ChainEndpoint, ...] = ()
    wallet_adapter: str = "readonly"
    observability: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.name.strip(): errors.append("integration.name is required")
        if self.chain_id <= 0: errors.append("integration.chain_id must be greater than zero")
        if not self.native_symbol.strip(): errors.append("integration.native_symbol is required")
        if self.wallet_adapter not in {"readonly", "custodial", "external"}: errors.append("integration.wallet_adapter is unsupported")
        if not self.endpoints: errors.append("integration.endpoints must not be empty")
        for endpoint in self.endpoints: errors.extend(endpoint.validate())
        return errors

    def health_report(self) -> dict[str, Any]:
        checks = {f"endpoint:{e.name}": bool(e.url) for e in self.endpoints}
        checks["config_valid"] = not self.validate()
        checks["metrics_enabled"] = bool(self.observability.get("metrics_enabled", False))
        checks["structured_logging_enabled"] = bool(self.observability.get("structured_logging_enabled", False))
        return {"ready": all(checks.values()), "checks": checks, "chain_id": self.chain_id, "native_symbol": self.native_symbol}
