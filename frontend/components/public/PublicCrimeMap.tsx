"use client";

import { useEffect, useRef, useState } from "react";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { useRouter } from "next/navigation";

interface Filters {
  dateFrom: string;
  dateTo: string;
  crimeTypes: string[];
  jurisdictions: string[];
}

interface IncidentFeature {
  id: string;
  title: string;
  type: string;
  lat: number;
  lng: number;
  location: string;
  date: string;
  jurisdiction: string;
  evidence_count?: number;
}

// Helper function to validate coordinates
function isValidCoordinate(lat: number, lng: number): boolean {
  return (
    typeof lat === "number" &&
    typeof lng === "number" &&
    lat >= -90 &&
    lat <= 90 &&
    lng >= -180 &&
    lng <= 180 &&
    !isNaN(lat) &&
    !isNaN(lng)
  );
}

export default function PublicCrimeMap({ filters }: { filters: Filters }) {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);
  const [incidents, setIncidents] = useState<IncidentFeature[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedIncident, setSelectedIncident] = useState<IncidentFeature | null>(null);
  const router = useRouter();

  // Initialize map
  useEffect(() => {
    if (!mapContainer.current) return;

    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style: "https://tiles.openstreetmap.se/bright/style.json",
      center: [-95, 56], // Center of Canada
      zoom: 3.5,
    });

    return () => {
      map.current?.remove();
    };
  }, []);

  // Fetch incidents when filters change
  useEffect(() => {
    fetchIncidents();
  }, [filters]);

  const fetchIncidents = async () => {
    if (!map.current) return;

    setIsLoading(true);
    try {
      const bounds = map.current.getBounds();
      const params = new URLSearchParams({
        bbox_min_lat: bounds.getSouth().toString(),
        bbox_min_lng: bounds.getWest().toString(),
        bbox_max_lat: bounds.getNorth().toString(),
        bbox_max_lng: bounds.getEast().toString(),
      });

      if (filters.dateFrom) params.append("date_from", filters.dateFrom);
      if (filters.dateTo) params.append("date_to", filters.dateTo);
      filters.crimeTypes.forEach((type) =>
        params.append("crime_types", type)
      );
      filters.jurisdictions.forEach((jurisdiction) =>
        params.append("jurisdictions", jurisdiction)
      );

      const response = await fetch(
        `/api/public/map/incidents?${params.toString()}`
      );

      if (!response.ok) throw new Error("Failed to fetch incidents");

      const data = await response.json();
      // Filter to only incidents with valid coordinates
      const features: IncidentFeature[] = (data.incidents || []).filter(
        (incident: IncidentFeature) =>
          isValidCoordinate(incident.lat, incident.lng)
      );

      console.log(
        "[v0] Loaded",
        features.length,
        "valid incidents (filtered from",
        data.incidents?.length || 0,
        ")"
      );
      setIncidents(features);

      // Add GeoJSON source to map
      if (map.current) {
        if (map.current.getSource("incidents")) {
          map.current.removeLayer("incidents-cluster");
          map.current.removeLayer("incidents-point");
          map.current.removeSource("incidents");
        }

        map.current.addSource("incidents", {
          type: "geojson",
          data: {
            type: "FeatureCollection",
            features: features.map((f) => ({
              type: "Feature",
              geometry: {
                type: "Point",
                coordinates: [f.lng, f.lat],
              },
              properties: {
                id: f.id,
                title: f.title,
                type: f.type,
              },
            })),
          },
          cluster: true,
          clusterMaxZoom: 14,
          clusterRadius: 50,
        });

        // Cluster layer
        map.current.addLayer({
          id: "incidents-cluster",
          type: "circle",
          source: "incidents",
          filter: ["has", "point_count"],
          paint: {
            "circle-color": "#3b82f6",
            "circle-radius": [
              "step",
              ["get", "point_count"],
              20,
              5,
              30,
              10,
              40,
            ],
            "circle-opacity": 0.8,
          },
        });

        // Individual point layer
        map.current.addLayer({
          id: "incidents-point",
          type: "circle",
          source: "incidents",
          filter: ["!", ["has", "point_count"]],
          paint: {
            "circle-color": "#ef4444",
            "circle-radius": 6,
            "circle-opacity": 0.8,
          },
        });

        // Click handlers
        map.current.on("click", "incidents-point", (e) => {
          const properties = e.features?.[0]?.properties;
          if (properties?.id) {
            router.push(`/public/incident/${properties.id}`);
          }
        });

        map.current.on("mouseenter", "incidents-point", () => {
          map.current!.getCanvas().style.cursor = "pointer";
        });

        map.current.on("mouseleave", "incidents-point", () => {
          map.current!.getCanvas().style.cursor = "";
        });
      }
    } catch (error) {
      console.error("[v0] Error fetching incidents:", error);
    } finally {
      setIsLoading(false);
    }
  };

  // Refetch on map move
  useEffect(() => {
    if (!map.current) return;

    const handleMove = () => {
      // Debounce
      const timeout = setTimeout(fetchIncidents, 500);
      return () => clearTimeout(timeout);
    };

    map.current.on("moveend", handleMove);
    return () => {
      map.current?.off("moveend", handleMove);
    };
  }, []);

  return (
    <div className="relative w-full h-full">
      <div ref={mapContainer} className="w-full h-full" />

      {isLoading && (
        <div className="absolute top-4 left-4 bg-white px-4 py-2 rounded-lg shadow">
          <p className="text-sm text-slate-600">Loading incidents...</p>
        </div>
      )}

      <div className="absolute bottom-4 left-4 bg-white px-4 py-2 rounded-lg shadow text-sm text-slate-600">
        {incidents.length} incident{incidents.length !== 1 ? "s" : ""} visible
      </div>
    </div>
  );
}
