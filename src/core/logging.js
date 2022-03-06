/****************************************************************
 * IMPORTS
 ****************************************************************/

const { sprintf } = require('sprintf-js');
const { split_non_empty_parts } = require('./utils');

/****************************************************************
 * METHODS special error logging
 ****************************************************************/

const ErrorMessageListener = (context, err, full_censor) => (sprintf(
`Non fatal error caught in context
%s

Details of Exception:
%s

...continuing silently.`, context.toCensoredString(full_censor), err));

const logListenerError = (context, err, full_censor) => (console.error(ErrorMessageListener(context, err, full_censor)));
const logListenerErrorSilently = (context, err, full_censor) => (console.log(ErrorMessageListener(context, err, full_censor)));

/****************************************************************
 * METHODS censoring
 ****************************************************************/

const CENSOR_ATTRIBUTE = '*****';
const CENSOR_DIGITS = '####';

const censorMessage = (text) => {
    text = (text || '').trim();

    // apply full censorship if text contains more than one line:
    if (/[\r\n]/.test(text)) {
        return CENSOR_ATTRIBUTE;
    }

    // replace occurrences of the form /abc@xyz with /abc @xyz:
    text = text.replace(/(^|\s)(\/[\w_]+)(\@\w)/g, `$1$2 $3`);

    // split into parts and check which parts need censoring:
    let words = split_non_empty_parts(text);
    for (let k=0; k < words.length; k++) {
        let word = words[k];

        // fully censor all 'words' that contain non-alphanumeric (excl. some signs that could occur in commands):
        if (/(?![-_\.\/])\W|.(?![-_\.])\W/.test(word)) {
            words[k] = CENSOR_ATTRIBUTE
            continue;
        }
        // replace all numerical values by #:
        words[k] = word.replace(/(\d*[\.\,]\d+|\d+[\.\,]\d*|\d+)/g, CENSOR_DIGITS);
    }
    text = words.join(' ');
    return text;
}

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    CENSOR_ATTRIBUTE,
    CENSOR_DIGITS,
    censorMessage,
    logListenerError,
    logListenerErrorSilently,
};
