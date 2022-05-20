#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.types import *;
from tests.thirdparty.unit import *;

from src.core.log import log_dev;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FIXTURES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@fixture(scope='module', autouse=True)
def test() -> TestCase:
    return TestCase();

@fixture(scope='module', autouse=True)
def debug() -> Callable[..., None]:
    '''
    Fixture for development purposes only.
    Logs to file 'logs/debug.log'.
    '''
    return log_dev;
