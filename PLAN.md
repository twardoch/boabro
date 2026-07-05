# Boabro Plan

## What Boabro is

A font inspector that runs where you already are: the browser. Drop a font on the
page, or point the CLI at a file, and `fontTools` parses it into names, metrics,
glyph counts, and the full OpenType table list — no server, no upload. The same
`analyze_font_data` function backs the web pages, the `boabro` CLI, and any script
that imports the module.

## Shape of the code

- `src/boabro/boabro.py` — the core: `fetch_font_bytes_from_url` (URL loading via
  GitHub-raw rewrite, CORS proxies, then direct/no-cors) and `analyze_font_data`
  (parse + extract). The browser-only imports (`js`, `pyodide`, `to_js`) degrade to
  plain-Python stand-ins so the module imports cleanly under pytest and the CLI.
- `src/boabro/__main__.py` — the `boabro` console script: text or JSON output.
- `docs/*.html` — one static PyScript page per UI framework, each importing the
  core module. Runtime pinned to a specific PyScript release.
- `tests/` — unit tests over the bundled `docs/testfont.ttf` plus network-free
  mocks of the fetch strategies.

## State after this pass

Green across ruff, mypy (strict), and pytest. Template scaffolding removed. Async
tests actually run in CI now (`pytest-asyncio` was missing). Three workflows do
three distinct jobs: `push.yml` builds and tests, `ci.yml` smoke-tests the web
pages, `release.yml` publishes to PyPI on a tag.

## Roadmap

Near-term work lives in `TODO.md`. The themes:

1. **Retire or repair the dead examples.** Five framework pages load but never
   render (`lit`, `preact-signals`, `webcomponents`, `solidjs`, `svelte`). Each is
   either fixed to import the core module cleanly or removed — a broken example
   teaches the wrong thing.
2. **An offline end-to-end test.** One Playwright run that drives a real page with
   the bundled font and asserts the family name appears, with no dependence on live
   font URLs or CDN availability in the assertions.
3. **Deeper analysis, kept honest.** Surface `GSUB`/`GPOS` feature tags; add a CLI
   `--compare` that diffs two fonts. Only what earns its place — no plugin
   framework, no PWA, no bundler.
