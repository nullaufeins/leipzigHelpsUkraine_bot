#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.api import *;
from src.thirdparty.code import *;
from src.thirdparty.misc import *;
from src.thirdparty.types import *;

from src.setup.config import *;
from src.models.telegram import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'get_menu_inline',
    'get_menu_hidden',
    'get_message_options_basic',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Creates inline keyboard categories for the user to select from
def get_menu_inline(
    lang: str,
    reply_to_msg: Option[Message] = Nothing()
) -> MessageLayout:
    rows = create_rows(lang=lang);
    reply_markup = TgInlineKeyboardMarkup(row_width=3);
    for row in rows:
        reply_markup.row(*[TgInlineKeyboardButton(**button) for button in row]);
    return MessageLayout(
        reply_markup = reply_markup,
        disable_notification = True,
        parse_mode = PARSE_MODE.NONE,
        reply_to_message_id = Result.of(lambda: reply_to_msg.unwrap().getMessageId()).unwrap_or(None),
    );

def get_menu_hidden(
    lang: str,
    reply_to_msg: Option[Message] = Nothing()
) -> MessageLayout:
    reply_markup = TgReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3);
    rows = create_rows(lang=lang);
    for row in rows:
        reply_markup.row(*[TgKeyboardButton(**button) for button in row]);
    return MessageLayout(
        reply_markup = reply_markup,
        disable_notification = True,
        parse_mode = PARSE_MODE.NONE,
        reply_to_message_id = Result.of(lambda: reply_to_msg.unwrap().getMessageId()).unwrap_or(None),
    );

def get_message_options_basic(
    reply_to_msg: Option[Message] = Nothing()
) -> MessageLayout:
    return MessageLayout(
        disable_notification = True,
        parse_mode = PARSE_MODE.NONE,
        reply_to_message_id = Result.of(lambda: reply_to_msg.unwrap().getMessageId()).unwrap_or(None),
    );

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def create_rows(lang: str) -> List[List[dict]]:
    rows = [];
    count = 0;
    current_row = [];
    for command in COMMANDS:
        if isinstance(command.menu, Nothing) or isinstance(command.aspects.redirect, Nothing):
            continue;
        menu = command.menu.unwrap();
        redirect = command.aspects.redirect.unwrap();
        if isinstance(redirect.group, Some):
            url = create_url_from_group_link(redirect.group.unwrap());
        elif isinstance(redirect.url, Some):
            url = redirect.url.unwrap();
        else:
            continue;
        if menu.new_row and count > 0:
            rows.append(current_row[:]);
            current_row = [];
        text = get_translation(keyword=menu.keyword, lang=lang);
        current_row.append(dict(text=text, url=url));
        count += 1;
    rows.append(current_row[:]);
    return rows;

def create_url_from_group_link(text: str) -> str:
    return re.sub(r'^\@(.*)$', repl=r'https://t.me/\1', string=text);
