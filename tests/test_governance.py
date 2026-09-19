from decimal import Decimal
from pathlib import Path

from governance.engine import evaluate_proposal, load_policy
from governance.models import GovernancePolicy, Proposal


ROOT = Path(__file__).parents[1]
EXAMPLE = ROOT / "config/examples/example-governance.yaml"


def test_example_policy_is_valid() -> None:
    assert load_policy(EXAMPLE).validate() == []


def test_proposal_passes_quorum_and_approval() -> None:
    policy = load_policy(EXAMPLE)
    proposal = Proposal("p-001", "Increase treasury budget", "treasury_spend", "alice", Decimal("2000"), Decimal("10000"), Decimal("3000"), Decimal("1000"))
    result = evaluate_proposal(policy, proposal)
    assert result["outcome"] == "passed"


def test_quorum_failure_is_detected() -> None:
    policy = GovernancePolicy(proposal_threshold=Decimal("1"), quorum=Decimal("0.5"))
    proposal = Proposal("p-002", "Low turnout", "text", "alice", Decimal("1"), Decimal("100"), Decimal("10"), Decimal("5"))
    assert proposal.outcome(policy) == "quorum_not_met"


def test_rejection_when_approval_threshold_is_not_met() -> None:
    policy = GovernancePolicy(proposal_threshold=Decimal("1"), quorum=Decimal("0.1"), approval_threshold=Decimal("0.6"))
    proposal = Proposal("p-003", "Reject me", "parameter_change", "alice", Decimal("1"), Decimal("100"), Decimal("4"), Decimal("6"))
    assert proposal.outcome(policy) == "rejected"


def test_threshold_and_vote_bounds_are_validated() -> None:
    policy = GovernancePolicy(proposal_threshold=Decimal("100"))
    proposal = Proposal("bad", "", "unknown", "", Decimal("1"), Decimal("10"), Decimal("9"), Decimal("9"))
    errors = proposal.validate(policy)
    assert any("proposal threshold" in error for error in errors)
    assert any("title is required" in error for error in errors)
    assert any("unsupported" in error for error in errors)
    assert any("votes cannot exceed" in error for error in errors)


def test_cancelled_proposal_is_not_executable() -> None:
    policy = GovernancePolicy(proposal_threshold=Decimal("1"))
    proposal = Proposal("p-004", "Cancelled", "text", "alice", Decimal("1"), Decimal("10"), Decimal("9"), Decimal("0"), cancelled=True)
    assert proposal.outcome(policy) == "cancelled"
