from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
import re


SUPPORTED_TARGETS = {"evm"}
SUPPORTED_SOLIDITY_PRAGMAS = {"^0.8.24", "^0.8.25", "^0.8.26"}


@dataclass(frozen=True)
class ContractSpec:
    """Validated inputs required to generate a deterministic ERC-20 contract."""

    name: str
    symbol: str
    decimals: int
    initial_supply: Decimal
    max_supply: Decimal
    minting: bool = False
    burning: bool = False
    permit: bool = True
    target: str = "evm"
    solidity_pragma: str = "^0.8.26"
    contract_name: str = "CoinToken"

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.name.strip():
            errors.append("contract.name is required")
        if not self.symbol.strip():
            errors.append("contract.symbol is required")
        if not 0 <= self.decimals <= 36:
            errors.append("contract.decimals must be between 0 and 36")
        if self.initial_supply < 0:
            errors.append("contract.initial_supply cannot be negative")
        if self.max_supply <= 0:
            errors.append("contract.max_supply must be greater than zero")
        if self.initial_supply > self.max_supply:
            errors.append("contract.initial_supply cannot exceed contract.max_supply")
        if self.target not in SUPPORTED_TARGETS:
            errors.append(f"contract.target must be one of: {', '.join(sorted(SUPPORTED_TARGETS))}")
        if self.solidity_pragma not in SUPPORTED_SOLIDITY_PRAGMAS:
            errors.append("contract.solidity_pragma is not supported")
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", self.contract_name):
            errors.append("contract.contract_name must be a valid Solidity identifier")
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9 ._-]*", self.symbol):
            errors.append("contract.symbol contains unsupported characters")
        return errors
