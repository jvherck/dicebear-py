# DiceBear Py Wrapper  
![Downloads](https://static.pepy.tech/personalized-badge/dicebear?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads)
![Downloads](https://static.pepy.tech/personalized-badge/dicebear?period=month&units=international_system&left_color=grey&right_color=orange&left_text=Downloads/Month) \
![PyPI](https://img.shields.io/pypi/v/dicebear)
![GitHub issues](https://img.shields.io/github/issues/jvherck/dicebear)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dicebear)
![GitHub](https://img.shields.io/github/license/jvherck/dicebear)
![Maintenance](https://img.shields.io/maintenance/yes/2025)
![PyPI - Status](https://img.shields.io/pypi/status/dicebear)

Always keep an eye on https://dicebear.vhjan.me/ for updates and warnings about this packages!

[`dicebear`](https://pypi.org/project/dicebear/) is a Python API wrapper for https://dicebear.com. Using this wrapper you can get custom avatars for your program. \
For an example go to [`examples/dicebear.py`](https://github.com/jvherck/dicebear/tree/main/examples).

## Other languages
If you want to use Dicebear avatars but don't use Python, you can use the 
[dicebear Golang package](https://github.com/jvherck/dicebear-go) or the 
[official JS/TS package](https://github.com/dicebear/dicebear).

## Useful links  
* Official Dicebear: [https://dicebear.com/](https://dicebear.com/)
* PyPI: [https://pypi.org/project/dicebear/](https://pypi.org/project/dicebear/)
* Docs: [https://dicebear.vhjan.me/](https://dicebear.vhjan.me/)  
* GitHub: [https://github.com/jvherck/dicebear](https://github.com/jvherck/dicebear)  
* Dicebear Python CLI: [https://github.com/jvherck/dicebear-cli](https://github.com/jvherck/dicebear-cli)  
* Golang package: [https://github.com/jvherck/dicebear-go](https://github.com/jvherck/dicebear-go)
* JS/TS library: [https://github.com/dicebear/dicebear](https://github.com/dicebear/dicebear)

## Changelog
Find the changelog here: https://dicebear.vhjan.me/changelog

## How to install  
Run `pip install -U dicebear` \
If that doesn't work try `py -m pip install -U dicebear`  
If that still does not work, try replacing `py` with `python` or `python3`

## Usage  
Important note: *Pillow* is not a required dependency, it's only required when you want to be able to edit the avatar images (using `DAvatar.pillow()`).
When using a `PIL` function while it's not installed it will raise `dicebear.errors.PILError`.  

When the environment variable `ENABLE_PYTHON_DICEBEAR_USAGE_STATS` is set to true, an API will be pinged on most function calls to update this package's usage stats. This will be used to analyse Dicebear's usage and improve your overall experience, but may have performance costs.

```py  
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
Dicebear has a CLI package that uses Python to generate avatars quickly.
You can't customize each avatar, to do that you'll need to use the Python module.

To use the CLI run `pip install dicebear-cli` in a terminal. 
Documentation can be found here: https://github.com/jvherck/dicebear-cli.

## Customization
Customize your avatars with these possibilities.  


### Styles  
All the possible avatar styles. \
https://dicebear.com/styles  
  
* `adventurer`  
* `adventurer-neutral`  
* `avataaars`  
* `avataaars-neutral`  
* `big-ears`  
* `big-ears-neutral`  
* `big-smile`  
* `bottts`  
* `bottts-neutral`  
* `croodles`  
* `croodles-neutral`  
* `dylan`
* `fun-emoji`  
* `glass`
* `icons`  
* `identicon`  
* `initials`  
* `lorelei`  
* `lorelei-neutral`  
* `micah`  
* `miniavs`  
* `notionists`
* `notionists-neutral`
* `open-peeps`  
* `personas`  
* `pixel-art`  
* `pixel-art-neutral`
* `rings`
* `shapes`
* `thumbs`
* `toon-head`


### Base Options  
All the possible options for the avatar. These options work for all the styles.  

* `seed` (type: `str`) - the seed for the avatar generator, determine its basic looks  
* `flip` (type: `bool`) - flips the image vertically (default False)  
* `rotate` (type: `int`) - rotates the avatar (default 0, min 0, max 360)  
* `scale` (type: `int`) - the scale of the avatar drawing itself (default 100, min 0, max 200)  
* `radius` (type: `int`) - the radius of the avatar (default 0, min 0, max 50)  
* `size` (type: `int`) - the size of the avatar (px) (default 256, min 1, max 256)  
* `backgroundColor` (type: `DColor("transparent")` ) - the background color of the avatar. this can be a list of strings
if you have *backgroundType* set to "gradientLinear". (default transparent)  
* `backgroundType` (type: `str` ) - set the background to either `gradientLinear` or `solid` (default solid)  
* `backgroundRotation` (type: `int` ) - rotate the background if backgroundType is set to `gradientLinear` (default 0)  
* `translateX` (type: `int`) - move the avatar horizontally (default 0, min -100, max 100)  
* `translateY` (type: `int`) - move the avatar vertically (default 0, min -100, max 100)  
* `randomizeIds` (type: `bool`) - randomize the IDs in the generated SVG/XML, can be useful if the avatars are included 
directly in HTML and you want to avoid ID conflicts (default false)  


### Specific Style Options   
Specific options to get a more detailed avatar. This is different for every style. \
Click the style to see its options.  

* [adventurer](https://dicebear.com/styles/adventurer#options)  
* [adventurer-neutral](https://dicebear.com/styles/adventurer-neutral#options)  
* [avataaars](https://dicebear.com/styles/avataaars#options)  
* [avataaars-neutral](https://dicebear.com/styles/avataaars-neutral#options)  
* [big-ears](https://dicebear.com/styles/big-ears#options)  
* [big-ears-neutral](https://dicebear.com/styles/big-ears-neutral#options)  
* [big-smile](https://dicebear.com/styles/big-smile#options)  
* [bottts](https://dicebear.com/styles/bottts#options)  
* [bottts-neutral](https://dicebear.com/styles/bottts-neutral#options)  
* [croodles](https://dicebear.com/styles/croodles#options)  
* [croodles-neutral](https://dicebear.com/styles/croodles-neutral#options)  
* [dylan](https://dicebear.com/styles/dylan#options)  
* [fun-emoji](https://dicebear.com/styles/fun-emoji#options)  
* [glass](https://dicebear.com/styles/glass#options)  
* [icons](https://dicebear.com/styles/icons#options)  
* [identicon](https://dicebear.com/styles/identicon#options)  
* [initials](https://dicebear.com/styles/initials#options)  
* [lorelei](https://dicebear.com/styles/lorelei#options)  
* [lorelei-neutral](https://dicebear.com/styles/lorelei-neutral#options)  
* [micah](https://dicebear.com/styles/micah#options)  
* [miniavs](https://dicebear.com/styles/miniavs#options)  
* [notionists](https://dicebear.com/styles/notionists#options)  
* [notionists-neutral](https://dicebear.com/styles/notionists-neutral#options)  
* [open-peeps](https://dicebear.com/styles/open-peeps#options)  
* [personas](https://dicebear.com/styles/personas#options)  
* [pixel-art](https://dicebear.com/styles/pixel-art#options)  
* [pixel-art-neutral](https://dicebear.com/styles/pixel-art-neutral#options)  
* [rings](https://www.dicebear.com/styles/rings#options)
* [shapes](https://dicebear.com/styles/shapes#options)  
* [thumbs](https://dicebear.com/styles/thumbs#options)  
* [toon-head](https://dicebear.com/styles/toon-head#options)  


### Formats   
These are the only supported formats. \
If you have Pillow (PIL) installed you can convert `DAvatar` to a `PIL.Image.Image` object to get a
wider range of formats (Pillow doesn't support svg).  
  
* `DFormat.svg` (default)  
* `DFormat.webp`  
* `DFormat.avif`  
* `DFormat.png`  
* `DFormat.jpg`  
* `DFormat.jpeg`  
* `DFormat.json`

## Credits  
Special thanks to [DiceBear](https://github.com/dicebear) ([Florian Körner](https://github.com/FlorianKoerner)) for 
making this amazing API and to [all artists](https://dicebear.com/licenses) for creating these avatars!  

Disclaimer: this repository and its owner are not affiliated with DiceBear.

## Licenses and privacy policy  
- Dicebear **Licenses**: https://dicebear.com/licenses  
- Dicebear **Privacy Policy**: https://dicebear.com/legal/privacy-policy  
- Dicebear Python API wrapper (this project): https://dicebear.vhjan.me/license
