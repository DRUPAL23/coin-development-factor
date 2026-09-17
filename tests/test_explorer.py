from explorer.indexer import Indexer
from explorer.models import Block, Transaction
from explorer.store import ExplorerStore


ZERO = "0x" + "0" * 64
ADDR1 = "0x" + "1" * 40
ADDR2 = "0x" + "2" * 40


def test_block_and_transaction_round_trip() -> None:
    indexer = Indexer(ExplorerStore())
    block = Block(1, ZERO, ZERO, 100, 1)
    tx = Transaction("0x" + "3" * 64, 1, ADDR1, ADDR2, "42")
    indexer.add_block(block, [tx])
    assert indexer.store.get_block(1)["transaction_count"] == 1
    assert indexer.store.get_transaction(tx.tx_hash)["value"] == "42"
    assert indexer.store.list_transactions(address=ADDR1)[0]["tx_hash"] == tx.tx_hash


def test_indexer_rejects_count_mismatch() -> None:
    indexer = Indexer()
    try:
        indexer.add_block(Block(1, ZERO, ZERO, 100, 1), [])
    except ValueError as exc:
        assert "transaction count" in str(exc)
    else:
        raise AssertionError("expected count mismatch")


def test_store_rejects_transaction_for_unknown_block() -> None:
    store = ExplorerStore()
    try:
        store.upsert_transaction(Transaction("0x" + "3" * 64, 9, ADDR1, ADDR2))
    except ValueError as exc:
        assert "unknown block" in str(exc)
    else:
        raise AssertionError("expected unknown block failure")
