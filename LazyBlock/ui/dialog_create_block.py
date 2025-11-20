from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, simpledialog
from typing import Callable

from lazy_block.ttk_compat import ttk

from core.blocks_model import Block


class CreateBlockDialog:
    """Modal dialog used to collect new block definitions."""

    def __init__(self, master: tk.Misc, *, on_submit: Callable[[Block], None]) -> None:
        self._parent = master
        self._on_submit = on_submit
        self._window = tk.Toplevel(master)
        self._window.title("創建方塊")
        self._window.transient(master)
        self._window.grab_set()
        self._window.resizable(False, False)

        self._name_var = tk.StringVar()
        self._display_var = tk.StringVar()
        self._input_text: tk.Text | None = None
        self._output_text: tk.Text | None = None
        self._focused_text: tk.Text | None = None

        self._build_ui()
        self._window.protocol("WM_DELETE_WINDOW", self._cancel)

    def _build_ui(self) -> None:
        content = ttk.Frame(self._window, padding=12)
        content.grid(row=0, column=0, sticky="nsew")

        ttk.Label(content, text="請為你方塊(資料夾)命名：").grid(row=0, column=0, sticky="w")
        ttk.Entry(content, textvariable=self._name_var, width=32).grid(
            row=1, column=0, sticky="ew", pady=(0, 8)
        )

        ttk.Label(content, text="請輸入你要\"顯示\"的文字：").grid(row=2, column=0, sticky="w")
        ttk.Entry(content, textvariable=self._display_var, width=32).grid(
            row=3, column=0, sticky="ew", pady=(0, 8)
        )

        template_frame = ttk.Frame(content)
        template_frame.grid(row=4, column=0, sticky="nsew")
        template_frame.columnconfigure(0, weight=1)
        template_frame.columnconfigure(1, weight=1)

        ttk.Label(template_frame, text="顯示內容 (B 區)").grid(row=0, column=0, sticky="w")
        ttk.Label(template_frame, text="轉換內容 (C 區)").grid(row=0, column=1, sticky="w")

        self._input_text = tk.Text(template_frame, width=40, height=8, wrap="word")
        self._output_text = tk.Text(template_frame, width=40, height=8, wrap="word")
        self._input_text.grid(row=1, column=0, sticky="nsew", padx=(0, 8), pady=(0, 8))
        self._output_text.grid(row=1, column=1, sticky="nsew", pady=(0, 8))

        for widget in (self._input_text, self._output_text):
            widget.bind("<FocusIn>", lambda _e, w=widget: self._set_focus(w))

        tools_frame = ttk.LabelFrame(content, text="工具區")
        tools_frame.grid(row=5, column=0, sticky="ew", pady=(0, 8))
        ttk.Button(
            tools_frame,
            text="{填入文字()}",
            command=self._insert_input_placeholder,
        ).grid(row=0, column=0, padx=4, pady=4)

        buttons = ttk.Frame(content)
        buttons.grid(row=6, column=0, sticky="e")
        ttk.Button(buttons, text="取消", command=self._cancel).pack(side="right", padx=(4, 0))
        ttk.Button(buttons, text="創建", command=self._submit).pack(side="right")

    def _set_focus(self, widget: tk.Text) -> None:
        self._focused_text = widget

    def _insert_input_placeholder(self) -> None:
        text_widget = self._focused_text or self._input_text
        if text_widget is None:
            return
        idx = simpledialog.askinteger(
            "插入輸入文字",
            "請輸入輸入文字索引（數字）：",
            parent=self._window,
            minvalue=1,
            maxvalue=50,
        )
        if idx is None:
            return
        text_widget.insert(tk.INSERT, f"{{輸入文字({idx})}}")

    def _cancel(self) -> None:
        self._window.grab_release()
        self._window.destroy()

    def _get_text(self, widget: tk.Text | None) -> str:
        if widget is None:
            return ""
        return widget.get("1.0", tk.END).rstrip("\n")

    def _submit(self) -> None:
        folder_name = self._name_var.get().strip()
        display_text = self._display_var.get().strip()
        input_template = self._get_text(self._input_text)
        output_template = self._get_text(self._output_text)

        if not folder_name:
            messagebox.showerror("錯誤", "請輸入方塊資料夾名稱。", parent=self._window)
            return
        if any(char in folder_name for char in ("/", "\\")):
            messagebox.showerror("錯誤", "資料夾名稱不可包含路徑符號。", parent=self._window)
            return
        if not display_text:
            messagebox.showerror("錯誤", "請輸入顯示文字。", parent=self._window)
            return
        if not input_template or not output_template:
            messagebox.showerror("錯誤", "顯示與轉換內容皆不可為空。", parent=self._window)
            return

        block = Block(
            name=folder_name,
            display_text=display_text,
            input_template=input_template,
            output_template=output_template,
            inputs=[],
        )
        block.inputs = block.get_used_inputs_from_templates()
        self._on_submit(block)
        self._cancel()

    def wait(self) -> None:
        self._parent.wait_window(self._window)


def show_create_block_dialog(master: tk.Misc, *, on_submit: Callable[[Block], None]) -> None:
    """Helper to instantiate and run the modal create dialog."""
    dialog = CreateBlockDialog(master, on_submit=on_submit)
    dialog.wait()
