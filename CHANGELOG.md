# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Moved all module-level imports to the top of `boabro.py` and gave the
  browser-runtime imports (`js`, `pyodide`, `to_js`) one honest fallback block.
- `_log_util_debug` now stays silent on the command line (logger-gated) and only
  mirrors to the real browser console, so the CLI output is clean.
- Type-annotated the name-table extraction and header helpers; added a
  `_to_js_headers` helper that replaces the always-false `"to_js" in globals()`
  guard that ruff and mypy flagged.
- Rewrote the test suite: one `tests/` copy (removed the duplicate that shipped
  inside the package), stronger fixture-font assertions, precise `TTLibError`
  expectations instead of bare `Exception`.
- Modernized CI: `ci.yml` is now a focused web-smoke check (the duplicate test
  matrix moved out), `release.yml` drops the PyInstaller binary matrix and its
  duplicated inline CLI in favour of the packaged `boabro` console script.

### Removed
- Template scaffolding that never did anything: `Config`, `process_data` (a
  `# TODO` stub returning `{}`), and the unused `main()` in `boabro.py`.

### Added
- `pytest-asyncio` to the test extra — the async fetch tests need it, and CI
  was silently missing it.
- mypy overrides for the unstubbed `fontTools` and browser-only modules.
- Project icon at `docs/assets/icon.png`.
- `llms.txt` / `md.txt` (generated snapshots) added to `.gitignore`.

### Documentation
- README: fixed the dead `examples/` path (pages live in `docs/`), documented
  the `boabro` CLI and `pip install`, and how to serve the web app locally.

### Historical
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