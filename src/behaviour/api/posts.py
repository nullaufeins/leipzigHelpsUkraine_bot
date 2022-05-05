#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.api import *;
from src.thirdparty.code import *;

from src.core.calls import *;
from src.models.telegram import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'api_pin_message',
    'api_send_and_pin_message',
    'api_send_message',
    'api_send_message_as_overwrite',
    'api_remove_message',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS posting
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@run_safely(error_message='Api call to send message did not complete.')
def api_send_message(
    bot:    TgBot,
    msg:    Message,
    text:   str,
    layout: MessageLayout,
) -> Result[CallValue, CallError]:
    '''
    Calls Telegram API to to send message.
    '''
    response = bot.send_message(
        text                        = text,
        chat_id                     = msg.getChatId(),
        parse_mode                  = layout.parse_mode.value,
        reply_markup                = layout.reply_markup,
        reply_to_message_id         = layout.reply_to_message_id,
        disable_notification        = layout.disable_notification,
        protect_content             = True,
        allow_sending_without_reply = True,
    );
    if isinstance(response, TgMessage):
        return Ok(CallValue(action_taken=True, message=Message(msg=response)));
    return Err(CallError(err='Api call to send message completed in failure.'));

@run_safely(error_message='Api call to edit message did not complete.')
def api_send_message_as_overwrite(
    bot:    TgBot,
    msg:    Message,
    text:   str,
    layout: MessageLayout,
) -> Result[CallValue, CallError]:
    '''
    Calls Telegram API to to edit an existing message.
    '''
    response = bot.edit_message_text(
        chat_id                     = msg.getChatId(),
        message_id                  = msg.getMessageId(),
        text                        = text,
        protect_content             = True,
        parse_mode                  = layout.parse_mode.value,
        reply_markup                = layout.reply_markup,
        reply_to_message_id         = layout.reply_to_message_id,
        allow_sending_without_reply = True,
    );
    if isinstance(response, TgMessage) or (isinstance(response, bool) and response is True):
        return Ok(CallValue(action_taken=True));
    return Err(CallError(err='Api call to edit message completed in failure.'));

@run_safely(error_message='Api call to pin message did not complete.')
def api_pin_message(
    bot:    TgBot,
    msg:    Message,
) -> Result[CallValue, CallError]:
    '''
    Calls Telegram API to to pin an existing message.
    '''
    success = bot.pin_chat_message(
        chat_id              = msg.getChatId(),
        message_id           = msg.getMessageId(),
        disable_notification = False,
    );
    if success:
        return Ok(CallValue(action_taken=True));
    return Err(CallError(err='Api call to pin message completed in failure.'));

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS posting - complex
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@run_safely(error_message='Api call to send+pin message did not complete.')
def api_send_and_pin_message(
    bot:    TgBot,
    msg:    Message,
    text:   str,
    layout: MessageLayout,
) -> Result[CallValue, CallError]:
    '''
    Calls Telegram API to to send message then pin it.
    '''
    return api_send_message(bot=bot, msg=msg, text=text, layout=layout) \
        .and_then(
            lambda V: api_pin_message(bot=bot, msg=V.message.unwrap())
        );

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS deletion
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@run_safely(error_message='Api call to delete message did not complete.')
def api_remove_message(bot: TgBot, msg: Message) -> Result[CallValue, CallError]:
    '''
    Calls Telegram API to to delete an existing message.
    '''
    success = bot.delete_message(
        chat_id    = msg.getChatId(),
        message_id = msg.getMessageId(),
    );
    if success:
        return Ok(CallValue(action_taken=True));
    return Err(CallError(err='Api call to delete message completed in failure.'));
