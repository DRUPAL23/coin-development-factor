from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Optional


@dataclass(frozen=True)
class SupplyModel:
    max_supply: Decimal
    initial_supply: Decimal
    decimals: int = 18


@dataclass(frozen=True)
class VestingSchedule:
    cliff_months: int = 0
    duration_months: int = 0

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.cliff_months < 0:
            errors.append("cliff_months cannot be negative")
        if self.duration_months < 0:
            errors.append("duration_months cannot be negative")
        if self.duration_months and self.cliff_months > self.duration_months:
            errors.append("cliff_months cannot exceed duration_months")
        return errors


@dataclass(frozen=True)
class Tokenomics:
    name: str
    symbol: str
    supply: SupplyModel
    allocation: Dict[str, Decimal]
    vesting: Dict[str, VestingSchedule] = field(default_factory=dict)
    minting: bool = False
    burning: bool = False
    staking: bool = False
    governance: bool = False

    def allocation_total(self) -> Decimal:
        return sum(self.allocation.values(), Decimal("0"))

    def allocation_amounts(self) -> Dict[str, Decimal]:
        return {
            category: self.supply.max_supply * percentage / Decimal("100")
            for category, percentage in self.allocation.items()
        }

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.name.strip():
            errors.append("coin.name is required")
        if not self.symbol.strip():
            errors.append("coin.symbol is required")
        if not 0 <= self.supply.decimals <= 36:
            errors.append("decimals must be between 0 and 36")
        if self.supply.max_supply <= 0:
            errors.append("max_supply must be greater than zero")
        if self.supply.initial_supply < 0:
            errors.append("initial_supply cannot be negative")
        if self.supply.initial_supply > self.supply.max_supply:
            errors.append("initial_supply cannot exceed max_supply")
        if any(value < 0 for value in self.allocation.values()):
            errors.append("allocation percentages cannot be negative")
        if self.allocation_total() != Decimal("100"):
            errors.append("allocation percentages must total exactly 100")
        for category, schedule in self.vesting.items():
            errors.extend(f"vesting.{category}: {error}" for error in schedule.validate())
        return errors
