# Boabro - Browser-based Font Analysis Tools

This repository contains a collection of browser-based font analysis tools using various Python-to-JavaScript frameworks and libraries.

## Project Overview

Boabro is a comprehensive browser-based font analysis tool that leverages Python in the browser through technologies like Pyodide and PyScript. It allows users to analyze font files (TTF/OTF) directly in their web browser without requiring server-side processing or installation.

### Key Features

- **Browser-based Analysis**: Analyze font files directly in your web browser
- **Multiple UI Frameworks**: Implementations using various modern JavaScript frameworks
- **Font Information Display**: View detailed font metadata, name tables, and glyph information
- **File Upload & URL Support**: Analyze fonts from local files or remote URLs
- **Offline Capability**: Works without an internet connection once loaded

### Technical Implementation

Boabro demonstrates how to use Python for font analysis in the browser through multiple implementation approaches:

- **Python in the Browser**: Uses [Pyodide](https://pyodide.org/) and [PyScript](https://pyscript.net/) to run Python code directly in the browser
- **Font Analysis**: Leverages [fontTools](https://github.com/fonttools/fonttools) Python library for font parsing and analysis
- **UI Frameworks**: Multiple implementations using different JavaScript frameworks and libraries

## Project Structure

The main tools are located in the `docs` directory and follow a specific naming convention:

- **Framework-specific tools**:
  - `gradio.html` - Font Inspector using Gradio-Lite
  - `stlite.html` - Font Analyzer using Stlite (Streamlit)

- **PyScript-based tools** (prefix: `pyscript-`):
  - `pyscript-puepy-bootstrap.html` - PuePy implementation with Bootstrap
  - `pyscript-puepy-bulma.html` - PuePy implementation with Bulma
  - `pyscript-puepy-uikit.html` - PuePy implementation with UIkit
  - `pyscript-puepy-frankenui.html` - PuePy implementation with FrankenUI
  - `pyscript-alpinejs.html` - PyScript with Alpine.js
  - `pyscript-htmx.html` - PyScript with HTMX
  - `pyscript-indexeddb.html` - PyScript with IndexedDB
  - `pyscript-lit.html` - PyScript with Lit
  - `pyscript-preact-signals.html` - PyScript with Preact Signals
  - `pyscript-solidjs.html` - PyScript with Solid.js
  - `pyscript-svelte.html` - PyScript with Svelte
  - `pyscript-vuejs.html` - PyScript with Vue.js
  - `pyscript-webcomponents.html` - PyScript with Web Components

- **Pyodide-based tools** (prefix: `pyodide-`):
  - `pyodide-worker.html` - Pyodide with Web Worker
  - `pyodide-workerspool.html` - Pyodide with Workers Pool
  - `pyodide-tailwindcss.html` - Pyodide with Tailwind CSS
  - `pyodide-streamlit-browser.html` - Pyodide with Streamlit in browser
  - `pyodide-wasm-notebooks.html` - Pyodide with WASM notebooks
  - `pyodide-fs.html` - Pyodide with filesystem support

## File Naming Convention

The HTML files follow a specific naming convention:

1. **Framework-specific tools**: Direct name of the framework
   - Example: `gradio.html`, `stlite.html`

2. **PyScript-based tools**: `pyscript-[framework].html`
   - Example: `pyscript-puepy-bootstrap.html`, `pyscript-vuejs.html`

3. **Pyodide-based tools**: `pyodide-[framework].html`
   - Example: `pyodide-worker.html`, `pyodide-fs.html`

## Renaming Script

The repository includes a script `rename_files.sh` to standardize the file naming convention. The script can be run with the following options:

```bash
./rename_files.sh [options]
```

Options:
- `--dry-run`: Show what would be done without making changes
- `--verbose`: Show more detailed output
- `-h, --help`: Show help message

## Getting Started

To run any of the examples:

1. Clone the repository:
   ```bash
   git clone https://github.com/twardoch/boabro.git
   cd boabro
   ```

2. Start a local web server:
   ```bash
   python -m http.server 8080
   ```

3. Open your browser and navigate to:
   ```
   http://127.0.0.1:8080/docs/
   ```

4. Select any of the HTML files to try different implementations.

## Progress Tracking

The project progress is tracked in the following files:
- `PROGRESS.md`: Detailed progress report with completed tasks and fixes
- `TODO.md`: List of pending tasks and issues to be addressed

## Development Status

The project is currently in active development. See `PROGRESS.md` for the latest updates and `TODO.md` for upcoming tasks.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Created by Adam Twardoch (adam+github@twardoch.com)