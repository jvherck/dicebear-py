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

from random import choices, choice, randint
from string import ascii_lowercase, digits
from typing import Union, List, Annotated

from .avatar import DAvatar
from .models import DStyle, DOptions, DColor, _stats_increase

__all__ = (
    "create_avatar",
    "create_random",
    "bulk_create",
)
__filename__ = "utility.py"


def create_avatar(
    style: Union[str, DStyle],
    seed: str,
    options: Union[DOptions, None] = None,
    customisations: Union[dict, None] = None,
) -> DAvatar:
    """
    Creates a DAvatar object and returns it.

    :param style: class `DStyle` :: the style of your avatar
    :param seed: class `str` :: the seed for the avatar; the avatar will be edited according to the seed
    :param options: class `DOptions` :: the options for the avatar
    :param customisations: class `dict` :: customisations for the specified avatar style
    :return: DAvatar object
    """
    if not seed or not isinstance(seed, str):
        raise ValueError("Seed must be a non-empty string")
    _stats_increase(__filename__, "/", ".create_avatar()")
    return DAvatar(style, seed, options=options, custom=customisations)


def create_random(randomOptions: bool = False) -> DAvatar:
    """
    Creates a random DAvatar object and returns it.

    :param randomOptions: class `bool` :: whether to use random (background) options for this avatar or not
    :type randomOptions: bool
    :return: DAvatar object
    """
    _stats_increase(__filename__, "/", ".create_random()")
    options = None
    if randomOptions:
        _type = choice(["solid", "gradientLinear"])
        _color = [DColor.random()]
        if _type == "gradientLinear":
            _color.append(DColor.random())
        options = DOptions(
            flip=choice([True, False]),
            backgroundColor=DColor([str(x) for x in _color]),
            backgroundType=_type,
            backgroundRotation=randint(0, 360),
        )
    return DAvatar(
        DStyle.random(),
        "".join(choices(ascii_lowercase + digits, k=20)),
        options=options,
    )


def bulk_create(
    style: Union[str, DStyle] = DStyle.random(),
    amount: Annotated[int, "Min: 1, Max: 50"] = 2,
    *,
    options: DOptions = None,
    custom: dict = None,
) -> List[DAvatar]:
    """
    Creates a list of :py:class:`DAvatar` objects. Easy way to make multiple of the same style (but different randomly generated seeds) at once.

    :param style: class `DStyle` :: the style to apply to all avatars
    :type style: dicebear.models.DStyle
    :param amount: class `int` :: the amount of DAvatars to create. Default: 2, Min: 1, Max: 50
    :type amount: int
    :param options: class `DOptions` :: options for the avatar
    :type options: dicebear.models.DOptions
    :param custom: class `dict` :: customisations for the specified style
    :type custom: dict
    :return: list[DAvatar] :: a list with DAvatar objects
    """
    if amount >= 50 or amount < 1:
        raise ValueError("argument `amount` must be between 1 and 50")
    _stats_increase(__filename__, "/", ".bulk_create()")
    if style is None:
        style = DStyle.random()
    if custom is None:
        custom = {}
    if options is None:
        options = DOptions.empty
    result = []
    for _ in range(amount):
        try:
            result.append(
                DAvatar(
                    style,
                    "".join(choices(ascii_lowercase + digits, k=20)),
                    options=options,
                    custom=custom,
                )
            )
        except Exception as e:
            print(f"Error creating DAvatar: {e}")
    return result
