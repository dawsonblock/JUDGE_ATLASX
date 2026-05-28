import type { ReactNode } from "react";

export interface EvidenceSnapshot {
  id: string;
  source_id: string;
  source_label?: string;
  sha256_hash?: string;
  captured_at: string;
  content_type?: string;
  storage_backend?: string;
  review_status: string;
  linked_claims?: string[];
  integrity_status?: "ok" | "tampered" | "unverified" | "missing";
}

interface Props {
  snapshot: EvidenceSnapshot;
  /** When true, show admin-only fields (storage path etc). Defaults false. */
  adminView?: boolean;
}

const INTEGRITY_LABELS: Record<string, { label: string; classes: string }> = {
  ok: { label: "Integrity verified", classes: "bg-green-100 text-green-800 border-green-200" },
  tampered: { label: "Integrity failure", classes: "bg-red-100 text-red-800 border-red-200" },
  unverified: { label: "Not yet verified", classes: "bg-yellow-100 text-yellow-800 border-yellow-200" },
  missing: { label: "Snapshot missing", classes: "bg-red-100 text-red-800 border-red-200" },
};

const REVIEW_STATUS_LABELS: Record<string, { label: string; classes: string }> = {
  approved: { label: "Approved", classes: "bg-green-100 text-green-800 border-green-200" },
  pending_review: { label: "Pending review", classes: "bg-yellow-100 text-yellow-800 border-yellow-200" },
  needs_revision: { label: "Needs revision", classes: "bg-orange-100 text-orange-800 border-orange-200" },
  rejected: { label: "Rejected", classes: "bg-red-100 text-red-800 border-red-200" },
  archived: { label: "Archived", classes: "bg-slate-100 text-slate-700 border-slate-200" },
};

function StatusBadge({ status, map }: { status: string; map: Record<string, { label: string; classes: string }> }) {
  const config = map[status] ?? { label: status, classes: "bg-slate-100 text-slate-700 border-slate-200" };
  return (
    <span className={`inline-flex items-center rounded border px-2 py-0.5 text-xs font-semibold ${config.classes}`}>
      {config.label}
    </span>
  );
}

function Field({ label, children }: { label: string; children: ReactNode }) {
  return (
    <div className="flex flex-col gap-0.5 py-2 border-b border-slate-100 last:border-0">
      <span className="text-xs font-medium text-slate-500 uppercase tracking-wide">{label}</span>
      <span className="text-sm text-slate-800 break-all">{children}</span>
    </div>
  );
}

export function EvidenceSnapshotCard({ snapshot, adminView = false }: Props) {
  const integrityConfig =
    snapshot.integrity_status && INTEGRITY_LABELS[snapshot.integrity_status]
      ? INTEGRITY_LABELS[snapshot.integrity_status]
      : INTEGRITY_LABELS["unverified"];

  return (
    <div className="rounded-lg border border-slate-200 bg-white shadow-sm">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-200 px-4 py-3">
        <h3 className="text-sm font-semibold text-slate-900">Evidence Snapshot</h3>
        <span
          className={`inline-flex items-center rounded border px-2 py-0.5 text-xs font-semibold ${integrityConfig.classes}`}
        >
          {integrityConfig.label}
        </span>
      </div>

      <div className="px-4">
        <Field label="Snapshot ID">{snapshot.id}</Field>
        <Field label="Source ID">{snapshot.source_id}</Field>
        {snapshot.source_label && (
          <Field label="Source">{snapshot.source_label}</Field>
        )}
        <Field label="Captured At">
          {new Date(snapshot.captured_at).toLocaleString("en-CA", {
            dateStyle: "medium",
            timeStyle: "short",
          })}
        </Field>
        {snapshot.content_type && (
          <Field label="Content Type">{snapshot.content_type}</Field>
        )}
        <Field label="Review Status">
          <StatusBadge status={snapshot.review_status} map={REVIEW_STATUS_LABELS} />
        </Field>

        {/* SHA-256 — always visible */}
        {snapshot.sha256_hash ? (
          <Field label="SHA-256 Hash">
            <code className="text-xs font-mono text-slate-600">{snapshot.sha256_hash}</code>
          </Field>
        ) : (
          <Field label="SHA-256 Hash">
            <span className="text-xs text-slate-400 italic">Not recorded</span>
          </Field>
        )}

        {/* Admin-only fields */}
        {adminView && snapshot.storage_backend && (
          <Field label="Storage Backend">{snapshot.storage_backend}</Field>
        )}

        {/* Linked claims */}
        {snapshot.linked_claims && snapshot.linked_claims.length > 0 && (
          <Field label={`Linked Claims (${snapshot.linked_claims.length})`}>
            <ul className="space-y-1 mt-1">
              {snapshot.linked_claims.map((claim, i) => (
                <li key={i} className="text-xs font-mono text-slate-600 bg-slate-50 rounded px-2 py-0.5">
                  {claim}
                </li>
              ))}
            </ul>
          </Field>
        )}
      </div>

      {/* Private storage path warning */}
      {!adminView && (
        <div className="border-t border-slate-100 px-4 py-2">
          <p className="text-xs text-slate-400">
            Storage paths are not exposed in the public API.
          </p>
        </div>
      )}
    </div>
  );
}
