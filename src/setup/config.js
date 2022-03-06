/****************************************************************
 * IMPORTS
 ****************************************************************/

const yaml = require('js-yaml');
const fs = require('fs-extra');
const { yaml_to_js_dictionary } = require('./../core/utils.js');
const { TranslatedTexts } = require('./../classes/language.js');

/****************************************************************
 * CONSTANTS - extract from data assets + app configuration
 ****************************************************************/

const LANGUAGE = yaml.load(fs.readFileSync('assets/language.yaml', 'utf8'));
const CONFIG = yaml.load(fs.readFileSync('setup/config.yaml', 'utf8'));

const OPTIONS = yaml_to_js_dictionary(
    CONFIG['options'] || {} || {
        debug:          false,
        full_censor:    true,
        show_side_menu: false,
        listen_to_text: false,
        delete_calls:   false,
        message_expiry: 10*1000,
        timeout:        10*1000,
        timeout_menu:   60*1000
    }, true);
const COMMANDS = (CONFIG['commands'] || [])
    .map((options) => yaml_to_js_dictionary(options, true))
    .map((options) => {
        const { aspects } = options;
        const { match } = aspects;
        aspects.match = new RegExp(match);
        return options;
    });

const DEFAULT_LANGUAGE = CONFIG['default-language'] || 'en';
const LANGUAGE_PATTERNS = Object.assign({},
    ...Object.entries(CONFIG['languages'] || {})
        .map(([key, value]) => ({[key]: new RegExp(value)}))
    );
const SUPPORTED_LANGUAGES = Object.keys(LANGUAGE_PATTERNS);
const TRANSLATIONS = new TranslatedTexts(LANGUAGE || {}, DEFAULT_LANGUAGE);

/****************************************************************
 * METHODS
 ****************************************************************/

const get_translation = (lang, text) => (TRANSLATIONS.value(lang, text));

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    OPTIONS,
    COMMANDS,
    DEFAULT_LANGUAGE,
    LANGUAGE_PATTERNS,
    SUPPORTED_LANGUAGES,
    get_translation
};
