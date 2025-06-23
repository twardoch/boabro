# Boabro - Font Analysis Tool Examples

This directory contains various implementations of browser-based font analysis tools, primarily using Python via PyScript. Each example demonstrates a different approach to UI integration or a specific PyScript feature.

All examples leverage the core font analysis logic from `src/boabro/boabro.py`.

## Font Inspector Implementations

1.  **`_pyscript-alpinejs.html`**: Font analysis tool using PyScript with Alpine.js for lightweight reactive components.
2.  **`_pyscript-fs.html`**: Demonstrates PyScript's capabilities for interacting with a virtual filesystem to load and analyze fonts.
3.  **`_pyscript-htmx.html`**: Font inspector combining PyScript with HTMX for AJAX interactions. Uses Bootstrap for styling.
4.  **`_pyscript-indexeddb.html`**: Example showing PyScript integration with the browser's IndexedDB for potential local storage of font data or results.
5.  **`_pyscript-lit.html`**: PyScript integrated with Lit, a library for building lightweight Web Components.
6.  **`_pyscript-preact-signals.html`**: Font inspector using PyScript and Preact with Signals for state management.
7.  **`_pyscript-tailwindcss.html`**: A font inspector web application using PyScript with Tailwind CSS for styling.
8.  **`_pyscript-vuejs.html`**: Font analysis tool combining PyScript with Vue.js for reactive UI components.
9.  **`_pyscript-webcomponents.html`**: Font inspector using PyScript with native Web Components for modular UI.
10. **`_pyscript-worker.html`** (with `_pyscript-worker-script.py`): Demonstrates running font analysis in a Web Worker using PyScript, improving UI responsiveness.
11. **`_pyscript-workerspool.html`** (with `_pyscript-pool-worker.py`): Shows a pool of PyScript Web Workers for potentially parallelizing tasks (though font analysis is typically serial per font).
12. **`gradio.html`**: Font analysis interface built with Gradio-Lite, running entirely in the browser.
13. **`pyscript-mako.html`**: Implementation using PyScript with Mako templates for server-side style templating rendered in the browser.
14. **`pyscript-puepy-bootstrap.html`**: Font inspector built with PyScript and PuePy, styled with Bootstrap 5.
15. **`pyscript-puepy-bulma.html`**: Font inspector built with PyScript and PuePy, styled with Bulma.
16. **`pyscript-puepy-frankenui.html`**: Font inspector built with PyScript and PuePy, styled with FrankenUI.
17. **`pyscript-puepy-uikit.html`**: Font inspector built with PyScript and PuePy, styled with UIkit.
18. **`stlite.html`**: Streamlit implementation of the font analyzer, running in the browser with Stlite (Streamlit-lite).

### Experimental/Other Examples:
*   **`pyodide-react.jsx`**: A React-based implementation. (Note: Uses JSX and may require a build step or specific environment if run outside a compatible setup).
*   **`pyscript-solidjs.html`**: Font analysis application using PyScript with SolidJS. (May require specific setup or be experimental).
*   **`pyscript-svelte.html`**: PyScript implementation with Svelte. (May require specific setup or be experimental).

### Supporting Files:
*   **`testfont.ttf`**: A test font file used by some examples.

## Common Features

Most of these implementations provide similar core functionality:

- Upload TTF/OTF/WOFF/WOFF2 font files directly.
- Analyze fonts from URLs (subject to CORS).
- Display basic font information (family name, subfamily, version, etc.).
- Show metadata like Units Per Em (UPM) and glyph count.
- List all available OpenType tables.
- Display name table entries.
