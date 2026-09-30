from electrumx.lib.coins import Coin
from electrumx.coin.acecoin import AceCoinMainnet, AceCoinTestnet


def test_coin_classes_are_discoverable():
    assert Coin.lookup_coin_class("AceCoin", "mainnet") is AceCoinMainnet
    assert Coin.lookup_coin_class("AceCoin", "testnet") is AceCoinTestnet


def test_network_ports():
    assert AceCoinMainnet.RPC_PORT == 9332
    assert AceCoinTestnet.RPC_PORT == 19332


def test_utxo_parameters_are_explicit():
    assert AceCoinMainnet.BASIC_HEADER_SIZE == 80
    assert AceCoinMainnet.VALUE_PER_COIN == 100_000_000
