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


def list_blocks_in_folder(root_folder: Path) -> list[Block]:
    """Enumerate all blocks stored under the provided root folder."""
    if not root_folder.exists():
        return []

    blocks: list[Block] = []
    for child in root_folder.iterdir():
        if not child.is_dir():
            continue
        block_file = child / _BLOCK_FILE_NAME
        if block_file.is_file():
            blocks.append(load_block(child))
    return blocks


__all__ = ["load_block", "save_block", "delete_block", "list_blocks_in_folder"]
