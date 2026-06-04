"""
Public API integration tests: Avatar, Options, Color, Format.
"""
from __future__ import annotations

import os

import pytest

from dicebear import Avatar, Color, Format, Options
from dicebear.styles import Avataaars, Thumbs


# ---------------------------------------------------------------------------
# Color
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("value,expected", [
    ("ff0000", "#ff0000"),
    ("#ff0000", "#ff0000"),
    ("FF0000", "#ff0000"),
    ("#AABBCC", "#aabbcc"),
    ("00ddd0", "#00ddd0"),
])
def test_color_normalizes(value: str, expected: str) -> None:
    assert str(Color(value)) == expected


@pytest.mark.parametrize("value", [
    "ff00",       # too short
    "ff000000",   # 8 hex digits without #
    "#ff000000",  # 8 hex digits with #
    "gggggg",     # non-hex characters
    "",           # empty string
    "red",        # named color
])
def test_color_invalid_raises(value: str) -> None:
    with pytest.raises(ValueError):
        Color(value)


def test_color_equality() -> None:
    assert Color("ff0000") == Color("#ff0000")
    assert Color("FF0000") == Color("ff0000")


def test_color_inequality() -> None:
    assert Color("ff0000") != Color("00ff00")


def test_color_hash_consistent_with_eq() -> None:
    a = Color("aabbcc")
    b = Color("#AABBCC")
    assert a == b
    assert hash(a) == hash(b)


def test_color_usable_as_dict_key() -> None:
    d = {Color("ff0000"): "red"}
    assert d[Color("#ff0000")] == "red"


# ---------------------------------------------------------------------------
# Format
# ---------------------------------------------------------------------------

def test_format_members_exist() -> None:
    assert Format.SVG.value == "svg"
    assert Format.PNG.value == "png"
    assert Format.JPG.value == "jpg"
    assert Format.JPEG.value == "jpeg"
    assert Format.WEBP.value == "webp"


# ---------------------------------------------------------------------------
# Options
# ---------------------------------------------------------------------------

def test_options_all_defaults_none() -> None:
    o = Options()
    assert o.flip is None
    assert o.rotate is None
    assert o.scale is None
    assert o.radius is None
    assert o.size is None
    assert o.translateX is None
    assert o.translateY is None
    assert o.backgroundColor is None
    assert o.backgroundType is None
    assert o.backgroundRotation is None


def test_options_accepts_color_object() -> None:
    o = Options(backgroundColor=Color("ff0000"))
    assert isinstance(o.backgroundColor, Color)


def test_options_accepts_str_color() -> None:
    o = Options(backgroundColor="#ff0000")
    assert o.backgroundColor == "#ff0000"


def test_options_explicit_fields() -> None:
    o = Options(flip=True, rotate=90, scale=80, radius=50, size=200)
    assert o.flip is True
    assert o.rotate == 90
    assert o.scale == 80
    assert o.radius == 50
    assert o.size == 200


# ---------------------------------------------------------------------------
# Avatar — construction and .svg
# ---------------------------------------------------------------------------

def test_avatar_init_does_not_render() -> None:
    av = Avatar(Thumbs(), "test-seed")
    assert av._svg is None


def test_avatar_svg_returns_string() -> None:
    av = Avatar(Thumbs(), "test-seed")
    assert isinstance(av.svg, str)


def test_avatar_svg_starts_with_svg_tag() -> None:
    av = Avatar(Thumbs(), "test-seed")
    assert av.svg.lstrip().startswith("<svg")


def test_avatar_svg_ends_with_svg_close() -> None:
    av = Avatar(Thumbs(), "test-seed")
    assert av.svg.rstrip().endswith("</svg>")


def test_avatar_svg_cached() -> None:
    av = Avatar(Thumbs(), "test-seed")
    first = av.svg
    second = av.svg
    assert first is second


def test_avatar_svg_deterministic() -> None:
    assert Avatar(Thumbs(), "parity-1").svg == Avatar(Thumbs(), "parity-1").svg


def test_avatar_different_seeds_differ() -> None:
    assert Avatar(Thumbs(), "seed-alpha").svg != Avatar(Thumbs(), "seed-beta").svg


def test_avatar_different_styles_differ() -> None:
    assert Avatar(Thumbs(), "same-seed").svg != Avatar(Avataaars(), "same-seed").svg


# ---------------------------------------------------------------------------
# Avatar.save
# ---------------------------------------------------------------------------

def test_save_creates_file(tmp_path) -> None:
    path = str(tmp_path / "avatar.svg")
    Avatar(Thumbs(), "save-test").save(path)
    assert os.path.exists(path)


def test_save_content_matches_svg_property(tmp_path) -> None:
    av = Avatar(Thumbs(), "save-test")
    path = str(tmp_path / "avatar.svg")
    av.save(path)
    assert open(path, encoding="utf-8").read() == av.svg


def test_save_raises_file_exists_error(tmp_path) -> None:
    path = str(tmp_path / "avatar.svg")
    av = Avatar(Thumbs(), "save-test")
    av.save(path)
    with pytest.raises(FileExistsError):
        av.save(path)


def test_save_overwrite_replaces_file(tmp_path) -> None:
    path = str(tmp_path / "avatar.svg")
    av1 = Avatar(Thumbs(), "seed-one")
    av2 = Avatar(Thumbs(), "seed-two")
    av1.save(path)
    av2.save(path, overwrite=True)
    assert open(path, encoding="utf-8").read() == av2.svg


# ---------------------------------------------------------------------------
# Avatar.bulk_create
# ---------------------------------------------------------------------------

def test_bulk_create_from_class_count() -> None:
    avatars = Avatar.bulk_create(Thumbs, amount=4)
    assert len(avatars) == 4


def test_bulk_create_from_class_types() -> None:
    avatars = Avatar.bulk_create(Thumbs, amount=3)
    assert all(isinstance(a, Avatar) for a in avatars)


def test_bulk_create_from_instance() -> None:
    avatars = Avatar.bulk_create(Thumbs(), amount=4)
    assert len(avatars) == 4
    assert all(isinstance(a, Avatar) for a in avatars)


def test_bulk_create_produces_unique_svgs() -> None:
    avatars = Avatar.bulk_create(Thumbs, amount=5)
    assert len({a.svg for a in avatars}) > 1


def test_bulk_create_passes_options_to_all() -> None:
    opts = Options(backgroundColor=Color("ff0000"))
    avatars = Avatar.bulk_create(Thumbs, amount=3, options=opts)
    assert all("#ff0000" in a.svg for a in avatars)


def test_bulk_create_instance_carries_style_options() -> None:
    style = Avataaars(eyes=Avataaars.Eyes.WINK)
    avatars = Avatar.bulk_create(style, amount=2)
    for a in avatars:
        assert a.svg.lstrip().startswith("<svg")


# ---------------------------------------------------------------------------
# Options → renderer integration
# ---------------------------------------------------------------------------

def test_background_color_from_color_object_appears_in_svg() -> None:
    av = Avatar(Thumbs(), "color-test", options=Options(backgroundColor=Color("ff0000")))
    assert "#ff0000" in av.svg


def test_background_color_from_str_appears_in_svg() -> None:
    av = Avatar(Thumbs(), "color-test", options=Options(backgroundColor="#00ff00"))
    assert "#00ff00" in av.svg


def test_flip_adds_negative_scale_transform() -> None:
    av = Avatar(Thumbs(), "flip-test", options=Options(flip=True))
    assert "scale(-1" in av.svg


def test_radius_adds_rounded_clip_path() -> None:
    av = Avatar(Thumbs(), "radius-test", options=Options(radius=50))
    assert 'rx=' in av.svg


def test_no_radius_has_zero_rx() -> None:
    av = Avatar(Thumbs(), "radius-test")
    assert 'rx="0"' in av.svg


def test_style_specific_options_affect_output() -> None:
    seed = "style-options-test"
    wink = Avatar(Avataaars(eyes=Avataaars.Eyes.WINK), seed).svg
    default_eyes = Avatar(Avataaars(eyes=Avataaars.Eyes.DEFAULT), seed).svg
    assert wink != default_eyes
