#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from thirdparty.api import *;
from thirdparty.code import *;

from src.core.calls import *;
from src.models.telegram import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'pin_message',
    'send_and_pin_message',
    'send_message',
    'send_message_as_overwrite',
    'remove_message',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS posting
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@run_safely()
def send_message(
    bot:    MyBot,
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
    assert isinstance(response, TgMessage), \
        'Api call to send message completed in failure.';
    return Ok(CallValue(action_taken=True, message=Message(msg=response)));

@run_safely()
def send_message_as_overwrite(
    bot:    MyBot,
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
    assert isinstance(response, TgMessage) or (isinstance(response, bool) and response is True), \
        'Api call to edit message completed in failure.';
    return Ok(CallValue(action_taken=True));

@run_safely()
def pin_message(
    bot:    MyBot,
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
    assert isinstance(success, bool) and success is True, \
        'Api call to pin message completed in failure.';
    return Ok(CallValue(action_taken=True));

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS posting - complex
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@run_safely(error_message='Api call to send+pin message did not complete.')
def send_and_pin_message(
    bot:    MyBot,
    msg:    Message,
    text:   str,
    layout: MessageLayout,
) -> Result[CallValue, CallError]:
    '''
    Calls Telegram API to to send message then pin it.
    '''
    return send_message(bot=bot, msg=msg, text=text, layout=layout) \
        .and_then(
            lambda V: pin_message(bot=bot, msg=V.message.unwrap())
        );

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS deletion
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@run_safely()
def remove_message(bot: MyBot, msg: Message) -> Result[CallValue, CallError]:
    '''
    Calls Telegram API to to delete an existing message.
    '''
    success = bot.delete_message(
        chat_id    = msg.getChatId(),
        message_id = msg.getMessageId(),
    );
    assert isinstance(success, bool) and success is True, \
        'Api call to delete message completed in failure.';
    return Ok(CallValue(action_taken=True));
