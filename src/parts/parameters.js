/****************************************************************
 * IMPORTS
 ****************************************************************/

const { CONFIG } = require.main.require('./setup/config.js');
const { TranslatedTexts } = require.main.require('./classes/language.js');

/****************************************************************
 * DEFINITIONS
 ****************************************************************/

const COMMANDS = CONFIG['commands'] || {};
const SUPPORTED_LANGUAGES = CONFIG['languages'] || [];
const TRANSLATIONS = new TranslatedTexts(data=CONFIG['texts'] || {}, default_lang='en');

const get_command_by_condition = (condition) => COMMANDS.filter(condition);
const get_command_by_keyword = (text) => get_command_by_condition(({keyword}) => (keyword === text));
const get_command_by_command = (text) => get_command_by_condition(({command}) => (command === text));

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    COMMANDS,
    get_command_by_keyword,
    get_command_by_command,
    SUPPORTED_LANGUAGES,
    TRANSLATIONS
};
