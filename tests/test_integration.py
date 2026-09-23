from integration.engine import load_spec

def test_example_integration_is_valid_and_ready():
    spec = load_spec('config/examples/example-integration.yaml')
    assert spec.validate() == []
    report = spec.health_report()
    assert report['ready'] is True
    assert report['checks']['metrics_enabled'] is True

def test_missing_observability_fails_closed(tmp_path):
    path = tmp_path / 'bad.yaml'
    path.write_text('integration:\n  name: x\n  chain_id: 1\n  native_symbol: X\n  endpoints:\n    - name: rpc\n      url: https://rpc.example\n      timeout_seconds: 5\n      required: true\n')
    spec = load_spec(path)
    assert spec.validate() == []
    assert spec.health_report()['ready'] is False

def test_invalid_endpoint_is_rejected(tmp_path):
    path = tmp_path / 'bad.yaml'
    path.write_text('integration:\n  name: x\n  chain_id: 1\n  native_symbol: X\n  endpoints:\n    - name: rpc\n      url: ftp://rpc.example\n      timeout_seconds: 5\n      required: true\n  wallet_adapter: readonly\n  observability:\n    metrics_enabled: true\n    structured_logging_enabled: true\n')
    assert 'http(s) or ws(s)' in load_spec(path).validate()[0]
