import { describe, expect, it } from "vitest";

import {
  publicEntityDetailSchema,
  publicMapMarkersResponseSchema,
} from "@/lib/schemas";

describe("public map and detail contract", () => {
  it("accepts reviewed public map markers", () => {
    const payload = {
      items: [
        { entity_id: "event-1", lat: 52.13, lon: -106.67, label: "Reviewed" },
      ],
    };
    expect(publicMapMarkersResponseSchema.safeParse(payload).success).toBe(true);
  });

  it("accepts public entity detail shape for verified records", () => {
    const detail = {
      entity_id: "event-1",
      review_status: "verified_court_record",
      public_visibility: true,
      source_key: "justice_canada_laws_xml",
      summary: "Evidence-backed summary",
    };
    expect(publicEntityDetailSchema.safeParse(detail).success).toBe(true);
  });
});
