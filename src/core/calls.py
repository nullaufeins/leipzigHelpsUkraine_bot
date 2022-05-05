#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import annotations;

from src.thirdparty.code import *;
from src.thirdparty.types import *;

from src.core.dataclasses import *;
from src.models.telegram import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'CallValue',
    'CallError',
    'keep_calm_and_carry_on',
    'run_safely',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# local usage only
V = TypeVar('V');
E = TypeVar('E', bound=list);
ARGS = ParamSpec('ARGS');

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS Trace for debugging only!
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@paramdataclass
class CallValue():
    action_taken: bool       = field(default=False);
    message: Option[Message] = optionalparamfield();

class CallError(list):
    errors: List[str];

    def __init__(self, err: Any):
        self.errors = [];
        if isinstance(err, list):
            for e in err:
                self.append(e);
        else:
            self.append(err);

    def __len__(self) -> int:
        return len(self.errors);

    def append(self, e: Any):
        self.errors.append(str(e));

    def extend(self, E: CallError):
        self.errors.extend(E.errors);

    def __repr__(self) -> str:
        return 'CallError([{}])'.format(
            ', '.join(self.errors)
        );

    def __str__(self) -> str:
        return self.__repr__();

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD keep_calm_and_carry_on - handles chain of promises
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@dataclass
class State():
    value: Option[V] = field(default_factory=Nothing);
    error: Option[E] = field(default_factory=Nothing);

def keep_calm_and_carry_on(*actions: Callable[[], Result[V, E]]) -> Result[V, E]:
    '''
    This executes a chain of promises silently accumulating errors along the way,
    then processes the array (tuple) of results at the end.

    NOTE: Assumes that each action only executes safely (i.e. is guaranteed to return a Result[...]).
    '''
    return Result.collect((call_action_passively(action) for action in actions)) \
        .and_then(post_process_results);

def call_action_passively(action: Callable[[], Result[V, E]]) -> Result[State, Nothing]:
    '''
    Calls action and transforms result into a an Ok-state.

    NOTE: Assumes that action only executes safely (i.e. is guaranteed to return a Result[...]).
    '''
    result = action() \
        .and_then(lambda value: Ok(State(value=Some(value)))) \
        .or_else(lambda err: Ok(State(error=Some(err))));
    return result;

def post_process_results(states: Tuple[State]) -> Result[V, E]:
    '''
    Looks at the resulting State-object of each perfomed action.
    If any errors occurred, these are combined into a single error and returned.
    Otherwise the last value is returned.
    '''
    errors_filt = [ state.error.unwrap() for state in states if isinstance(state.error, Some) ];
    if len(errors_filt) == 0:
        return Ok(states[-1].value.unwrap());
    else:
        errors = errors_filt[0];
        for err in errors_filt[1:]:
            errors.extend(err);
        return Err(errors);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DECORATOR - forces methods to run safely
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def run_safely(error_message: Union[str, None] = None):
    '''
    Creates a decorator for an action to perform it safely.

    @inputs (parameters)
    - `error_message` - optional string. If an execption is caught,
      then this overwrites the error message in the case of caught exceptions.
    '''
    def dec(action: Callable[ARGS, Result[V, CallError]]) -> Callable[ARGS, Result[V, CallError]]:
        '''
        Wraps action with return type Result[..., CallError],
        so that it is performed safely a promise,
        catching any internal exceptions as an Err(...)-component of the Result.
        '''
        @wraps(action)
        def wrapped_action(*_, **__) -> Result[V, CallError]:
            return Result.of(lambda: action(*_, **__)) \
                .and_then(lambda res: res) \
                .or_else(lambda err: Err(CallError(error_message or err)));
        return wrapped_action;
    return dec;
