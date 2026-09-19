from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from typing import Any

import yaml

from governance.models import GovernancePolicy, Proposal


def load_policy(path: str | Path) -> GovernancePolicy:
    with Path(path).open("r", encoding="utf-8") as handle:
        data: dict[str, Any] = yaml.safe_load(handle) or {}
    governance = data.get("governance", data)
    return GovernancePolicy(
        enabled=bool(governance.get("enabled", True)),
        voting_model=str(governance.get("voting_model", "token")),
        proposal_threshold=Decimal(str(governance.get("proposal_threshold", 1000))),
        quorum=Decimal(str(governance.get("quorum", "0.20"))),
        approval_threshold=Decimal(str(governance.get("approval_threshold", "0.50"))),
        voting_period_days=int(governance.get("voting_period_days", 7)),
        timelock_days=int(governance.get("timelock_days", 2)),
        execution_delay_days=int(governance.get("execution_delay_days", 2)),
        proposer_whitelist_enabled=bool(governance.get("proposer_whitelist_enabled", False)),
        guardian_enabled=bool(governance.get("guardian_enabled", True)),
    )


def evaluate_proposal(policy: GovernancePolicy, proposal: Proposal) -> dict[str, str]:
    errors = policy.validate() + proposal.validate(policy)
    return {
        "proposal_id": proposal.proposal_id,
        "outcome": proposal.outcome(policy) if not errors else "invalid",
        "turnout_ratio": str(proposal.turnout() / proposal.total_voting_power) if proposal.total_voting_power else "0",
        "approval_ratio": str(proposal.yes_votes / (proposal.yes_votes + proposal.no_votes)) if proposal.yes_votes + proposal.no_votes else "0",
        "validation_errors": "|".join(errors),
    }
