# Boabro Documentation Files

This directory contains various implementations of font analysis tools using Python in the browser.

## Font Inspector Implementations

1. **pyodide-tailwindcss.html** - A font inspector web application using Pyodide (Python in the browser) with Tailwind CSS for styling. It allows users to upload TTF/OTF font files or provide URLs to analyze font properties like family name, UPM, glyphs count, and name table entries.

2. **pyodide-worker.html** - A font analysis tool using Web Workers with Pyodide to offload Python processing to a separate thread. This improves UI responsiveness while analyzing fonts. Uses Bootstrap for styling.

3. **pyodide-worker.js** - The Web Worker JavaScript file that handles the Pyodide Python environment initialization and font analysis processing. This works alongside pyodide-worker.html.

4. **pyscript-vuejs.html** - A font analysis tool combining PyScript (for Python in browser) with Vue.js for reactive UI components.

5. **pyscript-preact-signals.html** - Font inspector implementation using PyScript and Preact with Signals for state management.

6. **pyscript-puepy-bulma.html** - Font inspector using PyScript with the Bulma CSS framework and PueJS for UI structure.

7. **pyscript-puepy-uikit.html** - Font analysis tool using PyScript with UIKit CSS framework.

8. **pyscript-htmx.html** - Font inspector combining PyScript with HTMX for simple AJAX interactions without full JavaScript frameworks. Uses Bootstrap for styling.

9. **pyscript-puepy-bootstrap.html** - Font inspector with PyScript, Bootstrap 5 for UI components, and PueJS.

10. **pyodide-react.jsx** - React-based implementation of the font inspector using Pyodide for Python processing.

11. **pyscript-solidjs.html** - Font analysis application using PyScript with SolidJS for reactive UI.

12. **pyscript-svelte.html** - PyScript implementation with Svelte framework for UI components.

13. **pyscript-puepy-frankenui.html** - A custom UI implementation combining PyScript with various UI components.

14. **testfont.ttf** - A test font file for demonstration purposes.

15. **stlite.html** - Streamlit implementation of the font analyzer, running in the browser with Stlite (Streamlit-lite).

16. **pyscript-alpinejs.html** - Font analysis tool using PyScript with AlpineJS for lightweight reactive components.

17. **gradio.html** - Font analysis interface built with Gradio, which simplifies building ML/data science UIs.

18. **pyscript-mako.html** - Implementation using PyScript with Mako templates for rendering.

19. **pyodide-fs.html** - Font analyzer with file system access capabilities using Pyodide.

20. **pyscript-indexeddb.html** - Font analyzer with browser's IndexedDB integration for local storage of fonts.

21. **pyodide-workerspool.html** - Font analysis tool using a pool of Web Workers with Pyodide for parallel processing.

22. **pyscript-webcomponents.html** - Font inspector using PyScript with Web Components for modular, reusable UI elements.

23. **pyscript-lit.html** - Implementation using PyScript with Lit (a lightweight library for building web components).

## Common Features

All these implementations provide similar functionality:

- Upload TTF/OTF font files directly
- Analyze fonts from URLs
- Display basic font information (family name, subfamily, version)
- Show metadata like Units Per Em (UPM) and glyph count
- List all available OpenType tables
- Display the full name table entries with IDs and platform information

## Directory Structure

- **new/** - A directory containing development files:
  - `.DS_Store` - macOS system file for folder attributes
  - `.specstory` - Configuration or specification file for a new version
