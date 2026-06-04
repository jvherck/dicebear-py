"""
Parity tests for _options_resolver.py.

For each case in the five avatar fixture files, we:
  1. Load the corresponding style definition (parity/styles/*.json).
  2. Construct a Resolver from that definition + the fixture's options.
  3. Exercise the resolver with a traverser that mimics Renderer.render()
     so that exactly the same accessor calls are made.
  4. Assert resolver.resolved() == fixture["resolvedOptions"].

Fixtures live at:
  ../dicebear-js/tests/fixtures/parity/avatars/*.json
  ../dicebear-js/tests/fixtures/parity/styles/*.json
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from dicebear._options_resolver import Resolver

# ---------------------------------------------------------------------------
# Fixture paths
# ---------------------------------------------------------------------------

PARITY = Path(__file__).parent.parent.parent / "dicebear-js" / "tests" / "fixtures" / "parity"
AVATARS = PARITY / "avatars"
STYLES  = PARITY / "styles"

STYLE_NAMES = ["thumbs", "glass", "initials", "notionists", "shape-grid"]


def _load_avatar_cases(style_name: str) -> list[dict]:
    return json.loads((AVATARS / f"{style_name}.json").read_text("utf-8"))


def _load_style(style_name: str) -> dict:
    return json.loads((STYLES / f"{style_name}.json").read_text("utf-8"))


# Build all (style_name, case) pairs once at import time.
_ALL_CASES: list[tuple[str, dict]] = []
for _sn in STYLE_NAMES:
    for _case in _load_avatar_cases(_sn):
        _ALL_CASES.append((_sn, _case))


# ---------------------------------------------------------------------------
# Traverser — mimics Renderer.render() so resolver.resolved() matches fixture
# ---------------------------------------------------------------------------

def _base_component(definition: dict, name: str) -> dict | None:
    """Follow one 'extends' level to the base component data."""
    components = definition.get('components', {})
    comp = components.get(name)
    if comp is None:
        return None
    target = comp.get('extends')
    if target is not None:
        return components.get(target)
    return comp


def _resolve_color_ref(resolver: Resolver, name: str) -> None:
    """
    Mirror Renderer.#resolveColorReference.

    Calls resolver.color() and resolver.color_fill(); calls resolver.color_angle()
    only when building a gradient (non-solid fill with more than one colour stop).
    """
    colors = resolver.color(name)
    fill = resolver.color_fill(name)
    if fill != 'solid' and len(colors) > 1:
        resolver.color_angle(name)


def _process_attr_value(resolver: Resolver, value: Any) -> None:
    """Dispatch a single attribute or text-node value to the appropriate resolver call."""
    if not isinstance(value, dict):
        return
    vtype = value.get('type')
    if vtype == 'color':
        _resolve_color_ref(resolver, value['name'])
    elif vtype == 'variable':
        varname = value.get('name')
        if varname == 'fontFamily':
            resolver.font_family()
        elif varname == 'fontWeight':
            resolver.font_weight()
        # 'initial' / 'initials' → uses resolver.seed() only, not memoised


def _traverse_elements(resolver: Resolver, definition: dict, elements: list[dict]) -> None:
    """
    Recursively walk style-definition elements in the same order as the renderer.

    - 'component' → variant() + component_transform() + recurse into variant elements
    - 'element'   → process attribute colour/variable refs + recurse into children
    - 'text'      → process value variable refs
    """
    for element in elements:
        etype = element.get('type')

        if etype == 'component':
            name = element.get('name')
            if not name:
                continue
            chosen = resolver.variant(name)
            if chosen:
                resolver.component_transform(name)
                base = _base_component(definition, name)
                variant_elements = (base or {}).get('variants', {}).get(chosen, {}).get('elements', [])
                _traverse_elements(resolver, definition, variant_elements)

        elif etype == 'element':
            for attr_val in (element.get('attributes') or {}).values():
                _process_attr_value(resolver, attr_val)
            _traverse_elements(resolver, definition, element.get('children') or [])

        elif etype == 'text':
            _process_attr_value(resolver, element.get('value'))


def exercise_resolver(resolver: Resolver, definition: dict) -> None:
    """
    Drive the resolver through the same call sequence that Renderer.render() uses.

    After this returns, resolver.resolved() should equal the fixture's
    resolvedOptions for the same seed + options.
    """
    # 1. Background (always rendered first; colour_angle only for gradient fills)
    _resolve_color_ref(resolver, 'background')

    # 2. Canvas element tree
    _traverse_elements(resolver, definition, definition.get('canvas', {}).get('elements', []))

    # 3. Global transforms (always applied / always memoised)
    resolver.scale()
    resolver.flip()
    resolver.rotate()
    resolver.translate_x()
    resolver.translate_y()
    resolver.border_radius()

    # 4. Metadata read by the SVG tag builder
    resolver.size()
    resolver.title()

    # 5. ID randomisation flag
    resolver.id_randomization()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "style_name, case",
    _ALL_CASES,
    ids=[f"{sn}:{c['id']}" for sn, c in _ALL_CASES],
)
def test_resolved_options(style_name: str, case: dict) -> None:
    definition = _load_style(style_name)
    resolver = Resolver(definition, case['options'])
    exercise_resolver(resolver, definition)
    assert resolver.resolved() == case['resolvedOptions']
