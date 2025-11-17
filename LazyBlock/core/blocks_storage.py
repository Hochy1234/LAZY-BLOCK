from __future__ import annotations

import json
from pathlib import Path

from .blocks_model import Block


_BLOCK_FILE_NAME = "block.json"


def load_block(block_folder: Path) -> Block:
    block_file = block_folder / _BLOCK_FILE_NAME
    with block_file.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return Block.from_dict(data)


def save_block(block: Block, block_folder: Path) -> None:
    block_folder.mkdir(parents=True, exist_ok=True)
    block_file = block_folder / _BLOCK_FILE_NAME
    with block_file.open("w", encoding="utf-8") as file:
        json.dump(block.to_dict(), file, ensure_ascii=False, indent=2)


def list_blocks_in_folder(root_folder: Path) -> list[Block]:
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