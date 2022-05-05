#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.code import *;

from src.core.utils import *;
from src.models.telegram import *;
from src.setup.config import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'getLanguageByPriorityBasic',
    'getLanguageByPriorityInContext',
    'getLanguageByPriorityInContextIgnoreCaller',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS get languages
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getLanguageByPriorityBasic(
    lang_config: Option[str],
    lang_flag:   Option[str],
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
    lang_config: Option[str],
    lang_flag:   Option[str],
) -> str:
    '''
    Computes language code based on priorities:
    - language code provided as **flag** in command
    - language code hardcoded in command **configuration**
    - language **setting** of user whose message was replied to
    - language **setting** of user who issued the cammand
    - **default language** set in configuration
    '''
    lang_reply_to = context.getLanguageMessageRepliedTo();
    lang_caller   = Some(context.getLanguageCaller());
    return prioritise_language(
        lang_flag,
        lang_config,
        lang_reply_to,
        lang_caller,
    ).unwrap_or(DEFAULT_LANGUAGE);

def getLanguageByPriorityInContextIgnoreCaller(
    context:     CallContext,
    lang_config: Option[str],
    lang_flag:   Option[str],
) -> str:
    '''
    Computes language code based on priorities:
    - language code provided as **flag** in command
    - language code hardcoded in command **configuration**
    - language **setting** of user whose message was replied to
    - **default language** set in configuration
    '''
    lang_reply_to = context.getLanguageMessageRepliedTo();
    return prioritise_language(
        lang_flag,
        lang_config,
        lang_reply_to,
    ).unwrap_or(DEFAULT_LANGUAGE);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS - recognise language code
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@wrap_output_as_option
def prioritise_language(*codes: Option[str]) -> str:
    '''
    Loops through each language code and tries to recognise it.
    Then returns the first recognised language code if possible,
    otherwise returns **default language** as set in configuration
    '''
    is_some = lambda code: isinstance(code, Some);
    unwrap = lambda code: code.unwrap();

    # filter language code which are Something + unwrap them:
    codes_filt = map(unwrap, filter(is_some, codes));

    # apply recognise_language-function to each language code + filter out codes which are not Something:
    codes_recognised = filter(is_some, map(LANGUAGE_PATTERNS.recognise, codes_filt));

    # obtain (value of) fist recognised language code + unwrap it:
    code_recognised = next(codes_recognised).unwrap();

    return code_recognised;
