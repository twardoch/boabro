#!/usr/bin/env -S uv run --script
# pyright: reportMissingImports=false, reportAttributeAccessIssue=false
# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "pywebview",
#     "pywebview-htmx",
#     "webview-proc",
# ]
# ///

"""File Drop Utility – pywebview-htmx + Xel + Tailwind CSS + Lucide + Alpine.js.

Combines pywebview-htmx's declarative py-call/py-target/py-swap attributes
with Xel web components, Tailwind CSS utilities, Lucide icon assets, and
Alpine.js for local UI state.

- pywebview-htmx: wires toolbar controls to Python methods returning HTML
  fragments; the runtime JS handles DOM swaps automatically.
- Xel: native-like desktop controls (x-buttons, x-button, x-switch, x-label).
- Tailwind CSS: utility-first layout and spacing.
- Lucide: SVG icon paths embedded as data URIs for x-icon.
- Alpine.js: manages drop-zone drag-over visual state declaratively.

webview-proc is a dependency for thread-isolated startup patterns.
On macOS the main thread owns the event loop, so we call webview.start()
directly.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

import webview
import webview_proc  # noqa: F401
from pywebview_htmx import inject_runtime
from webview.dom import DOMEventHandler

IMAGE_EXTENSIONS: set[str] = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".tiff",
    ".webp",
    ".svg",
    ".ico",
}


def _html_escape(text: str) -> str:
    """Minimal HTML entity escaping for untrusted path strings."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


HTML = """\
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="xel-theme" content="https://cdn.jsdelivr.net/npm/xel@0.41.1/themes/adwaita-dark.css">
<meta name="xel-icons" content="https://cdn.jsdelivr.net/npm/xel@0.41.1/icons/fluent-outlined.svg">
<script src="https://cdn.jsdelivr.net/npm/xel@0.41.1/xel.js" type="module"></script>
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://unpkg.com/alpinejs" defer></script>
<style>
  body { user-select: none; }
  .drag-region { -webkit-app-region: drag; }
  .nodrag { -webkit-app-region: no-drag; }

  #drop-zone::-webkit-scrollbar { width: 8px; }
  #drop-zone::-webkit-scrollbar-thumb {
    background: rgba(0,0,0,0.18);
    border-radius: 4px;
    border: 2px solid transparent;
    background-clip: content-box;
  }
  #drop-zone::-webkit-scrollbar-track { background: transparent; }
  @media (prefers-color-scheme: dark) {
    #drop-zone::-webkit-scrollbar-thumb {
      background: rgba(255,255,255,0.22);
      border-radius: 4px;
      border: 2px solid transparent;
      background-clip: content-box;
    }
  }

  #drop-zone:empty::after {
    content: "Drop files here or click + to add";
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #999;
    font-size: 13px;
    font-style: italic;
    pointer-events: none;
  }
  @media (prefers-color-scheme: dark) {
    #drop-zone:empty::after { color: #666; }
  }

  #drop-zone.dragover {
    background: rgba(0, 122, 255, 0.04);
    box-shadow: inset 0 0 0 2px rgba(0, 122, 255, 0.22);
  }
  @media (prefers-color-scheme: dark) {
    #drop-zone.dragover {
      background: rgba(10, 132, 255, 0.06);
      box-shadow: inset 0 0 0 2px rgba(10, 132, 255, 0.3);
    }
  }

  .file-row {
    padding: 1px 10px;
    margin: 0 4px;
    font-family: "SF Mono", ui-monospace, Menlo, monospace;
    font-size: 12px;
    line-height: 22px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    border-radius: 5px;
    cursor: default;
    color: #334155;
    transition: background-color 60ms ease;
  }
  .file-row:nth-child(even) { background: rgba(0,0,0,0.03); }
  .file-row:hover { background: rgba(0,0,0,0.04); }
  .file-row.selected { background: #3b82f6; color: #fff; }
  .file-row.selected:hover { background: #2563eb; color: #fff; }
  @media (prefers-color-scheme: dark) {
    .file-row { color: #cbd5e1; }
    .file-row:nth-child(even) { background: rgba(255,255,255,0.03); }
    .file-row:hover { background: rgba(255,255,255,0.06); }
    .file-row.selected { background: #3b82f6; }
    .file-row.selected:hover { background: #2563eb; }
  }
</style>
</head>
<body class="h-screen overflow-hidden font-sans text-[13px] bg-transparent">
<div class="flex flex-col h-screen bg-white dark:bg-[#1e1e1e] text-slate-800 dark:text-slate-200">

  <header class="drag-region flex items-center justify-between min-h-[40px] px-2.5 py-[5px]
                  bg-white/80 dark:bg-[#2a2a2a]/80
                  backdrop-blur-xl backdrop-saturate-[180%]
                  border-b border-slate-200 dark:border-slate-700/60">

    <div class="nodrag flex items-center gap-1">
      <x-buttons tracking="-1">
        <x-button py-call="add_files" py-target="#drop-zone" py-swap="innerHTML" title="Add files">
          <x-icon href="#add"></x-icon>
        </x-button>
        <x-button py-call="remove_selected" py-target="#drop-zone" py-swap="innerHTML" title="Remove selected">
          <x-icon href="#remove"></x-icon>
        </x-button>
        <x-button py-call="clear_all" py-target="#drop-zone" py-swap="innerHTML" title="Clear all">
          <x-icon href="#close"></x-icon>
        </x-button>
        <x-button py-call="print_all" py-target="#status" py-swap="innerHTML" title="Print to stdout">
          <x-icon href="#send"></x-icon>
        </x-button>
      </x-buttons>
    </div>

    <div class="nodrag flex items-center gap-2 pr-1">
      <x-label for="img-only">Images only</x-label>
      <x-switch id="img-only"
                py-call="set_image_filter"
                py-trigger="toggle"
                py-target="#status"
                py-swap="innerHTML"></x-switch>
    </div>
  </header>

  <div class="flex-1 overflow-hidden flex flex-col min-h-0 bg-white dark:bg-[#1e1e1e]">
    <div id="drop-zone"
         x-data="{ dc: 0 }"
         @dragenter="dc++"
         @dragleave="if (--dc < 0) dc = 0"
         @dragover.prevent
         @drop.prevent="dc = 0"
         :class="{ 'dragover': dc > 0 }"
         class="flex-1 overflow-y-auto overflow-x-hidden min-h-0 py-0.5
                transition-[background-color,box-shadow] duration-150 ease-in-out"></div>
  </div>

  <div class="flex items-center min-h-[24px] px-2.5
              border-t border-slate-200 dark:border-slate-700/60
              bg-slate-50/70 dark:bg-[#252525]">
    <x-label id="status" class="text-[11px] tracking-tight tabular-nums text-slate-500 dark:text-slate-400">Files: 0</x-label>
  </div>

</div>





























































<script>
  // Client-side selection state (instant feedback, no server round-trip)
  let selected = new Set();
  let lastClicked = -1;

  /* ── Canvas-based middle-truncation ── */
  function truncMiddle(t, maxPx, ctx) {
    if (ctx.measureText(t).width <= maxPx) return t;
    let lo = 0, hi = Math.floor(t.length / 2), best = "\\u22ee";
    while (lo <= hi) {
      const m = (lo + hi) >> 1;
      const s = m > 0 ? t.slice(0, m) + "\\u22ee" + t.slice(-m) : "\\u22ee";
      ctx.measureText(s).width <= maxPx ? (best = s, lo = m + 1) : (hi = m - 1);
    }
    return best;
  }

  /* ── Post-swap setup: truncate paths + attach click handlers ── */
  function afterSwapSetup() {
    const zone = document.getElementById("drop-zone");
    const rows = zone.querySelectorAll(".file-row");
    if (!rows.length) return;

    const w = zone.clientWidth - 28;
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    ctx.font = '12px "SF Mono", ui-monospace, Menlo, monospace';

    rows.forEach((div) => {
      const fullPath = div.getAttribute("data-path") || "";
      const idx = parseInt(div.getAttribute("data-index"), 10);
      div.textContent = truncMiddle(fullPath, w, ctx);

      if (selected.has(idx)) div.classList.add("selected");

      div.onclick = (e) => {
        if (e.shiftKey && lastClicked >= 0) {
          const lo = Math.min(lastClicked, idx);
          const hi = Math.max(lastClicked, idx);
          if (!e.metaKey && !e.ctrlKey) selected.clear();
          for (let j = lo; j <= hi; j++) selected.add(j);
        } else if (e.metaKey || e.ctrlKey) {
          selected.has(idx) ? selected.delete(idx) : selected.add(idx);
        } else {
          selected.clear();
          selected.add(idx);
        }
        lastClicked = idx;
        zone.querySelectorAll(".file-row").forEach((r) => {
          const ri = parseInt(r.getAttribute("data-index"), 10);
          r.classList.toggle("selected", selected.has(ri));
        });
      };
    });
  }

  /* ── Lifecycle hook: re-bind rows whenever drop-zone content changes ── */
  new MutationObserver(() => {
    afterSwapSetup();
    if (window.pywebview?.api?.get_status) {
      window.pywebview.api.get_status().then((html) => {
        document.getElementById("status").innerHTML = html;
      });
    }
  }).observe(document.getElementById("drop-zone"), { childList: true });

  /* ── Debounced resize re-truncation ── */
  let resizeTimer;
  window.addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      const zone = document.getElementById("drop-zone");
      const rows = zone.querySelectorAll(".file-row");
      if (!rows.length) return;
      const w = zone.clientWidth - 28;
      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");
      ctx.font = '12px "SF Mono", ui-monospace, Menlo, monospace';
      rows.forEach((div) => {
        div.textContent = truncMiddle(div.getAttribute("data-path") || "", w, ctx);
      });
    }, 80);
  });
</script>
</body>
</html>
"""


# ── Python API ──
# Every py-call method returns an HTML string fragment that
# pywebview-htmx swaps into the DOM via py-target/py-swap.


class Api:
    """Exposed to JS as ``window.pywebview.api``."""

    def __init__(self) -> None:
        self._paths: list[str] = []
        self._image_filter: bool = False
        self._selected: set[int] = set()
        self._window: webview.Window | None = None

    def set_window(self, window: webview.Window) -> None:
        self._window = window

    # ── Rendering helpers ──

    def _render_file_list(self) -> str:
        """Return HTML fragment of file rows, or empty string for CSS :empty hint."""
        if not self._paths:
            return ""
        rows: list[str] = []
        for i, path in enumerate(self._paths):
            sel = " selected" if i in self._selected else ""
            escaped = _html_escape(path)
            rows.append(f'<div class="file-row{sel}" data-index="{i}" data-path="{escaped}">{escaped}</div>')
        return "\n".join(rows)

    def _render_status(self) -> str:
        n = len(self._paths)
        img = " (images only)" if self._image_filter else ""
        return f"Files: {n}{img}"

    # ── py-call targets ──

    def add_files(self, params: dict | None = None) -> str:  # noqa: ARG002
        """Open native file dialog, add chosen files, return updated list."""
        if self._window:
            result = self._window.create_file_dialog(webview.FileDialog.OPEN, allow_multiple=True)
            if result:
                self._add(list(result))
        self._selected.clear()
        return self._render_file_list()

    def remove_selected(self, params: dict | None = None) -> str:  # noqa: ARG002
        """Remove JS-selected indices, return updated list."""
        indices: list[int] = []
        if self._window:
            raw = self._window.evaluate_js("JSON.stringify(Array.from(selected))")
            if raw:
                try:
                    indices = json.loads(raw)
                except (json.JSONDecodeError, TypeError):
                    pass
        for i in sorted(indices, reverse=True):
            if 0 <= i < len(self._paths):
                del self._paths[i]
        self._selected.clear()
        return self._render_file_list()

    def clear_all(self, params: dict | None = None) -> str:  # noqa: ARG002
        """Remove all files, return empty list fragment."""
        self._paths.clear()
        self._selected.clear()
        return self._render_file_list()

    def print_all(self, params: dict | None = None) -> str:  # noqa: ARG002
        """Print all file paths to stdout, return status fragment."""
        for p in self._paths:
            print(p)
        return self._render_status()

    def set_image_filter(self, params: dict | None = None) -> str:  # noqa: ARG002
        """Toggle image-only filter, return updated status fragment."""
        self._image_filter = not self._image_filter
        return self._render_status()

    def get_status(self, params: dict | None = None) -> str:  # noqa: ARG002
        """Return current status fragment (called by JS after list swaps)."""
        return self._render_status()

    # ── Internal helpers ──

    def _add(self, paths: list[str]) -> None:
        for p in paths:
            if not os.path.exists(p):
                continue
            if self._image_filter and os.path.splitext(p)[1].lower() not in IMAGE_EXTENSIONS:
                continue
            if p not in self._paths:
                self._paths.append(p)

    def handle_dropped_files(self, paths: list[str]) -> None:
        """Called from the DnD handler, not a py-call target."""
        self._add(paths)
        self._selected.clear()


# ── Drag-and-drop via pywebview DOM events ──
# DnD bypasses pywebview-htmx's py-call pipeline, so after a drop
# we manually push updated HTML into the DOM.


def _on_drag(e: dict) -> None:  # noqa: ARG001
    """Consume drag events so the browser doesn't navigate."""


def _on_drop(e: dict, api: Api, window: webview.Window) -> None:
    """Handle file drops: add to model, then push HTML to DOM."""
    files = e.get("dataTransfer", {}).get("files", [])
    paths = [f["pywebviewFullPath"] for f in files if f.get("pywebviewFullPath")]
    if paths:
        api.handle_dropped_files(paths)
        html = api._render_file_list()
        window.evaluate_js(f"document.getElementById('drop-zone').innerHTML = {json.dumps(html)};afterSwapSetup();")
        status = api._render_status()
        window.evaluate_js(f"document.getElementById('status').innerHTML = {json.dumps(status)};")


def _bind_dnd(window: webview.Window, api: Api) -> None:
    """Attach pywebview DOM event handlers for drag-and-drop."""
    doc = window.dom.document
    handler_drag = DOMEventHandler(_on_drag, True, True)
    handler_drop = DOMEventHandler(lambda e: _on_drop(e, api, window), True, True)
    doc.events.dragenter += handler_drag
    doc.events.dragstart += handler_drag
    doc.events.dragover += DOMEventHandler(_on_drag, True, True, debounce=500)
    doc.events.drop += handler_drop


def main() -> None:
    api = Api()

    # Inject pywebview-htmx runtime (py-call/py-target/py-swap wiring)
    html = inject_runtime(HTML)

    # Write to temp file so WebKit gets a file:// origin.
    # Xel's constructable stylesheets require a non-null origin.
    tmp_dir = Path(tempfile.mkdtemp(prefix="pywebview_htmx_"))
    tmp_html = tmp_dir / "app.html"
    tmp_html.write_text(html)

    window = webview.create_window(
        "File Drop Utility – HTMX+Xel",
        url=str(tmp_html),
        js_api=api,
        width=600,
        height=400,
        background_color="#ffffff",
    )
    api.set_window(window)
    webview.start(_bind_dnd, (window, api))


if __name__ == "__main__":
    main()
