#!/bin/bash
set -euo pipefail

# This script builds the FINAL distributable archive.
# It does NOT package the working directory.
# It packages ONLY the canonical final archive plus documentation.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FINAL_ARCHIVE="$ROOT/dist/JUDGE_ATLAS-main-final.zip"
DISTRIBUTABLE_NAME="JUDGE_ATLAS-main-final-distributable.zip"
DISTRIBUTABLE_PATH="$ROOT/dist/$DISTRIBUTABLE_NAME"
TEMP_DIR=$(mktemp -d)

trap "rm -rf $TEMP_DIR" EXIT

# Verify canonical archive exists
if [ ! -f "$FINAL_ARCHIVE" ]; then
    echo "ERROR: Canonical archive not found: $FINAL_ARCHIVE"
    echo "Run: python3 scripts/build_release_archive.py"
    exit 1
fi

# Create staging directory
mkdir -p "$TEMP_DIR/JUDGE_ATLAS-main-final-release"

# Copy ONLY:
# 1. The final canonical archive
# 2. The handoff document
# 3. The repair summary

cp "$FINAL_ARCHIVE" "$TEMP_DIR/JUDGE_ATLAS-main-final-release/"
cp "$ROOT/FINAL_RELEASE_HANDOFF.md" "$TEMP_DIR/JUDGE_ATLAS-main-final-release/"
cp "$ROOT/REPAIR_EXECUTION_SUMMARY.md" "$TEMP_DIR/JUDGE_ATLAS-main-final-release/" 2>/dev/null || true

# Create distributable archive
cd "$TEMP_DIR"
zip -q -r "$DISTRIBUTABLE_PATH" "JUDGE_ATLAS-main-final-release/"

echo "✅ Distributable archive built:"
echo "  Path: $DISTRIBUTABLE_PATH"
ls -lh "$DISTRIBUTABLE_PATH"
echo ""
echo "Contents:"
unzip -l "$DISTRIBUTABLE_PATH" | head -20
echo ""
echo "Hash:"
shasum -a 256 "$DISTRIBUTABLE_PATH"
