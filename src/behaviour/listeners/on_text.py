#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from thirdparty.code import *;

from src.core.calls import *;
from src.models.config import *;
from src.models.telegram import *;
from src.behaviour.actions import *;
from src.behaviour.recognition import *;
from src.behaviour.listeners.misc import *;
from src.behaviour.listeners.on_messages import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'listener_on_text',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# LISTENER - on text
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@run_safely()
def listener_on_text(
    bot:         MyBot,
    context:     CallContext,
    app_options: AppOptions,
) -> Result[CallValue, CallError]:
    '''
    Listens to all messages and decides if Bot has been spoken to
    and if a command is to be carried out.

    See README-TECHNICAL.md.
    '''
    let_user_through = (context.isBotCaller() is False) or (context.isGroupAdminCaller(bot) is True);
    if not let_user_through or context.messageTooOldCaller():
        return action_ignore(context);

    text = context.getTextCaller();
    if is_valid_communication_addess(text):
        context.track('text-listener');
        result = recognise_command_address(text=text, botname=context.getBotname());
        cmd = result.command;
        arguments = result.arguments;
        verified = result.verified;

        # command addressed to another bot - ignore
        if verified is False:
            return action_ignore(context);

        # if command not recognised - delete
        commands_recognised = recognise_commands(cmd);
        if isinstance(commands_recognised, Nothing):
            return action_delete_and_ignore_with_error(
                bot     = bot,
                context = context,
                text    = f'Command \'@<botname> {cmd} ...\' addressed to bot but not recognised!',
            );

        command = commands_recognised.unwrap();
        # if command not addressed to bot AND command is strict, then ignore it:
        if not (verified is True) and command.aspects.strict:
            return action_ignore(context);
        # otherwise perform action:
        return universal_action(bot=bot, context=context, command=command, arguments=arguments, app_options=app_options);
    elif text.startswith(r'/'):
        return listener_on_message(bot=bot, context=context, app_options=app_options);
    else:
        # if not potentially a command:
        return action_ignore(context);
