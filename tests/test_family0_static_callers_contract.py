from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/windows/family0-sweep-callers.ps1"
WRAPPER = ROOT / "scripts/windows/static-family0-sweep-callers.sh"


class FamilyZeroStaticCallersContract(unittest.TestCase):
    def test_static_script_is_bounded_and_aggregate_only(self):
        text = SCRIPT.read_text()
        self.assertIn("STATIC_ANALYSIS=READ_ONLY", text)
        self.assertIn("TARGET_SIGNATURE_MATCHES=", text)
        self.assertIn("DIRECT_REL32_CALLERS=", text)
        self.assertIn("DIRECT_REL32_TAIL_JUMPS=", text)
        self.assertIn("ABSOLUTE_POINTER_REFERENCES=", text)
        self.assertNotIn("TARGET_RVA=", text)
        self.assertNotIn("CALLER_RVAS=", text)
        self.assertNotIn("IMAGE_SHA256=", text)
        self.assertNotIn("WriteAllBytes", text)
        self.assertNotIn("Set-Content", text)

    def test_wrapper_uses_the_project_runtime_transport(self):
        text = WRAPPER.read_text()
        self.assertIn('source "$(dirname "$0")/common.sh"', text)
        self.assertIn("win_scp_to", text)
        self.assertIn("win_ps", text)
        self.assertIn("family0-sweep-callers.ps1", text)


if __name__ == "__main__":
    unittest.main()
