"""Simple template helpers for lazy_block package."""

from __future__ import annotations

import re

from .blocks_model import Block

_INPUT_PATTERN = re.compile(r"\{輸入文字\((\d+)\)\}")


def extract_input_ids_from_template(template: str) -> list[int]:
    matches = _INPUT_PATTERN.findall(template or "")
    return list(dict.fromkeys(int(m) for m in matches))


def render_template(template: str, values: dict[int, str]) -> str:
    def replace(match: re.Match[str]) -> str:
        idx = int(match.group(1))
        return values.get(idx, "")

    return _INPUT_PATTERN.sub(replace, template or "")


def render_block_for_input(block: Block, values: dict[int, str]) -> str:
    return render_template(block.input_template, values)


def render_block_for_output(block: Block, values: dict[int, str]) -> str:
    return render_template(block.output_template, values)