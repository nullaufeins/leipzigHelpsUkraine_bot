#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# for unit tests:
from contextlib import nullcontext as does_not_raise;
from pytest import fixture;
from pytest_lazyfixture import lazy_fixture;
from pytest import mark;
from pytest import raises as assert_raises;
from unittest import TestCase;
from unittest.mock import patch;

# for integration tests:
from telethon.sync import TelegramClient;
from telethon.sessions import StringSession;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'does_not_raise',
    'fixture',
    'lazy_fixture',
    'mark',
    'assert_raises',
    'TestCase',
    'patch',
    'TelegramClient',
    'StringSession',
];
