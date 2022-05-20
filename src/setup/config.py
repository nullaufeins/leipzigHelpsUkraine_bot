#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.misc import *;
from src.thirdparty.config import *;
from src.thirdparty.code import *;
from src.thirdparty.types import *;

from src.models.config import *;
from src.core.utils import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'OPTIONS',
    'COMMANDS',
    'DEFAULT_LANGUAGE',
    'LANGUAGE_CODES',
    'SUPPORTED_LANGUAGES',
    'TRANSLATIONS',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ON_MISSING: str = '<missing>';

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANTS - extract from data assets + app configuration
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

with open('assets/language.yaml', 'r') as fp:
    _TEXTS = yaml_load(fp, Loader=yaml_FullLoader);
    assert isinstance(_TEXTS, dict);

with open('setup/config.yaml', 'r') as fp:
    _SPEC = yaml_to_js_dictionary(yaml_load(fp, Loader=yaml_FullLoader), deep=True);
    assert isinstance(_SPEC, dict);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANTS - derived
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CONFIG = Config(**_SPEC);
OPTIONS = CONFIG.app_options;
COMMANDS = Commands(CONFIG.commands);
LANGUAGE_CODES = LanguagePatterns(CONFIG.language_codes);
SUPPORTED_LANGUAGES = LANGUAGE_CODES.keys();
DEFAULT_LANGUAGE = OPTIONS.default_language;
TRANSLATIONS = TranslatedTexts(assets=_TEXTS, on_missing=ON_MISSING, default=DEFAULT_LANGUAGE);
