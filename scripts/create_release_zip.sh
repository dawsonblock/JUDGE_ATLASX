#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEFAULT_OUTPUT="agent_eval_skills_merged_clean-pruned-smoke.zip"
DEFAULT_ROOT_NAME="JUDGE_ATLASX-main"

OUTPUT="${DEFAULT_OUTPUT}"
ROOT_NAME="${DEFAULT_ROOT_NAME}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output)
      OUTPUT="$2"
      shift 2
      ;;
    --root-name)
      ROOT_NAME="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1"
      exit 2
      ;;
  esac
done

if [[ "${OUTPUT}" = /* ]]; then
  OUT_PATH="${OUTPUT}"
else
  OUT_PATH="${ROOT_DIR}/${OUTPUT}"
fi

echo "[create_release_zip] Building archive: ${OUT_PATH}"
python3 "${ROOT_DIR}/scripts/build_release_archive.py" \
  --output "${OUT_PATH}" \
  --root-name "${ROOT_NAME}"

echo "[create_release_zip] Running release zip validation"
python3 "${ROOT_DIR}/scripts/validate_release_zip.py" --zip "${OUT_PATH}"

echo "[create_release_zip] Running release surface validation"
python3 "${ROOT_DIR}/scripts/check_release_surface.py" --archive "${OUT_PATH}"

echo "[create_release_zip] Archive is clean and validated: ${OUT_PATH}"
