/****************************************************************
 * IMPORTS
 ****************************************************************/

const assert = require('assert');

const {
    split_non_empty_parts,
    take_one,
    yaml_to_js_dictionary,
} = require('../../src/core/utils.js');

/****************************************************************
 * TESTS
 ****************************************************************/

describe('String splitter', () => {
    it('should return empty array', () => {
        assert.deepEqual(split_non_empty_parts(''), []);
        assert.deepEqual(split_non_empty_parts('    '), []);
    });

    it('should return correct numbers of arguments', () => {
        assert.deepEqual(split_non_empty_parts('katze'), ['katze']);
        assert.deepEqual(split_non_empty_parts('cat dog-mouse horse'), ['cat', 'dog-mouse', 'horse']);
        assert.deepEqual(split_non_empty_parts('/help me obiwan Kenobi!'), ['/help', 'me', 'obiwan', 'Kenobi!']);
    });

    it('should not be fussy about spaces', () => {
        assert.deepEqual(split_non_empty_parts('    cat dog-mouse horse'), ['cat', 'dog-mouse', 'horse']);
        assert.deepEqual(split_non_empty_parts('cat dog-mouse horse    '), ['cat', 'dog-mouse', 'horse']);
        assert.deepEqual(split_non_empty_parts('     cat dog-mouse horse    '), ['cat', 'dog-mouse', 'horse']);
        assert.deepEqual(split_non_empty_parts('cat    dog-mouse   horse'), ['cat', 'dog-mouse', 'horse']);
        assert.deepEqual(split_non_empty_parts('     cat    dog-mouse   horse    '), ['cat', 'dog-mouse', 'horse']);
    });
});

describe('Taking arguments from arrays', () => {
    it('should take no arguments when array empty', () => {
        assert.deepEqual(take_one([]), [undefined, []]);
    });

    it('should leave behind empty array when array has 1 element', () => {
        assert.deepEqual(take_one(['cat']), ['cat', []]);
    });

    it('should extract first and leave the rest', () => {
        assert.deepEqual(take_one(['cat', 'dog', 'mouse']), ['cat', ['dog', 'mouse']]);
        // assert.deepEqual(take_one(['cat', 'cat', 'dog', 'mouse']), ['cat', ['cat', 'dog', 'mouse']]);
        // assert.deepEqual(take_one([897, 'cat', 'dog', 'mouse']), [897, ['cat', 'dog', 'mouse']]);
    });
});

describe('Convert dictionary keys', () => {
    it('should not convert values', () => {
        assert.deepEqual(yaml_to_js_dictionary({name: 'Ludwig-Boltzmann _4'}), {name: 'Ludwig-Boltzmann _4'});
        assert.notDeepEqual(yaml_to_js_dictionary({name: 'Ludwig-Boltzmann _4'}), {name: 'Ludwig_Boltzmann _4'});
    });

    it('should convert keys with - to _', () => {
        assert.deepEqual(yaml_to_js_dictionary({'max-delay-time_1': 10000}), {max_delay_time_1: 10000});
        assert.deepEqual(yaml_to_js_dictionary({
            colour: 'red',
            age_limit: 70,
            'max-delay': 10000
        }), {
            colour: 'red',
            age_limit: 70,
            max_delay: 10000
        });
    });

    it('should perform deep conversion of nested dictionaries', () => {
        assert.deepEqual(
            yaml_to_js_dictionary({'named-constants': {'physical-constants': { 'atomic-numbers': {Hg: 80, Ag: 47}}}}, true),
            {named_constants: {physical_constants: { atomic_numbers: {Hg: 80, Ag: 47}}}}
        );
        assert.deepEqual(
            yaml_to_js_dictionary({
                system: ['mercury', 'venus', 'earth', 'mars'],
                'time-parameters': {'max-delay': 78}
            }, true),
            {
                system: ['mercury', 'venus', 'earth', 'mars'],
                'time_parameters': { max_delay: 78 }
            }
        );
    });
});
