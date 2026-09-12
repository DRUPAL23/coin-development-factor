from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from typing import Any

import yaml

from tokenomics.models import SupplyModel, Tokenomics, VestingSchedule


def load_config(path: str | Path) -> Tokenomics:
    with Path(path).open("r", encoding="utf-8") as handle:
        data: dict[str, Any] = yaml.safe_load(handle) or {}

    coin = data.get("coin", {})
    supply = data.get("supply", {})
    allocation = data.get("allocation", {})
    vesting = data.get("vesting", {})
    mechanics = data.get("mechanics", {})

    return Tokenomics(
        name=str(coin.get("name", "")),
        symbol=str(coin.get("symbol", "")),
        supply=SupplyModel(
            max_supply=Decimal(str(supply.get("max", 0))),
            initial_supply=Decimal(str(supply.get("initial", 0))),
            decimals=int(coin.get("decimals", 18)),
        ),
        allocation={key: Decimal(str(value)) for key, value in allocation.items()},
        vesting={
            key: VestingSchedule(
                cliff_months=int(value.get("cliff_months", 0)),
                duration_months=int(value.get("duration_months", 0)),
            )
            for key, value in vesting.items()
        },
        minting=bool(mechanics.get("minting", False)),
        burning=bool(mechanics.get("burning", False)),
        staking=bool(mechanics.get("staking", False)),
        governance=bool(mechanics.get("governance", False)),
    )


def calculate(path: str | Path) -> dict[str, Any]:
    model = load_config(path)
    return {
        "name": model.name,
        "symbol": model.symbol,
        "max_supply": str(model.supply.max_supply),
        "initial_supply": str(model.supply.initial_supply),
        "allocation_total_percent": str(model.allocation_total()),
        "allocation_amounts": {
            key: str(value) for key, value in model.allocation_amounts().items()
        },
        "validation_errors": model.validate(),
    }
