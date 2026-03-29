# Refactoring Plan: Splitting Large Code Files

This document outlines a plan for splitting large code files in the `boabro` project into smaller, more manageable units. The goal is to improve code organization, readability, and maintainability while preserving all existing functionality.

## I. General Principles for Code Splitting

Before starting, understand these core principles:

1.  **Modularity**: Identify logical blocks of code (CSS styles, JavaScript functions, Python classes/functions) that can operate independently or with minimal dependencies.
2.  **Separation of Concerns**: HTML for structure, CSS for styling, JavaScript for interactivity, and Python for application logic should reside in separate files.
3.  **Maintain Functionality**: After each step, verify that the application still works exactly as before. Use a local web server (`python -m http.server 8080`) and test thoroughly in a browser.
4.  **Clear Naming**: Use descriptive names for new files that reflect their content and purpose (e.g., `pyscript-puepy-bulma.css`, `pyscript-puepy-bulma.js`, `pyscript-puepy-bulma.py`).
5.  **Relative Paths**: When linking to new files, use relative paths from the HTML document.
6.  **Version Control**: Commit changes frequently, especially after completing each major step (e.g., "Extract CSS for bulma.html").

## II. Detailed Plan for Specific Files

### A. Splitting `docs/pyscript-puepy-bulma.html` (43 KB)

This file needs splitting due to its size and embedded CSS, JavaScript, and Python.

**Current Structure:**
- HTML boilerplate and structure
- CSS rules within a `<style>` block
- PyScript configuration (`<py-config>`)
- Python application logic in a `<script type="py">` block, including a PuePy `FontInspector` class
- JavaScript for UI interactions in a `<script>` block

**Refactoring Steps:**

#### Step 1: Prepare Directories

Create directories for extracted files:
```bash
mkdir -p /Users/adam/Developer/vcs/github.twardoch/pub/boabro/docs/css
mkdir -p /Users/adam/Developer/vcs/github.twardoch/pub/boabro/docs/js
mkdir -p /Users/adam/Developer/vcs/github.twardoch/pub/boabro/docs/py
```

#### Step 2: Extract CSS

1. Open `/Users/adam/Developer/vcs/github.twardoch/pub/boabro/docs/pyscript-puepy-bulma.html`
2. Locate and cut the entire `<style>` block
3. Create `/Users/adam/Developer/vcs/github.twardoch/pub/boabro/docs/css/pyscript-puepy-bulma.css`
4. Paste CSS content into the new file
5. Replace original `<style>` block with:
    ```html
    <link rel="stylesheet" href="./css/pyscript-puepy-bulma.css">
    ```

**Verification:**
- Save both files
- Start local server: `python -m http.server 8080`
- Open `http://localhost:8080/docs/pyscript-puepy-bulma.html`
- Visually inspect page styling (colors, layout, fonts, buttons)
- Check browser console for CSS loading errors

#### Step 3: Extract JavaScript

1. Open the HTML file
2. Locate JavaScript code block at end of `<body>` (starting with `document.addEventListener('DOMContentLoaded', ...`)
3. Cut entire content of `<script>` block (excluding tags)
4. Create `/Users/adam/Developer/vcs/github.twardoch/pub/boabro/docs/js/pyscript-puepy-bulma.js`
5. Paste JavaScript content into new file
6. Replace original `<script>` block with:
    ```html
    <script src="./js/pyscript-puepy-bulma.js"></script>
    ```
    Place after PyScript `<script type="py">` tag if JavaScript depends on PyScript

**Verification:**
- Save both files
- Refresh browser
- Test all UI interactions: navbar, modals, file upload, URL input, process button, preview changes, reset button
- Check browser console for JavaScript errors

#### Step 4: Extract Python

1. Open the HTML file
2. Locate `<script type="py">` block
3. Cut entire content (excluding tags, but including `config` attribute)
4. Create `/Users/adam/Developer/vcs/github.twardoch/pub/boabro/docs/py/pyscript-puepy-bulma.py`
5. Paste Python content into new file
6. Modify HTML tag to use `src` attribute:
    ```html
    <script type="py" src="./py/pyscript-puepy-bulma.py" config='{"packages":["puepy","fonttools"], "paths": ["../../src"]}'></script>
    ```

**Important**: The `paths = ["../../src"]` in `config` is essential for `boabro.boabro` imports to work correctly.

**Verification:**
- Save both files
- Refresh browser
- Test core functionality: font upload, URL processing, preview changes, reset
- Check browser console for PyScript or Python errors

### B. Splitting Other HTML Files

Apply the same strategy to other large HTML files (`docs/pyscript-puepy-bootstrap.html`, `docs/pyscript-puepy-frankenui.html`, etc.).

**Key Considerations:**
- CSS: Each framework may have different styles. Extract the correct `<style>` block
- JavaScript: Interaction logic varies by framework. Extract relevant `<script>` blocks
- Python: Code may have different class names or methods. Transfer `config` attribute correctly
- Shared Python Logic: Most scripts import from `boabro.boabro`, which remains centralized

### C. Refactoring `src/boabro/boabro.py` (14 KB)

This file contains core font analysis utilities and generic placeholder code.

**Current Structure:**
- `Config` dataclass
- `fetch_font_bytes_from_url`: Fetches font data
- `analyze_font_data`: Analyzes font data
- `process_data`: Generic placeholder function
- `main`: Example entry point

**Refactoring Steps:**

#### Step 1: Isolate Core Utilities

Keep `Config`, `fetch_font_bytes_from_url`, and `analyze_font_data` in `src/boabro/boabro.py`. These are reusable core components.

#### Step 2: Extract Generic/CLI Logic

Move `process_data` and `main` functions to separate the core library from CLI-specific code.

1. Create `/Users/adam/Developer/vcs/github.twardoch/pub/boabro/src/boabro/__main__.py`
2. Cut `process_data` and `main` functions from `src/boabro/boabro.py`
3. Paste into `src/boabro/__main__.py`
4. Add necessary imports in `__main__.py`:
    ```python
    from .boabro import Config, process_data
    ```

**Verification:**
- Save both files
- Run `python -m boabro` from project root
- Re-test HTML examples that import `boabro.boabro`

## III. Post-Refactoring Verification

After completing all splitting tasks:

1. **Full Regression Test**: Test every HTML file in `docs/` directory
    - Upload local font files
    - Test URL fetching (especially default GitHub URL)
    - Interact with all UI elements (buttons, sliders, tabs, modals)
    - Check browser console for any errors

2. **Code Review**: Verify:
    - No functionality lost
    - Code logically separated
    - File paths correct
    - Imports/links updated
    - Naming conventions consistent

3. **Documentation Update**: Update `README.md` and other documentation to reflect new file structure and development procedures

This approach maintains project integrity while improving code organization.