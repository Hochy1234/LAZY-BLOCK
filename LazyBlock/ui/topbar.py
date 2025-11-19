"""Top bar widget for Lazy Block UI."""
from __future__ import annotations

from typing import Callable, Iterable, Sequence

from lazy_block.ttk_compat import ttk


class TopBar(ttk.Frame):
    """Displays category buttons, tool shortcuts, and a create action."""

    def __init__(
        self,
        master,
        on_category_changed: Callable[[str], None],
        on_create_block: Callable[[], None],
        *,
        categories: Sequence[str] | None = None,
        tools: Iterable[str] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(master, **kwargs)
        self._on_category_changed = on_category_changed
        self._on_create_block = on_create_block

        category_names = list(categories or ("主要", "功能", "美術", "其他", "+"))
        tool_names = list(tools or ("工具1", "工具2", "工具3"))

        categories_row = ttk.Frame(self)
        categories_row.pack(fill="x", padx=6, pady=(6, 3))
        for name in category_names:
            ttk.Button(categories_row, text=name, command=lambda c=name: self._change_category(c)).pack(
                side="left", padx=3
            )

        tools_row = ttk.Frame(self)
        tools_row.pack(fill="x", padx=6, pady=(3, 6))
        tools_group = ttk.Frame(tools_row)
        tools_group.pack(side="left")
        for tool in tool_names:
            ttk.Button(tools_group, text=tool).pack(side="left", padx=3)

        ttk.Button(tools_row, text="創建", command=self._create_block).pack(side="right")

    def _change_category(self, name: str) -> None:
        if callable(self._on_category_changed):
            self._on_category_changed(name)

    def _create_block(self) -> None:
        if callable(self._on_create_block):
            self._on_create_block()

