from __future__ import annotations

import re
from dataclasses import dataclass


_INPUT_PATTERN = re.compile(r"\{輸入文字\((\d+)\)\}")


@dataclass
class Block:
    name: str
    display_text: str
    input_template: str
    output_template: str
    inputs: list[int]

    @classmethod
    def from_dict(cls, data: dict) -> "Block":
        return cls(
            name=data["name"],
            display_text=data["display_text"],
            input_template=data["input_template"],
            output_template=data["output_template"],
            inputs=list(data.get("inputs", [])),
        )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "display_text": self.display_text,
            "input_template": self.input_template,
            "output_template": self.output_template,
            "inputs": list(self.inputs),
        }

    def get_used_inputs_from_templates(self) -> list[int]:
        values = set(_INPUT_PATTERN.findall(self.input_template))
        values.update(_INPUT_PATTERN.findall(self.output_template))
        return sorted(int(v) for v in values)
    
from core.blocks_model import Block

__all__ = ["Block"]