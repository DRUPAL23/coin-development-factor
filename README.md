# Coin Development Factory

A reusable framework for designing, validating, and eventually deploying crypto token and native-coin projects.

## Completed sprints

- **Sprint 1 — Tokenomics Engine:** supply, allocations, vesting, and mechanics.
- **Sprint 2 — Blockchain Architecture:** network, consensus, execution, RPC, and storage policy.
- **Sprint 3 — Smart Contract Engine:** deterministic OpenZeppelin ERC-20 generation.
- **Sprint 4 — Testing & Security:** conservative Solidity static checks and CI enforcement.
- **Sprint 5 — Wallet Infrastructure:** non-custodial wallet policy validation.
- **Sprint 6 — Backend/API:** versioned FastAPI service for validated project specifications.
- **Sprint 7 — Explorer & Indexer:** deterministic block/transaction read model with SQLite persistence.

## Sprint 8 — Staking

Sprint 8 adds a validated staking policy layer and deterministic reward calculations for delegation planning and API consumption.

### Scope

- staking policy model and validation
- minimum stake and unbonding-period rules
- annual reward-rate and validator commission controls
- maximum-validator policy
- native/custom reward-asset selection
- delegation input validation
- gross reward, commission, and net reward calculation
- staking CLI validation and reward calculator
- staking JSON Schema
- API endpoints for policy and reward estimation
- unit tests and CI smoke coverage

### Commands

```bash
pip install -r requirements.txt
pytest -q
python -m cli.staking_cli validate config/examples/example-staking.yaml
python -m cli.staking_cli reward config/examples/example-staking.yaml 1000 365
uvicorn api.app:app --reload
```

### Staking API

```text
GET /v1/staking
GET /v1/staking/reward?amount=1000&duration_days=365
```

Reward calculations are deterministic planning utilities. They do not perform on-chain staking, custody assets, select validators, guarantee yield, or replace protocol-level accounting and security review. Commission and reward semantics must be reconciled with the final chain runtime or smart contract implementation before deployment.

## Project status

**Sprint 8: Staking — complete**

Next: **Sprint 9 — Governance**.

## Design principle

Economic parameters are configuration, not hard-coded implementation assumptions. The same specification should feed contract generation, testing, deployment, and analytics.

## Disclaimer

This repository provides software and economic modeling infrastructure. It is not financial, investment, legal, tax, or regulatory advice. Token launches must be reviewed for applicable laws and regulations before deployment or distribution.
