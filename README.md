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

## Sprint 9 — Governance

Sprint 9 adds a policy-driven governance layer for proposal eligibility, quorum, approval thresholds, cancellation, and timelock planning.

### Scope

- governance policy model and validation
- token, quadratic, and one-wallet-one-vote policy identifiers
- proposal threshold validation
- quorum and approval-threshold validation
- voting-period and timelock controls
- proposal model with typed proposal categories
- proposer, voting-power, and vote-bound validation
- deterministic outcomes: passed, rejected, quorum_not_met, cancelled, invalid
- governance CLI validation and proposal evaluation
- governance JSON Schema
- API endpoints for policy and proposal evaluation
- unit tests and CI smoke coverage

### Commands

```bash
pip install -r requirements.txt
pytest -q
python -m cli.governance_cli validate config/examples/example-governance.yaml
python -m cli.governance_cli evaluate config/examples/example-governance.yaml p-001 \
  "Increase treasury budget" treasury_spend alice 2000 10000 3000 1000
uvicorn api.app:app --reload
```

### Governance API

```text
GET /v1/governance
GET /v1/governance/evaluate?proposal_id=p-001&title=Increase%20treasury%20budget&proposal_type=treasury_spend&proposer=alice&voting_power=2000&total_voting_power=10000&yes_votes=3000&no_votes=1000
```

Governance evaluation is a deterministic planning and validation utility. It does not execute on-chain proposals, custody voting assets, authenticate wallets, prevent sybil attacks, or replace protocol-level governance contracts, snapshot logic, or security review. Timelock and guardian controls must be reconciled with the final runtime before deployment.

## Project status

**Sprint 9: Governance — complete**

Next: **Sprint 10 — DEX/Liquidity**.

## Design principle

Economic parameters are configuration, not hard-coded implementation assumptions. The same specification should feed contract generation, testing, deployment, and analytics.

## Disclaimer

This repository provides software and economic modeling infrastructure. It is not financial, investment, legal, tax, or regulatory advice. Token launches must be reviewed for applicable laws and regulations before deployment or distribution.
