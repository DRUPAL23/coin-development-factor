from decimal import Decimal

from tokenomics.models import SupplyModel, Tokenomics, VestingSchedule


def make_model(**overrides):
    data = dict(
        name="Example Coin",
        symbol="EXC",
        supply=SupplyModel(Decimal("1000000000"), Decimal("500000000"), 18),
        allocation={
            "community": Decimal("30"),
            "ecosystem": Decimal("20"),
            "liquidity": Decimal("15"),
            "treasury": Decimal("10"),
            "team": Decimal("10"),
            "investors": Decimal("10"),
            "partnerships": Decimal("5"),
        },
    )
    data.update(overrides)
    return Tokenomics(**data)


def test_valid_tokenomics():
    assert make_model().validate() == []


def test_allocation_must_equal_100_percent():
    model = make_model(allocation={"team": Decimal("50")})
    assert "allocation percentages must total exactly 100" in model.validate()


def test_initial_supply_cannot_exceed_max_supply():
    model = make_model(
        supply=SupplyModel(Decimal("100"), Decimal("101"), 18)
    )
    assert "initial_supply cannot exceed max_supply" in model.validate()


def test_vesting_cliff_cannot_exceed_duration():
    model = make_model(
        vesting={"team": VestingSchedule(cliff_months=24, duration_months=12)}
    )
    assert any("cliff_months cannot exceed duration_months" in e for e in model.validate())


def test_allocation_amounts_use_max_supply():
    amounts = make_model().allocation_amounts()
    assert amounts["community"] == Decimal("300000000")
    assert amounts["team"] == Decimal("100000000")
