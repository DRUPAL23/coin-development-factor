from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


SUPPORTED_NETWORKS = {"evm", "solana", "cosmos", "substrate", "sovereign"}
SUPPORTED_CONSENSUS = {"proof_of_stake", "proof_of_authority", "tendermint_bft", "nominated_proof_of_stake", "custom"}


@dataclass(frozen=True)
class NetworkConfig:
    network_id: str
    environment: str = "testnet"
    native_symbol: str = "COIN"
    chain_type: str = "evm"


@dataclass(frozen=True)
class ConsensusConfig:
    mechanism: str = "proof_of_stake"
    block_time_seconds: int = 5
    finality_blocks: int = 2
    validator_minimum: int = 4


@dataclass(frozen=True)
class Architecture:
    name: str
    network: NetworkConfig
    consensus: ConsensusConfig
    execution: dict[str, Any] = field(default_factory=dict)
    rpc: dict[str, Any] = field(default_factory=dict)
    storage: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.name.strip():
            errors.append("architecture.name is required")
        if self.network.chain_type not in SUPPORTED_NETWORKS:
            errors.append(f"network.chain_type must be one of: {', '.join(sorted(SUPPORTED_NETWORKS))}")
        if not self.network.network_id.strip():
            errors.append("network.network_id is required")
        if self.consensus.mechanism not in SUPPORTED_CONSENSUS:
            errors.append(f"consensus.mechanism must be one of: {', '.join(sorted(SUPPORTED_CONSENSUS))}")
        if self.consensus.block_time_seconds <= 0:
            errors.append("consensus.block_time_seconds must be greater than zero")
        if self.consensus.finality_blocks <= 0:
            errors.append("consensus.finality_blocks must be greater than zero")
        if self.consensus.validator_minimum < 1:
            errors.append("consensus.validator_minimum must be at least one")
        return errors
