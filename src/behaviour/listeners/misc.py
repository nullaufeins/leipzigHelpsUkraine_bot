#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.api import *;
from src.thirdparty.code import *;
from src.thirdparty.misc import *;
from src.thirdparty.types import *;

from src.core.log_special import *;
from src.core.calls import *;
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

def log_listener(bot: TgBot, app_options: AppOptions):
    '''
    Creates a decorator which adds logging in the post-processing of the action performed by a listener
    '''
    def dec(
        listener: Callable[[TgBot, CallContext, AppOptions], Result[CallValue, CallError]]
    ) -> Callable[[TgMessage], Result[Nothing, Exception]]:
        '''
        Adds logging in the post-processing of the action performed by a listener
        '''
        @wraps(listener)
        @run_safely()
        def wrapped_listener(ctx: TgMessage) -> Result[Nothing, Exception]:
            context = CallContext(ctx, t=datetime.now(), expiry=app_options.message_expiry);
            user = context.getUserCaller(bot);

            result: Result[CallValue, CallError] = listener(bot=bot, context=context, app_options=app_options);
            result_post_processed = result \
                .and_then(pipe_ok(context=context, user=user, app_options=app_options)) \
                .or_else(pipe_err(context=context, user=user, app_options=app_options));

            return result_post_processed;
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
            context_as_json = Result.of(lambda: context.toCensoredRepr(full_censor)).unwrap_or('---');
            user_as_json = Result.of(lambda: user.unwrap().toCensoredRepr(full_censor_user)).unwrap_or('---');
            logDebugListener(context=context_as_json, user=user_as_json, action_taken=value.action_taken);
        else:
            # live logging of success only if action taken:
            if value.action_taken:
                context_as_str = Result.of(lambda: context.toCensoredString(full_censor)).unwrap_or('---');
                user_as_str = Result.of(lambda: user.unwrap().toCensoredString(full_censor_user)).unwrap_or('---');
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

        context_as_str = Result.of(lambda: context.toCensoredString(full_censor)).unwrap_or('---');
        user_as_str = Result.of(lambda: user.unwrap().toCensoredString(full_censor_user)).unwrap_or('---');
        logListenerError(context=context_as_str, user=user_as_str, err=err);
        return Err(err);
    return pipe;
