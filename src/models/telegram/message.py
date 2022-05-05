#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.api import *;
from src.thirdparty.code import *;
from src.thirdparty.config import *;
from src.thirdparty.misc import *;
from src.thirdparty.types import *;

from src.core.log_special import *;
from src.models.telegram.users import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'Message',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS Message
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Message():
    text:      str;
    lang:      str;
    is_bot:    str;
    chatId:    int;
    userId:    int;
    messageId: int;
    timestamp: datetime;

    def __init__(self, msg: TgMessage):
        self.timestamp = datetime.fromtimestamp(msg.date);
        self.text = msg.text.strip();
        self.lang = msg.from_user.language_code;
        self.is_bot = msg.from_user.is_bot;
        # IDs:
        self.messageId = msg.message_id;
        self.chatId = msg.chat.id;
        self.userId = msg.from_user.id;

    def getChatId(self) -> int:
        return self.chatId;

    def getMessageId(self) -> int:
        return self.messageId;

    def getUserId(self) -> int:
        return self.userId;

    def getText(self) -> str:
        return self.text;

    def getLanguage(self) -> str:
        return self.lang;

    def isBot(self) -> bool:
        return self.is_bot;

    def getTimestamp(self) -> datetime:
        '''
        Returns timestamp in ms
        '''
        return self.timestamp;

    def getUser(self, bot: TgBot) -> Option[User]:
        '''
        Returns User class,
        if data can be retrieved or else undefined.
        '''
        return Result.of(
            lambda: Some(User(bot.get_chat_member(chat_id=self.chatId, user_id=self.userId)))
        ).unwrap_or_else(Nothing);

    def messageTooOld(self, t: datetime, expiry: timedelta) -> bool:
        return self.timestamp + expiry < t;

    def toRepr(self) -> Dict[str, Any]:
        return {
            'timestamp': str(self.timestamp),
            'text':      self.text,
            'lang':      self.lang,
            'is_bot':    self.is_bot,
            'messageId': self.messageId,
            'chatId':    self.chatId,
            'userId':    self.userId,
        };

    def __str__(self) -> str:
        return json.dumps(self.toRepr());

    def toCensoredRepr(self, full_censor: bool = False) -> Dict[str, Any]:
        '''
        Provides a censored representation of Message:
        - text` content of message partially censored.
        - fully censored, if `full_censor=true` passed as argument.
        '''
        return {
            'timestamp': str(self.timestamp),
            'text':      partiallyCensorMessage(self.text) if full_censor is False else CENSOR_ATTRIBUTE,
            'lang':      self.lang,
            'is_bot':    self.is_bot,
            'messageId': self.messageId,
            'chatId':    self.chatId,
            'userId':    self.userId,
        };

    def toCensoredString(self, full_censor: bool) -> str:
        '''
        Provides a censored representation of Message:
        - text` content of message partially censored.
        - fully censored, if `full_censor=true` passed as argument.
        '''
        return json.dumps(self.toCensoredRepr(full_censor));
