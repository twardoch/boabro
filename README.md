# boabro

Crack open any font file in your browser. No installs, no uploads, no server.

Boabro runs Python and the `fontTools` library entirely in the browser using [PyScript](https://pyscript.net/). Drop a font file on the page — or paste a URL — and it shows you everything inside: names, metrics, glyph counts, all OpenType tables.

## What it does

Load a font from a local file or a remote URL and get back:

- **Identity**: family name, PostScript name, version string, manufacturer, designer, license
- **Metrics**: Units Per Em (the design grid size), number of glyphs
- **Structure**: which OpenType tables are present (e.g. `glyf`, `CFF `, `GPOS`, `GSUB`, `fvar`)
- **Full name table**: every raw name record with platform and language IDs

All of this happens in your browser tab. Nothing leaves your machine except the optional URL fetch.

## Who it's for

- **Web developers** debugging why a WOFF2 looks wrong — check the actual names and metrics without installing anything
- **Type designers** doing a quick sanity check on a build — confirm the right version string made it in
- **Font engineers** poking at table structures without firing up a dedicated font editor
- **The curious** — a font file is surprisingly readable once you know what to look for

## How it works

PyScript embeds a Python interpreter (via WebAssembly/Pyodide) directly in the page. `fontTools` — the standard Python library for parsing OpenType fonts — runs inside that interpreter. The `boabro.py` module handles:

1. Fetching font bytes from a URL (trying GitHub raw URLs, then CORS proxies, then direct fetch)
2. Parsing with `fontTools.ttLib.TTFont`
3. Extracting name table records, head table metrics, and the full glyph order
4. Returning a structured dict the browser page can render

## Running locally

Clone the repo and open any HTML file in `examples/` in a modern browser:

```bash
git clone https://github.com/twardoch/boabro
cd boabro
# open examples/index.html in your browser
```

No build step. No `npm install`. The PyScript runtime loads from a CDN.

## Using the Python module

The core analysis logic is importable as a regular Python module for non-browser use:

```python
from boabro.boabro import analyze_font_data

with open("MyFont.ttf", "rb") as f:
    font_bytes = f.read()

info = analyze_font_data(font_bytes, filename="MyFont.ttf")
print(info["familyName"])   # e.g. "MyFont"
print(info["numGlyphs"])    # e.g. 512
print(info["tables"])       # ['GDEF', 'GPOS', 'GSUB', 'OS/2', 'cmap', 'glyf', ...]
```

## OpenType basics for the uninitiated

A font file is not a collection of images. It is a structured binary file containing:

- **Outline data** (`glyf` for TrueType, `CFF ` for PostScript): the actual letter shapes as mathematical curves
- **Metrics tables** (`hhea`, `OS/2`, `hmtx`): advance widths, vertical alignment, line spacing
- **Layout tables** (`GSUB`, `GPOS`): rules for ligatures, kerning, and complex script shaping
- **Name table**: human-readable strings — family name, version, copyright, designer URL
- **`head` table**: fundamental values including Units Per Em (UPM), the coordinate system scale

UPM is the denominator that makes everything else make sense: if UPM is 1000, then an ascender of 800 means "80% of the cap height". Common values are 1000 (PostScript) and 2048 (TrueType).

## License

MIT
