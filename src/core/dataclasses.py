#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import re;
from safetywrap import Nothing;
from safetywrap import Some;
from dataclasses import dataclass;
from dataclasses import MISSING;
from dataclasses import field;
from dataclasses import Field;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'field',
    'Field',
    'optionalparamfield',
    'paramfield',
    'ParamField',
    'dataclass',
    'paramdataclass',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS ParamField
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ParamField():
    '''
    Like `Field`, except that it allows for a parameterised alternative, `param_factory` to `default_factory`.
    '''
    options: dict;
    param_factory: callable;
    kind: str;

    def __init__(self, **options):
        self.kind = 'single';
        if 'kind' in options:
            self.kind = options['kind'];
            del options['kind'];
        if 'param_factory' in options:
            self.param_factory = options['param_factory'];
            del options['param_factory'];
        self.options = options;

    def create_field(self, name, **params) -> Field:
        '''
        @inputs
        - `name` - name of field;
        - `**params` - keyword arguments presented in __init__ method of class instantiation.

        @returns Field (parameter-initialisation if arguments given)
        '''
        if hasattr(self, 'param_factory') and name in params:
            argument = params[name];
            if self.kind == 'nested':
                assert isinstance(argument, dict), f'Argument `{name}` must be a dict!';
                factory = lambda: self.param_factory.__call__(**argument);
            elif self.kind == 'dict':
                assert isinstance(argument, dict), \
                    f'Argument `{name}` must be a list of dicts!';
                factory = lambda: { key: self.param_factory(item) for key, item in argument.items() };
            elif self.kind == 'list':
                assert isinstance(argument, list), \
                    f'Argument `{name}` must be a list of dicts!';
                factory = lambda: [ self.param_factory(item) for item in argument ];
            elif self.kind == 'nested-dict':
                assert isinstance(argument, dict) and all(isinstance(item, dict) for _, item in argument.items()), \
                    f'Argument `{name}` must be a list of dicts!';
                factory = lambda: { key: self.param_factory(**item) for key, item in argument.items() };
            elif self.kind == 'nested-list':
                assert isinstance(argument, list) and all(isinstance(item, dict) for item in argument), \
                    f'Argument `{name}` must be a list of dicts!';
                factory = lambda: [ self.param_factory(**item) for item in argument ];
            else: #if self.kind == 'single':
                factory = lambda: self.param_factory.__call__(argument)
            return field(**{**self.options, 'default': MISSING, 'default_factory': factory});

        return field(**self.options);

def paramfield(**options) -> ParamField:
    '''
    Extends `field(...)`, by the keyword:

    - `kind` - `'single'` (default) | `nested` | `'list'` | `'dict'` | `'nested-list'` | `'nested-dict'`
    - `param_factory = lambda **params: ...`

    which creates a field that either provides default values based on `default`/`default_factory`,
    or else initialises based on a parameterised input, depending upon `kind`.

    NOTE:
    - use in conjunction with @paramdatacass.
    - can use `default` or `default_factory` in conjunction `param_factory` argument (but, as usual, not both!).
    - if `param_factory` argument is missing, then behaves just like `field`.
    '''
    return ParamField(**options);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DECORATOR @paramdataclass
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def paramdataclass(cls):
    '''
    A decorator which extends `@dataclass.dataclass` by parameterised fields.

    ## Example usage ##

    ```py
    @dataclass
    class Atom():
        element: str = field(default='-');
        number:  int = field(default=-1);

    @paramdataclass
    class Table():
        age:     int       = field(default=28);
        colour:  str       = field(default='red');
        history: List[str] = field(default_factory=lambda: []);
        name:  str         = paramfield(param_factory=lambda parts: '-'.join(name));
        format:  str       = paramfield(kind='nested' param_factory=lambda **item: '+'.join(item.values()));
        rows:    List[Row] = paramfield(kind='nested-list', param_factory=lambda **entry: Atom(**entry));

    x = Table(
        colour = 'blue',
        name   = ['Nikola', 'Tesla'],
        format = dict(charset='utf8', size='A4', font='10pt'),
        rows   = [{'number': 14}, {'element': 'Cu'}, {'element': 'Mg', number: 12}]
    );
    assert x.age == 28;
    assert x.colour == 'blue';
    assert x.history == [];
    assert x.name == 'Nikola-Tesla';
    assert x.format == 'utf8+A4+10pt';
    assert x.values == [Atom(element='-', number=14), Atom(element='Cu', number=-1), Atom(element='Mg', number=12)];
    ```
    '''
    # create method to overwrite cls.__init__:
    def initialise(self, *_, **params):
        # create empty class:
        class cls_:
            pass;
        setattr(cls_, '__annotations__', {});
        ################
        # Loop through attributes of original class
        # - add ordinary attributes, resolving ParamField appropriately.
        # - add type annotations according to original class.
        ################
        types = cls.__dict__.get('__annotations__', {});
        used_keys = [];
        for key in dir(cls):
            if not key.startswith('__'):
                attr = getattr(cls, key);
                if isinstance(attr, ParamField):
                    used_keys.append(key);
                    attr = attr.create_field(key, **params);
                setattr(cls_, key, attr);
                cls_.__annotations__[key] = types[key];
        # now that all ParamField's have been converted to fields, replace by dataclass:
        cls_ = dataclass(cls_);
        # instantiate class:
        C = cls_(*_, **{
            key: value for key, value in params.items() if key not in used_keys
        });
        # transfer over instance:
        for key in dir(C):
            if not key.startswith('__'):
                setattr(self, key, getattr(C, key));
        setattr(self, '__str_temp__', getattr(C, '__str__'));
        return;

    # NOTE: need to force-create this string method, as above method does not suffice:
    def display(self):
        expr = self.__str_temp__();
        class_name = self.__class__.__name__;
        args = re.sub(r'^(.*?)\((.*)\)$', repl=r'\2', string=expr);
        return f'{class_name}({args})';

    # overwrite cls.__init__, cls.__str__, cls.__repr__:
    setattr(cls, '__init__', initialise);
    setattr(cls, '__str__', display);
    setattr(cls, '__repr__', display);
    return cls;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD optionalfield
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def optionalparamfield(**options) -> ParamField:
    '''
    Creates a Field using the Nothing/Some constructors.
    '''
    if 'default' in options:
        options['default'] = Some(options['default']);
    if 'default_factory' in options:
        f = options['default_factory'];
        options['default_factory'] = lambda: Some(f());
    if not('default' in options or 'default_factory' in options):
        options['default_factory'] = lambda: Nothing();
    if 'param_factory' in options:
        f = options['param_factory'];
        options['param_factory'] = lambda *_, **__: Some(f(*_, **__));
    else:
        options['param_factory'] = lambda value: Some(value);
    return paramfield(**options);
