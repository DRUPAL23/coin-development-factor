from contracts.engine import generate_erc20, load_spec
from security.static_checks import blocking_findings, scan_solidity


def test_generated_contract_has_no_blocking_findings() -> None:
    source = generate_erc20(load_spec("config/examples/example-contract.yaml"))
    findings = scan_solidity(source)
    assert blocking_findings(findings) == []


def test_scanner_flags_dangerous_patterns() -> None:
    source = "contract Bad { function f() external { require(tx.origin == msg.sender); selfdestruct(payable(msg.sender)); } }"
    findings = scan_solidity(source)
    assert {finding.rule_id for finding in findings} >= {"SC001", "SC003", "SC005", "SC006"}
    assert len(blocking_findings(findings)) == 2


def test_scanner_is_clean_for_safe_minimal_source() -> None:
    source = "uint256 public constant MAX_SUPPLY = 1; _mint(msg.sender, 1);"
    assert scan_solidity(source) == []
