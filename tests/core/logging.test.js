/****************************************************************
 * IMPORTS
 ****************************************************************/

const assert = require('assert');

const {
    CENSOR_ATTRIBUTE,
    CENSOR_DIGITS,
    partiallyCensorMessage,
} = require('../../src/core/logging.js');

/****************************************************************
 * TESTS
 ****************************************************************/

describe('Censor texts', () => {
    it('Should fully censor long messages', () => {
        let msg = '';

        msg = `this is a long message
        that spans 2 lines`;
        assert.equal(partiallyCensorMessage(msg), CENSOR_ATTRIBUTE);

        msg = `this is a long message
        that spans multiples lines

        like this`;
        assert.equal(partiallyCensorMessage(msg), CENSOR_ATTRIBUTE);

        msg = `nothing to see here`;
        assert.equal(partiallyCensorMessage(msg), msg);
    });

    it('Should censor sensitive information', () => {
        let msg = '';

        msg = `my email is chancellor@bmi.de`;
        assert.equal(partiallyCensorMessage(msg), `my email is ${CENSOR_ATTRIBUTE}`);

        msg = `my website is http://xkcd.com check it out`;
        assert.equal(partiallyCensorMessage(msg), `my website is ${CENSOR_ATTRIBUTE} check it out`);
    });

    it('Should censor numbers and not betray length', () => {
        let msg = '';

        msg = `my credit card number is ax912039810`;
        assert.equal(partiallyCensorMessage(msg), `my credit card number is ax${CENSOR_DIGITS}`);

        msg = `my credit card number is 0192830810238018239018209380`;
        assert.equal(partiallyCensorMessage(msg), `my credit card number is ${CENSOR_DIGITS}`);

        msg = `my weight is 65.3 kg`;
        assert.equal(partiallyCensorMessage(msg), `my weight is ${CENSOR_DIGITS} kg`);

        msg = `my weight is 51 kg`;
        assert.equal(partiallyCensorMessage(msg), `my weight is ${CENSOR_DIGITS} kg`);
    });

    it('Should non censor non-sensitive parts of potential commands', () => {
        let msg = '';

        msg = `@botname help en`;
        assert.equal(partiallyCensorMessage(msg), `${CENSOR_ATTRIBUTE} help en`);

        msg = `/help @botname`;
        assert.equal(partiallyCensorMessage(msg), `/help ${CENSOR_ATTRIBUTE}`);

        msg = `/help@botname`;
        assert.equal(partiallyCensorMessage(msg), `/help ${CENSOR_ATTRIBUTE}`);
    });

    it('Should censor non-plain parts', () => {
        let msg = '';

        msg = `#trend@botname test`;
        assert.equal(partiallyCensorMessage(msg), `${CENSOR_ATTRIBUTE} test`);

        msg = `apple cat/mouse house ICE-Zug node_js x^y "blabla"`;
        assert.equal(partiallyCensorMessage(msg), `apple ${CENSOR_ATTRIBUTE} house ICE-Zug node_js ${CENSOR_ATTRIBUTE} ${CENSOR_ATTRIBUTE}`);
    });
});
