import shutil
import subprocess
import unittest


class TestSafetyMonitorBehavior(unittest.TestCase):
    def test_safety_monitor_behavioral_sim(self):
        if shutil.which("iverilog") is None or shutil.which("vvp") is None:
            self.skipTest("iverilog/vvp not installed")

        proc = subprocess.run(
            ["python3", "scripts/run_safety_monitor_sim.py"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("TB_PASS tb_safety_monitor", proc.stdout)


if __name__ == "__main__":
    unittest.main()
