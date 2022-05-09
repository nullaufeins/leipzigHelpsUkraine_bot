#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from thirdparty.api import *;
from thirdparty.code import *;
from thirdparty.config import *;
from thirdparty.types import *;

from src.core.log_special import *;
from models.config import Rights;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'User',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS User
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class User():
    id:         int;
    is_bot:     bool;
    first_name: str;
    username:   str;
    lang:       str;
    user_type:  str;

    def __init__(self, member: TgChatMember):
        self.id = member.user.id;
        self.is_bot = member.user.is_bot;
        self.first_name = member.user.first_name;
        self.username = member.user.username;
        self.lang = member.user.language_code;
        self.user_type = member.status;

    def isBot(self) -> bool:
        return self.is_bot;

    def getId(self) -> int:
        return self.id;

    def getLanguage(self) -> str:
        return self.lang;


    def getUserName(self) -> str:
        return self.username;

    def getUserNameWithReference(self) -> str:
        return '@' + self.username;

    def getFirstName(self) -> str:
        return self.first_name;

    def getUserType(self) -> str:
        return self.user_type;

    def hasRights(self, rights: List[Rights]) -> bool:
        return any( self.user_type == r.value for r in rights );

    def toRepr(self) -> Dict[str, Any]:
        return {
            'id':         self.id,
            'user_type':  self.user_type,
            'is_bot':     self.is_bot,
            'first_name': self.first_name,
            'username':   self.getUserNameWithReference(),
            'lang':       self.lang,
        };

    def toString(self) -> str:
        return json.dumps(self.toRepr());

    def toCensoredRepr(self, full_censor=False) -> Dict[str, Any]:
        '''
        Provides a censored representation of User.
        - censors `first_name`.
        - censors `username` <==> `full_censor=true` passed as argument.

        NOTE: `first_name` forcibly censored as we never want to log self.
        The `username` is not necessarily sensitive information.
        '''
        return {
            'id':         self.id,
            'user_type':  self.user_type,
            'is_bot':     self.is_bot,
            'first_name': CENSOR_ATTRIBUTE,
            # only censor censor if absolutely necessary:
            'username':   self.getUserName() if full_censor is False else CENSOR_ATTRIBUTE,
            'lang':       self.lang,
        };

    def toCensoredString(self, full_censor=False) -> str:
        '''
        Provides a censored representation of User.
        - censors `first_name`.
        - censors `username` <==> `full_censor=true` passed as argument.

        NOTE: `first_name` forcibly censored as we never want to log self.
        The `username` is not necessarily sensitive information.
        '''
        return json.dumps(self.toCensoredRepr(full_censor));
