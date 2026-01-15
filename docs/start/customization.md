---
description: >-
  Customise your avatars with these possibilities. There are over 1 sexdecillion
  (that's 17 zero's!) unique possibilities!
---

# ✏️ Customization

## Styles

All the possible avatar styles.\
[https://dicebear.com/styles](https://dicebear.com/styles)

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

## Base Options

All the possible options for the avatar. These options work for all the styles.

* `seed` (type: [`str`](https://docs.python.org/3/library/stdtypes.html#str)) - the seed for the avatar generator, determine its basic looks
* `flip` (type: [`bool`](https://docs.python.org/3/library/functions.html#bool)) - flips the image vertically (default False)
* `rotate` (type: [`int`](https://docs.python.org/3/library/functions.html#int)) - rotates the avatar (default 0, min 0, max 360)
* `scale` (type: [`int`](https://docs.python.org/3/library/functions.html#int)) - the scale of the avatar drawing itself (default 100, min 0, max 200)
* `radius` (type: [`int`](https://docs.python.org/3/library/functions.html#int)) - the radius of the avatar (default 0, min 0, max 50)
* `size` (type: [`int`](https://docs.python.org/3/library/functions.html#int)) - the size of the avatar (px) (default 256, min 1, max 256)
* `backgroundColor` (type: [`DColor( "transparent" )`](../reference/models.md#class-dcolor) ) - the background color of the avatar (default transparent)
* `backgroundType` (type: [`str`](https://docs.python.org/3/library/stdtypes.html#str)) - the type of background (only `solid` or `gradientLinear`)
* `backgroundRotation` (type: [`int`](https://docs.python.org/3/library/functions.html#int)) - the rotation of the background (only with `gradientLinear`)
* `translateX` (type: [`int`](https://docs.python.org/3/library/functions.html#int)) - move the avatar horizontally (default 0, min -100, max 100)
* `translateY` (type: [`int`](https://docs.python.org/3/library/functions.html#int)) - move the avatar vertically (default 0, min -100, max 100)
* `randomizeIds` (type: [`bool`](https://docs.python.org/3/library/functions.html#bool)) - randomize the IDs in the generated SVG/XML, can be useful if the avatars are included directly in HTML and you want to avoid ID conflicts (default False)

## Specific Style Options

Specific options to get a more detailed avatar. This is different for every style.\
Click the style to see its options.

* [adventurer](https://dicebear.com/styles/adventurer#options)
* [adventurer-neutral](https://dicebear.com/styles/adventurer-neutral#options)
* [avataaars](https://dicebear.com/styles/avataaars#options)
* [avataars-neutral](https://dicebear.com/styles/avataaars-neutral#options)
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
* [notionists](https://www.dicebear.com/styles/notionists#options)
* [notionists-neutral](https://www.dicebear.com/styles/notionists-neutral#options)
* [open-peeps](https://dicebear.com/styles/open-peeps#options)
* [personas](https://dicebear.com/styles/personas#options)
* [pixel-art](https://dicebear.com/styles/pixel-art#options)
* [pixel-art-neutral](https://dicebear.com/styles/pixel-art-neutral#options)
* [rings](https://dicebear.com/styles/rings#options)
* [shapes](https://dicebear.com/styles/shapes#options)
* [thumbs](https://dicebear.com/styles/thumbs#options)
* [toon-head](https://dicebear.com/styles/toon-head#options)

## Formats

These are the only supported formats.\
If you have Pillow (PIL) installed you can convert [`DAvatar` ](../reference/avatar.md#class-davatar)to a [`PIL.Image.Image`](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image) object to get a wider range of formats (Pillow doesn't support svg).

* `DFormat.svg` (default)
* `DFormat.webp`
* `DFormat.avif`
* `DFormat.png`
* `DFormat.jpg`
* `DFormat.jpeg`
* `DFormat.json`
