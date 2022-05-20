#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.code import *;
from src.thirdparty.misc import *;
from src.thirdparty.types import *;

from src.core.utils import *;
from models.generated.config import LanguageCode;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'TranslatedTexts',
    'LanguagePatterns',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASSES TranslatedText, TranslatedTexts
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TranslatedText():
    texts: Dict[str, str];

    def __init__(self, **texts: str):
        self.texts = texts;

    @wrap_output_as_option
    def value(self, lang: str, default: str) -> str:
        '''
        @inputs
        - `lang` - language code to use when extracting the text from the dictionary.
        - `default` - (optional) language code to use, if no translation for `lang` can be found.

        @returns
        The appropriate asset in the desired (or else deafult) language code.
        Returns safely wrapped as an Option[str].
        '''
        if not(lang in self.texts):
            lang = default;
        return self.texts[lang];

class TranslatedTexts():
    assets: Dict[str, TranslatedText];
    default: str;
    on_missing: str;

    def __init__(
        self,
        assets:     Dict[str, Dict[str, str]],
        on_missing: str,
        default:    str
    ):
        self.assets = {
            keyword: TranslatedText(**phrases)
            for keyword, phrases in assets.items()
        };
        self.default = default;
        self.on_missing = on_missing;

    def value(
        self,
        keyword: str,
        lang:    str,
        missing: Optional[str] = None,
        default: Optional[str] = None,
    ) -> str:
        '''
        @inputs
        - `keyword` - keyword of asset to translate.
        - `lang` - language code to use when extracting the text from tha assets file.
        - `default` - (optional) language code to use, if no translation for `lang` can be found.
        - `missing` - (optional) value to return if translation fails.

        @returns
        The appropriate asset in the desired (or else deafult) language code,
        otherwise returns the 'missing' value.
        '''
        return self.assets[keyword] \
            .value(lang=lang, default=default or self.default) \
            .unwrap_or(missing or self.on_missing);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS LanguagePatterns
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LanguagePatterns(List[LanguageCode]):
    _tests: Option[List[Callable[[str], bool]]] = Nothing();

    def keys(self) -> List[str]:
        return [obj.code for obj in self];

    @wrap_output_as_option
    def recognise(self, text: str) -> str:
        if isinstance(self._tests, Some):
            tests = self._tests.unwrap();
        else:
            tests = [ create_matcher(obj) for obj in self ];
            self._tests = Some(tests);
        return next(obj.code for obj, test in zip(self, tests) if test(text));

# Auxiliary function, creates wrapper:
def create_matcher(obj: LanguageCode) -> Callable[[str], bool]:
    r = re.compile(obj.pattern); # compile once!
    return lambda text: not (r.match(text) is None);
