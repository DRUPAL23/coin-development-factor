from decimal import Decimal
from pathlib import Path

import pytest

from staking.engine import calculate_reward, load_policy
from staking.models import StakingPolicy

ROOT = Path(__file__).parents[1]
EXAMPLE = ROOT / "config/examples/example-staking.yaml"


def test_example_policy_validates() -> None:
    policy = load_policy(EXAMPLE)
    assert policy.validate() == []
    assert policy.min_stake == Decimal("100")


def test_reward_calculation_applies_commission() -> None:
    policy = load_policy(EXAMPLE)
    result = calculate_reward(policy, Decimal("1000"), 365)
    assert result["gross_reward"] == "100.00"
    assert result["commission"] == "5.0000"
    assert result["net_reward"] == "95.000000000000000000"


def test_invalid_rate_rejected() -> None:
    policy = StakingPolicy(reward_rate_annual=Decimal("1.1"))
    assert any("reward_rate_annual" in error for error in policy.validate())


def test_invalid_delegation_amount_rejected() -> None:
    policy = load_policy(EXAMPLE)
    with pytest.raises(ValueError, match="amount"):
        calculate_reward(policy, Decimal("0"), 10)


def test_negative_duration_rejected() -> None:
    policy = load_policy(EXAMPLE)
    with pytest.raises(ValueError, match="duration_days"):
        calculate_reward(policy, Decimal("100"), -1)
