# Boabro - Browser-based Font Analysis Tools

Boabro analyzes font files (TTF, OTF, WOFF, WOFF2) directly in your web browser. It uses Python and the `fontTools` library, running client-side via [PyScript](https://pyscript.net/).

## What does Boabro do?

Boabro lets you:
*   **Inspect Font Details**: Upload a font file or provide a URL for analysis
*   **View Metadata**: See family name, style, version, manufacturer, designer, and license info
*   **Explore Font Tables**: Examine OpenType tables that define font structure and features
*   **Check Key Metrics**: View units per em (UPM), glyph counts, and other technical details
*   **Run Anywhere**: Works on any device with a modern browser—no specialized software needed

## Who is Boabro for?

*   **Web Developers & Designers**: Quick font checks, web font troubleshooting, characteristic verification
*   **Typographers & Font Engineers**: Rapid analysis during design or testing
*   **Students & Educators**: Interactive learning about font structures and OpenType features
*   **Font Curious**: Anyone wanting to peek inside font files

## Why is Boabro useful?

*   **Zero Installation**: Runs in-browser, no downloads required
*   **Client-Side Processing**: Local files stay local, remote files fetch securely
*   **Python Powered**: Proves Python libraries can work in web environments
*   **UI Flexibility**: Demonstrates various web UI integrations with PyScript
*   **Cross-Platform**: Any OS with a compatible browser

## Getting Started

Boabro is a collection of demonstration tools, not a traditional library. To explore:

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/twardoch/boabro.git
    cd boabro
    ```

2.  **Start a Local Web Server**:
    ```bash
    python -m http.server 8080
    ```

3.  **Access the Tools**:
    Open your browser to:
    ```
    http://127.0.0.1:8080/docs/
    ```
    Click any HTML file to launch that tool. Example: `pyscript-puepy-bulma.html`

## How to Use Boabro

### Using the Example Tools

The `docs/` directory contains HTML examples demonstrating different UI setups:
*   **Upload or Fetch**: Most tools accept local files or URLs
*   **View Analysis**: Results display in categorized sections (metadata, tables, etc.)

Available examples include integrations with:
*   **PuePy** (Bootstrap, Bulma, UIkit, FrankenUI)
*   **Alpine.js**, **Lit**, **Preact**, **HTMX**, **Vue.js**, **Web Components**
*   **Gradio-Lite** and **Stlite** (browser-based Streamlit)
*   Direct PyScript features: filesystem access, IndexedDB, web workers

See the `docs` directory for the complete list of HTML files.

### Programmatic Usage

To integrate Boabro into your PyScript projects:

1.  **Include `boabro.py`**: Place it where your HTML can access it
2.  **Import Functions**:
    ```python
    from boabro import fetch_font_bytes_from_url, analyze_font_data

    async def process_font_from_url(font_url):
        font_bytes = await fetch_font_bytes_from_url(font_url)
        if font_bytes:
            analysis_result = analyze_font_data(font_bytes, filename="myfont.otf")
            print(analysis_result)
        else:
            print(f"Could not fetch font from {font_url}")

    async def process_local_font_file(js_file_proxy):
        filename = js_file_proxy.name
        array_buffer = await js_file_proxy.arrayBuffer()
        font_bytes = array_buffer.to_bytes()

        if font_bytes:
            analysis_result = analyze_font_data(font_bytes, filename=filename)
            print(analysis_result)
    ```

The `fetch_font_bytes_from_url` function handles CORS issues. The `analyze_font_data` function parses font bytes and returns detailed information.

### Command-Line Usage

The `src/boabro/boabro.py` script is designed for browser use. While executable, its `main()` function is minimal and offers no CLI features. Use it within PyScript environments.

## Technical Deep Dive & Contributing

### How the Code Works

#### Core Logic (`src/boabro/boabro.py`)

*   **`fetch_font_bytes_from_url(url_str: str) -> Optional[bytes]`**:
    *   Asynchronous function that retrieves font bytes from URLs
    *   Tries GitHub raw URL conversion, CORS proxies, direct fetch, then `mode="no-cors"`
    *   Uses `pyodide.http.pyfetch` with common HTTP headers
    *   Returns `bytes` or `None`

*   **`analyze_font_data(font_bytes: bytes, filename: Optional[str] = "font") -> Dict[str, Any]`**:
    *   Parses font bytes using `fontTools.ttLib.TTFont`
    *   Extracts name table entries (NameIDs 1-14, 16-25), `upm`, `numGlyphs`, table tags, decoded name records
    *   Returns font information dictionary; logs and re-raises errors

*   **Logging**:
    *   Uses Python's `logging` module
    *   Attempts to log to `js.console.log` in PyScript environments

#### PyScript Integration

Python runs in-browser via [PyScript](https://pyscript.net/)/[Pyodide](https://pyodide.org/), compiling to WebAssembly. `fontTools` loads through PyScript configuration.

#### UI Examples (`docs/`)

HTML examples in `docs/` integrate `boabro.py` with various UI libraries. They handle UI interaction, call core functions, and display results.

**File Naming**:
*   PyScript examples: `_pyscript-[feature_or_framework].html`
*   PuePy examples: `pyscript-puepy-[css_framework].html`
*   Standalone tools: e.g., `gradio.html`

### Project Structure

*   **`src/boabro/`**: Core Python code (`boabro.py`, `test_boabro.py`)
*   **`docs/`**: Runnable HTML examples
*   **`tests/`**: Package-level tests
*   **`pyproject.toml`**: Project metadata, dependencies, build config (Hatch)
*   **`.pre-commit-config.yaml`**: Pre-commit hooks
*   **`README.md`**: This file
*   **`LICENSE`**: MIT License
*   **`PROGRESS.md`**, **`TODO.md`**: Development tracking

### Development Setup

1.  **Python**: 3.10+
2.  **Clone Repository**
3.  **Virtual Environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    ```
    Or with [Hatch](https://hatch.pypa.io/latest/):
    ```bash
    hatch env create dev
    hatch shell dev
    ```
4.  **Install Dependencies**:
    With Hatch: handled automatically
    With pip:
    ```bash
    pip install -r requirements-dev.txt
    ```
    Or editable install:
    ```bash
    pip install -e .[dev,test]
    ```

### Code Quality

Uses `ruff` for linting/formatting and `mypy` for type checking.

**Pre-commit Hooks**:
1.  Install: `pip install pre-commit`
2.  Setup: `pre-commit install` in repo root
3.  Manual run: `pre-commit run --all-files`

### Testing

*   **Unit Tests**:
    ```bash
    python -m unittest src/boabro/test_boabro.py
    ```
    Or with pytest:
    ```bash
    pytest src/boabro/test_boabro.py
    ```
    Hatch users:
    ```bash
    hatch run default:test       # Tests
    hatch run default:test-cov   # Coverage
    ```

*   **Manual Testing**:
    1.  Start server: `python -m http.server 8080`
    2.  Open several examples from `docs/`
    3.  Test uploads and URLs
    4.  Check browser console for errors

### Dependencies

*   **Runtime**: `fontTools` (loaded by PyScript)
*   **Development**: Linters, formatters, test runners in `pyproject.toml`

### Contributing

*   **Bugs/Enhancements**: Open GitHub issues
*   **Examples**: Improve or add new ones
*   **Code**:
    1.  Fork, create branch
    2.  Follow style (`ruff`), pass tests, add unit tests
    3.  Pre-commit checks must pass
    4.  Submit pull request
    Focus: browser-based font analysis, PyScript demonstrations

## Progress Tracking

See:
*   **`PROGRESS.md`**: Completed tasks and milestones
*   **`TODO.md`**: Pending work and known issues

## License

MIT License. See `LICENSE` file.

## Author

Adam Twardoch ([adam+github@twardoch.com](mailto:adam+github@twardoch.com))