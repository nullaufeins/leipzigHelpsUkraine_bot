/****************************************************************
 * IMPORTS
 ****************************************************************/

yaml = require('js-yaml');
fs = require('fs-extra');
const { yaml_to_js_dictionary } = require.main.require('./core/utils.js');
const { TranslatedTexts } = require.main.require('./classes/language.js');

/****************************************************************
 * CONSTANTS - extract from data assets + app configuration
 ****************************************************************/

const LANGUAGE = yaml.load(fs.readFileSync('assets/language.yaml', 'utf8'));
const CONFIG = yaml.load(fs.readFileSync('src/setup/config.yaml', 'utf8'));

const default_lang = CONFIG['default-language'];
const OPTIONS = yaml_to_js_dictionary(CONFIG['options'] || {} || {debug: false, timeout: 10*1000, timeout_menu: 60*1000});
const COMMANDS = CONFIG['commands'] || {};
const SUPPORTED_LANGUAGES = CONFIG['languages'] || [];
const TRANSLATIONS = new TranslatedTexts(data=LANGUAGE || {}, default_lang=default_lang);

/****************************************************************
 * METHODS
 ****************************************************************/

const get_translation = (lang, text) => (TRANSLATIONS.value(lang, text));
const get_command_by_condition = (condition) => COMMANDS.filter(condition);
const get_command_by_keyword = (text) => get_command_by_condition(({keyword}) => (keyword === text));
const get_command_by_command = (text) => get_command_by_condition(({command}) => (command === text));

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    OPTIONS,
    COMMANDS,
    SUPPORTED_LANGUAGES,
    get_command_by_keyword,
    get_command_by_command,
    get_translation
};
