from __future__ import annotations

import re
from dataclasses import dataclass, field


_INPUT_PATTERN = re.compile(r"\{輸入文字\((\d+)\)\}")


@dataclass(frozen=True)
class BlockValidation:
    """Simple container describing problems found on a block definition."""

    missing_inputs: list[int] = field(default_factory=list)
    unused_inputs: list[int] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.missing_inputs and not self.unused_inputs


@dataclass
class Block:
    name: str
    display_text: str
    input_template: str
    output_template: str
    inputs: list[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        # Keep the inputs list deterministic and deduplicated.
        self.inputs = sorted(dict.fromkeys(self.inputs))

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

    def validate_inputs(self) -> BlockValidation:
        required = self.get_used_inputs_from_templates()
        declared = list(self.inputs)
        missing = [idx for idx in required if idx not in declared]
        unused = [idx for idx in declared if idx not in required]
        return BlockValidation(missing_inputs=missing, unused_inputs=unused)


__all__ = ["Block", "BlockValidation"]
