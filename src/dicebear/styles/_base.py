from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any, ClassVar

__all__ = ("StyleBase",)


@dataclass
class StyleBase:
    style_name: ClassVar[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            f.name: getattr(self, f.name)
            for f in fields(self)
            if getattr(self, f.name) is not None
        }

    def __str__(self) -> str:
        return self.style_name

    def __repr__(self) -> str:
        set_fields = {
            f.name: getattr(self, f.name)
            for f in fields(self)
            if getattr(self, f.name) is not None
        }
        args = ", ".join(f"{k}={v!r}" for k, v in set_fields.items())
        return f"{type(self).__name__}({args})"
