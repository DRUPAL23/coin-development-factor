# Coin Development Factory

A reusable framework for designing, validating, and eventually deploying crypto token and native-coin projects.

## Sprint 1 — Tokenomics Engine

- Supply configuration and validation
- Allocation percentages and token quantities
- Vesting schedules
- Emission and burn configuration
- Machine-readable YAML configuration
- Python domain models and CLI foundation

## Sprint 2 — Blockchain Architecture

- Network identity and environment metadata
- Chain type selection: EVM, Solana, Cosmos, Substrate, or sovereign
- Consensus mechanism and safety parameters
- Execution/runtime configuration
- RPC exposure controls
- Storage and pruning policy
- Architecture validation and CI enforcement

## Sprint 3 — Smart Contract Engine

- Deterministic OpenZeppelin-based ERC-20 generation
- Burnable, permit, and capped minting options
- Supply precision and Solidity identifier validation
- Contract CLI and JSON Schema

## Sprint 4 — Testing & Security

- Conservative Solidity static checks
- Blocking finding classification
- Security scan CLI
- Generated-source CI smoke validation
- Audit-readiness documentation and limitations

## Sprint 5 — Wallet Infrastructure

Sprint 5 defines a non-custodial wallet policy layer for EVM deployments. It deliberately does not generate or store private keys, seed phrases, or keystores.

### Scope

- Wallet policy model for browser, mobile, hardware, and external custody workflows
- EVM chain validation
- BIP-44-style derivation-path validation
- 20-byte EVM address validation
- Hardware-signing enforcement
- Private-key export prohibition for hardware policies
- Wallet policy YAML loader and CLI
- Wallet policy JSON Schema
- Unit tests and CI validation

### Commands

```bash
python -m cli.wallet_cli config/examples/example-wallet.yaml
python -m cli.wallet_cli config/examples/example-wallet.yaml --json
pytest -q
```

### Operational security policy

Private keys and seed phrases must never be committed to the repository, passed through CI logs, or handled by this configuration layer. Use hardware-wallet signing or an audited external custody provider for production operations. Address ownership, chain ID, transaction simulation, nonce management, and human approval remain deployment-time controls.

## Project status

**Sprint 5: Wallet Infrastructure — complete**

Next: **Sprint 6 — Backend/API**.

## Design principle

Economic parameters are configuration, not hard-coded implementation assumptions. The same specification should feed contract generation, testing, deployment, and analytics.

## Disclaimer

This repository provides software and economic modeling infrastructure. It is not financial, investment, legal, tax, or regulatory advice. Token launches must be reviewed for applicable laws and regulations before deployment or distribution.
