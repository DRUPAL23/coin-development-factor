from decimal import Decimal
from pathlib import Path

import pytest

from contracts.engine import generate_erc20, load_spec, validate_source
from contracts.models import ContractSpec


ROOT = Path(__file__).parents[1]
EXAMPLE = ROOT / "config/examples/example-contract.yaml"


def test_example_contract_loads_and_validates() -> None:
    spec = load_spec(EXAMPLE)
    assert spec.validate() == []
    assert spec.symbol == "EXC"
    assert spec.initial_supply == Decimal("500000000")


def test_generator_is_deterministic() -> None:
    spec = load_spec(EXAMPLE)
    assert generate_erc20(spec) == generate_erc20(spec)


def test_generated_source_contains_required_features() -> None:
    source = generate_erc20(load_spec(EXAMPLE))
    assert "contract ExampleCoin is ERC20, ERC20Burnable, ERC20Permit" in source
    assert "uint256 public constant MAX_SUPPLY = 1000000000000000000000000000;" in source
    assert "_mint(msg.sender, 500000000000000000000000000);" in source
    assert "function decimals() public pure override returns (uint8)" in source
    assert "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol" in source
    assert "@openzeppelin/contracts/token/ERC20/extensions/ERC20Permit.sol" in source
    assert validate_source(source) == []


def test_minting_adds_owner_guard() -> None:
    spec = ContractSpec(
        name="Mintable Coin",
        symbol="MNT",
        decimals=18,
        initial_supply=Decimal("100"),
        max_supply=Decimal("1000"),
        minting=True,
        burning=False,
        permit=False,
        contract_name="MintableCoin",
    )
    source = generate_erc20(spec)
    assert "import {Ownable}" in source
    assert "Ownable(msg.sender)" in source
    assert "function mint(address to, uint256 amount) external onlyOwner" in source
    assert "totalSupply() + amount <= MAX_SUPPLY" in source


def test_initial_supply_cannot_exceed_max_supply() -> None:
    spec = ContractSpec(
        name="Invalid",
        symbol="BAD",
        decimals=18,
        initial_supply=Decimal("1001"),
        max_supply=Decimal("1000"),
    )
    with pytest.raises(ValueError, match="initial_supply cannot exceed"):
        generate_erc20(spec)


def test_precision_cannot_exceed_decimals() -> None:
    spec = ContractSpec(
        name="Precise",
        symbol="PRC",
        decimals=2,
        initial_supply=Decimal("1.001"),
        max_supply=Decimal("2"),
    )
    with pytest.raises(ValueError, match="more precision"):
        generate_erc20(spec)


def test_invalid_contract_identifier_is_rejected() -> None:
    spec = ContractSpec(
        name="Invalid",
        symbol="BAD",
        decimals=18,
        initial_supply=Decimal("1"),
        max_supply=Decimal("2"),
        contract_name="123Bad",
    )
    assert any("valid Solidity identifier" in error for error in spec.validate())
