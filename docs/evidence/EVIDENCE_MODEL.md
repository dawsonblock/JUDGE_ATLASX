# Evidence Model

Canonical evidence model for alpha runtime.

## Authority Rule

Evidence snapshots are authoritative. AI and memory outputs are derivative only.

## Snapshot Requirements

- stored in evidence root outside repository
- content-addressed by SHA256
- stored hash must match computed hash
- snapshot blobs are immutable after write

## Publication Rule

No public record may be shown without:

- approved review state
- at least one linked evidence snapshot

## Validation Commands

- `python3 scripts/verify_evidence_store.py`
- `python3 scripts/verify_snapshot_hashes.py`
- `python3 scripts/find_orphan_snapshots.py`
