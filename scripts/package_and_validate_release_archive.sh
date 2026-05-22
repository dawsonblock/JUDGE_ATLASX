#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "${TMP_DIR}"' EXIT INT TERM

ARCHIVE_VALIDATION_LOG="${ROOT_DIR}/artifacts/proof/current/archive_validation.log"
ARCHIVE_VALIDATION_MD="${ROOT_DIR}/artifacts/proof/current/archive_validation.md"

ARCHIVE_PATH="/tmp/JUDGE_ATLAS-main-final.zip"
PACKAGE_ROOT_NAME="JUDGE_ATLAS-main"
SKIP_RELEASE_GATE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --archive-path)
      ARCHIVE_PATH="$2"
      shift 2
      ;;
    --package-root-name)
      PACKAGE_ROOT_NAME="$2"
      shift 2
      ;;
    --skip-release-gate)
      SKIP_RELEASE_GATE=true
      shift
      ;;
    *)
      echo "ERROR: unknown argument: $1"
      exit 2
      ;;
  esac
done

log() {
  echo "[release_package] $*"
}

cd "${ROOT_DIR}"

if [[ "${SKIP_RELEASE_GATE}" != "true" ]]; then
  log "Running release proof gate"
  make release-proof-local
fi

log "Validating local proof freshness"
python scripts/check_proof_freshness.py
python scripts/check_proof_freshness.py --strict-extra-files

log "Validating local proof integrity"
python scripts/check_proof_consistency.py
python scripts/check_single_proof_authority.py --root .
python scripts/check_required_proof_logs.py --root .
python scripts/check_no_local_paths_in_release_proof.py --root .

log "Building archive at ${ARCHIVE_PATH}"
python scripts/build_release_archive.py \
  --output "${ARCHIVE_PATH}" \
  --root-name "${PACKAGE_ROOT_NAME}"

archive_sha256() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
    return
  fi
  shasum -a 256 "$1" | awk '{print $1}'
}

ARCHIVE_BASENAME="$(basename "${ARCHIVE_PATH}")"
ARCHIVE_SHA256="$(archive_sha256 "${ARCHIVE_PATH}")"
log "Built archive filename=${ARCHIVE_BASENAME} sha256=${ARCHIVE_SHA256}"

log "Running archive validation"
bash scripts/validate_archive_proof.sh "${ARCHIVE_PATH}"

python scripts/validate_final_zip.py "${ARCHIVE_PATH}" | tee -a "${ARCHIVE_VALIDATION_LOG}"
python scripts/verify_archive_proof_freshness.py --archive "${ARCHIVE_PATH}" | tee -a "${ARCHIVE_VALIDATION_LOG}"

python - <<'PY'
import json
import re
from pathlib import Path

root = Path('.').resolve()
log_path = root / 'artifacts/proof/current/archive_validation.log'
md_path = root / 'artifacts/proof/current/archive_validation.md'

patterns = (
  re.compile(r"/Users/[^\s\"'`]+"),
  re.compile(r"/home/[^\s\"'`]+"),
  re.compile(r"/private/[^\s\"'`]+"),
  re.compile(r"[A-Za-z]:\\[^\s\"'`]+"),
)

repo_prefix = str(root).replace('\\', '/')

def redact_text(text: str) -> str:
  normalized = text.replace('\\', '/')
  redacted = normalized.replace(repo_prefix, '[REDACTED_LOCAL_PATH]')
  for pattern in patterns:
    redacted = pattern.sub('[REDACTED_LOCAL_PATH]', redacted)
  return redacted

def redact_file(path: Path) -> None:
  if not path.exists() or not path.is_file():
    return

  if path.suffix.lower() == '.json':
    try:
      parsed = json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
      parsed = None
    if parsed is not None:
      serialized = json.dumps(parsed, indent=2)
      path.write_text(redact_text(serialized) + '\n', encoding='utf-8')
      return

  text = path.read_text(encoding='utf-8', errors='ignore')
  redacted = redact_text(text)
  if redacted != text:
    path.write_text(redacted, encoding='utf-8')

redact_file(log_path)
redact_file(md_path)
PY

EXTRACT_DIR="${TMP_DIR}/extracted"
mkdir -p "${EXTRACT_DIR}"
unzip -q "${ARCHIVE_PATH}" -d "${EXTRACT_DIR}"

EXTRACTED_ROOT="$(python scripts/archive_validation_paths.py --extract-dir "${EXTRACT_DIR}")"
log "Resolved extracted root: ${EXTRACTED_ROOT}"

PYTHON_BIN="${EXTRACTED_ROOT}/backend/.venv/bin/python"
if [[ ! -x "${PYTHON_BIN}" ]]; then
  PYTHON_BIN="python3"
fi

(
  cd "${EXTRACTED_ROOT}"
  python scripts/check_path_hygiene.py --root .
  python scripts/check_no_generated_files.py --root .
  "${PYTHON_BIN}" scripts/check_false_claims.py
  "${PYTHON_BIN}" scripts/check_truth_claims.py
  "${PYTHON_BIN}" scripts/check_proof_freshness.py
  "${PYTHON_BIN}" scripts/check_proof_freshness.py --strict-extra-files
  "${PYTHON_BIN}" scripts/check_source_registry_docs.py
  "${PYTHON_BIN}" scripts/check_proof_consistency.py
  "${PYTHON_BIN}" scripts/check_single_proof_authority.py
  "${PYTHON_BIN}" scripts/check_required_proof_logs.py --root .
  "${PYTHON_BIN}" scripts/check_no_local_paths_in_release_proof.py --root .
  bash scripts/check_no_pyc.sh
  "${PYTHON_BIN}" scripts/check_external_boundaries.py
  "${PYTHON_BIN}" backend/scripts/check_repo_boundaries.py
  "${PYTHON_BIN}" backend/scripts/check_no_direct_ingestion_network_clients.py
  "${PYTHON_BIN}" scripts/validate_workflows.py
  "${PYTHON_BIN}" scripts/verify_status_consistency.py --root .
  "${PYTHON_BIN}" -m compileall -q backend/app scripts
)

log "Verifying proof hash synchronization"
python - <<'PY'
import json
import re
from pathlib import Path

root = Path('.')
rg = json.loads((root / 'artifacts/proof/current/release_gate.json').read_text(encoding='utf-8'))
cp = (root / 'artifacts/proof/current/CURRENT_PROOF.md').read_text(encoding='utf-8')
pf = (root / 'artifacts/proof/current/proof_freshness.log').read_text(encoding='utf-8')
av = (root / 'artifacts/proof/current/archive_validation.log').read_text(encoding='utf-8')

release_hash = rg.get('proof_input_tree_hash', '')
cp_match = re.search(r"- proof_input_tree_hash: ([0-9a-f]{64})", cp)
pf_match = re.search(r"proof_input_tree_hash=([0-9a-f]{64})", pf)
av_release_match = re.search(r"release_gate\.json proof_input_tree_hash=([0-9a-f]{64})", av)
av_actual_match = re.search(r"proof_freshness actual_hash=([0-9a-f]{64})", av)

if not av_release_match:
  av_release_match = re.search(r"proof_input_tree_hash=([0-9a-f]{64})", av)
if not av_actual_match:
  av_actual_match = re.search(r"proof_freshness.*actual_hash=([0-9a-f]{64})", av)

values = {
    'release_gate.json': release_hash,
    'CURRENT_PROOF.md': cp_match.group(1) if cp_match else '',
    'proof_freshness.log': pf_match.group(1) if pf_match else '',
    'archive_validation.log release_hash': av_release_match.group(1) if av_release_match else '',
    'archive_validation.log actual_hash': av_actual_match.group(1) if av_actual_match else '',
}

missing = [name for name, value in values.items() if not value]
if missing:
    raise SystemExit('Missing hash values in: ' + ', '.join(missing))

unique = set(values.values())
if len(unique) != 1:
    lines = ['Hash mismatch across proof artifacts:']
    for name, value in values.items():
        lines.append(f'  {name}: {value}')
    raise SystemExit('\n'.join(lines))

print(f"PASS: synchronized proof_input_tree_hash={release_hash}")
PY

log "PASS: release package and proof validation complete"
log "AUTHORITATIVE_RELEASE_ARCHIVE=${ARCHIVE_PATH}"
log "AUTHORITATIVE_RELEASE_ARCHIVE_SHA256=${ARCHIVE_SHA256}"
log "Ship the validated archive at ${ARCHIVE_PATH} exactly; do not re-zip the working tree."
