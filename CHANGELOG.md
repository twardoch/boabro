# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Major refactoring of core logic into centralized `src/boabro/boabro.py` module
- All PyScript examples now import and use shared utilities from the core module
- Renamed examples with underscore prefix (_) to indicate working/stable status
- Updated PyScript configurations to correctly resolve local module imports from `src/`
- Improved code organization and reduced duplication across all examples

### Added
- Unit tests for `analyze_font_data` in `src/boabro/test_boabro.py`
- `requirements-dev.txt` with development dependencies (ruff)
- Comprehensive docstrings for key functions in core module
- Professional development apparatus leveraging existing `pyproject.toml` and `.pre-commit-config.yaml`

### Fixed
- Alpine.js initialization race conditions and PyScript function access
- Vue.js Python string literal syntax errors in table generation
- Web Components event listener attachment after re-renders
- Lit component PyScript readiness handling
- Preact Signals component PyScript function calls after initialization
- HTMX example multiple "Starting font analysis" log messages
- IndexedDB example "pyscript is not defined" errors

### Documentation
- Revised `README.md` to accurately reflect current project state and technologies
- Updated `docs/index.md` with correct example filenames and descriptions
- Added sections on running unit tests and using pre-commit hooks

## [0.1.0] - 2025-06-23

### Added
- Initial release of browser-based font analysis toolkit
- Support for TTF, OTF, WOFF, and WOFF2 font formats
- Multiple UI framework integrations with PyScript:
  - PuePy with Bootstrap, Bulma, UIkit, and FrankenUI
  - Alpine.js, Lit, Preact with Signals, Vue.js
  - Native Web Components, HTMX
  - Gradio-Lite and Stlite (Streamlit)
- Font analysis features:
  - Font metadata extraction
  - Name table entries display
  - OpenType table listing
  - Glyph count and UPM values
- CORS proxy fallback mechanisms for URL-based font loading
- Web Worker implementations for parallel processing
- IndexedDB integration for font storage
- Virtual filesystem support

### Known Issues
- Solid.js example has Babel/module loading issues
- Svelte example requires compilation step not suitable for browser-only approach
- Some examples still show console errors during initialization (being addressed)