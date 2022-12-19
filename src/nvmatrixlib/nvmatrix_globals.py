"""Provide global variables and functions.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/nv_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os

__all__ = ['Error',
           'norm_path',
           ]


class Error(Exception):
    """Base class for exceptions."""


def norm_path(path):
    if path is None:
        path = ''
    return os.path.normpath(path)

