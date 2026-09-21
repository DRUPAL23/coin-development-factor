from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

SUPPORTED_ENVIRONMENTS = {"local", "testnet", "staging", "mainnet"}
SUPPORTED_PROVIDERS = {"docker", "kubernetes", "managed"}
REQUIRED_READINESS_CHECKS = (
    "genesis_published",
    "monitoring_configured",
    "backups_configured",
)

@dataclass(frozen=True)
class DeploymentSpec:
    name: str
    environment: str
    provider: str
    chain_id: int
    rpc_url: str
    explorer_url: str = ""
    image: str = ""
    replicas: int = 1
    validators: int = 1
    readiness: dict[str, bool] = field(default_factory=dict)
    secrets_required: tuple[str, ...] = ()
    resources: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.name.strip(): errors.append("deployment.name is required")
        if self.environment not in SUPPORTED_ENVIRONMENTS: errors.append("deployment.environment is unsupported")
        if self.provider not in SUPPORTED_PROVIDERS: errors.append("deployment.provider is unsupported")
        if self.chain_id <= 0: errors.append("deployment.chain_id must be greater than zero")
        if not self.rpc_url.startswith(("http://", "https://")): errors.append("deployment.rpc_url must be an HTTP(S) URL")
        if self.environment == "mainnet" and not self.rpc_url.startswith("https://"): errors.append("mainnet RPC must use HTTPS")
        if self.environment == "mainnet" and not self.explorer_url.startswith("https://"): errors.append("mainnet explorer_url must use HTTPS")
        if self.replicas < 1: errors.append("deployment.replicas must be at least one")
        if self.validators < 1: errors.append("deployment.validators must be at least one")
        if self.environment == "mainnet" and self.validators < 4: errors.append("mainnet requires at least four validators")
        if not self.image.strip(): errors.append("deployment.image is required")
        return errors

    def readiness_report(self) -> dict[str, object]:
        checks = {
            "config_valid": not self.validate(),
            "rpc_configured": bool(self.rpc_url),
            "explorer_configured": bool(self.explorer_url),
            "container_image_configured": bool(self.image),
            "secrets_declared": bool(self.secrets_required),
            **{name: self.readiness.get(name, False) for name in REQUIRED_READINESS_CHECKS},
            **{name: value for name, value in self.readiness.items() if name not in REQUIRED_READINESS_CHECKS},
        }
        return {"ready": all(checks.values()), "checks": checks}
