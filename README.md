# Coin Development Factory

A reusable framework for designing, validating, and eventually deploying crypto token and native-coin projects.

## Completed sprints

- **Sprint 1 — Tokenomics Engine:** supply, allocations, vesting, and mechanics.
- **Sprint 2 — Blockchain Architecture:** network, consensus, execution, RPC, and storage policy.
- **Sprint 3 — Smart Contract Engine:** deterministic OpenZeppelin ERC-20 generation.
- **Sprint 4 — Testing & Security:** conservative Solidity static checks and CI enforcement.
- **Sprint 5 — Wallet Infrastructure:** non-custodial wallet policy validation.

## Sprint 6 — Backend/API

Sprint 6 exposes the validated project specifications through a small, testable FastAPI service.

### Scope

- FastAPI application with versioned `/v1` endpoints
- `/health` liveness endpoint
- tokenomics, architecture, wallet, and example-contract read endpoints
- aggregate `/v1/validate` endpoint for cross-layer configuration validation
- Pydantic response contract for validation results
- API tests using FastAPI's TestClient
- CI dependency installation, test execution, and API smoke test

### Run locally

```bash
pip install -r requirements.txt
uvicorn api.app:app --reload
```

API documentation is available from FastAPI at `/docs` and `/redoc` when the service is running.

### Endpoints

```text
GET /health
GET /v1/tokenomics
GET /v1/architecture
GET /v1/wallets
GET /v1/contracts/example
GET /v1/validate
```

The current API reads repository example configurations intentionally. Authentication, persistence, rate limiting, chain RPC integration, transaction submission, and secrets management remain outside this sprint and must be designed before production exposure.

## Project status

**Sprint 6: Backend/API — complete**

Next: **Sprint 7 — Explorer & Indexer**.

## Design principle

Economic parameters are configuration, not hard-coded implementation assumptions. The same specification should feed contract generation, testing, deployment, and analytics.

## Disclaimer

This repository provides software and economic modeling infrastructure. It is not financial, investment, legal, tax, or regulatory advice. Token launches must be reviewed for applicable laws and regulations before deployment or distribution.
