from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from wallets.models import WalletSpec


def load_spec(path: str | Path) -> WalletSpec:
    with Path(path).open("r", encoding="utf-8") as handle:
        data: dict[str, Any] = yaml.safe_load(handle) or {}
    wallet = data.get("wallet", {})
    return WalletSpec(
        name=str(wallet.get("name", "")),
        wallet_type=str(wallet.get("wallet_type", "hardware")),
        chain=str(wallet.get("chain", "evm")),
        derivation_path=str(wallet.get("derivation_path", "m/44'/60'/0'/0/0")),
        require_hardware_signing=bool(wallet.get("require_hardware_signing", True)),
        allow_private_key_export=bool(wallet.get("allow_private_key_export", False)),
        address=wallet.get("address"),
    )


def summarize(path: str | Path) -> dict[str, Any]:
    spec = load_spec(path)
    return {
        "name": spec.name,
        "wallet_type": spec.wallet_type,
        "chain": spec.chain,
        "derivation_path": spec.derivation_path,
        "validation_errors": spec.validate(),
    }
