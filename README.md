# Coin Development Factory

A reusable framework for designing, validating, and eventually deploying crypto token and native-coin projects.

## Completed sprints

- **Sprint 1 — Tokenomics Engine:** supply, allocations, vesting, and mechanics.
- **Sprint 2 — Blockchain Architecture:** network, consensus, execution, RPC, and storage policy.
- **Sprint 3 — Smart Contract Engine:** deterministic OpenZeppelin ERC-20 generation.
- **Sprint 4 — Testing & Security:** conservative Solidity static checks and CI enforcement.
- **Sprint 5 — Wallet Infrastructure:** non-custodial wallet policy validation.
- **Sprint 6 — Backend/API:** versioned FastAPI service for validated project specifications.

## Sprint 7 — Explorer & Indexer

Sprint 7 adds a deterministic explorer read model and a SQLite-backed index store for blocks and transactions.

### Scope

- typed block and transaction read models
- structural validation for hashes, addresses, timestamps, and status
- SQLite persistence with indexes for block number and transaction address lookups
- deterministic indexer service enforcing block/transaction relationships
- explorer CLI smoke command
- API endpoints for indexer status, block lookup, and transaction listing
- explorer JSON Schema
- unit tests for round trips and invalid relationship handling
- CI validation and API smoke tests

### Commands

```bash
pip install -r requirements.txt
pytest -q
python -m cli.explorer_cli --json
uvicorn api.app:app --reload
```

### Explorer API

```text
GET /v1/explorer/status
GET /v1/explorer/blocks/{number}
GET /v1/explorer/transactions?address=0x...&limit=50
```

The current indexer is intentionally a deterministic local read-model component. It does not connect to a live chain RPC, handle reorg resolution, decode arbitrary event ABIs, or expose authenticated production ingestion. Those concerns belong in the next infrastructure stages and must be designed before public deployment.

## Project status

**Sprint 7: Explorer & Indexer — complete**

Next: **Sprint 8 — Staking**.

## Design principle

Economic parameters are configuration, not hard-coded implementation assumptions. The same specification should feed contract generation, testing, deployment, and analytics.

## Disclaimer

This repository provides software and economic modeling infrastructure. It is not financial, investment, legal, tax, or regulatory advice. Token launches must be reviewed for applicable laws and regulations before deployment or distribution.
