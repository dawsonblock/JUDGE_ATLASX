"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";

interface Statute {
  id: number;
  title: string;
  citation: string;
  short_title: string;
  type: string;
  last_amended: string | null;
}

export default function StatutesBrowserPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [statutes, setStatutes] = useState<Statute[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState(searchParams.get("q") || "");
  const [sortBy, setSortBy] = useState<"frequency" | "title" | "recent">(
    (searchParams.get("sort") as any) || "frequency"
  );
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);

  const limit = 20;

  useEffect(() => {
    fetchStatutes();
  }, [searchTerm, sortBy, page]);

  const fetchStatutes = async () => {
    setIsLoading(true);
    try {
      const params = new URLSearchParams({
        limit: limit.toString(),
        offset: ((page - 1) * limit).toString(),
        sort_by: sortBy,
      });

      if (searchTerm) params.append("search", searchTerm);

      const response = await fetch(`/api/public/statutes?${params.toString()}`);

      if (!response.ok) throw new Error("Failed to fetch statutes");

      const data = await response.json();
      setStatutes(data.items || []);
      setTotal(data.total || 0);
    } catch (error) {
      console.error("[v0] Error fetching statutes:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    router.push(`/public/statutes?q=${encodeURIComponent(searchTerm)}`);
  };

  const totalPages = Math.ceil(total / limit);

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center mb-4">
            <div>
              <Link href="/" className="text-xl font-bold text-slate-900">
                Crime & Law Explorer
              </Link>
            </div>
            <nav className="flex gap-6">
              <Link href="/public/map" className="text-slate-700 hover:text-slate-900">
                Map
              </Link>
              <Link href="/public/statutes" className="text-blue-600 font-semibold">
                Laws
              </Link>
              <Link href="/public/about" className="text-slate-700 hover:text-slate-900">
                About
              </Link>
            </nav>
          </div>

          {/* Search Bar */}
          <form onSubmit={handleSearch} className="flex gap-3">
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search statutes..."
              className="flex-1 px-4 py-2 border border-slate-300 rounded-lg"
            />
            <button
              type="submit"
              className="px-6 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700"
            >
              Search
            </button>
          </form>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-6xl mx-auto px-6 py-12">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-slate-900">
            Canadian Federal Statutes
          </h1>
          <select
            value={sortBy}
            onChange={(e) => {
              setSortBy(e.target.value as any);
              setPage(1);
            }}
            className="px-4 py-2 border border-slate-300 rounded-lg bg-white"
          >
            <option value="frequency">Most Incidents</option>
            <option value="title">A-Z</option>
            <option value="recent">Recently Amended</option>
          </select>
        </div>

        {isLoading ? (
          <div className="text-center py-12">
            <p className="text-slate-600">Loading statutes...</p>
          </div>
        ) : statutes.length === 0 ? (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
            <p className="text-slate-700">
              No statutes found. Try a different search term.
            </p>
          </div>
        ) : (
          <>
            <div className="space-y-4 mb-8">
              {statutes.map((statute) => (
                <Link
                  key={statute.id}
                  href={`/public/statute/${statute.id}`}
                  className="block bg-white border border-slate-200 rounded-lg p-6 hover:border-blue-300 hover:bg-blue-50 transition"
                >
                  <div className="flex justify-between items-start mb-2">
                    <div className="flex-1">
                      <p className="font-mono text-sm text-blue-600 mb-1">
                        {statute.citation}
                      </p>
                      <h3 className="text-lg font-semibold text-slate-900">
                        {statute.title}
                      </h3>
                      {statute.short_title && statute.short_title !== statute.title && (
                        <p className="text-sm text-slate-600 mt-1">
                          {statute.short_title}
                        </p>
                      )}
                    </div>
                    <div className="text-right text-sm text-slate-500">
                      {statute.type}
                    </div>
                  </div>
                </Link>
              ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex justify-center gap-2 mt-8">
                <button
                  onClick={() => setPage(Math.max(1, page - 1))}
                  disabled={page === 1}
                  className="px-4 py-2 border border-slate-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Previous
                </button>
                <div className="flex items-center gap-2">
                  {Array.from({ length: totalPages }, (_, i) => i + 1).map(
                    (p) => (
                      <button
                        key={p}
                        onClick={() => setPage(p)}
                        className={`px-4 py-2 rounded-lg border ${
                          p === page
                            ? "bg-blue-600 text-white border-blue-600"
                            : "border-slate-300 hover:border-blue-300"
                        }`}
                      >
                        {p}
                      </button>
                    )
                  )}
                </div>
                <button
                  onClick={() => setPage(Math.min(totalPages, page + 1))}
                  disabled={page === totalPages}
                  className="px-4 py-2 border border-slate-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Next
                </button>
              </div>
            )}

            <p className="text-center text-sm text-slate-600 mt-6">
              Showing {(page - 1) * limit + 1}-
              {Math.min(page * limit, total)} of {total} statutes
            </p>
          </>
        )}
      </div>
    </div>
  );
}
