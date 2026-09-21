from deployment.engine import load_spec
from deployment.models import DeploymentSpec

def test_example_deployment_is_valid():
    spec=load_spec('config/examples/example-deployment.yaml')
    assert spec.validate()==[]
    assert spec.readiness_report()['ready'] is True

def test_mainnet_requires_https_and_four_validators():
    spec=DeploymentSpec('main','mainnet','docker',1,'http://rpc','http://explorer','img',1,2,{'x':True},('SECRET',))
    errors=spec.validate()
    assert 'mainnet RPC must use HTTPS' in errors
    assert 'mainnet explorer_url must use HTTPS' in errors
    assert 'mainnet requires at least four validators' in errors

def test_readiness_requires_explicit_operational_checks():
    spec=DeploymentSpec('test','testnet','docker',1,'https://rpc','https://explorer','img',1,1,{},('SECRET',))
    report=spec.readiness_report()
    assert report['ready'] is False
    assert report['checks']['monitoring_configured'] is not True
