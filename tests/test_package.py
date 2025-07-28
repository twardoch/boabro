"""Test suite for boabro."""

def test_version():
    """Verify package exposes version."""
    import boabro
    assert boabro.__version__
    assert isinstance(boabro.__version__, str)
    assert len(boabro.__version__) > 0

def test_imports():
    """Test that all expected functions are importable."""
    from boabro import analyze_font_data, fetch_font_bytes_from_url, process_data, Config
    assert callable(analyze_font_data)
    assert callable(fetch_font_bytes_from_url)
    assert callable(process_data)
    assert Config is not None
