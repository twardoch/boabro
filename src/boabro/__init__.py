# this_file: src/boabro/__init__.py
"""Boabro - Browser-based Font Analysis Tools."""

from .boabro import analyze_font_data, fetch_font_bytes_from_url, process_data, Config

try:
    from .__version__ import __version__
except ImportError:
    __version__ = "unknown"

__all__ = ["Config", "__version__", "analyze_font_data", "fetch_font_bytes_from_url", "process_data"]
