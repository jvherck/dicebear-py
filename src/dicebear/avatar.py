from __future__ import annotations

import os
import random
import string

from .options import Options
from .styles._style import StyleBase
from .types import Format


class Avatar:
    def __init__(
            self,
            style: StyleBase,
            seed: str,
            options: Options | None = None,
    ) -> None:
        self._style = style
        self._seed = seed
        self._options = options
        self._svg: str | None = None

    @property
    def svg(self) -> str:
        if self._svg is None:
            from dicebear._renderer import render
            definition = self._style.load_definition()
            self._svg = render(definition, self._build_user_options(definition))
        return self._svg

    def _build_user_options(self, definition: dict) -> dict:
        opts: dict = {'seed': self._seed}
        component_names = set(definition.get('components', {}).keys())
        for key, val in self._style._resolved.items():
            opts[f'{key}Variant' if key in component_names else key] = val

        o = self._options
        if o is None:
            return opts

        scalar_mapping = (
            ('flip', o.flip),
            ('rotate', o.rotate),
            ('scale', o.scale),
            ('borderRadius', o.radius),
            ('size', o.size),
            ('translateX', o.translateX),
            ('translateY', o.translateY),
            ('backgroundColorFill', o.backgroundType),
            ('backgroundColorAngle', o.backgroundRotation),
        )
        for key, val in scalar_mapping:
            if val is not None:
                opts[key] = val

        if o.backgroundColor is not None:
            opts['backgroundColor'] = str(o.backgroundColor)

        return opts

    def save(self, path: str, *, format: Format = Format.SVG, overwrite: bool = False) -> None:
        if not overwrite and os.path.exists(path):
            raise FileExistsError(
                f"File already exists: {path!r}. Pass overwrite=True to overwrite."
            )
        if format == Format.SVG:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self.svg)
            return
        try:
            import cairosvg
            from PIL import Image
            import io
        except ImportError as exc:
            raise ImportError(
                "Saving raster formats requires cairosvg and Pillow.\n"
                "Install with: pip install dicebear[pillow]"
            ) from exc
        svg_bytes = self.svg.encode('utf-8')
        if format == Format.PNG:
            cairosvg.svg2png(bytestring=svg_bytes, write_to=path)
        elif format in (Format.JPG, Format.JPEG):
            png = cairosvg.svg2png(bytestring=svg_bytes)
            Image.open(io.BytesIO(png)).convert('RGB').save(path)
        elif format == Format.WEBP:
            png = cairosvg.svg2png(bytestring=svg_bytes)
            Image.open(io.BytesIO(png)).save(path, format='WEBP')

    def pillow(self):
        try:
            import cairosvg
            from PIL import Image
            import io
        except ImportError as exc:
            raise ImportError(
                "pillow() requires cairosvg and Pillow. "
                "Install with: pip install dicebear[pillow]"
            ) from exc
        png_bytes = cairosvg.svg2png(bytestring=self.svg.encode('utf-8'))
        import io as _io
        return Image.open(_io.BytesIO(png_bytes))

    @classmethod
    def bulk_create(
            cls,
            style: type[StyleBase] | StyleBase,
            amount: int,
            options: Options | None = None,
    ) -> list[Avatar]:
        chars = string.ascii_letters + string.digits
        result: list[Avatar] = []
        for _ in range(amount):
            seed = ''.join(random.choices(chars, k=20))
            if isinstance(style, type):
                style_instance: StyleBase = style()
            else:
                style_instance = style
            result.append(cls(style_instance, seed, options))
        return result
