# this_file: tests/conftest.py
"""pytest configuration.

Add `src/` to the import path so the tests run against the working tree even
without an editable install.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
