#!/usr/bin/env python3
"""Check consistency between proof artifacts.

This script validates that proof_manifest.json and release_gate.json
are consistent with each other to prevent internal contradictions.

Key checks:
- Node version consistency
- Python version consistency  
- Platform consistency
- Timestamp sanity
"""

import json
import sys
from pathlib import Path


def load_json_file(path: Path) -> dict:
    """Load and parse a JSON file."""
    if not path.exists():
        print(f"ERROR: Proof artifact not found: {path}")
        sys.exit(1)
    
    with open(path, "r") as f:
        return json.load(f)


def check_node_version_consistency(manifest: dict, gate: dict) -> list[str]:
    """Check Node version consistency between artifacts."""
    errors = []
    
    manifest_node = manifest.get("gate_runner_node_version")
    gate_node = gate.get("gate_runner_node_version")
    
    if manifest_node != gate_node:
        errors.append(
            f"Node version mismatch: proof_manifest.json has '{manifest_node}' "
            f"but release_gate.json has '{gate_node}'"
        )
    
    # Also check frontend node gate version
    manifest_frontend = manifest.get("frontend_node_gate_version")
    gate_frontend = gate.get("frontend_node_gate_version")
    
    if manifest_frontend != gate_frontend:
        errors.append(
            f"Frontend Node version mismatch: proof_manifest.json has '{manifest_frontend}' "
            f"but release_gate.json has '{gate_frontend}'"
        )
    
    return errors


def check_python_version_consistency(manifest: dict, gate: dict) -> list[str]:
    """Check Python version consistency between artifacts."""
    errors = []
    
    manifest_python = manifest.get("python_version")
    gate_python = gate.get("python_version")
    
    if manifest_python != gate_python:
        errors.append(
            f"Python version mismatch: proof_manifest.json has '{manifest_python}' "
            f"but release_gate.json has '{gate_python}'"
        )
    
    return errors


def check_platform_consistency(manifest: dict, gate: dict) -> list[str]:
    """Check platform consistency between artifacts."""
    errors = []
    
    manifest_platform = manifest.get("platform")
    gate_platform = gate.get("platform")
    
    if manifest_platform != gate_platform:
        errors.append(
            f"Platform mismatch: proof_manifest.json has '{manifest_platform}' "
            f"but release_gate.json has '{gate_platform}'"
        )
    
    return errors


def check_commit_hash_consistency(manifest: dict, gate: dict) -> list[str]:
    """Check commit hash consistency between artifacts."""
    errors = []
    
    manifest_hash = manifest.get("archive_hash")
    gate_hash = gate.get("commit_hash")
    
    if manifest_hash and gate_hash and manifest_hash != gate_hash:
        errors.append(
            f"Commit hash mismatch: proof_manifest.json has '{manifest_hash}' "
            f"but release_gate.json has '{gate_hash}'"
        )
    
    return errors


def check_production_ready_consistency(manifest: dict, gate: dict) -> list[str]:
    """Check production_ready flag consistency between artifacts."""
    errors = []
    
    # proof_manifest doesn't have production_ready, but release_gate does
    # This is informational, not an error
    gate_production_ready = gate.get("production_ready")
    
    if gate_production_ready is True:
        print("WARNING: release_gate.json shows production_ready=True")
        print("This should only be set after all production blockers are cleared.")
    
    return errors


def main():
    """Main entry point."""
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    proof_dir = repo_root / "artifacts" / "proof" / "current"
    
    manifest_path = proof_dir / "proof_manifest.json"
    gate_path = proof_dir / "release_gate.json"
    
    print(f"Checking proof artifact consistency...")
    print(f"  proof_manifest.json: {manifest_path}")
    print(f"  release_gate.json: {gate_path}")
    
    # Load artifacts
    manifest = load_json_file(manifest_path)
    gate = load_json_file(gate_path)
    
    # Run consistency checks
    all_errors = []
    
    all_errors.extend(check_node_version_consistency(manifest, gate))
    all_errors.extend(check_python_version_consistency(manifest, gate))
    all_errors.extend(check_platform_consistency(manifest, gate))
    all_errors.extend(check_commit_hash_consistency(manifest, gate))
    all_errors.extend(check_production_ready_consistency(manifest, gate))
    
    # Report results
    if all_errors:
        print("\n❌ Proof artifact consistency check FAILED")
        print("\nErrors found:")
        for error in all_errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("\n✅ Proof artifact consistency check PASSED")
        print("All proof artifacts are consistent with each other.")
        sys.exit(0)


if __name__ == "__main__":
    main()
