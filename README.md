# Boabro - Browser-based Font Analysis Tools

This repository contains a collection of browser-based font analysis tools, primarily utilizing Python through PyScript, to demonstrate various UI integrations and font analysis techniques.

## Project Overview

Boabro showcases how Python's powerful `fontTools` library can be leveraged directly in the web browser for font file analysis (TTF, OTF, WOFF, WOFF2). Users can inspect font metadata, table information, and other details without server-side processing or native software installation.

The project emphasizes:
- Running Python in the browser using [PyScript](https://pyscript.net/) (which itself builds on [Pyodide](https://pyodide.org/)).
- Centralizing core font analysis logic in a reusable Python module.
- Demonstrating integration with a wide variety of JavaScript UI approaches and libraries.

### Key Features

- **In-Browser Font Analysis**: Analyze TTF, OTF, WOFF, and WOFF2 font files.
- **Multiple UI Examples**: See implementations with various UI frameworks and patterns.
- **Detailed Font Information**: View font metadata, OpenType tables, glyph counts, and more.
- **File Upload & URL Support**: Analyze fonts from local files or remote URLs (with CORS considerations).
- **Core Python Logic**: Shared Python utilities in `src/boabro/boabro.py` provide consistent analysis results.

### Technical Implementation

- **Python in the Browser**: Primarily uses [PyScript](https://pyscript.net/) to execute Python code.
- **Font Analysis**: Leverages the [fontTools](https://github.com/fonttools/fonttools) Python library.
- **Shared Utilities**: Core font fetching and analysis logic is located in `src/boabro/boabro.py`.
- **UI Demonstrations**: The `docs` directory contains examples using:
    - PuePy (with Bootstrap, Bulma, UIkit, FrankenUI)
    - Alpine.js, Lit, Preact, HTMX, Vue.js, Web Components
    - PyScript workers for background processing
    - Direct PyScript for filesystem access, IndexedDB, etc.
- **Standalone Framework Tools**: Examples using Gradio-Lite and Stlite.

## Project Structure

The main example tools are HTML files located in the `docs` directory. Core Python logic is in `src/`.

- **`src/boabro/boabro.py`**: Contains the primary Python functions for fetching font data from URLs and analyzing font bytes.
- **`docs/`**: Contains all runnable HTML examples.
    - **PyScript-based tools** (typically prefixed with `_pyscript-`):
        - `_pyscript-alpinejs.html`
        - `_pyscript-fs.html` (formerly `pyodide-fs.html`)
        - `_pyscript-htmx.html`
        - `_pyscript-indexeddb.html`
        - `_pyscript-lit.html`
        - `_pyscript-preact-signals.html`
        - `_pyscript-tailwindcss.html` (formerly `pyodide-tailwindcss.html`)
        - `_pyscript-vuejs.html`
        - `_pyscript-webcomponents.html`
        - `_pyscript-worker.html` (and `_pyscript-worker-script.py`) (formerly `pyodide-worker.html`)
        - `_pyscript-workerspool.html` (and `_pyscript-pool-worker.py`) (formerly `pyodide-workerspool.html`)
        - `pyscript-puepy-bootstrap.html`
        - `pyscript-puepy-bulma.html`
        - `pyscript-puepy-frankenui.html`
        - `pyscript-puepy-uikit.html`
        - `pyscript-mako.html`
        - `pyscript-solidjs.html` (experimental)
        - `pyscript-svelte.html` (experimental)
    - **Other Framework-specific tools**:
        - `gradio.html` - Font Inspector using Gradio-Lite
        - `stlite.html` - Font Analyzer using Stlite (Streamlit)
        - `pyodide-react.jsx` - React-based example (status may vary)

## File Naming Convention

- Most PyScript examples are HTML files typically named `_pyscript-[feature_or_framework].html`.
- PuePy examples follow `pyscript-puepy-[css_framework].html`.
- Standalone tools like `gradio.html` or `stlite.html` are named directly.

## Renaming Script (Historical)

The repository previously included a script `rename_files.sh` to standardize file naming. Most files now follow the updated conventions.

## Getting Started

To run any of the examples:

1. Clone the repository:
   ```bash
   git clone https://github.com/twardoch/boabro.git
   cd boabro
   ```

2. Start a local web server from the repository root:
   ```bash
   python -m http.server 8080
   # Or use another simple HTTP server
   ```

3. Open your browser and navigate to:
   ```
   http://127.0.0.1:8080/docs/
   ```
   You can then click on individual HTML files to view the examples. For instance, to view the PuePy Bulma example: `http://127.0.0.1:8080/docs/pyscript-puepy-bulma.html`.

## Progress Tracking

The project progress is tracked in the following files:
- `PROGRESS.md`: Detailed progress report with completed tasks and fixes.
- `TODO.md`: List of pending tasks and issues to be addressed.

## Development Status

The project is actively being refactored and improved towards an MVP. See `PROGRESS.md` for the latest updates and `TODO.md` for upcoming tasks.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Testing

Basic unit tests for the core Python logic in `src/boabro/boabro.py` are available. To run them:

1.  Ensure you have Python installed.
2.  Navigate to the root directory of the repository.
3.  Run the tests using the `unittest` module:
    ```bash
    python -m unittest src/boabro/test_boabro.py
    ```
    Alternatively, if you are in the `src/boabro/` directory:
    ```bash
    python test_boabro.py
    ```

Manual smoke testing of the HTML examples in the `docs/` directory is recommended after any significant changes, by opening them in a web browser and verifying basic functionality.

### Code Quality & Pre-commit Hooks

This project uses `ruff` for linting and formatting, configured in `pyproject.toml`.
Pre-commit hooks are set up using `.pre-commit-config.yaml` to automatically run checks before each commit.

To use the pre-commit hooks:
1. Install `pre-commit`:
   ```bash
   pip install pre-commit
   # Or, if you use hatch:
   # hatch env create dev
   # hatch shell dev
   # pip install pre-commit
   # (pre-commit is listed in dev dependencies in pyproject.toml, so hatch env should have it)
   ```
2. Install the git hooks:
   ```bash
   pre-commit install
   ```
Now, `ruff` and other checks will run automatically on `git commit`.

## Author

Created by Adam Twardoch (adam+github@twardoch.com)