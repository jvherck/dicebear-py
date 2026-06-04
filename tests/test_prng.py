"""Parity tests for _prng.py against the language-neutral fixture files.

Fixtures live at:
  ../dicebear-js/tests/fixtures/parity/fnv1a.json
  ../dicebear-js/tests/fixtures/parity/mulberry32.json
  ../dicebear-js/tests/fixtures/parity/prng.json

Never modify the fixtures — they are the ground truth.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from dicebear._prng import (
    Mulberry32,
    Prng,
    _fnv1a,
    _fnv1a_hex,
)

# ---------------------------------------------------------------------------
# Fixture loading
# ---------------------------------------------------------------------------

FIXTURES = Path(__file__).parent.parent.parent / "dicebear-js" / "tests" / "fixtures" / "parity"


def _load(name: str) -> object:
    return json.loads((FIXTURES / name).read_text("utf-8"))


FNV1A_CASES = _load("fnv1a.json")
MULBERRY32_CASES = _load("mulberry32.json")
PRNG_DATA = _load("prng.json")


# ---------------------------------------------------------------------------
# FNV-1a
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("case", FNV1A_CASES, ids=[c["input"][:40] or "<empty>" for c in FNV1A_CASES])
def test_fnv1a_hash(case: dict) -> None:
    assert _fnv1a(case["input"]) == case["hash"]


@pytest.mark.parametrize("case", FNV1A_CASES, ids=[c["input"][:40] or "<empty>" for c in FNV1A_CASES])
def test_fnv1a_hex(case: dict) -> None:
    assert _fnv1a_hex(case["input"]) == case["hex"]


# ---------------------------------------------------------------------------
# Mulberry32
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("case", MULBERRY32_CASES, ids=[f"seed={c['seed']}" for c in MULBERRY32_CASES])
def test_mulberry32_sequence(case: dict) -> None:
    prng = Mulberry32(case["seed"])
    for step in case["sequence"]:
        assert prng.next_float() == pytest.approx(step["float"], rel=1e-15)
        assert prng.state() == step["state"]


# ---------------------------------------------------------------------------
# Prng.get_value
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "case",
    PRNG_DATA["getValue"],
    ids=[f"seed={c['seed']} key={c['key']}" for c in PRNG_DATA["getValue"]],
)
def test_prng_get_value(case: dict) -> None:
    result = Prng(case["seed"]).get_value(case["key"])
    assert result == pytest.approx(case["result"], rel=1e-15)


# ---------------------------------------------------------------------------
# Prng.pick
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "case",
    PRNG_DATA["pick"],
    ids=[f"seed={c['seed']} key={c['key']} items={c['items']}" for c in PRNG_DATA["pick"]],
)
def test_prng_pick(case: dict) -> None:
    result = Prng(case["seed"]).pick(case["key"], case["items"])
    assert result == case["result"]


# ---------------------------------------------------------------------------
# Prng.weighted_pick
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "case",
    PRNG_DATA["weightedPick"],
    ids=[f"seed={c['seed']} key={c['key']}" for c in PRNG_DATA["weightedPick"]],
)
def test_prng_weighted_pick(case: dict) -> None:
    result = Prng(case["seed"]).weighted_pick(case["key"], case["weights"])
    assert result == case["result"]


# ---------------------------------------------------------------------------
# Prng.bool
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "case",
    PRNG_DATA["bool"],
    ids=[f"seed={c['seed']} key={c['key']} likelihood={c['likelihood']}" for c in PRNG_DATA["bool"]],
)
def test_prng_bool(case: dict) -> None:
    result = Prng(case["seed"]).bool(case["key"], case["likelihood"])
    assert result == case["result"]


# ---------------------------------------------------------------------------
# Prng.float
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "case",
    PRNG_DATA["float"],
    ids=[f"seed={c['seed']} key={c['key']} range={c['range']}" for c in PRNG_DATA["float"]],
)
def test_prng_float(case: dict) -> None:
    result = Prng(case["seed"]).float(case["key"], case["range"])
    assert result == pytest.approx(case["result"], abs=1e-9)


# ---------------------------------------------------------------------------
# Prng.integer
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "case",
    PRNG_DATA["integer"],
    ids=[f"seed={c['seed']} key={c['key']} range={c['range']}" for c in PRNG_DATA["integer"]],
)
def test_prng_integer(case: dict) -> None:
    result = Prng(case["seed"]).integer(case["key"], case["range"])
    assert result == case["result"]


# ---------------------------------------------------------------------------
# Prng.shuffle
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "case",
    PRNG_DATA["shuffle"],
    ids=[f"seed={c['seed']} key={c['key']} items={c['items']}" for c in PRNG_DATA["shuffle"]],
)
def test_prng_shuffle(case: dict) -> None:
    result = Prng(case["seed"]).shuffle(case["key"], case["items"])
    assert result == case["result"]
