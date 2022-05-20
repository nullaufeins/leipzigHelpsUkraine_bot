#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.code import *;
from src.thirdparty.config import *;
from src.thirdparty.system import *;
from src.thirdparty.types import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'get_env_string',
    'get_env_optional_string',
    'get_env_int',
    'get_env_optional_int',
    'get_env_float',
    'get_env_optional_float',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_env_value(env: dict, key: str, default: Any = None) -> Any:
    return env[key] if key in env else default;

def get_env_string(env: dict, key: str, default: Optional[str] = None) -> str:
    result = Result.of(lambda: str(get_env_value(env=env, key=key)));
    if default is None:
        return result.unwrap();
    return result.unwrap_or(default);

def get_env_optional_string(env: dict, key: str) -> Optional[str]:
    result = Result.of(lambda: str(get_env_value(env=env, key=key)));
    return result.unwrap_or(None);

def get_env_int(env: dict, key: str, default: Optional[int] = None) -> int:
    result = Result.of(lambda: int(get_env_value(env=env, key=key)));
    if default is None:
        return result.unwrap();
    return result.unwrap_or(default);

def get_env_optional_int(env: dict, key: str) -> Optional[int]:
    result = Result.of(lambda: int(get_env_value(env=env, key=key)));
    return result.unwrap_or(None);

def get_env_float(env: dict, key: str, default: Optional[float] = None) -> float:
    result = Result.of(lambda: float(get_env_value(env=env, key=key)));
    if default is None:
        return result.unwrap();
    return result.unwrap_or(default);

def get_env_optional_float(env: dict, key: str) -> Optional[float]:
    result = Result.of(lambda: float(get_env_value(env=env, key=key)));
    return result.unwrap_or(None);
