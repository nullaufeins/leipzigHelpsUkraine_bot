/****************************************************************
 * IMPORTS
 ****************************************************************/

//

/****************************************************************
 * DEFINITIONS
 ****************************************************************/

const yaml_key_to_js_key = (key) => (key.replace(/-/g, '_'));

const yaml_to_js_dictionary = (data, deep = false) => {
    if (!( data.constructor == Object )) return data;
    const revalue = deep ? (value) => (value) : (value) => yaml_to_js_dictionary(value, true);
    const entries = Object.entries(data)
        .map(([key, value]) => ([yaml_key_to_js_key(key), revalue(value)]))
        .map(([key, value]) => ({ [key]: value }));
    return Object.assign({}, ...entries);
}

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    yaml_to_js_dictionary,
};
