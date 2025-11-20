from __future__ import annotations

import tkinter as tk
from tkinter import filedialog
from typing import Callable, Iterable

from lazy_block.ttk_compat import ttk

from core.blocks_model import Block


class BlocksPanel(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc | None = None,
        *,
        on_folder_changed: Callable[[str], None],
        on_block_clicked: Callable[[Block], None],
        on_block_delete: Callable[[Block], None] | None = None,
        on_block_rename: Callable[[Block], None] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(master, **kwargs)
        self._on_folder_changed = on_folder_changed
        self._on_block_clicked = on_block_clicked
        self._on_block_delete = on_block_delete
        self._on_block_rename = on_block_rename
        self._blocks: list[Block] = []
        self._block_buttons: list[ttk.Button] = []
        self._folder_var = tk.StringVar()

        self._build_ui()

    def _build_ui(self) -> None:
        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        top_frame.columnconfigure(0, weight=1)

        entry = ttk.Entry(top_frame, textvariable=self._folder_var, state="readonly")
        entry.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        browse_btn = ttk.Button(top_frame, text="選擇資料夾", command=self._handle_browse)
        browse_btn.grid(row=0, column=1)

        container = ttk.Frame(self)
        container.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        canvas = tk.Canvas(container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self._blocks_frame = ttk.Frame(canvas)
        self._blocks_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=self._blocks_frame, anchor="nw")

    def _handle_browse(self) -> None:
        directory = filedialog.askdirectory()
        if directory:
            self.set_folder_path(directory, notify=True)

    def set_folder_path(self, directory: str, *, notify: bool = False) -> None:
        """Update the folder entry and optionally tell listeners."""
        self._folder_var.set(directory)
        if notify and callable(self._on_folder_changed):
            self._on_folder_changed(directory)

    def set_blocks(self, blocks: Iterable[Block]) -> None:
        for button in self._block_buttons:
            button.destroy()
        self._block_buttons.clear()
        self._blocks = list(blocks)

        for block in self._blocks:
            button = ttk.Button(
                self._blocks_frame,
                text=block.display_text,
                command=lambda b=block: self._on_block_clicked(b),
            )
            button.pack(fill="x", padx=4, pady=2)
            button.bind("<Button-3>", lambda event, b=block: self._show_context_menu(event, b))
            button.bind("<Button-2>", lambda event, b=block: self._show_context_menu(event, b))
            self._block_buttons.append(button)

    def _show_context_menu(self, event: tk.Event, block: Block) -> None:
        if self._on_block_delete is None and self._on_block_rename is None:
            return

        menu = tk.Menu(self, tearoff=False)
        if self._on_block_rename is not None:
            menu.add_command(label="重新命名", command=lambda b=block: self._on_block_rename(b))
        if self._on_block_delete is not None:
            if menu.index("end") is not None:
                menu.add_separator()
            menu.add_command(label="刪除", command=lambda b=block: self._on_block_delete(b))

        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
