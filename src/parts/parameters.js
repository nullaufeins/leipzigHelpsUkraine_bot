/****************************************************************
 * IMPORTS
 ****************************************************************/

const { CONFIG } = require.main.require('./settings/config.js');
const { TranslatedTexts } = require.main.require('./classes/language.js');

/****************************************************************
 * DEFINITIONS
 ****************************************************************/

const COMMANDS = CONFIG['commands'] || {};
const SUPPORTED_LANGUAGES = CONFIG['languages'] || [];
const TRANSLATIONS = new TranslatedTexts(data=CONFIG['texts'] || {}, default_lang='en');

function get_command_by_keyword(text) {
    return COMMANDS.filter((option) => (option.keyword == text));
};

function get_command_by_command(cmd) {
    return COMMANDS.filter((option) => (option.command == cmd));
};

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
