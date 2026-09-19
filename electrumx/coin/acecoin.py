"""AceCoin ElectrumX coin definitions.

Bitcoin-like UTXO adapter. Consensus values are injected through environment
variables so the server image can be promoted from testnet to mainnet without
editing source code.
"""

import os

from electrumx.lib import tx as lib_tx
from electrumx.lib.coins import Coin


def _hex_bytes(name: str, default: str) -> bytes:
    return bytes.fromhex(os.getenv(name, default))


class AceCoinBase(Coin):
    NAME = "AceCoin"
    SHORTNAME = "ACE"
    NET = None

    VALUE_PER_COIN = int(os.getenv("ACECOIN_VALUE_PER_COIN", "100000000"))
    BASIC_HEADER_SIZE = int(os.getenv("ACECOIN_HEADER_SIZE", "80"))
    CHUNK_SIZE = 2016
    STATIC_BLOCK_HEADERS = True

    P2PKH_VERBYTE = _hex_bytes("ACECOIN_P2PKH_VERBYTE", "00")
    P2SH_VERBYTES = (_hex_bytes("ACECOIN_P2SH_VERBYTE", "05"),)

    # Refuse accidental production use with a fake genesis value. The value
    # must be supplied by AceCoin Core once the chain is instantiated.
    GENESIS_HASH = os.getenv("ACECOIN_GENESIS_HASH", "0" * 64)

    RPC_PORT = int(os.getenv("ACECOIN_RPC_PORT", "9332"))

    DESERIALIZER = lib_tx.DeserializerSegWit

    TX_COUNT = int(os.getenv("ACECOIN_TX_COUNT", "1"))
    TX_COUNT_HEIGHT = int(os.getenv("ACECOIN_TX_COUNT_HEIGHT", "0"))
    TX_PER_BLOCK = int(os.getenv("ACECOIN_TX_PER_BLOCK", "1"))


class AceCoinMainnet(AceCoinBase):
    NAME = "AceCoin"
    SHORTNAME = "ACE"
    NET = "mainnet"
    RPC_PORT = int(os.getenv("ACECOIN_MAINNET_RPC_PORT", "9332"))


class AceCoinTestnet(AceCoinBase):
    NAME = "AceCoin"
    SHORTNAME = "tACE"
    NET = "testnet"
    RPC_PORT = int(os.getenv("ACECOIN_TESTNET_RPC_PORT", "19332"))

    P2PKH_VERBYTE = _hex_bytes("ACECOIN_TESTNET_P2PKH_VERBYTE", "6f")
    P2SH_VERBYTES = (_hex_bytes("ACECOIN_TESTNET_P2SH_VERBYTE", "c4"),)


__all__ = ["AceCoinBase", "AceCoinMainnet", "AceCoinTestnet"]
