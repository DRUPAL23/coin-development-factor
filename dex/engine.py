from __future__ import annotations
from decimal import Decimal
import yaml
from .models import LiquidityPool

def load_pool(path: str) -> LiquidityPool:
    with open(path, encoding='utf-8') as f: data=yaml.safe_load(f) or {}
    c=data.get('dex', {})
    return LiquidityPool(pool_id=str(c.get('pool_id','')), base_asset=str(c.get('base_asset','')), quote_asset=str(c.get('quote_asset','')), fee_tier=Decimal(str(c.get('fee_tier','0.003'))), initial_base=Decimal(str(c.get('initial_base','0'))), initial_quote=Decimal(str(c.get('initial_quote','0'))), min_price=Decimal(str(c.get('min_price','0'))), max_price=Decimal(str(c.get('max_price','0'))), slippage_bps=int(c.get('slippage_bps',100)), enabled=bool(c.get('enabled',True)))

def summary(pool: LiquidityPool) -> dict:
    errors=pool.validate()
    return {'valid': not errors, 'validation_errors': errors, 'pool_id': pool.pool_id, 'pair': f'{pool.base_asset}/{pool.quote_asset}', 'fee_tier': str(pool.fee_tier), 'spot_price': str(pool.spot_price()) if not errors else None}
