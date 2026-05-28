"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import ConfidenceBadge from "@/components/public/ConfidenceBadge";

interface Statute {
  section_id: number;
  section_label: string;
  marginal_note: string;
  text_excerpt: string;
  statute_title: string;
  citation: string;
  relevance: string;
  confidence: number;
  review_status?: string;
  ai_model_version?: string;
}

interface NewsArticle {
  id: number;
  title: string;
  url: string;
  publication: string;
  date: string | null;
  excerpt: string;
}

interface IncidentDetail {
  id: string;
  title: string;
  type: string;
  description: string;
  public_summary: string;
  location: string;
  lat: number;
  lng: number;
  jurisdiction: string;
  occurred_at: string | null;
  published_at: string | null;
  statutes: Statute[];
  news: NewsArticle[];
  confidence: number;
}

// ── Skeleton ──────────────────────────────────────────────────────────────────
function Skeleton({ className = "" }: { className?: string }) {
  return (
    <div
      className={`animate-pulse rounded ${className}`}
      style={{ background: "var(--pub-border)" }}
    />
  );
}

function LoadingState() {
  return (
    <div className="max-w-6xl mx-auto px-6 py-8">
      <Skeleton className="h-4 w-24 mb-6" />
      <div className="grid lg:grid-cols-[280px_1fr_280px] gap-6">
        <div className="flex flex-col gap-3">
          <Skeleton className="h-6 w-32 mb-2" />
          {[...Array(5)].map((_, i) => (
            <Skeleton key={i} className="h-10" />
          ))}
        </div>
        <div className="flex flex-col gap-4">
          <Skeleton className="h-32" />
          <Skeleton className="h-24" />
          <Skeleton className="h-24" />
        </div>
        <div className="flex flex-col gap-3">
          <Skeleton className="h-6 w-32 mb-2" />
          <Skeleton className="h-16" />
          <Skeleton className="h-16" />
        </div>
      </div>
    </div>
  );
}

// ── Meta row helper ───────────────────────────────────────────────────────────
function MetaRow({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div className="flex flex-col gap-0.5">
      <span
        className="text-xs font-semibold uppercase tracking-wider"
        style={{ color: "var(--pub-muted)" }}
      >
        {label}
      </span>
      <span className="text-sm" style={{ color: "var(--pub-ink)" }}>
        {value}
      </span>
    </div>
  );
}

// ── Main page ─────────────────────────────────────────────────────────────────
export default function IncidentDetailPage() {
  const params = useParams();
  const incidentId = params.id as string;

  const [incident, setIncident] = useState<IncidentDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedStatute, setExpandedStatute] = useState<number | null>(null);

  useEffect(() => {
    const fetchIncident = async () => {
      try {
        const response = await fetch(`/api/public/incident/${incidentId}`);
        if (!response.ok) throw new Error("Incident not found");
        const data = await response.json();
        setIncident(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Error loading incident");
      } finally {
        setIsLoading(false);
      }
    };
    fetchIncident();
  }, [incidentId]);

  // ── Loading ────────────────────────────────────────────────────────────────
  if (isLoading) {
    return <LoadingState />;
  }

  // ── Error ──────────────────────────────────────────────────────────────────
  if (error || !incident) {
    return (
      <div className="max-w-3xl mx-auto px-6 py-12">
        <Link
          href="/public/map"
          className="inline-flex items-center gap-1.5 text-sm font-medium mb-8 hover:underline"
          style={{ color: "var(--pub-navy)" }}
        >
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">
            <path d="M9 2L4 7l5 5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
          Back to Map
        </Link>
        <div
          className="rounded-lg p-6"
          style={{
            background: "var(--pub-danger-bg)",
            border: "1px solid #FECACA",
            color: "var(--pub-danger)",
          }}
        >
          <p className="font-semibold mb-1">Incident not found</p>
          <p className="text-sm">{error || "This incident may have been removed or the ID is invalid."}</p>
        </div>
      </div>
    );
  }

  const dateStr = incident.occurred_at
    ? new Date(incident.occurred_at).toLocaleDateString("en-CA", {
        year: "numeric",
        month: "long",
        day: "numeric",
      })
    : "Date unknown";

  return (
    <div style={{ background: "var(--pub-bg)" }}>
      {/* ── Breadcrumb / title bar ─────────────────────── */}
      <div
        className="px-6 py-4"
        style={{
          background: "var(--pub-surface)",
          borderBottom: "1px solid var(--pub-border)",
        }}
      >
        <div className="max-w-6xl mx-auto">
          <Link
            href="/public/map"
            className="inline-flex items-center gap-1.5 text-xs font-medium mb-3 hover:underline"
            style={{ color: "var(--pub-navy)" }}
          >
            <svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true">
              <path d="M7.5 2L3 6l4.5 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
            Back to Map
          </Link>
          <div className="flex items-start justify-between gap-4 flex-wrap">
            <div>
              <h1
                className="text-xl font-bold text-balance"
                style={{ color: "var(--pub-ink)", letterSpacing: "-0.01em" }}
              >
                {incident.title}
              </h1>
              <p className="text-sm mt-1" style={{ color: "var(--pub-muted)" }}>
                {incident.location} &middot; {dateStr}
              </p>
            </div>
            <div className="flex items-center gap-2 flex-shrink-0">
              <span
                className="text-xs px-2.5 py-1 rounded font-semibold capitalize"
                style={{
                  background: "rgba(15,76,117,0.08)",
                  color: "var(--pub-navy)",
                }}
              >
                {incident.type.replace(/_/g, " ")}
              </span>
              <ConfidenceBadge score={incident.confidence} />
            </div>
          </div>
        </div>
      </div>

      {/* ── 3-panel body ──────────────────────────────── */}
      <div className="max-w-6xl mx-auto px-6 py-8">
        <div className="grid lg:grid-cols-[268px_1fr_268px] gap-6 items-start">

          {/* ── Left panel: Basic facts ──────────────────── */}
          <aside>
            <div
              className="rounded-lg overflow-hidden"
              style={{
                background: "var(--pub-surface)",
                border: "1px solid var(--pub-border)",
              }}
            >
              <div
                className="px-5 py-4"
                style={{ borderBottom: "1px solid var(--pub-border)" }}
              >
                <h2
                  className="text-sm font-semibold"
                  style={{ color: "var(--pub-ink)" }}
                >
                  Basic Facts
                </h2>
              </div>
              <div className="px-5 py-5 flex flex-col gap-4">
                <MetaRow label="Offence type" value={incident.type.replace(/_/g, " ")} />
                <MetaRow label="Location" value={incident.location} />
                <MetaRow label="Jurisdiction" value={incident.jurisdiction} />
                <MetaRow label="Date" value={dateStr} />
                <MetaRow
                  label="Data confidence"
                  value={<ConfidenceBadge score={incident.confidence} />}
                />
              </div>

              {incident.description && (
                <div
                  className="px-5 pb-5"
                  style={{ borderTop: "1px solid var(--pub-border)" }}
                >
                  <p
                    className="text-xs font-semibold uppercase tracking-wider pt-4 mb-2"
                    style={{ color: "var(--pub-muted)" }}
                  >
                    Description
                  </p>
                  <p
                    className="text-sm leading-relaxed"
                    style={{ color: "var(--pub-text)" }}
                  >
                    {incident.description}
                  </p>
                </div>
              )}
            </div>
          </aside>

          {/* ── Centre panel: Laws + Summary ─────────────── */}
          <div className="flex flex-col gap-6">
            {/* AI summary */}
            {incident.public_summary && (
              <div
                className="rounded-lg p-5"
                style={{
                  background: "rgba(15,76,117,0.04)",
                  border: "1px solid rgba(15,76,117,0.14)",
                }}
              >
                <div className="flex items-center justify-between gap-3 mb-3">
                  <h2
                    className="text-sm font-semibold"
                    style={{ color: "var(--pub-ink)" }}
                  >
                    Why this matters
                  </h2>
                  <span
                    className="text-xs font-medium px-2 py-0.5 rounded"
                    style={{
                      background: "rgba(15,76,117,0.1)",
                      color: "var(--pub-navy)",
                    }}
                  >
                    AI summary
                  </span>
                </div>
                <p
                  className="text-sm leading-relaxed whitespace-pre-wrap"
                  style={{ color: "var(--pub-text)" }}
                >
                  {incident.public_summary}
                </p>
                <p
                  className="text-xs mt-4 pt-3 leading-relaxed"
                  style={{
                    borderTop: "1px solid rgba(15,76,117,0.12)",
                    color: "var(--pub-muted)",
                  }}
                >
                  AI-generated for civic understanding only. See statutes below for authoritative legal text.
                </p>
              </div>
            )}

            {/* Related statutes */}
            <div>
              <h2
                className="text-sm font-semibold mb-3"
                style={{ color: "var(--pub-ink)" }}
              >
                Related statutes{" "}
                <span style={{ color: "var(--pub-muted)", fontWeight: 400 }}>
                  ({incident.statutes.length})
                </span>
              </h2>

              {incident.statutes.length === 0 ? (
                <p className="text-sm" style={{ color: "var(--pub-muted)" }}>
                  No statute links have been generated yet.
                </p>
              ) : (
                <div className="flex flex-col gap-3">
                  {incident.statutes.map((statute) => {
                    const isOpen = expandedStatute === statute.section_id;
                    return (
                      <div
                        key={statute.section_id}
                        className="rounded-lg overflow-hidden"
                        style={{
                          background: "var(--pub-surface)",
                          border: "1px solid var(--pub-border)",
                        }}
                      >
                        <div className="px-5 py-4">
                          <div className="flex items-start justify-between gap-3 mb-2">
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center gap-2 flex-wrap mb-1">
                                <span
                                  className="text-xs font-mono font-semibold"
                                  style={{ color: "var(--pub-navy)" }}
                                >
                                  {statute.citation}
                                </span>
                                {statute.review_status === "approved" && (
                                  <span
                                    className="text-xs px-1.5 py-0.5 rounded font-medium"
                                    style={{
                                      background: "rgba(27,138,90,0.1)",
                                      color: "var(--pub-teal)",
                                    }}
                                  >
                                    Reviewed
                                  </span>
                                )}
                              </div>
                              <p
                                className="text-sm font-semibold"
                                style={{ color: "var(--pub-ink)" }}
                              >
                                {statute.marginal_note || statute.section_label}
                              </p>
                            </div>
                            <ConfidenceBadge score={statute.confidence} />
                          </div>

                          <p
                            className="text-xs leading-relaxed mb-3"
                            style={{ color: "var(--pub-text)" }}
                          >
                            <span style={{ color: "var(--pub-muted)" }}>Why relevant: </span>
                            {statute.relevance}
                          </p>

                          <div className="flex items-center gap-3">
                            <button
                              onClick={() =>
                                setExpandedStatute(isOpen ? null : statute.section_id)
                              }
                              className="text-xs font-medium hover:underline"
                              style={{ color: "var(--pub-navy)" }}
                            >
                              {isOpen ? "Hide" : "View"} statute text
                            </button>
                            <span style={{ color: "var(--pub-border-md)" }}>|</span>
                            <Link
                              href={`/public/statutes?highlight=${statute.section_id}`}
                              className="text-xs font-medium hover:underline"
                              style={{ color: "var(--pub-navy)" }}
                            >
                              Full statute
                            </Link>
                          </div>
                        </div>

                        {isOpen && (
                          <div
                            className="px-5 pb-4"
                            style={{ borderTop: "1px solid var(--pub-border)" }}
                          >
                            <p
                              className="text-xs leading-relaxed pt-4 font-mono"
                              style={{ color: "var(--pub-text)" }}
                            >
                              {statute.text_excerpt}
                            </p>
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </div>

          {/* ── Right panel: News + context ───────────────── */}
          <aside>
            <div
              className="rounded-lg overflow-hidden"
              style={{
                background: "var(--pub-surface)",
                border: "1px solid var(--pub-border)",
              }}
            >
              <div
                className="px-5 py-4"
                style={{ borderBottom: "1px solid var(--pub-border)" }}
              >
                <h2
                  className="text-sm font-semibold"
                  style={{ color: "var(--pub-ink)" }}
                >
                  News coverage{" "}
                  <span style={{ color: "var(--pub-muted)", fontWeight: 400 }}>
                    ({incident.news.length})
                  </span>
                </h2>
              </div>

              {incident.news.length === 0 ? (
                <p
                  className="text-sm px-5 py-5"
                  style={{ color: "var(--pub-muted)" }}
                >
                  No news articles linked to this incident.
                </p>
              ) : (
                <div className="divide-y" style={{ divideColor: "var(--pub-border)" }}>
                  {incident.news.map((article) => (
                    <a
                      key={article.id}
                      href={article.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block px-5 py-4 transition-colors hover:bg-slate-50"
                    >
                      <p
                        className="text-sm font-medium mb-1 leading-snug"
                        style={{ color: "var(--pub-ink)" }}
                      >
                        {article.title}
                      </p>
                      <p
                        className="text-xs mb-2"
                        style={{ color: "var(--pub-muted)" }}
                      >
                        {article.publication}
                        {article.date &&
                          ` · ${new Date(article.date).toLocaleDateString("en-CA", {
                            year: "numeric",
                            month: "short",
                            day: "numeric",
                          })}`}
                      </p>
                      {article.excerpt && (
                        <p
                          className="text-xs leading-relaxed line-clamp-3"
                          style={{ color: "var(--pub-text)" }}
                        >
                          {article.excerpt}
                        </p>
                      )}
                      <span
                        className="inline-flex items-center gap-1 text-xs font-medium mt-2"
                        style={{ color: "var(--pub-navy)" }}
                      >
                        Read article
                        <svg width="10" height="10" viewBox="0 0 10 10" fill="none" aria-hidden="true">
                          <path d="M2 5h6M5.5 2.5L8 5l-2.5 2.5" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                      </span>
                    </a>
                  ))}
                </div>
              )}
            </div>

            {/* Disclaimer */}
            <div
              className="rounded-lg px-4 py-3 mt-4 text-xs leading-relaxed"
              style={{
                background: "var(--pub-warn-bg)",
                border: "1px solid #FDE68A",
                color: "var(--pub-warn)",
              }}
            >
              Educational only. Statute links are AI-generated and may be incomplete. Not legal advice.
            </div>
          </aside>
        </div>
      </div>
    </div>
  );
}
