from __future__ import annotations

from enum import Enum

__all__ = ("StyleBase",)


class StyleBase:
    _name: str

    def __init__(self, **kwargs) -> None:
        self._resolved: dict[str, str | int | bool] = {
            k: (v.value if isinstance(v, Enum) else v) for k, v in kwargs.items() if v is not None
        }

    @classmethod
    def load_definition(cls) -> dict:
        from dicebear._loader import load_style

        return load_style(cls._name)
