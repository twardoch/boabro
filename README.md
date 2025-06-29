# Boabro - Browser-based Font Analysis Tools

Boabro is a versatile toolkit that empowers you to analyze font files (such as TTF, OTF, WOFF, and WOFF2) directly within your web browser. It leverages the power of Python and the robust `fontTools` library, all running seamlessly on the client-side thanks to [PyScript](https://pyscript.net/).

## What does Boabro do?

At its core, Boabro allows you to:

*   **Inspect Font Details**: Upload a font file or provide a URL, and Boabro will dissect it to reveal comprehensive information.
*   **View Metadata**: Access essential details like family name, style, version, manufacturer, designer, and license information.
*   **Explore Font Tables**: Examine the underlying OpenType tables (the data structures that define a font's appearance and behavior) that define the font's structure and features.
*   **Check Key Metrics**: Get insights into units per em (UPM), glyph counts, and more.
*   **Run Anywhere**: Because it runs in the browser, you can use it on almost any device with a modern web browser, without needing to install specialized font software.

## Who is Boabro for?

Boabro is designed for a wide range of users, including:

*   **Web Developers & Designers**: Quickly check font details, troubleshoot web font issues, or verify font characteristics without leaving the browser.
*   **Typographers & Font Engineers**: Perform quick analyses and inspections of font files during the design or testing process.
*   **Students & Educators**: Learn about font structures and OpenType features in an accessible, interactive way.
*   **Anyone Curious About Fonts**: If you've ever wanted to peek inside a font file, Boabro makes it easy.

## Why is Boabro useful?

*   **Zero Installation**: No need to download or install dedicated font software. It runs directly in your browser.
*   **Client-Side Processing**: All analysis happens on your computer (meaning analysis happens in your browser, not on a remote server for local files), ensuring privacy and speed.
*   **Python Powered**: Demonstrates how powerful Python libraries like `fontTools` can be used for complex tasks directly in a web environment.
*   **UI Flexibility**: Showcases integration with a diverse set of modern web UI technologies and approaches, making it a great learning resource for developers interested in PyScript.
*   **Cross-Platform**: Works on any operating system with a compatible web browser.

## Getting Started & Installation

Boabro is primarily a collection of demonstration tools rather than a traditional installable library. To explore its capabilities:

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/twardoch/boabro.git
    cd boabro
    ```

2.  **Start a Local Web Server**:
    Since the tools run in your browser, you need a local HTTP server to serve the files. Python's built-in server is a simple option:
    ```bash
    python -m http.server 8080
    # Or use any other simple HTTP server like 'npx serve'
    ```

3.  **Access the Tools**:
    Open your web browser and navigate to the `docs` directory, typically:
    ```
    http://127.0.0.1:8080/docs/
    ```
    You'll find a list of HTML files. Click on any of them to launch a specific font analysis tool. For example, to view the PuePy Bulma example, navigate to `http://127.0.0.1:8080/docs/pyscript-puepy-bulma.html`.

## How to Use Boabro

### Using the Example Tools (In-Browser)

The primary way to use Boabro is through the example HTML files located in the `docs/` directory. Each file demonstrates a different UI setup or feature:

*   **Upload or Fetch**: Most tools will provide an interface to either upload a font file from your computer or fetch one from a URL.
*   **View Analysis**: Once the font is loaded, the tool will display the analyzed information, often categorized into sections like metadata, table summaries, etc.

Some of the available examples include integrations with:
*   **PuePy** (with Bootstrap, Bulma, UIkit, FrankenUI)
*   **Alpine.js**, **Lit**, **Preact**, **HTMX**, **Vue.js**, **Web Components**
*   **Gradio-Lite** and **Stlite** (standalone Streamlit in the browser)
*   Direct PyScript features like filesystem access, IndexedDB, and web workers.
*   The `docs` directory contains a comprehensive list, including:
    *   `_pyscript-alpinejs.html`
    *   `_pyscript-fs.html` (formerly `pyodide-fs.html`)
    *   `_pyscript-htmx.html`
    *   `_pyscript-indexeddb.html`
    *   `_pyscript-lit.html`
    *   `_pyscript-preact-signals.html`
    *   `_pyscript-tailwindcss.html` (formerly `pyodide-tailwindcss.html`)
    *   `_pyscript-vuejs.html`
    *   `_pyscript-webcomponents.html`
    *   `_pyscript-worker.html` (and `_pyscript-worker-script.py`)
    *   `_pyscript-workerspool.html` (and `_pyscript-pool-worker.py`)
    *   `pyscript-puepy-bootstrap.html`
    *   `pyscript-puepy-bulma.html`
    *   `pyscript-puepy-frankenui.html`
    *   `pyscript-puepy-uikit.html`
    *   `pyscript-mako.html`
    *   `pyscript-solidjs.html` (experimental)
    *   `pyscript-svelte.html` (experimental)
    *   `gradio.html`
    *   `stlite.html`
    *   `pyodide-react.jsx` (status may vary)


### Programmatic Usage (within PyScript/HTML)

If you are a developer looking to integrate Boabro's font analysis capabilities into your own PyScript-based projects:

1.  **Include `boabro.py`**: Ensure the `boabro.py` script (from `src/boabro/`) is accessible to your HTML page (e.g., by placing it in the same directory or configuring paths in PyScript).
2.  **Import Functions**: In your Python code within a `<py-script>` tag or a Python web worker, you can import and use the core functions:

    ```python
    # In your PyScript code
    from boabro import fetch_font_bytes_from_url, analyze_font_data
    # Font bytes can be obtained via fetch_font_bytes_from_url or by reading a local file.

    async def process_font_from_url(font_url):
        font_bytes = await fetch_font_bytes_from_url(font_url)
        if font_bytes:
            analysis_result = analyze_font_data(font_bytes, filename="myfont.otf")
            # Process and display the result (e.g., convert to JS object, update DOM)
            print(analysis_result)
        else:
            print(f"Could not fetch font from {font_url}")

    async def process_local_font_file(js_file_proxy):
        # 'js_file_proxy' typically comes from an event listener on an <input type="file">.
        # It's a Pyodide proxy for the JavaScript File object.
        filename = js_file_proxy.name
        array_buffer = await js_file_proxy.arrayBuffer() # This is a JavaScript ArrayBuffer
        font_bytes = array_buffer.to_bytes() # Convert to Python bytes

        if font_bytes:
            analysis_result = analyze_font_data(font_bytes, filename=filename)
            # Process and display the result
            print(analysis_result)
    ```

    The `fetch_font_bytes_from_url` function is designed to retrieve font data from a URL, handling potential CORS issues. The `analyze_font_data` function takes the font file's raw bytes and an optional filename, returning a dictionary with detailed font information.

### Command-Line Usage

The `src/boabro/boabro.py` script itself is primarily a module intended for use within a PyScript environment. While it can be executed (`python src/boabro/boabro.py`), its `main()` function is currently a basic placeholder and does not offer command-line font analysis features. The core value lies in its functions being callable from browser-based Python.

---

## Technical Deep Dive & Contributing

This section provides a more detailed look into Boabro's architecture and guidelines for developers and contributors.

### How the Code Works

#### Core Logic (`src/boabro/boabro.py`)

The heart of Boabro's analysis capabilities resides in `src/boabro/boabro.py`. This module is designed to be used within a PyScript environment.

*   **`fetch_font_bytes_from_url(url_str: str) -> Optional[bytes]`**:
    *   This asynchronous function retrieves font file bytes from a URL.
    *   It attempts GitHub raw URL conversion, then iterates through known CORS proxies, followed by a direct fetch, and finally a `mode="no-cors"` attempt.
    *   Uses `pyodide.http.pyfetch` and includes common HTTP headers.
    *   Returns `bytes` or `None`.

*   **`analyze_font_data(font_bytes: bytes, filename: Optional[str] = "font") -> Dict[str, Any]`**:
    *   Parses font `bytes` using `fontTools.ttLib.TTFont`.
    *   Extracts:
        *   Common name table entries (NameIDs 1-14, 16-25).
        *   `upm` (unitsPerEm).
        *   `numGlyphs`.
        *   Sorted list of table tags.
        *   All `nameTableRecords` with decoded strings.
    *   Returns a dictionary of font information. Errors are logged and re-raised.

*   **Logging**:
    *   Uses Python's `logging` module. `util_logger` for module-specific logs.
    *   `_log_util_debug` helper attempts to also log to `js.console.log` in PyScript.

#### PyScript Integration

Python code runs in-browser via [PyScript](https://pyscript.net/)/[Pyodide](https://pyodide.org/), compiling Python and `fontTools` to WebAssembly. This enables client-side analysis. `fontTools` and other packages are declared in PyScript configuration (e.g., `<py-config>`).

#### UI Examples (`docs/`)

The `docs/` directory contains HTML examples integrating `boabro.py` with various UI libraries/patterns. They handle UI, call core functions, and display results.

**File Naming Convention in `docs/`**:
*   PyScript examples: `_pyscript-[feature_or_framework].html`.
*   PuePy examples: `pyscript-puepy-[css_framework].html`.
*   Standalone tools: e.g., `gradio.html`.

### Project Structure

*   **`src/boabro/`**: Core Python source (`boabro.py`, `test_boabro.py`).
*   **`docs/`**: Runnable HTML examples (see list in "Using the Example Tools").
*   **`tests/`**: Broader package-level tests (minimal).
*   **`pyproject.toml`**: Project metadata, dev dependencies, build (Hatch), tool configs.
*   **`.pre-commit-config.yaml`**: Pre-commit hook configuration.
*   **`README.md`**: This file.
*   **`LICENSE`**: MIT License.
*   **`PROGRESS.md`**, **`TODO.md`**: Project tracking.

### Development Environment Setup

1.  **Python**: Python 3.10+.
2.  **Clone Repository**.
3.  **Virtual Environment (Recommended)**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    ```
    Or with [Hatch](https://hatch.pypa.io/latest/):
    ```bash
    hatch env create dev
    hatch shell dev
    ```
4.  **Install Development Dependencies**:
    If using Hatch, the previous step handles this. Otherwise, using pip:
    ```bash
    pip install -r requirements-dev.txt
    ```
    Alternatively, for an editable install with development and test dependencies (ensure pip is up-to-date):
    ```bash
    pip install -e .[dev,test]
    ```
    Development dependencies are listed in `pyproject.toml`.

### Code Quality & Pre-commit Hooks

Uses `ruff` for linting/formatting and `mypy` for type checking (configs in `pyproject.toml`).

**Pre-commit Hooks**:
Automatically run checks (e.g., `ruff`) before commits.
1.  **Install `pre-commit`**: `pip install pre-commit` (included in dev dependencies).
2.  **Install Git Hooks**: In repo root, run `pre-commit install`.
    Manual run: `pre-commit run --all-files`.

### Testing

*   **Unit Tests**: For `src/boabro/boabro.py` are in `src/boabro/test_boabro.py`.
    ```bash
    python -m unittest src/boabro/test_boabro.py
    ```
    Or with `pytest` (from dev dependencies):
    ```bash
    pytest src/boabro/test_boabro.py
    ```
    Hatch users (scripts defined in `pyproject.toml` under `tool.hatch.envs.default.scripts`):
    ```bash
    hatch run default:test       # Runs tests
    hatch run default:test-cov # For test coverage
    ```

*   **Manual Smoke Testing**: Crucial after changes to `boabro.py` or `docs/` examples.
    1.  Start local HTTP server (`python -m http.server 8080`).
    2.  Open several HTML examples from `docs/`.
    3.  Test local file uploads and font URLs.
    4.  Check browser developer console for errors.

### Dependencies

*   **Runtime (In-Browser)**: `fontTools`, loaded by PyScript as per HTML `<py-config>`.
*   **Development**: Linters, formatters, test runners, build tools in `pyproject.toml` (`[project.optional-dependencies.dev]`, `[project.optional-dependencies.test]`).

### Contributing

Contributions are welcome!
*   **Bugs/Enhancements**: Open an issue on GitHub.
*   **Examples**: Improve existing or create new ones.
*   **Code Contributions**:
    1.  Fork, create a branch.
    2.  Make changes, adhere to style (`ruff`), ensure tests pass. Add unit tests for new logic.
    3.  Ensure pre-commit checks pass.
    4.  Submit a pull request.
    Align with project goals: browser-based font analysis, showcasing PyScript.

---

## Progress Tracking & Development Status

Project progress and status are tracked in:
*   **`PROGRESS.md`**: Detailed report of completed tasks and milestones.
*   **`TODO.md`**: Pending tasks, planned features, and known issues.
Refer to these for the latest updates.

## License

This project is licensed under the MIT License. See the `LICENSE` file for full details.

## Author

Boabro is created and maintained by Adam Twardoch ([adam+github@twardoch.com](mailto:adam+github@twardoch.com)).
