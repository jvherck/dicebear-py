from __future__ import annotations

import re
from enum import Enum

_HEX_RE = re.compile(r'^#?([0-9a-fA-F]{6})$')


class Color:
    def __init__(self, value: str) -> None:
        m = _HEX_RE.match(value)
        if not m and value != "transparent":
            raise ValueError(f"Invalid hex color: {value!r}. Expected 6-digit hex like 'ff0000' or '#ff0000'.")
        self._value = '#' + m.group(1).lower()

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f'Color({self._value!r})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Color):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)


class Format(Enum):
    SVG = "svg"
    PNG = "png"
    JPG = "jpg"
    JPEG = "jpeg"
    WEBP = "webp"
