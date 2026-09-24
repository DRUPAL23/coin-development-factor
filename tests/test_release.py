from release.models import DisasterRecoverySpec, ReleaseSpec


def valid_spec() -> ReleaseSpec:
    return ReleaseSpec(
        version="0.14.0",
        artifact_digest="sha256:abc123",
        signed=True,
        reproducible_build=True,
        changelog_present=True,
        rollback_plan_present=True,
        approvals=("release-manager", "security-reviewer"),
        disaster_recovery=DisasterRecoverySpec(
            backup_verified=True,
            restore_tested=True,
            recovery_point_objective_minutes=15,
            recovery_time_objective_minutes=60,
            runbook_url="https://example.invalid/runbook",
            owner="operations",
        ),
    )


def test_valid_release_is_ready():
    report = valid_spec().readiness_report()
    assert report["ready"] is True
    assert report["validation_errors"] == []


def test_release_fails_closed_without_signature_or_restore_test():
    spec = valid_spec()
    broken = ReleaseSpec(
        version=spec.version,
        artifact_digest=spec.artifact_digest,
        signed=False,
        reproducible_build=spec.reproducible_build,
        changelog_present=spec.changelog_present,
        rollback_plan_present=spec.rollback_plan_present,
        approvals=spec.approvals[:1],
        disaster_recovery=DisasterRecoverySpec(
            backup_verified=True,
            restore_tested=False,
            recovery_point_objective_minutes=15,
            recovery_time_objective_minutes=60,
            runbook_url=spec.disaster_recovery.runbook_url,
            owner=spec.disaster_recovery.owner,
        ),
    )
    report = broken.readiness_report()
    assert report["ready"] is False
    assert "release.signed must be true" in report["validation_errors"]
    assert "release.approvals must contain at least two approvers" in report["validation_errors"]
    assert "disaster_recovery.restore_tested must be true" in report["validation_errors"]


def test_invalid_digest_is_rejected():
    spec = valid_spec()
    invalid = ReleaseSpec(
        version=spec.version,
        artifact_digest="md5:abc",
        signed=spec.signed,
        reproducible_build=spec.reproducible_build,
        changelog_present=spec.changelog_present,
        rollback_plan_present=spec.rollback_plan_present,
        approvals=spec.approvals,
        disaster_recovery=spec.disaster_recovery,
    )
    assert invalid.readiness_report()["ready"] is False
