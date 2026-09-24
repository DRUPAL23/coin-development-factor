# Coin Development Factory

A reusable framework for designing, validating, and eventually deploying crypto token and native-coin projects.

## Completed sprints

- **Sprint 1 — Tokenomics Engine**
- **Sprint 2 — Blockchain Architecture**
- **Sprint 3 — Smart Contract Engine**
- **Sprint 4 — Testing & Security**
- **Sprint 5 — Wallet Infrastructure**
- **Sprint 6 — Backend/API**
- **Sprint 7 — Explorer & Indexer**
- **Sprint 8 — Staking**
- **Sprint 9 — Governance**
- **Sprint 10 — DEX/Liquidity**
- **Sprint 11 — Testnet/Deployment Readiness**
- **Sprint 12 — Audit & Mainnet Launch Controls**
- **Sprint 13 — Wallet/Chain Integration & Production Observability**
- **Sprint 14 — Release Automation & Disaster-Recovery Exercises**

## Sprint 14 — Release Automation & Disaster-Recovery Exercises

Sprint 14 adds fail-closed release readiness controls for signed artifacts, reproducible builds, changelog and rollback evidence, two-person approval, backup verification, restore testing, RPO/RTO targets, and an owned recovery runbook. The package provides typed models, YAML loading, a JSON Schema, CLI output, tests, and CI gates.

### Commands

```bash
pip install -r requirements.txt
pytest -q
python -m cli.release_cli config/examples/example-release.yaml --json
```

The release layer validates declared evidence and readiness controls; it does not perform signing, backup, restore, or deployment actions itself. Those operations must be implemented by the external release and operations systems and then represented by verified evidence.

## Project status

**Sprint 14: Release Automation & Disaster-Recovery Exercises — complete**

Next: **Sprint 15 — Mainnet Operations, SLOs & Incident Response**.

## Design principle

Economic parameters are configuration, not hard-coded implementation assumptions. The same specification should feed contract generation, testing, deployment, and analytics.

## Disclaimer

This repository provides software and economic modeling infrastructure. It is not financial, investment, legal, tax, or regulatory advice. Token launches must be reviewed for applicable laws and regulations before deployment or distribution.
