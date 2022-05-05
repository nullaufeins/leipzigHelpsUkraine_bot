#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.code import *;
from src.thirdparty.misc import *;
from src.thirdparty.types import *;

from src.core.utils import *;
from src.models.config import *;
from src.setup.config import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'is_valid_communication_addess',
    'is_valid_communication_sidemenu',
    'recognise_command_address',
    'recognise_command_sidemenu',
    'filter_commands',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS - pattern recognition
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PATTERN_ADDRESS: str = r'^\s*\@(\S+)\s+\/?(\S.*)$';
PATTERN_SIDEMENU: str = r'^\s*\/([^\@\s]+)\s*\@(\S+)\s*$';

def is_valid_communication_addess(text: str) -> bool:
    return re.match(PATTERN_ADDRESS, string=text);

def is_valid_communication_sidemenu(text: str) -> bool:
    return re.match(PATTERN_SIDEMENU, string=text);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS - argument extraction
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def recognise_command_address(text: str, botname: str) -> CommandRecognition:
    '''
    By typing `@` the user can address the bot issuing it a command.
    Recognises the following patterns:

    - `@BOTNAME COMMAND`
    - `@BOTNAME /COMMAND`
    - `@BOTNAME COMMAND arg1 arg2 ...`
    - `@BOTNAME /COMMAND arg1 arg2 ...`

    NOTE: Space after BOTNAME necessary!

    @inputs
    - `text`    - raw text input
    - `botname` - name of bot to be matched

    @returns
    - `CommandRecognition(command, arguments, verified)`, where
    - `command`   - command as text
    - `arguments` - list of flags
    - `verified`  - true/false if botname recognised and matches/not, else undefined

    NOTE: matching of botname is case insensitive.
    '''
    pattern = PATTERN_ADDRESS;
    if re.match(pattern, string=text):
        botname_ = re.sub(pattern, repl=r'\1', string=text).strip();
        text_ = re.sub(pattern, repl=r'\2', string=text).strip();
        parts = split_non_empty_parts(text_);
        return CommandRecognition(
            command   = parts[0],
            arguments = parts[1:],
            verified  = (botname_.lower() == botname.lower()),
        );
    return CommandRecognition();

def recognise_command_sidemenu(text: str, botname: str) -> CommandRecognition:
    '''
    By typing `/` the user is presented a menu of options.
    This results in a posting with the following pattern:

    - `/COMMAND @BOTNAME`

    recognises patterns (space before @BOTNAME not necessary):

    @inputs
    - text    = raw text input
    - botname = name of bot to be matched

    @returns
    `CommandRecognition(command, arguments, verified)`, where
    - `command` - name of command as `/...`-string
    - `arguments` - list of flags passed to command
    - `verified` - `<bool>`, whether botname recognised + matches

    NOTE: matching of botname is case insensitive.
    '''
    pattern = PATTERN_SIDEMENU;
    if re.match(pattern, string=text):
        botname_ = re.sub(pattern, repl=r'\2', string=text).strip();
        command = re.sub(pattern, repl=r'\1', string=text).strip();
        return CommandRecognition(
            command   = command,
            arguments = [],
            verified  = (botname_.lower().lstrip('@') == botname.lower().lstrip('@')),
        );
    return CommandRecognition();

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS - command filtration
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def filter_commands(text: str) -> List[Command]:
    def filt(command: Command):
        return command.aspects.match_command(text);
    return list(filter(filt, COMMANDS));
