# TODO

Near-term, honest work. Bigger ideas at the bottom. See `PLAN.md` for detail.

## Broken web examples

These pages load but never render results. Fix or retire each:

- [ ] `_pyscript-lit.html` — processing hangs after file selection
- [ ] `_pyscript-preact-signals.html` — "pyscript is not defined" on click
- [ ] `_pyscript-webcomponents.html` — spinner never resolves
- [ ] `pyscript-solidjs.html` — Babel/module loading fails; likely retire
- [ ] `pyscript-svelte.html` — needs a compile step a browser-only page can't do; likely retire

## Tests

- [ ] Add a Playwright end-to-end test that loads one page, feeds it the bundled
      `docs/testfont.ttf`, and asserts the family name renders. Keep it offline —
      no live font URLs, no CDN dependence in assertions.

## Docs

- [ ] Add a short "which page should I open?" table to `docs/` — the framework
      variants need a map for newcomers.

## Bigger ideas

- [ ] Show OpenType layout features (`GSUB`/`GPOS` feature tags), not just the
      table list.
- [ ] A `--compare a.ttf b.ttf` CLI mode that diffs metadata and table sets.
- [ ] Cache working CORS proxies within a session instead of retrying the full
      list every fetch.
