from audit.engine import load_spec
from audit.models import AuditFinding, LaunchControlSpec

def test_example_audit_is_ready():
    spec=load_spec('config/examples/example-audit.yaml')
    assert spec.validate()==[]
    assert spec.report()['ready'] is True

def test_mainnet_requires_change_freeze_and_rollback_window():
    spec=LaunchControlSpec(name='x',release_version='1.0.0',network='mainnet',controls={},signoff_roles=('ops',))
    errors=spec.validate()
    assert 'mainnet change_freeze must be enabled' in errors
    assert 'mainnet rollback_window_minutes must be at least 30' in errors

def test_high_finding_must_be_resolved():
    f=AuditFinding('A-1','high','Key risk','open')
    spec=LaunchControlSpec('x','1.0.0','testnet',{k:True for k in ('security_audit_complete','key_ceremony_rehearsed','rollback_plan_tested','incident_response_approved','legal_review_complete')},(f,),signoff_roles=('security',))
    assert any('critical/high findings must be resolved' in e for e in spec.validate())
