"use client";

import { Suspense, useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";

interface Statute {
  id: number;
  title: string;
  citation: string;
  short_title: string;
  type: string;
  incident_count?: number;
  last_amended: string | null;
}

// ── Skeleton row ──────────────────────────────────────────────────────────────
function SkeletonRow() {
  return (
    <div
      className="rounded-lg p-5 animate-pulse"
      style={{ background: "var(--pub-surface)", border: "1px solid var(--pub-border)" }}
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1">
          <div className="h-3 w-28 rounded mb-2" style={{ background: "var(--pub-border)" }} />
          <div className="h-4 w-64 rounded mb-1.5" style={{ background: "var(--pub-border)" }} />
          <div className="h-3 w-40 rounded" style={{ background: "var(--pub-border)" }} />
        </div>
        <div className="h-5 w-14 rounded" style={{ background: "var(--pub-border)" }} />
      </div>
    </div>
  );
}

// ── Core browser component ────────────────────────────────────────────────────
function StatutesBrowser() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [statutes, setStatutes] = useState<Statute[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState(searchParams.get("q") || "");
  const [draftSearch, setDraftSearch] = useState(searchParams.get("q") || "");
  const [sortBy, setSortBy] = useState<"frequency" | "title" | "recent">(
    (searchParams.get("sort") as "frequency" | "title" | "recent") || "frequency"
  );
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);

  const LIMIT = 20;

  const fetchStatutes = useCallback(async () => {
    setIsLoading(true);
    try {
      const params = new URLSearchParams({
        limit: LIMIT.toString(),
        offset: ((page - 1) * LIMIT).toString(),
        sort_by: sortBy,
      });
      if (searchTerm) params.append("search", searchTerm);
      const res = await fetch(`/api/public/statutes?${params}`);
      if (!res.ok) throw new Error("Failed to fetch statutes");
      const data = await res.json();
      setStatutes(data.items || []);
      setTotal(data.total || 0);
    } catch {
      setStatutes([]);
    } finally {
      setIsLoading(false);
    }
  }, [searchTerm, sortBy, page]);

  useEffect(() => {
    fetchStatutes();
  }, [fetchStatutes]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setSearchTerm(draftSearch);
    setPage(1);
    if (draftSearch) {
      router.push(`/public/statutes?q=${encodeURIComponent(draftSearch)}`);
    } else {
      router.push("/public/statutes");
    }
  };

  const totalPages = Math.ceil(total / LIMIT);
  const from = (page - 1) * LIMIT + 1;
  const to = Math.min(page * LIMIT, total);

  return (
    <div style={{ background: "var(--pub-bg)" }}>
      {/* ── Page header ──────────────────────────────── */}
      <div
        className="px-6 py-8"
        style={{
          background: "var(--pub-surface)",
          borderBottom: "1px solid var(--pub-border)",
        }}
      >
        <div className="max-w-5xl mx-auto">
          <h1
            className="text-2xl font-bold mb-1 text-balance"
            style={{ color: "var(--pub-ink)", letterSpacing: "-0.01em" }}
          >
            Canadian Federal Statutes
          </h1>
          <p className="text-sm mb-6" style={{ color: "var(--pub-muted)" }}>
            Browse statutes linked to crime incidents. Click any entry to see all related incidents.
          </p>

          {/* Search + sort row */}
          <form
            onSubmit={handleSearch}
            className="flex flex-col sm:flex-row gap-3"
          >
            <div className="flex-1 relative">
              <svg
                width="16"
                height="16"
                viewBox="0 0 16 16"
                fill="none"
                className="absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none"
                style={{ color: "var(--pub-muted)" }}
                aria-hidden="true"
              >
                <circle cx="7" cy="7" r="4.5" stroke="currentColor" strokeWidth="1.5" />
                <path d="M10.5 10.5L13 13" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
              </svg>
              <input
                type="search"
                value={draftSearch}
                onChange={(e) => setDraftSearch(e.target.value)}
                placeholder="Search by statute title or citation…"
                className="w-full pl-9 pr-4 py-2.5 rounded text-sm"
                style={{
                  border: "1px solid var(--pub-border-md)",
                  background: "var(--pub-bg)",
                  color: "var(--pub-ink)",
                  outline: "none",
                }}
              />
            </div>
            <button
              type="submit"
              className="px-5 py-2.5 rounded text-sm font-semibold transition-opacity hover:opacity-90"
              style={{ background: "var(--pub-navy)", color: "#fff" }}
            >
              Search
            </button>
            <select
              value={sortBy}
              onChange={(e) => {
                setSortBy(e.target.value as "frequency" | "title" | "recent");
                setPage(1);
              }}
              className="px-3 py-2.5 rounded text-sm"
              style={{
                border: "1px solid var(--pub-border-md)",
                background: "var(--pub-bg)",
                color: "var(--pub-ink)",
              }}
            >
              <option value="frequency">Most incidents</option>
              <option value="title">A – Z</option>
              <option value="recent">Recently amended</option>
            </select>
          </form>
        </div>
      </div>

      {/* ── Results ──────────────────────────────────── */}
      <div className="max-w-5xl mx-auto px-6 py-8">
        {/* Result count */}
        {!isLoading && total > 0 && (
          <p className="text-xs mb-4" style={{ color: "var(--pub-muted)" }}>
            Showing {from}–{to} of {total} statutes
            {searchTerm && (
              <>
                {" "}for <span style={{ color: "var(--pub-ink)" }}>&ldquo;{searchTerm}&rdquo;</span>
              </>
            )}
          </p>
        )}

        {isLoading ? (
          <div className="flex flex-col gap-3">
            {[...Array(8)].map((_, i) => <SkeletonRow key={i} />)}
          </div>
        ) : statutes.length === 0 ? (
          <div
            className="rounded-lg px-6 py-8 text-center"
            style={{ background: "var(--pub-warn-bg)", border: "1px solid #FDE68A" }}
          >
            <p className="text-sm font-semibold mb-1" style={{ color: "var(--pub-warn)" }}>
              No statutes found
            </p>
            <p className="text-xs" style={{ color: "var(--pub-warn)" }}>
              Try a different search term or{" "}
              <button
                onClick={() => { setDraftSearch(""); setSearchTerm(""); setPage(1); }}
                className="underline font-medium"
              >
                clear the search
              </button>
              .
            </p>
          </div>
        ) : (
          <div className="flex flex-col gap-2.5 mb-8">
            {statutes.map((statute) => (
              <Link
                key={statute.id}
                href={`/public/statute/${statute.id}`}
                className="flex items-start justify-between gap-4 rounded-lg px-5 py-4 transition-colors group"
                style={{
                  background: "var(--pub-surface)",
                  border: "1px solid var(--pub-border)",
                }}
              >
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1 flex-wrap">
                    <span
                      className="text-xs font-mono font-semibold"
                      style={{ color: "var(--pub-navy)" }}
                    >
                      {statute.citation}
                    </span>
                    <span
                      className="text-xs px-1.5 py-0.5 rounded"
                      style={{
                        background: "var(--pub-bg)",
                        color: "var(--pub-muted)",
                        border: "1px solid var(--pub-border)",
                      }}
                    >
                      {statute.type || "Federal"}
                    </span>
                  </div>
                  <p
                    className="text-sm font-semibold mb-0.5 group-hover:underline"
                    style={{ color: "var(--pub-ink)" }}
                  >
                    {statute.title}
                  </p>
                  {statute.short_title && statute.short_title !== statute.title && (
                    <p className="text-xs" style={{ color: "var(--pub-muted)" }}>
                      {statute.short_title}
                    </p>
                  )}
                </div>
                <div className="flex-shrink-0 text-right">
                  {statute.incident_count !== undefined && (
                    <div
                      className="text-xs font-semibold px-2.5 py-1 rounded"
                      style={{
                        background: statute.incident_count > 0
                          ? "rgba(15,76,117,0.08)"
                          : "var(--pub-bg)",
                        color: statute.incident_count > 0
                          ? "var(--pub-navy)"
                          : "var(--pub-muted)",
                      }}
                    >
                      {statute.incident_count} incident{statute.incident_count !== 1 ? "s" : ""}
                    </div>
                  )}
                </div>
              </Link>
            ))}
          </div>
        )}

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="flex items-center justify-center gap-2">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1}
              className="px-4 py-2 rounded text-sm font-medium disabled:opacity-40"
              style={{
                border: "1px solid var(--pub-border-md)",
                color: "var(--pub-text)",
                background: "var(--pub-surface)",
              }}
            >
              Previous
            </button>
            <div className="flex items-center gap-1">
              {Array.from({ length: Math.min(totalPages, 7) }, (_, i) => {
                const p = i + 1;
                return (
                  <button
                    key={p}
                    onClick={() => setPage(p)}
                    className="w-9 h-9 rounded text-sm font-medium transition-colors"
                    style={{
                      background: p === page ? "var(--pub-navy)" : "var(--pub-surface)",
                      color: p === page ? "#fff" : "var(--pub-text)",
                      border: p === page ? "1px solid var(--pub-navy)" : "1px solid var(--pub-border-md)",
                    }}
                  >
                    {p}
                  </button>
                );
              })}
            </div>
            <button
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
              className="px-4 py-2 rounded text-sm font-medium disabled:opacity-40"
              style={{
                border: "1px solid var(--pub-border-md)",
                color: "var(--pub-text)",
                background: "var(--pub-surface)",
              }}
            >
              Next
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

// ── Page export ───────────────────────────────────────────────────────────────
export default function StatutesBrowserPage() {
  return (
    <Suspense
      fallback={
        <div
          className="flex items-center justify-center py-24"
          style={{ background: "var(--pub-bg)" }}
        >
          <div className="text-center">
            <div
              className="w-7 h-7 rounded-full border-2 border-t-transparent animate-spin mx-auto mb-3"
              style={{ borderColor: "var(--pub-navy)" }}
            />
            <p className="text-sm" style={{ color: "var(--pub-muted)" }}>
              Loading statutes…
            </p>
          </div>
        </div>
      }
    >
      <StatutesBrowser />
    </Suspense>
  );
}
