"use client";

import { useState, useEffect, useCallback } from "react";
import Link from "next/link";
import dynamic from "next/dynamic";

// Dynamically import map to avoid SSR issues
const MapComponent = dynamic(() => import("@/components/public/PublicCrimeMap"), {
  ssr: false,
});

export default function PublicMapPage() {
  const [filters, setFilters] = useState({
    dateFrom: "",
    dateTo: "",
    crimeTypes: [] as string[],
    jurisdictions: [] as string[],
  });

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Common crime types for filtering
  const CRIME_TYPES = [
    "murder",
    "assault",
    "theft",
    "robbery",
    "fraud",
    "drug_offense",
    "property_crime",
    "violent_crime",
  ];

  // Canadian jurisdictions
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

  const handleCrimeTypeToggle = useCallback((type: string) => {
    setFilters((prev) => ({
      ...prev,
      crimeTypes: prev.crimeTypes.includes(type)
        ? prev.crimeTypes.filter((t) => t !== type)
        : [...prev.crimeTypes, type],
    }));
  }, []);

  const handleJurisdictionToggle = useCallback((jurisdiction: string) => {
    setFilters((prev) => ({
      ...prev,
      jurisdictions: prev.jurisdictions.includes(jurisdiction)
        ? prev.jurisdictions.filter((j) => j !== jurisdiction)
        : [...prev.jurisdictions, jurisdiction],
    }));
  }, []);

  const handleReset = useCallback(() => {
    setFilters({
      dateFrom: "",
      dateTo: "",
      crimeTypes: [],
      jurisdictions: [],
    });
  }, []);

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <div>
              <Link href="/" className="text-xl font-bold text-slate-900">
                Crime & Law Explorer
              </Link>
              <p className="text-sm text-slate-600">
                Crime incidents across Canada
              </p>
            </div>
            <nav className="flex gap-6">
              <Link href="/public/map" className="text-blue-600 font-semibold">
                Map
              </Link>
              <Link href="/public/statutes" className="text-slate-700 hover:text-slate-900">
                Laws
              </Link>
              <Link href="/public/about" className="text-slate-700 hover:text-slate-900">
                About
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex h-[calc(100vh-70px)]">
        {/* Sidebar - Filters */}
        <div className="w-80 bg-white border-r border-slate-200 overflow-y-auto">
          <div className="p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-lg font-bold text-slate-900">Filters</h2>
              <button
                onClick={handleReset}
                className="text-sm text-blue-600 hover:text-blue-700 font-medium"
              >
                Reset
              </button>
            </div>

            {/* Date Range */}
            <div className="mb-6">
              <label className="block text-sm font-semibold text-slate-900 mb-3">
                Date Range
              </label>
              <div className="space-y-2">
                <input
                  type="date"
                  value={filters.dateFrom}
                  onChange={(e) =>
                    setFilters((prev) => ({ ...prev, dateFrom: e.target.value }))
                  }
                  className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm"
                  placeholder="From"
                />
                <input
                  type="date"
                  value={filters.dateTo}
                  onChange={(e) =>
                    setFilters((prev) => ({ ...prev, dateTo: e.target.value }))
                  }
                  className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm"
                  placeholder="To"
                />
              </div>
            </div>

            {/* Crime Types */}
            <div className="mb-6">
              <label className="block text-sm font-semibold text-slate-900 mb-3">
                Crime Types
              </label>
              <div className="space-y-2">
                {CRIME_TYPES.map((type) => (
                  <label
                    key={type}
                    className="flex items-center gap-2 cursor-pointer"
                  >
                    <input
                      type="checkbox"
                      checked={filters.crimeTypes.includes(type)}
                      onChange={() => handleCrimeTypeToggle(type)}
                      className="w-4 h-4 rounded border-slate-300"
                    />
                    <span className="text-sm text-slate-700 capitalize">
                      {type.replace("_", " ")}
                    </span>
                  </label>
                ))}
              </div>
            </div>

            {/* Jurisdictions */}
            <div className="mb-6">
              <label className="block text-sm font-semibold text-slate-900 mb-3">
                Provinces/Territories
              </label>
              <div className="space-y-2 max-h-48 overflow-y-auto">
                {JURISDICTIONS.map((jurisdiction) => (
                  <label
                    key={jurisdiction}
                    className="flex items-center gap-2 cursor-pointer"
                  >
                    <input
                      type="checkbox"
                      checked={filters.jurisdictions.includes(jurisdiction)}
                      onChange={() =>
                        handleJurisdictionToggle(jurisdiction)
                      }
                      className="w-4 h-4 rounded border-slate-300"
                    />
                    <span className="text-sm text-slate-700">
                      {jurisdiction}
                    </span>
                  </label>
                ))}
              </div>
            </div>

            {/* Info Box */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <p className="text-xs text-slate-700">
                <strong>Tip:</strong> Click on incidents on the map to see
                related laws and news coverage.
              </p>
            </div>
          </div>
        </div>

        {/* Map Area */}
        <div className="flex-1 bg-slate-100">
          <MapComponent filters={filters} />
        </div>
      </div>
    </div>
  );
}
