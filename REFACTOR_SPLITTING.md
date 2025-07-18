# Refactoring Plan: Splitting Large Code Files

This document outlines a meticulous plan for a junior software developer to split large code files within the `boabro` project into smaller, more manageable units. The primary goal is to improve code organization, readability, and maintainability while ensuring that all existing functionality remains absolutely intact.

## I. General Principles for Code Splitting

Before starting, understand these core principles:

1.  **Modularity**: Identify logical blocks of code (e.g., CSS styles, JavaScript functions, Python classes/functions) that can operate independently or with minimal dependencies on other parts of the file.
2.  **Separation of Concerns**: HTML for structure, CSS for styling, JavaScript for interactivity, and Python for application logic should ideally reside in separate files.
3.  **Maintain Functionality**: After each step, verify that the application still works exactly as before. Use a local web server (`python -m http.server 8080`) and test thoroughly in a browser.
4.  **Clear Naming**: Use descriptive names for new files that reflect their content and purpose (e.g., `pyscript-puepy-bulma.css`, `pyscript-puepy-bulma.js`, `pyscript-puepy-bulma.py`).
5.  **Relative Paths**: When linking to new files, use relative paths from the HTML document.
6.  **Version Control**: Commit changes frequently, especially after successfully completing each major step (e.g., "Extract CSS for bulma.html").

## II. Detailed Plan for Specific Files

### A. Splitting `docs/pyscript-puepy-bulma.html` (43 KB)

This file is a prime candidate for splitting due to its size and embedded CSS, JavaScript, and Python.

**Current Structure Overview:**
-   HTML boilerplate and structure.
-   Extensive CSS rules within a `<style>` block.
-   PyScript configuration (`<py-config>`).
-   Python application logic within a `<script type="py">` block, including a PuePy `FontInspector` class with multiple methods.
-   JavaScript for UI interactions (navbar, modals, file selection, preset fonts) within a `<script>` block.

**Refactoring Steps:**

#### Step 1: Prepare Directories

1.  **Action**: Create new directories to house the extracted files.
    -   `mkdir -p /Users/adam/Developer/vcs/github.twardoch/pub/boabro/docs/css`
    -   `mkdir -p /Users/adam/Developer/vcs/github.twardoch/pub/boabro/docs/js`
    -   `mkdir -p /Users/adam/Developer/vcs/github.twardoch/pub/boabro/docs/py`

#### Step 2: Extract CSS

1.  **Action**: Open `/Users/adam/Developer/vcs/github.twardoch/pub/boabro/docs/pyscript-puepy-bulma.html`.
2.  **Action**: Locate the entire `<style>` block (including the `<style>` and `</style>` tags).
3.  **Action**: Cut the *entire content* of this `<style>` block.
4.  **Action**: Create a new file: `/Users/adam/Developer/vcs/github.twardoch/pub/boabro/docs/css/pyscript-puepy-bulma.css`.
5.  **Action**: Paste the cut CSS content into `pyscript-puepy-bulma.css`.
6.  **Action**: In `pyscript-puepy-bulma.html`, replace the original `<style>...</style>` block with a `<link>` tag to reference the new CSS file:
    ```html
    <link rel="stylesheet" href="./css/pyscript-puepy-bulma.css">
    ```
7.  **Verification**:
    -   Save both files.
    -   Start your local web server (`python -m http.server 8080`).
    -   Open `http://localhost:8080/docs/pyscript-puepy-bulma.html` in your browser.
    -   Visually inspect the page to ensure all styling (colors, layout, fonts, button styles, etc.) is identical to before the change. Check both dark and light themes if applicable.
    -   Check the browser's developer console for any errors related to loading the CSS file.

#### Step 3: Extract JavaScript

1.  **Action**: Open `/Users/adam/Developer/vcs/github.twardoch/pub/boabro/docs/pyscript-puepy-bulma.html`.
2.  **Action**: Locate the JavaScript code block at the very end of the `<body>` section (the one starting with `document.addEventListener('DOMContentLoaded', ...)` and containing UI interaction logic).
3.  **Action**: Cut the *entire content* of this `<script>` block (excluding the `<script>` and `</script>` tags themselves).
4.  **Action**: Create a new file: `/Users/adam/Developer/vcs/github.twardoch/pub/boabro/docs/js/pyscript-puepy-bulma.js`.
5.  **Action**: Paste the cut JavaScript content into `pyscript-puepy-bulma.js`.
6.  **Action**: In `pyscript-puepy-bulma.html`, replace the original `<script>...</script>` block with a `<script src>` tag to reference the new JavaScript file. Ensure it's placed *after* the PyScript `<script type="py">` tag if the JavaScript relies on PyScript being loaded:
    ```html
    <script src="./js/pyscript-puepy-bulma.js"></script>
    ```
7.  **Verification**:
    -   Save both files.
    -   Refresh `http://localhost:8080/docs/pyscript-puepy-bulma.html` in your browser.
    -   Test all UI interactions: navbar burger menu, help modal, file upload, URL input, process button, preview text/size changes, reset button. Ensure everything functions exactly as before.
    -   Check the browser's developer console for any JavaScript errors.

#### Step 4: Extract Python

1.  **Action**: Open `/Users/adam/Developer/vcs/github.twardoch/pub/boabro/docs/pyscript-puepy-bulma.html`.
2.  **Action**: Locate the `<script type="py">` block.
3.  **Action**: Cut the *entire content* of this `<script type="py">` block (excluding the `<script type="py">` and `</script>` tags themselves, but *including* the `config='...'` attribute).
4.  **Action**: Create a new file: `/Users/adam/Developer/vcs/github.twardoch/pub/boabro/docs/py/pyscript-puepy-bulma.py`.
5.  **Action**: Paste the cut Python content into `pyscript-puepy-bulma.py`.
6.  **Action**: In `pyscript-puepy-bulma.html`, modify the `<script type="py">` tag to use the `src` attribute, pointing to the new Python file. Ensure the `config` attribute is retained on the HTML tag:
    ```html
    <script type="py" src="./py/pyscript-puepy-bulma.py" config='{"packages":["puepy","fonttools"], "paths": ["../../src"]}'></script>
    ```
    **Important**: The `paths = ["../../src"]` in the `config` is crucial for `boabro.boabro` imports to work correctly from the new Python file's location.
7.  **Verification**:
    -   Save both files.
    -   Refresh `http://localhost:8080/docs/pyscript-puepy-bulma.html` in your browser.
    -   Test the core functionality: upload a font file, process a URL, change preview text/size, reset. Ensure all font analysis and display works correctly.
    -   Check the browser's developer console for any PyScript or Python-related errors.

### B. Splitting Other HTML Files (e.g., `docs/pyscript-puepy-bootstrap.html`, `docs/pyscript-puepy-frankenui.html`, etc.)

Apply the same "Extract CSS, Extract JavaScript, Extract Python" strategy as detailed for `pyscript-puepy-bulma.html` to the other large HTML files.

**Key Considerations for other HTML files:**
-   **CSS**: The CSS might be different for each framework. Ensure you extract the correct `<style>` block for each file.
-   **JavaScript**: The JavaScript interaction logic might vary. Extract the relevant `<script>` blocks.
-   **Python**: The Python code within `<script type="py">` might have different class names or methods depending on the UI framework. Ensure the `config` attribute (especially `packages` and `paths`) is correctly transferred to the new `<script type="py" src="...">` tag.
-   **Shared Python Logic**: Many of these Python scripts already import from `boabro.boabro`. This is good, as `boabro.boabro` is already a centralized module.

### C. Refactoring `src/boabro/boabro.py` (14 KB)

This file contains core font analysis utilities and some generic placeholder code.

**Current Structure Overview:**
-   `Config` dataclass.
-   `fetch_font_bytes_from_url`: Core utility for fetching font data.
-   `analyze_font_data`: Core utility for analyzing font data.
-   `process_data`: Generic placeholder function.
-   `main`: Example entry point.

**Refactoring Steps:**

#### Step 1: Isolate Core Utilities

1.  **Action**: Keep `Config`, `fetch_font_bytes_from_url`, and `analyze_font_data` in `src/boabro/boabro.py`. These are the core, reusable components of the `boabro` library.

#### Step 2: Extract Generic/CLI Logic

1.  **Decision**: The `process_data` and `main` functions appear to be generic or serve as a basic command-line entry point. To keep the core `boabro.py` focused on its primary responsibility (font analysis utilities), these should be moved.
2.  **Action**: Create a new file: `/Users/adam/Developer/vcs/github.twardoch/pub/boabro/src/boabro/__main__.py`.
3.  **Action**: Cut the `process_data` function and the `main` function (including the `if __name__ == "__main__":` block) from `src/boabro/boabro.py`.
4.  **Action**: Paste the cut code into `src/boabro/__main__.py`.
5.  **Action**: In `src/boabro/__main__.py`, add necessary imports from `boabro.boabro` if `process_data` or `main` rely on functions defined there (e.g., `from .boabro import Config, process_data`).
6.  **Verification**:
    -   Save both files.
    -   Run `python -m boabro` from the project root (or `python src/boabro/__main__.py`). Ensure it executes without errors (it should run the example `main` function).
    -   Crucially, re-test all HTML examples that import `boabro.boabro` (e.g., `pyscript-puepy-bulma.html`). Ensure they still function correctly, as they should only be importing the core utilities and not the `main` or `process_data` functions.

## III. Post-Refactoring Verification

After completing all splitting tasks:

1.  **Full Regression Test**: Systematically open and test *every* HTML file in the `docs/` directory.
    -   Upload local font files.
    -   Test URL fetching (especially the default GitHub URL).
    -   Interact with all UI elements (buttons, sliders, tabs, modals).
    -   Check the browser's developer console for *any* errors (JavaScript, Python, network, CSS loading).
2.  **Code Review**: Perform a self-review or request a peer review to ensure:
    -   No functionality was lost.
    -   Code is logically separated.
    -   File paths are correct.
    -   Imports/links are updated.
    -   Naming conventions are consistent.
3.  **Documentation Update**: Update `README.md` and any other relevant documentation to reflect the new file structure and how to run/develop with the refactored code.

This meticulous approach will ensure a smooth refactoring process and maintain the integrity of the `boabro` project.
