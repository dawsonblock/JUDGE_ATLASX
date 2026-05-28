import { AlphaReadinessPanel } from "@/components/status/AlphaReadinessPanel";
import { fetchAlphaReadiness } from "@/lib/api/status";

export const metadata = {
  title: "Alpha Status | JUDGE_ATLASX Admin",
  description: "Alpha readiness and system status for operators.",
};

export default async function AdminStatusPage() {
  let status = null;
  let error: string | null = null;

  try {
    status = await fetchAlphaReadiness();
  } catch (e) {
    error = e instanceof Error ? e.message : "Failed to load status";
  }

  return (
    <main className="mx-auto max-w-4xl px-4 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Alpha System Status</h1>
        <p className="mt-1 text-sm text-slate-500">
          Real-time readiness report for operators. Refresh to update.
        </p>
      </div>

      {error ? (
        <div className="rounded-lg border border-red-200 bg-red-50 p-6 text-sm text-red-800">
          <strong>Could not load status:</strong> {error}
          <p className="mt-2 text-xs text-red-600">
            Ensure the backend is running at{" "}
            {process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000"}.
          </p>
        </div>
      ) : status ? (
        <AlphaReadinessPanel status={status} />
      ) : (
        <p className="text-sm text-slate-500">Loading...</p>
      )}
    </main>
  );
}
