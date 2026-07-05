# this_file: tests/test_package.py
"""Smoke tests for the boabro package surface."""

import boabro


def test_version() -> None:
    """The package exposes a non-empty version string."""
    assert isinstance(boabro.__version__, str)
    assert boabro.__version__


def test_imports() -> None:
    """The two public functions are importable and callable."""
    assert callable(boabro.analyze_font_data)
    assert callable(boabro.fetch_font_bytes_from_url)
