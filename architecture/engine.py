from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from architecture.models import Architecture, ConsensusConfig, NetworkConfig


def load_config(path: str | Path) -> Architecture:
    with Path(path).open("r", encoding="utf-8") as handle:
        data: dict[str, Any] = yaml.safe_load(handle) or {}
    network = data.get("network", {})
    consensus = data.get("consensus", {})
    return Architecture(
        name=str(data.get("name", "")),
        network=NetworkConfig(
            network_id=str(network.get("network_id", "")),
            environment=str(network.get("environment", "testnet")),
            native_symbol=str(network.get("native_symbol", "COIN")),
            chain_type=str(network.get("chain_type", "evm")),
        ),
        consensus=ConsensusConfig(
            mechanism=str(consensus.get("mechanism", "proof_of_stake")),
            block_time_seconds=int(consensus.get("block_time_seconds", 5)),
            finality_blocks=int(consensus.get("finality_blocks", 2)),
            validator_minimum=int(consensus.get("validator_minimum", 4)),
        ),
        execution=dict(data.get("execution", {})),
        rpc=dict(data.get("rpc", {})),
        storage=dict(data.get("storage", {})),
    )


def summarize(path: str | Path) -> dict[str, Any]:
    model = load_config(path)
    return {
        "name": model.name,
        "network_id": model.network.network_id,
        "chain_type": model.network.chain_type,
        "consensus": model.consensus.mechanism,
        "validation_errors": model.validate(),
    }
