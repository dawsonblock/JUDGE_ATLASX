# Runbook: Releasing a Quarantined Ingestion Run

**Audience:** Senior Reviewer, Admin  
**Severity:** Medium — quarantined runs block new records from the public platform  
**Time to resolve:** 5–30 minutes depending on cause

---

## When This Runbook Applies

An ingestion run is quarantined when:
- The adapter declared a `parser_version` that does not match the active `SourceAdapterContract`
- The parsed records failed schema validation
- The run error rate exceeded the quarantine threshold (> 50 % failures)
- An operator manually quarantined the run via the admin UI

---

## Step 1: Identify the Run

1. Navigate to `/admin/quarantine` in the admin UI.
2. Find the run. Note:
   - `id` — the run ID (needed for API calls)
   - `quarantine_reason` — the specific reason
   - `pipeline_stage` — where in the pipeline it failed
   - `error_count` / `parsed_count` ratio

---

## Step 2: Diagnose the Cause

| Quarantine reason | Next action |
|---|---|
| `parser_version_mismatch` | See **Step 3a** |
| `schema_validation_failed` | See **Step 3b** |
| `high_error_rate` | See **Step 3c** |
| `manual_quarantine` | See **Step 3d** |

---

## Step 3a: Parser Version Mismatch

1. Check the adapter contract:
   ```
   GET /api/admin/sources/{source_key}
   ```
   Note the expected `parser_version`.

2. Check what version the adapter declared in the run:
   ```
   GET /api/admin/ingestion/{run_id}
   ```

3. If the adapter was updated intentionally:
   - Update the `SourceAdapterContract` via the admin source config page.
   - Then release the run (Step 4).

4. If the adapter was NOT intentionally updated:
   - Revert the adapter code change and re-run ingestion.
   - Do NOT release the quarantined run — discard it.

---

## Step 3b: Schema Validation Failure

1. Review the `error_count` and pipeline logs.
2. If the source changed its output format:
   - Update the adapter parser to handle the new format.
   - Bump `parser_version` in both the adapter and the `SourceAdapterContract`.
   - Re-run ingestion from scratch (do not release the quarantined run).
3. If it was a transient upstream issue (empty feed, malformed HTTP response):
   - Release the run (Step 4) — it will be retried.

---

## Step 3c: High Error Rate

1. Check if the source URL is still reachable:
   ```
   curl -I <source_base_url>
   ```
2. If the source is down: wait for recovery, then release (Step 4).
3. If the error rate is systematic: treat as Step 3b.

---

## Step 3d: Manual Quarantine

1. Read the `quarantine_reason` field — it should contain a note from the operator.
2. Resolve the noted issue.
3. Release (Step 4) once resolved.

---

## Step 4: Release the Run

Via admin UI:
1. Click the **Release** button next to the run in `/admin/quarantine`.

Via API (requires Senior Reviewer or Admin token):
```bash
curl -X POST \
  -H "Authorization: Bearer <token>" \
  https://<host>/api/admin/quarantine/<run_id>/release
```

Expected response:
```json
{
  "id": 42,
  "status": "pending",
  "pipeline_stage": null,
  "message": "Run released for retry"
}
```

---

## Step 5: Verify Recovery

1. Wait 2–5 minutes for the run to complete.
2. Navigate to `/admin/status` and confirm the source shows `healthy`.
3. Check that new records appear in the review queue.

---

## Escalation

If the issue persists after following this runbook, escalate to an Admin with
database access. Include:
- The run ID
- The quarantine reason
- Steps already taken
- Any relevant log excerpts (use `X-Request-ID` from the API response to grep logs)
