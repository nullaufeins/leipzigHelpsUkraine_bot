#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from thirdparty.code import *;
from thirdparty.types import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'Trace',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# local usage only
ARGS = ParamSpec('ARGS');
T = TypeVar('T');

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS Trace for debugging only!
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@dataclass
class TraceRaw():
    paths: List[str] = field(default_factory=lambda: []);

class Trace(TraceRaw):
    def add(self, x):
        self.paths.append(x);

    def toRepr(self) -> str:
        return ' -> '.join(self.paths);

    def __str__(self) -> str:
        return self.toRepr();

    # Decorator Trace
    def track_function(self, message: str):
        '''
        A decorator which takes arguments:
        - `message` - a string

        # Example Usage #
        ```py
        trace = Trace();

        @trace.track_function(message='f1')
        def do_stuff1(x: int, y: int) -> int:
            return x + y;

        @trace.track_function(message='f2')
        def do_stuff2(x: int, y: int) -> int:
            return x * y;

        do_stuff1(5, 7);
        do_stuff2(4, 8);
        assert trace.paths == ['f1', 'f2'];
        ```
        '''
        def dec(func: Callable[ARGS, T]) -> Callable[ARGS, T]:
            @wraps(func)
            def wrapped_f(*_, **__):
                self.add(message)
                return func.__call__(*_, **__);
            return wrapped_f;
        return dec;
