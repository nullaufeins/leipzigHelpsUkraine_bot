#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from functools import wraps;
from functools import partial;
from dataclasses import dataclass;
from dataclasses import field;
from dataclasses import Field;
from dataclasses import asdict;
from dataclasses import MISSING;
# cf. https://github.com/mplanchard/safetywrap
from safetywrap import Ok;
from safetywrap import Err;
from safetywrap import Nothing;
from safetywrap import Result;
from safetywrap import Option;
from safetywrap import Some;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'partial',
    'wraps',
    'asdict',
    'dataclass',
    'field',
    'Field',
    'MISSING',
    'Err',
    'Nothing',
    'Ok',
    'Option',
    'Result',
    'Some',
];
