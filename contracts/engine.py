from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from typing import Any

import yaml

from contracts.models import ContractSpec


def load_spec(path: str | Path) -> ContractSpec:
    """Load contract settings from YAML and normalize numeric values."""
    with Path(path).open("r", encoding="utf-8") as handle:
        data: dict[str, Any] = yaml.safe_load(handle) or {}
    contract = data.get("contract", {})
    supply = data.get("supply", {})
    mechanics = data.get("mechanics", {})
    coin = data.get("coin", {})
    return ContractSpec(
        name=str(contract.get("name", coin.get("name", ""))),
        symbol=str(contract.get("symbol", coin.get("symbol", ""))),
        decimals=int(contract.get("decimals", coin.get("decimals", 18))),
        initial_supply=Decimal(str(contract.get("initial_supply", supply.get("initial", 0)))),
        max_supply=Decimal(str(contract.get("max_supply", supply.get("max", 0)))),
        minting=bool(contract.get("minting", mechanics.get("minting", False))),
        burning=bool(contract.get("burning", mechanics.get("burning", False))),
        permit=bool(contract.get("permit", True)),
        target=str(contract.get("target", "evm")),
        solidity_pragma=str(contract.get("solidity_pragma", "^0.8.26")),
        contract_name=str(contract.get("contract_name", "CoinToken")),
    )


def _scaled_supply(value: Decimal, decimals: int) -> str:
    """Return a Solidity integer literal for a human-unit token amount."""
    scale = Decimal(10) ** decimals
    scaled = value * scale
    if scaled != scaled.to_integral_value():
        raise ValueError("supply values cannot contain more precision than token decimals")
    return str(scaled.to_integral_value())


def generate_erc20(spec: ContractSpec) -> str:
    """Generate deterministic OpenZeppelin-based ERC-20 Solidity source."""
    errors = spec.validate()
    if errors:
        raise ValueError("invalid contract specification: " + "; ".join(errors))

    imports = ["import {ERC20} from \"@openzeppelin/contracts/token/ERC20/ERC20.sol\";"]
    inheritance = ["ERC20"]
    constructor_base = [f"ERC20(\"{spec.name}\", \"{spec.symbol}\")"]
    body: list[str] = []

    if spec.burning:
        imports.append("import {ERC20Burnable} from \"@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol\";")
        inheritance.append("ERC20Burnable")

    if spec.permit:
        imports.append("import {ERC20Permit} from \"@openzeppelin/contracts/token/ERC20/extensions/ERC20Permit.sol\";")
        inheritance.append("ERC20Permit")
        constructor_base.append(f"ERC20Permit(\"{spec.name}\")")

    if spec.minting:
        imports.append("import {Ownable} from \"@openzeppelin/contracts/access/Ownable.sol\";")
        inheritance.append("Ownable")
        constructor_base.append("Ownable(msg.sender)")
        body.extend([
            "    /// @notice Mint new tokens without exceeding the configured supply cap.",
            "    /// @dev The owner must be governed by an external operational policy.",
            "    function mint(address to, uint256 amount) external onlyOwner {",
            "        require(totalSupply() + amount <= MAX_SUPPLY, \"max supply exceeded\");",
            "        _mint(to, amount);",
            "    }",
        ])

    body.extend([
        "    /// @dev Returns the configured token precision.",
        "    function decimals() public pure override returns (uint8) {",
        f"        return {spec.decimals};",
        "    }",
    ])

    max_supply = _scaled_supply(spec.max_supply, spec.decimals)
    initial_supply = _scaled_supply(spec.initial_supply, spec.decimals)
    body.insert(0, f"    uint256 public constant MAX_SUPPLY = {max_supply};")
    body.insert(1, "")
    body.insert(2, "    /// @dev Initial allocation is minted once to the deployer.")
    body.insert(3, "    constructor()" + ("\n        " + "\n        ".join(constructor_base) if constructor_base else "") + " {")
    body.insert(4, f"        _mint(msg.sender, {initial_supply});")
    body.insert(5, "    }")
    body.insert(6, "")

    return "\n".join([
        "// SPDX-License-Identifier: MIT",
        f"pragma solidity {spec.solidity_pragma};",
        "",
        *imports,
        "",
        f"contract {spec.contract_name} is {', '.join(inheritance)} {{",
        *body,
        "}",
        "",
    ])


def validate_source(source: str) -> list[str]:
    """Perform deterministic safety checks on generated Solidity source."""
    required = [
        "SPDX-License-Identifier:",
        "pragma solidity",
        "@openzeppelin/contracts/token/ERC20/ERC20.sol",
        "function decimals() public pure override returns (uint8)",
        "uint256 public constant MAX_SUPPLY",
        "_mint(msg.sender,",
    ]
    return [f"generated source is missing required marker: {marker}" for marker in required if marker not in source]
