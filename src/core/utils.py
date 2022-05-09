#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from thirdparty.code import *;
from thirdparty.misc import *;
from thirdparty.types import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'int_to_milliseconds',
    'split_non_empty_parts',
    'yaml_to_js_dictionary',
    'flatten',
    'wrap_output_as_option',
    'unwrap_or_none',
    'unwrap_or_string',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# local usage only
T = TypeVar('T');
ARGS = ParamSpec('ARGS');

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS - strings, arrays
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def split_non_empty_parts(text: str):
    text = text.strip();
    if text == '':
        return [];
    return re.split(r'\s+', string=text);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS - numerical
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def int_to_milliseconds(dt: int) -> timedelta:
    '''
    @inputs
    - `dt` in milliseconds

    @returns
    - `timedelta`-object with `dt` in milliseconds
    '''
    return timedelta(milliseconds=dt);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS - yaml
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def yaml_key_to_js_key(key: str):
    return re.sub(r'-', repl=r'_', string=key);

def yaml_to_js_dictionary(data: Any, deep: bool = False):
    if isinstance(data, dict):
        if deep:
            return {
                yaml_key_to_js_key(key): yaml_to_js_dictionary(value, deep=True)
                for key, value in data.items()
            };
        else:
            return {
                yaml_key_to_js_key(key): value
                for key, value in data.items()
            };
    elif isinstance(data, list):
        return [ yaml_to_js_dictionary(item, deep=deep) for item in data ];
    return data;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS - lists
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def flatten(*X: List[T]) -> List[T]:
    result: List[T] = []
    for x in X:
        result.extend(x);
    return result;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS - something, nothing
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def wrap_output_as_option(func: Callable[ARGS, T]) -> Callable[ARGS, Option[T]]:
    '''
    Wraps a function so that it can be carried out safely.

    ### Example usage ###
    The following renders a(n unsafe) function `f` of type `(str) -> int`
    as a safe function of type `(str) -> Option[int]`.

    ```py
    @wrap_output_as_option
    def f(x: str) -> int:
        # force an artificial internal failure:
        if x == '42':
            raise Exception('bug');
        return 1000*int(x);

    assert f('not a number') == Nothing();
    assert f('42') == Nothing();
    assert f('43') == Some(43000);
    ```
    '''
    @wraps(func)
    def wrapped_func(*_, **__) -> Option[T]:
        return Result.of(lambda: Some(func(*_, **__))).unwrap_or_else(Nothing);
    return wrapped_func;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS - unwrapping
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def unwrap_or_none(wrapped: Callable[[], T]) -> Optional[T]:
    return Result.of(wrapped).unwrap_or(None);

def unwrap_or_string(wrapped: Callable[[], str], default: str) -> str:
    return Result.of(wrapped).unwrap_or(default);
