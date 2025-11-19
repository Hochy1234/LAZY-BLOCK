"""Top bar widget for Lazy Block UI."""
from __future__ import annotations

import tkinter as tk
from typing import Callable, Iterable, Mapping, Sequence

from lazy_block.ttk_compat import ttk


class TopBar(ttk.Frame):
    """Displays category buttons, tool shortcuts, theme selector, and a create action."""

    def __init__(
        self,
        master,
        on_category_changed: Callable[[str], None],
        on_create_block: Callable[[], None],
        *,
        categories: Sequence[str] | None = None,
        tools_by_category: Mapping[str, Iterable[str]] | None = None,
        on_theme_changed: Callable[[str], None] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(master, **kwargs)
        self._on_category_changed = on_category_changed
        self._on_create_block = on_create_block
        self._on_theme_changed = on_theme_changed
        self._category_var = tk.StringVar()
        self._style = ttk.Style()
        self._available_themes = tuple(self._style.theme_names())
        current_theme = self._style.theme_use() if hasattr(self._style, "theme_use") else ""
        self._theme_var = tk.StringVar(value=current_theme)

        category_names = list(categories or ("主要", "功能", "美術", "其他"))
        if not category_names:
            raise ValueError("At least one category must be provided.")
        self._category_var.set(category_names[0])
        self._tools_by_category = {
            name: list(tools_by_category.get(name, [])) if tools_by_category else []
            for name in category_names
        }

        categories_row = ttk.Frame(self)
        categories_row.pack(fill="x", padx=6, pady=(6, 3))
        for name in category_names:
            ttk.Radiobutton(
                categories_row,
                text=name,
                value=name,
                variable=self._category_var,
                command=lambda c=name: self._change_category(c),
            ).pack(side="left", padx=3)

        tools_row = ttk.Frame(self)
        tools_row.pack(fill="x", padx=6, pady=(3, 6))
        self._tools_frame = ttk.Frame(tools_row)
        self._tools_frame.pack(side="left", fill="x", expand=True)
        ttk.Button(tools_row, text="創建", command=self._create_block).pack(side="right")

        self._render_tools(self._category_var.get())

    def _render_tools(self, category: str) -> None:
        for child in self._tools_frame.winfo_children():
            child.destroy()

        if category == "美術":
            self._render_theme_selector()
            return

        tools = self._tools_by_category.get(category) or ("工具1", "工具2", "工具3")
        for tool in tools:
            ttk.Button(self._tools_frame, text=tool).pack(side="left", padx=3)

    def _render_theme_selector(self) -> None:
        if not self._available_themes:
            ttk.Label(self._tools_frame, text="無可用主題").pack(side="left", padx=3)
            return

        ttk.Label(self._tools_frame, text="視窗主題").pack(side="left", padx=(0, 6))
        combo = ttk.Combobox(
            self._tools_frame,
            state="readonly",
            values=self._available_themes,
            textvariable=self._theme_var,
        )
        combo.bind("<<ComboboxSelected>>", lambda _event: self._theme_selected())
        combo.pack(side="left", padx=3)

    def _theme_selected(self) -> None:
        theme = self._theme_var.get()
        if callable(self._on_theme_changed):
            self._on_theme_changed(theme)
        elif hasattr(self._style, "theme_use"):
            try:
                self._style.theme_use(theme)
            except Exception:
                pass

    def _change_category(self, name: str) -> None:
        self._category_var.set(name)
        self._render_tools(name)
        if callable(self._on_category_changed):
            self._on_category_changed(name)

    def _create_block(self) -> None:
        if callable(self._on_create_block):
            self._on_create_block()

