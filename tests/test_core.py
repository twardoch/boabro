# this_file: tests/test_core.py
"""Comprehensive tests for boabro core functionality."""

import pytest
import json
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock
from boabro.boabro import analyze_font_data, fetch_font_bytes_from_url, Config, process_data


class TestAnalyzeFontData:
    """Test suite for analyze_font_data function."""

    @pytest.fixture
    def sample_font_bytes(self):
        """Load sample font bytes for testing."""
        font_path = Path(__file__).parent.parent / "docs" / "testfont.ttf"
        if font_path.exists():
            with open(font_path, "rb") as f:
                return f.read()
        return None

    def test_analyze_font_data_with_valid_font(self, sample_font_bytes):
        """Test font analysis with a valid font file."""
        if sample_font_bytes is None:
            pytest.skip("Test font not available")

        result = analyze_font_data(sample_font_bytes, "test.ttf")

        assert isinstance(result, dict)
        assert result["fileName"] == "test.ttf"
        assert "familyName" in result
        assert "subfamily" in result
        assert "upm" in result
        assert "numGlyphs" in result
        assert "tables" in result
        assert "nameTableRecords" in result

        # Check data types
        assert isinstance(result["upm"], int)
        assert isinstance(result["numGlyphs"], int)
        assert isinstance(result["tables"], list)
        assert isinstance(result["nameTableRecords"], list)

    def test_analyze_font_data_with_empty_bytes(self):
        """Test error handling with empty font bytes."""
        with pytest.raises(Exception):
            analyze_font_data(b"", "empty.ttf")

    def test_analyze_font_data_with_invalid_bytes(self):
        """Test error handling with invalid font bytes."""
        with pytest.raises(Exception):
            analyze_font_data(b"invalid font data", "invalid.ttf")

    def test_analyze_font_data_with_none_bytes(self):
        """Test error handling with None bytes."""
        with pytest.raises(TypeError):
            analyze_font_data(None, "none.ttf")

    def test_analyze_font_data_name_table_records_structure(self, sample_font_bytes):
        """Test name table records structure."""
        if sample_font_bytes is None:
            pytest.skip("Test font not available")

        result = analyze_font_data(sample_font_bytes, "test.ttf")

        name_records = result["nameTableRecords"]
        assert len(name_records) > 0

        # Check structure of first record
        first_record = name_records[0]
        required_keys = ["nameID", "platformID", "platEncID", "langID", "string"]
        for key in required_keys:
            assert key in first_record

        # Check data types
        assert isinstance(first_record["nameID"], int)
        assert isinstance(first_record["platformID"], int)
        assert isinstance(first_record["platEncID"], int)
        assert isinstance(first_record["langID"], int)
        assert isinstance(first_record["string"], str)


class TestFetchFontBytesFromUrl:
    """Test suite for fetch_font_bytes_from_url function."""

    @pytest.mark.asyncio
    async def test_fetch_font_bytes_invalid_url(self):
        """Test error handling with invalid URL."""
        result = await fetch_font_bytes_from_url("not-a-url")
        assert result is None

    @pytest.mark.asyncio
    async def test_fetch_font_bytes_empty_url(self):
        """Test error handling with empty URL."""
        result = await fetch_font_bytes_from_url("")
        assert result is None

    @pytest.mark.asyncio
    async def test_fetch_font_bytes_none_url(self):
        """Test error handling with None URL."""
        result = await fetch_font_bytes_from_url(None)
        assert result is None

    @pytest.mark.asyncio
    @patch("boabro.boabro.pyodide")
    async def test_fetch_font_bytes_github_conversion(self, mock_pyodide):
        """Test GitHub URL conversion to raw format."""
        mock_response = Mock()
        mock_response.status = 200
        mock_response.bytes = AsyncMock(return_value=b"font data")
        mock_pyodide.http.pyfetch = AsyncMock(return_value=mock_response)

        url = "https://github.com/user/repo/blob/main/font.ttf"
        result = await fetch_font_bytes_from_url(url)

        # Should convert to raw URL and fetch
        expected_raw_url = "https://raw.githubusercontent.com/user/repo/main/font.ttf"
        mock_pyodide.http.pyfetch.assert_called()
        call_args = mock_pyodide.http.pyfetch.call_args_list[0][0]
        assert call_args[0] == expected_raw_url

    @pytest.mark.asyncio
    @patch("boabro.boabro.pyodide")
    async def test_fetch_font_bytes_cors_proxy_fallback(self, mock_pyodide):
        """Test CORS proxy fallback mechanism."""
        # Mock failed direct fetch, successful proxy fetch
        mock_response_fail = Mock()
        mock_response_fail.status = 404

        mock_response_success = Mock()
        mock_response_success.status = 200
        mock_response_success.bytes = AsyncMock(return_value=b"font data")

        mock_pyodide.http.pyfetch = AsyncMock(side_effect=[
            mock_response_fail,  # Direct fetch fails
            mock_response_success  # Proxy fetch succeeds
        ])

        url = "https://example.com/font.ttf"
        result = await fetch_font_bytes_from_url(url)

        assert result == b"font data"
        assert mock_pyodide.http.pyfetch.call_count >= 2


class TestConfig:
    """Test suite for Config class."""

    def test_config_creation(self):
        """Test Config object creation."""
        config = Config(name="test", value="value")
        assert config.name == "test"
        assert config.value == "value"
        assert config.options is None

    def test_config_with_options(self):
        """Test Config object with options."""
        options = {"key1": "value1", "key2": 42}
        config = Config(name="test", value="value", options=options)
        assert config.options == options

    def test_config_different_value_types(self):
        """Test Config with different value types."""
        config_str = Config(name="test", value="string")
        config_int = Config(name="test", value=123)
        config_float = Config(name="test", value=3.14)

        assert isinstance(config_str.value, str)
        assert isinstance(config_int.value, int)
        assert isinstance(config_float.value, float)


class TestProcessData:
    """Test suite for process_data function."""

    def test_process_data_empty_input(self):
        """Test error handling with empty input."""
        with pytest.raises(ValueError, match="Input data cannot be empty"):
            process_data([])

    def test_process_data_none_input(self):
        """Test error handling with None input."""
        with pytest.raises(ValueError, match="Input data cannot be empty"):
            process_data(None)

    def test_process_data_with_config(self):
        """Test process_data with config parameter."""
        config = Config(name="test", value="value")
        result = process_data(["data"], config=config)
        assert isinstance(result, dict)

    def test_process_data_debug_mode(self):
        """Test process_data in debug mode."""
        with patch("boabro.boabro.logger") as mock_logger:
            result = process_data(["data"], debug=True)
            mock_logger.setLevel.assert_called_once()
            assert isinstance(result, dict)

    def test_process_data_valid_input(self):
        """Test process_data with valid input."""
        result = process_data(["item1", "item2"])
        assert isinstance(result, dict)


class TestIntegration:
    """Integration tests for boabro functionality."""

    def test_version_import(self):
        """Test that version can be imported."""
        from boabro import __version__
        assert isinstance(__version__, str)
        assert len(__version__) > 0

    def test_all_imports(self):
        """Test that all public functions can be imported."""
        from boabro import analyze_font_data, fetch_font_bytes_from_url, process_data, Config

        assert callable(analyze_font_data)
        assert callable(fetch_font_bytes_from_url)
        assert callable(process_data)
        assert Config is not None

    def test_end_to_end_analysis(self):
        """Test end-to-end font analysis workflow."""
        font_path = Path(__file__).parent.parent / "docs" / "testfont.ttf"
        if not font_path.exists():
            pytest.skip("Test font not available")

        # Load font
        with open(font_path, "rb") as f:
            font_bytes = f.read()

        # Analyze font
        result = analyze_font_data(font_bytes, font_path.name)

        # Verify essential information is present
        assert result["fileName"] == font_path.name
        assert result["familyName"] != "(N/A)"
        assert result["upm"] > 0
        assert result["numGlyphs"] > 0
        assert len(result["tables"]) > 0
        assert len(result["nameTableRecords"]) > 0

        # Test JSON serialization
        json_str = json.dumps(result)
        parsed = json.loads(json_str)
        assert parsed["fileName"] == result["fileName"]


if __name__ == "__main__":
    pytest.main([__file__])
