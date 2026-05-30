# MIT License
#
# Copyright (c) 2026 jvherck (on GitHub)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from os import environ
from random import choice, choices
from typing import Union, List

from requests import post, get

from .errors import *
from .errors import _logger
from .metadata import Metadata

__all__ = (
    "DColor",
    "DStyle",
    "DFormat",
    "DOptions",
    "options",
    "all_options",
    "default_options",
    "styles",
)
__filename__ = "models.py"


class _FindPil:
    """Not important for you, just makes things easier for me on the back-end ;)"""

    found: bool = True


ASCII_LOWERCASE = "abcdef"
DIGITS = "0123456789"
TIMEOUT = 30
API_VERSION = "10.x"
X = "https://api.dicebear.com/" + API_VERSION
Y = X + "/{}/schema.json"

options = all_options = [
    "flip",
    "rotate",
    "scale",
    "radius",
    "size",
    "backgroundColor",
    "backgroundType",
    "backgroundRotation",
    "translateX",
    "translateY",
    "randomizeIds",
]

styles = list(Metadata.keys())


# styles_depricated = ["female", "gridy", "human", "jdenticon", "male"]


class DColor:
    """
    Base class for DAvatar's colors.
    """

    def __init__(self, html_code: Union[str, List[str]] = "transparent"):
        """
        Colors used in this package. This uses HTML/hex color codes!

        :param html_code: :py:class:`str` :: the html color code to use as color. This can be a list of strings if `backgroundType` has been set to "gradientLinear". (default: transparent)
        :type html_code: str
        :raise dicebear.errors.IncorrectColor: if the given html_code is an invalid hex color
        """
        code_list: list = []
        hex_list: list = []
        if isinstance(html_code, str):
            code_list = html_code.replace(" ", "").split(",")
        elif isinstance(html_code, list) and all(isinstance(x, str) for x in html_code):
            code_list = html_code
        for code in code_list:
            code = code.replace("#", "")
            if (len(code) != 6 or any(x not in (ASCII_LOWERCASE + DIGITS) for x in code)) and code != "transparent":
                raise IncorrectColor(str(code))
            hex_list.append(code)
        self._html_code: str = ",".join(hex_list)

    @property
    def html_code(self) -> str:
        """Returns the validated and formatted html/hex color codes."""
        return str(self._html_code)

    hex_code = html_code

    def __str__(self):
        return str(self.html_code)

    def __repr__(self):
        return str(self.html_code)

    def __hash__(self):
        return hash(self.html_code)

    def __eq__(self, other):
        if isinstance(other, DColor):
            return self.html_code == other.html_code
        return self.html_code == other

    def __ne__(self, other):
        if isinstance(other, DColor):
            return self.html_code != other.html_code
        return self.html_code != other

    @staticmethod
    def random() -> "DColor":
        """
        Get a random html code.

        :return: :py:class:`dicebear.models.DColor`
        """
        return DColor("".join(choices(ASCII_LOWERCASE + DIGITS, k=6)))


class DStyle:
    """
    All possible styles for the avatars. Visit https://dicebear.com/styles to see what they look like.\n
    - Note: Only works with attributes!
    """

    list = all_styles = styles
    adventurer = styles[0]
    adventurer_neutral = styles[1]
    avataaars = styles[2]
    avataaars_neutral = styles[3]
    big_ears = styles[4]
    big_ears_neutral = styles[5]
    big_smile = styles[6]
    bottts = styles[7]
    bottts_neutral = styles[8]
    croodles = styles[9]
    croodles_neutral = styles[10]
    dylan = styles[11]
    fun_emoji = styles[12]
    glass = styles[13]
    icons = styles[14]
    identicon = styles[15]
    initials = styles[16]
    lorelei = styles[17]
    lorelei_neutral = styles[18]
    micah = styles[19]
    miniavs = styles[20]
    notionists = styles[21]
    notionists_neutral = styles[22]
    open_peeps = styles[23]
    personas = styles[24]
    pixel_art = styles[25]
    pixel_art_neutral = styles[26]
    rings = styles[27]
    shapes = styles[28]
    thumbs = styles[29]
    toon_head = styles[30]

    def __init__(self):
        """Only use `.attribute` to use a style."""
        raise NotImplementedError("DStyle should not be initialized.")

    @staticmethod
    def get_schema(style: str) -> dict:
        """
        Returns a dict with the JSON schema (all properties) of the given avatar style.

        :param style: :py:class:`str` :: the avatar style to get the JSON schema of
        :type style: str
        :return: :py:class:`dict`
        """
        if style not in styles:
            raise ValueError(f'"{style}" is not a valid avatar style.')
        try:
            return get(Y.format(style), timeout=TIMEOUT).json()
        except Exception as e:
            raise HTTPError({"exception": str(type(e)), "error": str(e)})

    @staticmethod
    def random() -> str:
        """
        Get a random style.

        :return: a random style
        """
        return choice(styles)

    @staticmethod
    def from_str(style_str: str) -> str:
        """
        Get an avatar style from a string.

        :param style_str: :py:class:`str` :: the string to convert to a DStyle
        :type style_str: str
        """
        try:
            return getattr(DStyle, style_str.lower().replace("-", "_"))
        except AttributeError:
            raise ValueError(f"Invalid style: {style_str}")


class DFormat:
    """
    All possible image formats for saving or converting avatars.
    - Note: Only works with attributes!
    """

    list = all_formats = ["svg", "webp", "avif", "png", "jpg", "jpeg", "json"]
    svg = "svg"
    webp = "webp"
    avif = "avif"
    png = "png"
    jpg = "jpg"
    jpeg = "jpeg"
    json = "json"

    def __init__(self):
        """Only use `.attribute` to use a format."""
        raise NotImplementedError("DFormat should not be initialized.")

    @staticmethod
    def from_str(format_str: str) -> str:
        """
        Get an avatar format from a string

        :param format_str: :py:class:`str` :: the string to convert to a DFormat
        :type format_str: str
        """
        return getattr(DFormat, format_str.lower().replace("dformat.", ""))


default_options: dict = {
    "flip": False,
    "rotate": 0,
    "scale": 100,
    "radius": 0,
    "size": 0,
    "backgroundColor": DColor(),
    "backgroundType": "solid",
    "backgroundRotation": 0,
    "translateX": 0,
    "translateY": 0,
    "randomizeIds": False,
}


class DOptions(dict):
    """
    The options class for :py:class:`dicebear.avatar.DAvatar`
    """

    empty: dict = {}
    default_options = default = default_options

    def __init__(
        self,
        *,
        flip: bool = False,
        rotate: int = 0,
        scale: int = 100,
        radius: int = 0,
        size: int = 0,
        backgroundColor: Union[DColor, List[DColor]] = DColor(),
        backgroundType: str = "solid",
        backgroundRotation: int = 0,
        translateX: int = 0,
        translateY: int = 0,
        randomizeIds: bool = False,
    ):
        """
        Go to https://github.com/jvherck/dicebear#base-options to see all info (important for minimum and maximum values for each option!)
        """
        d = {
            "flip": flip,
            "rotate": rotate,
            "scale": scale,
            "radius": radius,
            "size": size,
            "backgroundColor": backgroundColor,
            "backgroundType": backgroundType,
            "backgroundRotation": backgroundRotation,
            "translateX": translateX,
            "translateY": translateY,
            "randomizeIds": randomizeIds,
        }
        self.update(d.items() - default_options.items())
        if "size" in self and self["size"] == 0:
            self.pop("size")
        super().__init__(self)

    @classmethod
    def from_dict(cls, d: dict) -> "DOptions":
        """Return a new instance of DOptions from a dict."""
        for item in d:
            if item not in default_options or d[item] == default_options[item]:
                d.pop(item, None)
        self = cls()
        self.clear()
        self.update(d)
        return self


def _stats_increase(_file: str, _class: str, _function: str, *, _test: bool = False) -> None:
    """
    Pings an API to update this package's usage stats. This will be used to analyse Dicebear's usage and improve your overall experience.
    """
    if environ.get("ENABLE_PYTHON_DICEBEAR_USAGE_STATS", "").lower() != "true":
        return
    __body = {
        "file": _file,
        "class": _class,
        "function": _function,
        "test": str(_test).lower(),
    }
    __headers = {
        "User-Agent": "pipedream/1",
        "Content-Type": "application/json",
        "-Key": "acbd2023",
    }
    try:
        post(
            "https://eo1p6rm1ydzj8yl.m.pipedream.net/runs",
            json=__body,
            headers=__headers,
            timeout=10,
        )
    except Exception as e:
        _logger.warning("Failed to ping the API to update the usage stats. Error: %s", str(e), exc_info=True)


def _pilcheck(func):
    """Decorator to check if package Pillow is installed"""

    def wrapper(*args, **kwargs):
        if _FindPil.found is True:
            return func(*args, **kwargs)
        raise PILError()

    return wrapper
