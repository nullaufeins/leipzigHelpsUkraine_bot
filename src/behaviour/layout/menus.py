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
    row_width = 3;
    reply_markup = TgInlineKeyboardMarkup(row_width=row_width);
    for row in create_rows_of_button_parameters(lang=lang, row_width=row_width):
        reply_markup.row(*[TgInlineKeyboardButton(
            text=button.text,
            url=button.url,
        ) for button in row]);
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
    row_width = 3;
    reply_markup = TgReplyKeyboardMarkup(
        resize_keyboard   = True,
        one_time_keyboard = True,
        row_width         = row_width,
    );
    for row in create_rows_of_button_parameters(lang=lang, row_width=row_width):
        reply_markup.row(*[TgKeyboardButton(
            text=button.text,
        ) for button in row]);
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

@dataclass
class ButtonParameters():
    text: str = field(default='');
    url: str = field(default='');

def create_rows_of_button_parameters(lang: str, row_width: int) -> Generator[List[ButtonParameters], None, None]:
    first = True;
    row = [];
    for command in COMMANDS:
        if (command.menu is None) or (command.redirect is None):
            continue;
        menu = command.menu;
        group = command.redirect.group;
        url = command.redirect.url
        # ensure that either menu or redirect command set
        if not(group is None):
            url = create_url_from_group_link(group);
        if url is None:
            continue;
        # check if a new row is either needed or demanded:
        if not first and ((len(row) >= row_width) or menu.new_row):
            yield row;
            row = [];
        # add button parameters
        row.append(ButtonParameters(
            text = get_translation(keyword=menu.keyword, lang=lang),
            url  = url,
        ));
        first = False;
    yield row;

def create_url_from_group_link(text: str) -> str:
    return re.sub(PATTERN_GROUP, repl=REPLACE_PATTERN_URL_GROUP, string=text);
