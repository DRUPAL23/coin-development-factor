from __future__ import annotations

from dataclasses import dataclass
import re


EVM_ADDRESS_RE = re.compile(r"^0x[a-fA-F0-9]{40}$")
DERIVATION_PATH_RE = re.compile(r"^m(?:/[0-9]+'?)+$")
SUPPORTED_WALLET_TYPES = {"browser", "hardware", "mobile", "custody_external"}


@dataclass(frozen=True)
class WalletSpec:
    name: str
    wallet_type: str = "hardware"
    chain: str = "evm"
    derivation_path: str = "m/44'/60'/0'/0/0"
    require_hardware_signing: bool = True
    allow_private_key_export: bool = False
    address: str | None = None

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.name.strip():
            errors.append("wallet.name is required")
        if self.wallet_type not in SUPPORTED_WALLET_TYPES:
            errors.append(f"wallet.wallet_type must be one of: {', '.join(sorted(SUPPORTED_WALLET_TYPES))}")
        if self.chain != "evm":
            errors.append("wallet.chain must be evm for Sprint 5")
        if not DERIVATION_PATH_RE.fullmatch(self.derivation_path):
            errors.append("wallet.derivation_path must use BIP-44 style syntax")
        if self.wallet_type == "hardware" and not self.require_hardware_signing:
            errors.append("hardware wallets must require hardware signing")
        if self.require_hardware_signing and self.allow_private_key_export:
            errors.append("private-key export cannot be allowed when hardware signing is required")
        if self.address is not None and not EVM_ADDRESS_RE.fullmatch(self.address):
            errors.append("wallet.address must be a 20-byte EVM hex address")
        return errors
