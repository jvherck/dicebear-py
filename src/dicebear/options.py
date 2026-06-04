from __future__ import annotations

from dataclasses import dataclass

from dicebear.types import Color


@dataclass
class Options:
    flip: bool | None = None
    rotate: int | None = None
    scale: int | None = None
    radius: int | None = None
    size: int | None = None
    translateX: int | None = None
    translateY: int | None = None
    backgroundColor: Color | str | None = None
    backgroundType: str | None = None
    backgroundRotation: int | None = None
