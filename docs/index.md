# Boabro - Font Analysis Tool Examples

This directory contains browser-based font analysis tools implemented primarily with Python via PyScript. Each example demonstrates a different UI approach or PyScript feature.

All examples use the core font analysis logic from `src/boabro/boabro.py`.

## Font Inspector Implementations

1. **`_pyscript-alpinejs.html`**: PyScript with Alpine.js for reactive components
2. **`_pyscript-fs.html`**: PyScript virtual filesystem interaction for font loading
3. **`_pyscript-htmx.html`**: PyScript + HTMX for AJAX interactions, styled with Bootstrap
4. **`_pyscript-indexeddb.html`**: PyScript + IndexedDB for local font data storage
5. **`_pyscript-lit.html`**: PyScript with Lit Web Components
6. **`_pyscript-preact-signals.html`**: PyScript + Preact with Signals for state management
7. **`_pyscript-tailwindcss.html`**: PyScript with Tailwind CSS styling
8. **`_pyscript-vuejs.html`**: PyScript + Vue.js for reactive UI
9. **`_pyscript-webcomponents.html`**: PyScript with native Web Components
10. **`_pyscript-worker.html`** (`_pyscript-worker-script.py`): Font analysis in a Web Worker for better UI responsiveness
11. **`_pyscript-workerspool.html`** (`_pyscript-pool-worker.py`): Pool of Web Workers (though font analysis is typically serial per font)
12. **`gradio.html`**: Font analysis with Gradio-Lite, running entirely in-browser
13. **`pyscript-mako.html`**: PyScript with Mako templates for browser-side templating
14. **`pyscript-puepy-bootstrap.html`**: PyScript + PuePy, styled with Bootstrap 5
15. **`pyscript-puepy-bulma.html`**: PyScript + PuePy, styled with Bulma
16. **`pyscript-puepy-frankenui.html`**: PyScript + PuePy, styled with FrankenUI
17. **`pyscript-puepy-uikit.html`**: PyScript + PuePy, styled with UIkit
18. **`stlite.html`**: Streamlit font analyzer running in-browser with Stlite

### Experimental/Other Examples:
* **`pyodide-react.jsx`**: React implementation (requires JSX build step or compatible environment)
* **`pyscript-solidjs.html`**: PyScript + SolidJS (experimental/setup dependent)
* **`pyscript-svelte.html`**: PyScript + Svelte (experimental/setup dependent)

### Supporting Files:
* **`testfont.ttf`**: Test font file used by several examples

## Common Features

Most implementations provide the same core functionality:

- Upload TTF/OTF/WOFF/WOFF2 font files
- Analyze fonts from URLs (CORS restrictions apply)
- Display basic font information (family name, subfamily, version)
- Show metadata (Units Per Em, glyph count)
- List OpenType tables
- Display name table entries