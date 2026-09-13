from pathlib import Path

from architecture.engine import load_config
from architecture.models import Architecture, ConsensusConfig, NetworkConfig


ROOT = Path(__file__).resolve().parents[1]


def test_example_architecture_is_valid():
    model = load_config(ROOT / "config/examples/example-architecture.yaml")
    assert model.validate() == []
    assert model.network.chain_type == "evm"
    assert model.consensus.validator_minimum == 4


def test_invalid_chain_type_is_rejected():
    model = Architecture(
        name="Bad",
        network=NetworkConfig(network_id="bad-1", chain_type="unknown"),
        consensus=ConsensusConfig(),
    )
    assert any("chain_type" in error for error in model.validate())


def test_invalid_consensus_parameters_are_rejected():
    model = Architecture(
        name="Bad",
        network=NetworkConfig(network_id="bad-1"),
        consensus=ConsensusConfig(block_time_seconds=0, finality_blocks=0, validator_minimum=0),
    )
    errors = model.validate()
    assert len(errors) == 3
