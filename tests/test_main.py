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

import unittest
from urllib.parse import quote
from src.dicebear import avatar
from src.dicebear import errors
from src.dicebear import models
from src.dicebear import utility


class TColor(unittest.TestCase):
    def testBase(self):
        c1 = models.DColor("transparent")
        c2 = models.DColor("#fff333")
        c3 = models.DColor("transparent, 000fff")
        c4 = models.DColor(["transparent", "000fff"])
        self.assertEqual(c1, "transparent")
        self.assertEqual(c2, "fff333")
        self.assertRaises(errors.IncorrectColor, models.DColor, html_code="za32da")
        self.assertRaises(errors.IncorrectColor, models.DColor, html_code="transparentt")
        self.assertEqual(c3, "transparent,000fff")
        self.assertEqual(c4, "transparent,000fff")


class TOptions(unittest.TestCase):
    options = models.DOptions(flip=True, scale=50, backgroundType="gradientLinear", translateX=5, randomizeIds=True)

    def testBase(self):
        self.assertEqual(self.options, {
            "flip": True,
            "scale": 50,
            "backgroundType": "gradientLinear",
            "translateX": 5,
            "randomizeIds": True
        })


class TFormat(unittest.TestCase):
    def testBase(self):
        allf = models.DFormat.all_formats
        png = models.DFormat.png
        json = models.DFormat.from_str("json")
        webp = models.DFormat.from_str("webp")
        self.assertEqual(allf, ["svg", "webp", "avif", "png", "jpg", "jpeg", "json"])
        self.assertEqual(png, "png")
        self.assertEqual(json, "json")
        self.assertEqual(webp, "webp")
        self.assertRaises(AttributeError, models.DFormat.from_str, format_str="hvec")


class TStyle(unittest.TestCase):
    def testBase(self):
        alls = models.DStyle.all_styles
        bottts = models.DStyle.bottts
        avataaars = models.DStyle.from_str("avataaars")
        self.assertEqual(alls, models.styles)
        self.assertEqual(bottts, "bottts")
        self.assertEqual(avataaars, "avataaars")
        self.assertRaises(ValueError, models.DStyle.from_str, style_str="something-wrong")
        self.assertIn(models.DStyle.random(), models.styles)
        schema = models.DStyle.get_schema(models.DStyle.rings)
        self.assertEqual("object", schema["type"])
        self.assertIn("properties", schema)
        self.assertIn("seed", schema["properties"])
        self.assertIn("type", schema["properties"]["seed"])
        self.assertEqual("string", schema["properties"]["seed"]["type"])
        self.assertIn("ringOne", schema["properties"])
        self.assertIn("ringTwo", schema["properties"])
        self.assertIn("ringThree", schema["properties"])
        self.assertIn("ringFour", schema["properties"])
        self.assertIn("ringFive", schema["properties"])


class TAvatar(unittest.TestCase):
    def testBase(self):
        style = models.DStyle.random()
        seed = "John Apple"
        options = models.DOptions(flip=True, rotate=90, backgroundType="gradientLinear")
        av = avatar.DAvatar(style, seed, options=options)
        self.assertTrue(str(av).startswith(avatar.Y.format(quote(style), quote(seed)))) # import re
        urlparams = str(av).split('?')[1]
        self.assertIn("seed=John%20Apple", urlparams)
        self.assertIn("flip=true", urlparams)
        self.assertIn("rotate=90", urlparams)
        self.assertIn("backgroundType=gradientLinear", urlparams)

    def test2(self):
        style = "John Apple"
        seed = "John Apple"
        options = models.DOptions(flip=True, rotate=90, backgroundType="gradientLinear")
        self.assertRaises(
            errors.Error,
            avatar.DAvatar,
            style=style, seed=seed, options=options
        )

    def test3(self):
        style = "bottts"
        seed = "John Apple"
        options = models.DOptions(flip=True, rotate=90, backgroundType="gradientLinear")
        av = avatar.DAvatar(style, seed, options=options)
        self.assertIn("properties", av.schema)
        self.assertIn("rotate", av.schema["properties"])

    def testAdv(self):
        style = "bottts"
        seed = "John Apple"
        options = models.DOptions(flip=True)
        custom = {
            "eyes": "dizzy",
            "texture": "camo01",
            "somethingWrong": "doesNotMatter"
        }
        av = avatar.DAvatar(style, seed, options=options, custom=custom)
        self.assertEqual(
            str(av),
            avatar.Y.format(quote(style), quote(seed)) + "flip=true&eyes=dizzy&texture=camo01&somethingWrong=doesNotMatter"
        )


class TUtil(unittest.TestCase):
    def testSingle(self):
        style = models.DStyle.random()
        seed = "John Apple"
        options = models.DOptions(rotate=90)
        custom = {"scale": "52"}
        av = utility.create_avatar(style, seed, options, custom)
        self.assertEqual(
            av,
            avatar.Y.format(quote(style), quote(seed)) + "rotate=90&scale=52"
        )

    def testRandom(self):
        av = utility.create_random(True)
        _url_svg = av.url_svg
        self.assertEqual(av.url_svg, _url_svg)

    def testMulti(self):
        style = models.DStyle.thumbs
        options = models.DOptions(rotate=90)
        custom = {"faceOffsetX": 15}
        avs = utility.bulk_create(style, 3, options=options, custom=custom)
        self.assertEqual(len(avs), 3)
        for item in avs:
            self.assertEqual(
                item.url_svg.startswith("https://api.dicebear.com/") and item.url_svg.endswith("&rotate=90&faceOffsetX=15"),
                True
            )


if __name__ == '__main__':
    unittest.main()
