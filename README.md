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

## Sprint 12 — Audit & Mainnet Launch Controls

Sprint 12 adds a release-gating layer for security review, key-ceremony rehearsal, rollback testing, incident-response approval, legal review declaration, change freeze, sign-off roles, and audit finding closure. It produces a deterministic launch report and fails closed for missing required controls or unresolved critical/high findings.

### Commands

```bash
pip install -r requirements.txt
pytest -q
python -m cli.audit_cli config/examples/example-audit.yaml --json
```

The audit layer records declarations and evidence references; it does not replace an independent security audit, legal opinion, operational approval, or real-world incident drill.

## Project status

**Sprint 12: Audit & Mainnet Launch Controls — complete**

Next: **Sprint 13 — Wallet/Chain Integration & Production Observability**.

## Design principle

Economic parameters are configuration, not hard-coded implementation assumptions. The same specification should feed contract generation, testing, deployment, and analytics.

## Disclaimer

This repository provides software and economic modeling infrastructure. It is not financial, investment, legal, tax, or regulatory advice. Token launches must be reviewed for applicable laws and regulations before deployment or distribution.
