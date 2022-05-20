#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.code import *;

from src.core.calls import *;
from src.core.utils import *;
from src.api import posts;
from src.models.config import *;
from src.models.telegram import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'action_empty',
    'action_ignore',
    'action_ignore_with_error',
    'action_delete_and_ignore',
    'action_delete_and_ignore_with_error',
    'action_send_message',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS basic actions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@run_safely()
def action_empty() -> Result[CallValue, CallError]:
    '''
    return resolved with value false to indicated that no action was taken.
    '''
    return Ok(CallValue(action_taken=False));

@run_safely()
def action_ignore(context: CallContext) -> Result[CallValue, CallError]:
    '''
    return resolved with value false to indicated that no action was taken.
    '''
    context.track('basic-action:ignore');
    return action_empty();

@run_safely()
def action_ignore_with_error(context: CallContext, text: str) -> Result[CallValue, CallError]:
    context.track('basic-action:ignore-with-error');
    return Err([text or 'Something went wrong. Ignoring.']);

@run_safely()
def action_delete(
    bot:     MyBot,
    context: CallContext,
) -> Result[CallValue, CallError]:
    context.track('basic-action:delete');
    return posts.remove_message(bot=bot, msg=context.getCallerMessage());

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS actions consisting of a combination of basic actions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@run_safely()
def action_delete_and_ignore(
    bot:     MyBot,
    context: CallContext,
) -> Result[CallValue, CallError]:
    return keep_calm_and_carry_on(
        lambda: action_delete(bot=bot, context=context),
        lambda: action_ignore(context=context),
    );

@run_safely()
def action_delete_and_ignore_with_error(
    bot:     MyBot,
    context: CallContext,
    text:    str,
) -> Result[CallValue, CallError]:
    return keep_calm_and_carry_on(
        lambda: action_delete(bot=bot, context=context),
        lambda: action_ignore_with_error(context=context, text=text),
    );

@run_safely()
def action_delete_and_reply(
    bot:     MyBot,
    context: CallContext,
    text:         str,
    layout:       MessageLayout,
) -> Result[CallValue, CallError]:
    return keep_calm_and_carry_on(
        lambda: action_delete(bot=bot, context=context),
        context.track_function(message='basic-action:new-post')(
            lambda: posts.send_message(bot=bot, msg=context.getCallerMessage(), text=text, layout=layout)
        ),
    );

@run_safely()
def action_send_message(
    bot:          MyBot,
    context:      CallContext,
    text:         str,
    layout:       MessageLayout,
    app_options:  AppOptions
) -> Result[CallValue, CallError]:
    if app_options.delete_calls:
        return action_delete_and_reply(bot=bot, context=context, text=text, layout=layout);
    else:
        context.track('basic-action:edit-post');
        return posts.send_message_as_overwrite(bot=bot, msg=context.getCallerMessage(), text=text, layout=layout);
