#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "toga",
# ]
# ///

import os

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

# NOTE: Toga does not support native file drag-and-drop from OS file manager.
# There is no on_drop/on_drag_enter API on Widget, Window, or App.
# GitHub issue #3088 tracks this as an open enhancement request.
# Canvas.on_drag exists but is for internal mouse tracking (drawing), not file drops.

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


def truncate_middle(text: str, max_width: int) -> str:
    if max_width <= 0:
        return ""
    if len(text) <= max_width:
        return text
    if max_width == 1:
        return "\u22ee"
    keep = max_width - 1
    left = keep // 2
    right = keep - left
    return f"{text[:left]}\u22ee{text[-right:]}" if right else f"{text[:left]}\u22ee"


class FileListApp(toga.App):
    def startup(self) -> None:
        self._paths: list[str] = []

        main_box = toga.Box(style=Pack(direction=COLUMN, margin=10))
        toolbar = toga.Box(style=Pack(direction=ROW, margin_bottom=10))

        toolbar.add(toga.Button("+", on_press=self._on_add, style=Pack(margin_right=5)))
        toolbar.add(toga.Button("\u2212", on_press=self._on_remove, style=Pack(margin_right=5)))
        toolbar.add(toga.Button("\u2715", on_press=self._on_clear, style=Pack(margin_right=5)))
        toolbar.add(toga.Button("\u2713", on_press=self._on_print, style=Pack(margin_right=15)))
        self._chk_images = toga.Switch("Images")
        toolbar.add(self._chk_images)

        self._list_view = toga.Table(
            headings=["File"],
            multiple_select=True,
            on_select=self._on_select,
            missing_value="",
            style=Pack(flex=1),
        )
        self._status = toga.Label("Files: 0", style=Pack(margin_top=10))

        main_box.add(toolbar)
        main_box.add(self._list_view)
        main_box.add(self._status)

        self.main_window = toga.MainWindow(title=self.formal_name, size=(600, 400))
        self.main_window.content = main_box
        self.main_window.on_resize = self._on_resize
        self.main_window.show()

    def _add_paths(self, new_paths: list[str]) -> None:
        image_only = self._chk_images.value
        for p in new_paths:
            p = str(p)
            if not os.path.exists(p):
                continue
            if image_only and os.path.splitext(p)[1].lower() not in IMAGE_EXTENSIONS:
                continue
            if p not in self._paths:
                self._paths.append(p)
        self._refresh_display()

    def _refresh_display(self) -> None:
        width = self.main_window.size[0]
        max_chars = max(5, int(width / 8))
        rows = []
        for p in self._paths:
            display = truncate_middle(p, max_chars)
            rows.append((display,))
        self._list_view.data = rows
        self._status.text = f"Files: {len(self._paths)}"

    async def _on_add(self, widget: toga.Widget) -> None:
        try:
            result = await self.main_window.dialog(toga.OpenFileDialog("Select Files", multiple_select=True))
            if result:
                self._add_paths(list(result))
        except ValueError:
            pass

    def _on_remove(self, widget: toga.Widget) -> None:
        selection = self._list_view.selection
        if selection:
            selected = selection if isinstance(selection, list) else [selection]
            selected_ids = {id(item) for item in selected}
            indices: set[int] = set()
            for i, row in enumerate(self._list_view.data):
                if id(row) in selected_ids:
                    indices.add(i)
            self._paths = [p for i, p in enumerate(self._paths) if i not in indices]
            self._refresh_display()

    def _on_clear(self, widget: toga.Widget) -> None:
        self._paths.clear()
        self._refresh_display()

    def _on_print(self, widget: toga.Widget) -> None:
        for p in self._paths:
            print(p)

    def _on_select(self, widget: toga.Widget, row: object) -> None:
        pass

    def _on_resize(self, window: toga.Window, **kwargs: object) -> None:
        self._refresh_display()


def main() -> toga.App:
    return FileListApp("Toga File List", "org.beeware.toga.filelist")


if __name__ == "__main__":
    main().main_loop()
