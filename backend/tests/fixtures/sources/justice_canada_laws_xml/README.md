# Fixture: justice_canada_laws_xml

Deterministic replay fixture for the Justice Canada Laws XML ingestion adapter.

## Files

| File | Description |
|------|-------------|
| `raw_input.xml` | Minimal valid XML sample from the Justice Canada laws feed |
| `expected_record.json` | Expected parsed record structure |
| `expected_evidence_hash.txt` | SHA-256 of the raw_input.xml content |
| `expected_review_status.txt` | `pending_review` — always |
| `expected_public_visibility.txt` | `hidden` — unreviewed records are not public |

## Usage

```python
from pathlib import Path
import json, hashlib

fixture_dir = Path("backend/tests/fixtures/sources/justice_canada_laws_xml")
raw = (fixture_dir / "raw_input.xml").read_bytes()
expected_hash = (fixture_dir / "expected_evidence_hash.txt").read_text().strip()
assert hashlib.sha256(raw).hexdigest() == expected_hash
```

## Network-off mode

Set `JTA_TEST_NO_NETWORK=true` to force ingestion to use fixtures only.
The adapter must raise `NetworkNotAllowedError` if a live request is attempted
in this mode.
