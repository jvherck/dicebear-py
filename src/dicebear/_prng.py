from __future__ import annotations

import math
from typing import TypedDict


# ---------------------------------------------------------------------------
# Range type (mirrors JS StyleDefinition.Range)
# ---------------------------------------------------------------------------

class _RangeRequired(TypedDict):
    min: float
    max: float


class Range(_RangeRequired, total=False):
    step: float


# ---------------------------------------------------------------------------
# Internal bit-manipulation helpers
# ---------------------------------------------------------------------------

def _to_int32(n: int) -> int:
    """Reinterpret the lower 32 bits of n as a signed 32-bit integer (JS `| 0`)."""
    n &= 0xFFFFFFFF
    return n - 0x100000000 if n >= 0x80000000 else n


def _imul32(a: int, b: int) -> int:
    """Lower-32-bit signed multiply, matching JS Math.imul."""
    return _to_int32((a & 0xFFFFFFFF) * (b & 0xFFFFFFFF) & 0xFFFFFFFF)


# ---------------------------------------------------------------------------
# FNV-1a 32-bit hash
# ---------------------------------------------------------------------------

def _fnv1a(text: str) -> int:
    """
    FNV-1a 32-bit hash over UTF-16 code units.

    Iterates utf-16-le code units (2 bytes each) so surrogate pairs for
    supplementary characters are hashed separately — identical to JS charCodeAt().
    """
    encoded = text.encode('utf-16-le')
    hash_ = 0x811C9DC5
    for i in range(0, len(encoded), 2):
        code_unit = encoded[i] | (encoded[i + 1] << 8)
        hash_ ^= code_unit
        hash_ = (hash_ * 0x01000193) & 0xFFFFFFFF
    return hash_


def _fnv1a_hex(text: str) -> str:
    """FNV-1a hash as an 8-character lowercase hex string."""
    return format(_fnv1a(text), '08x')


# ---------------------------------------------------------------------------
# Mulberry32 PRNG
# ---------------------------------------------------------------------------

class Mulberry32:
    """
    Stateful Mulberry32 PRNG, matching the C reference by Tommy Ettinger.

    The internal state is a signed 32-bit integer after the first advance,
    mirroring JS `| 0` semantics.
    """

    def __init__(self, seed: int) -> None:
        # Store as-is; _to_int32 is applied on each advance, not at construction.
        self._state: int = seed

    def next(self) -> int:
        """Advance the state and return the next unsigned 32-bit value."""
        self._state = _to_int32(self._state + 0x6D2B79F5)
        z = self._state

        # z ^ (z >>> 15): unsigned right-shift via masking
        z_u = z & 0xFFFFFFFF
        t = _imul32(z_u ^ (z_u >> 15), z | 1)

        # t ^= t + Math.imul(t ^ (t >>> 7), t | 61)
        t_u = t & 0xFFFFFFFF
        inner = _imul32(t_u ^ (t_u >> 7), t | 61)
        t = _to_int32(t ^ (t + inner))

        # (t ^ (t >>> 14)) >>> 0: final unsigned result
        t_u = t & 0xFFFFFFFF
        return t_u ^ (t_u >> 14)

    def next_float(self) -> float:
        """Advance the state and return the next value in [0, 1)."""
        return self.next() / 4294967296  # 2 ** 32

    def state(self) -> int:
        """Return the current internal state (signed 32-bit after first advance)."""
        return self._state


# ---------------------------------------------------------------------------
# Key-based PRNG
# ---------------------------------------------------------------------------

class Prng:
    """
    Key-based deterministic PRNG.

    Each method takes a key; combined with the seed it produces a
    deterministic value. Call order does not affect results.
    """

    def __init__(self, seed: str) -> None:
        self._seed = seed

    def get_value(self, key: str) -> float:
        """Return a float in [0, 1) derived from seed:key."""
        return Mulberry32(_fnv1a(self._seed + ':' + key)).next_float()

    def pick(self, key: str, items: list) -> object | None:
        """
        Pick one item deterministically.

        Deduplicates by str() representation (first occurrence wins), sorts
        by string order, then indexes with floor(getValue * len).
        Returns None for an empty list.
        """
        if len(items) == 0:
            return None
        if len(items) == 1:
            return items[0]

        unique = _unique_by_repr(items)
        if len(unique) == 1:
            return unique[0]

        sorted_items = sorted(unique, key=str)
        index = math.floor(self.get_value(key) * len(sorted_items))
        return sorted_items[index]

    def weighted_pick(self, key: str, weights: dict[str, float]) -> str | None:
        """
        Pick a key proportional to its weight.

        Falls back to unweighted pick when all weights are zero.
        Returns None for an empty dict.
        """
        keys = list(weights.keys())
        if len(keys) == 0:
            return None
        if len(keys) == 1:
            return keys[0]

        sorted_keys = sorted(keys)
        total_weight = sum(weights[k] for k in sorted_keys)

        if total_weight == 0:
            return self.pick(key, sorted_keys)

        threshold = self.get_value(key) * total_weight
        cumulative = 0.0
        for k in sorted_keys:
            cumulative += weights[k]
            if threshold < cumulative:
                return k

        return sorted_keys[-1]

    def bool(self, key: str, likelihood: float = 50) -> bool:
        """Return True with the given probability (0–100)."""
        return self.get_value(key) * 100 < likelihood

    def float(self, key: str, range_: Range) -> float:
        """
        Return a deterministic float in range_, rounded to 4 decimal places.

        With step > 0, draws uniformly from the discrete set of bucket values.
        Mirrors JS Math.round (round half toward +infinity) via floor(x + 0.5).
        """
        min_ = min(range_['min'], range_['max'])
        max_ = max(range_['min'], range_['max'])
        step = range_.get('step') or 0

        if step > 0:
            buckets = math.floor((max_ - min_) / step) + 1
            i = math.floor(self.get_value(key) * buckets)
            value = min_ + i * step
        else:
            value = min_ + self.get_value(key) * (max_ - min_)

        return math.floor(value * 10000 + 0.5) / 10000

    def integer(self, key: str, range_: Range) -> int:
        """
        Return a deterministic integer in range_.

        The step field (if present) is ignored — integers always step by 1.
        """
        min_ = int(min(range_['min'], range_['max']))
        max_ = int(max(range_['min'], range_['max']))
        return math.floor(self.get_value(key) * (max_ - min_ + 1)) + min_

    def shuffle(self, key: str, items: list) -> list:
        """
        Fisher-Yates shuffle with a Mulberry32 seeded from seed:key.

        Deduplicates and sorts before shuffling so input order and
        duplicates cannot affect the result.
        """
        if len(items) <= 1:
            return list(items)

        result = sorted(_unique_by_repr(items), key=str)
        prng = Mulberry32(_fnv1a(self._seed + ':' + key))

        for i in range(len(result) - 1, 0, -1):
            j = math.floor(prng.next_float() * (i + 1))
            result[i], result[j] = result[j], result[i]

        return result


# ---------------------------------------------------------------------------
# Internal utilities
# ---------------------------------------------------------------------------

def _unique_by_repr(items: list) -> list:
    """Deduplicate by str() representation, keeping the first occurrence."""
    seen: set[str] = set()
    result = []
    for item in items:
        key = str(item)
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result
