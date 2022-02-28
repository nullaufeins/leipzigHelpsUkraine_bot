/****************************************************************
 * IMPORTS
 ****************************************************************/

yaml = require('js-yaml');
fs = require('fs-extra');
const { yaml_to_js_dictionary } = require.main.require('./core/utils.js');

/****************************************************************
 * DEFINITIONS
 ****************************************************************/

const LANGUAGE = yaml.load(fs.readFileSync('../assets/language.yaml', 'utf8'));
let CONFIG = Object.assign(
    yaml.load(fs.readFileSync('setup/config.yaml', 'utf8')),
    { 'texts': LANGUAGE }
);
const OPTIONS = yaml_to_js_dictionary(CONFIG['options'] || {} || {debug: false, timeout: 10*1000, timeout_menu: 60*1000});

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    CONFIG,
    OPTIONS
};
