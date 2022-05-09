#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from thirdparty.code import *;
from thirdparty.misc import *;
from thirdparty.types import *;

from src.core.calls import *;
from src.models.config import *;
from src.models.telegram import *;
from src.behaviour.actions.basic import *;
from src.behaviour.actions.special import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'universal_action',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS universal action
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@run_safely()
def universal_action(
    bot:         MyBot,
    context:     CallContext,
    command:     Command,
    arguments:   List[str],
    app_options: AppOptions
) -> Result[CallValue, CallError]:
    '''
    Once a command has been processed as a valid command,
    this method decides, based on the configuration of the command,
    what action to perform.
    '''
    user = context.getUserCaller(bot);

    ################
    # NOTE: Not currently implemented.
    #
    # # special treatment if new chat member:
    # # if ('new_chat_members' in msg) {
    # #     ...
    # # }
    ################

    # caller has rights <==> status allowed by config of command, or user is anonymous admin:
    has_rights = isinstance(user, Some) and (
        user.unwrap().hasRights(command.aspects.rights) \
        or (context.isGroupAdminCaller(bot) is Some(True))
    );
    cmd = command.aspects.command;
    lang_flag = None;
    if len(arguments) > 0:
        lang_flag = arguments[0];

    if not has_rights:
        return action_delete_and_ignore_with_error(
            bot     = bot,
            context = context,
            text    = 'Caller has insufficient rights!'
        );
    elif not(command.text is None):
        command_text = command.text;
        if not(command.redirect is None):
            return action_on_redirect(
                bot          = bot,
                context      = context,
                redirect     = command.redirect,
                command_text = command_text,
                lang_flag    = lang_flag,
                app_options  = app_options
            );
        else:
            if re.match(r'^\/pin(?:|_(.*))$', string=cmd):
                if lang_flag == 'all':
                    return action_on_pin_all_languages(
                        bot          = bot,
                        context      = context,
                        command_text = command_text
                    );
                else:
                    return action_on_pin_one_language(
                        bot          = bot,
                        context      = context,
                        command_text = command_text,
                        lang_flag    = lang_flag,
                    );
            elif cmd == '/help':
                return action_on_help(
                    bot          = bot,
                    context      = context,
                    command_text = command_text,
                    lang_flag    = lang_flag,
                    app_options  = app_options
                );
            # this cmd is ONLY available if debug=true in config.
            elif cmd == '/hello':
                if (app_options.debug):
                    user_replied_to = context.getUserMessageRepliedTo(bot);
                    return action_on_hello(
                        bot             = bot,
                        context         = context,
                        user            = user,
                        user_replied_to = user_replied_to,
                        command_text    = command_text,
                        lang_flag       = lang_flag,
                        app_options     = app_options
                    );
            else:
                return action_delete_and_ignore_with_error(
                    bot,
                    context,
                    f'Unrecognised command: \'{cmd}\'!'
                );
    else:
        return action_delete_and_ignore_with_error(
            bot,
            context,
            f'Configuration for command \'{cmd}\' missing \'text\' attribute!'
        );
