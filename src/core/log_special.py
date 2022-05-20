#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.misc import *;
from src.thirdparty.types import *;

from src.core.log import *;
from src.core.utils import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'logDebugListener',
    'logListenerError',
    'logListenerSuccess',
    'CENSOR_ATTRIBUTE',
    'CENSOR_DIGITS',
    'partiallyCensorMessage',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CENSOR_ATTRIBUTE: str = '*****';
CENSOR_DIGITS: str    = '####';

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS special error logging
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def SuccessMessageListener(context, user) -> str:
    return f'{{"status": "success", "context": {context}, "caller": {user} }}';

def ErrorMessageListener(context, user, err: List[str]) -> str:
    errors_as_str = ' '.join(err);
    return f'[(non fatal) ERROR]: {errors_as_str} {{ "status": "error", "context": {context}, "caller": {user} }}';

def logDebugListener(context: dict, user: dict, action_taken: bool):
    log_debug('Context of Call:');
    log_debug(context);
    log_debug('Called by User:');
    log_debug(user);
    log_debug(f'Action taken: {action_taken}');

def logListenerSuccess(context: str, user: str):
    log_info(SuccessMessageListener(context, user));

def logListenerError(context: str, user: str, err: List[str]):
    log_error(ErrorMessageListener(context, user, err));

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS censoring
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def partiallyCensorMessage(text: str) -> str:
    text = (text or '').strip();

    # apply full censorship if text contains more than one line:
    if re.match(r'[\r\n]', text):
        return CENSOR_ATTRIBUTE;

    # replace occurrences of the form /abc@xyz with /abc @xyz:
    text = re.sub(r'(^|\s)(\/[\w_]+)(\@\w)', repl=r'\1\2 \3', string=text);

    # split into parts and check which parts need censoring:
    words = split_non_empty_parts(text);
    for k, word in enumerate(split_non_empty_parts(text)):
        # fully censor all 'words' that contain non-alphanumeric (excl. some signs that could occur in commands):
        if re.match(r'(?![-_\.\/])\W|.(?![-_\.])\W', word):
            word = CENSOR_ATTRIBUTE
            continue;
        # replace all numerical values by #:
        words[k] = re.sub(r'(\d*[\.\,]\d+|\d+[\.\,]\d*|\d+)', repl=CENSOR_DIGITS, string=word);

    text = ' '.join(words);
    return text;
