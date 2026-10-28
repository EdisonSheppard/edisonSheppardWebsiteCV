import tempfile
import unittest
from pathlib import Path
from tools.build import safe_relative
from tools.check_publish import inspect_text

class BuildSafetyTests(unittest.TestCase):
    def test_safe_assets(self):
        self.assertTrue(safe_relative("assets/rc-car/cover.webp", "assets"))
        self.assertFalse(safe_relative("assets/../../private/report.docx", "assets"))
        self.assertFalse(safe_relative("https://example.com/cover.jpg", "assets"))
        self.assertFalse(safe_relative("assets\\backslash.jpg", "assets"))

    def test_sensitive_strings(self):
        self.assertTrue(inspect_text(Path("index.html"), "email: someone@example.org"))
        self.assertFalse(inspect_text(Path("README.md"), "Simple CAD prototype description."))

if __name__ == "__main__":
    unittest.main()
