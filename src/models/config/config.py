#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.types import *;
from src.core.dataclasses import *;

from src.models.config.app import *;
from src.models.config.languages import *;
from src.models.config.commands import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'Config',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS Config
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@paramdataclass
class Config():
    info: dict            = paramfield(kind='nested', default_factory=dict, param_factory=dict);
    options: AppOptions   = paramfield(kind='nested', default_factory=AppOptions, param_factory=AppOptions);
    default_language: str = field(default = 'en');
    languages: LanguagePatterns = paramfield(
        default_factory = LanguagePatterns,
        param_factory = lambda patterns: LanguagePatterns(patterns=patterns),
        repr = False,
    );
    commands: List[Command] = paramfield(
        kind = 'nested-list',
        default_factory = list,
        param_factory = Command,
        repr = False,
    );
