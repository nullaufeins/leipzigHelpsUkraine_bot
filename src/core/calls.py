#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import annotations;

from src.thirdparty.code import *;
from src.thirdparty.misc import *;
from src.thirdparty.run import *;
from src.thirdparty.types import *;

from src.models.telegram import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'CallValue',
    'CallError',
    'keep_calm_and_carry_on',
    'run_safely',
    'to_async',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# local usage only
T = TypeVar('T');
V = TypeVar('V');
E = TypeVar('E', bound=list);
ARGS = ParamSpec('ARGS');

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS Trace for debugging only!
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CallValue():
    '''
    A auxiliary class which keeps track of the latest return value during calls.
    '''
    action_taken: bool = False;
    message: Option[Message] = Nothing();

    def __init__(self, action_taken: bool = False, message: Optional[Message] = None):
        self.action_taken = action_taken;
        if not (message is None):
            self.message = Some(message);

class CallError(list):
    '''
    An auxiliary class which keeps track of potentially multiple errors during calls.
    '''
    timestamp: str;
    tag: str;
    errors: List[str];

    def __init__(self, tag: str, err: Any = Nothing()):
        self.timestamp = str(datetime.now());
        self.tag = tag;
        self.errors = [];
        if isinstance(err, list):
            for e in err:
                self.append(e);
        else:
            self.append(err);

    def __len__(self) -> int:
        return len(self.errors);

    def append(self, e: Any):
        if isinstance(e, Nothing):
            return;
        if isinstance(e, Some):
            e = e.unwrap();
        self.errors.append(str(e));

    def extend(self, E: CallError):
        self.errors.extend(E.errors);

    def __repr__(self) -> str:
        return f'CallError(tag=\'{self.tag}\', errors={self.errors})';

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

def run_safely(tag: Union[str, None] = None, error_message: Union[str, None] = None):
    '''
    Creates a decorator for an action to perform it safely.

    @inputs (parameters)
    - `tag` - optional string to aid error tracking.
    - `error_message` - optional string for an error message.

    ### Example usage ###
    ```py
    @run_safely(tag='recognise int', error_message='unrecognise string')
    def action1(x: str) -> Result[int, CallError]:
        return Ok(int(x));

    assert action1('5') == Ok(5);
    result = action1('not a number');
    assert isinstance(result, Err);
    err = result.unwrap_err();
    assert isinstance(err, CallError);
    assert err.tag == 'recognise int';
    assert err.errors == ['unrecognise string'];

    @run_safely('recognise int')
    def action2(x: str) -> Result[int, CallError]:
        return Ok(int(x));

    assert action2('5') == Ok(5);
    result = action2('not a number');
    assert isinstance(result, Err);
    err = result.unwrap_err();
    assert isinstance(err, CallError);
    assert err.tag == 'recognise int';
    assert len(err.errors) == 1;
    ```
    NOTE: in the second example, err.errors is a list containing
    the stringified Exception generated when calling `int('not a number')`.
    '''
    def dec(action: Callable[ARGS, Result[V, CallError]]) -> Callable[ARGS, Result[V, CallError]]:
        '''
        Wraps action with return type Result[..., CallError],
        so that it is performed safely a promise,
        catching any internal exceptions as an Err(...)-component of the Result.
        '''
        @wraps(action)
        def wrapped_action(*_, **__) -> Result[V, CallError]:
            # NOTE: intercept Exceptions first, then flatten:
            return Result.of(lambda: action(*_, **__)) \
                .or_else(
                    lambda err: Err(CallError(
                        tag = tag or action.__name__,
                        err = error_message or err
                    ))
                ) \
                .and_then(lambda V: V);
        return wrapped_action;
    return dec;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DECORATOR - converts to async method
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def to_async(executor: Optional[Any] = None):
    '''
    Creates a decorator for a synchronous function to perform it asynchronously.
    '''
    def dec(routine: Callable[ARGS, T]) -> Callable[Concatenate[AbstractEventLoop, ARGS], Awaitable[T]]:
        '''
        Decoratos a synchronous function to perform it asynchronously.
        '''
        @wraps(routine)
        def wrapped_method(*_: ARGS.args, loop: AbstractEventLoop, **__: ARGS.kwargs) -> T:
            return loop.run_in_executor(
                executor = executor,
                func     = lambda: routine(*_, **__),
            );
        return wrapped_method;
    return dec;
