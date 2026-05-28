export interface AlphaReadinessStatus {
  alpha_gate_passed: boolean;
  production_ready: boolean;
  proof_chain_complete: boolean;
  archive_self_verifying: boolean;
  runnable_sources: number;
  total_sources: number;
  enable_ready_sources: number;
  deprecated_sources: number;
  evidence_store: "ok" | "missing" | "not_configured";
  storage_backend: string;
  queue_backend: string;
  rate_limit_backend: string;
  public_review_gate: "enabled" | "disabled";
  public_platform: "enabled" | "disabled";
  experimental_live_map: "enabled" | "disabled";
  workflow_admin: "enabled" | "disabled";
  runtime_profile: string;
  warnings: string[];
}

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function fetchAlphaReadiness(): Promise<AlphaReadinessStatus> {
  const res = await fetch(`${API_BASE}/api/v1/status/alpha-readiness`, {
    next: { revalidate: 30 },
  });
  if (!res.ok) {
    throw new Error(`Failed to fetch alpha readiness: ${res.status}`);
  }
  return res.json();
}
