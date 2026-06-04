from __future__ import annotations

import math
import random
import re
import unicodedata
from typing import Any

from dicebear._prng import _fnv1a_hex
from dicebear._options_resolver import Resolver

# ---------------------------------------------------------------------------
# XML utilities
# ---------------------------------------------------------------------------


def _xml_escape(value: str) -> str:
    """Escape the five predefined XML entities. & must go first."""
    value = value.replace("&", "&amp;")
    value = value.replace("'", "&apos;")
    value = value.replace('"', "&quot;")
    value = value.replace("<", "&lt;")
    value = value.replace(">", "&gt;")
    return value


# ---------------------------------------------------------------------------
# Number formatting
# ---------------------------------------------------------------------------


def _number_format(value: float) -> str:
    """
    Round to at most 5 decimal places, strip trailing zeros, no exponent form.

    Matches JS Number.format: uses Math.round semantics (round half toward
    +infinity) via math.floor(x + 0.5).
    """
    if value != value:  # NaN check without importing math.isnan
        return "NaN"
    if value == float("inf"):
        return "Infinity"
    if value == float("-inf"):
        return "-Infinity"

    scaled_f = value * 100000
    f = math.floor(scaled_f)
    frac = scaled_f - f
    scaled = f + 1 if frac >= 0.5 else f
    sign = "-" if scaled < 0 else ""
    scaled = abs(scaled)
    integer_part = scaled // 100000
    fraction = str(scaled % 100000).zfill(5).rstrip("0")
    return f"{sign}{integer_part}" + (f".{fraction}" if fraction else "")


# ---------------------------------------------------------------------------
# Initials extraction
# ---------------------------------------------------------------------------

# Characters treated as apostrophes/quotes and stripped before word extraction.
# grave, acute, apostrophe, right-single-quote, modifier-apostrophe
_APOSTROPHE_CHARS = "`´’’ʼ"


def _is_letter(ch: str) -> bool:
    return unicodedata.category(ch)[0] == "L"


def _is_mark(ch: str) -> bool:
    return unicodedata.category(ch)[0] == "M"


def _find_letter_words(text: str) -> list[str]:
    """Extract maximal runs of \\p{L}[\\p{L}\\p{M}]* (Unicode letter words)."""
    words: list[str] = []
    i, n = 0, len(text)
    while i < n:
        if _is_letter(text[i]):
            j = i + 1
            while j < n and (_is_letter(text[j]) or _is_mark(text[j])):
                j += 1
            words.append(text[i:j])
            i = j
        else:
            i += 1
    return words


def _take_grapheme_clusters(word: str, count: int) -> str:
    """Take up to `count` grapheme clusters (\\p{L}\\p{M}*) from `word`."""
    parts: list[str] = []
    i, taken = 0, 0
    while i < len(word) and taken < count:
        if _is_letter(word[i]):
            j = i + 1
            while j < len(word) and _is_mark(word[j]):
                j += 1
            parts.append(word[i:j])
            i = j
            taken += 1
        else:
            i += 1
    return "".join(parts)


def _initials_from_seed(seed: str, _discard_at: bool = True) -> str:
    """
    Derive one or two uppercase initials from a seed string.

    Strips email suffixes (@...) by default, removes apostrophe-like chars,
    then extracts Unicode letter words. Mirrors JS Initials.fromSeed().
    """
    text = seed
    if _discard_at:
        at_idx = seed.find("@")
        if at_idx >= 0:
            text = seed[:at_idx]

    for ch in _APOSTROPHE_CHARS:
        text = text.replace(ch, "")

    words = _find_letter_words(text)

    if not words:
        return _initials_from_seed(seed, False) if _discard_at else ""

    if len(words) == 1:
        return _take_grapheme_clusters(words[0], 2).upper()

    first = _take_grapheme_clusters(words[0], 1)
    last = _take_grapheme_clusters(words[-1], 1)
    if not first or not last:
        return ""
    return (first + last).upper()


# ---------------------------------------------------------------------------
# License / metadata
# ---------------------------------------------------------------------------


def _license_text(meta: dict) -> str:
    """Single-line attribution string, or '' when no meta fields are set."""
    source = meta.get("source") or {}
    creator = meta.get("creator") or {}
    license_ = meta.get("license") or {}

    source_name = source.get("name")
    source_url = source.get("url")
    creator_name = creator.get("name")
    license_name = license_.get("name")
    license_url = license_.get("url")

    if not source_name and not creator_name and not license_name:
        return ""

    title = f"“{source_name}”" if source_name else "Design"
    if source_url:
        title += f" ({source_url})"

    inner = creator_name if creator_name is not None else "Unknown"
    creator_str = f"“{inner}”"
    result = ""

    if license_name != "MIT" and creator_name != "DiceBear" and source_name:
        result += "Remix of "

    result += f"{title} by {creator_str}"

    if license_name:
        result += f", licensed under “{license_name}”"
        if license_url:
            result += f" ({license_url})"

    return result


def _license_xml(meta: dict) -> str:
    """Embedded RDF/Dublin Core metadata block, or '' when no fields are set."""
    source = meta.get("source") or {}
    creator = meta.get("creator") or {}
    license_ = meta.get("license") or {}

    title = source.get("name")
    creator_name = creator.get("name")
    source_url = source.get("url")
    license_url = license_.get("url")
    rights = _license_text(meta)

    if not title and not creator_name and not source_url and not license_url and not rights:
        return ""

    fields: list[str] = []
    if title:
        fields.append(f"<dc:title>{_xml_escape(title)}</dc:title>")
    if creator_name:
        fields.append(f"<dc:creator>{_xml_escape(creator_name)}</dc:creator>")
    if source_url:
        fields.append(f'<dc:source xsi:type="dcterms:URI">{_xml_escape(source_url)}</dc:source>')
    if license_url:
        fields.append(f'<dcterms:license xsi:type="dcterms:URI">{_xml_escape(license_url)}</dcterms:license>')
    if rights:
        fields.append(f"<dc:rights>{_xml_escape(rights)}</dc:rights>")

    return (
        "<metadata"
        ' xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"'
        ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
        ' xmlns:dc="http://purl.org/dc/elements/1.1/"'
        ' xmlns:dcterms="http://purl.org/dc/terms/">'
        "<rdf:RDF><rdf:Description>" + "".join(fields) + "</rdf:Description></rdf:RDF>"
        "</metadata>"
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def render(definition: dict, user_options: dict) -> str:
    """Render a DiceBear avatar SVG from a style definition and user options."""
    resolver = Resolver(definition, user_options)
    return _Renderer(definition, resolver).render()


# ---------------------------------------------------------------------------
# Internal renderer
# ---------------------------------------------------------------------------


class _Renderer:
    """
    Single-use SVG renderer.

    Accumulates <defs> entries across the render and caches the seed hash
    and initials. Construct a new instance for each avatar.
    """

    def __init__(self, definition: dict, resolver: Resolver) -> None:
        self._definition = definition
        self._resolver = resolver
        self._defs: dict[str, str] = {}
        self._seed_hash: str | None = None
        self._cached_initials: str | None = None

    def render(self) -> str:
        canvas = self._definition.get("canvas", {})
        w: float = canvas.get("width", 0)
        h: float = canvas.get("height", 0)

        background = self._render_background(w, h)
        body = self._render_elements(canvas.get("elements", []))

        # Transform order: scale and flip around centre, then rotate,
        # translate, and finally clip with border-radius (outermost).
        body = self._apply_scale(body, w, h)
        body = self._apply_flip(body, w, h)
        body = self._apply_rotate(body, w, h)
        body = self._apply_translate(body, w, h)
        body = self._apply_border_radius(background + body, w, h)

        metadata = _license_xml(self._definition.get("meta") or {})
        defs_html = "<defs>" + "".join(self._defs.values()) + "</defs>" if self._defs else ""

        size = self._resolver.size()
        title = self._resolver.title()
        escaped_title = _xml_escape(title) if title is not None else None

        attrs: list[str] = [
            'xmlns="http://www.w3.org/2000/svg"',
            f'viewBox="0 0 {_number_format(w)} {_number_format(h)}"',
        ]

        root_attrs = self._render_attributes(self._definition.get("attributes") or {})
        if root_attrs:
            attrs.append(root_attrs.lstrip())

        if escaped_title is not None:
            attrs += ['role="img"', f'aria-label="{escaped_title}"']
        else:
            attrs.append('aria-hidden="true"')

        if size is not None:
            s = _number_format(size)
            attrs += [f'width="{s}"', f'height="{s}"']

        title_el = f"<title>{escaped_title}</title>" if escaped_title is not None else ""

        svg = f'<svg {" ".join(attrs)}>{metadata}{defs_html}{title_el}{body}</svg>'

        if self._resolver.id_randomization():
            svg = self._randomize_ids(svg)

        return svg

    # -----------------------------------------------------------------------
    # Background
    # -----------------------------------------------------------------------

    def _render_background(self, w: float, h: float) -> str:
        colors = self._resolver.color("background")
        if not colors:
            return ""
        fill = self._resolve_color_reference("background")
        return f'<rect width="{_number_format(w)}" height="{_number_format(h)}"' f' fill="{_xml_escape(fill)}"/>'

    # -----------------------------------------------------------------------
    # Global transforms
    # -----------------------------------------------------------------------

    def _apply_scale(self, body: str, w: float, h: float) -> str:
        scale = self._resolver.scale()
        if scale == 1:
            return body
        cx, cy = w / 2, h / 2
        return (
            f'<g transform="translate({_number_format(cx)}, {_number_format(cy)})'
            f" scale({_number_format(scale)})"
            f' translate({_number_format(-cx)}, {_number_format(-cy)})">'
            f"{body}</g>"
        )

    def _apply_flip(self, body: str, w: float, h: float) -> str:
        flip = self._resolver.flip()
        if flip == "none":
            return body
        if flip == "horizontal":
            transform = f"translate({_number_format(w)}, 0) scale(-1, 1)"
        elif flip == "vertical":
            transform = f"translate(0, {_number_format(h)}) scale(1, -1)"
        else:  # 'both'
            transform = f"translate({_number_format(w)}, {_number_format(h)}) scale(-1, -1)"
        return f'<g transform="{transform}">{body}</g>'

    def _apply_rotate(self, body: str, w: float, h: float) -> str:
        rotate = self._resolver.rotate()
        if rotate == 0:
            return body
        cx, cy = w / 2, h / 2
        return (
            f'<g transform="rotate({_number_format(rotate)},'
            f' {_number_format(cx)}, {_number_format(cy)})">'
            f"{body}</g>"
        )

    def _apply_translate(self, body: str, w: float, h: float) -> str:
        tx = self._resolver.translate_x()
        ty = self._resolver.translate_y()
        if tx == 0 and ty == 0:
            return body
        x = _number_format((tx / 100) * w)
        y = _number_format((ty / 100) * h)
        return f'<g transform="translate({x}, {y})">{body}</g>'

    def _apply_border_radius(self, body: str, w: float, h: float) -> str:
        radius = self._resolver.border_radius()
        clip_id = f"clip-{self._hash_seed()}"
        rx = _number_format((radius / 100) * w)
        ry = _number_format((radius / 100) * h)
        self._defs[clip_id] = (
            f'<clipPath id="{clip_id}">'
            f'<rect width="{_number_format(w)}" height="{_number_format(h)}"'
            f' rx="{rx}" ry="{ry}"/>'
            f"</clipPath>"
        )
        return f'<g clip-path="url(#{clip_id})">{body}</g>'

    # -----------------------------------------------------------------------
    # Element tree
    # -----------------------------------------------------------------------

    def _render_elements(self, elements: list[dict]) -> str:
        return "".join(self._render_element(e) for e in elements)

    def _render_element(self, element: dict) -> str:
        etype = element.get("type")
        if etype == "element":
            return self._render_svg_element(element)
        if etype == "text":
            return self._render_text_element(element)
        if etype == "component":
            return self._render_component_element(element)
        return ""

    def _render_svg_element(self, element: dict) -> str:
        name = element.get("name")
        if not name:
            return ""

        # Special case: collect children into the shared defs map.
        if name == "defs":
            for child in element.get("children") or []:
                rendered = self._render_element(child)
                if rendered:
                    child_id = (child.get("attributes") or {}).get("id")
                    key = child_id if isinstance(child_id, str) else f"_{len(self._defs)}"
                    self._defs[key] = rendered
            return ""

        attrs = self._render_attributes(element.get("attributes") or {})
        children = self._render_elements(element.get("children") or [])

        if children:
            return f"<{name}{attrs}>{children}</{name}>"
        return f"<{name}{attrs}/>"

    def _render_text_element(self, element: dict) -> str:
        value = element.get("value")
        if value is None:
            return ""
        return _xml_escape(self._resolve_value(value))

    def _render_component_element(self, element: dict) -> str:
        comp_name = element.get("name")
        if not isinstance(comp_name, str):
            return ""

        variant_name = self._resolver.variant(comp_name)
        if not variant_name:
            return ""

        base = self._base_component(comp_name)
        if base is None:
            return ""

        variant_data = base.get("variants", {}).get(variant_name)
        if variant_data is None:
            return ""

        source = self._source_name(comp_name)
        def_id = f"{source}-{variant_name}-{self._hash_seed()}"

        if def_id not in self._defs:
            body = self._render_elements(variant_data.get("elements", []))
            self._defs[def_id] = f'<g id="{def_id}">{body}</g>'

        transforms = self._build_transforms(comp_name, base)
        user_attrs: dict = dict(element.get("attributes") or {})
        merged = user_attrs

        if transforms:
            user_tf = user_attrs.get("transform", "")
            all_parts = ([user_tf] if isinstance(user_tf, str) and user_tf else []) + transforms
            merged = {**user_attrs, "transform": " ".join(all_parts)}

        attrs = self._render_attributes(merged)
        return f'<use{attrs} href="#{def_id}"/>'

    # -----------------------------------------------------------------------
    # Per-component transforms
    # -----------------------------------------------------------------------

    def _build_transforms(self, name: str, base: dict) -> list[str]:
        tf = self._resolver.component_transform(name)
        rotate = tf["rotate"]
        tx = tf["translate_x"]
        ty = tf["translate_y"]
        scale = tf["scale"]

        if tx == 0 and ty == 0 and rotate == 0 and scale == 1:
            return []

        w: float = base.get("width", 0)
        h: float = base.get("height", 0)
        cx, cy = w / 2, h / 2
        parts: list[str] = []

        if tx != 0 or ty != 0:
            x = _number_format((tx / 100) * w)
            y = _number_format((ty / 100) * h)
            parts.append(f"translate({x}, {y})")

        if rotate != 0:
            parts.append(f"rotate({_number_format(rotate)}," f" {_number_format(cx)}, {_number_format(cy)})")

        if scale != 1:
            cx_s = _number_format(cx)
            cy_s = _number_format(cy)
            parts.append(
                f"translate({cx_s}, {cy_s})"
                f" scale({_number_format(scale)})"
                f" translate({_number_format(-cx)}, {_number_format(-cy)})"
            )

        return parts

    # -----------------------------------------------------------------------
    # Attributes
    # -----------------------------------------------------------------------

    def _render_attributes(self, attributes: dict) -> str:
        parts: list[str] = []
        for key, value in attributes.items():
            if value is None:
                continue
            resolved = self._resolve_attribute_value(value)
            parts.append(f'{key}="{_xml_escape(resolved)}"')
        if not parts:
            return ""
        return " " + " ".join(parts)

    def _resolve_attribute_value(self, value: Any) -> str:
        if isinstance(value, str):
            return value
        if isinstance(value, dict):
            vtype = value.get("type")
            if vtype == "color":
                return self._resolve_color_reference(value["name"])
            if vtype == "variable":
                return self._resolve_variable(value["name"])
        return str(value)

    def _resolve_value(self, value: Any) -> str:
        if isinstance(value, str):
            return value
        if isinstance(value, dict) and value.get("type") == "variable":
            return self._resolve_variable(value["name"])
        return ""

    def _resolve_variable(self, name: str) -> str:
        if name == "initial":
            s = self._initials()
            return s[0] if s else ""
        if name == "initials":
            return self._initials()
        if name == "fontWeight":
            return _number_format(self._resolver.font_weight())
        if name == "fontFamily":
            return self._resolver.font_family()
        return ""

    # -----------------------------------------------------------------------
    # Colour references
    # -----------------------------------------------------------------------

    def _resolve_color_reference(self, name: str) -> str:
        colors = self._resolver.color(name)
        fill = self._resolver.color_fill(name)
        if fill == "solid" or len(colors) <= 1:
            return colors[0] if colors else "none"
        return self._build_gradient_def(name, colors, fill)

    def _build_gradient_def(self, name: str, colors: list[str], fill: str) -> str:
        rotation = self._resolver.color_angle(name)
        grad_id = f"{name}-color-{self._hash_seed()}"
        tag = "linearGradient" if fill == "linear" else "radialGradient"

        rotate_attr = ""
        if rotation != 0:
            rotate_attr = f' gradientTransform="rotate({_number_format(rotation)}, 0.5, 0.5)"'

        n = len(colors) - 1
        stops: list[str] = []
        for i, color in enumerate(colors):
            offset = _number_format((i / n) * 100) if n > 0 else "0"
            stops.append(f'<stop offset="{offset}%" stop-color="{_xml_escape(color)}"/>')

        self._defs[grad_id] = f'<{tag} id="{grad_id}"{rotate_attr}>{"".join(stops)}</{tag}>'
        return f"url(#{grad_id})"

    # -----------------------------------------------------------------------
    # ID randomisation
    # -----------------------------------------------------------------------

    def _randomize_ids(self, svg: str) -> str:
        suffix = format(random.randint(0, 0xFFFFFF), "06x")
        ids = {m.group(1) for m in re.finditer(r'\bid="([^"]+)"', svg)}
        if not ids:
            return svg
        escaped = [re.escape(id_) for id_ in ids]
        pattern = re.compile(r'(id="|url\(#|href="#)(' + "|".join(escaped) + r')("|\))')
        return pattern.sub(
            lambda m: m.group(1) + m.group(2) + "-" + suffix + m.group(3),
            svg,
        )

    # -----------------------------------------------------------------------
    # Cached helpers
    # -----------------------------------------------------------------------

    def _hash_seed(self) -> str:
        if self._seed_hash is None:
            self._seed_hash = _fnv1a_hex(self._resolver.seed())
        return self._seed_hash

    def _initials(self) -> str:
        if self._cached_initials is None:
            self._cached_initials = _initials_from_seed(self._resolver.seed())
        return self._cached_initials

    # -----------------------------------------------------------------------
    # Style-definition helpers
    # -----------------------------------------------------------------------

    def _source_name(self, name: str) -> str:
        comp = self._definition.get("components", {}).get(name, {})
        return comp.get("extends", name)

    def _base_component(self, name: str) -> dict | None:
        components = self._definition.get("components", {})
        comp = components.get(name)
        if comp is None:
            return None
        target = comp.get("extends")
        if target is not None:
            return components.get(target)
        return comp
