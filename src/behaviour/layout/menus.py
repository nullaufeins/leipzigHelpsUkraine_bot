#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.api import *;
from src.thirdparty.code import *;
from src.thirdparty.misc import *;
from src.thirdparty.types import *;

from src.core.utils import *;
from src.setup.config import *;
from src.models.telegram import *;
from src.behaviour.recognition import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'get_menu_inline',
    'get_menu_hidden',
    'get_message_options_basic',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PATTERN_GROUP = r'^\@(.*)$';
REPLACE_PATTERN_URL_GROUP = r'https://t.me/\1';

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
        reply_to_message_id = unwrap_or_none(lambda: reply_to_msg.unwrap().getMessageId()),
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
        reply_to_message_id = unwrap_or_none(lambda: reply_to_msg.unwrap().getMessageId()),
    );

def get_message_options_basic(
    reply_to_msg: Option[Message] = Nothing()
) -> MessageLayout:
    return MessageLayout(
        disable_notification = True,
        parse_mode = PARSE_MODE.NONE,
        reply_to_message_id = unwrap_or_none(lambda: reply_to_msg.unwrap().getMessageId()),
    );

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def create_rows(lang: str) -> List[List[dict]]:
    rows = [];
    count = 0;
    current_row = [];
    for command in COMMANDS:
        if (command.menu is None) or (command.redirect is None):
            continue;
        menu = command.menu;
        redirect = command.redirect;
        if not(redirect.group is None):
            url = create_url_from_group_link(redirect.group);
        elif not(redirect.url is None):
            url = redirect.url;
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
    return re.sub(PATTERN_GROUP, repl=REPLACE_PATTERN_URL_GROUP, string=text);
