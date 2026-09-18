from __future__ import annotations

from decimal import Decimal, ROUND_DOWN
from pathlib import Path
from typing import Any

import yaml

from staking.models import Delegation, StakingPolicy


def load_policy(path: str | Path) -> StakingPolicy:
    with Path(path).open("r", encoding="utf-8") as handle:
        data: dict[str, Any] = yaml.safe_load(handle) or {}
    staking = data.get("staking", {})
    return StakingPolicy(
        enabled=bool(staking.get("enabled", True)),
        min_stake=Decimal(str(staking.get("min_stake", 1))),
        unbonding_period_days=int(staking.get("unbonding_period_days", 7)),
        reward_rate_annual=Decimal(str(staking.get("reward_rate_annual", "0.10"))),
        commission_rate=Decimal(str(staking.get("commission_rate", "0.05"))),
        max_validators=int(staking.get("max_validators", 100)),
        reward_asset=str(staking.get("reward_asset", "native")),
    )


def calculate_reward(policy: StakingPolicy, amount: Decimal, duration_days: int) -> dict[str, str]:
    errors = policy.validate()
    if errors:
        raise ValueError("invalid staking policy: " + "; ".join(errors))
    delegation = Delegation("delegator", "validator", amount, duration_days)
    if delegation.validate():
        raise ValueError("invalid delegation: " + "; ".join(delegation.validate()))
    gross = amount * policy.reward_rate_annual * Decimal(duration_days) / Decimal(365)
    commission = gross * policy.commission_rate
    net = (gross - commission).quantize(Decimal("0.000000000000000001"), rounding=ROUND_DOWN)
    return {"principal": str(amount), "gross_reward": str(gross), "commission": str(commission), "net_reward": str(net)}


def summarize(path: str | Path) -> dict[str, Any]:
    policy = load_policy(path)
    return {"enabled": policy.enabled, "min_stake": str(policy.min_stake), "unbonding_period_days": policy.unbonding_period_days, "reward_rate_annual": str(policy.reward_rate_annual), "commission_rate": str(policy.commission_rate), "max_validators": policy.max_validators, "validation_errors": policy.validate()}
