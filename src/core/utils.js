/****************************************************************
 * IMPORTS
 ****************************************************************/

//

/****************************************************************
 * METHODS - strings, arrays
 ****************************************************************/

const split_non_empty_parts = (text) => {
    text = text.trim();
    return text === '' ? [] : text.split(/\s+/);
}

const take_one = (X) => ([X[0], X.slice(1)]);

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
 * EXPORTS
 ****************************************************************/

module.exports = {
    split_non_empty_parts,
    take_one,
    yaml_to_js_dictionary,
};
