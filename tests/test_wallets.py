from pathlib import Path

from wallets.engine import load_spec
from wallets.models import WalletSpec


ROOT = Path(__file__).parents[1]


def test_example_wallet_policy_is_valid() -> None:
    spec = load_spec(ROOT / "config/examples/example-wallet.yaml")
    assert spec.validate() == []
    assert spec.wallet_type == "hardware"


def test_invalid_derivation_path_is_rejected() -> None:
    spec = WalletSpec(name="Bad", derivation_path="not-a-path")
    assert any("derivation_path" in error for error in spec.validate())


def test_hardware_wallet_cannot_export_private_keys() -> None:
    spec = WalletSpec(name="Bad", allow_private_key_export=True)
    assert any("private-key export" in error for error in spec.validate())


def test_invalid_evm_address_is_rejected() -> None:
    spec = WalletSpec(name="Bad", address="0x1234")
    assert any("20-byte EVM" in error for error in spec.validate())
