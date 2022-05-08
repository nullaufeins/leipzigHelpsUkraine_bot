#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from tests.thirdparty.tests import *;

from src.thirdparty.code import *;
from src.core.utils import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FIXTURES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@fixture(scope='module')
def yaml() -> dict:
    return {
        'first-name': 'Max-Rodriguez',
        'last_name':  'Mustermann',
        'age': 48,
        'keywords': [ 'bio-chemistry', 'gene-editting' ],
        'address': {
            'street-name': 'Hauptstraße',
            'house-number': '78-a',
            'zip': 'SW1100',
        },
        'data': [
            (5.09, 18),
            (-5.9, 1.8),
            (5.97, 0.8),
        ],
        'books': [
            {
                'author-first-name': 'Clive',
                'author-last-name': 'Lewis',
                'title': 'The Chronicles of Narnia - The lion the witch and the wardrobe',
            },
            {
                'author-first-name': 'Joanne',
                'author-last-name': 'Rowling',
                'title': 'Harry Potter - and the goblet of fire',
            },
        ]
    };

@fixture(scope='module')
def yaml_shallow() -> dict:
    return {
        'first_name': 'Max-Rodriguez',
        'last_name':  'Mustermann',
        'age': 48,
        'keywords': [ 'bio-chemistry', 'gene-editting' ],
        'address': {
            'street-name': 'Hauptstraße',
            'house-number': '78-a',
            'zip': 'SW1100',
        },
        'data': [
            (5.09, 18),
            (-5.9, 1.8),
            (5.97, 0.8),
        ],
        'books': [
            {
                'author-first-name': 'Clive',
                'author-last-name': 'Lewis',
                'title': 'The Chronicles of Narnia - The lion the witch and the wardrobe',
            },
            {
                'author-first-name': 'Joanne',
                'author-last-name': 'Rowling',
                'title': 'Harry Potter - and the goblet of fire',
            },
        ]
    };

@fixture(scope='module')
def yaml_deep() -> dict:
    return {
        'first_name': 'Max-Rodriguez',
        'last_name':  'Mustermann',
        'age': 48,
        'keywords': [ 'bio-chemistry', 'gene-editting' ],
        'address': {
            'street_name': 'Hauptstraße',
            'house_number': '78-a',
            'zip': 'SW1100',
        },
        'data': [
            (5.09, 18),
            (-5.9, 1.8),
            (5.97, 0.8),
        ],
        'books': [
            {
                'author_first_name': 'Clive',
                'author_last_name': 'Lewis',
                'title': 'The Chronicles of Narnia - The lion the witch and the wardrobe',
            },
            {
                'author_first_name': 'Joanne',
                'author_last_name': 'Rowling',
                'title': 'Harry Potter - and the goblet of fire',
            },
        ]
    };

def func1(x: str) -> int:
    # force an artificial internal failure:
    if x == '42':
        raise Exception('bug');
    return 1000*int(x);

@wrap_output_as_option
def func2(x: str) -> int:
    return func1(x);

def func3a() -> float:
    raise Exception('bug');

def func3b() -> float:
    return 789.14;

def func4a() -> str:
    raise Exception('bug');

def func4b() -> str:
    return '789.14';

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Test strings
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@mark.usefixtures('test')
def test_split_non_empty_parts(test: TestCase):
    result = split_non_empty_parts('   ');
    test.assertEqual(result, []);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Test numerical
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@mark.usefixtures('test')
def test_int_to_milliseconds(test: TestCase):
    result = int_to_milliseconds(78);
    test.assertEqual(result.seconds, 0);
    test.assertEqual(result.microseconds, 78000);
    result = int_to_milliseconds(15000);
    test.assertEqual(result.seconds, 15);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS - yaml
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@mark.usefixtures('test', 'yaml', 'yaml_deep')
def test_yaml_to_js_dictionary__shallow(test: TestCase, yaml: dict, yaml_shallow: dict):
    test.assertDictEqual(
        yaml_to_js_dictionary(yaml, deep=False),
        yaml_shallow
    );

@mark.usefixtures('test', 'yaml', 'yaml_deep')
def test_yaml_to_js_dictionary__shallow(test: TestCase, yaml: dict, yaml_deep: dict):
    test.assertDictEqual(
        yaml_to_js_dictionary(yaml, deep=True),
        yaml_deep
    );

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS - lists
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@mark.usefixtures('test')
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

@mark.usefixtures('test')
def test_wrap_output_as_option(test: TestCase):
    # check that func set up to fail:
    with assert_raises(Exception):
        func1('not a number');
    with assert_raises(Exception):
        func1('42');
    # check that failures result in Nothing() and successes in Some(...):
    test.assertEqual(func2('not a number'), Nothing(), 'Thrown exceptions should result in Nothing().');
    test.assertEqual(func2('42'), Nothing(), 'Thrown exceptions should result in Nothing().');
    test.assertIsInstance(func2('43'), Some, 'Output should be enapsulated in Some().');
    test.assertEqual(func2('43'), Some(43000));

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TESTS unwrapping
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_unwrap_or_none(test: TestCase):
    # check that func set up to fail/succeed:
    with assert_raises(Exception):
        func3a();
    with does_not_raise():
        func3b();
    # check that outputs are unwrapped as desired:
    test.assertIsNone(unwrap_or_none(func3a));
    test.assertEqual(unwrap_or_none(func3b), 789.14);

def test_unwrap_or_string(test: TestCase):
    # check that func set up to fail/succeed:
    with assert_raises(Exception):
        func4a();
    with does_not_raise():
        func4b();
    # check that outputs are unwrapped as desired:
    test.assertEqual(unwrap_or_string(func4a, default='---'), '---');
    test.assertEqual(unwrap_or_string(func4b, default='---'), '789.14');
