from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
import re

SUPPORTED_FEE_TIERS = {"0.01", "0.05", "0.30", "1.00"}

@dataclass(frozen=True)
class LiquidityPool:
    pool_id: str
    base_asset: str
    quote_asset: str
    fee_tier: Decimal = Decimal("0.003")
    initial_base: Decimal = Decimal("0")
    initial_quote: Decimal = Decimal("0")
    min_price: Decimal = Decimal("0")
    max_price: Decimal = Decimal("0")
    slippage_bps: int = 100
    enabled: bool = True

    def validate(self) -> list[str]:
        e=[]
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{2,63}", self.pool_id): e.append("dex.pool_id must be 3-64 safe characters")
        if not self.base_asset.strip() or not self.quote_asset.strip() or self.base_asset == self.quote_asset: e.append("dex assets must be non-empty and distinct")
        if not Decimal("0") < self.fee_tier < Decimal("0.1"): e.append("dex.fee_tier must be greater than 0 and less than 0.1")
        if self.initial_base <= 0 or self.initial_quote <= 0: e.append("dex initial liquidity must be greater than zero")
        if self.min_price < 0 or self.max_price < 0: e.append("dex price bounds cannot be negative")
        if self.max_price and self.min_price and self.min_price >= self.max_price: e.append("dex.min_price must be less than dex.max_price")
        if not 1 <= self.slippage_bps <= 5000: e.append("dex.slippage_bps must be between 1 and 5000")
        return e

    def spot_price(self) -> Decimal:
        return self.initial_quote / self.initial_base

    def quote_output(self, base_input: Decimal) -> Decimal:
        if base_input <= 0: raise ValueError("base_input must be greater than zero")
        fee_adjusted = base_input * (Decimal("1") - self.fee_tier)
        return (self.initial_quote * fee_adjusted) / (self.initial_base + fee_adjusted)
