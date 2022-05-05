#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import annotations;

from src.thirdparty.code import *;
from src.thirdparty.misc import *;
from src.thirdparty.types import *;
from src.core.dataclasses import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'CommandMenu',
    'CommandSideMenu',
    'CommandText',
    'CommandRedirect',
    'CommandAspectsRaw',
    'CommandAspects',
    'Command',
    'CommandRecognition',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS Command, CommandAspects
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@paramdataclass
class CommandMenu():
    # necessary fields:
    keyword: str = field();
    # optional fields:
    new_row: bool = field(default=False);
    # optional fields - can be empty:
    lang: Option[str] = optionalparamfield();

@paramdataclass
class CommandSideMenu():
    # necessary fields:
    keyword: str = field();
    # optional fields - can be empty:
    lang: Option[str] = optionalparamfield();

@paramdataclass
class CommandText():
    # necessary fields:
    keyword: str = field();
    # optional fields - can be empty:
    lang: Option[str] = optionalparamfield();

@paramdataclass
class CommandRedirect():
    '''
    Structure of `Command` > `aspects` > `redirect` in config-file:

    - `group` - if included, command treated as redirection to @group.
    - `url`   - if included, command treated as redirection to website.
    '''
    group: Option[str] = optionalparamfield();
    url:   Option[str] = optionalparamfield();

@paramdataclass
class CommandAspectsRaw():
    '''
    Structure of `Command` > `aspects` in config-file:

    - `command`  - '/...' # exact form of command to be registered.
    - `rights`   - [ list of user stati who can use this command ]
    - `strict`   - true => only those commands accepted, which address bot with @<botname>
    - `match`    - regex by which bot should recognise user input as command (after removing @ + trimming)
    - `redirect` - if command is used to redirect user
    '''
    # necessary fields:
    command: str = field();
    # optional fields:
    rights: List[str] = field(default_factory=list);
    strict: bool      = field(default=True);
    # optional fields - can be empty:
    match: Option[str] = optionalparamfield();
    redirect: Option[CommandRedirect] = optionalparamfield(kind='nested', param_factory=CommandRedirect);

class CommandAspects(CommandAspectsRaw):
    def match_command(self, text: str):
        '''
        If `match` is set, then matches text against regex.
        Otherwise checks if text coincides with `command` (stripped of preliminary `/`).
        '''
        if isinstance(self.match, Some):
            return not (re.match(self.match.unwrap(), text) is None);
        return text == self.command.lstrip(r'\/+');

@paramdataclass
class Command():
    '''
    Structure of `Command` in config-file:

    - `aspects`   - defines basic attributes fo command;
    - `menu`      - optional, if command should appear as a button in a menu.
    - `side_menu` - optional, if command should appear in side-menu (suggestions).
    - `text`      - for handling of inline text
    '''
    # necessary fields:
    aspects: CommandAspects = paramfield(kind='nested', param_factory=CommandAspects);
    # optional fields - can be empty:
    menu:      Option[CommandMenu]     = optionalparamfield(kind='nested', param_factory=CommandMenu);
    side_menu: Option[CommandSideMenu] = optionalparamfield(kind='nested', param_factory=CommandSideMenu);
    text:      Option[CommandText]     = optionalparamfield(kind='nested', param_factory=CommandText);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS CommandRecognition
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@dataclass
class CommandRecognition():
    '''
    Contains the most important information about a recognised command:
    - `command`   - string
    - `verified`  - whether post is syntactically valid + acceptable
    - `arguments` - flags
    '''
    command: str = field();
    arguments: List[str] = field(default_factory = []);
    verified: bool = field(default=False);
