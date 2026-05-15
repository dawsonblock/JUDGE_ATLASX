import { z } from "zod";

export const publicMapMarkerSchema = z.object({
  entity_id: z.string(),
  lat: z.number(),
  lon: z.number(),
  label: z.string().optional(),
  review_status: z.string().optional(),
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
