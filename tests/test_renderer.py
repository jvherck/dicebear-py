"""
Parity tests for _renderer.py, _number_format, and _initials_from_seed.

Fixtures:
  ../dicebear-js/tests/fixtures/parity/avatars/*.json   — byte-identical SVG
  ../dicebear-js/tests/fixtures/parity/numbers.json     — Number.format cases
  ../dicebear-js/tests/fixtures/parity/initials.json    — Initials.fromSeed cases
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from dicebear._renderer import render, _number_format, _initials_from_seed

PARITY = Path(__file__).parent.parent.parent / "dicebear-js" / "tests" / "fixtures" / "parity"
AVATARS = PARITY / "avatars"
STYLES  = PARITY / "styles"

STYLE_NAMES = ["thumbs", "glass", "initials", "notionists", "shape-grid"]

# ---------------------------------------------------------------------------
# Fixture data loaded at import time
# ---------------------------------------------------------------------------

def _load_avatar_cases(style_name: str) -> list[dict]:
    return json.loads((AVATARS / f"{style_name}.json").read_text("utf-8"))


def _load_style(style_name: str) -> dict:
    return json.loads((STYLES / f"{style_name}.json").read_text("utf-8"))


_NUMBER_CASES: list[dict] = json.loads((PARITY / "numbers.json").read_text("utf-8"))
_INITIALS_CASES: list[dict] = json.loads((PARITY / "initials.json").read_text("utf-8"))

_ALL_AVATAR_CASES: list[tuple[str, dict]] = [
    (sn, case)
    for sn in STYLE_NAMES
    for case in _load_avatar_cases(sn)
]

# Pre-load style definitions once (they're large for notionists)
_STYLE_DEFS: dict[str, dict] = {sn: _load_style(sn) for sn in STYLE_NAMES}


# ---------------------------------------------------------------------------
# Number.format parity
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "case",
    _NUMBER_CASES,
    ids=[str(c["input"]) for c in _NUMBER_CASES],
)
def test_number_format(case: dict) -> None:
    assert _number_format(case["input"]) == case["output"]


# ---------------------------------------------------------------------------
# Initials.fromSeed parity
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "case",
    _INITIALS_CASES,
    ids=[repr(c["seed"]) for c in _INITIALS_CASES],
)
def test_initials_from_seed(case: dict) -> None:
    assert _initials_from_seed(case["seed"]) == case["result"]


# ---------------------------------------------------------------------------
# Full SVG parity (byte-identical)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "style_name, case",
    _ALL_AVATAR_CASES,
    ids=[f"{sn}:{c['id']}" for sn, c in _ALL_AVATAR_CASES],
)
def test_render_svg(style_name: str, case: dict) -> None:
    definition = _STYLE_DEFS[style_name]
    result = render(definition, case["options"])
    assert result == case["svg"]
