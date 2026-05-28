"use client";

import type { AlphaReadinessStatus } from "@/lib/api/status";

interface Props {
  status: AlphaReadinessStatus;
}

type Verdict = "pass" | "fail" | "warn" | "info";

function Badge({ verdict, label }: { verdict: Verdict; label: string }) {
  const styles: Record<Verdict, string> = {
    pass: "bg-green-100 text-green-800 border-green-200",
    fail: "bg-red-100 text-red-800 border-red-200",
    warn: "bg-yellow-100 text-yellow-800 border-yellow-200",
    info: "bg-slate-100 text-slate-700 border-slate-200",
  };
  return (
    <span
      className={`inline-flex items-center rounded border px-2 py-0.5 text-xs font-semibold ${styles[verdict]}`}
    >
      {label}
    </span>
  );
}

function Row({
  label,
  verdict,
  value,
}: {
  label: string;
  verdict: Verdict;
  value: string;
}) {
  return (
    <div className="flex items-center justify-between py-2 border-b border-slate-100 last:border-0">
      <span className="text-sm text-slate-600">{label}</span>
      <Badge verdict={verdict} label={value} />
    </div>
  );
}

export function AlphaReadinessPanel({ status }: Props) {
  const evidenceVerdict =
    status.evidence_store === "ok"
      ? "pass"
      : status.evidence_store === "missing"
        ? "fail"
        : "warn";

  return (
    <div className="space-y-6">
      {/* Alpha notice — always visible */}
      <div className="rounded-lg border border-amber-300 bg-amber-50 p-4">
        <p className="text-sm font-semibold text-amber-900">
          This system is an alpha. Public-facing records require human review
          and evidence snapshots. Production readiness is false.
        </p>
      </div>

      {/* Gate summary */}
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
        <GateTile
          label="Alpha Gate"
          passed={status.alpha_gate_passed}
          passLabel="Passed"
          failLabel="Not Passed"
        />
        <GateTile
          label="Production Ready"
          passed={status.production_ready}
          passLabel="Yes"
          failLabel="No"
        />
        <GateTile
          label="Proof Chain"
          passed={status.proof_chain_complete}
          passLabel="Complete"
          failLabel="Incomplete"
        />
        <GateTile
          label="Archive Self-Verifying"
          passed={status.archive_self_verifying}
          passLabel="Yes"
          failLabel="No"
        />
      </div>

      {/* Source coverage */}
      <Section title="Source Coverage">
        <Row
          label="Runnable sources"
          verdict={status.runnable_sources > 0 ? "pass" : "fail"}
          value={`${status.runnable_sources} / ${status.total_sources}`}
        />
        <Row
          label="Enable-ready sources"
          verdict="info"
          value={String(status.enable_ready_sources)}
        />
        <Row
          label="Deprecated sources"
          verdict="info"
          value={String(status.deprecated_sources)}
        />
      </Section>

      {/* Infrastructure */}
      <Section title="Infrastructure">
        <Row
          label="Evidence store"
          verdict={evidenceVerdict}
          value={status.evidence_store}
        />
        <Row label="Storage backend" verdict="info" value={status.storage_backend} />
        <Row label="Queue backend" verdict="info" value={status.queue_backend} />
        <Row
          label="Rate limit backend"
          verdict={status.rate_limit_backend === "memory" ? "warn" : "pass"}
          value={status.rate_limit_backend}
        />
      </Section>

      {/* Feature gates */}
      <Section title="Feature Gates">
        <Row
          label="Public review gate"
          verdict={status.public_review_gate === "enabled" ? "pass" : "fail"}
          value={status.public_review_gate}
        />
        <Row
          label="Public platform"
          verdict={status.public_platform === "enabled" ? "warn" : "info"}
          value={status.public_platform}
        />
        <Row
          label="Experimental live map"
          verdict={status.experimental_live_map === "enabled" ? "warn" : "info"}
          value={status.experimental_live_map}
        />
        <Row
          label="Workflow admin"
          verdict={status.workflow_admin === "enabled" ? "warn" : "info"}
          value={status.workflow_admin}
        />
        <Row label="Runtime profile" verdict="info" value={status.runtime_profile} />
      </Section>

      {/* Warnings */}
      {status.warnings.length > 0 && (
        <Section title={`Warnings (${status.warnings.length})`}>
          <ul className="space-y-2">
            {status.warnings.map((w, i) => (
              <li
                key={i}
                className="rounded bg-yellow-50 border border-yellow-200 px-3 py-2 text-sm text-yellow-900"
              >
                {w}
              </li>
            ))}
          </ul>
        </Section>
      )}
    </div>
  );
}

function GateTile({
  label,
  passed,
  passLabel,
  failLabel,
}: {
  label: string;
  passed: boolean;
  passLabel: string;
  failLabel: string;
}) {
  return (
    <div
      className={`rounded-lg border p-4 text-center ${
        passed
          ? "border-green-200 bg-green-50"
          : "border-red-200 bg-red-50"
      }`}
    >
      <p className="text-xs text-slate-500 mb-1">{label}</p>
      <p
        className={`text-sm font-bold ${
          passed ? "text-green-800" : "text-red-800"
        }`}
      >
        {passed ? passLabel : failLabel}
      </p>
    </div>
  );
}

function Section({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white">
      <div className="border-b border-slate-200 px-4 py-3">
        <h3 className="text-sm font-semibold text-slate-800">{title}</h3>
      </div>
      <div className="px-4">{children}</div>
    </div>
  );
}
