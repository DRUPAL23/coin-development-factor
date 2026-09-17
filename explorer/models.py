from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class Block:
    number: int
    block_hash: str
    parent_hash: str
    timestamp: int
    transaction_count: int = 0

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.number < 0:
            errors.append("block.number cannot be negative")
        if len(self.block_hash) != 66 or not self.block_hash.startswith("0x"):
            errors.append("block.block_hash must be a 32-byte hex hash")
        if len(self.parent_hash) != 66 or not self.parent_hash.startswith("0x"):
            errors.append("block.parent_hash must be a 32-byte hex hash")
        if self.timestamp <= 0:
            errors.append("block.timestamp must be positive")
        if self.transaction_count < 0:
            errors.append("block.transaction_count cannot be negative")
        return errors

    def as_dict(self) -> dict[str, int | str]:
        return {
            "number": self.number,
            "block_hash": self.block_hash,
            "parent_hash": self.parent_hash,
            "timestamp": self.timestamp,
            "transaction_count": self.transaction_count,
            "timestamp_iso": datetime.fromtimestamp(self.timestamp, tz=timezone.utc).isoformat(),
        }


@dataclass(frozen=True)
class Transaction:
    tx_hash: str
    block_number: int
    from_address: str
    to_address: str | None
    value: str = "0"
    status: str = "confirmed"

    def validate(self) -> list[str]:
        errors: list[str] = []
        if len(self.tx_hash) != 66 or not self.tx_hash.startswith("0x"):
            errors.append("transaction.tx_hash must be a 32-byte hex hash")
        if self.block_number < 0:
            errors.append("transaction.block_number cannot be negative")
        for field, value in (("from_address", self.from_address), ("to_address", self.to_address)):
            if value is not None and (len(value) != 42 or not value.startswith("0x")):
                errors.append(f"transaction.{field} must be a 20-byte EVM hex address")
        if self.status not in {"confirmed", "failed"}:
            errors.append("transaction.status must be confirmed or failed")
        return errors

    def as_dict(self) -> dict[str, str | int | None]:
        return self.__dict__.copy()
