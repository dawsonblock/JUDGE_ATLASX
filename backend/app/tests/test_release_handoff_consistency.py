from __future__ import annotations

import importlib.util
import hashlib
import sys
from pathlib import Path


def _load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_handoff(path: Path, archive_rel: str, sha256: str) -> None:
    path.write_text(
        "\n".join(
            [
                "# Final Release Handoff",
                "",
                "- Path: " + archive_rel,
                "- SHA-256: " + sha256,
                "",
            ]
        ),
        encoding="utf-8",
    )


def _module():
    return _load_module(
        "check_release_handoff_consistency_module",
        Path(__file__).resolve().parents[3]
        / "scripts"
        / "check_release_handoff_consistency.py",
    )


def test_handoff_consistency_passes(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "dist").mkdir(parents=True, exist_ok=True)
    archive = repo_root / "dist" / "JUDGE_ATLAS-main-final.zip"
    archive.write_bytes(b"archive-bytes")
    handoff = repo_root / "FINAL_RELEASE_HANDOFF.md"
    _write_handoff(
        handoff,
        "dist/JUDGE_ATLAS-main-final.zip",
        _sha256(archive),
    )

    module = _module()
    ok, errors = module.validate_handoff(repo_root, archive, handoff)
    assert ok
    assert not errors


def test_handoff_consistency_fails_on_sha_mismatch(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "dist").mkdir(parents=True, exist_ok=True)
    archive = repo_root / "dist" / "JUDGE_ATLAS-main-final.zip"
    archive.write_bytes(b"archive-bytes")
    handoff = repo_root / "FINAL_RELEASE_HANDOFF.md"
    _write_handoff(
        handoff,
        "dist/JUDGE_ATLAS-main-final.zip",
        "0" * 64,
    )

    module = _module()
    ok, errors = module.validate_handoff(repo_root, archive, handoff)
    assert not ok
    assert any(err.startswith("sha256_mismatch:") for err in errors)


def test_handoff_consistency_fails_on_path_mismatch(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "dist").mkdir(parents=True, exist_ok=True)
    archive = repo_root / "dist" / "JUDGE_ATLAS-main-final.zip"
    archive.write_bytes(b"archive-bytes")
    handoff = repo_root / "FINAL_RELEASE_HANDOFF.md"
    _write_handoff(handoff, "dist/other.zip", _sha256(archive))

    module = _module()
    ok, errors = module.validate_handoff(repo_root, archive, handoff)
    assert not ok
    assert any(err.startswith("archive_path_mismatch:") for err in errors)


def test_handoff_consistency_fails_on_missing_claims(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "dist").mkdir(parents=True, exist_ok=True)
    archive = repo_root / "dist" / "JUDGE_ATLAS-main-final.zip"
    archive.write_bytes(b"archive-bytes")
    handoff = repo_root / "FINAL_RELEASE_HANDOFF.md"
    handoff.write_text("# Final Release Handoff\n", encoding="utf-8")

    module = _module()
    ok, errors = module.validate_handoff(repo_root, archive, handoff)
    assert not ok
    assert "missing_claimed_path" in errors
    assert "missing_claimed_sha256" in errors
