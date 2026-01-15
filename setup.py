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
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dicebear",
    license="MIT License",
    author="jvherck",
    author_email="jan@vhjan.me",
    maintainer="jvherck",
    maintainer_email="jan@vhjan.me",
    url="https://dicebear.vhjan.me/",
    project_urls={"Documentation": "https://dicebear.vhjan.me/", "Source": "https://github.com/jvherck/dicebear", "Tracker": "https://github.com/jvherck/dicebear/issues"},
    description="A python wrapper for DiceBear's avatar generating API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=['requests', 'urllib3'],
    python_requires='>=3.7',
    keywords=['python', 'dicebear', 'avatar', 'avatars', 'generating', 'generation', 'generator', 'API', 'wrapper',
              'image', 'images', 'picture', 'pictures', 'png', 'jpg', 'svg', 'json', 'cli', 'pillow', 'pil', 'requests',
              'adventurer', 'adventurer-neutral', 'avataaars', 'avataaars-neutral', 'big-ears', 'big-ears-neutral',
              'big-smile', 'bottts', 'bottts-neutral', 'croodles', 'croodles-neutral', 'fun-emoji', 'icons',
              'identicon', 'initials', 'lorelei', 'lorelei-neutral', 'micah', 'miniavs', 'notionists',
              'notionists-neutral', 'open-peeps', 'personas', 'pixel-art', 'pixel-art-neutral', 'shapes', 'thumbs',
              'toon-head'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Other Audience",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Operating System :: Unix",
        "Operating System :: MacOS", # :: MacOS X
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
        "Topic :: Artistic Software",
        "Topic :: Games/Entertainment",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Other/Nonlisted Topic",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
