#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.code import *;
from src.thirdparty.misc import *;
from src.thirdparty.types import *;

from src.core.dataclasses import *;
from src.core.log import *;
from src.core.utils import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'TranslatedTexts',
    'LanguagePatterns',
    'FactoryLanguagePatterns',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASSES TranslatedText
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TranslatedText():
    texts: Dict[str, str];

    def __init__(self, **texts: str):
        self.texts = texts;

    @wrap_output_as_option
    def value(self, lang: str, default: str) -> str:
        if not(lang in self.texts):
            lang = default;
        return self.texts[lang];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASSES TranslatedTexts
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@paramdataclass
class TranslatedTextsRaw():
    assets: Dict[str, TranslatedText] = paramfield(
        kind = 'nested-dict',
        default_factory = dict,
        param_factory = TranslatedText,
    );

class TranslatedTexts(TranslatedTextsRaw):
    @wrap_output_as_option
    def value(self, keyword: str, lang: str, default: str) -> str:
        return self.assets[keyword].value(lang, default).unwrap();

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS LanguagePatterns
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@paramdataclass
class LanguagePatternsRaw():
    patterns: Dict[str, re.Pattern] = paramfield(
        kind = 'nested',
        default_factory = dict,
        param_factory = lambda **patterns: { key: re.compile(value) for key, value in patterns.items() },
    );

class LanguagePatterns(LanguagePatternsRaw):
    def keys(self) -> List[str]:
        return self.patterns.keys();

    @wrap_output_as_option
    def recognise(self, code: str) -> str:
        return next(code_ for code_, pattern in self.patterns.items() if pattern.match(code));

def FactoryLanguagePatterns(**patterns: str):
    return LanguagePatterns(patterns=patterns);
