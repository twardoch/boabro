import unittest
import os
from pathlib import Path
from typing import Dict, Any

# Add the src directory to sys.path to allow importing boabro
import sys
# It's better to adjust sys.path relative to this test file's location
# to make it runnable from any directory.
BASE_DIR = Path(__file__).resolve().parent.parent # This should point to the repo root
SRC_DIR = BASE_DIR / "src"
sys.path.insert(0, str(SRC_DIR.parent)) # Add repo root to path

from boabro.boabro import analyze_font_data

class TestBoabroAnalyzeFontData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Construct the path to testfont.ttf relative to this test file
        # Assuming test_boabro.py is in src/boabro/ and testfont.ttf is in docs/
        # So, from src/boabro/ -> ../../docs/testfont.ttf
        cls.test_font_path = BASE_DIR / "docs" / "testfont.ttf"
        try:
            with open(cls.test_font_path, "rb") as f:
                cls.test_font_bytes = f.read()
        except FileNotFoundError:
            cls.test_font_bytes = None
            print(f"ERROR: Test font file not found at {cls.test_font_path}. Tests involving this font will fail.")
        except Exception as e:
            cls.test_font_bytes = None
            print(f"ERROR: Could not read test font file: {e}")

    def test_analyze_valid_font(self):
        if not self.test_font_bytes:
            self.skipTest(f"Skipping test_analyze_valid_font due to missing test font: {self.test_font_path}")

        filename = "testfont.ttf"
        result = analyze_font_data(self.test_font_bytes, filename)

        self.assertIsInstance(result, dict)
        self.assertEqual(result.get("fileName"), filename)

        # Check for essential keys based on the docstring of analyze_font_data
        self.assertIn("familyName", result)
        self.assertEqual(result.get("familyName"), "Abril Fatface")

        self.assertIn("subfamily", result)
        self.assertEqual(result.get("subfamily"), "Regular")

        self.assertIn("fullName", result)
        self.assertEqual(result.get("fullName"), "Abril Fatface") # For this font, family and full are same initially

        self.assertIn("psName", result)
        self.assertEqual(result.get("psName"), "AbrilFatface-Regular")

        self.assertIn("upm", result)
        self.assertEqual(result.get("upm"), 1000) # Common UPM for this font

        self.assertIn("numGlyphs", result)
        self.assertIsInstance(result.get("numGlyphs"), int)
        self.assertGreater(result.get("numGlyphs", 0), 0) # Should have some glyphs

        self.assertIn("tables", result)
        self.assertIsInstance(result.get("tables"), list)
        self.assertTrue(len(result.get("tables", [])) > 0)
        self.assertIn("name", result.get("tables", [])) # 'name' table should exist
        self.assertIn("head", result.get("tables", [])) # 'head' table should exist

        self.assertIn("nameTableRecords", result)
        self.assertIsInstance(result.get("nameTableRecords"), list)
        self.assertTrue(len(result.get("nameTableRecords", [])) > 0)

        # Check structure of a name table record
        first_record = result.get("nameTableRecords", [{}])[0]
        self.assertIn("nameID", first_record)
        self.assertIn("platformID", first_record)
        self.assertIn("platEncID", first_record)
        self.assertIn("langID", first_record)
        self.assertIn("string", first_record)

    def test_analyze_empty_bytes(self):
        with self.assertRaises(Exception): # fontTools should raise an error
            analyze_font_data(b"", "empty.ttf")

    def test_analyze_random_bytes(self):
        random_data = os.urandom(1024) # 1KB of random data
        with self.assertRaises(Exception): # fontTools should raise an error
            analyze_font_data(random_data, "random.dat")

    def test_analyze_none_bytes(self):
        with self.assertRaises(TypeError): # Passing None should raise TypeError
            analyze_font_data(None, "none.dat") # type: ignore

if __name__ == "__main__":
    # This allows running the tests directly from this file
    # Make sure the script is run from the repository root or adjust paths accordingly
    # e.g., python src/boabro/test_boabro.py
    unittest.main()
