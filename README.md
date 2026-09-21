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
- **Sprint 10 — DEX/Liquidity:** pool configuration, fee tiers, price bounds, slippage policy, and constant-product quotes.
- **Sprint 11 — Testnet/Deployment Readiness:** environment-aware deployment policy, RPC/explorer gates, validator minimums, secret declarations, operational readiness checks, API, CLI, schema, tests, and CI validation.

## Sprint 11 — Testnet/Deployment Readiness

Sprint 11 adds a deployment-readiness layer that validates whether a configured testnet, staging, local, or mainnet rollout has the minimum technical and operational controls declared before deployment.

### Scope

- environment and provider policy
- chain ID, RPC, explorer, and node image configuration
- replica and validator minimums
- mainnet HTTPS enforcement
- required-secret declarations without handling secret values
- operational readiness checks for genesis, monitoring, backups, and related controls
- deployment CLI and JSON Schema
- FastAPI deployment summary and aggregate validation endpoint
- unit tests and CI smoke coverage

### Commands

```bash
pip install -r requirements.txt
pytest -q
python -m cli.deployment_cli config/examples/example-deployment.yaml --json
uvicorn api.app:app --reload
```

### Deployment API

```text
GET /v1/deployment
GET /v1/validate
```

The deployment layer is a readiness gate, not an infrastructure provisioner. It does not create cloud resources, generate validator keys, store secrets, publish genesis files, deploy contracts, or prove that an RPC endpoint is reachable. Production rollout still requires environment-specific IaC, secret management, monitoring, backups, incident response, security review, and an operator-run deployment checklist.

## Project status

**Sprint 11: Testnet/Deployment Readiness — complete**

Next: **Sprint 12 — Audit & Mainnet Launch Controls**.

## Design principle

Economic parameters are configuration, not hard-coded implementation assumptions. The same specification should feed contract generation, testing, deployment, and analytics.

## Disclaimer

This repository provides software and economic modeling infrastructure. It is not financial, investment, legal, tax, or regulatory advice. Token launches must be reviewed for applicable laws and regulations before deployment or distribution.
