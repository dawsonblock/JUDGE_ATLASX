import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def build_proof_root(base: Path) -> Path:
    root = base / "waveform_brain-main-proof"
    reports = root / "reports"
    reports.mkdir(parents=True, exist_ok=True)

    metadata = {
        "schema_version": 1,
        "generated_at_utc": "2026-05-28T00:00:00Z",
        "command": "python3 scripts/preboard_check.py --mode proof",
        "source_tree_hash": "abcd" * 16,
    }
    preboard = {
        **metadata,
        "pass": True,
        "overall_pass": True,
        "checks": [],
    }
    impl = {
        "generated_at_utc": "2026-05-28T00:00:00Z",
        "pass": True,
        "checks": {
            "cdc_critical": {"pass": True, "detail": "ok"},
            "cdc_cell_match": {"pass": True, "detail": "ok"},
            "timing": {"pass": True, "detail": "ok"},
            "drc": {"pass": True, "detail": "ok"},
        },
    }

    (reports / "preboard_local_summary.json").write_text(
        json.dumps(preboard), encoding="utf-8"
    )
    (reports / "preboard_local_summary.md").write_text(
        "ok\n",
        encoding="utf-8",
    )
    (reports / "local_toolchain_summary.json").write_text(
        json.dumps({**metadata, "pass": True}),
        encoding="utf-8",
    )
    (reports / "source_tree_hash_summary.json").write_text(
        json.dumps({**metadata, "pass": True, "command": "hash"}),
        encoding="utf-8",
    )
    (reports / "source_tree_hash.txt").write_text(
        f"{metadata['source_tree_hash']}\n",
        encoding="utf-8",
    )
    (reports / "source_tree_clean_summary.json").write_text(
        json.dumps({**metadata, "pass": True, "command": "clean"}),
        encoding="utf-8",
    )
    (reports / "cdc_static_summary.json").write_text(
        json.dumps({**metadata, "pass": True, "command": "cdc"}),
        encoding="utf-8",
    )
    (reports / "register_map.json").write_text(
        json.dumps({"registers": []}),
        encoding="utf-8",
    )
    (reports / "implementation_gate_summary.json").write_text(
        json.dumps(impl), encoding="utf-8"
    )
    (reports / "implementation_gate_summary.md").write_text(
        "ok\n",
        encoding="utf-8",
    )
    (reports / "axilite_regfile_sim_summary.json").write_text(
        json.dumps({**metadata, "pass": True}), encoding="utf-8"
    )
    (reports / "axilite_regfile_sim.log").write_text(
        "axilite sim ok\n",
        encoding="utf-8",
    )
    (reports / "packer_axis_sim_summary.json").write_text(
        json.dumps({**metadata, "pass": True}), encoding="utf-8"
    )
    (reports / "packer_axis_sim.log").write_text(
        "packer sim ok\n",
        encoding="utf-8",
    )
    (reports / "safety_monitor_sim_summary.json").write_text(
        json.dumps({**metadata, "pass": True}), encoding="utf-8"
    )
    (reports / "safety_monitor_sim.log").write_text(
        "safety sim ok\n",
        encoding="utf-8",
    )
    (reports / "prbs_datapath_sim_summary.json").write_text(
        json.dumps({**metadata, "pass": True}),
        encoding="utf-8",
    )
    (reports / "gkp_decoder_sim_summary.json").write_text(
        json.dumps({**metadata, "pass": True}),
        encoding="utf-8",
    )
    (reports / "gkp_decoder_sim.log").write_text(
        "gkp sim ok\n",
        encoding="utf-8",
    )
    (reports / "prbs_datapath_sim.log").write_text(
        "prbs sim ok\n",
        encoding="utf-8",
    )
    (reports / "rtl_arithmetic_audit.json").write_text(
        json.dumps({"pass": True}),
        encoding="utf-8",
    )
    (reports / "rtl_arithmetic_audit.md").write_text(
        "audit ok\n",
        encoding="utf-8",
    )
    (reports / "rtl_arithmetic_audit.log").write_text(
        "audit log\n",
        encoding="utf-8",
    )
    (reports / "rtl_sanity.log").write_text(
        "rtl sanity ok\n",
        encoding="utf-8",
    )
    (reports / "cdc_critical_summary.json").write_text(
        json.dumps({"pass": True}), encoding="utf-8"
    )
    (reports / "cdc_cell_match_summary.md").write_text(
        "ok\n",
        encoding="utf-8",
    )
    (reports / "timing_summary.rpt").write_text(
        "WNS(ns) 0.100\n",
        encoding="utf-8",
    )
    (reports / "drc.rpt").write_text("No errors\n", encoding="utf-8")
    (reports / "cdc_full.rpt").write_text("No issues\n", encoding="utf-8")
    (reports / "cdc_critical.rpt").write_text("No issues\n", encoding="utf-8")
    (reports / "clock_interaction.rpt").write_text(
        "No issues\n",
        encoding="utf-8",
    )
    (reports / "utilization.rpt").write_text("No issues\n", encoding="utf-8")
    (reports / "vivado_synth.log").write_text("synth ok\n", encoding="utf-8")
    (reports / "vivado_impl.log").write_text("impl ok\n", encoding="utf-8")
    (reports / "unittest.log").write_text("tests ok\n", encoding="utf-8")
    (reports / "cosim_gkp.log").write_text("cosim ok\n", encoding="utf-8")
    (reports / "make_validate.log").write_text(
        "validate ok\n",
        encoding="utf-8",
    )
    (reports / "board_smoke_summary.json").write_text(
        json.dumps({"pass": True}),
        encoding="utf-8",
    )
    (reports / "board_capture_summary.json").write_text(
        json.dumps({"pass": True}),
        encoding="utf-8",
    )

    return root


def zip_tree(root: Path, out_zip: Path) -> None:
    with ZipFile(out_zip, "w", ZIP_DEFLATED) as zf:
        for item in sorted(root.rglob("*")):
            if item.is_dir():
                continue
            zf.write(item, item.relative_to(root.parent).as_posix())


class TestReleaseArchiveValidation(unittest.TestCase):
    def setUp(self) -> None:
        self.python = shutil.which("python3") or "python3"

    def run_validator(
        self,
        archive: Path,
        mode: str = "proof-local",
        *extra_args: str,
    ) -> subprocess.CompletedProcess[str]:
        cmd = [
            self.python,
            "scripts/validate_release_archive.py",
            str(archive),
            "--mode",
            mode,
            *extra_args,
        ]
        return subprocess.run(
            cmd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=90,
        )

    def test_proof_semantics_fail_when_preboard_failed(self):
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            root = build_proof_root(td_path)

            preboard_path = root / "reports" / "preboard_local_summary.json"
            preboard = json.loads(preboard_path.read_text(encoding="utf-8"))
            preboard["pass"] = False
            preboard_path.write_text(json.dumps(preboard), encoding="utf-8")

            archive = td_path / "proof.zip"
            zip_tree(root, archive)
            proc = self.run_validator(archive, "proof-local")
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("preboard_local_summary pass=false", proc.stdout)

    def test_proof_semantics_fail_when_impl_check_failed(self):
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            root = build_proof_root(td_path)

            impl_path = root / "reports" / "implementation_gate_summary.json"
            impl = json.loads(impl_path.read_text(encoding="utf-8"))
            impl["checks"]["timing"]["pass"] = False
            impl_path.write_text(json.dumps(impl), encoding="utf-8")

            archive = td_path / "proof.zip"
            zip_tree(root, archive)
            proc = self.run_validator(archive, "proof-board")
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("implementation check failed: timing", proc.stdout)

    def test_board_proof_requires_raw_logs(self):
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            root = build_proof_root(td_path)
            (root / "reports" / "gkp_decoder_sim.log").unlink()
            archive = td_path / "proof.zip"
            zip_tree(root, archive)

            proc = self.run_validator(archive, "proof-board")
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("missing required proof entry", proc.stdout)
            self.assertIn("reports/gkp_decoder_sim.log", proc.stdout)

    def test_proof_semantics_fail_when_metadata_missing(self):
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            root = build_proof_root(td_path)
            p = root / "reports" / "packer_axis_sim_summary.json"
            data = json.loads(p.read_text(encoding="utf-8"))
            data.pop("generated_at_utc", None)
            p.write_text(json.dumps(data), encoding="utf-8")

            archive = td_path / "proof.zip"
            zip_tree(root, archive)
            proc = self.run_validator(archive, "proof-local")
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn(
                "missing metadata field generated_at_utc",
                proc.stdout,
            )

    def test_proof_semantics_fail_when_hash_text_mismatch(self):
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            root = build_proof_root(td_path)
            (root / "reports" / "source_tree_hash.txt").write_text(
                "f" * 64 + "\n",
                encoding="utf-8",
            )

            archive = td_path / "proof.zip"
            zip_tree(root, archive)
            proc = self.run_validator(archive, "proof-local")
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn(
                "proof freshness failure",
                proc.stdout,
            )

    def test_proof_semantics_fail_when_summary_hash_mismatch(self):
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            root = build_proof_root(td_path)
            p = root / "reports" / "packer_axis_sim_summary.json"
            data = json.loads(p.read_text(encoding="utf-8"))
            data["source_tree_hash"] = "0" * 64
            p.write_text(json.dumps(data), encoding="utf-8")

            archive = td_path / "proof.zip"
            zip_tree(root, archive)
            proc = self.run_validator(archive, "proof-local")
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn(
                "hash mismatch",
                proc.stdout,
            )


if __name__ == "__main__":
    unittest.main()
