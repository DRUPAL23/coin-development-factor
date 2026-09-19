from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from architecture.engine import load_config as load_architecture
from contracts.engine import generate_erc20, load_spec as load_contract
from explorer.indexer import Indexer
from explorer.models import Block
from governance.engine import evaluate_proposal, load_policy as load_governance
from governance.models import Proposal
from staking.engine import calculate_reward, load_policy
from tokenomics.engine import calculate as calculate_tokenomics
from wallets.engine import load_spec as load_wallets

ROOT = Path(__file__).resolve().parents[1]
app = FastAPI(title="Coin Development Factory API", version="0.9.0")
EXPLORER = Indexer()
EXPLORER.add_block(Block(0, "0x" + "0" * 64, "0x" + "0" * 64, 1, 0))


class ValidationResponse(BaseModel):
    valid: bool
    errors: list[str] = Field(default_factory=list)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "coin-development-factor"}


@app.get("/v1/tokenomics")
def tokenomics() -> dict[str, Any]:
    return calculate_tokenomics(ROOT / "config/examples/example-coin.yaml")


@app.get("/v1/architecture")
def architecture() -> dict[str, Any]:
    model = load_architecture(ROOT / "config/examples/example-architecture.yaml")
    return {"name": model.name, "network_id": model.network.network_id, "chain_type": model.network.chain_type, "consensus": model.consensus.mechanism, "validation_errors": model.validate()}


@app.get("/v1/wallets")
def wallets() -> dict[str, Any]:
    model = load_wallets(ROOT / "config/examples/example-wallet.yaml")
    return {"wallet_type": model.wallet_type, "chain": model.chain, "validation_errors": model.validate()}


@app.get("/v1/contracts/example")
def example_contract() -> dict[str, Any]:
    spec = load_contract(ROOT / "config/examples/example-contract.yaml")
    return {"contract_name": spec.contract_name, "target": spec.target, "validation_errors": spec.validate(), "source": generate_erc20(spec)}


@app.get("/v1/staking")
def staking() -> dict[str, Any]:
    policy = load_policy(ROOT / "config/examples/example-staking.yaml")
    return {"enabled": policy.enabled, "min_stake": str(policy.min_stake), "unbonding_period_days": policy.unbonding_period_days, "reward_rate_annual": str(policy.reward_rate_annual), "commission_rate": str(policy.commission_rate), "max_validators": policy.max_validators, "validation_errors": policy.validate()}


@app.get("/v1/staking/reward")
def staking_reward(amount: str = Query(...), duration_days: int = Query(..., ge=0)) -> dict[str, str]:
    policy = load_policy(ROOT / "config/examples/example-staking.yaml")
    try:
        return calculate_reward(policy, Decimal(amount), duration_days)
    except (ValueError, ArithmeticError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/v1/governance")
def governance() -> dict[str, Any]:
    policy = load_governance(ROOT / "config/examples/example-governance.yaml")
    return {"enabled": policy.enabled, "voting_model": policy.voting_model, "proposal_threshold": str(policy.proposal_threshold), "quorum": str(policy.quorum), "approval_threshold": str(policy.approval_threshold), "voting_period_days": policy.voting_period_days, "timelock_days": policy.timelock_days, "execution_delay_days": policy.execution_delay_days, "guardian_enabled": policy.guardian_enabled, "validation_errors": policy.validate()}


@app.get("/v1/governance/evaluate")
def governance_evaluate(proposal_id: str, title: str, proposal_type: str, proposer: str, voting_power: str, total_voting_power: str, yes_votes: str, no_votes: str, abstain_votes: str = "0") -> dict[str, str]:
    policy = load_governance(ROOT / "config/examples/example-governance.yaml")
    try:
        proposal = Proposal(proposal_id, title, proposal_type, proposer, Decimal(voting_power), Decimal(total_voting_power), Decimal(yes_votes), Decimal(no_votes), Decimal(abstain_votes))
        return evaluate_proposal(policy, proposal)
    except (ValueError, ArithmeticError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/v1/validate", response_model=ValidationResponse)
def validate_all() -> ValidationResponse:
    errors: list[str] = []
    for model in [
        load_architecture(ROOT / "config/examples/example-architecture.yaml"),
        load_wallets(ROOT / "config/examples/example-wallet.yaml"),
        load_contract(ROOT / "config/examples/example-contract.yaml"),
        load_policy(ROOT / "config/examples/example-staking.yaml"),
        load_governance(ROOT / "config/examples/example-governance.yaml"),
    ]:
        errors.extend(model.validate())
    return ValidationResponse(valid=not errors, errors=errors)


@app.get("/v1/explorer/status")
def explorer_status() -> dict[str, Any]:
    return EXPLORER.status()


@app.get("/v1/explorer/blocks/{number}")
def explorer_block(number: int) -> dict[str, Any]:
    block = EXPLORER.store.get_block(number)
    if block is None:
        raise HTTPException(status_code=404, detail="block not found")
    return block


@app.get("/v1/explorer/transactions")
def explorer_transactions(address: str | None = None, limit: int = Query(50, ge=1, le=100)) -> dict[str, Any]:
    return {"items": EXPLORER.store.list_transactions(address=address, limit=limit), "limit": limit}
