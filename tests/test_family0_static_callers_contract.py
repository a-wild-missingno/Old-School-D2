from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/windows/family0-sweep-callers.ps1"
WRAPPER = ROOT / "scripts/windows/static-family0-sweep-callers.sh"
LOADED_SCRIPT = ROOT / "scripts/windows/family0-sweep-loaded-callers.ps1"
LOADED_WRAPPER = ROOT / "scripts/windows/scan-loaded-family0-sweep-callers.sh"


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

    def test_loaded_scan_is_read_only_and_aggregate_only(self):
        text = LOADED_SCRIPT.read_text()
        self.assertIn("LOADED_PROCESS_ANALYSIS=READ_ONLY", text)
        self.assertIn("TARGET_SIGNATURE_MATCHES=", text)
        self.assertIn("DIRECT_REL32_CALLERS=", text)
        self.assertIn("DIRECT_REL32_TAIL_JUMPS=", text)
        self.assertIn("ABSOLUTE_POINTER_REFERENCES=", text)
        self.assertIn("ReadProcessMemory", text)
        self.assertIn("FamilyZeroAggregateScanner", text)
        self.assertNotIn("WriteProcessMemory", text)
        self.assertNotIn("TARGET_RVA=", text)
        self.assertNotIn("CALLER_RVAS=", text)
        self.assertNotIn("IMAGE_SHA256=", text)

    def test_loaded_wrapper_uses_project_runtime_transport(self):
        text = LOADED_WRAPPER.read_text()
        self.assertIn('source "$(dirname "$0")/common.sh"', text)
        self.assertIn("win_scp_to", text)
        self.assertIn("win_ps", text)
        self.assertIn("family0-sweep-loaded-callers.ps1", text)

    def test_wrapper_uses_the_project_runtime_transport(self):
        text = WRAPPER.read_text()
        self.assertIn('source "$(dirname "$0")/common.sh"', text)
        self.assertIn("win_scp_to", text)
        self.assertIn("win_ps", text)
        self.assertIn("family0-sweep-callers.ps1", text)


if __name__ == "__main__":
    unittest.main()
