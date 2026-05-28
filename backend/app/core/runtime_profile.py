"""Runtime profile definitions for JUDGE_ATLASX.

Each profile defines what is allowed, required, and forbidden in that environment.
Startup validation calls get_active_profile() and enforces its rules.

Profiles:
  development   - local dev, all fallbacks allowed
  alpha_local   - evidence required, Docker optional
  alpha_docker  - PostGIS/Redis/evidence required
  staging       - near-production constraints
  production    - full enforcement, no experimental routes
  test          - deterministic, no network, fixture-only
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache


@dataclass(frozen=True)
class RuntimeProfile:
    name: str
    production_ready: bool
    # Storage / infra
    evidence_store_required: bool
    redis_required: bool
    docker_required: bool
    postgis_required: bool
    object_storage_required: bool
    # Egress / safety
    egress_policy_required: bool
    wildcard_cors_forbidden: bool
    # Queue / rate-limit flexibility
    allow_inprocess_queue: bool
    allow_memory_rate_limit: bool
    allow_local_storage: bool
    # Experimental routes
    allow_experimental_live_map: bool
    allow_workflow_admin: bool
    allow_legacy_admin_token: bool
    allow_legacy_us_routes: bool
    allow_public_platform: bool
    # Review gates
    public_review_gate_required: bool
    # Network
    allow_live_network: bool
    # Human-readable notes
    notes: list[str] = field(default_factory=list)


PROFILES: dict[str, RuntimeProfile] = {
    "development": RuntimeProfile(
        name="development",
        production_ready=False,
        evidence_store_required=False,
        redis_required=False,
        docker_required=False,
        postgis_required=False,
        object_storage_required=False,
        egress_policy_required=False,
        wildcard_cors_forbidden=False,
        allow_inprocess_queue=True,
        allow_memory_rate_limit=True,
        allow_local_storage=True,
        allow_experimental_live_map=True,
        allow_workflow_admin=True,
        allow_legacy_admin_token=True,
        allow_legacy_us_routes=True,
        allow_public_platform=True,
        public_review_gate_required=False,
        allow_live_network=True,
        notes=["All fallbacks allowed", "Not for public deployment"],
    ),
    "test": RuntimeProfile(
        name="test",
        production_ready=False,
        evidence_store_required=False,
        redis_required=False,
        docker_required=False,
        postgis_required=False,
        object_storage_required=False,
        egress_policy_required=False,
        wildcard_cors_forbidden=False,
        allow_inprocess_queue=True,
        allow_memory_rate_limit=True,
        allow_local_storage=True,
        allow_experimental_live_map=False,
        allow_workflow_admin=False,
        allow_legacy_admin_token=False,
        allow_legacy_us_routes=False,
        allow_public_platform=True,
        public_review_gate_required=True,
        allow_live_network=False,
        notes=["No live network", "Fixture data only", "Deterministic"],
    ),
    "alpha_local": RuntimeProfile(
        name="alpha_local",
        production_ready=False,
        evidence_store_required=True,
        redis_required=False,
        docker_required=False,
        postgis_required=False,
        object_storage_required=False,
        egress_policy_required=False,
        wildcard_cors_forbidden=False,
        allow_inprocess_queue=True,
        allow_memory_rate_limit=True,
        allow_local_storage=True,
        allow_experimental_live_map=False,
        allow_workflow_admin=False,
        allow_legacy_admin_token=False,
        allow_legacy_us_routes=False,
        allow_public_platform=True,
        public_review_gate_required=True,
        allow_live_network=True,
        notes=[
            "Evidence store required",
            "Public review gates required",
            "Docker optional",
            "Production ready: false",
        ],
    ),
    "alpha_docker": RuntimeProfile(
        name="alpha_docker",
        production_ready=False,
        evidence_store_required=True,
        redis_required=True,
        docker_required=True,
        postgis_required=True,
        object_storage_required=False,
        egress_policy_required=False,
        wildcard_cors_forbidden=True,
        allow_inprocess_queue=False,
        allow_memory_rate_limit=False,
        allow_local_storage=True,
        allow_experimental_live_map=False,
        allow_workflow_admin=False,
        allow_legacy_admin_token=False,
        allow_legacy_us_routes=False,
        allow_public_platform=True,
        public_review_gate_required=True,
        allow_live_network=True,
        notes=[
            "Evidence store required",
            "PostGIS required",
            "Redis required",
            "Docker proof expected",
            "Production ready: false",
        ],
    ),
    "staging": RuntimeProfile(
        name="staging",
        production_ready=False,
        evidence_store_required=True,
        redis_required=True,
        docker_required=True,
        postgis_required=True,
        object_storage_required=True,
        egress_policy_required=True,
        wildcard_cors_forbidden=True,
        allow_inprocess_queue=False,
        allow_memory_rate_limit=False,
        allow_local_storage=False,
        allow_experimental_live_map=False,
        allow_workflow_admin=False,
        allow_legacy_admin_token=False,
        allow_legacy_us_routes=False,
        allow_public_platform=True,
        public_review_gate_required=True,
        allow_live_network=True,
        notes=["Near-production constraints", "Object storage required"],
    ),
    "production": RuntimeProfile(
        name="production",
        production_ready=False,  # still false until certified
        evidence_store_required=True,
        redis_required=True,
        docker_required=True,
        postgis_required=True,
        object_storage_required=True,
        egress_policy_required=True,
        wildcard_cors_forbidden=True,
        allow_inprocess_queue=False,
        allow_memory_rate_limit=False,
        allow_local_storage=False,
        allow_experimental_live_map=False,
        allow_workflow_admin=False,
        allow_legacy_admin_token=False,
        allow_legacy_us_routes=False,
        allow_public_platform=False,  # must be explicitly enabled post-certification
        public_review_gate_required=True,
        allow_live_network=True,
        notes=[
            "Full enforcement",
            "Experimental routes forbidden",
            "Wildcard CORS forbidden",
            "Egress policy required",
            "Production ready may still be false until certified",
        ],
    ),
}


@lru_cache(maxsize=1)
def get_active_profile() -> RuntimeProfile:
    """Return the active runtime profile based on APP_ENV / JTA_APP_ENV."""
    import os

    env = os.environ.get("JTA_APP_ENV", os.environ.get("APP_ENV", "development")).lower()
    return PROFILES.get(env, PROFILES["development"])


def get_profile_warnings(profile: RuntimeProfile) -> list[str]:
    """Return human-readable warnings for the active profile."""
    warnings: list[str] = []
    if not profile.production_ready:
        warnings.append(
            f"Production readiness is FALSE for profile '{profile.name}'. "
            "Do not treat this system as production-certified."
        )
    if profile.allow_legacy_admin_token:
        warnings.append("Legacy admin token auth is enabled. Use JWT in production.")
    if not profile.public_review_gate_required:
        warnings.append("Public review gate is NOT required. Records may be unreviewed.")
    if profile.allow_inprocess_queue:
        warnings.append("In-process queue is active. Not suitable for production.")
    return warnings
