from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class StakingPolicy:
    enabled: bool = True
    min_stake: Decimal = Decimal("1")
    unbonding_period_days: int = 7
    reward_rate_annual: Decimal = Decimal("0.10")
    commission_rate: Decimal = Decimal("0.05")
    max_validators: int = 100
    reward_asset: str = "native"

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.min_stake <= 0:
            errors.append("staking.min_stake must be greater than zero")
        if self.unbonding_period_days < 0:
            errors.append("staking.unbonding_period_days cannot be negative")
        if not Decimal("0") <= self.reward_rate_annual <= Decimal("1"):
            errors.append("staking.reward_rate_annual must be between 0 and 1")
        if not Decimal("0") <= self.commission_rate < Decimal("1"):
            errors.append("staking.commission_rate must be between 0 and 1")
        if self.max_validators < 1:
            errors.append("staking.max_validators must be at least one")
        if self.reward_asset not in {"native", "custom"}:
            errors.append("staking.reward_asset must be native or custom")
        return errors


@dataclass(frozen=True)
class Delegation:
    delegator: str
    validator: str
    amount: Decimal
    duration_days: int = 0

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.delegator.strip():
            errors.append("delegation.delegator is required")
        if not self.validator.strip():
            errors.append("delegation.validator is required")
        if self.amount <= 0:
            errors.append("delegation.amount must be greater than zero")
        if self.duration_days < 0:
            errors.append("delegation.duration_days cannot be negative")
        return errors
