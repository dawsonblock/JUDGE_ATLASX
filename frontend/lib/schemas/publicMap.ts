import { z } from "zod";

export const CANONICAL_REVIEW_STATUSES = [
  "verified_court_record",
  "official_police_open_data_report",
  "official_statistics_aggregate",
  "corrected",
  "pending_review",
  "news_only_context",
  "disputed",
  "rejected",
  "removed_from_public",
] as const;

export type CanonicalReviewStatus = (typeof CANONICAL_REVIEW_STATUSES)[number];

export const publicMapMarkerSchema = z.object({
  entity_id: z.string(),
  lat: z.number(),
  lon: z.number(),
  label: z.string().optional(),
  review_status: z.enum(CANONICAL_REVIEW_STATUSES).optional(),
  public_visibility: z.boolean().optional(),
  source_quality: z.string().optional(),
  is_context_only: z.boolean().optional(),
  evidence_type: z.string().optional(),
});

export const publicMapMarkersResponseSchema = z.object({
  items: z.array(publicMapMarkerSchema),
});

export type PublicMapMarker = z.infer<typeof publicMapMarkerSchema>;
export type PublicMapMarkersResponse = z.infer<typeof publicMapMarkersResponseSchema>;
