import sys
from importlib import util
from pathlib import Path


def _load_release_gate_module():
    module_path = Path(__file__).resolve().parents[3] / "scripts" / "release_gate.py"
    spec = util.spec_from_file_location("release_gate_schema_module", module_path)
    assert spec is not None and spec.loader is not None
    module = util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_release_candidate_requires_archive_validation_pass():
    module = _load_release_gate_module()
    payload = {
        "alpha_gate_passed": True,
        "archive_validation_result": "FAIL",
    }

    module._refresh_release_payload_schema(payload, [])

    assert payload["release_candidate"] is False


def test_release_candidate_is_true_only_when_alpha_gate_and_archive_validation_pass():
    module = _load_release_gate_module()
    payload = {
        "alpha_gate_passed": True,
        "archive_validation_result": "PASS",
    }

    module._refresh_release_payload_schema(payload, [])

    assert payload["release_candidate"] is True