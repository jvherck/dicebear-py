# dicebear — Python package

## Important

This is a complete rewrite. The old codebase was an HTTP API wrapper
and is entirely obsolete. Do not reference, preserve, or work around
any old code. Every file is written from scratch. There is no
migration concern at the implementation level — that is the README's
problem, not the code's.

## What this package is

`dicebear` is a Python library for generating DiceBear avatars locally.
Avatars are produced entirely in-process from JSON style definitions —
no HTTP calls, no dependency on api.dicebear.com.

PyPI: https://pypi.org/project/dicebear/
Docs: https://dicebear.vhjan.me/

## Reference implementation

The JS core at `../dicebear-js/src/js/core/src/` is the authoritative
reference. When in doubt about rendering behaviour, read the JS source.
The parity fixtures at `../dicebear-js/tests/fixtures/parity/` define
correct output — the Python implementation must produce byte-identical
SVGs for the same seed and style.

| JS file              | Python equivalent                   |
|----------------------|-------------------------------------|
| `Prng/Fnv1a.js`      | `_prng.py` → `_fnv1a()`             |
| `Prng/Mulberry32.js` | `_prng.py` → `Mulberry32`           |
| `Prng.js`            | `_prng.py` → `Prng` class           |
| `Options.js`         | `_options_resolver.py` → `Resolver` |
| `Renderer.js`        | `_renderer.py`                      |
| `Avatar.js`          | `avatar.py` → `Avatar`              |

## Style definitions source

Style definitions come from the official `dicebear-styles` PyPI package
(`pip install dicebear-styles`), maintained by the official DiceBear project.
Never sync or bundle JSON files manually — the pip package handles versioning.

The raw load call exists in exactly one place and nowhere else:

```python
# src/dicebear/_loader.py — only place that touches importlib.resources
from importlib.resources import files
import json


def load_style(name: str) -> dict:
    try:
        return json.loads(
            files('dicebear_styles').joinpath(f'{name}.json').read_text('utf-8')
        )
    except FileNotFoundError:
        raise ValueError(
            f"Unknown style '{name}'. "
            f"Try upgrading: pip install -U dicebear-styles"
        )
```

## Package structure

```
dicebear-py/
  src/dicebear/
    __init__.py            ← public exports: Avatar, Options, Color, Format
    avatar.py              ← Avatar class
    options.py             ← Options dataclass (public, user-facing)
    types.py               ← Color, Format
    _loader.py             ← internal, single place that touches importlib.resources
    _prng.py               ← internal, FNV-1a, Mulberry32, all PRNG selection methods
    _options_resolver.py   ← internal, options resolution (mirrors JS Options.js)
    _renderer.py           ← internal, SVG rendering pipeline (mirrors JS Renderer.js)
    styles/
      __init__.py          ← re-exports all style classes (AUTO-GENERATED)
      _style.py            ← internal, StyleBase base class
      avataaars.py         ← Avataaars style class (AUTO-GENERATED)
      pixel_art.py         ← PixelArt style class (AUTO-GENERATED)
      adventurer.py        ← Adventurer style class (AUTO-GENERATED)
      ...                  ← one file per style (AUTO-GENERATED)
  scripts/
    generate_styles.py     ← reads dicebear-styles, writes src/dicebear/styles/
  tests/
    test_prng.py           ← parity tests against fixtures/fnv1a.json + mulberry32.json
    test_prng_methods.py   ← parity tests against fixtures/prng.json
    test_renderer.py       ← parity tests against fixtures/avatars/*.json
    test_avatar.py         ← public API integration tests
  pyproject.toml
```

## Naming conventions

- Underscore prefix = internal implementation detail, never imported
  directly by users (_prng.py, _renderer.py, _options_resolver.py,
  _loader.py, styles/_style.py)
- No underscore = public API, user-facing or re-exported via
  __init__.py (avatar.py, options.py, types.py)

## Public API

### Creating an avatar

```python
from dicebear import Avatar, Options, Color, Format
from dicebear.styles import Avataaars, PixelArt

# Style-specific options passed to the style instance
# Universal options passed to Options
av = Avatar(
    Avataaars(eyes=Avataaars.Eyes.WINK, hair=Avataaars.Hair.SHORT_HAIR_SHORT_FLAT),
    seed="john doe",
    options=Options(flip=True, rotate=90, backgroundColor=Color("00ddd0")),
)

# Style with no customisation
av = Avatar(PixelArt(), seed="jane doe")

# SVG output — generated locally, no network
print(av.svg)  # str — raw SVG string
```

### Saving

```python
av.save("avatar.svg")
av.save("avatar.svg", overwrite=True)
```

### Pillow integration (optional dependency)

```python
img: PIL.Image.Image = av.pillow()
```

### Bulk creation

```python
avatars: list[Avatar] = Avatar.bulk_create(Avataaars, amount=10)

# With fixed style options applied to all
avatars = Avatar.bulk_create(
    Avataaars(eyes=Avataaars.Eyes.WINK),
    amount=10,
    options=Options(flip=True),
)
```

## Style class design — the core DX decision

Each style is a generated class with:

- Nested `Enum` classes for every component (the static data / namespace)
- A fully typed `__init__` that accepts those enums (the DX / IDE hints)
- Inherits `StyleBase`

This design means:

- Typing `Avataaars(` → IDE shows every available component param with its type
- Typing `Avataaars.` → IDE shows every nested Enum class
- Typing `Avataaars.Eyes.` → IDE shows every valid variant
- Typos in variant names are caught at type-check time, not silently at render time
- `str` is always accepted as a fallback for forward compatibility

```python
# AUTO-GENERATED from avataaars.json — do not edit
from __future__ import annotations
from enum import Enum
from ._style import StyleBase


class Avataaars(StyleBase):
    _name = "avataaars"

    class Eyes(Enum):
        WINK = "wink"
        DEFAULT = "default"
        HAPPY = "happy"

    class Hair(Enum):
        SHORT_HAIR_SHORT_FLAT = "shortHairShortFlat"
        LONG_HAIR_STRAIGHT = "longHairStraight"

    class SkinColor(Enum):
        TANNED = "tanned"
        PALE = "pale"

    def __init__(
            self,
            eyes: Eyes | str | None = None,
            eyesProbability: int | None = None,
            hair: Hair | str | None = None,
            hairProbability: int | None = None,
            skinColor: SkinColor | str | None = None,
    ) -> None:
        super().__init__(
            eyes=eyes,
            eyesProbability=eyesProbability,
            hair=hair,
            hairProbability=hairProbability,
            skinColor=skinColor,
        )
```

Note: generated style files use relative imports (`from ._style import StyleBase`)
since they live in the same package as `_style.py`.

### StyleBase

```python
# src/dicebear/styles/_style.py
from enum import Enum


class StyleBase:
    _name: str  # overridden per generated subclass

    def __init__(self, **kwargs) -> None:
        # Unwrap Enum values to strings, drop None values
        self._resolved: dict[str, str | int | bool] = {
            k: (v.value if isinstance(v, Enum) else v)
            for k, v in kwargs.items()
            if v is not None
        }

    @classmethod
    def load_definition(cls) -> dict:
        from dicebear._loader import load_style
        return load_style(cls._name)
```

### Naming conventions for generated code

| Source (JSON)                 | Generated                                   |
|-------------------------------|---------------------------------------------|
| Style name `"pixel-art"`      | Class name `PixelArt`                       |
| Style name `"avataaars"`      | Class name `Avataaars`                      |
| Component name `"eyes"`       | Nested class `Eyes`                         |
| Component name `"skinColor"`  | Nested class `SkinColor`                    |
| Variant name `"variant01"`    | Enum member `VARIANT01`                     |
| Variant name `"longCurly"`    | Enum member `LONG_CURLY`                    |
| Variant name `"angryNatural"` | Enum member `ANGRY_NATURAL`                 |
| Module filename               | `snake_case` of style name (`pixel_art.py`) |

Component aliases (defined via `extends` in JSON) share the source
component's Enum class — never generate a duplicate Enum for an alias.

## Options design

Universal rendering options only. No style awareness, no kwargs, no
`**extra`. Every field is explicitly typed. Adding an unknown field is
a type error, not a silent passthrough.

```python
# src/dicebear/options.py
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
```

## Avatar design

```python
# src/dicebear/avatar.py
from dicebear.styles._style import StyleBase
from dicebear.options import Options
from dicebear.types import Format


class Avatar:
    def __init__(
            self,
            style: StyleBase,
            seed: str,
            options: Options | None = None,
    ) -> None:
        self._style = style
        self._seed = seed
        self._options = options or Options()
        self._svg: str | None = None  # lazy — not rendered until accessed

    @property
    def svg(self) -> str:
        if self._svg is None:
            definition = self._style.load_definition()
            self._svg = render(
                definition,
                self._seed,
                self._style._resolved,
                self._options,
            )
        return self._svg

    def save(self, path: str, *, format: Format = Format.SVG, overwrite: bool = False) -> None:
        ...

    def pillow(self):
        ...

    @classmethod
    def bulk_create(
            cls,
            style: type[StyleBase] | StyleBase,
            amount: int,
            options: Options | None = None,
    ) -> list[Avatar]:
        ...
```

The JSON definition is only loaded when `.svg` is first accessed.
Constructing an `Avatar` is always instant regardless of how many are created.

## types.py design

```python
# src/dicebear/types.py
from enum import Enum


class Color:
    # Accepts "ff0000" or "#ff0000", normalises to "#ff0000"
    # Raises ValueError on invalid hex
    # Implements __str__, __eq__, __hash__
    ...


class Format(Enum):
    SVG = "svg"
    PNG = "png"
    JPG = "jpg"
    JPEG = "jpeg"
    WEBP = "webp"
    AVIF = "avif"
```

## _prng.py — critical implementation notes

This is the most important correctness requirement. Read
`../dicebear-js/src/js/core/src/Prng/Fnv1a.js` carefully before
writing a single line.

FNV-1a MUST iterate UTF-16 code units — not Unicode code points, not
UTF-8 bytes. For ASCII they are identical, but for input outside the
Basic Multilingual Plane (emoji, some CJK) they diverge and will produce
wrong hashes that cascade into wrong avatar output.

```python
def _fnv1a(text: str) -> int:
    # encode to UTF-16 LE, read as 16-bit units — matches JS charCodeAt()
    encoded = text.encode('utf-16-le')
    hash_ = 0x811c9dc5
    for i in range(0, len(encoded), 2):
        code_unit = encoded[i] | (encoded[i + 1] << 8)
        hash_ ^= code_unit
        hash_ = (hash_ * 0x01000193) & 0xffffffff
    return hash_
```

Mulberry32 must replicate JS 32-bit signed overflow (`| 0` in JS):

```python
def _to_int32(n: int) -> int:
    n &= 0xffffffff
    return n - 0x100000000 if n >= 0x80000000 else n
```

These are already implemented and all parity tests pass — do not
modify _prng.py.

## Testing order

Always work in this order — each layer depends on the one below it:

1. `test_prng.py` — FNV-1a and Mulberry32 against `fnv1a.json` + `mulberry32.json`
2. `test_prng_methods.py` — pick, weightedPick, bool, float, integer, shuffle against `prng.json`
3. `test_renderer.py` — full SVG output against `avatars/*.json` (byte-identical)
4. `test_avatar.py` — public API integration tests

The parity fixture files are the ground truth. Never modify them.
Never write tests that assert against hardcoded strings you invented —
always derive expected values from the fixture files.

## Code generation

`scripts/generate_styles.py` reads from the installed `dicebear-styles`
package and writes `src/dicebear/styles/*.py`. All generated files start with:

```python
# AUTO-GENERATED by scripts/generate_styles.py — do not edit manually
# Source: dicebear-styles <version>
```

Generated files use relative imports:

```python
from ._style import StyleBase
```

Generated files are committed to the repo. Users never run the generator.
The generator runs in CI when `dicebear-styles` releases a new version,
opens a PR, and a human reviews before merging.

## Dependencies

```toml
[project]
dependencies = [
    "dicebear-styles>=10.0.0",
]

[project.optional-dependencies]
pillow = [
    "cairosvg>=2.7.0",
    "Pillow>=10.0.0",
]
```

The core engine (`_prng.py`, `_renderer.py`, `_options_resolver.py`)
uses only the standard library. Do not add third-party imports to these
files. Ask before touching `pyproject.toml`.

## Python conventions

- Python 3.10+ minimum
- Type hints on every function and method signature — no bare `Any`
- `X | Y` union syntax — never `Optional[X]` or `Union[X, Y]`
- `@dataclass` for data-holding classes
- `snake_case` for modules, functions, variables, method names
- `PascalCase` for classes including generated style classes
- `SCREAMING_SNAKE_CASE` for enum members
- `importlib.resources.files()` for all resource access — never `__file__`,
  `os.path`, or `pathlib.Path(__file__).parent` tricks
- SOLID principles throughout — single responsibility per class,
  depend on abstractions not concretions

## Do not touch without asking

- `pyproject.toml`
- `.github/workflows/`
- `tests/` (ask before modifying existing tests; adding new ones is fine)
- `src/dicebear/_prng.py` (complete, all parity tests pass)
- `src/dicebear/_options_resolver.py` (complete, all parity tests pass)
- `src/dicebear/_renderer.py` (complete, all parity tests pass)
- `src/dicebear/_loader.py` (complete)
- `src/dicebear/styles/_style.py` (complete)
- Any AUTO-GENERATED file under `src/dicebear/styles/` (re-run the
  generator instead)
