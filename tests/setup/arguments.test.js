/****************************************************************
 * IMPORTS
 ****************************************************************/

const assert = require('assert');

const { DEFAULT_LANGUAGE, } = require('../../src/setup/config.js');
const {
    recognise_language,
    recognise_arguments_q_and_a,
} = require('../../src/setup/arguments.js');

/****************************************************************
 * TESTS
 ****************************************************************/

describe('Recognition of language codes', () => {
    it('should recognise certain different codes properly', () => {
        assert.equal(recognise_language('deu'), 'de');
        assert.equal(recognise_language('ukr'), 'uk');
        assert.equal(recognise_language('ua'), 'uk');
    });

    it('should treat unrecognisable codes as default language', () => {
        assert.equal(recognise_language('xxxxxxx'), undefined);
        assert.equal(recognise_language('xxxxxxx') || DEFAULT_LANGUAGE, DEFAULT_LANGUAGE);
    });
});

describe('Recognition of 2-argument recognition for Q & A scheme', () => {
    it('should return defaults for empty args', () => {
        assert.deepEqual(recognise_arguments_q_and_a([]), {number: 0, lang: DEFAULT_LANGUAGE});
    });

    it('should treat single numerical arg as number', () => {
        assert.deepEqual(recognise_arguments_q_and_a(['897']), {number: 896, lang: DEFAULT_LANGUAGE});
        assert.deepEqual(recognise_arguments_q_and_a(['-5']), {number: 0, lang: DEFAULT_LANGUAGE});
    });

    it('should treat single non-numerical arg as language', () => {
        assert.deepEqual(recognise_arguments_q_and_a(['de']), {number: 0, lang: 'de'});
        assert.deepEqual(recognise_arguments_q_and_a(['ua']), {number: 0, lang: 'uk'});
        assert.deepEqual(recognise_arguments_q_and_a(['something']), {number: 0, lang: DEFAULT_LANGUAGE});
    });

    it('should treat single non-numerical arg as language', () => {
        assert.deepEqual(recognise_arguments_q_and_a(['de']), {number: 0, lang: 'de'});
        assert.deepEqual(recognise_arguments_q_and_a(['ua']), {number: 0, lang: 'uk'});
        assert.deepEqual(recognise_arguments_q_and_a(['xxxxxxx']), {number: 0, lang: DEFAULT_LANGUAGE});
    });

    it('should handle [number, lang] correctly', () => {
        assert.deepEqual(recognise_arguments_q_and_a(['4', 'de']), {number: 3, lang: 'de'});
        assert.deepEqual(recognise_arguments_q_and_a(['4', 'xxxx']), {number: 3, lang: DEFAULT_LANGUAGE});
        assert.deepEqual(recognise_arguments_q_and_a(['-2981', 'de']), {number: 0, lang: 'de'});
        assert.deepEqual(recognise_arguments_q_and_a(['-2981', 'xxxx']), {number: 0, lang: DEFAULT_LANGUAGE});
    });

    it('should handle [lang, number] correctly', () => {
        assert.deepEqual(recognise_arguments_q_and_a(['de', '4']), {number: 3, lang: 'de'});
        assert.deepEqual(recognise_arguments_q_and_a(['xxxx', '4']), {number: 3, lang: DEFAULT_LANGUAGE});
        assert.deepEqual(recognise_arguments_q_and_a(['de', '-2981']), {number: 0, lang: 'de'});
        assert.deepEqual(recognise_arguments_q_and_a(['xxxx', '-2981']), {number: 0, lang: DEFAULT_LANGUAGE});
    });

    it('should handle [lang, non-number] correctly', () => {
        assert.deepEqual(recognise_arguments_q_and_a(['de', 'x0984e']), {number: 0, lang: 'de'});
        assert.deepEqual(recognise_arguments_q_and_a(['de', 'uk']), {number: 0, lang: 'de'});
        assert.deepEqual(recognise_arguments_q_and_a(['xxxxx', 'uk']), {number: 0, lang: DEFAULT_LANGUAGE});
    });
});
