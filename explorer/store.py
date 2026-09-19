from __future__ import annotations

import sqlite3
from pathlib import Path
from threading import RLock

from explorer.models import Block, Transaction


class ExplorerStore:
    """Small SQLite read store for indexed explorer data."""

    def __init__(self, path: str | Path = ":memory:") -> None:
        self.connection = sqlite3.connect(str(path), check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self._lock = RLock()
        self._init_schema()

    def _init_schema(self) -> None:
        with self._lock:
            self.connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS blocks (
                    number INTEGER PRIMARY KEY,
                    block_hash TEXT NOT NULL UNIQUE,
                    parent_hash TEXT NOT NULL,
                    timestamp INTEGER NOT NULL,
                    transaction_count INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS transactions (
                    tx_hash TEXT PRIMARY KEY,
                    block_number INTEGER NOT NULL,
                    from_address TEXT NOT NULL,
                    to_address TEXT,
                    value TEXT NOT NULL,
                    status TEXT NOT NULL,
                    FOREIGN KEY(block_number) REFERENCES blocks(number)
                );
                CREATE INDEX IF NOT EXISTS idx_transactions_block_number ON transactions(block_number);
                CREATE INDEX IF NOT EXISTS idx_transactions_from_address ON transactions(from_address);
                CREATE INDEX IF NOT EXISTS idx_transactions_to_address ON transactions(to_address);
                """
            )
            self.connection.commit()

    def upsert_block(self, block: Block) -> None:
        errors = block.validate()
        if errors:
            raise ValueError("invalid block: " + "; ".join(errors))
        with self._lock:
            self.connection.execute(
                "INSERT OR REPLACE INTO blocks(number, block_hash, parent_hash, timestamp, transaction_count) VALUES (?, ?, ?, ?, ?)",
                (block.number, block.block_hash, block.parent_hash, block.timestamp, block.transaction_count),
            )
            self.connection.commit()

    def upsert_transaction(self, tx: Transaction) -> None:
        errors = tx.validate()
        if errors:
            raise ValueError("invalid transaction: " + "; ".join(errors))
        with self._lock:
            if self.get_block(tx.block_number) is None:
                raise ValueError("transaction references an unknown block")
            self.connection.execute(
                "INSERT OR REPLACE INTO transactions(tx_hash, block_number, from_address, to_address, value, status) VALUES (?, ?, ?, ?, ?, ?)",
                (tx.tx_hash, tx.block_number, tx.from_address, tx.to_address, tx.value, tx.status),
            )
            self.connection.commit()

    def get_block(self, number: int) -> dict | None:
        with self._lock:
            row = self.connection.execute("SELECT * FROM blocks WHERE number = ?", (number,)).fetchone()
            return dict(row) if row else None

    def get_transaction(self, tx_hash: str) -> dict | None:
        with self._lock:
            row = self.connection.execute("SELECT * FROM transactions WHERE tx_hash = ?", (tx_hash,)).fetchone()
            return dict(row) if row else None

    def latest_block(self) -> dict | None:
        with self._lock:
            row = self.connection.execute("SELECT * FROM blocks ORDER BY number DESC LIMIT 1").fetchone()
            return dict(row) if row else None

    def list_transactions(self, address: str | None = None, limit: int = 50) -> list[dict]:
        if not 1 <= limit <= 100:
            raise ValueError("limit must be between 1 and 100")
        with self._lock:
            if address:
                rows = self.connection.execute(
                    "SELECT * FROM transactions WHERE from_address = ? OR to_address = ? ORDER BY block_number DESC LIMIT ?",
                    (address, address, limit),
                ).fetchall()
            else:
                rows = self.connection.execute("SELECT * FROM transactions ORDER BY block_number DESC LIMIT ?", (limit,)).fetchall()
            return [dict(row) for row in rows]
