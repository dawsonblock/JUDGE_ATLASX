import subprocess
import tempfile
import unittest
from pathlib import Path
import json


class TestV15PreboardGate(unittest.TestCase):
    def test_new_scripts_exist(self):
        for rel in [
            "scripts/preboard_check.py",
            "scripts/implementation_gate.py",
            "scripts/package_vivado_signoff.py",
            "docs/PREBOARD_GATE_V15.md",
            "docs/BOARD_READY_TEMPLATE.md",
        ]:
            self.assertTrue(Path(rel).exists(), rel)

    def test_makefile_targets_exist(self):
        text = Path("Makefile").read_text()
        for target in ["preboard-check", "implementation-gate", "vivado-signoff-package"]:
            self.assertIn(target, text)

    def test_cdc_parser_json_output_on_clean_report(self):
        with tempfile.TemporaryDirectory() as td:
            report = Path(td) / "cdc.rpt"
            out = Path(td) / "summary.json"
            report.write_text("CDC Summary\nNo issues here\n")
            proc = subprocess.run(
                ["python3", "scripts/parse_cdc_report.py", str(report), "--json-out", str(out), "--fail-on-critical"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout)
            data = json.loads(out.read_text())
            self.assertTrue(data["pass"])

    def test_cdc_parser_fails_on_critical(self):
        with tempfile.TemporaryDirectory() as td:
            report = Path(td) / "cdc.rpt"
            out = Path(td) / "summary.json"
            report.write_text("Critical Warning: Unknown CDC structure\n")
            proc = subprocess.run(
                ["python3", "scripts/parse_cdc_report.py", str(report), "--json-out", str(out), "--fail-on-critical"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            self.assertNotEqual(proc.returncode, 0)
            data = json.loads(out.read_text())
            self.assertFalse(data["pass"])

    def test_implementation_gate_fails_when_reports_missing(self):
        with tempfile.TemporaryDirectory() as td:
            proc = subprocess.run(
                ["python3", "scripts/implementation_gate.py", "--reports", td],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            self.assertNotEqual(proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()
