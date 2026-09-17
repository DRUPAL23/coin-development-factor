from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from architecture.engine import load_config as load_architecture
from contracts.engine import generate_erc20, load_spec as load_contract
from explorer.indexer import Indexer
from explorer.models import Block
from tokenomics.engine import calculate as calculate_tokenomics
from wallets.engine import load_config as load_wallets

ROOT = Path(__file__).resolve().parents[1]
app = FastAPI(title="Coin Development Factory API", version="0.7.0")
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


@app.get("/v1/validate", response_model=ValidationResponse)
def validate_all() -> ValidationResponse:
    errors: list[str] = []
    for model in [
        load_architecture(ROOT / "config/examples/example-architecture.yaml"),
        load_wallets(ROOT / "config/examples/example-wallet.yaml"),
        load_contract(ROOT / "config/examples/example-contract.yaml"),
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
