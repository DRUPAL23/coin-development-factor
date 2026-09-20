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
- **Sprint 8 — Staking:** validated staking policy and deterministic reward calculations.
- **Sprint 9 — Governance:** policy-driven proposal eligibility, quorum, approval thresholds, cancellation, and timelock planning.

## Sprint 10 — DEX/Liquidity

Sprint 10 adds a deterministic liquidity-pool planning layer for pair configuration, fee tiers, price bounds, slippage policy, spot-price calculation, and constant-product quote estimation.

### Scope

- liquidity-pool model and validation
- base/quote asset pair checks
- fee-tier and slippage-bounds policy
- initial liquidity validation
- price-range controls
- deterministic spot-price and quote calculation
- DEX CLI validation and quote commands
- DEX JSON Schema
- FastAPI endpoints for pool summary and quote estimation
- unit tests and CI smoke coverage

### Commands

```bash
pip install -r requirements.txt
pytest -q
python -m cli.dex_cli validate config/examples/example-dex.yaml
python -m cli.dex_cli quote config/examples/example-dex.yaml 1000
uvicorn api.app:app --reload
```

### DEX API

```text
GET /v1/dex
GET /v1/dex/quote?base_input=1000
```

DEX calculations are planning utilities, not a live exchange. They do not execute swaps, custody funds, route across venues, account for oracle manipulation, MEV, market impact beyond the constant-product estimate, or replace audited AMM contracts and integration testing. Fee tiers and price bounds must be reconciled with the selected protocol before deployment.

## Project status

**Sprint 10: DEX/Liquidity — complete**

Next: **Sprint 11 — Testnet/Deployment Readiness**.

## Design principle

Economic parameters are configuration, not hard-coded implementation assumptions. The same specification should feed contract generation, testing, deployment, and analytics.

## Disclaimer

This repository provides software and economic modeling infrastructure. It is not financial, investment, legal, tax, or regulatory advice. Token launches must be reviewed for applicable laws and regulations before deployment or distribution.
