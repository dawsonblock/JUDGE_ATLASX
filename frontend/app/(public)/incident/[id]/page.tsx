"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";

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

export default function IncidentDetailPage() {
  const params = useParams();
  const incidentId = params.id as string;

  const [incident, setIncident] = useState<IncidentDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchIncident = async () => {
      try {
        const response = await fetch(
          `/api/public/incident/${incidentId}`
        );

        if (!response.ok) {
          throw new Error("Incident not found");
        }

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

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-slate-600 mb-4">Loading incident details...</div>
        </div>
      </div>
    );
  }

  if (error || !incident) {
    return (
      <div className="min-h-screen bg-slate-50">
        <header className="bg-white border-b border-slate-200">
          <div className="max-w-7xl mx-auto px-6 py-4">
            <Link href="/public/map" className="text-blue-600 hover:text-blue-700">
              ← Back to Map
            </Link>
          </div>
        </header>
        <div className="max-w-4xl mx-auto px-6 py-12">
          <div className="bg-red-50 border border-red-200 rounded-lg p-6">
            <p className="text-red-800">{error || "Incident not found"}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div>
            <Link href="/public/map" className="text-blue-600 hover:text-blue-700 text-sm font-medium mb-2 block">
              ← Back to Map
            </Link>
            <h1 className="text-2xl font-bold text-slate-900">{incident.title}</h1>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-6xl mx-auto px-6 py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Left Panel - Basic Facts */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg border border-slate-200 p-6">
              <h2 className="text-lg font-bold text-slate-900 mb-6">
                Basic Facts
              </h2>

              <div className="space-y-4">
                <div>
                  <p className="text-xs font-semibold text-slate-500 uppercase">
                    Type
                  </p>
                  <p className="text-slate-900 capitalize">
                    {incident.type.replace("_", " ")}
                  </p>
                </div>

                <div>
                  <p className="text-xs font-semibold text-slate-500 uppercase">
                    Location
                  </p>
                  <p className="text-slate-900">{incident.location}</p>
                </div>

                <div>
                  <p className="text-xs font-semibold text-slate-500 uppercase">
                    Jurisdiction
                  </p>
                  <p className="text-slate-900">{incident.jurisdiction}</p>
                </div>

                <div>
                  <p className="text-xs font-semibold text-slate-500 uppercase">
                    Date
                  </p>
                  <p className="text-slate-900">
                    {incident.occurred_at
                      ? new Date(incident.occurred_at).toLocaleDateString()
                      : "Unknown"}
                  </p>
                </div>

                <div>
                  <p className="text-xs font-semibold text-slate-500 uppercase">
                    Confidence
                  </p>
                  <div className="flex items-center gap-2">
                    <div className="flex-1 bg-slate-200 rounded-full h-2">
                      <div
                        className="bg-blue-600 h-2 rounded-full"
                        style={{ width: `${incident.confidence * 100}%` }}
                      />
                    </div>
                    <span className="text-sm text-slate-600">
                      {Math.round(incident.confidence * 100)}%
                    </span>
                  </div>
                </div>
              </div>

              {incident.description && (
                <div className="mt-6 pt-6 border-t border-slate-200">
                  <p className="text-xs font-semibold text-slate-500 uppercase mb-2">
                    Description
                  </p>
                  <p className="text-slate-700 text-sm leading-relaxed">
                    {incident.description}
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Middle Panel - Statutes and Explanation */}
          <div className="lg:col-span-2 space-y-8">
            {/* Public Summary */}
            {incident.public_summary && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                <div className="flex items-start justify-between gap-4 mb-4">
                  <h2 className="text-lg font-bold text-slate-900">
                    Why This Matters
                  </h2>
                  <span className="bg-blue-100 text-blue-800 text-xs font-semibold px-3 py-1 rounded whitespace-nowrap">
                    AI-Generated
                  </span>
                </div>
                <p className="text-slate-700 leading-relaxed whitespace-pre-wrap">
                  {incident.public_summary}
                </p>
                <p className="text-xs text-slate-500 mt-4 pt-4 border-t border-blue-200">
                  This explanation is generated by AI to help you understand context. See approved laws below for authoritative information.
                </p>
              </div>
            )}

            {/* Related Statutes */}
            <div>
              <h2 className="text-lg font-bold text-slate-900 mb-4">
                Related Laws ({incident.statutes.length})
              </h2>

              {incident.statutes.length === 0 ? (
                <p className="text-slate-600">
                  No related statutes found yet.
                </p>
              ) : (
                <div className="space-y-4">
                  {incident.statutes.map((statute, idx) => (
                    <div
                      key={idx}
                      className="bg-white border border-slate-200 rounded-lg p-6"
                    >
                      <div className="flex justify-between items-start mb-3">
                        <div>
                          <div className="flex items-center gap-2 mb-1">
                            <p className="font-mono text-sm text-blue-600">
                              {statute.citation}
                            </p>
                            {statute.review_status === "approved" && (
                              <span className="bg-green-100 text-green-800 text-xs font-semibold px-2 py-1 rounded">
                                Approved
                              </span>
                            )}
                          </div>
                          <p className="font-semibold text-slate-900">
                            {statute.marginal_note || statute.section_label}
                          </p>
                        </div>
                        <div className="text-right">
                          <p className="text-xs text-slate-500 uppercase">
                            Confidence
                          </p>
                          <p className="font-semibold text-blue-600">
                            {Math.round(statute.confidence * 100)}%
                          </p>
                        </div>
                      </div>

                      <p className="text-sm text-slate-600 mb-4">
                        <strong>Why relevant:</strong> {statute.relevance}
                      </p>

                      <details className="bg-slate-50 rounded p-3">
                        <summary className="cursor-pointer font-medium text-slate-700 text-sm">
                          View statute text
                        </summary>
                        <p className="mt-3 text-slate-700 text-sm leading-relaxed">
                          {statute.text_excerpt}
                        </p>
                      </details>

                      <Link
                        href={`/public/statute/${statute.section_id}`}
                        className="inline-block mt-3 text-blue-600 hover:text-blue-700 text-sm font-medium"
                      >
                        View full statute →
                      </Link>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Related News */}
            <div>
              <h2 className="text-lg font-bold text-slate-900 mb-4">
                News Coverage ({incident.news.length})
              </h2>

              {incident.news.length === 0 ? (
                <p className="text-slate-600">
                  No news articles found for this incident.
                </p>
              ) : (
                <div className="space-y-3">
                  {incident.news.map((article) => (
                    <a
                      key={article.id}
                      href={article.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block bg-white border border-slate-200 rounded-lg p-4 hover:border-blue-300 hover:bg-blue-50 transition"
                    >
                      <p className="font-semibold text-slate-900 mb-1">
                        {article.title}
                      </p>
                      <p className="text-xs text-slate-500 mb-2">
                        {article.publication}
                        {article.date &&
                          ` • ${new Date(article.date).toLocaleDateString()}`}
                      </p>
                      {article.excerpt && (
                        <p className="text-sm text-slate-700 line-clamp-2">
                          {article.excerpt}
                        </p>
                      )}
                    </a>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
