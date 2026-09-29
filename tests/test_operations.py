from operations.engine import load_spec

def test_example_operations_is_ready():
    spec = load_spec("config/examples/example-operations.yaml")
    report = spec.readiness_report()
    assert report["ready"] is True
    assert report["validation_errors"] == []

def test_mainnet_requires_sev1(tmp_path):
    p = tmp_path / "bad.yaml"
    p.write_text("""operations:
  name: x
  service: y
  environment: mainnet
  slos:
    - name: rpc
      availability_target: 99.9
      latency_p95_ms: 500
      error_rate_target: 1
      owner: sre
  incident_policies:
    - severity: sev2
      acknowledgement_minutes: 15
      update_interval_minutes: 30
      escalation_path: [oncall]
      runbook_url: https://example.invalid/runbook
  paging_enabled: true
  metrics_enabled: true
  logs_enabled: true
  traces_enabled: true
  oncall_roster: [oncall]
  status_page_url: https://example.invalid/status
""")
    assert "mainnet requires a sev1 incident policy" in load_spec(p).validate()

def test_missing_observability_fails_closed(tmp_path):
    p = tmp_path / "bad.yaml"
    p.write_text("""operations:
  name: x
  service: y
  environment: staging
  slos:
    - name: rpc
      availability_target: 99.9
      latency_p95_ms: 500
      error_rate_target: 1
      owner: sre
  incident_policies:
    - severity: sev1
      acknowledgement_minutes: 5
      update_interval_minutes: 15
      escalation_path: [oncall]
      runbook_url: https://example.invalid/runbook
  paging_enabled: true
  metrics_enabled: false
  logs_enabled: true
  traces_enabled: true
  oncall_roster: [oncall]
  status_page_url: https://example.invalid/status
""")
    assert load_spec(p).readiness_report()["ready"] is False
