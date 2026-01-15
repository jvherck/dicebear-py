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

import logging
from typing import Union

__all__ = (
    "IncorrectColor",
    "InvalidOption",
    "Error",
    "HTTPError",
    "ImageError",
    "ImageValueError",
    "ImageOSError",
    "PILError",
    "log_error",
)
__filename__ = "errors.py"


class IncorrectColor(Exception):
    """Incorrect color"""

    def __init__(self, wrong_color: str = None):
        super().__init__(f'Incorrect color given: "{wrong_color}" is not an html hex code! (example: #ffffff)')


class InvalidOption(Exception):
    """Invalid option"""

    def __init__(self, wrong_option: str = None):
        super().__init__(
            f'Invalid option given: "{wrong_option}" is not an existing option! (use `Avatar.options` to get all possible options)'
        )


class Error(Exception):
    """General error"""

    def __init__(self, error_type: str = "", message: str = ""):
        super().__init__(f"{error_type + (': ' if error_type else '')}{message}")


class HTTPError(Error):
    """HTTP error"""

    def __init__(self, d: dict):
        super().__init__(message=str(d))


class ImageError(Exception):
    """General image error"""

    def __init__(self, message: str = None):
        super().__init__(message)


class ImageValueError(ImageError):
    """Image value error"""

    def __init__(self, file_name: str = None):
        super().__init__(f'The output format could not be determined ("{file_name}")')


class ImageOSError(ImageError):
    """Image OS error"""

    def __init__(self, message: str = None):
        super().__init__(
            f'The file could not be written. The file may have been created, and may contain partial data. ("{message}")'
        )


class PILError(ImageError):
    """Pillow error"""

    def __init__(self, message: str = "To use this function you need to install Pillow."):
        super().__init__(f'Module "PIL (=Pillow)" is not found! {message}')


_logger = logging.getLogger()
_error_handler = logging.StreamHandler()
_logger.setLevel(logging.ERROR)
_error_handler.setLevel(logging.ERROR)
_logger.addHandler(_error_handler)


def log_error(exception: Union[Exception, str], raise_error: bool = False) -> None:
    """
    Log an error.

    :param exception: class `Exception` | `str` :: the exception or string to log as error
    :type exception: Union[Exception, str]
    :param raise_error: class `bool` :: whether to raise this exception or not (default: False)
    :type raise_error: bool
    """
    if raise_error is False:
        exception_name = exception.__class__.__name__ if isinstance(exception, Exception) else "Error"
        _error_handler.setFormatter(logging.Formatter(f"%(levelname)s: {exception_name}: %(message)s"))
        _logger.error(exception)
        return
    raise RuntimeError(exception) if isinstance(exception, str) else exception
