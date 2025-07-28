# this_file: tests/conftest.py
"""pytest configuration and shared fixtures."""

import pytest
import sys
from pathlib import Path

# Add src to path for testing
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

@pytest.fixture
def sample_font_path():
    """Return path to sample font file."""
    return Path(__file__).parent.parent / "docs" / "testfont.ttf"

@pytest.fixture
def sample_font_bytes(sample_font_path):
    """Load sample font bytes for testing."""
    if sample_font_path.exists():
        with open(sample_font_path, "rb") as f:
            return f.read()
    return None
