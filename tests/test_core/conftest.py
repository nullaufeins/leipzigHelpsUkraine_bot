#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from tests.thirdparty.unit import *;

from src.thirdparty.code import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FIXTURES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@fixture(scope='function')
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

@fixture(scope='function')
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

@fixture(scope='function')
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

@fixture(scope='module')
def func1():
    def func(x: str) -> int:
        # force an artificial internal failure:
        if x == '42':
            raise Exception('bug');
        return 1000*int(x);
    return func;

@fixture(scope='module')
def func2a():
    def func() -> float:
        raise Exception('bug');
    return func;

@fixture(scope='module')
def func2b():
    def func() -> float:
        return 789.14;
    return func;

@fixture(scope='module')
def func3a():
    def func() -> str:
        raise Exception('bug');
    return func;

@fixture(scope='module')
def func3b():
    def func() -> str:
        return '789.14';
    return func;
