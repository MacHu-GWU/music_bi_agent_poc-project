# -*- coding: utf-8 -*-

import typing as T
import textwrap

def get_description(method: T.Callable) -> str:
    """
    Get the description of a function, falling back to its docstring if available.
    """
    return textwrap.dedent(method.__doc__).strip()
