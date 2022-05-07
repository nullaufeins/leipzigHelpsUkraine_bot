#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.code import *;
from src.thirdparty.types import *;

from src.core.utils import *;
from src.models.telegram import *;
from src.setup.config import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'get_translation',
    'getLanguageByPriorityBasic',
    'getLanguageByPriorityInContext',
    'getLanguageByPriorityInContextIgnoreCaller',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS get translation
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_translation(
    keyword: str,
    lang:    str,
    missing: Optional[str] = None
) -> str:
    return TRANSLATIONS.value(keyword=keyword, lang=lang, missing=missing);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS get languages
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getLanguageByPriorityBasic(
    lang_config: Optional[str],
    lang_flag:   Optional[str],
) -> str:
    '''
    Computes language code based on priorities:
    - language code provided as **flag** in command
    - language code hardcoded in command **configuration**
    - **default language** set in configuration
    '''
    return prioritise_language(
        lang_flag,
        lang_config,
    ).unwrap_or(DEFAULT_LANGUAGE);

def getLanguageByPriorityInContext(
    context:     CallContext,
    lang_config: Optional[str],
    lang_flag:   Optional[str],
) -> str:
    '''
    Computes language code based on priorities:
    - language code provided as **flag** in command
    - language code hardcoded in command **configuration**
    - language **setting** of user whose message was replied to
    - language **setting** of user who issued the cammand
    - **default language** set in configuration
    '''
    lang_reply_to = unwrap_or_none(lambda: context.getLanguageMessageRepliedTo().unwrap());
    lang_caller   = context.getLanguageCaller();
    return prioritise_language(
        lang_flag,
        lang_config,
        lang_reply_to,
        lang_caller,
    ).unwrap_or(DEFAULT_LANGUAGE);

def getLanguageByPriorityInContextIgnoreCaller(
    context:     CallContext,
    lang_config: Optional[str],
    lang_flag:   Optional[str],
) -> str:
    '''
    Computes language code based on priorities:
    - language code provided as **flag** in command
    - language code hardcoded in command **configuration**
    - language **setting** of user whose message was replied to
    - **default language** set in configuration
    '''
    lang_reply_to = unwrap_or_none(lambda: context.getLanguageMessageRepliedTo().unwrap());
    return prioritise_language(
        lang_flag,
        lang_config,
        lang_reply_to,
    ).unwrap_or(DEFAULT_LANGUAGE);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS - recognise language code
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@wrap_output_as_option
def prioritise_language(*codes: Optional[str]) -> str:
    '''
    Loops through each language code and tries to recognise it.
    Then returns the first recognised language code if possible,
    otherwise returns **default language** as set in configuration
    '''

    ################
    # NOTE: (for development)
    # - next(·) only applicable to iterators, filters, generators, etc. not lists.
    # - next(A) alters A itself.
    ################

    # filter language code which are not None:
    codes_filt = ( code for code in codes if not(code is None) );

    # apply recognise_language-function to each language code + filter out codes which are not Something:
    is_some = lambda code: isinstance(code, Some);
    codes_recognised = filter(is_some, map(LANGUAGE_CODES.recognise, codes_filt));

    # obtain (value of) fist recognised language code + unwrap it:
    code = next(codes_recognised).unwrap();

    return code;
