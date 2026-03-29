#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "PyQt6",
# ]
# ///

import os
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFileDialog,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

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


class FileList(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.setAlternatingRowColors(True)
        self.setAcceptDrops(True)
        self._paths: list[str] = []

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            paths = [u.toLocalFile() for u in event.mimeData().urls() if u.isLocalFile()]
            window = self.window()
            if isinstance(window, MainWindow):
                window.add_paths(paths)
            event.acceptProposedAction()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.refresh_display()

    def refresh_display(self):
        fm = QFontMetrics(self.font())
        avail = max(1, self.viewport().width() - 10)
        avg_char = fm.averageCharWidth()
        max_chars = max(5, avail // avg_char) if avg_char > 0 else 80

        for i in range(self.count()):
            item = self.item(i)
            full = item.data(Qt.ItemDataRole.UserRole)
            item.setText(truncate_middle(full, max_chars))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 File List")
        self.resize(600, 400)

        self._paths: list[str] = []

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        toolbar = QHBoxLayout()
        btn_add = QPushButton("+")
        btn_remove = QPushButton("\u2212")
        btn_clear = QPushButton("\u2715")
        btn_print = QPushButton("\u2713")
        self._chk_images = QCheckBox("Images")

        btn_add.setFixedWidth(32)
        btn_remove.setFixedWidth(32)
        btn_clear.setFixedWidth(32)
        btn_print.setFixedWidth(32)

        btn_add.clicked.connect(self._on_add)
        btn_remove.clicked.connect(self._on_remove)
        btn_clear.clicked.connect(self._on_clear)
        btn_print.clicked.connect(self._on_print)

        toolbar.addWidget(btn_add)
        toolbar.addWidget(btn_remove)
        toolbar.addWidget(btn_clear)
        toolbar.addWidget(btn_print)
        toolbar.addWidget(self._chk_images)
        toolbar.addStretch()

        self._list = FileList()
        self._status = QStatusBar()
        self._status.showMessage("Files: 0")
        self.setStatusBar(self._status)

        layout.addLayout(toolbar)
        layout.addWidget(self._list)

    def add_paths(self, paths: list[str]):
        image_only = self._chk_images.isChecked()
        for p in paths:
            if not os.path.exists(p):
                continue
            if image_only and os.path.splitext(p)[1].lower() not in IMAGE_EXTENSIONS:
                continue
            if p not in self._paths:
                self._paths.append(p)
                item = QListWidgetItem()
                item.setData(Qt.ItemDataRole.UserRole, p)
                self._list.addItem(item)
        self._list.refresh_display()
        self._update_status()

    def _on_add(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files")
        if files:
            self.add_paths(files)

    def _on_remove(self):
        for item in reversed(self._list.selectedItems()):
            path = item.data(Qt.ItemDataRole.UserRole)
            if path in self._paths:
                self._paths.remove(path)
            self._list.takeItem(self._list.row(item))
        self._update_status()

    def _on_clear(self):
        self._paths.clear()
        self._list.clear()
        self._update_status()

    def _on_print(self):
        for p in self._paths:
            print(p)

    def _update_status(self):
        self._status.showMessage(f"Files: {len(self._paths)}")


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    win.raise_()
    win.activateWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
