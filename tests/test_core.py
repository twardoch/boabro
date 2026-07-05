# this_file: tests/test_core.py
"""Tests for boabro's font-analysis core."""

import json
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fontTools.ttLib import TTLibError

from boabro.boabro import analyze_font_data, fetch_font_bytes_from_url

TEST_FONT = Path(__file__).parent.parent / "docs" / "testfont.ttf"


@pytest.fixture
def sample_font_bytes() -> bytes | None:
    """Raw bytes of the bundled Abril Fatface test font, if present."""
    if TEST_FONT.exists():
        return TEST_FONT.read_bytes()
    return None


class TestAnalyzeFontData:
    """Exercise analyze_font_data against real and malformed input."""

    def test_valid_font_shape(self, sample_font_bytes: bytes | None) -> None:
        """A real font yields the documented dictionary shape and types."""
        if sample_font_bytes is None:
            pytest.skip("Test font not available")

        result = analyze_font_data(sample_font_bytes, "test.ttf")

        assert result["fileName"] == "test.ttf"
        assert isinstance(result["upm"], int)
        assert isinstance(result["numGlyphs"], int)
        assert isinstance(result["tables"], list)
        assert isinstance(result["nameTableRecords"], list)

    def test_known_font_values(self, sample_font_bytes: bytes | None) -> None:
        """The bundled font parses to its known Abril Fatface metadata."""
        if sample_font_bytes is None:
            pytest.skip("Test font not available")

        result = analyze_font_data(sample_font_bytes, "testfont.ttf")

        assert result["familyName"] == "Abril Fatface"
        assert result["subfamily"] == "Regular"
        assert result["psName"] == "AbrilFatface-Regular"
        assert result["upm"] == 1000
        assert result["numGlyphs"] > 0
        assert "name" in result["tables"]
        assert "head" in result["tables"]

    def test_empty_bytes_raises(self) -> None:
        """Empty input is not a font; fontTools rejects it."""
        with pytest.raises(TTLibError):
            analyze_font_data(b"", "empty.ttf")

    def test_invalid_bytes_raises(self) -> None:
        """Garbage bytes are not a font; fontTools rejects them."""
        with pytest.raises(TTLibError):
            analyze_font_data(b"invalid font data", "invalid.ttf")

    def test_none_bytes_raises(self) -> None:
        """Passing None instead of bytes is a programming error."""
        with pytest.raises(TypeError):
            analyze_font_data(None, "none.ttf")  # type: ignore[arg-type]

    def test_name_record_structure(self, sample_font_bytes: bytes | None) -> None:
        """Each name record carries the five documented, typed fields."""
        if sample_font_bytes is None:
            pytest.skip("Test font not available")

        records = analyze_font_data(sample_font_bytes, "test.ttf")["nameTableRecords"]
        assert records

        first = records[0]
        assert isinstance(first["nameID"], int)
        assert isinstance(first["platformID"], int)
        assert isinstance(first["platEncID"], int)
        assert isinstance(first["langID"], int)
        assert isinstance(first["string"], str)


class TestFetchFontBytesFromUrl:
    """Exercise the URL fetch strategies without hitting the network."""

    @pytest.mark.asyncio
    async def test_invalid_url(self) -> None:
        assert await fetch_font_bytes_from_url("not-a-url") is None

    @pytest.mark.asyncio
    async def test_empty_url(self) -> None:
        assert await fetch_font_bytes_from_url("") is None

    @pytest.mark.asyncio
    async def test_none_url(self) -> None:
        assert await fetch_font_bytes_from_url(None) is None  # type: ignore[arg-type]

    @pytest.mark.asyncio
    @patch("boabro.boabro.pyodide")
    async def test_github_url_conversion(self, mock_pyodide: Mock) -> None:
        """A GitHub blob URL is rewritten to raw.githubusercontent.com first."""
        response = Mock()
        response.status = 200
        response.bytes = AsyncMock(return_value=b"font data")
        mock_pyodide.http.pyfetch = AsyncMock(return_value=response)

        url = "https://github.com/user/repo/blob/main/font.ttf"
        await fetch_font_bytes_from_url(url)

        first_call_url = mock_pyodide.http.pyfetch.call_args_list[0][0][0]
        assert (
            first_call_url
            == "https://raw.githubusercontent.com/user/repo/main/font.ttf"
        )

    @pytest.mark.asyncio
    @patch("boabro.boabro.pyodide")
    async def test_cors_proxy_fallback(self, mock_pyodide: Mock) -> None:
        """A failing first proxy falls through to the next until one succeeds."""
        fail = Mock()
        fail.status = 404
        ok = Mock()
        ok.status = 200
        ok.bytes = AsyncMock(return_value=b"font data")
        mock_pyodide.http.pyfetch = AsyncMock(side_effect=[fail, ok])

        result = await fetch_font_bytes_from_url("https://example.com/font.ttf")

        assert result == b"font data"
        assert mock_pyodide.http.pyfetch.call_count >= 2


class TestIntegration:
    """End-to-end checks over the bundled font."""

    def test_version_import(self) -> None:
        import boabro

        assert isinstance(boabro.__version__, str)
        assert boabro.__version__

    def test_end_to_end_analysis(self, sample_font_bytes: bytes | None) -> None:
        """Analyze the bundled font and confirm the result is JSON-serializable."""
        if sample_font_bytes is None:
            pytest.skip("Test font not available")

        result = analyze_font_data(sample_font_bytes, "testfont.ttf")

        assert result["familyName"] != "(N/A)"
        assert result["upm"] > 0
        assert result["numGlyphs"] > 0
        assert result["tables"]
        assert result["nameTableRecords"]

        parsed = json.loads(json.dumps(result))
        assert parsed["fileName"] == result["fileName"]


if __name__ == "__main__":
    pytest.main([__file__])
