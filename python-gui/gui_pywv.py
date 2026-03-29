#!/usr/bin/env -S uv run --script
# pyright: reportMissingImports=false, reportAttributeAccessIssue=false
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pywebview",
#     "webview-proc",
# ]
# ///

"""File Drop Utility - native pywebview js_api + Tailwind.

This single-file script is the native ``window.pywebview.api`` variant and
does not use pywebview-htmx. Toolbar buttons use inline onclick handlers that
call Python API methods and update DOM fragments. No Alpine, no Xel, no Lucide.
"""

from __future__ import annotations

import json
import os

import webview
import webview_proc  # noqa: F401
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
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


HTML = """\
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script src="https://cdn.tailwindcss.com"></script>
<script>
  tailwind.config = {
    darkMode: 'media',
    corePlugins: { preflight: true },
    theme: {
      extend: {
        fontFamily: {
          mono: ['"SF Mono"', 'ui-monospace', 'Menlo', 'monospace'],
          sans: ['-apple-system', 'BlinkMacSystemFont', '"Helvetica Neue"', 'sans-serif'],
        },
      },
    },
  }
</script>
<style>
  body { user-select: none; -webkit-font-smoothing: antialiased; }
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

  .toggle-switch {
    appearance: none;
    width: 42px;
    height: 24px;
    background: #ccc;
    border-radius: 12px;
    position: relative;
    cursor: pointer;
    transition: background-color 0.2s ease;
    flex-shrink: 0;
  }
  .toggle-switch::after {
    content: "";
    position: absolute;
    top: 2px;
    left: 2px;
    width: 20px;
    height: 20px;
    background: white;
    border-radius: 50%;
    transition: transform 0.2s ease;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2);
  }
  .toggle-switch:checked { background: #34c759; }
  .toggle-switch:checked::after { transform: translateX(18px); }
  @media (prefers-color-scheme: dark) {
    .toggle-switch { background: #555; }
    .toggle-switch:checked { background: #30d158; }
  }
</style>
</head>
<body class="h-screen overflow-hidden font-sans text-[13px] bg-transparent">
<div class="flex flex-col h-screen bg-white dark:bg-[#1e1e1e] text-slate-800 dark:text-slate-200">

  <header class="drag-region flex items-center justify-between min-h-[40px] px-2.5 py-[5px]
                  bg-white/80 dark:bg-[#2a2a2a]/80
                  backdrop-blur-xl backdrop-saturate-[180%]
                  border-b border-slate-200 dark:border-slate-700/60">

    <div class="nodrag flex items-center">
      <button id="btn-add" title="Add files"
              class="inline-flex items-center justify-center h-7 min-w-[38px] px-2.5
                     border border-slate-200 dark:border-slate-600 border-r-0
                     rounded-l-md
                     text-slate-700 dark:text-slate-200 text-sm
                     hover:bg-slate-100 dark:hover:bg-slate-700
                     transition-colors duration-100">\uff0b</button>
      <button id="btn-remove" title="Remove selected"
              class="inline-flex items-center justify-center h-7 min-w-[38px] px-2.5
                     border border-slate-200 dark:border-slate-600 border-r-0
                     text-slate-700 dark:text-slate-200 text-sm
                     hover:bg-slate-100 dark:hover:bg-slate-700
                     transition-colors duration-100">\u2212</button>
      <button id="btn-clear" title="Clear all"
              class="inline-flex items-center justify-center h-7 min-w-[38px] px-2.5
                     border border-slate-200 dark:border-slate-600 border-r-0
                     text-slate-700 dark:text-slate-200 text-sm
                     hover:bg-slate-100 dark:hover:bg-slate-700
                     transition-colors duration-100">\u2715</button>
      <button id="btn-confirm" title="Print to stdout"
              class="inline-flex items-center justify-center h-7 min-w-[38px] px-2.5
                     border border-transparent
                     rounded-r-md
                     bg-blue-500 text-white text-sm
                     hover:bg-blue-600
                     transition-colors duration-100">\u2713</button>
    </div>

    <label class="nodrag flex items-center gap-1.5 cursor-pointer select-none">
      <span class="whitespace-nowrap text-slate-500 dark:text-slate-400 text-xs">Images only</span>
      <input type="checkbox" id="chk" class="toggle-switch">
    </label>
  </header>

  <div class="flex-1 overflow-hidden flex flex-col min-h-0 bg-white dark:bg-[#1e1e1e]">
    <div id="drop-zone"
         class="flex-1 overflow-y-auto overflow-x-hidden min-h-0 py-0.5
                transition-[background-color,box-shadow] duration-150 ease-in-out"></div>
  </div>

  <footer class="flex items-center min-h-[24px] px-2.5
                  border-t border-slate-200 dark:border-slate-700/60
                  bg-slate-50/70 dark:bg-[#252525]">
    <span id="status"
          class="text-[11px] tracking-tight tabular-nums
                 text-slate-500 dark:text-slate-400">Files: 0</span>
  </footer>

</div>

<script>
  let selected = new Set();
  let lastClicked = -1;

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

  function wireButtons() {
    const api = window.pywebview.api;
    const status = document.getElementById("status");

    document.getElementById("btn-add").addEventListener("click", () => api.add_files());
    document.getElementById("btn-remove").addEventListener("click", () => api.remove_selected());
    document.getElementById("btn-clear").addEventListener("click", () => api.clear_all());
    document.getElementById("btn-confirm").addEventListener("click", () => {
      api.print_all().then(s => { status.textContent = s; });
    });
    document.getElementById("chk").addEventListener("change", () => {
      api.set_image_filter().then(s => { status.textContent = s; });
    });

    api.get_status().then((s) => { status.textContent = s; });
    afterSwapSetup();
  }

  (function() {
    const zone = document.getElementById("drop-zone");
    let dc = 0;
    zone.addEventListener("dragenter", () => { dc++; zone.classList.add("dragover"); });
    zone.addEventListener("dragleave", () => { if (--dc <= 0) { dc = 0; zone.classList.remove("dragover"); } });
    zone.addEventListener("dragover", (e) => e.preventDefault());
    zone.addEventListener("drop", (e) => { e.preventDefault(); dc = 0; zone.classList.remove("dragover"); });
  })();

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


class Api:
    def __init__(self) -> None:
        self._paths: list[str] = []
        self._image_filter: bool = False
        self._selected: set[int] = set()
        self._window: webview.Window | None = None

    def set_window(self, window: webview.Window) -> None:
        self._window = window

    def _render_file_list(self) -> str:
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

    def _push_dom_update(self) -> None:
        """Push file list + status into the DOM via evaluate_js (reliable path)."""
        if not self._window:
            return
        html = self._render_file_list()
        status = self._render_status()
        self._window.evaluate_js(
            f"document.getElementById('drop-zone').innerHTML = {json.dumps(html)};"
            f"afterSwapSetup();"
            f"document.getElementById('status').textContent = {json.dumps(status)};"
        )

    def add_files(self) -> None:
        if self._window:
            result = self._window.create_file_dialog(webview.FileDialog.OPEN, allow_multiple=True)
            if result:
                self._add(list(result))
        self._selected.clear()
        self._push_dom_update()

    def remove_selected(self) -> None:
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
        self._push_dom_update()

    def clear_all(self) -> None:
        self._paths.clear()
        self._selected.clear()
        self._push_dom_update()

    def print_all(self) -> str:
        for p in self._paths:
            print(p)
        return self._render_status()

    def set_image_filter(self) -> str:
        self._image_filter = not self._image_filter
        return self._render_status()

    def get_status(self) -> str:
        return self._render_status()

    def _add(self, paths: list[str]) -> None:
        for p in paths:
            if not os.path.exists(p):
                continue
            if self._image_filter and os.path.splitext(p)[1].lower() not in IMAGE_EXTENSIONS:
                continue
            if p not in self._paths:
                self._paths.append(p)

    def handle_dropped_files(self, paths: list[str]) -> None:
        self._add(paths)
        self._selected.clear()


def _on_drag(e: dict) -> None:  # noqa: ARG001
    pass


def _on_drop(e: dict, api: Api, window: webview.Window) -> None:  # noqa: ARG001
    files = e.get("dataTransfer", {}).get("files", [])
    paths = [f["pywebviewFullPath"] for f in files if f.get("pywebviewFullPath")]
    if paths:
        api.handle_dropped_files(paths)
        api._push_dom_update()


def _bind_dnd(window: webview.Window, api: Api) -> None:
    doc = window.dom.document
    handler_drag = DOMEventHandler(_on_drag, True, True)
    handler_drop = DOMEventHandler(lambda e: _on_drop(e, api, window), True, True)
    doc.events.dragenter += handler_drag
    doc.events.dragstart += handler_drag
    doc.events.dragover += DOMEventHandler(_on_drag, True, True, debounce=500)
    doc.events.drop += handler_drop
    window.evaluate_js("wireButtons();")


def main() -> None:
    api = Api()
    window = webview.create_window(
        "File Drop Utility – Tailwind",
        html=HTML,
        js_api=api,
        width=600,
        height=400,
        background_color="#ffffff",
    )
    api.set_window(window)
    webview.start(_bind_dnd, (window, api))


if __name__ == "__main__":
    main()
