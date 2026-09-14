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

- Typed smart-contract specification model
- EVM target validation
- Solidity compiler pragma allow-list
- OpenZeppelin ERC-20 base implementation
- Optional burnable and permit extensions
- Optional owner-controlled minting with a hard maximum-supply cap
- Deterministic source generation
- CLI validation and generation

## Sprint 4 — Testing & Security

Sprint 4 hardens the generated-contract workflow with repeatable tests and conservative static security checks.

### Scope

- Security scanner for dangerous Solidity patterns
- Blocking finding classification
- Generated-source safety checks
- Security scanning CLI
- Unit tests for clean and malicious source samples
- CI integration for generation plus security scan
- Audit-readiness documentation and limitations

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

# Security scan
python -m cli.security_cli build/contracts/ExampleCoin.sol

# Full test suite
pytest -q
```

### Security policy

The scanner is intentionally conservative and lexical. It flags `tx.origin`, `delegatecall`, `selfdestruct`, and timestamp-dependent logic, and requires explicit supply-cap and initial-mint markers. A clean scan is not a formal audit, compiler proof, economic review, or deployment approval. Before deployment, pin dependencies, compile with a supported toolchain, run static analysis and fuzz/property tests, review privileged roles, and obtain an independent security assessment.

## Project status

**Sprint 4: Testing & Security — complete**

Next: **Sprint 5 — Wallet Infrastructure**.

## Design principle

Economic parameters are configuration, not hard-coded implementation assumptions. The same specification should feed contract generation, testing, deployment, and analytics.

## Disclaimer

This repository provides software and economic modeling infrastructure. It is not financial, investment, legal, tax, or regulatory advice. Token launches must be reviewed for applicable laws and regulations before deployment or distribution.
