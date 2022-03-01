/****************************************************************
 * IMPORTS
 ****************************************************************/

const yaml = require('js-yaml');
const fs = require('fs-extra');
const { yaml_to_js_dictionary } = require.main.require('./src/core/utils.js');
const { TranslatedTexts } = require.main.require('./src/classes/language.js');

/****************************************************************
 * CONSTANTS - extract from data assets + app configuration
 ****************************************************************/

const LANGUAGE = yaml.load(fs.readFileSync('assets/language.yaml', 'utf8'));
const CONFIG = yaml.load(fs.readFileSync('src/setup/config.yaml', 'utf8'));

const OPTIONS = yaml_to_js_dictionary(CONFIG['options'] || {} || {debug: false, timeout: 10*1000, timeout_menu: 60*1000});
const COMMANDS = (CONFIG['commands'] || []).map((options) => yaml_to_js_dictionary(options));
const SUPPORTED_LANGUAGES = CONFIG['languages'] || [];
const TRANSLATIONS = new TranslatedTexts(LANGUAGE || {}, CONFIG['default-language'] || 'en');

/****************************************************************
 * METHODS
 ****************************************************************/

const get_translation = (lang, text) => (TRANSLATIONS.value(lang, text));
const get_command_by_condition = (condition) => COMMANDS.filter(condition);
const get_command_by_keyword = (text) => get_command_by_condition(({keyword}) => (keyword === text));
const get_command_by_command = (text) => {
    const cmd = text.replace(/^(.*?)\@.*$/, `$1`);
    return get_command_by_condition(({command}) => (command === cmd));
};

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
