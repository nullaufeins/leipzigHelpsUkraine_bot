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
const COMMANDS = (CONFIG['commands'] || [])
    .map((options) => yaml_to_js_dictionary(options))
    .map((options) => {
        const { match } = options;
        options['match'] = new RegExp(match);
        return options;
    });
const DEFAULT_LANGUAGE = CONFIG['default-language'] || 'en';
const SUPPORTED_LANGUAGES = CONFIG['languages'] || [];
const TRANSLATIONS = new TranslatedTexts(LANGUAGE || {}, DEFAULT_LANGUAGE);

/****************************************************************
 * METHODS
 ****************************************************************/
const COMMAND_PATTERN = /^(.*?)\@(.*)$/;
const strip_botname = (text, botname) => {
    if (COMMAND_PATTERN.test(text)) {
        const _text = text.replace(COMMAND_PATTERN, `$1`).trim();
        const _botname = text.replace(COMMAND_PATTERN, `$2`).trim();
        return { text: _text, botname: _botname, verified: botname == _botname };
    }
    const _text = text.trim();
    return { text: _text, botname: '', verified: true };
}

const get_translation = (lang, text) => (TRANSLATIONS.value(lang, text));
const get_command_by_condition = (condition) => COMMANDS.filter(condition);
const get_command_by_keyword = (text_, botname) => {
    // extract information about bot addressed:
    const { text, verified } = strip_botname(text_, botname);
    if (!verified) return [];
    // condition: bot names must match if command is strict, and keyword must match
    const condition = ({keyword}) => ((!strict || botname == botname_) && (keyword === text));
    return get_command_by_condition(condition);
}
const get_command_by_command = (text_, botname_) => {
    // extract information about bot addressed:
    const { text, botname, verified } = strip_botname(text_, botname_);
    if (!verified) return [];
    // condition: bot names must match if command is strict, and command must match
    const condition = ({match, strict}) => ((!strict || botname == botname_) && match.test(text));
    return get_command_by_condition(condition);
};

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    OPTIONS,
    COMMANDS,
    DEFAULT_LANGUAGE,
    SUPPORTED_LANGUAGES,
    get_command_by_keyword,
    get_command_by_command,
    get_translation
};
