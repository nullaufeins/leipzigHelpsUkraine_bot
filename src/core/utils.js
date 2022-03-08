/****************************************************************
 * IMPORTS
 ****************************************************************/

const { sprintf } = require('sprintf-js');

/****************************************************************
 * METHODS - strings, arrays
 ****************************************************************/

const split_non_empty_parts = (text) => {
    text = text.trim();
    return text === '' ? [] : text.split(/\s+/);
}

const take_one = (X) => ([X[0], X.slice(1)]);

/****************************************************************
 * METHODS errors
 ****************************************************************/

const CombineErrors = (err1, err2) => (sprintf(`%s %s`, err1, err2));

/****************************************************************
 * METHODS - dict
 ****************************************************************/

const yaml_key_to_js_key = (key) => (key.replace(/-/g, '_'));

const yaml_to_js_dictionary = (data, deep = false) => {
    if (!( data.constructor == Object )) return data;
    const revalue = deep ? (value) => yaml_to_js_dictionary(value, true) : (value) => (value);
    const entries = Object.entries(data)
        .map(([key, value]) => ([yaml_key_to_js_key(key), revalue(value)]))
        .map(([key, value]) => ({ [key]: value }));
    return Object.assign({}, ...entries);
}

/****************************************************************
 * METHODS - promises/async methods
 ****************************************************************/

/********
 * This allows for a complex chain of promises:
 *
 * - attempt action1
 *     - if succeeds: perform action2.
 *     - if fails with err1:
 *         - attempt action2
 *         - throw err1 + potential errors from action2
 ********/
 const try_action1_silently_then_perform_action2 = async(action1, action2) => {
    return action1()
        .catch((err1) => {
            return action2()
                .catch((err2) => {throw CombineErrors(err1, err2)})
                .then(() => {throw err1});
        })
        .then(action2);
}

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    CombineErrors,
    split_non_empty_parts,
    take_one,
    yaml_to_js_dictionary,
    try_action1_silently_then_perform_action2,
};
