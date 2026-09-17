from __future__ import annotations

from explorer.models import Block, Transaction
from explorer.store import ExplorerStore


class Indexer:
    def __init__(self, store: ExplorerStore | None = None) -> None:
        self.store = store or ExplorerStore()

    def add_block(self, block: Block, transactions: list[Transaction] | None = None) -> None:
        txs = transactions or []
        if block.transaction_count != len(txs):
            raise ValueError("block.transaction_count must equal supplied transaction count")
        self.store.upsert_block(block)
        for tx in txs:
            if tx.block_number != block.number:
                raise ValueError("transaction block_number does not match containing block")
            self.store.upsert_transaction(tx)

    def status(self) -> dict:
        latest = self.store.latest_block()
        return {"indexed": latest is not None, "latest_block": latest}
