import shutil
import subprocess
import unittest


class TestAxiliteRegfileBehavior(unittest.TestCase):
    def test_axilite_behavioral_sim(self):
        if shutil.which("iverilog") is None or shutil.which("vvp") is None:
            self.skipTest("iverilog/vvp not installed")

        proc = subprocess.run(
            ["python3", "scripts/run_axilite_regfile_sim.py"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("TB_PASS tb_axilite_regfile_full", proc.stdout)


if __name__ == "__main__":
    unittest.main()
