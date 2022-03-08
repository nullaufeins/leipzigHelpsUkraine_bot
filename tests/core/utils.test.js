/****************************************************************
 * IMPORTS
 ****************************************************************/

const assert = require('assert');
const expect = require('expect');

const {
    CombineErrors,
    split_non_empty_parts,
    take_one,
    yaml_to_js_dictionary,
    try_action1_silently_then_perform_action2,
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

describe('Perform actions1 silently then action2 and combine errors', () => {
    it('should carry out both actions and not return errors', async () => {
        let action1_done = false;
        let action2_done = false;
        let action1 = () => {
            action1_done = true;
            return Promise.resolve('value1');
        };
        let action2 = () => {
            action2_done = true;
            return Promise.resolve('value2');
        };
        let value = await try_action1_silently_then_perform_action2(action1, action2);
        expect(value).toEqual('value2')
        expect(action1_done).toEqual(true);
        expect(action2_done).toEqual(true);
    });

    it('should ignore 1st error, carry out action2 and throw error1', async () => {
        let action1_done = false;
        let action2_done = false;
        let action1 = () => {
            action1_done = true;
            return Promise.reject('Something went wrong!');
        };
        let action2 = () => {
            action2_done = true;
            return Promise.resolve('value2');
        };
        let err = await try_action1_silently_then_perform_action2(action1, action2)
            .then((_) => {})
            .catch((_) => _);
        expect(err).toEqual('Something went wrong!')
        expect(action1_done).toEqual(true);
        expect(action2_done).toEqual(true);
    });

    it('should ignore 1st error, carry out action2 and throw both errors combined', async () => {
        let action1_done = false;
        let action2_done = false;
        let action1 = () => {
            action1_done = true;
            return Promise.reject('Something went wrong!');
        };
        let action2 = () => {
            action2_done = true;
            return Promise.reject('Something else went wrong!');
        };
        let err = await try_action1_silently_then_perform_action2(action1, action2)
            .then((_) => {})
            .catch((_) => _);
        expect(err).toEqual(CombineErrors('Something went wrong!', 'Something else went wrong!'));
        expect(action1_done).toEqual(true);
        expect(action2_done).toEqual(true);
    });
});
