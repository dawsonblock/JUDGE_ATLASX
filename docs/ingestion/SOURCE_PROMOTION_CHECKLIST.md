# Source Promotion Checklist

No source moves from `enable_ready` to `runnable_now` without completing this checklist.

Complete every item and record the operator name and date in the source's `admin_notes` field.

---

## Registry entry

- [ ] Source registry entry exists (`source_key` is unique, non-empty)
- [ ] Jurisdiction is set (`jurisdiction` field populated)
- [ ] Source type is set (`source_type` field populated)
- [ ] `lifecycle_state` is currently `enable_ready`
- [ ] `operator_next_step` describes what this checklist completion does

## Access and legal notes

- [ ] Access / legal notes documented in `notes` or `admin_notes`
- [ ] `terms_url` populated (or explicitly set to `"not_applicable"` with reason in notes)
- [ ] `terms_verified` set to the ISO date terms were last confirmed
- [ ] `authentication_required` is accurate (True/False)
- [ ] If `authentication_required=True`: credentials note present in `admin_notes`
- [ ] `allowed_domains` populated (prevents SSRF attacks)

## Adapter

- [ ] Adapter implemented in `backend/app/ingestion/source_adapters/`
- [ ] Adapter includes `parser_version` and `schema_version`
- [ ] Adapter does not write to DB directly — uses pipeline
- [ ] Adapter respects `JTA_TEST_NO_NETWORK=true` (raises if live network attempted)

## Dry-run

- [ ] Dry-run supported: `POST /admin/ingestion/sources/{id}/dry-run` returns no blocking issues
- [ ] Dry-run result shows `safe_to_enable: true`
- [ ] No `records_would_bypass_review: true`

## Fixture replay

- [ ] Fixture directory exists under `backend/tests/fixtures/sources/{source_key}/`
- [ ] `raw_input.*` file is present and deterministic
- [ ] `expected_record.json` matches parser output
- [ ] `expected_evidence_hash.txt` matches SHA-256 of raw input
- [ ] `expected_review_status.txt` is `pending_review`
- [ ] `expected_public_visibility.txt` is `hidden`
- [ ] Network-off test passes: `JTA_TEST_NO_NETWORK=true pytest backend/tests/fixtures/...`

## Evidence and review

- [ ] Evidence snapshot created (hash stored in `SourceSnapshot`)
- [ ] Claims extracted as derivative records (not primary evidence)
- [ ] Public visibility defaults to `pending_review`
- [ ] Human reviewer identity requirements met (see `docs/review/REVIEWER_REQUIREMENTS.md`)

## Public API and review path

- [ ] Admin review path tested (record moves from `pending_review` → `approved`)
- [ ] Public API hides unreviewed records (verified via negative E2E path)
- [ ] Public API returns `evidence_snapshot_id` and `evidence_url` on approved records

## Documentation and proof

- [ ] Status docs regenerated: `python3 scripts/export_source_registry_status.py`
- [ ] Proof logs generated: `python3 scripts/generate_current_proof.py`
- [ ] `lifecycle_state` updated to `runnable_now` in source registry

---

## Completion record

| Field | Value |
|-------|-------|
| Source key | |
| Operator | |
| Date completed | |
| Dry-run run ID | |
| Evidence snapshot hash | |
| Notes | |
