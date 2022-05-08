#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.api import *;
from src.thirdparty.code import *;
from src.thirdparty.misc import *;
from src.thirdparty.types import *;

from src.core.calls import *;
from src.core.log_special import *;
from src.core.utils import *;
from src.models.config import *;
from src.models.telegram import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'log_listener',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DECORATOR - for listeners
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def log_listener(bot: MyBot, app_options: AppOptions):
    '''
    Creates a decorator which adds logging in the post-processing of the action performed by a listener.
    '''
    def dec(
        listener: Callable[[MyBot, CallContext, AppOptions], Result[CallValue, CallError]]
    ) -> Callable[[TgMessage], Result[Nothing, Exception]]:
        '''
        Adds logging in the post-processing of the action performed by a listener.
        '''
        @wraps(listener)
        @run_safely(tag='listener + post-processing')
        def wrapped_listener(ctx: TgMessage) -> Result[Nothing, Exception]:
            botname = bot.get_me().username;
            context = CallContext(ctx, botname=botname, timestamp=datetime.now(), expiry=options_expiry(app_options));
            user = context.getUserCaller(bot);
            # NOTE: Typehints break, when using named arguments.
            # Need to ensure that signature of listeners is correct, when using decorator.
            return listener(bot, context, app_options) \
                .and_then(pipe_ok(context=context, user=user, app_options=app_options)) \
                .or_else(pipe_err(context=context, user=user, app_options=app_options));
        return wrapped_listener;

    return dec;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS - pipes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def pipe_ok(
    context:     CallContext,
    user:        Option[User],
    app_options: AppOptions,
) -> Callable[[CallValue], Result[Nothing, CallError]]:
    @run_safely(error_message='Post processing of successful action failed!')
    def pipe(value: CallValue) -> Result[Nothing, CallError]:
        '''
        Post actions upon successful completion of work by listener.
        '''
        debug = app_options.debug;
        full_censor = app_options.full_censor;
        full_censor_user = app_options.full_censor_user;

        if debug:
            # !!! only in debug mode during local testing !!!
            context_as_json = unwrap_or_string(lambda: context.toCensoredRepr(full_censor), default='---');
            user_as_json = unwrap_or_string(lambda: user.unwrap().toCensoredRepr(full_censor_user), default='---');
            logDebugListener(context=context_as_json, user=user_as_json, action_taken=value.action_taken);
        else:
            # live logging of success only if action taken:
            if value.action_taken:
                context_as_str = unwrap_or_string(lambda: context.toCensoredString(full_censor), default='---');
                user_as_str = unwrap_or_string(lambda: user.unwrap().toCensoredString(full_censor_user), default='---');
                logListenerSuccess(context=context_as_str, user=user_as_str);
        return Ok(Nothing());
    return pipe;

def pipe_err(
    context:     CallContext,
    user:        Option[User],
    app_options: AppOptions,
) -> Callable[[CallError], Result[Nothing, CallError]]:
    @run_safely(error_message='Post processing of failed action failed!')
    def pipe(err: CallError) -> Result[Nothing, CallError]:
        '''
        Post actions upon failed completion of work by listener.
        '''
        full_censor = app_options.full_censor;
        full_censor_user = app_options.full_censor_user;
        context_as_str = unwrap_or_string(lambda: context.toCensoredString(full_censor), default='---');
        user_as_str = unwrap_or_string(lambda: user.unwrap().toCensoredString(full_censor_user), default='---');
        logListenerError(context=context_as_str, user=user_as_str, err=err.errors);
        return Err(err);
    return pipe;
