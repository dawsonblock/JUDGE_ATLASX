"""Tests for the role-based permission matrix."""

from __future__ import annotations

import pytest

from app.auth.permission_matrix import Permission, all_roles, can, get_permissions


class TestPublicRole:
    def test_can_read_published(self):
        assert can("public", Permission.READ_PUBLISHED_INCIDENTS)
        assert can("public", Permission.READ_PUBLISHED_STATUTES)

    def test_cannot_approve(self):
        assert not can("public", Permission.APPROVE_RECORD)

    def test_cannot_trigger_ingestion(self):
        assert not can("public", Permission.TRIGGER_INGESTION)

    def test_cannot_manage_users(self):
        assert not can("public", Permission.MANAGE_USERS)


class TestDataEntryRole:
    def test_can_trigger_ingestion(self):
        assert can("data_entry", Permission.TRIGGER_INGESTION)

    def test_can_dry_run(self):
        assert can("data_entry", Permission.TRIGGER_DRY_RUN)

    def test_cannot_approve_records(self):
        assert not can("data_entry", Permission.APPROVE_RECORD)

    def test_cannot_publish(self):
        assert not can("data_entry", Permission.PUBLISH_RECORD)


class TestReviewerRole:
    def test_can_approve(self):
        assert can("reviewer", Permission.APPROVE_RECORD)

    def test_can_reject(self):
        assert can("reviewer", Permission.REJECT_RECORD)

    def test_can_publish(self):
        assert can("reviewer", Permission.PUBLISH_RECORD)

    def test_cannot_approve_high_risk(self):
        """Reviewers must not approve high-risk records without senior escalation."""
        assert not can("reviewer", Permission.APPROVE_HIGH_RISK_RECORD)

    def test_cannot_release_quarantine(self):
        assert not can("reviewer", Permission.RELEASE_QUARANTINE)

    def test_cannot_manage_users(self):
        assert not can("reviewer", Permission.MANAGE_USERS)


class TestSeniorReviewerRole:
    def test_can_approve_high_risk(self):
        assert can("senior_reviewer", Permission.APPROVE_HIGH_RISK_RECORD)

    def test_can_release_quarantine(self):
        assert can("senior_reviewer", Permission.RELEASE_QUARANTINE)

    def test_can_view_alpha_status(self):
        assert can("senior_reviewer", Permission.VIEW_ALPHA_STATUS)

    def test_cannot_manage_users(self):
        assert not can("senior_reviewer", Permission.MANAGE_USERS)

    def test_cannot_manage_feature_flags(self):
        assert not can("senior_reviewer", Permission.MANAGE_FEATURE_FLAGS)


class TestAdminRole:
    def test_has_all_permissions(self):
        """Admin must have every single permission."""
        for perm in Permission:
            assert can("admin", perm), f"Admin missing permission: {perm}"

    def test_can_manage_users(self):
        assert can("admin", Permission.MANAGE_USERS)


class TestSystemRole:
    def test_can_trigger_ingestion(self):
        assert can("system", Permission.TRIGGER_INGESTION)

    def test_cannot_manage_users(self):
        assert not can("system", Permission.MANAGE_USERS)

    def test_cannot_approve_records(self):
        assert not can("system", Permission.APPROVE_RECORD)


class TestUnknownRole:
    def test_unknown_role_falls_back_to_public(self):
        """Unknown roles must not get elevated permissions."""
        assert not can("hacker", Permission.APPROVE_RECORD)
        assert not can("", Permission.TRIGGER_INGESTION)
        assert can("unknown_role", Permission.READ_PUBLISHED_INCIDENTS)


class TestHelpers:
    def test_get_permissions_returns_frozenset(self):
        perms = get_permissions("reviewer")
        assert isinstance(perms, frozenset)

    def test_all_roles_includes_expected(self):
        roles = all_roles()
        for expected in ["public", "data_entry", "reviewer", "senior_reviewer", "admin"]:
            assert expected in roles
