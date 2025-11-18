"""Main entry point for Lazy Block UI demo."""
from __future__ import annotations

import ttkbootstrap as ttk

from core.blocks_model import Block
from core.transform_engine import render_block_for_input, render_block_for_output
from ui.panel_blocks import BlocksPanel
from ui.panel_editor import EditorPanel
from ui.panel_output import OutputPanel
from ui.topbar import TopBar


def main() -> None:
    root = ttk.Window(themename="journal")
    root.title("Lazy Block")
    root.geometry("1200x720")

    def handle_category_changed(name: str) -> None:
        print(f"Category changed: {name}")

    def handle_create_block() -> None:
        print("Create block clicked")

    def handle_folder_changed(path: str) -> None:
        print(f"Folder changed: {path}")

    TopBar(
        root,
        on_category_changed=handle_category_changed,
        on_create_block=handle_create_block,
    ).pack(fill="x")

    main_frame = ttk.Frame(root)
    main_frame.pack(fill="both", expand=True)
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure(0, weight=2)
    main_frame.grid_columnconfigure(1, weight=3)
    main_frame.grid_columnconfigure(2, weight=2)

    editor_panel = EditorPanel(main_frame)
    output_panel = OutputPanel(main_frame)

    def handle_block_clicked(block: Block) -> None:
        values = {1: "AAA", 2: "BBB"}
        editor_panel.set_text(render_block_for_input(block, values))
        output_panel.set_text(render_block_for_output(block, values))

    blocks_panel = BlocksPanel(
        main_frame,
        on_folder_changed=handle_folder_changed,
        on_block_clicked=handle_block_clicked,
    )
    blocks_panel.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)

    editor_panel.grid(row=0, column=1, sticky="nsew", padx=6, pady=6)
    output_panel.grid(row=0, column=2, sticky="nsew", padx=6, pady=6)

    sample_blocks = [
        Block(
            name="sample_a",
            display_text="方塊 A",
            input_template="輸入 {輸入文字(1)}",
            output_template="輸出 {輸入文字(2)}",
            inputs=[1, 2],
        ),
        Block(
            name="sample_b",
            display_text="方塊 B",
            input_template="Hello {輸入文字(1)}!",
            output_template="Bye {輸入文字(2)}!",
            inputs=[1, 2],
        ),
    ]
    blocks_panel.set_blocks(sample_blocks)

    root.mainloop()


if __name__ == "__main__":
    main()