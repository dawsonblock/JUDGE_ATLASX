# RELEASE_READINESS

This document tracks release-readiness references for the active alpha surface.

## Artifact Classes

- Source snapshot archive: a raw tree export used for development exchange and inspection. It is not a distributable release artifact.
- Authoritative release archive: a zip produced only by `scripts/package_and_validate_release_archive.sh` and validated by the release/archive proof checks.

Only the authoritative release archive may be distributed as an alpha release artifact.

## Canonical References

- STATUS.md
- artifacts/proof/current/CURRENT_PROOF.md
- artifacts/proof/current/release_readiness.md

## Policy

Release readiness is determined by artifacts/proof/current/release_readiness.md and the machine-readable gate output in artifacts/proof/current/release_gate.json.
Production ready: false.

The final distributable must be the exact archive built by:

python scripts/build_release_archive.py

inside the package-and-validate flow, followed by:

- scripts/validate_release_archive.py
- scripts/check_release_surface.py
- scripts/validate_final_zip.py
- scripts/verify_archive_proof_freshness.py

Manual re-zipping of the workspace is not a supported release path.
