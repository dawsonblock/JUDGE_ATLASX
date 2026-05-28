/**
 * Alpha Readiness Status
 *
 * Canonical TypeScript model for the backend AlphaReadinessResponse schema.
 * Mirrors backend/app/api/routes/alpha_status.py:AlphaReadinessResponse exactly.
 *
 * Any field rename in the backend MUST be reflected here and in
 * frontend/lib/api/status.ts before the frontend is redeployed.
 *
 * Endpoint: GET /api/v1/status/alpha-readiness
 * Auth:     admin session required
 */
export interface AlphaReadinessStatus {
  // Overall gates --------------------------------------------------------
  /** True only when ALL proof gates have passed AND sources are runnable. */
  alpha_gate_passed: boolean;
  /**
   * Always false in alpha. Becomes true only after independent security audit,
   * load tests, and legal sign-off. Do NOT enable the public platform based
   * solely on alpha_gate_passed.
   */
  production_ready: boolean;
  /** True when CURRENT_PROOF.md / REPAIR_PROOF.json exists and is non-empty. */
  proof_chain_complete: boolean;
  /** True when validate_release_archive.py exits 0 (self-verifying archive). */
  archive_self_verifying: boolean;

  // Source coverage -------------------------------------------------------
  /** DB count of sources with lifecycle_state = "runnable" (active). */
  runnable_sources: number;
  /** Total count of all sources in SourceRegistry table. */
  total_sources: number;
  /** DB count of sources with lifecycle_state = "runnable_disabled" (can enable). */
  enable_ready_sources: number;
  /** DB count of sources with lifecycle_state = "deprecated" (read-only). */
  deprecated_sources: number;

  // Infrastructure --------------------------------------------------------
  /** "ok" | "missing" | "not_configured" — evidence store directory state. */
  evidence_store: "ok" | "missing" | "not_configured";
  /** Name of the active storage backend (e.g. "local", "s3"). */
  storage_backend: string;
  /** Name of the active queue backend (e.g. "redis", "memory", "none"). */
  queue_backend: string;
  /** Name of the active rate-limit backend (e.g. "memory", "redis", "none"). */
  rate_limit_backend: string;

  // Feature gates ---------------------------------------------------------
  /** "enabled" | "disabled" — controlled by JTA_ENABLE_PUBLIC_REVIEW_GATE. */
  public_review_gate: "enabled" | "disabled";
  /** "enabled" | "disabled" — controlled by JTA_ENABLE_PUBLIC_PLATFORM. */
  public_platform: "enabled" | "disabled";
  /** "enabled" | "disabled" — controlled by JTA_ENABLE_EXPERIMENTAL_LIVE_MAP. */
  experimental_live_map: "enabled" | "disabled";
  /** "enabled" | "disabled" — controlled by JTA_ENABLE_WORKFLOW_ADMIN. */
  workflow_admin: "enabled" | "disabled";

  // Runtime ---------------------------------------------------------------
  /** Active runtime profile name (e.g. "alpha", "development", "test"). */
  runtime_profile: string;
  /** Non-fatal warnings about configuration gaps — always shown. */
  warnings: string[];
}

/**
 * Minimal type for feature-gate checks only.
 * Use when you only need to test whether a feature is enabled,
 * without pulling the full readiness model.
 */
export type FeatureGates = Pick<
  AlphaReadinessStatus,
  "public_platform" | "public_review_gate" | "experimental_live_map" | "workflow_admin"
>;

/** Source lifecycle counts extracted from the full readiness status. */
export type SourceCounts = Pick<
  AlphaReadinessStatus,
  "runnable_sources" | "enable_ready_sources" | "deprecated_sources" | "total_sources"
>;
