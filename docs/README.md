---
description: >-
  This is an API wrapper for Dicebear written in Python so Python users can also
  easily make use of this amazing API! The API can generate more than 1
  sexdecillion (that's 17 zero's!) unique avatars!
---

# 🐻 Dicebear Python API Wrapper

<figure><img src="https://img.shields.io/pypi/v/dicebear" alt="Version"><figcaption><p><strong>CURRENT VERSION</strong></p></figcaption></figure>

![Total Downloads](https://static.pepy.tech/badge/dicebear?period=total\&units=international_system\&left_color=grey\&right_color=blue\&left_text=Downloads) ![Downloads / Month](https://static.pepy.tech/badge/dicebear/month?period=month\&units=international_system\&left_color=grey\&right_color=orange\&left_text=Downloads/Month) ![License](https://img.shields.io/github/license/jvherck/dicebear)

![Supported Python Versions](https://img.shields.io/pypi/pyversions/dicebear) ![GitHub Issues](https://img.shields.io/github/issues/jvherck/dicebear) ![Maintenance](https://img.shields.io/maintenance/yes/2025) ![Version Status](https://img.shields.io/pypi/status/dicebear)

{% hint style="info" %}
Dicebear's Python package is <mark style="color:$success;background-color:$success;">up-to-date</mark> with Dicebear's API!
{% endhint %}

{% hint style="warning" %}
Always make sure to update to the latest version to avoid experiencing unresolved bugs!
{% endhint %}

## Introduction

[`dicebear`](https://pypi.org/project/dicebear/) is an API wrapper for [https://dicebear.com](https://dicebear.com). Using this wrapper you can get custom avatars for your program.\
For an example go to [`examples/dicebear.py`](https://github.com/jvherck/dicebear/tree/main/examples).

## Other languages

If you want to use Dicebear avatars but don't use Python, you can use the [dicebear Golang package](https://github.com/jvherck/dicebear-go) or the [official JS/TS package](https://github.com/dicebear/dicebear).

## Useful links

* Official Dicebear: [https://dicebear.com/](https://dicebear.com/)
* PyPI: [https://pypi.org/project/dicebear/](https://pypi.org/project/dicebear/)
* Docs: [https://dicebear.vhjan.me/](https://dicebear.vhjan.me/)
* GitHub: [https://github.com/jvherck/dicebear](https://github.com/jvherck/dicebear)
* Dicebear Python CLI: [https://github.com/jvherck/dicebear-cli](https://github.com/jvherck/dicebear-cli)
* Golang package: [https://github.com/jvherck/dicebear-go](https://github.com/jvherck/dicebear-go)
* JS/TS library: [https://github.com/dicebear/dicebear](https://github.com/dicebear/dicebear)

## How to install

Run `pip install -U dicebear`\
If that doesn't work try `py -m pip install -U dicebear` If that still does not work, try replacing `py` with `python` or `python3`

## Usage

Important note: _Pillow_ is not a required dependency, it's only required when you want to be able to edit the avatar images (using [`DAvatar.pillow()`](reference/avatar.md#def-pillow)). When using a `PIL` function while it's not installed it will raise [`dicebear.errors.PILError`](reference/errors.md#class-pilerror-imageerror).

When the environment variable `ENABLE_PYTHON_DICEBEAR_USAGE_STATS` is set to true, an API will be pinged on most function calls to update this package's usage stats. This will be used to analyse Dicebear's usage and improve your overall experience, but may have performance costs.

```python
import PIL.Image
import os
from dicebear import DAvatar, DStyle, DOptions, DColor, DFormat, bulk_create

# Enable anonymous usage statistics
os.environ['ENABLE_PYTHON_DICEBEAR_USAGE_STATS'] = 'true'

# Creating options
options = DOptions(
    backgroundColor=DColor("00ddd0"),
    rotate=90
)

# Making a DAvatar object
av = DAvatar(
    style=DStyle.pixel_art,
    seed="John Apple",
    options=options
)
print(av.url_svg)  # Prints the svg url

# Editing the DAvatar object
av.edit(
    extra_options=DOptions(backgroundColor=DColor("000000"))
)
# Using `extra_options` keep the `rotate` option but override the `backgroundColor` option

print(av.url_webp)  # Prints the webp url

# Editing the style specific customisations
av.customise(
    blank_options={
        "face": "variant04"
    }
)
# Using `blank_options` will delete your previous customisations for this DAvatar and generate new ones

print(av.url_png)  # Prints the png url

# Saving an avatar to your device
av.save(
    location=None,  # Passing `None` will save it in the current working directory
    file_name="dicebear_avatar",
    file_format=DFormat.svg,
    overwrite=True,
    open_after_save=False
)

# Converting the DAvatar object into a PIL.Image.Image object
av_img: PIL.Image.Image = av.pillow()

# Opening and viewing the DAvatar image
av.open(use_pil=True)  # or av.view()

# Creating multiple random avatars of the same style at once
avatars: list = bulk_create(style=DStyle.random(), amount=10)
```

## CLI Usage

Dicebear has a CLI package that uses Python to generate avatars quickly. You can't customize each avatar, to do that you'll need to use the Python module.

To use the CLI run `pip install dicebear-cli` in a terminal. Documentation can be found here: [https://github.com/jvherck/dicebear-cli](https://github.com/jvherck/dicebear-cli).

## Credits

Special thanks to [DiceBear](https://github.com/dicebear) ([Florian Körner](https://github.com/FlorianKoerner)) for making this amazing API and to [all artists](https://dicebear.com/licenses) that helped making avatars!

## Licenses and privacy policy

* Dicebear **Licenses**: [https://dicebear.com/licenses](https://dicebear.com/licenses)
* Dicebear **Privacy Policy**: [https://dicebear.com/legal/privacy-policy](https://dicebear.com/legal/privacy-policy)
* Dicebear Python API wrapper (this project): [https://jvh.gitbook.io/dicebear/license/](https://jvh.gitbook.io/dicebear/license/)
