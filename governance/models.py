from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
import re


SUPPORTED_VOTING = {"token", "quadratic", "one_wallet_one_vote"}
SUPPORTED_PROPOSAL_TYPES = {"text", "parameter_change", "treasury_spend", "upgrade"}


@dataclass(frozen=True)
class GovernancePolicy:
    enabled: bool = True
    voting_model: str = "token"
    proposal_threshold: Decimal = Decimal("1000")
    quorum: Decimal = Decimal("0.20")
    approval_threshold: Decimal = Decimal("0.50")
    voting_period_days: int = 7
    timelock_days: int = 2
    execution_delay_days: int = 0
    proposer_whitelist_enabled: bool = False
    guardian_enabled: bool = True

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.voting_model not in SUPPORTED_VOTING:
            errors.append("governance.voting_model must be token, quadratic, or one_wallet_one_vote")
        if self.proposal_threshold < 0:
            errors.append("governance.proposal_threshold cannot be negative")
        if not Decimal("0") < self.quorum <= Decimal("1"):
            errors.append("governance.quorum must be greater than 0 and at most 1")
        if not Decimal("0") < self.approval_threshold <= Decimal("1"):
            errors.append("governance.approval_threshold must be greater than 0 and at most 1")
        if self.voting_period_days < 1:
            errors.append("governance.voting_period_days must be at least one")
        if self.timelock_days < 0:
            errors.append("governance.timelock_days cannot be negative")
        if self.execution_delay_days < 0:
            errors.append("governance.execution_delay_days cannot be negative")
        if self.execution_delay_days < self.timelock_days:
            errors.append("governance.execution_delay_days cannot be less than timelock_days")
        return errors


@dataclass(frozen=True)
class Proposal:
    proposal_id: str
    title: str
    proposal_type: str
    proposer: str
    voting_power: Decimal
    total_voting_power: Decimal
    yes_votes: Decimal
    no_votes: Decimal = Decimal("0")
    abstain_votes: Decimal = Decimal("0")
    cancelled: bool = False

    def validate(self, policy: GovernancePolicy) -> list[str]:
        errors: list[str] = []
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{2,63}", self.proposal_id):
            errors.append("proposal.proposal_id must be 3-64 characters using letters, numbers, '.', '_' or '-'")
        if not self.title.strip():
            errors.append("proposal.title is required")
        if self.proposal_type not in SUPPORTED_PROPOSAL_TYPES:
            errors.append("proposal.proposal_type is unsupported")
        if not self.proposer.strip():
            errors.append("proposal.proposer is required")
        if self.voting_power < 0 or self.total_voting_power <= 0:
            errors.append("proposal voting power values are invalid")
        if self.voting_power < policy.proposal_threshold:
            errors.append("proposal proposer does not meet the proposal threshold")
        for label, value in (("yes_votes", self.yes_votes), ("no_votes", self.no_votes), ("abstain_votes", self.abstain_votes)):
            if value < 0:
                errors.append(f"proposal.{label} cannot be negative")
        if self.yes_votes + self.no_votes + self.abstain_votes > self.total_voting_power:
            errors.append("proposal votes cannot exceed total voting power")
        return errors

    def turnout(self) -> Decimal:
        return self.yes_votes + self.no_votes + self.abstain_votes

    def outcome(self, policy: GovernancePolicy) -> str:
        errors = self.validate(policy)
        if errors or self.cancelled:
            return "invalid" if errors else "cancelled"
        turnout_ratio = self.turnout() / self.total_voting_power
        participating = self.yes_votes + self.no_votes
        approval_ratio = self.yes_votes / participating if participating else Decimal("0")
        if turnout_ratio < policy.quorum:
            return "quorum_not_met"
        if approval_ratio < policy.approval_threshold:
            return "rejected"
        return "passed"
