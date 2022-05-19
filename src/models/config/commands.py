#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from thirdparty.misc import *;
from thirdparty.code import *;
from thirdparty.types import *;

from src.core.utils import *;
from models.generated.config import Command;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'Commands',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS Commands
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Commands(List[Command]):
    _tests: Option[List[Callable[[str], bool]]] = Nothing();

    @wrap_output_as_option
    def recognise(self, text: str) -> Command:
        '''
        Goes through each command:

        - If `match` is set, then matches text against regex.
        - Otherwise checks if text coincides with `command` (stripped of preliminary `/`).

        @returns
        If a match is found, Some(command) is returned.
        Otherwise Nothing() is returned.
        '''
        if isinstance(self._tests, Some):
            tests = self._tests.unwrap();
        else:
            tests = [create_matcher(command) for command in self];
            self._tests = Some(tests);
        return next(command for command, test in zip(self, tests) if test(text));

# Auxiliary function, creates wrapper:
def create_matcher(command: Command) -> Callable[[str], bool]:
    m = command.aspects.match
    if not(m is None):
        matcher = re.compile(m);
        return lambda text: not (matcher.match(text) is None);
    else:
        cmd = command.aspects.command
        return lambda text: text == cmd;
