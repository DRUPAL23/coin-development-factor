from __future__ import annotations
import argparse, json
from decimal import Decimal
from dex.engine import load_pool, summary

def main() -> int:
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest='cmd',required=True)
    v=sub.add_parser('validate'); v.add_argument('config')
    q=sub.add_parser('quote'); q.add_argument('config'); q.add_argument('base_input', type=Decimal)
    a=p.parse_args(); pool=load_pool(a.config); errors=pool.validate()
    if a.cmd=='validate': print(json.dumps(summary(pool), indent=2)); return 0 if not errors else 1
    if errors: print(json.dumps({'validation_errors':errors}, indent=2)); return 1
    print(json.dumps({'pool_id':pool.pool_id,'base_input':str(a.base_input),'quote_output':str(pool.quote_output(a.base_input))}, indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
