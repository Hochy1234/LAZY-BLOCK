"""Main entry point for Lazy Block UI demo."""
from __future__ import annotations

from pathlib import Path
from tkinter import messagebox, simpledialog

from lazy_block.ttk_compat import ttk

from core.blocks_model import Block
from core.blocks_storage import (
    delete_block,
    list_block_folder_entries,
    rename_block_folder,
    save_block,
)
from core.transform_engine import render_block_for_input, render_block_for_output
from ui.dialog_create_block import show_create_block_dialog
from ui.panel_blocks import BlocksPanel
from ui.panel_editor import EditorPanel
from ui.panel_output import OutputPanel
from ui.topbar import TopBar


def main() -> None:
    root = ttk.Window(themename="journal")
    root.title("Lazy Block")
    root.geometry("1200x720")
    style = ttk.Style()

    sample_blocks = [
        Block(
            name="upgrade",
            display_text="升級",
            input_template="1!2!3! ABCD 哈哈哈 [升級] 一筆一筆\n第二段",
            output_template="1!2!3! ABCD 哈哈哈 Upgrade! 一筆一筆\n第二段",
            inputs=[],
        ),
        Block(
            name="greeting",
            display_text="問候",
            input_template="Hello {輸入文字(1)}!",
            output_template="Upgrade greeting: {輸入文字(1)} -> {輸入文字(2)}",
            inputs=[1, 2],
        ),
    ]

    project_root = Path(__file__).resolve().parent.parent
    blocks_root = project_root / "blocks"
    default_folder = blocks_root / "samples"
    default_folder.mkdir(parents=True, exist_ok=True)
    for block in sample_blocks:
        block_folder = default_folder / block.name
        block_file = block_folder / "block.json"
        if not block_file.exists():
            save_block(block, block_folder)

    current_folder_path = str(default_folder)
    block_locations: dict[str, Path] = {}

    def handle_category_changed(name: str) -> None:
        print(f"Category changed: {name}")

    def handle_create_block() -> None:
        if not current_folder_path:
            messagebox.showerror("創建方塊失敗", "請先選擇資料夾。", parent=root)
            return

        def _on_submit(block: Block) -> None:
            folder = Path(current_folder_path)
            block_folder = folder / block.name
            if block_folder.exists():
                messagebox.showerror(
                    "創建方塊失敗",
                    f"資料夾已存在：{block_folder}",
                    parent=root,
                )
                return
            save_block(block, block_folder)
            load_blocks_from_folder(current_folder_path)

        show_create_block_dialog(root, on_submit=_on_submit)

    def handle_theme_changed(theme: str) -> None:
        if hasattr(style, "theme_use"):
            try:
                style.theme_use(theme)
                print(f"Theme changed to: {theme}")
            except Exception as exc:  # pragma: no cover - visual aid
                print(f"Unable to change theme: {exc}")

    tool_catalog = {
        "主要": ("快速輸入", "片語組合"),
        "功能": ("複製輸出", "清空輸入"),
        "美術": tuple(),
        "其他": ("設定",),
    }

    TopBar(
        root,
        on_category_changed=handle_category_changed,
        on_create_block=handle_create_block,
        tools_by_category=tool_catalog,
        on_theme_changed=handle_theme_changed,
    ).pack(fill="x")

    main_frame = ttk.Frame(root)
    main_frame.pack(fill="both", expand=True)
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure(0, weight=2)
    main_frame.grid_columnconfigure(1, weight=3)
    main_frame.grid_columnconfigure(2, weight=2)

    editor_panel = EditorPanel(main_frame)
    output_panel = OutputPanel(main_frame)
    blocks_panel: BlocksPanel | None = None

    def prompt_for_inputs(block: Block) -> dict[int, str] | None:
        input_ids = block.inputs or block.get_used_inputs_from_templates()
        if not input_ids:
            return {}
        values: dict[int, str] = {}
        for idx in input_ids:
            value = simpledialog.askstring("輸入文字", f"請輸入「輸入文字({idx})」：", parent=root)
            if value is None:
                return None
            values[idx] = value
        return values

    def handle_block_clicked(block: Block) -> None:
        validation = block.validate_inputs()
        if validation.missing_inputs:
            messagebox.showwarning(
                "方塊設定不完整",
                f"方塊缺少輸入: {', '.join(str(i) for i in validation.missing_inputs)}",
                parent=root,
            )
        values = prompt_for_inputs(block)
        if values is None:
            return
        editor_panel.set_text(render_block_for_input(block, values))
        output_panel.set_text(render_block_for_output(block, values))

    def load_blocks_from_folder(path: str) -> None:
        folder = Path(path)
        try:
            entries = list_block_folder_entries(folder)
        except Exception as exc:
            messagebox.showerror("讀取方塊失敗", str(exc), parent=root)
            return
        block_locations.clear()
        blocks: list[Block] = []
        for block, block_path in entries:
            block_locations[block.name] = block_path
            blocks.append(block)
        if blocks_panel is not None:
            blocks_panel.set_blocks(blocks)
        print(f"Loaded {len(blocks)} blocks from {folder}")

    def handle_folder_changed(path: str) -> None:
        nonlocal current_folder_path
        current_folder_path = path
        load_blocks_from_folder(path)

    def handle_block_delete(block: Block) -> None:
        path = block_locations.get(block.name)
        if path is None:
            return
        confirm = messagebox.askyesno(
            "刪除方塊",
            f"確認刪除方塊「{block.display_text}」？這個動作無法復原。",
            parent=root,
        )
        if not confirm:
            return
        delete_block(path)
        load_blocks_from_folder(current_folder_path)

    def handle_block_rename(block: Block) -> None:
        path = block_locations.get(block.name)
        if path is None:
            return
        new_name = simpledialog.askstring(
            "重新命名方塊",
            "請輸入新的方塊資料夾名稱：",
            initialvalue=block.name,
            parent=root,
        )
        if not new_name or new_name.strip() == block.name:
            return
        try:
            rename_block_folder(path, new_name.strip())
        except FileExistsError:
            messagebox.showerror("重新命名失敗", "已存在相同名稱的方塊。", parent=root)
            return
        except Exception as exc:
            messagebox.showerror("重新命名失敗", str(exc), parent=root)
            return
        load_blocks_from_folder(current_folder_path)

    blocks_panel = BlocksPanel(
        main_frame,
        on_folder_changed=handle_folder_changed,
        on_block_clicked=handle_block_clicked,
        on_block_delete=handle_block_delete,
        on_block_rename=handle_block_rename,
    )
    blocks_panel.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
    blocks_panel.set_folder_path(str(default_folder))
    load_blocks_from_folder(str(default_folder))

    editor_panel.grid(row=0, column=1, sticky="nsew", padx=6, pady=6)
    output_panel.grid(row=0, column=2, sticky="nsew", padx=6, pady=6)

    root.mainloop()


if __name__ == "__main__":
    main()
