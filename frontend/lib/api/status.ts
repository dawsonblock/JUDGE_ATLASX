/**
 * Alpha Readiness API client.
 *
 * The canonical TypeScript interface lives in types/alpha-status.ts.
 * This module re-exports it so existing imports of AlphaReadinessStatus
 * from "lib/api/status" continue to work without change.
 */

export type {
  AlphaReadinessStatus,
  FeatureGates,
  SourceCounts,
} from "@/types/alpha-status";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

/**
 * Fetch the current alpha readiness status from the backend.
 * Requires an active admin session cookie; unauthenticated requests return 401.
 *
 * @throws {Error} when the HTTP response is not 2xx
 */
export async function fetchAlphaReadiness(
  options?: RequestInit,
): Promise<import("@/types/alpha-status").AlphaReadinessStatus> {
  const res = await fetch(`${API_BASE}/api/v1/status/alpha-readiness`, {
    ...options,
    next: { revalidate: 30 },
    credentials: "include",
  });
  if (!res.ok) {
    throw new Error(
      `Failed to fetch alpha readiness: ${res.status} ${res.statusText}`,
    );
  }
  return res.json();
}
