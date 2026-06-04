from __future__ import annotations

from typing import Any

from dicebear._prng import Prng


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class CircularColorReferenceError(Exception):
    def __init__(self, chain: list[str]) -> None:
        super().__init__('Circular color reference: ' + ' -> '.join(chain))
        self.chain = chain


# ---------------------------------------------------------------------------
# Colour utilities  (also imported by _renderer.py)
# ---------------------------------------------------------------------------

def _to_hex(hex_str: str) -> str:
    """Normalize any hex color to 6- or 8-digit lowercase with # prefix."""
    h = hex_str.lstrip('#').lower()
    if len(h) == 3:
        return '#' + h[0] * 2 + h[1] * 2 + h[2] * 2
    if len(h) == 4:
        return '#' + h[0] * 2 + h[1] * 2 + h[2] * 2 + h[3] * 2
    return '#' + h


def _to_rgb_hex(hex_str: str) -> str:
    """Strip alpha channel and return 6-digit hex."""
    h = _to_hex(hex_str)
    return h[:7] if len(h) > 7 else h


def _parse_hex(hex_str: str) -> tuple[int, int, int]:
    """Parse a hex color into an (r, g, b) tuple of 8-bit values."""
    h = _to_hex(hex_str)[1:]
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _linearize(channel: int) -> float:
    """Convert an 8-bit sRGB channel to linear-light space (WCAG 2.1)."""
    s = channel / 255
    if s <= 0.04045:
        return s / 12.92
    return ((s + 0.055) / 1.055) ** 2.4


def _luminance(hex_str: str) -> float:
    """WCAG 2.1 relative luminance for a hex color."""
    r, g, b = _parse_hex(hex_str)
    return 0.2126 * _linearize(r) + 0.7152 * _linearize(g) + 0.0722 * _linearize(b)


def _sort_by_contrast(candidates: list[str], ref_color: str) -> list[str]:
    """Return candidates sorted by descending WCAG contrast ratio against ref_color."""
    ref_lum = _luminance(ref_color)

    def ratio(c: str) -> float:
        lum = _luminance(c)
        hi, lo = max(lum, ref_lum), min(lum, ref_lum)
        return (hi + 0.05) / (lo + 0.05)

    return sorted(candidates, key=ratio, reverse=True)


def _filter_not_equal_to(candidates: list[str], excluded: list[str]) -> list[str]:
    """Remove excluded colors (compared as 6-digit RGB hex); fall back to originals if all excluded."""
    excluded_set = {_to_rgb_hex(c) for c in excluded}
    filtered = [c for c in candidates if _to_rgb_hex(c) not in excluded_set]
    return filtered if filtered else list(candidates)


# ---------------------------------------------------------------------------
# Input normalisation helpers
# ---------------------------------------------------------------------------

def _to_range(value: Any) -> dict | None:
    """
    Convert a user-facing range option to {min, max} or None.

    Scalar → {min: n, max: n}; [n] → {min: n, max: n}; [a, b] → sorted bounds.
    None or [] → None (resolver falls back to default).
    """
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        n = float(value)
        return {'min': n, 'max': n}
    if isinstance(value, list):
        if not value:
            return None
        nums = [float(v) for v in value]
        return {'min': min(nums), 'max': max(nums)}
    return None


def _as_array(value: Any) -> list:
    """Normalise scalar/array/None to a list."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


# ---------------------------------------------------------------------------
# Resolver
# ---------------------------------------------------------------------------

class Resolver:
    """
    Key-based options resolver.

    Combines the JS Options (input normalisation) and Resolver (PRNG-based
    resolution) into one class. Takes a raw style definition dict and a raw
    user-options dict; derives a seeded Prng. Every public accessor memoises
    its result under the camelCase key used in the JS snapshot so that
    resolved() matches the parity fixture format exactly.
    """

    def __init__(self, definition: dict, user_options: dict) -> None:
        self._definition = definition
        self._opts = user_options
        self._seed: str = user_options.get('seed') or ''
        self._prng = Prng(self._seed)
        self._memo: dict[str, Any] = {}
        self._color_resolving: list[str] = []

    # -----------------------------------------------------------------------
    # Public accessors — scalar pass-through
    # -----------------------------------------------------------------------

    def seed(self) -> str:
        # Deliberately NOT memoised — excluded from the resolved() snapshot.
        return self._seed

    def size(self) -> int | None:
        return self._memo_get('size', lambda: self._opts.get('size'))

    def id_randomization(self) -> bool:
        return self._memo_get('idRandomization', lambda: bool(self._opts.get('idRandomization', False)))

    def title(self) -> str | None:
        return self._memo_get('title', lambda: self._opts.get('title'))

    # -----------------------------------------------------------------------
    # Public accessors — PRNG picks
    # -----------------------------------------------------------------------

    def flip(self) -> str:
        return self._memo_get(
            'flip',
            lambda: self._prng.pick('flip', _as_array(self._opts.get('flip'))) or 'none',
        )

    def font_family(self) -> str:
        return self._memo_get(
            'fontFamily',
            lambda: self._prng.pick('fontFamily', _as_array(self._opts.get('fontFamily'))) or 'system-ui',
        )

    def font_weight(self) -> int | float:
        return self._memo_get(
            'fontWeight',
            lambda: self._prng.pick('fontWeight', _as_array(self._opts.get('fontWeight'))) or 400,
        )

    # -----------------------------------------------------------------------
    # Public accessors — PRNG floats
    # -----------------------------------------------------------------------

    def scale(self) -> float:
        return self._memo_float('scale', _to_range(self._opts.get('scale')), 1.0)

    def border_radius(self) -> float:
        return self._memo_float('borderRadius', _to_range(self._opts.get('borderRadius')), 0.0)

    def rotate(self) -> float:
        return self._memo_float('rotate', _to_range(self._opts.get('rotate')), 0.0)

    def translate_x(self) -> float:
        return self._memo_float('translateX', _to_range(self._opts.get('translateX')), 0.0)

    def translate_y(self) -> float:
        return self._memo_float('translateY', _to_range(self._opts.get('translateY')), 0.0)

    # -----------------------------------------------------------------------
    # Public accessors — component resolution
    # -----------------------------------------------------------------------

    def variant(self, name: str) -> str | None:
        """
        Pick a variant for component `name`.

        Returns None when the component is not defined, the probability check
        fails, or all user-specified variants are invalid (none exist in the
        style definition).
        """
        def compute() -> str | None:
            comp_raw = self._definition.get('components', {}).get(name)
            if comp_raw is None:
                return None

            base = self._base_component(name)
            source = self._source_name(name)

            user_prob = self._opts.get(f'{source}Probability')
            style_prob = (base or {}).get('probability', 100)
            prob = user_prob if user_prob is not None else style_prob

            if not self._prng.bool(f'{name}Probability', prob):
                return None

            all_variants: dict = (base or {}).get('variants', {})
            raw = self._variant_option(source)
            weights: dict[str, float] = {}

            if raw is None:
                for v, vdata in all_variants.items():
                    weights[v] = float(vdata.get('weight', 1))
            else:
                for v, w in raw.items():
                    if v in all_variants:
                        weights[v] = float(w)

            return self._prng.weighted_pick(f'{name}Variant', weights)

        return self._memo_get(f'{name}Variant', compute)

    def color(self, name: str) -> list[str]:
        return self._memo_get(f'{name}Color', lambda: self._resolve_color(name))

    def color_fill(self, name: str) -> str:
        return self._memo_get(
            f'{name}ColorFill',
            lambda: self._prng.pick(f'{name}ColorFill', _as_array(self._opts.get(f'{name}ColorFill'))) or 'solid',
        )

    def color_angle(self, name: str) -> float:
        return self._memo_float(
            f'{name}ColorAngle',
            _to_range(self._opts.get(f'{name}ColorAngle')),
            0.0,
        )

    def component_transform(self, name: str) -> dict:
        """
        Resolve and memoize per-component rotate/translateX/translateY/scale.

        The four values are stored under camelCase keys so they appear
        correctly in resolved(). Returns a dict with snake_case keys for
        callers (Renderer).
        """
        base = self._base_component(name)
        translate = ((base or {}).get('translate') or {})
        return {
            'rotate':      self._memo_float(f'{name}Rotate',     (base or {}).get('rotate'),    0.0),
            'translate_x': self._memo_float(f'{name}TranslateX', translate.get('x'),            0.0),
            'translate_y': self._memo_float(f'{name}TranslateY', translate.get('y'),            0.0),
            'scale':       self._memo_float(f'{name}Scale',      (base or {}).get('scale'),     1.0),
        }

    def resolved(self) -> dict:
        """
        Snapshot of every memoised value, excluding None (hidden components).

        Matches the JS Resolver.resolved() behaviour: keys set to undefined
        in JS are excluded from JSON.stringify — in Python we filter None.
        Seed is never included.
        """
        return {k: v for k, v in self._memo.items() if v is not None}

    # -----------------------------------------------------------------------
    # Private helpers
    # -----------------------------------------------------------------------

    def _memo_get(self, key: str, compute) -> Any:
        if key not in self._memo:
            self._memo[key] = compute()
        return self._memo[key]

    def _memo_float(self, key: str, range_: dict | None, fallback: float) -> float:
        return self._memo_get(
            key,
            lambda: self._prng.float(key, range_) if range_ is not None else fallback,
        )

    def _source_name(self, name: str) -> str:
        comp = self._definition.get('components', {}).get(name, {})
        return comp.get('extends', name)

    def _base_component(self, name: str) -> dict | None:
        """Follow one level of 'extends' to reach the base component data."""
        components = self._definition.get('components', {})
        comp = components.get(name)
        if comp is None:
            return None
        target = comp.get('extends')
        if target is not None:
            return components.get(target)
        return comp

    def _variant_option(self, source_name: str) -> dict[str, float] | None:
        """Normalise ${source_name}Variant user input to a weighted dict, or None."""
        raw = self._opts.get(f'{source_name}Variant')
        if raw is None:
            return None
        if isinstance(raw, str):
            return {raw: 1.0}
        if isinstance(raw, list):
            return {v: 1.0 for v in raw}
        return {k: float(v) for k, v in raw.items()}

    def _color_fill_stops(self, name: str) -> int:
        range_ = _to_range(self._opts.get(f'{name}ColorFillStops'))
        if range_ is not None:
            return self._prng.integer(f'{name}ColorFillStops', range_)
        return 2

    def _resolve_color(self, name: str) -> list[str]:
        user_raw = self._opts.get(f'{name}Color')
        user_colors = [_to_hex(c) for c in _as_array(user_raw)] if user_raw is not None else None

        style_def = self._definition.get('colors', {}).get(name)

        if user_colors is not None:
            source = user_colors
        elif style_def is not None:
            source = [_to_hex(c) for c in style_def.get('values', [])]
        else:
            source = []

        fill = self.color_fill(name)
        stops = 1 if fill == 'solid' else self._color_fill_stops(name)

        if style_def is None:
            return self._prng.shuffle(f'{name}Color', source)[:stops]

        if name in self._color_resolving:
            raise CircularColorReferenceError(self._color_resolving + [name])

        self._color_resolving.append(name)
        try:
            contrast_to: str | None = style_def.get('contrastTo')
            not_equal_to: list[str] = style_def.get('notEqualTo', [])
            candidates = list(source)

            if contrast_to:
                ref = self.color(contrast_to)
                if ref:
                    candidates = _sort_by_contrast(candidates, ref[0])

            if not_equal_to:
                excluded: list[str] = []
                for ref_name in not_equal_to:
                    excluded.extend(self.color(ref_name))
                candidates = _filter_not_equal_to(candidates, excluded)
        finally:
            self._color_resolving.pop()

        if contrast_to:
            return candidates[:stops]
        return self._prng.shuffle(f'{name}Color', candidates)[:stops]
