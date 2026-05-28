"use client";

import { useState, useCallback } from "react";
import dynamic from "next/dynamic";
import type { Metadata } from "next";

const MapComponent = dynamic(
  () => import("@/components/public/PublicCrimeMap"),
  { ssr: false, loading: () => <MapPlaceholder /> }
);

function MapPlaceholder() {
  return (
    <div
      className="flex-1 flex items-center justify-center"
      style={{ background: "#E8EEF4" }}
    >
      <div className="text-center">
        <div
          className="w-8 h-8 rounded-full border-2 border-t-transparent animate-spin mx-auto mb-3"
          style={{ borderColor: "var(--pub-navy)" }}
        />
        <p className="text-sm" style={{ color: "var(--pub-muted)" }}>
          Loading map…
        </p>
      </div>
    </div>
  );
}

const CRIME_TYPES = [
  { value: "murder", label: "Murder" },
  { value: "assault", label: "Assault" },
  { value: "theft", label: "Theft" },
  { value: "robbery", label: "Robbery" },
  { value: "fraud", label: "Fraud" },
  { value: "drug_offense", label: "Drug offence" },
  { value: "property_crime", label: "Property crime" },
  { value: "violent_crime", label: "Violent crime" },
];

const JURISDICTIONS = [
  "Ontario",
  "Quebec",
  "British Columbia",
  "Alberta",
  "Manitoba",
  "Saskatchewan",
  "Nova Scotia",
  "New Brunswick",
  "Prince Edward Island",
  "Newfoundland and Labrador",
  "Yukon",
  "Northwest Territories",
  "Nunavut",
];

interface Filters {
  dateFrom: string;
  dateTo: string;
  crimeTypes: string[];
  jurisdictions: string[];
}

const DEFAULT_FILTERS: Filters = {
  dateFrom: "",
  dateTo: "",
  crimeTypes: [],
  jurisdictions: [],
};

export default function PublicMapPage() {
  const [filters, setFilters] = useState<Filters>(DEFAULT_FILTERS);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const toggleCrimeType = useCallback((val: string) => {
    setFilters((prev) => ({
      ...prev,
      crimeTypes: prev.crimeTypes.includes(val)
        ? prev.crimeTypes.filter((t) => t !== val)
        : [...prev.crimeTypes, val],
    }));
  }, []);

  const toggleJurisdiction = useCallback((val: string) => {
    setFilters((prev) => ({
      ...prev,
      jurisdictions: prev.jurisdictions.includes(val)
        ? prev.jurisdictions.filter((j) => j !== val)
        : [...prev.jurisdictions, val],
    }));
  }, []);

  const activeCount =
    filters.crimeTypes.length +
    filters.jurisdictions.length +
    (filters.dateFrom ? 1 : 0) +
    (filters.dateTo ? 1 : 0);

  return (
    /* The layout already provides <PublicNav> and the outer <main>.
       This page fills the remaining viewport height as a flex row. */
    <div className="flex" style={{ height: "calc(100vh - 56px)" }}>
      {/* ── Sidebar ────────────────────────────────────── */}
      <aside
        className="flex-shrink-0 flex flex-col overflow-hidden transition-all duration-200"
        style={{
          width: sidebarOpen ? "288px" : "0px",
          borderRight: "1px solid var(--pub-border)",
          background: "var(--pub-surface)",
        }}
        aria-label="Map filters"
      >
        <div
          className="flex-1 overflow-y-auto"
          style={{ display: sidebarOpen ? "block" : "none" }}
        >
          {/* Sidebar header */}
          <div
            className="px-5 py-4 flex items-center justify-between"
            style={{ borderBottom: "1px solid var(--pub-border)" }}
          >
            <div className="flex items-center gap-2">
              <span
                className="text-sm font-semibold"
                style={{ color: "var(--pub-ink)" }}
              >
                Filters
              </span>
              {activeCount > 0 && (
                <span
                  className="text-xs font-semibold px-1.5 py-0.5 rounded-full"
                  style={{
                    background: "var(--pub-navy)",
                    color: "#fff",
                  }}
                >
                  {activeCount}
                </span>
              )}
            </div>
            <button
              onClick={() => setFilters(DEFAULT_FILTERS)}
              className="text-xs font-medium hover:underline"
              style={{ color: "var(--pub-navy)" }}
              disabled={activeCount === 0}
            >
              Reset all
            </button>
          </div>

          <div className="px-5 py-5 flex flex-col gap-6">
            {/* Date range */}
            <fieldset>
              <legend
                className="text-xs font-semibold uppercase tracking-wider mb-3 block"
                style={{ color: "var(--pub-muted)" }}
              >
                Date range
              </legend>
              <div className="flex flex-col gap-2">
                {[
                  { key: "dateFrom", label: "From" },
                  { key: "dateTo", label: "To" },
                ].map(({ key, label }) => (
                  <div key={key} className="relative">
                    <label
                      className="absolute left-3 top-1/2 -translate-y-1/2 text-xs pointer-events-none"
                      style={{ color: "var(--pub-muted)" }}
                      htmlFor={`date-${key}`}
                    >
                      {label}
                    </label>
                    <input
                      id={`date-${key}`}
                      type="date"
                      value={filters[key as keyof Filters] as string}
                      onChange={(e) =>
                        setFilters((prev) => ({
                          ...prev,
                          [key]: e.target.value,
                        }))
                      }
                      className="w-full pl-10 pr-3 py-2 rounded text-sm"
                      style={{
                        border: "1px solid var(--pub-border-md)",
                        color: "var(--pub-ink)",
                        background: "var(--pub-bg)",
                      }}
                    />
                  </div>
                ))}
              </div>
            </fieldset>

            {/* Crime types */}
            <fieldset>
              <legend
                className="text-xs font-semibold uppercase tracking-wider mb-3 block"
                style={{ color: "var(--pub-muted)" }}
              >
                Offence type
              </legend>
              <div className="flex flex-col gap-2">
                {CRIME_TYPES.map(({ value, label }) => (
                  <label
                    key={value}
                    className="flex items-center gap-2.5 cursor-pointer group"
                  >
                    <input
                      type="checkbox"
                      checked={filters.crimeTypes.includes(value)}
                      onChange={() => toggleCrimeType(value)}
                      className="w-4 h-4 rounded"
                      style={{ accentColor: "var(--pub-navy)" }}
                    />
                    <span
                      className="text-sm"
                      style={{ color: "var(--pub-text)" }}
                    >
                      {label}
                    </span>
                  </label>
                ))}
              </div>
            </fieldset>

            {/* Jurisdictions */}
            <fieldset>
              <legend
                className="text-xs font-semibold uppercase tracking-wider mb-3 block"
                style={{ color: "var(--pub-muted)" }}
              >
                Province / Territory
              </legend>
              <div
                className="flex flex-col gap-2 overflow-y-auto"
                style={{ maxHeight: "180px" }}
              >
                {JURISDICTIONS.map((j) => (
                  <label
                    key={j}
                    className="flex items-center gap-2.5 cursor-pointer"
                  >
                    <input
                      type="checkbox"
                      checked={filters.jurisdictions.includes(j)}
                      onChange={() => toggleJurisdiction(j)}
                      className="w-4 h-4 rounded"
                      style={{ accentColor: "var(--pub-navy)" }}
                    />
                    <span
                      className="text-sm"
                      style={{ color: "var(--pub-text)" }}
                    >
                      {j}
                    </span>
                  </label>
                ))}
              </div>
            </fieldset>

            {/* Tip */}
            <div
              className="rounded p-3 text-xs leading-relaxed"
              style={{
                background: "rgba(15,76,117,0.06)",
                color: "var(--pub-navy)",
                border: "1px solid rgba(15,76,117,0.12)",
              }}
            >
              Click any incident marker to view related statutes and news coverage.
            </div>
          </div>
        </div>
      </aside>

      {/* ── Toggle button ─────────────────────────────── */}
      <button
        onClick={() => setSidebarOpen((o) => !o)}
        className="absolute left-0 z-20 flex items-center justify-center w-6 rounded-r transition-all duration-200"
        style={{
          top: "50%",
          transform: "translateY(-50%)",
          marginLeft: sidebarOpen ? "288px" : "0",
          height: "48px",
          background: "var(--pub-surface)",
          border: "1px solid var(--pub-border)",
          borderLeft: "none",
          color: "var(--pub-muted)",
          cursor: "pointer",
        }}
        aria-label={sidebarOpen ? "Collapse filters" : "Expand filters"}
      >
        <svg
          width="10"
          height="10"
          viewBox="0 0 10 10"
          fill="none"
          style={{
            transform: sidebarOpen ? "rotate(0deg)" : "rotate(180deg)",
            transition: "transform 0.2s",
          }}
          aria-hidden="true"
        >
          <path
            d="M6 2L3 5l3 3"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </button>

      {/* ── Map ───────────────────────────────────────── */}
      <div className="flex-1 relative">
        <MapComponent filters={filters} />
      </div>
    </div>
  );
}
