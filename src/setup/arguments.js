/****************************************************************
 * IMPORTS
 ****************************************************************/

const {
    LANGUAGE_PATTERNS,
    DEFAULT_LANGUAGE,
} = require('./config.js');

/****************************************************************
 * METHODS - pattern recognition
 ****************************************************************/

const recognise_language = (arg) => {
    arg = arg || '';
    let lang = undefined;
    Object.entries(LANGUAGE_PATTERNS).some(([key, match]) => {
        if (match.test(arg)) {
            lang = key;
            return true;
        }
    });
    return lang;
}

const recognise_integer = (arg) => {
    try {
        return parseInt(arg || '') || undefined;
    } catch(error) {
        return undefined
    }
}

const recognise_arguments_q_and_a = (args) => {
    const [ arg1, arg2 ] = args;
    let lang = DEFAULT_LANGUAGE;
    let number = recognise_integer(arg1);
    if (number === undefined) {
        number = recognise_integer(arg2) || 1;
        lang = recognise_language(arg1) || DEFAULT_LANGUAGE;
    } else {
        lang = recognise_language(arg2) || DEFAULT_LANGUAGE;
    }
    number = Math.max(number - 1, 0);
    return { number, lang };
}

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    recognise_language,
    recognise_arguments_q_and_a,
};
