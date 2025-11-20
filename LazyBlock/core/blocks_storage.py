from __future__ import annotations

import json
import shutil
from pathlib import Path

from .blocks_model import Block


_BLOCK_FILE_NAME = "block.json"


def load_block(block_folder: Path) -> Block:
    """Read a block definition from ``block.json`` inside the folder."""
    block_file = block_folder / _BLOCK_FILE_NAME
    with block_file.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return Block.from_dict(data)


def save_block(block: Block, block_folder: Path) -> None:
    """Persist the block definition to its folder."""
    block_folder.mkdir(parents=True, exist_ok=True)
    block_file = block_folder / _BLOCK_FILE_NAME
    with block_file.open("w", encoding="utf-8") as file:
        json.dump(block.to_dict(), file, ensure_ascii=False, indent=2)


def delete_block(block_folder: Path) -> None:
    """Remove a block folder and its contents."""
    if block_folder.exists() and block_folder.is_dir():
        shutil.rmtree(block_folder)


def rename_block_folder(block_folder: Path, new_name: str) -> Path:
    """Rename a block folder and update the block's internal name."""
    if "/" in new_name or "\\" in new_name:
        raise ValueError("資料夾名稱不可包含路徑符號。")
    new_folder = block_folder.with_name(new_name)
    if new_folder.exists():
        raise FileExistsError(f"目標資料夾已存在: {new_folder}")
    shutil.move(str(block_folder), str(new_folder))
    block = load_block(new_folder)
    block.name = new_name
    save_block(block, new_folder)
    return new_folder


def list_block_folder_entries(root_folder: Path) -> list[tuple[Block, Path]]:
    """Enumerate blocks with their backing folders."""
    if not root_folder.exists():
        return []

    entries: list[tuple[Block, Path]] = []
    for child in root_folder.iterdir():
        if not child.is_dir():
            continue
        block_file = child / _BLOCK_FILE_NAME
        if block_file.is_file():
            entries.append((load_block(child), child))
    return entries


def list_blocks_in_folder(root_folder: Path) -> list[Block]:
    """Backwards-compatible helper returning only block objects."""
    return [block for block, _ in list_block_folder_entries(root_folder)]


__all__ = [
    "load_block",
    "save_block",
    "delete_block",
    "rename_block_folder",
    "list_block_folder_entries",
    "list_blocks_in_folder",
]
