#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13,<3.14"
# dependencies = [
#     "customtkinter",
#     "tkinterdnd2",
#     "CTkMenuBarPlus",
#     "CTkManager",
#     "ctk-sidebar",
#     "CTkTable",
#     "CTkToolTip",
# ]
# ///

from __future__ import annotations

import os
import tkinter as tk
from tkinter import font as tkfont
from typing import Any, cast

import customtkinter  # type: ignore[import-untyped]
from customtkinter import filedialog  # type: ignore[import-untyped]
from CTkManager import CTkManager  # type: ignore[import-untyped]
from CTkMenuBarPlus import CTkMenuBar, ContextMenu, CustomDropdownMenu  # type: ignore[import-untyped]
from CTkTable import CTkTable  # type: ignore[import-untyped]
from CTkTableRowSelector import CTkTableRowSelector  # type: ignore[import-untyped]
from CTkToolTip import CTkToolTip  # type: ignore[import-untyped]
from ctksidebar import CTkSidebarNavigation  # type: ignore[import-untyped]
from tkinterdnd2 import DND_FILES, TkinterDnD  # type: ignore[import-untyped]

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
        return "⋮"
    keep = max_width - 1
    left = keep // 2
    right = keep - left
    return f"{text[:left]}⋮{text[-right:]}" if right else f"{text[:left]}⋮"


class App(customtkinter.CTk, TkinterDnD.DnDWrapper):
    def __init__(self) -> None:
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)

        self.title("CustomTkinter File List")
        self.geometry("800x480")

        self._paths: list[str] = []
        self._rows: list[Any] = []
        self._selected_indices: set[int] = set()
        self._anchor_index: int | None = None
        self._last_width = 0
        self._resize_job: str | None = None

        self._selected_color = ("#3B8ED0", "#1F6AA5")
        self._row_color_even = ("#e8e8e8", "#333333")
        self._row_color_odd = ("#f6f6f6", "#2b2b2b")
        self._table_visible_var = tk.BooleanVar(value=False)
        self._images_only_var = tk.BooleanVar(value=False)

        # CTkManager can be used for convenience in standard CTk apps, but this
        # script keeps the dual-inheritance DnD pattern and runs via mainloop().
        self._ctk_manager: CTkManager | None = None
        try:
            self._ctk_manager = CTkManager(self)
        except Exception:
            self._ctk_manager = None

        self._build_menu_bar()
        self._build_toolbar()
        self._build_center_layout()
        self._build_status_bar()
        self._build_context_menu()

        sample_label = customtkinter.CTkLabel(self, text="")
        sample_font = sample_label.cget("font")
        sample_label.destroy()
        if isinstance(sample_font, str):
            self._font = tkfont.nametofont(sample_font)
        else:
            self._font = tkfont.Font(font=sample_font)

        self._register_dnd_targets()
        self.bind("<Configure>", self._on_resize)
        self._sync_menu_checks()

        self.after(50, self._raise_window)

    def _raise_window(self) -> None:
        self.lift()
        self.attributes("-topmost", True)
        self.after(100, lambda: self.attributes("-topmost", False))
        self.focus_force()

    def _build_menu_bar(self) -> None:
        self._menu_bar = CTkMenuBar(self)
        self._menu_bar.pack(fill=tk.X, padx=6, pady=(4, 2))

        file_btn = self._menu_bar.add_cascade("File")
        ui_font = file_btn.cget("font")

        self._file_menu = CustomDropdownMenu(widget=file_btn, font=ui_font)
        self._file_menu.add_option("Add Files", command=self._on_add, accelerator="CmdOrCtrl+O")
        self._file_menu.add_option("Remove Selected", command=self._on_remove, accelerator="CmdOrCtrl+Backspace")
        self._file_menu.add_option("Clear All", command=self._on_clear, accelerator="CmdOrCtrl+K")
        self._file_menu.add_separator()
        self._file_menu.add_option("Print Paths", command=self._on_print, accelerator="CmdOrCtrl+P")
        self._file_menu.add_separator()
        self._file_menu.add_option("Quit", command=self.destroy, accelerator="CmdOrCtrl+Q")

        edit_btn = self._menu_bar.add_cascade("Edit")
        self._edit_menu = CustomDropdownMenu(widget=edit_btn, font=ui_font)
        self._edit_menu.add_option("Select All", command=self._on_select_all, accelerator="CmdOrCtrl+A")
        self._edit_menu.add_option("Deselect All", command=self._on_deselect_all, accelerator="CmdOrCtrl+Shift+A")

        view_btn = self._menu_bar.add_cascade("View")
        self._view_menu = CustomDropdownMenu(widget=view_btn, font=ui_font)
        self._view_menu.add_option("Images Only", command=self._toggle_images_only_from_menu, accelerator="CmdOrCtrl+I")
        self._view_menu.add_option(
            "Show Table View", command=self._toggle_table_view_from_menu, accelerator="CmdOrCtrl+T"
        )

    def _build_toolbar(self) -> None:
        toolbar = customtkinter.CTkFrame(self, corner_radius=6)
        toolbar.pack(fill=tk.X, padx=6, pady=(0, 4))

        self._add_btn = customtkinter.CTkButton(toolbar, text="+", width=28, height=26, command=self._on_add)
        self._add_btn.pack(side=tk.LEFT, padx=(4, 2), pady=4)
        CTkToolTip(self._add_btn, message="Add files (+)", delay=0.3)

        self._remove_btn = customtkinter.CTkButton(toolbar, text="−", width=28, height=26, command=self._on_remove)
        self._remove_btn.pack(side=tk.LEFT, padx=2, pady=4)
        CTkToolTip(self._remove_btn, message="Remove selected (−)", delay=0.3)

        self._clear_btn = customtkinter.CTkButton(toolbar, text="✕", width=28, height=26, command=self._on_clear)
        self._clear_btn.pack(side=tk.LEFT, padx=2, pady=4)
        CTkToolTip(self._clear_btn, message="Clear all (✕)", delay=0.3)

        self._print_btn = customtkinter.CTkButton(toolbar, text="✓", width=28, height=26, command=self._on_print)
        self._print_btn.pack(side=tk.LEFT, padx=2, pady=4)
        CTkToolTip(self._print_btn, message="Print paths (✓)", delay=0.3)

        self._images_checkbox = customtkinter.CTkCheckBox(
            toolbar,
            text="Images",
            variable=self._images_only_var,
            command=self._on_images_checkbox_changed,
            checkbox_width=16,
            checkbox_height=16,
        )
        self._images_checkbox.pack(side=tk.LEFT, padx=(6, 4), pady=4)
        CTkToolTip(self._images_checkbox, message="Filter for image files only", delay=0.3)

    def _build_center_layout(self) -> None:
        self._center_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self._center_frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=(0, 4))

        self._sidebar_nav = CTkSidebarNavigation(self._center_frame, width=130)
        self._sidebar_nav.sidebar.add_item("files", text="Files")
        self._sidebar_nav.sidebar.add_item("table", text="Table")
        self._sidebar_nav.pack(fill=tk.BOTH, expand=True)

        self._files_view = self._sidebar_nav.view("files")
        self._table_view = self._sidebar_nav.view("table")

        self._list_frame = customtkinter.CTkScrollableFrame(self._files_view, corner_radius=6)
        self._list_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        self._table_frame = customtkinter.CTkFrame(self._table_view, corner_radius=6)
        self._table_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        self._table_data: list[list[str]] = [["#", "Filename", "Extension", "Size"]]
        self._table = CTkTable(master=self._table_frame, values=self._table_data)
        self._table.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        self._table_selector: CTkTableRowSelector | None = None
        try:
            self._table_selector = CTkTableRowSelector(self._table)
        except Exception:
            self._table_selector = None

        self._show_view("files")

    def _build_status_bar(self) -> None:
        status_bar = customtkinter.CTkFrame(self, corner_radius=6)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=6, pady=(0, 4))
        self._status_label = customtkinter.CTkLabel(
            status_bar, text="Files: 0", anchor="w", font=customtkinter.CTkFont(size=11)
        )
        self._status_label.pack(fill=tk.X, padx=8, pady=3)

    def _build_context_menu(self) -> None:
        self._context_menu = ContextMenu(self._list_frame)
        self._context_menu.add_option("Remove Selected", command=self._on_remove)
        self._context_menu.add_option("Clear All", command=self._on_clear)
        self._context_menu.add_option("Print Paths", command=self._on_print)

    def _register_dnd_targets(self) -> None:
        targets: list[Any] = [self, self._list_frame]
        interior = getattr(self._list_frame, "_scrollable_frame", None)
        if interior is not None:
            targets.append(interior)

        for target in targets:
            target.drop_target_register(DND_FILES)
            target.dnd_bind("<<Drop>>", self._on_drop)

    def _show_view(self, view_id: str) -> None:
        self._table_visible_var.set(view_id == "table")
        if hasattr(self._sidebar_nav, "show_view"):
            self._sidebar_nav.show_view(view_id)
        elif hasattr(self._sidebar_nav, "set_view"):
            self._sidebar_nav.set_view(view_id)
        else:
            self._files_view.pack_forget()
            self._table_view.pack_forget()
            if view_id == "table":
                self._table_view.pack(fill=tk.BOTH, expand=True)
            else:
                self._files_view.pack(fill=tk.BOTH, expand=True)
        self._sync_menu_checks()

    def _sync_menu_checks(self) -> None:
        self._set_view_menu_option("Images Only", self._images_only_var.get())
        self._set_view_menu_option("Show Table View", self._table_visible_var.get())

    def _set_view_menu_option(self, label: str, checked: bool) -> None:
        if hasattr(self._view_menu, "set_option"):
            self._view_menu.set_option(label, checked=checked)
            return
        if hasattr(self._view_menu, "set_checked"):
            self._view_menu.set_checked(label, checked)
            return
        if hasattr(self._view_menu, "configure_option"):
            self._view_menu.configure_option(label, text=f"{'✓ ' if checked else ''}{label}")

    def add_paths(self, paths: list[str]) -> None:
        image_only = self._images_only_var.get()
        changed = False
        for path in paths:
            if not os.path.exists(path):
                continue
            if image_only and os.path.splitext(path)[1].lower() not in IMAGE_EXTENSIONS:
                continue
            if path not in self._paths:
                self._paths.append(path)
                changed = True

        if changed:
            self._refresh_all_views()

    def _refresh_all_views(self) -> None:
        self._refresh_display()
        self._refresh_table()

    def _refresh_display(self) -> None:
        for row in self._rows:
            row.destroy()
        self._rows.clear()

        self._selected_indices = {idx for idx in self._selected_indices if 0 <= idx < len(self._paths)}
        width_px = max(10, self._list_frame.winfo_width() - 24)

        for index, path in enumerate(self._paths):
            text = self._truncate_for_width(path, width_px)
            base_color = self._row_color_even if index % 2 == 0 else self._row_color_odd
            row = customtkinter.CTkLabel(
                self._list_frame,
                text=text,
                anchor="w",
                padx=6,
                pady=2,
                corner_radius=4,
                fg_color=base_color,
            )
            row.pack(fill=tk.X, padx=2, pady=1)
            row.bind("<Button-1>", lambda event, idx=index: self._on_row_click(event, idx))
            self._rows.append(row)

        self._apply_selection_styles()
        self._status_label.configure(text=f"Files: {len(self._paths)}")

    def _refresh_table(self) -> None:
        values: list[list[str]] = [["#", "Filename", "Extension", "Size"]]
        for index, path in enumerate(self._paths, start=1):
            filename = os.path.basename(path)
            extension = os.path.splitext(path)[1].lower() or "—"
            size_text = self._format_size(path)
            values.append([str(index), filename, extension, size_text])

        self._table_data = values

        self._table.destroy()
        self._table = CTkTable(master=self._table_frame, values=self._table_data, command=self._on_table_click)
        self._table.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        try:
            self._table_selector = CTkTableRowSelector(self._table)
            selector = self._table_selector
            if selector is not None and hasattr(selector, "set_selected_rows"):
                selector.set_selected_rows([idx + 1 for idx in sorted(self._selected_indices)])
        except Exception:
            self._table_selector = None

    def _format_size(self, path: str) -> str:
        try:
            size = os.path.getsize(path)
        except OSError:
            return "—"

        units = ["B", "KB", "MB", "GB", "TB"]
        value = float(size)
        unit = units[0]
        for candidate in units:
            unit = candidate
            if value < 1024.0 or candidate == units[-1]:
                break
            value /= 1024.0
        return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"

    def _truncate_for_width(self, path: str, width_px: int) -> str:
        if self._font.measure(path) <= width_px:
            return path
        avg_char_px = self._font.measure("x") or 7
        max_chars = max(5, width_px // avg_char_px)
        return truncate_middle(path, max_chars)

    def _on_row_click(self, event: tk.Event[tk.Misc], index: int) -> None:
        state = cast(int, event.state)
        shift = bool(state & 0x0001)
        toggle = bool(state & (0x0004 | 0x0010))

        if shift and self._anchor_index is not None:
            start, end = sorted((self._anchor_index, index))
            self._selected_indices = set(range(start, end + 1))
        elif toggle:
            if index in self._selected_indices:
                self._selected_indices.remove(index)
            else:
                self._selected_indices.add(index)
            self._anchor_index = index
        else:
            self._selected_indices = {index}
            self._anchor_index = index

        self._apply_selection_styles()
        self._refresh_table()

    def _on_table_click(self, cell_info: dict[str, Any] | Any) -> None:
        if not isinstance(cell_info, dict):
            return
        row = cast(int, cell_info.get("row", 0))
        if row <= 0:
            return
        index = row - 1
        if not (0 <= index < len(self._paths)):
            return

        if index in self._selected_indices:
            self._selected_indices.remove(index)
        else:
            self._selected_indices.add(index)
        self._anchor_index = index
        self._apply_selection_styles()

    def _apply_selection_styles(self) -> None:
        for index, row in enumerate(self._rows):
            if index in self._selected_indices:
                row.configure(fg_color=self._selected_color)
            else:
                row.configure(fg_color=self._row_color_even if index % 2 == 0 else self._row_color_odd)

        selector = self._table_selector
        if selector is not None and hasattr(selector, "set_selected_rows"):
            selector.set_selected_rows([idx + 1 for idx in sorted(self._selected_indices)])

    def _on_drop(self, event: tk.Event[tk.Misc]) -> None:
        data = cast(str, getattr(event, "data", ""))
        self.add_paths(list(self.tk.splitlist(data)))

    def _on_resize(self, event: tk.Event[tk.Misc]) -> None:
        if event.widget is not self:
            return
        width = self.winfo_width()
        if abs(width - self._last_width) <= 5:
            return
        self._last_width = width
        if self._resize_job is not None:
            self.after_cancel(self._resize_job)
        self._resize_job = self.after(70, self._resize_refresh)

    def _resize_refresh(self) -> None:
        self._resize_job = None
        self._refresh_display()

    def _on_add(self) -> None:
        paths = filedialog.askopenfilenames(title="Select Files")
        if paths:
            self.add_paths(list(paths))

    def _on_remove(self) -> None:
        if not self._selected_indices:
            return
        for index in sorted(self._selected_indices, reverse=True):
            del self._paths[index]
        self._selected_indices.clear()
        self._anchor_index = None
        self._refresh_all_views()

    def _on_clear(self) -> None:
        self._paths.clear()
        self._selected_indices.clear()
        self._anchor_index = None
        self._refresh_all_views()

    def _on_print(self) -> None:
        for path in self._paths:
            print(path)

    def _on_select_all(self) -> None:
        self._selected_indices = set(range(len(self._paths)))
        self._anchor_index = len(self._paths) - 1 if self._paths else None
        self._apply_selection_styles()

    def _on_deselect_all(self) -> None:
        self._selected_indices.clear()
        self._anchor_index = None
        self._apply_selection_styles()

    def _toggle_images_only_from_menu(self) -> None:
        self._images_only_var.set(not self._images_only_var.get())
        self._on_images_checkbox_changed()

    def _toggle_table_view_from_menu(self) -> None:
        self._show_view("files" if self._table_visible_var.get() else "table")

    def _on_images_checkbox_changed(self) -> None:
        if self._images_only_var.get():
            filtered_paths = [path for path in self._paths if os.path.splitext(path)[1].lower() in IMAGE_EXTENSIONS]
            if len(filtered_paths) != len(self._paths):
                self._paths = filtered_paths
                self._selected_indices = {idx for idx in self._selected_indices if 0 <= idx < len(self._paths)}
                self._anchor_index = (
                    None if self._anchor_index is None else min(self._anchor_index, len(self._paths) - 1)
                )
                self._refresh_all_views()
        self._sync_menu_checks()

    def destroy(self) -> None:
        if self._resize_job is not None:
            self.after_cancel(self._resize_job)
            self._resize_job = None
        self.withdraw()
        self.quit()
        super().destroy()


def main() -> None:
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
