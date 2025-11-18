"""UI panel for showing conversion output."""

from __future__ import annotations

import tkinter as tk
from ttkbootstrap import ttk


class OutputPanel(ttk.Frame):
    """Panel dedicated to display conversion results."""

    def __init__(self, master: tk.Misc | None = None, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._text_widget: tk.Text | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        ttk.Label(self, text="轉換結果").grid(row=0, column=0, sticky="w", padx=8, pady=(8, 4))

        container = ttk.Frame(self)
        container.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(container, orient="vertical")
        text = tk.Text(
            container,
            wrap="word",
            state="disabled",
            yscrollcommand=scrollbar.set,
            disabledbackground="#f5f5f5",
            disabledforeground="#1a1a1a",
            relief="flat",
        )
        scrollbar.configure(command=text.yview)
        text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self._text_widget = text

    def _text(self) -> tk.Text:
        if self._text_widget is None:
            raise RuntimeError("Text widget has not been initialized.")
        return self._text_widget

    def set_text(self, text: str) -> None:
        widget = self._text()
        widget.configure(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert("1.0", text)
        widget.configure(state="disabled")

    def get_text(self) -> str:
        widget = self._text()
        widget.configure(state="normal")
        value = widget.get("1.0", tk.END).rstrip("\n")
        widget.configure(state="disabled")
        return value