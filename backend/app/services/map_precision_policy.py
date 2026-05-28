"""Map precision policy for public platform.

Controls what coordinate precision is exposed on the public map for each
incident, based on:
  - The source's declared ``precision_level``
  - The incident's legal risk level
  - The crime type (some types require extra privacy protection)

Precision levels (coarsest to finest):
  ``country``         – Country centroid only
  ``province``        – Province centroid
  ``city_centroid``   – City/municipality centroid (default for public)
  ``neighbourhood``   – ~500m radius jitter applied
  ``street_block``    – Block-level (100m jitter)
  ``exact``           – Exact coordinates (never exposed publicly)

Usage
-----
    from app.services.map_precision_policy import MapPrecisionPolicy
    coords = MapPrecisionPolicy.apply(lat=52.1332, lng=-106.6700, source=src, event=ev)
"""

from __future__ import annotations

import logging
import random
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Jitter amounts in degrees for each precision level
JITTER_DEGREES: dict[str, float] = {
    "exact": 0.0,
    "street_block": 0.001,       # ~100 m
    "neighbourhood": 0.005,       # ~500 m
    "city_centroid": 0.0,         # replaced with city centroid lookup
    "province": 0.0,              # replaced with province centroid
    "country": 0.0,               # replaced with country centroid
}

# Province centroids (lat, lng) for Saskatchewan and surrounding provinces
PROVINCE_CENTROIDS: dict[str, tuple[float, float]] = {
    "SK": (54.5353, -105.3427),
    "AB": (55.0000, -115.0000),
    "MB": (56.4153, -98.7394),
    "BC": (53.7267, -127.6476),
    "ON": (51.2538, -85.3232),
    "QC": (53.0000, -71.8282),
}

# City centroids for major Saskatchewan cities
CITY_CENTROIDS: dict[str, tuple[float, float]] = {
    "Saskatoon": (52.1332, -106.6700),
    "Regina": (50.4452, -104.6189),
    "Prince Albert": (53.2033, -105.7531),
    "Moose Jaw": (50.3934, -105.5543),
    "Swift Current": (50.2854, -107.7977),
}

# Crime types that require city_centroid or coarser precision
COARSE_PRECISION_CRIME_TYPES: set[str] = {
    "sexual_assault",
    "sexual_offence",
    "domestic_violence",
    "stalking",
    "child_exploitation",
    "human_trafficking",
    "witness_intimidation",
}


@dataclass
class PublicCoords:
    """Coordinates safe to expose on the public map."""

    lat: float
    lng: float
    precision_level: str  # What precision was applied
    is_jittered: bool
    note: str  # Human-readable explanation of precision applied


class MapPrecisionPolicy:
    """Apply coordinate precision rules for public map display."""

    @classmethod
    def apply(
        cls,
        lat: float,
        lng: float,
        source_precision: str,
        crime_type: str = "",
        legal_risk_level: str = "low",
        jurisdiction: str = "SK",
        city: str | None = None,
    ) -> PublicCoords:
        """Apply the least precise of: source precision, crime type policy,
        and legal risk level policy.

        Args:
            lat: Raw latitude from source.
            lng: Raw longitude from source.
            source_precision: The precision_level declared by the source.
            crime_type: Normalised crime type string.
            legal_risk_level: Output from LegalRiskLabeller.
            jurisdiction: Province code (e.g. "SK").
            city: City name for city_centroid lookup.

        Returns:
            PublicCoords with safe coordinates and metadata.
        """
        effective_precision = cls._compute_effective_precision(
            source_precision=source_precision,
            crime_type=crime_type,
            legal_risk_level=legal_risk_level,
        )

        return cls._apply_precision(
            lat=lat,
            lng=lng,
            precision=effective_precision,
            jurisdiction=jurisdiction,
            city=city,
        )

    @classmethod
    def _compute_effective_precision(
        cls,
        source_precision: str,
        crime_type: str,
        legal_risk_level: str,
    ) -> str:
        """Return the coarsest required precision from all applicable policies."""
        # Start with source's declared precision
        effective = source_precision or "city_centroid"

        # High/unknown risk → coarsen to city_centroid at minimum
        if legal_risk_level in ("high", "unknown"):
            effective = cls._coarsen(effective, "city_centroid")

        # Sensitive crime types → coarsen to city_centroid at minimum
        normalised_type = crime_type.lower().replace(" ", "_")
        if normalised_type in COARSE_PRECISION_CRIME_TYPES:
            effective = cls._coarsen(effective, "city_centroid")

        # Never expose exact coordinates publicly
        if effective == "exact":
            effective = "street_block"

        return effective

    @classmethod
    def _apply_precision(
        cls,
        lat: float,
        lng: float,
        precision: str,
        jurisdiction: str,
        city: str | None,
    ) -> PublicCoords:
        """Apply coordinate transformation for the given precision level."""
        if precision == "country":
            return PublicCoords(
                lat=56.1304, lng=-106.3468,
                precision_level=precision, is_jittered=False,
                note="Country centroid (Canada)",
            )

        if precision == "province":
            centroid = PROVINCE_CENTROIDS.get(jurisdiction, PROVINCE_CENTROIDS["SK"])
            return PublicCoords(
                lat=centroid[0], lng=centroid[1],
                precision_level=precision, is_jittered=False,
                note=f"Province centroid ({jurisdiction})",
            )

        if precision == "city_centroid":
            if city and city in CITY_CENTROIDS:
                centroid = CITY_CENTROIDS[city]
                return PublicCoords(
                    lat=centroid[0], lng=centroid[1],
                    precision_level=precision, is_jittered=False,
                    note=f"City centroid ({city})",
                )
            # Fall back to jittered neighbourhood precision
            precision = "neighbourhood"

        jitter = JITTER_DEGREES.get(precision, 0.005)
        jittered_lat = lat + random.uniform(-jitter, jitter)
        jittered_lng = lng + random.uniform(-jitter, jitter)

        return PublicCoords(
            lat=round(jittered_lat, 5),
            lng=round(jittered_lng, 5),
            precision_level=precision,
            is_jittered=jitter > 0,
            note=f"Jittered to {precision} precision (±{jitter:.3f}°)",
        )

    @staticmethod
    def _coarsen(current: str, minimum_coarse: str) -> str:
        """Return the coarser of two precision levels."""
        order = {
            "exact": 6,
            "street_block": 5,
            "neighbourhood": 4,
            "city_centroid": 3,
            "province": 2,
            "country": 1,
        }
        current_rank = order.get(current, 3)
        minimum_rank = order.get(minimum_coarse, 3)
        if current_rank <= minimum_rank:
            return current
        return minimum_coarse
