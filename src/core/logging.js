/****************************************************************
 * IMPORTS
 ****************************************************************/

const { sprintf } = require('sprintf-js');

/****************************************************************
 * METHODS special error logging
 ****************************************************************/

const ErrorMessageListener = (context, err) => (sprintf(
`Non fatal error caught in context
%s

Details of Exception:
%s

...continuing silently.`, context, err));

const logListenerError = (context, err) => (console.error(ErrorMessageListener(context, err)));
const logListenerErrorSilently = (context, err) => (console.log(ErrorMessageListener(context, err)));

/****************************************************************
 * EXPORTS
 ****************************************************************/

 module.exports = {
    logListenerError,
    logListenerErrorSilently,
};
