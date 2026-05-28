"use client";

import { useState } from "react";
import useSWR from "swr";
import useSWRMutation from "swr/mutation";

const BACKEND = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

interface QuarantinedRun {
  id: number;
  source_name: string;
  status: string;
  pipeline_stage: string | null;
  quarantine_reason: string | null;
  started_at: string;
  finished_at: string | null;
  fetched_count: number;
  parsed_count: number;
  persisted_count: number;
  error_count: number;
}

const fetcher = (url: string) =>
  fetch(url, {
    credentials: "include",
    headers: { Authorization: `Bearer ${document.cookie.match(/jta_access_token=([^;]+)/)?.[1] ?? ""}` },
  }).then((r) => {
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    return r.json();
  });

async function releaseRun(url: string, { arg }: { arg: { id: number } }) {
  const token = document.cookie.match(/jta_access_token=([^;]+)/)?.[1] ?? "";
  const res = await fetch(`${BACKEND}/api/admin/quarantine/${arg.id}/release`, {
    method: "POST",
    credentials: "include",
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

export default function QuarantinePage() {
  const { data, error, isLoading, mutate } = useSWR<QuarantinedRun[]>(
    `${BACKEND}/api/admin/quarantine`,
    fetcher,
    { refreshInterval: 30_000 }
  );
  const { trigger: release, isMutating } = useSWRMutation(
    `${BACKEND}/api/admin/quarantine/release`,
    releaseRun
  );
  const [releasing, setReleasing] = useState<number | null>(null);
  const [toast, setToast] = useState<string | null>(null);

  async function handleRelease(id: number) {
    setReleasing(id);
    try {
      await release({ id });
      setToast(`Run #${id} released.`);
      mutate();
    } catch {
      setToast(`Failed to release run #${id}.`);
    } finally {
      setReleasing(null);
      setTimeout(() => setToast(null), 4000);
    }
  }

  return (
    <main className="p-6 max-w-5xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Quarantined Ingestion Runs</h1>
        <p className="text-sm text-slate-500 mt-1">
          Runs flagged due to parser version mismatch, schema errors, or contradictions.
          Review and release or discard each run.
        </p>
      </div>

      {toast && (
        <div className="mb-4 rounded bg-blue-50 border border-blue-200 px-4 py-2 text-sm text-blue-800">
          {toast}
        </div>
      )}

      {isLoading && (
        <div className="text-sm text-slate-400 py-12 text-center">Loading quarantined runs...</div>
      )}

      {error && (
        <div className="rounded border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          Failed to load quarantined runs. Check backend connectivity.
        </div>
      )}

      {data && data.length === 0 && (
        <div className="rounded border border-green-200 bg-green-50 px-4 py-6 text-center text-sm text-green-800">
          No quarantined runs. All ingestion pipelines are clean.
        </div>
      )}

      {data && data.length > 0 && (
        <div className="space-y-4">
          {data.map((run) => (
            <div
              key={run.id}
              className="rounded-lg border border-amber-200 bg-amber-50 p-5"
            >
              <div className="flex items-start justify-between gap-4">
                <div className="min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-mono text-xs bg-amber-100 text-amber-800 px-2 py-0.5 rounded">
                      #{run.id}
                    </span>
                    <span className="font-semibold text-slate-900 truncate">
                      {run.source_name}
                    </span>
                    <span className="text-xs uppercase tracking-wide text-amber-700 font-medium">
                      {run.status}
                    </span>
                  </div>

                  {run.quarantine_reason && (
                    <p className="text-sm text-red-700 bg-red-50 border border-red-200 rounded px-3 py-2 mt-2">
                      <span className="font-semibold">Reason:</span> {run.quarantine_reason}
                    </p>
                  )}

                  <div className="mt-3 flex flex-wrap gap-4 text-xs text-slate-500">
                    <span>Stage: <span className="text-slate-700">{run.pipeline_stage ?? "—"}</span></span>
                    <span>Started: <span className="text-slate-700">{new Date(run.started_at).toLocaleString()}</span></span>
                    {run.finished_at && (
                      <span>Finished: <span className="text-slate-700">{new Date(run.finished_at).toLocaleString()}</span></span>
                    )}
                    <span>Fetched: <span className="text-slate-700">{run.fetched_count}</span></span>
                    <span>Parsed: <span className="text-slate-700">{run.parsed_count}</span></span>
                    <span>Persisted: <span className="text-slate-700">{run.persisted_count}</span></span>
                    <span>
                      Errors:{" "}
                      <span className={run.error_count > 0 ? "text-red-600 font-semibold" : "text-slate-700"}>
                        {run.error_count}
                      </span>
                    </span>
                  </div>
                </div>

                <button
                  onClick={() => handleRelease(run.id)}
                  disabled={releasing === run.id || isMutating}
                  className="shrink-0 rounded px-4 py-2 text-sm font-medium bg-slate-900 text-white hover:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {releasing === run.id ? "Releasing..." : "Release"}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
