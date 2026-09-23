from __future__ import annotations
from decimal import Decimal
from pathlib import Path
from typing import Any
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from architecture.engine import load_config as load_architecture
from contracts.engine import generate_erc20, load_spec as load_contract
from deployment.engine import load_spec as load_deployment, summary as deployment_summary
from dex.engine import load_pool, summary as dex_summary
from explorer.indexer import Indexer
from explorer.models import Block
from governance.engine import evaluate_proposal, load_policy as load_governance
from governance.models import Proposal
from staking.engine import calculate_reward, load_policy
from tokenomics.engine import calculate as calculate_tokenomics
from wallets.engine import load_spec as load_wallets
from integration.engine import load_spec as load_integration, summary as integration_summary
ROOT=Path(__file__).resolve().parents[1]
app=FastAPI(title='Coin Development Factory API',version='1.2.0')
EXPLORER=Indexer(); EXPLORER.add_block(Block(0,'0x'+'0'*64,'0x'+'0'*64,1,0))
class ValidationResponse(BaseModel):
    valid: bool
    errors: list[str]=Field(default_factory=list)
@app.get('/health')
def health()->dict[str,str]: return {'status':'ok','service':'coin-development-factor'}
@app.get('/v1/tokenomics')
def tokenomics()->dict[str,Any]: return calculate_tokenomics(ROOT/'config/examples/example-coin.yaml')
@app.get('/v1/architecture')
def architecture()->dict[str,Any]:
    m=load_architecture(ROOT/'config/examples/example-architecture.yaml'); return {'name':m.name,'network_id':m.network.network_id,'chain_type':m.network.chain_type,'consensus':m.consensus.mechanism,'validation_errors':m.validate()}
@app.get('/v1/wallets')
def wallets()->dict[str,Any]:
    m=load_wallets(ROOT/'config/examples/example-wallet.yaml'); return {'wallet_type':m.wallet_type,'chain':m.chain,'validation_errors':m.validate()}
@app.get('/v1/contracts/example')
def example_contract()->dict[str,Any]:
    s=load_contract(ROOT/'config/examples/example-contract.yaml'); return {'contract_name':s.contract_name,'target':s.target,'validation_errors':s.validate(),'source':generate_erc20(s)}
@app.get('/v1/staking')
def staking()->dict[str,Any]:
    p=load_policy(ROOT/'config/examples/example-staking.yaml'); return {'enabled':p.enabled,'min_stake':str(p.min_stake),'unbonding_period_days':p.unbonding_period_days,'reward_rate_annual':str(p.reward_rate_annual),'commission_rate':str(p.commission_rate),'max_validators':p.max_validators,'validation_errors':p.validate()}
@app.get('/v1/staking/reward')
def staking_reward(amount:str=Query(...),duration_days:int=Query(...,ge=0))->dict[str,str]:
    try:return calculate_reward(load_policy(ROOT/'config/examples/example-staking.yaml'),Decimal(amount),duration_days)
    except (ValueError,ArithmeticError) as exc: raise HTTPException(400,str(exc)) from exc
@app.get('/v1/governance')
def governance()->dict[str,Any]:
    p=load_governance(ROOT/'config/examples/example-governance.yaml'); return {'enabled':p.enabled,'voting_model':p.voting_model,'proposal_threshold':str(p.proposal_threshold),'quorum':str(p.quorum),'approval_threshold':str(p.approval_threshold),'voting_period_days':p.voting_period_days,'timelock_days':p.timelock_days,'execution_delay_days':p.execution_delay_days,'guardian_enabled':p.guardian_enabled,'validation_errors':p.validate()}
@app.get('/v1/governance/evaluate')
def governance_evaluate(proposal_id:str,title:str,proposal_type:str,proposer:str,voting_power:str,total_voting_power:str,yes_votes:str,no_votes:str,abstain_votes:str='0')->dict[str,str]:
    try:
        p=load_governance(ROOT/'config/examples/example-governance.yaml'); x=Proposal(proposal_id,title,proposal_type,proposer,Decimal(voting_power),Decimal(total_voting_power),Decimal(yes_votes),Decimal(no_votes),Decimal(abstain_votes)); return evaluate_proposal(p,x)
    except (ValueError,ArithmeticError) as exc: raise HTTPException(400,str(exc)) from exc
@app.get('/v1/dex')
def dex()->dict[str,Any]: return dex_summary(load_pool(ROOT/'config/examples/example-dex.yaml'))
@app.get('/v1/dex/quote')
def dex_quote(base_input:str=Query(...))->dict[str,str]:
    pool=load_pool(ROOT/'config/examples/example-dex.yaml'); errors=pool.validate()
    if errors: raise HTTPException(500,errors)
    try:return {'pool_id':pool.pool_id,'base_input':base_input,'quote_output':str(pool.quote_output(Decimal(base_input)))}
    except (ValueError,ArithmeticError) as exc: raise HTTPException(400,str(exc)) from exc
@app.get('/v1/deployment')
def deployment()->dict[str,Any]: return deployment_summary(load_deployment(ROOT/'config/examples/example-deployment.yaml'))
@app.get('/v1/integration')
def integration()->dict[str,Any]: return integration_summary(load_integration(ROOT/'config/examples/example-integration.yaml'))
@app.get('/v1/observability')
def observability()->dict[str,Any]:
    report=integration_summary(load_integration(ROOT/'config/examples/example-integration.yaml'))['health']
    return {'status':'healthy' if report['ready'] else 'degraded','checks':report['checks']}
@app.get('/v1/validate',response_model=ValidationResponse)
def validate_all()->ValidationResponse:
    models=[load_architecture(ROOT/'config/examples/example-architecture.yaml'),load_wallets(ROOT/'config/examples/example-wallet.yaml'),load_contract(ROOT/'config/examples/example-contract.yaml'),load_policy(ROOT/'config/examples/example-staking.yaml'),load_governance(ROOT/'config/examples/example-governance.yaml'),load_pool(ROOT/'config/examples/example-dex.yaml'),load_deployment(ROOT/'config/examples/example-deployment.yaml'),load_integration(ROOT/'config/examples/example-integration.yaml')]
    errors=[]
    for m in models: errors.extend(m.validate())
    return ValidationResponse(valid=not errors,errors=errors)
@app.get('/v1/explorer/status')
def explorer_status()->dict[str,Any]: return EXPLORER.status()
@app.get('/v1/explorer/blocks/{number}')
def explorer_block(number:int)->dict[str,Any]:
    block=EXPLORER.store.get_block(number)
    if block is None: raise HTTPException(404,'block not found')
    return block
@app.get('/v1/explorer/transactions')
def explorer_transactions(address:str|None=None,limit:int=Query(50,ge=1,le=100))->dict[str,Any]: return {'items':EXPLORER.store.list_transactions(address=address,limit=limit),'limit':limit}
