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

from src.core.utils import *;
from src.core.trace import *;
from src.models.telegram.bot import *;
from src.models.telegram.message import *;
from src.models.telegram.users import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'CallContext',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS Call Context
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CallContext:
    trace:        Trace
    timestamp:    datetime; # NOTE: time point at which command is processed!
    expiry:       timedelta;
    botname:      str;
    caller_msg:   Message;
    reply_to_msg: Option[Message];
    userCaller:   Option[User];
    userReplyTo:  Option[User];
    groupId:      int;
    groupTitle:   str;

    def __init__(self, ctx: TgMessage, botname: str, timestamp: datetime, expiry: timedelta):
        self.timestamp = timestamp;
        self.expiry = expiry;
        self.trace = Trace();
        self.botname = botname;
        self.caller_msg = Message(ctx);
        self.reply_to_msg = Some(Message(ctx.reply_to_message)) if isinstance(ctx.reply_to_message, TgMessage) else Nothing();
        self.userCaller = Nothing();
        self.userReplyTo = Nothing();
        self.groupId = ctx.chat.id;
        self.groupTitle = ctx.chat.title;

    def track(self, message: str):
        self.trace.add(message);

    def track_function(self, message: str):
        '''
        A decorator which takes arguments:
        - `message` - a string

        # Example Usage #
        ```py
        context = CallContext(...);

        @context.track_function(message='f1')
        def do_stuff1(x: int, y: int) -> int:
            return x + y;

        @context.track_function(message='f2')
        def do_stuff2(x: int, y: int) -> int:
            return x * y;

        do_stuff1(5, 7);
        do_stuff2(4, 8);
        assert trace.paths == ['f1', 'f2'];
        ```
        '''
        dec = self.trace.track_function(message);
        return dec;

    def getCallerMessage(self) -> Message:
        return self.caller_msg;

    def getReplyToMessage(self) -> Option[Message]:
        return self.reply_to_msg;

    def getBotname(self) -> str:
        return self.botname;

    def toRepr(self) -> Dict[str, Any]:
        return {
            'botname': self.botname,
            'group_id': self.groupId,
            'group_title': self.groupTitle,
            'message': self.caller_msg.toRepr(),
            'reply_to': self.reply_to_msg.unwrap().toRepr() \
                if isinstance(self.reply_to_msg, Some) else None,
            'trace': self.trace.toRepr(),
        };

    def __str__(self) -> str:
        return json.dumps(self.toRepr());

    def toCensoredRepr(self, full_censor: bool = False) -> Dict[str, Any]:
        '''
        Provides a censored representation of CallContext.
        - censors `message` attributes (fully if `full_censor=true`).
        - fully censors `reply_to` message attributes.^

        NOTE: ^forced, as we never want to log text contents of this message.
        '''
        return {
            'botname': self.botname,
            'group_id': self.groupId,
            'group_title': self.groupTitle,
            'message': self.caller_msg.toCensoredRepr(full_censor),
            'reply_to': self.reply_to_msg.unwrap().toCensoredRepr(True) \
                if isinstance(self.reply_to_msg, Some) else None,
            'trace': self.trace.toRepr(),
        };

    def toCensoredString(self, full_censor: bool = False) -> str:
        '''
        Provides a censored representation of CallContext.
        - censors `message` attributes (fully if `full_censor=true`).
        - fully censors `reply_to` message attributes.^

        NOTE: ^forced, as we never want to log text contents of this message.
        '''
        return json.dumps(self.toCensoredRepr(full_censor));

    '''
    Methods related just to caller
    '''

    @wrap_output_as_option
    def isGroupAdminCaller(self, bot: MyBot) -> bool:
        '''
        Returns true/false <==> user is/is not anon admin.
        If information cannot be obtained, returns None.
        '''
        user = self.getUserCaller(bot);
        return user.unwrap().isBot() is True \
            and user.unwrap().getFirstName() == 'Group' \
            and user.unwrap().getUserName() == 'GroupAnonymousBot';

    def getTextCaller(self) -> str:
        self.isGroupAdminCaller
        return self.caller_msg.getText();

    def getLanguageCaller(self) -> str:
        return self.caller_msg.getLanguage();

    def isBotCaller(self) -> bool:
        return self.caller_msg.isBot();

    def messageTooOldCaller(self) -> bool:
        return self.caller_msg.messageTooOld(self.timestamp, self.expiry);

    def getUserCaller(self, bot: MyBot) -> Option[User]:
        '''
        Returns User class for caller, if data can be retrieved or else undefined.
        '''
        # compute once!
        if isinstance(self.userCaller, Nothing):
            self.userCaller = self.caller_msg.getUser(bot);
        return self.userCaller;

    '''
    Methods related just to message_replied to
    '''

    @wrap_output_as_option
    def getTextMessageRepliedTo(self) -> str:
        return self.reply_to_msg.unwrap().getText();

    @wrap_output_as_option
    def getLanguageMessageRepliedTo(self) -> str:
        return self.reply_to_msg.unwrap().getLanguage();

    @wrap_output_as_option
    def isBotMessageRepliedTo(self) ->bool:
        return self.reply_to_msg.unwrap().isBot();

    @wrap_output_as_option
    def messageTooOldMessageRepliedTo(self) -> bool:
        return self.reply_to_msg.unwrap().messageTooOld(self.timestamp, self.expiry);

    def getUserMessageRepliedTo(self, bot: MyBot) -> Option[User]:
        '''
        Returns User class for message replied to, if data can be retrieved or else undefined.
        '''
        # compute once!
        if isinstance(self.userReplyTo, Nothing) and isinstance(self.reply_to_msg, Some):
            self.userReplyTo = self.reply_to_msg.unwrap().getUser(bot);
        return self.userReplyTo;
