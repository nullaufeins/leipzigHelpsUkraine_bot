/****************************************************************
 * IMPORTS
 ****************************************************************/

//

/****************************************************************
 * DEFINITIONS
 ****************************************************************/

const yaml_key_to_js_key = (key) => (key.replace(/-/g, '_'));

const yaml_to_js_dictionary = (data) => {
    let entries = Object.entries(data);
    entries = entries.map(([key, value]) => ({[yaml_key_to_js_key(key)]: value}));
    return Object.assign({}, ...entries);
}

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    yaml_to_js_dictionary,
};
