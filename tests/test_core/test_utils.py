#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.code import *;
from src.thirdparty.types import *;
from tests.thirdparty.unit import *;

from src.core.utils import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FIXTURES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Test strings
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_split_non_empty_parts(test: TestCase):
    result = split_non_empty_parts('   ');
    test.assertEqual(result, []);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Test numerical
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_int_to_milliseconds(test: TestCase):
    result = int_to_milliseconds(78);
    test.assertEqual(result.seconds, 0);
    test.assertEqual(result.microseconds, 78000);
    result = int_to_milliseconds(15000);
    test.assertEqual(result.seconds, 15);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS - yaml
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@mark.usefixtures('yaml', 'yaml_deep')
def test_yaml_to_js_dictionary__shallow(test: TestCase, yaml: dict, yaml_shallow: dict):
    test.assertDictEqual(
        yaml_to_js_dictionary(yaml, deep=False),
        yaml_shallow
    );

@mark.usefixtures('yaml', 'yaml_deep')
def test_yaml_to_js_dictionary__shallow(test: TestCase, yaml: dict, yaml_deep: dict):
    test.assertDictEqual(
        yaml_to_js_dictionary(yaml, deep=True),
        yaml_deep
    );

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS - lists
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_flatten(test: TestCase):
    test.assertListEqual(flatten(), []);
    test.assertListEqual(flatten([]), []);
    test.assertListEqual(flatten([], []), []);
    test.assertListEqual(flatten(['a', 'bc']), ['a', 'bc']);
    test.assertListEqual(flatten(['a', 'bc'], []), ['a', 'bc']);
    test.assertListEqual(flatten(
        [],
        [1, 7],
        ['a', 'b', 'c'],
        [8],
        [],
        [-1],
        []
    ), [1, 7, 'a', 'b', 'c', 8, -1]);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TESTS something, nothing
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@mark.usefixtures('func1')
def test_wrap_output_as_option(test: TestCase, func1: Callable[[str], int]):
    # create decorated function:
    @wrap_output_as_option
    def func_decorated(x: str) -> int:
        '''
        Like func1, but wrapped.
        '''
        return func1(x);
    # check that func set up to fail:
    with assert_raises(Exception):
        func1('not a number');
    with assert_raises(Exception):
        func1('42');
    # check that failures result in Nothing() and successes in Some(...):
    test.assertEqual(func_decorated('not a number'), Nothing(), 'Thrown exceptions should result in Nothing().');
    test.assertEqual(func_decorated('42'), Nothing(), 'Thrown exceptions should result in Nothing().');
    test.assertIsInstance(func_decorated('43'), Some, 'Output should be enapsulated in Some().');
    test.assertEqual(func_decorated('43'), Some(43000));

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TESTS unwrapping
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@mark.usefixtures('func2a', 'func2b')
def test_unwrap_or_none(test: TestCase, func2a: Callable[[], float], func2b:  Callable[[], float]):
    # check that func set up to fail/succeed:
    with assert_raises(Exception):
        func2a();
    with does_not_raise():
        func2b();
    # check that outputs are unwrapped as desired:
    test.assertIsNone(unwrap_or_none(func2a));
    test.assertEqual(unwrap_or_none(func2b), 789.14);

@mark.usefixtures('func3a', 'func3b')
def test_unwrap_or_string(test: TestCase, func3a: Callable[[], str], func3b:  Callable[[], str]):
    # check that func set up to fail/succeed:
    with assert_raises(Exception):
        func3a();
    with does_not_raise():
        func3b();
    # check that outputs are unwrapped as desired:
    test.assertEqual(unwrap_or_string(func3a, default='---'), '---');
    test.assertEqual(unwrap_or_string(func3b, default='---'), '789.14');
