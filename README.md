# Coin Development Factory

A reusable framework for designing, validating, and eventually deploying crypto token and native-coin projects.

## Sprint 1 — Tokenomics Engine

Sprint 1 establishes the economic specification layer before smart-contract or blockchain implementation.

- Supply configuration and validation
- Allocation percentages and token quantities
- Vesting schedules
- Emission and burn configuration
- Machine-readable YAML configuration
- Python domain models and CLI foundation

## Sprint 2 — Blockchain Architecture

Sprint 2 converts the economic specification into a machine-readable technical architecture contract.

- Network identity and environment metadata
- Chain type selection: EVM, Solana, Cosmos, Substrate, or sovereign
- Consensus mechanism and safety parameters
- Execution/runtime configuration
- RPC exposure controls
- Storage and pruning policy
- Architecture validation and CI enforcement

## Sprint 3 — Smart Contract Engine

Sprint 3 converts a validated contract specification into deterministic Solidity source for an EVM ERC-20 deployment.

### Scope

- Typed smart-contract specification model
- EVM target validation
- Solidity compiler pragma allow-list
- OpenZeppelin ERC-20 base implementation
- Optional burnable extension
- Optional EIP-2612 permit extension
- Optional owner-controlled minting with a hard maximum-supply cap
- Initial supply minted to the deployer
- Explicit token-decimal handling
- Deterministic source generation
- Generated-source structural validation
- JSON Schema for contract configuration
- CLI validation and generation
- Unit tests for valid and invalid contract specifications
- CI validation and generation smoke test

### Commands

```bash
# Tokenomics
python -m cli.tokenomics_cli validate config/examples/example-coin.yaml
python -m cli.tokenomics_cli calculate config/examples/example-coin.yaml

# Architecture
python - <<'PY'
from architecture.engine import load_config
model = load_config('config/examples/example-architecture.yaml')
print(model.validate())
PY

# Smart contract
python -m cli.smart_contract_cli validate config/examples/example-contract.yaml
python -m cli.smart_contract_cli generate \
  config/examples/example-contract.yaml \
  build/contracts/ExampleCoin.sol

# Full test suite
pytest -q
```

### Generated contract policy

The engine generates source code that imports OpenZeppelin Contracts rather than copying third-party library implementations into this repository. The generated source should be compiled against a pinned OpenZeppelin dependency and reviewed/audited before deployment. CI currently performs Python tests plus deterministic Solidity-source smoke validation; it does not treat source generation as a substitute for a compiler, audit, or deployment review.

## Project status

**Sprint 3: Smart Contract Engine — complete**

Next: **Sprint 4 — Testing & Security**.

## Design principle

Economic parameters are configuration, not hard-coded implementation assumptions. The same specification should feed contract generation, testing, deployment, and analytics.

## Disclaimer

This repository provides software and economic modeling infrastructure. It is not financial, investment, legal, tax, or regulatory advice. Token launches must be reviewed for applicable laws and regulations before deployment or distribution.
