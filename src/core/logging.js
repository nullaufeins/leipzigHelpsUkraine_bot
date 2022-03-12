/****************************************************************
 * IMPORTS
 ****************************************************************/

const { sprintf } = require('sprintf-js');
const { split_non_empty_parts } = require('./utils');

/****************************************************************
 * METHODS special error logging
 ****************************************************************/

const SuccessMessageListener = (context, user) => (sprintf(
`[INFO]: Call succeeded. Context + Calling User:
%s
%s`, context, user));

const ErrorMessageListener = (context, user, err) => (sprintf(
`[(non fatal) ERROR]: %s
Context + Calling User:
%s
%s
...continuing silently.`, err, context, user));

const logDebugListener = (context, user, action_taken) => {
    console.debug(`Context of Call:`);
    console.debug(context);
    console.debug(`Called by User:`);
    console.debug(user);
    console.debug(`Action taken:`, action_taken);
};

const logListenerError = (context, user, err) => (console.error(ErrorMessageListener(context, user, err)));
const logListenerErrorSilently = (context, user, err) => (console.log(ErrorMessageListener(context, user, err)));
const logListenerSuccess = (context, user) => (console.log(SuccessMessageListener(context, user)));

/****************************************************************
 * METHODS censoring
 ****************************************************************/

const CENSOR_ATTRIBUTE = '*****';
const CENSOR_DIGITS = '####';

const partiallyCensorMessage = (text) => {
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
    logDebugListener,
    logListenerError,
    logListenerErrorSilently,
    logListenerSuccess,
    CENSOR_ATTRIBUTE,
    CENSOR_DIGITS,
    partiallyCensorMessage,
};
