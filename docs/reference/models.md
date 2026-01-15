---
description: Classes used to facilitate the module's usage.
---

# Models

## Variables

* `options` ([list](https://docs.python.org/3/library/stdtypes.html#list)): all possible basic options (work for all styles)
* `default_options` ([dict](https://docs.python.org/3/library/stdtypes.html#dict)): a dict with all default options
* `styles` ([list](https://docs.python.org/3/library/stdtypes.html#list)): all available styles



## _class DColor_

### _def \_\_init\_\_()_

All colors used for this module are made with this class. This uses HTML/hex color codes.

Note that `html_code` can also be `transparent` when used for the `backgroundColor` option!

```python
def __init__(self,
    html_code: str | list[str] = "transparent"
) -> None
```

> Returns: [`None`](https://docs.python.org/3.10/c-api/none.html): when called as string it will return the color code
>
> Raises: [`IncorrectColor`](errors.md#class-incorrectcolor-exception): an incorrect html color code is given

<table><thead><tr><th width="148.80536912751677">Parameter</th><th width="124">Type</th><th width="166">Default</th><th>Description</th></tr></thead><tbody><tr><td><code>html_code</code></td><td><a href="https://docs.python.org/3/library/stdtypes.html#str">str</a> | <a href="https://docs.python.org/3/library/stdtypes.html#list">list</a>[<a href="https://docs.python.org/3/library/stdtypes.html#str">str</a>]</td><td><code>"transparent"</code></td><td>HTML/hex color code. This can be a list of strings if <code>backgroundType</code> has been set to "gradientLinear"</td></tr></tbody></table>

### _def random()_

Get a random valid HTML color code.

```python
def random(
) -> DColor()
```

> Returns: [`DColor`](models.md#class-dcolor): the [`DColor` ](models.md#class-dcolor)instance with a random color.



## _class DStyle_

### _def \_\_init\_\_()_

Not to be initialized!

### _def get\_schema()_

Returns a dict with the JSON schema (all properties) of the given avatar style.

```python
def get_schema(
    style: str
) -> dict
```

> Returns: [`dict`](https://docs.python.org/3/library/stdtypes.html#dict): the dictionary containing the avatar style's schema.

<table><thead><tr><th>Parameter</th><th width="150">Type</th><th width="195">Default</th><th>Description</th></tr></thead><tbody><tr><td><code>style</code></td><td><a href="https://docs.python.org/3/library/stdtypes.html#str">str</a></td><td><em>N/A</em></td><td>The name of the style you want to get the schema of.</td></tr></tbody></table>

### _def random()_

Get a random style for [`DStyle`](models.md#class-dstyle).

```python
def random(
) -> str
```

> Returns: [`str`](https://docs.python.org/3/library/stdtypes.html#str): returns a random Style string.

### _def from\_str()_

Get an avatar style from a string.

```python
def from_str(
    style_str: str
) -> str
```

> Returns: [`str`](https://docs.python.org/3/library/stdtypes.html#str): returns a Style string from the given string if the style exists.

<table><thead><tr><th>Parameter</th><th width="150">Type</th><th width="195">Default</th><th>Description</th></tr></thead><tbody><tr><td><code>style_str</code></td><td><a href="https://docs.python.org/3/library/stdtypes.html#str">str</a></td><td><em>N/A</em></td><td>The string to form a style.</td></tr></tbody></table>

### Attributes

For more info check [#styles](../start/customization.md#styles "mention").

* `list` = `all_styles`
* `adventurer`
* `adventurer_neutral`
* `avataaars`
* `avataaars_neutral`
* `big_ears`
* `big_ears_neutral`
* `big_smile`
* `bottts`
* `bottts_neutral`
* `croodles`
* `croodles_neutral`
* `dylan`
* `fun_emoji`
* `glass`
* `icons`
* `identicon`
* `initials`
* `lorelei`
* `lorelei_neutral`
* `micah`
* `miniavs`
* `notionists`
* `notionists_neutral`
* `open_peeps`
* `personas`
* `pixel_art`
* `pixel_art_neutral`
* `rings`
* `shapes`
* `thumbs`
* `toon-head`



## _class DFormat_

### _def \_\_init\_\_()_

Not to be initiated!

### _def from\_str()_

```python
def from_str(
    format_str: str
) -> str
```

> Returns: [`str`](https://docs.python.org/3/library/stdtypes.html#str): returns a Format string from the given string if the format exists.

<table><thead><tr><th>Parameter</th><th width="150">Type</th><th width="195">Default</th><th>Description</th></tr></thead><tbody><tr><td><code>format_str</code></td><td><a href="https://docs.python.org/3/library/stdtypes.html#str">str</a></td><td><em>N/A</em></td><td>The string to form a format.</td></tr></tbody></table>

### Attributes

* `list` = `all_formats`
* `svg`
* `webp`
* `avif`
* `png`
* `jpg`
* `jpeg`
* `json`



## _class DOptions_

### _def \_\_init\_\_()_

```python
def __init__(self,
    *,
    flip: bool = False,
    rotate: int = 0,
    scale: int = 100,
    radius: int = 0,
    size: int = 0,
    backgroundColor: DColor | list(DColor) = DColor(),
    backgroundType: str = "solid",
    backgroundRotation: int = 0,
    translateX: int = 0,
    translateY: int = 0,
    randomizeIds: bool = False
    **kwargs
) -> None
```

> Returns: [`DOptions`](models.md#class-doptions): the [`DOptions` ](models.md#class-doptions)instance to use for [`DAvatar`](avatar.md#class-davatar).

<table><thead><tr><th width="236.50101522441776">Parameter</th><th width="110">Type</th><th width="175.98889174651296">Default</th><th>Description</th></tr></thead><tbody><tr><td><code>flip</code></td><td><a href="https://docs.python.org/3/library/functions.html#bool">bool</a></td><td><code>False</code></td><td>Whether to flip the image vertically</td></tr><tr><td><code>rotate</code></td><td><a href="https://docs.python.org/3/library/functions.html#int">int</a></td><td><p>default <code>0</code></p><p>min <code>0</code>, max <code>360</code></p></td><td>Rotate the avatar</td></tr><tr><td><code>scale</code></td><td><a href="https://docs.python.org/3/library/functions.html#int">int</a></td><td>default <code>100</code><br>min <code>0</code>, max <code>200</code></td><td>Scale of the drawn avatar</td></tr><tr><td><code>radius</code></td><td><a href="https://docs.python.org/3/library/functions.html#int">int</a></td><td>default <code>0</code><br>min <code>0</code>, max <code>50</code></td><td>Radius of the avatar (borders)</td></tr><tr><td><code>size</code></td><td><a href="https://docs.python.org/3/library/functions.html#int">int</a></td><td>default <code>256</code><br>min <code>1</code>, max <code>256</code></td><td>Size of the avatar (in pixels)</td></tr><tr><td><code>backgroundColor</code></td><td><a href="models.md#class-dcolor">DColor</a></td><td><code>DColor("transparent")</code></td><td>Background color for the avatar image</td></tr><tr><td><code>backgroundType</code></td><td><a href="https://docs.python.org/3/library/stdtypes.html#str">str</a></td><td><code>solid</code></td><td>The type of background (only <code>solid</code> or <code>gradientLinear</code>)</td></tr><tr><td><code>backgroundRotation</code></td><td><a href="https://docs.python.org/3/library/functions.html#int">int</a></td><td><code>0</code></td><td>The background's rotation (only with <code>gradientLinear</code>)</td></tr><tr><td><code>translateX</code></td><td><a href="https://docs.python.org/3/library/functions.html#int">int</a></td><td>default <code>0</code><br>min <code>-100</code>, max <code>100</code></td><td>Move the avatar horizontally</td></tr><tr><td><code>translateY</code></td><td><a href="https://docs.python.org/3/library/functions.html#int">int </a></td><td>default <code>0</code><br>min <code>-100</code>, max <code>100</code></td><td>Move the avatar vertically</td></tr><tr><td><code>randomizeIds</code></td><td><a href="https://docs.python.org/3/library/functions.html#bool">bool</a></td><td>default <code>False</code></td><td>Randomize the IDs in the generated SVG/XML, can be useful if the avatars are included directly in HTML and you want to avoid ID conflicts.</td></tr><tr><td><code>**kwargs</code></td><td><em>Any</em></td><td><em>N/A</em></td><td>Kwargs</td></tr></tbody></table>

### Attributes

* `empty`
* `default_options` = `default`
