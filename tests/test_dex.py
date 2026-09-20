from decimal import Decimal
from dex.engine import load_pool

def test_pool_loads_and_quotes():
    pool=load_pool('config/examples/example-dex.yaml')
    assert pool.validate()==[]
    assert pool.spot_price()==Decimal('0.1')
    assert pool.quote_output(Decimal('1000')) > 0

def test_invalid_pool_rejected():
    from dex.models import LiquidityPool
    pool=LiquidityPool('bad','EXC','EXC',initial_base=Decimal('1'),initial_quote=Decimal('1'))
    assert pool.validate()

def test_price_bounds_and_slippage():
    from dex.models import LiquidityPool
    pool=LiquidityPool('pool1','EXC','USDC',initial_base=Decimal('1'),initial_quote=Decimal('1'),min_price=Decimal('2'),max_price=Decimal('1'))
    assert any('min_price' in e for e in pool.validate())
