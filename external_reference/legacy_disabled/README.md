<!-- markdownlint-disable -->

# legacy_disabled/

This directory holds source files that are **quarantined from runtime loading**.

Files here are preserved for historical reference and to maintain git blame / audit trails,
but **must not** be imported by any production code path.

## Contents

| Directory                | Description                                                                                                       |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| `us_ingestion_adapters/` | US-only data adapters with `NOT_RUNTIME: bool = True` sentinels; not part of the Canada-first production pipeline |

## Rules

1. **Never import** any file in this directory from `backend/app/` unless explicitly gated by a `JTA_ENABLE_*` environment variable.
2. **Never add** files here that do not have a `NOT_RUNTIME: bool = True` sentinel in the original source location.
3. **Files are read-only reference copies.** The canonical source for each file remains in its original location with the `NOT_RUNTIME` sentinel. The copy here is for archival and documentation purposes.
4. If a file is later promoted back to active use (e.g., a Canadian equivalent replaces it), remove it from this directory and remove the `NOT_RUNTIME` sentinel from the original.

## Adding a New File

```
# 1. Add NOT_RUNTIME sentinel to original
echo "NOT_RUNTIME: bool = True" >> backend/app/ingestion/your_file.py

# 2. Copy to this directory
cp backend/app/ingestion/your_file.py legacy_disabled/category/your_file.py

# 3. Add header comment to the copy (see us_ingestion_adapters/ for example)
```
